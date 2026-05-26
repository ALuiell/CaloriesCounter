# Data Model

## Purpose

This document defines the data structures needed for the current Level 1 MVP and for later expansion.

The Level 1 priority is product import and product lookup.

## Level 1 Core Entities

### Product

This is the main imported product record used for lookup and macro calculation.

Recommended fields:

- `id`
- `slug`
- `name_ru`
- `category`
- `state`
- `usda_description`
- `fdc_id`
- `usda_category`
- `calories_per_100g`
- `protein_per_100g`
- `fat_per_100g`
- `carbs_per_100g`
- `is_active`
- `created_at`
- `updated_at`

Notes:

- `name_ru` is the primary Level 1 lookup name
- macros are stored per 100 grams
- `state` is important for cases such as cooked vs dry products
- USDA reference fields are stored for traceability and future seed expansion

### ProductAlias

Used for lookup variants.

Recommended fields:

- `id`
- `product_id`
- `alias`
- `language`
- `created_at`

Notes:

- Level 1 should primarily store Russian aliases
- later expansion may add English and Ukrainian aliases
- a normalized alias index is recommended for fast lookup

## Later Expansion Entities

### User

Useful after Level 1:

- `id`
- `telegram_id`
- `username`
- `sex`
- `age`
- `height_cm`
- `weight_kg`
- `activity_level`
- `goal_type`
- `target_calories`
- `target_protein_g`
- `target_fat_g`
- `target_carbs_g`
- `created_at`
- `updated_at`

### FoodEntry

Useful after Level 1 when entry storage is introduced:

- `id`
- `user_id`
- `product_id`
- `raw_text`
- `product_text`
- `weight_g`
- `calories`
- `protein_g`
- `fat_g`
- `carbs_g`
- `consumed_at`
- `created_at`

### ParseLog

Useful when parse logging is introduced:

- `id`
- `user_id`
- `raw_message`
- `status`
- `error_reason`
- `created_at`

## Recommended Indexes

- `products.name_ru`
- `products.slug`
- `product_aliases.alias`
- later: `users.telegram_id`
- later: `food_entries.user_id + consumed_at`

## Data Notes

- Products should be imported from the starter seed, not queried directly from the large USDA JSON at runtime.
- Product lookup should be aligned with the current starter seed fields and alias model.
- SQLite is sufficient for MVP.

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Starter Products](F:\Python\CaloriesCounter\docs\starter-products.md)
- [Architecture](F:\Python\CaloriesCounter\docs\architecture.md)
