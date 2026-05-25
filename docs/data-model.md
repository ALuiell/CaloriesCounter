# Data Model

## Основные сущности

### User

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

### Product

- `id`
- `name`
- `canonical_name`
- `calories_per_100g`
- `protein_per_100g`
- `fat_per_100g`
- `carbs_per_100g`
- `brand`
- `category`
- `is_active`
- `created_at`
- `updated_at`

### ProductAlias

- `id`
- `product_id`
- `alias`

Нужно для:

- синонимов;
- разных форм написания;
- частых пользовательских вариантов.

### FoodEntry

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

- `id`
- `user_id`
- `raw_message`
- `status`
- `error_reason`
- `created_at`

## Индексы

Желательные индексы:

- `users.telegram_id`
- `products.canonical_name`
- `product_aliases.alias`
- `food_entries.user_id + consumed_at`

## Замечания по данным

- Продукты лучше хранить в расчете на 100 грамм.
- Для MVP достаточно SQLite.
- Дату приема пищи лучше хранить отдельно от даты создания записи, чтобы позже поддержать добавление "задним числом".
