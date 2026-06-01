from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, time

from app.db.database import Database
from app.schemas.nutrition import CalculationResult, RecognizedItem
from app.services.normalization import normalize_product_name
from app.services.parser import parse_food_message
from app.services.profile import DailyNutritionTargets, ProfileService


@dataclass(frozen=True)
class ProductCategory:
    slug: str
    name: str
    count: int


@dataclass(frozen=True)
class ProductSummary:
    name: str
    calories_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    carbs_per_100g: float


@dataclass(frozen=True)
class UserProductSummary(ProductSummary):
    id: int


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

            product = self._find_product(telegram_id, item.product_text)
            if product is None:
                result.unrecognized_items.append(item.raw_item_text)
                continue

            multiplier = item.weight_g / 100.0
            result.recognized_items.append(
                RecognizedItem(
                    product_id=product["id"],
                    product_source=product["source"],
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

    def create_user_product(
        self,
        telegram_id: int,
        username: str | None,
        name_ru: str,
        calories_per_100g: float,
        protein_per_100g: float,
        fat_per_100g: float,
        carbs_per_100g: float,
    ) -> None:
        self.profile_service.ensure_user(telegram_id, username)
        user_id = self.profile_service.get_user_id(telegram_id)
        now = self.database.now_iso()
        normalized_name = normalize_product_name(name_ru)
        with self.database.connection() as conn:
            conn.execute(
                """
                INSERT INTO user_products (
                    user_id,
                    name_ru,
                    normalized_name_ru,
                    calories_per_100g,
                    protein_per_100g,
                    fat_per_100g,
                    carbs_per_100g,
                    is_active,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                ON CONFLICT(user_id, normalized_name_ru)
                DO UPDATE SET
                    name_ru = excluded.name_ru,
                    calories_per_100g = excluded.calories_per_100g,
                    protein_per_100g = excluded.protein_per_100g,
                    fat_per_100g = excluded.fat_per_100g,
                    carbs_per_100g = excluded.carbs_per_100g,
                    is_active = 1,
                    updated_at = excluded.updated_at
                """,
                (
                    user_id,
                    name_ru,
                    normalized_name,
                    calories_per_100g,
                    protein_per_100g,
                    fat_per_100g,
                    carbs_per_100g,
                    now,
                    now,
                ),
            )

    def store_entries(self, telegram_id: int, items: Iterable[RecognizedItem]) -> None:
        user_id = self.profile_service.get_user_id(telegram_id)
        now = self.database.now_iso()
        with self.database.connection() as conn:
            for item in items:
                product_id = item.product_id if item.product_source == "base" else None
                user_product_id = item.product_id if item.product_source == "user" else None
                conn.execute(
                    """
                    INSERT INTO food_entries (
                        user_id,
                        product_source,
                        product_id,
                        user_product_id,
                        raw_item_text,
                        product_text,
                        weight_g,
                        calories,
                        protein_g,
                        fat_g,
                        carbs_g,
                        consumed_at,
                        created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        item.product_source,
                        product_id,
                        user_product_id,
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

    def search_products(self, query: str, telegram_id: int | None = None, limit: int = 10) -> list[str]:
        normalized = normalize_product_name(query)
        if not normalized:
            return []

        pattern = f"%{normalized}%"
        matches: list[str] = []
        with self.database.connection() as conn:
            user_id = self._get_user_id_or_none(conn, telegram_id)
            if user_id is not None:
                rows = conn.execute(
                    """
                    SELECT name_ru
                    FROM user_products
                    WHERE user_id = ? AND is_active = 1 AND normalized_name_ru LIKE ?
                    ORDER BY name_ru
                    LIMIT ?
                    """,
                    (user_id, pattern, limit),
                ).fetchall()
                matches.extend(f"{row['name_ru']} (личное)" for row in rows)

            remaining_limit = max(limit - len(matches), 0)
            if remaining_limit == 0:
                return matches

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
                (pattern, pattern, remaining_limit),
            ).fetchall()
        for row in rows:
            name = str(row["name_ru"])
            if name not in matches:
                matches.append(name)
        return matches

    def list_categories(self) -> list[ProductCategory]:
        with self.database.connection() as conn:
            rows = conn.execute(
                """
                SELECT category, COUNT(*) AS count
                FROM products
                WHERE is_active = 1
                GROUP BY category
                ORDER BY category
                """
            ).fetchall()
        return [
            ProductCategory(
                slug=self._category_slug(str(row["category"])),
                name=str(row["category"]),
                count=int(row["count"]),
            )
            for row in rows
        ]

    def list_products_by_category(self, category_slug: str, limit: int = 30) -> list[ProductSummary]:
        category = self._category_name_by_slug(category_slug)
        if category is None:
            return []

        with self.database.connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    name_ru,
                    calories_per_100g,
                    protein_per_100g,
                    fat_per_100g,
                    carbs_per_100g
                FROM products
                WHERE is_active = 1 AND category = ?
                ORDER BY name_ru
                LIMIT ?
                """,
                (category, limit),
            ).fetchall()
        return [
            ProductSummary(
                name=str(row["name_ru"]),
                calories_per_100g=float(row["calories_per_100g"]),
                protein_per_100g=float(row["protein_per_100g"]),
                fat_per_100g=float(row["fat_per_100g"]),
                carbs_per_100g=float(row["carbs_per_100g"]),
            )
            for row in rows
        ]

    def list_user_products(self, telegram_id: int, limit: int = 20) -> list[UserProductSummary]:
        with self.database.connection() as conn:
            user_id = self._get_user_id_or_none(conn, telegram_id)
            if user_id is None:
                return []

            rows = conn.execute(
                """
                SELECT
                    id,
                    name_ru,
                    calories_per_100g,
                    protein_per_100g,
                    fat_per_100g,
                    carbs_per_100g
                FROM user_products
                WHERE user_id = ? AND is_active = 1
                ORDER BY name_ru
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        return [
            UserProductSummary(
                id=int(row["id"]),
                name=str(row["name_ru"]),
                calories_per_100g=float(row["calories_per_100g"]),
                protein_per_100g=float(row["protein_per_100g"]),
                fat_per_100g=float(row["fat_per_100g"]),
                carbs_per_100g=float(row["carbs_per_100g"]),
            )
            for row in rows
        ]

    def delete_user_product(self, telegram_id: int, product_id: int) -> bool:
        now = self.database.now_iso()
        with self.database.connection() as conn:
            user_id = self._get_user_id_or_none(conn, telegram_id)
            if user_id is None:
                return False

            cursor = conn.execute(
                """
                UPDATE user_products
                SET is_active = 0, updated_at = ?
                WHERE id = ? AND user_id = ? AND is_active = 1
                """,
                (now, product_id, user_id),
            )
        return cursor.rowcount > 0

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

    def _find_product(self, telegram_id: int, product_text: str):
        normalized = normalize_product_name(product_text)
        with self.database.connection() as conn:
            user_id = self._get_user_id_or_none(conn, telegram_id)
            if user_id is not None:
                row = conn.execute(
                    """
                    SELECT
                        id,
                        name_ru,
                        calories_per_100g,
                        protein_per_100g,
                        fat_per_100g,
                        carbs_per_100g,
                        'user' AS source
                    FROM user_products
                    WHERE user_id = ? AND normalized_name_ru = ? AND is_active = 1
                    """,
                    (user_id, normalized),
                ).fetchone()
                if row is not None:
                    return row

            row = conn.execute(
                """
                SELECT p.*, 'base' AS source
                FROM products p
                WHERE p.normalized_name_ru = ? AND p.is_active = 1
                """,
                (normalized,),
            ).fetchone()
            if row is not None:
                return row

            row = conn.execute(
                """
                SELECT p.*, 'base' AS source
                FROM product_aliases pa
                JOIN products p ON p.id = pa.product_id
                WHERE pa.normalized_alias = ? AND p.is_active = 1
                LIMIT 1
                """,
                (normalized,),
            ).fetchone()
            return row

    @staticmethod
    def _get_user_id_or_none(conn, telegram_id: int | None) -> int | None:
        if telegram_id is None:
            return None
        row = conn.execute(
            "SELECT id FROM users WHERE telegram_id = ?",
            (telegram_id,),
        ).fetchone()
        if row is None:
            return None
        return int(row["id"])

    @staticmethod
    def _category_slug(category: str) -> str:
        return normalize_product_name(category).replace(" ", "_")

    def _category_name_by_slug(self, category_slug: str) -> str | None:
        for category in self.list_categories():
            if category.slug == category_slug:
                return category.name
        return None

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
