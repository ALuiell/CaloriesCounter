from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, time

from app.db.database import Database
from app.schemas.nutrition import CalculationResult, RecognizedItem
from app.services.normalization import normalize_product_name
from app.services.parser import parse_food_message
from app.services.profile import DailyNutritionTargets, ProfileService


class NutritionService:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.profile_service = ProfileService(database)

    def process_message(self, telegram_id: int, message_text: str) -> CalculationResult:
        parsed_items = parse_food_message(message_text)
        result = CalculationResult(
            assistant_enabled=(
                self.profile_service.is_assistant_enabled(telegram_id)
                and self.profile_service.has_complete_profile(telegram_id)
            )
        )

        for item in parsed_items:
            if not item.product_text or item.weight_g <= 0:
                result.unrecognized_items.append(item.raw_item_text)
                continue

            product = self._find_product(item.product_text)
            if product is None:
                result.unrecognized_items.append(item.raw_item_text)
                continue

            multiplier = item.weight_g / 100.0
            result.recognized_items.append(
                RecognizedItem(
                    product_id=product["id"],
                    raw_item_text=item.raw_item_text,
                    product_text=item.product_text,
                    display_name=product["name_ru"],
                    weight_g=item.weight_g,
                    calories=product["calories_per_100g"] * multiplier,
                    protein_g=product["protein_per_100g"] * multiplier,
                    fat_g=product["fat_per_100g"] * multiplier,
                    carbs_g=product["carbs_per_100g"] * multiplier,
                )
            )
        return result

    def store_entries(self, telegram_id: int, items: Iterable[RecognizedItem]) -> None:
        user_id = self.profile_service.get_user_id(telegram_id)
        now = self.database.now_iso()
        with self.database.connection() as conn:
            for item in items:
                conn.execute(
                    """
                    INSERT INTO food_entries (
                        user_id,
                        product_id,
                        raw_item_text,
                        product_text,
                        weight_g,
                        calories,
                        protein_g,
                        fat_g,
                        carbs_g,
                        consumed_at,
                        created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        item.product_id,
                        item.raw_item_text,
                        item.product_text,
                        item.weight_g,
                        item.calories,
                        item.protein_g,
                        item.fat_g,
                        item.carbs_g,
                        now,
                        now,
                    ),
                )

    def get_today_summary(self, telegram_id: int) -> dict[str, float | int]:
        user_id = self.profile_service.get_user_id(telegram_id)
        now = datetime.now(self.database.timezone)
        day_start = datetime.combine(now.date(), time.min, tzinfo=self.database.timezone).isoformat()
        day_end = now.isoformat()

        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT
                    COUNT(*) AS count,
                    COALESCE(SUM(calories), 0) AS calories,
                    COALESCE(SUM(protein_g), 0) AS protein_g,
                    COALESCE(SUM(fat_g), 0) AS fat_g,
                    COALESCE(SUM(carbs_g), 0) AS carbs_g
                FROM food_entries
                WHERE user_id = ? AND consumed_at >= ? AND consumed_at <= ?
                """,
                (user_id, day_start, day_end),
            ).fetchone()
        return {
            "count": int(row["count"]),
            "calories": float(row["calories"]),
            "protein_g": float(row["protein_g"]),
            "fat_g": float(row["fat_g"]),
            "carbs_g": float(row["carbs_g"]),
        }

    def search_products(self, query: str, limit: int = 10) -> list[str]:
        normalized = normalize_product_name(query)
        if not normalized:
            return []

        pattern = f"%{normalized}%"
        with self.database.connection() as conn:
            rows = conn.execute(
                """
                SELECT name_ru
                FROM (
                    SELECT p.name_ru AS name_ru
                    FROM products p
                    WHERE p.is_active = 1 AND p.normalized_name_ru LIKE ?

                    UNION

                    SELECT p.name_ru AS name_ru
                    FROM product_aliases pa
                    JOIN products p ON p.id = pa.product_id
                    WHERE p.is_active = 1 AND pa.normalized_alias LIKE ?
                )
                ORDER BY name_ru
                LIMIT ?
                """,
                (pattern, pattern, limit),
            ).fetchall()
        return [str(row["name_ru"]) for row in rows]

    def format_calc_reply(self, result: CalculationResult) -> str:
        parts: list[str] = []
        if result.recognized_items:
            parts.append("Посчитано:")
            parts.extend(self._format_recognized_item(item) for item in result.recognized_items)
            parts.append("")

        if result.unrecognized_items:
            parts.append("Не удалось распознать:")
            parts.extend(f"- {item}" for item in result.unrecognized_items)
            parts.append("")

        if result.recognized_items:
            parts.append(
                self._format_total_block(
                    result.total_calories,
                    result.total_protein,
                    result.total_fat,
                    result.total_carbs,
                )
            )
        else:
            parts.append(
                "Ничего не удалось посчитать.\n"
                "Используй формат: <code>продукт + граммы</code>\n"
                "Пример: <code>гречка 120, курица 180</code>"
            )
        return "\n".join(parts).strip()

    def format_assistant_reply(
        self,
        result: CalculationResult,
        today: dict[str, float | int],
        targets: DailyNutritionTargets,
    ) -> str:
        base = self.format_calc_reply(result)
        if not result.recognized_items:
            return base
        return f"{base}\n\n{self._format_today_block(today)}\n\n{self._format_targets_block(targets)}"

    def format_today_with_targets(
        self,
        today: dict[str, float | int],
        targets: DailyNutritionTargets,
    ) -> str:
        return f"{self._format_today_block(today)}\n\n{self._format_targets_block(targets)}"

    def _find_product(self, product_text: str):
        normalized = normalize_product_name(product_text)
        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT p.*
                FROM products p
                WHERE p.normalized_name_ru = ? AND p.is_active = 1
                """,
                (normalized,),
            ).fetchone()
            if row is not None:
                return row

            row = conn.execute(
                """
                SELECT p.*
                FROM product_aliases pa
                JOIN products p ON p.id = pa.product_id
                WHERE pa.normalized_alias = ? AND p.is_active = 1
                LIMIT 1
                """,
                (normalized,),
            ).fetchone()
            return row

    @staticmethod
    def _format_total_block(calories: float, protein: float, fat: float, carbs: float) -> str:
        return (
            "Итого:\n"
            f"{round(calories)} ккал\n"
            f"Белки: {NutritionService._format_number(protein)} г\n"
            f"Жиры: {NutritionService._format_number(fat)} г\n"
            f"Углеводы: {NutritionService._format_number(carbs)} г"
        )

    @staticmethod
    def _format_today_block(today: dict[str, float | int]) -> str:
        return (
            "За сегодня:\n"
            f"{round(float(today['calories']))} ккал\n"
            f"Белки: {NutritionService._format_number(float(today['protein_g']))} г\n"
            f"Жиры: {NutritionService._format_number(float(today['fat_g']))} г\n"
            f"Углеводы: {NutritionService._format_number(float(today['carbs_g']))} г"
        )

    @staticmethod
    def _format_targets_block(targets: DailyNutritionTargets) -> str:
        return (
            "Профиль:\n"
            f"BMR: <b>{round(targets.bmr)}</b> ккал\n"
            f"TDEE: <b>{round(targets.tdee)}</b> ккал\n"
            f"Активность по умолчанию: {targets.default_activity_label}\n"
            f"Активность для расчета сегодня: {targets.effective_activity_label}\n"
            f"{targets.activity_source_label}\n"
            "Расчетная дневная норма БЖУ (приблизительно):\n"
            f"Б: {NutritionService._format_number(targets.protein_g)} г / "
            f"Ж: {NutritionService._format_number(targets.fat_g)} г / "
            f"У: {NutritionService._format_number(targets.carbs_g)} г\n"
            "BMR — расход в покое, TDEE — расход с учетом активности.\n"
            "Подробнее: /terms"
        )

    @staticmethod
    def _format_recognized_item(item: RecognizedItem) -> str:
        return (
            f"- {item.display_name} {NutritionService._format_number(item.weight_g)} г: "
            f"{round(item.calories)} ккал, "
            f"Б {NutritionService._format_number(item.protein_g)} / "
            f"Ж {NutritionService._format_number(item.fat_g)} / "
            f"У {NutritionService._format_number(item.carbs_g)}"
        )

    @staticmethod
    def _format_number(value: float) -> str:
        text = f"{value:.1f}"
        if text.endswith(".0"):
            return text[:-2]
        return text
