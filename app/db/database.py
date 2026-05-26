from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    name_ru TEXT NOT NULL,
    normalized_name_ru TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    state TEXT NOT NULL,
    usda_description TEXT NOT NULL,
    fdc_id INTEGER NOT NULL,
    usda_category TEXT NOT NULL,
    calories_per_100g REAL NOT NULL,
    protein_per_100g REAL NOT NULL,
    fat_per_100g REAL NOT NULL,
    carbs_per_100g REAL NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    alias TEXT NOT NULL,
    normalized_alias TEXT NOT NULL UNIQUE,
    language TEXT NOT NULL DEFAULT 'ru',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL UNIQUE,
    username TEXT,
    assistant_enabled INTEGER NOT NULL DEFAULT 0,
    sex TEXT,
    age INTEGER,
    height_cm REAL,
    weight_kg REAL,
    activity_level TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS food_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    raw_item_text TEXT NOT NULL,
    product_text TEXT NOT NULL,
    weight_g REAL NOT NULL,
    calories REAL NOT NULL,
    protein_g REAL NOT NULL,
    fat_g REAL NOT NULL,
    carbs_g REAL NOT NULL,
    consumed_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_activity_overrides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity_level TEXT NOT NULL,
    activity_date TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(user_id, activity_date)
);

CREATE INDEX IF NOT EXISTS idx_products_name_ru ON products(normalized_name_ru);
CREATE INDEX IF NOT EXISTS idx_product_aliases_alias ON product_aliases(normalized_alias);
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_food_entries_user_consumed_at ON food_entries(user_id, consumed_at);
CREATE INDEX IF NOT EXISTS idx_user_activity_overrides_user_date ON user_activity_overrides(user_id, activity_date);
"""


class Database:
    def __init__(self, database_path: Path, timezone_name: str) -> None:
        self.database_path = database_path
        self.timezone = ZoneInfo(timezone_name)

    def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as conn:
            conn.executescript(SCHEMA_SQL)
            self._migrate_legacy_schema(conn)

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def now_iso(self) -> str:
        return datetime.now(self.timezone).isoformat()

    def today_local_date(self) -> date:
        return datetime.now(self.timezone).date()

    def today_local_date_iso(self) -> str:
        return self.today_local_date().isoformat()

    @staticmethod
    def _migrate_legacy_schema(conn: sqlite3.Connection) -> None:
        user_columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
        if "activity_level" not in user_columns:
            conn.execute("ALTER TABLE users ADD COLUMN activity_level TEXT")
