from __future__ import annotations

from dataclasses import dataclass

from app.db.database import Database


ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

ACTIVITY_LABELS = {
    "sedentary": "спокойный день / минимальная активность",
    "light": "легкая активность",
    "moderate": "умеренная активность",
    "active": "высокая активность",
    "very_active": "очень высокая активность",
}


@dataclass(frozen=True)
class UserProfile:
    telegram_id: int
    username: str | None
    assistant_enabled: bool
    sex: str | None
    age: int | None
    height_cm: float | None
    weight_kg: float | None
    activity_level: str | None
    language: str = "ru"
    language_set: bool = False

    @property
    def is_complete(self) -> bool:
        return all(
            value is not None
            for value in (self.sex, self.age, self.height_cm, self.weight_kg, self.activity_level)
        )


@dataclass(frozen=True)
class DailyNutritionTargets:
    bmr: float
    tdee: float
    protein_g: float
    fat_g: float
    carbs_g: float
    default_activity_level: str
    effective_activity_level: str
    activity_source: str

    def default_activity_label(self, lang: str = "ru") -> str:
        return activity_label(self.default_activity_level, lang)

    def effective_activity_label(self, lang: str = "ru") -> str:
        return activity_label(self.effective_activity_level, lang)

    def activity_source_label(self, lang: str = "ru") -> str:
        from app.core.i18n import get_text
        if self.activity_source == "override":
            return get_text(lang, "activity_override_active")
        return get_text(lang, "activity_default_used")


def activity_label(activity_level: str, lang: str = "ru") -> str:
    from app.core.i18n import get_text
    return get_text(lang, f"activity_{activity_level}")


def calculate_bmr(sex: str, age: int, height_cm: float, weight_kg: float) -> float:
    if sex == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_tdee(bmr: float, activity_level: str) -> float:
    return bmr * ACTIVITY_MULTIPLIERS[activity_level]


def calculate_daily_macro_norms(tdee: float) -> dict[str, float]:
    return {
        "protein_g": round(tdee * 0.25 / 4, 1),
        "fat_g": round(tdee * 0.30 / 9, 1),
        "carbs_g": round(tdee * 0.45 / 4, 1),
    }


