from __future__ import annotations

import json
from pathlib import Path

from app.db.database import Database
from app.services.normalization import normalize_product_name


def seed_products_if_empty(database: Database, seed_path: Path) -> None:
    payload = json.loads(seed_path.read_text(encoding="utf-8"))
    with database.connection() as conn:
        now = database.now_iso()

        # 1. Deactivate products in DB that are not in the seed payload anymore
        active_slugs = {product["slug"] for product in payload["products"]}
        conn.execute(
            "UPDATE products SET is_active = 0, updated_at = ? WHERE slug NOT IN ({})".format(
                ",".join("?" for _ in active_slugs)
            ),
            (now, *active_slugs)
        )

        # 2. Add or update products and aliases
        for product in payload["products"]:
            row = conn.execute(
                "SELECT id FROM products WHERE slug = ?",
                (product["slug"],),
            ).fetchone()

            if row is None:
                conn.execute(
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
                row = conn.execute(
                    "SELECT id FROM products WHERE slug = ?",
                    (product["slug"],),
                ).fetchone()
            else:
                # Make sure the product is active and has correct name and category
                conn.execute(
                    """
                    UPDATE products
                    SET name_ru = ?, normalized_name_ru = ?, category = ?, state = ?, is_active = 1, updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        product["name_ru"],
                        normalize_product_name(product["name_ru"]),
                        product["category"],
                        product["state"],
                        now,
                        row["id"],
                    ),
                )

            product_id = row["id"]
            aliases = set(product.get("aliases", []))
            aliases.add(product["name_ru"])

            # Delete aliases in DB for this product that are not in the seed file anymore
            normalized_aliases = {normalize_product_name(a) for a in aliases}
            conn.execute(
                "DELETE FROM product_aliases WHERE product_id = ? AND normalized_alias NOT IN ({})".format(
                    ",".join("?" for _ in normalized_aliases)
                ),
                (product_id, *normalized_aliases)
            )

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

