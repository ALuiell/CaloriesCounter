from __future__ import annotations

import json
from pathlib import Path

from app.db.database import Database
from app.services.normalization import normalize_product_name


def seed_products_if_empty(database: Database, seed_path: Path) -> None:
    with database.connection() as conn:
        count = conn.execute("SELECT COUNT(*) AS count FROM products").fetchone()["count"]
        if count:
            return

        payload = json.loads(seed_path.read_text(encoding="utf-8"))
        now = database.now_iso()

        for product in payload["products"]:
            cursor = conn.execute(
                """
                INSERT INTO products (
                    slug,
                    name_ru,
                    normalized_name_ru,
                    category,
                    state,
                    usda_description,
                    fdc_id,
                    usda_category,
                    calories_per_100g,
                    protein_per_100g,
                    fat_per_100g,
                    carbs_per_100g,
                    is_active,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    product["slug"],
                    product["name_ru"],
                    normalize_product_name(product["name_ru"]),
                    product["category"],
                    product["state"],
                    product["usda_description"],
                    product["fdc_id"],
                    product["usda_category"],
                    product["calories_per_100g"],
                    product["protein_per_100g"],
                    product["fat_per_100g"],
                    product["carbs_per_100g"],
                    now,
                    now,
                ),
            )
            product_id = cursor.lastrowid

            aliases = set(product.get("aliases", []))
            aliases.add(product["name_ru"])
            for alias in aliases:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO product_aliases (
                        product_id,
                        alias,
                        normalized_alias,
                        language,
                        created_at
                    ) VALUES (?, ?, ?, 'ru', ?)
                    """,
                    (
                        product_id,
                        alias,
                        normalize_product_name(alias),
                        now,
                    ),
                )