class ProfileService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def ensure_user(self, telegram_id: int, username: str | None, default_lang: str | None = None) -> None:
        now = self.database.now_iso()
        with self.database.connection() as conn:
            existing = conn.execute(
                "SELECT id, language_set, language FROM users WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchone()
            if existing:
                lang_set = bool(existing["language_set"]) if "language_set" in existing.keys() else True
                current_lang = existing["language"] if "language" in existing.keys() else "ru"
                if not lang_set and default_lang and current_lang != default_lang:
                    conn.execute(
                        "UPDATE users SET username = ?, language = ?, updated_at = ? WHERE telegram_id = ?",
                        (username, default_lang, now, telegram_id),
                    )
                else:
                    conn.execute(
                        "UPDATE users SET username = ?, updated_at = ? WHERE telegram_id = ?",
                        (username, now, telegram_id),
                    )
                return

            lang_to_insert = default_lang if default_lang else "ru"
            conn.execute(
                """
                INSERT INTO users (
                    telegram_id,
                    username,
                    assistant_enabled,
                    language,
                    created_at,
                    updated_at
                ) VALUES (?, ?, 0, ?, ?, ?)
                """,
                (telegram_id, username, lang_to_insert, now, now),
            )

    def update_profile(
        self,
        telegram_id: int,
        username: str | None,
        sex: str,
        age: int,
        height_cm: float,
        weight_kg: float,
        activity_level: str,
    ) -> None:
        self.ensure_user(telegram_id, username)
        self._validate_activity_level(activity_level)
        now = self.database.now_iso()
        with self.database.connection() as conn:
            conn.execute(
                """
                UPDATE users
                SET username = ?, sex = ?, age = ?, height_cm = ?, weight_kg = ?, activity_level = ?, updated_at = ?
                WHERE telegram_id = ?
                """,
                (username, sex, age, height_cm, weight_kg, activity_level, now, telegram_id),
            )

    def update_profile_field(
        self,
        telegram_id: int,
        username: str | None,
        field_name: str,
        value: str | int | float,
    ) -> None:
        allowed_fields = {"sex", "age", "height_cm", "weight_kg", "activity_level"}
        if field_name not in allowed_fields:
            raise ValueError(f"Unsupported profile field: {field_name}")
        if field_name == "activity_level":
            self._validate_activity_level(str(value))

        self.ensure_user(telegram_id, username)
        now = self.database.now_iso()
        with self.database.connection() as conn:
            conn.execute(
                f"UPDATE users SET username = ?, {field_name} = ?, updated_at = ? WHERE telegram_id = ?",
                (username, value, now, telegram_id),
            )

    def set_assistant_mode(self, telegram_id: int, enabled: bool) -> None:
        now = self.database.now_iso()
        with self.database.connection() as conn:
            conn.execute(
                "UPDATE users SET assistant_enabled = ?, updated_at = ? WHERE telegram_id = ?",
                (1 if enabled else 0, now, telegram_id),
            )

    def has_complete_profile(self, telegram_id: int) -> bool:
        profile = self.get_profile(telegram_id)
        return bool(profile and profile.is_complete)

    def is_assistant_enabled(self, telegram_id: int) -> bool:
        with self.database.connection() as conn:
            row = conn.execute(
                "SELECT assistant_enabled FROM users WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchone()
        return bool(row and row["assistant_enabled"])

    def get_user_id(self, telegram_id: int) -> int:
        with self.database.connection() as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchone()
        if row is None:
            raise RuntimeError("User does not exist")
        return int(row["id"])

    def get_profile(self, telegram_id: int) -> UserProfile | None:
        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT telegram_id, username, assistant_enabled, sex, age, height_cm, weight_kg, activity_level, language, language_set
                FROM users
                WHERE telegram_id = ?
                """,
                (telegram_id,),
            ).fetchone()
        if row is None:
            return None
        
        # Check if language column exists in database keys (handles pre-migration in unit tests)
        lang = "ru"
        if "language" in row.keys() and row["language"] is not None:
            lang = row["language"]
            
        lang_set = False
        if "language_set" in row.keys() and row["language_set"] is not None:
            lang_set = bool(row["language_set"])

        return UserProfile(
            telegram_id=int(row["telegram_id"]),
            username=row["username"],
            assistant_enabled=bool(row["assistant_enabled"]),
            sex=row["sex"],
            age=int(row["age"]) if row["age"] is not None else None,
            height_cm=float(row["height_cm"]) if row["height_cm"] is not None else None,
            weight_kg=float(row["weight_kg"]) if row["weight_kg"] is not None else None,
            activity_level=row["activity_level"],
            language=lang,
            language_set=lang_set,
        )

    def update_profile_language(self, telegram_id: int, language: str) -> None:
        now = self.database.now_iso()
        with self.database.connection() as conn:
            conn.execute(
                "UPDATE users SET language = ?, language_set = 1, updated_at = ? WHERE telegram_id = ?",
                (language, now, telegram_id),
            )

    def set_activity_override_for_today(self, telegram_id: int, activity_level: str) -> None:
        self._validate_activity_level(activity_level)
        user_id = self.get_user_id(telegram_id)
        now = self.database.now_iso()
        today = self.database.today_local_date_iso()
        with self.database.connection() as conn:
            conn.execute(
                """
                INSERT INTO user_activity_overrides (
                    user_id,
                    activity_level,
                    activity_date,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, activity_date)
                DO UPDATE SET activity_level = excluded.activity_level, updated_at = excluded.updated_at
                """,
                (user_id, activity_level, today, now, now),
            )

    def clear_activity_override_for_today(self, telegram_id: int) -> None:
        user_id = self.get_user_id(telegram_id)
        today = self.database.today_local_date_iso()
        with self.database.connection() as conn:
            conn.execute(
                "DELETE FROM user_activity_overrides WHERE user_id = ? AND activity_date = ?",
                (user_id, today),
            )

    def get_effective_activity(self, telegram_id: int) -> tuple[str, str]:
        profile = self.get_profile(telegram_id)
        if profile is None or profile.activity_level is None:
            raise RuntimeError("Profile is incomplete")

        user_id = self.get_user_id(telegram_id)
        today = self.database.today_local_date_iso()
        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT activity_level
                FROM user_activity_overrides
                WHERE user_id = ? AND activity_date = ?
                """,
                (user_id, today),
            ).fetchone()
        if row is not None:
            return str(row["activity_level"]), "override"
        return profile.activity_level, "default"

    def get_bmr(self, telegram_id: int) -> float:
        profile = self.get_profile(telegram_id)
        if profile is None or not profile.is_complete:
            raise RuntimeError("Profile is incomplete")
        return calculate_bmr(
            sex=str(profile.sex),
            age=int(profile.age),
            height_cm=float(profile.height_cm),
            weight_kg=float(profile.weight_kg),
        )

    def get_daily_targets(self, telegram_id: int) -> DailyNutritionTargets:
        profile = self.get_profile(telegram_id)
        if profile is None or not profile.is_complete:
            raise RuntimeError("Profile is incomplete")

        bmr = calculate_bmr(
            sex=str(profile.sex),
            age=int(profile.age),
            height_cm=float(profile.height_cm),
            weight_kg=float(profile.weight_kg),
        )
        effective_activity, source = self.get_effective_activity(telegram_id)
        tdee = calculate_tdee(bmr, effective_activity)
        macros = calculate_daily_macro_norms(tdee)
        return DailyNutritionTargets(
            bmr=bmr,
            tdee=tdee,
            protein_g=macros["protein_g"],
            fat_g=macros["fat_g"],
            carbs_g=macros["carbs_g"],
            default_activity_level=str(profile.activity_level),
            effective_activity_level=effective_activity,
            activity_source=source,
        )

    @staticmethod
    def _validate_activity_level(activity_level: str) -> None:
        if activity_level not in ACTIVITY_MULTIPLIERS:
            raise ValueError(f"Unsupported activity level: {activity_level}")
