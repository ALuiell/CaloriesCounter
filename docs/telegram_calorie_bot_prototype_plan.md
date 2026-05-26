# Telegram Bot Prototype Plan — Calorie Counter MVP

## Summary

Build the first working bot as a **Russian-first calorie counter** with an optional personal assistant layer on top.

The default behavior is simple food calculation from free-text messages using comma-separated or newline-separated items. A user may optionally create a profile and enable assistant mode. Only then the bot stores daily food entries and adds **Today totals** plus **BMR** to food replies.

**Out of scope for this prototype:**

- TDEE
- goal modes
- remaining calories
- diet recommendations
- fuzzy guessing
- barcode scanning
- edit/delete/history UI beyond `/today`

The main goal of v1 is not to build a full diet app, but to make food input fast and reliable.

---

## Core Product Logic

The bot should support messages like:

```text
гречка 120, курица 180, помидор 80
```

Also supported:

```text
гречка 120
курица 180
помидор 80
```

And mixed input:

```text
гречка 120, курица 180
помидор 80
```

The bot parses each item, looks up the product in the local database, calculates calories and macros based on grams, and returns a compact summary.

---

## Important MVP Decision

The bot has two separate modes:

### 1. Plain Calc Mode

Default mode.

- User can calculate food without profile.
- No food entries are saved.
- Bot returns only the result for the current message.
- No Today totals.
- No BMR.
- No personal context.

### 2. Assistant Mode

Optional mode.

Requires completed profile.

- Food entries are saved.
- Bot shows current message total.
- Bot also shows Today totals.
- Bot also shows BMR.
- `/today` uses persisted food history.

This separation keeps the prototype simple and avoids storing user data unless the user explicitly enables assistant behavior.

---

## Key Changes / Implementation Plan

### Runtime Skeleton

Create the basic project structure:

- `aiogram`
- `.env` config
- SQLite database
- startup entrypoint
- seed import script
- command handlers
- message parser
- calculation service
- product lookup service

Recommended `.env` values:

```env
BOT_TOKEN=your_token_here
DATABASE_URL=sqlite:///bot.db
APP_TIMEZONE=Europe/Kyiv
```

Important: the bot token must be stored only in `.env`. If it was exposed in chat or logs, rotate it in BotFather before real deployment.

---

## Seed Import

Import the curated USDA SR Legacy starter set into SQLite.

The JSON seed already contains useful fields:

- `slug`
- `name_ru`
- `category`
- `state`
- `usda_description`
- `aliases`
- `fdc_id`
- `usda_category`
- `calories_per_100g`
- `protein_per_100g`
- `fat_per_100g`
- `carbs_per_100g`

Recommended target tables:

- `products`
- `product_aliases`

---

## Database Schema

### `products`

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name_ru TEXT NOT NULL,
    normalized_name_ru TEXT NOT NULL,

    category TEXT,
    state TEXT,

    calories_per_100g REAL NOT NULL,
    protein_per_100g REAL NOT NULL,
    fat_per_100g REAL NOT NULL,
    carbs_per_100g REAL NOT NULL,

    source TEXT,
    source_id TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Why `state` is important

Keep product state because food calories may differ heavily depending on whether the product is raw, dry, cooked, or prepared.

Examples:

```text
гречка сухая
гречка вареная
рис сухой
рис вареный
макароны сухие
макароны вареные
```

The bot should show the selected product clearly in replies, for example:

```text
гречка вареная — 120 г
```

Not just:

```text
гречка — 120 г
```

This prevents confusion.

---

### `product_aliases`

```sql
CREATE TABLE product_aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    alias TEXT NOT NULL,
    normalized_alias TEXT NOT NULL,

    priority INTEGER DEFAULT 100,
    is_default BOOLEAN DEFAULT 0,

    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Why `priority` / `is_default` matters

Some aliases are ambiguous.

Example:

```text
рис
```

Could mean:

- рис белый вареный
- рис белый сухой
- рис бурый вареный
- рис бурый сухой

For MVP, the default user intent should usually be cooked/prepared food.

Recommended defaults:

```text
рис -> рис белый вареный
гречка -> гречка вареная
макароны -> макароны вареные
овсянка -> овсянка на воде
картошка -> картофель вареный or картофель сырой, depending on product name
```

Use lower `priority` value for more preferred matches.

Example:

```text
priority = 10 means preferred
priority = 100 means normal
priority = 200 means fallback
```

---

### `users`

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    username TEXT,

    assistant_enabled BOOLEAN DEFAULT 0,

    sex TEXT,
    age INTEGER,
    height_cm REAL,
    weight_kg REAL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

Allowed `sex` values:

```text
male
female
```

For MVP, avoid extra sex/gender logic because BMR formula only needs male/female constants.

---

### `food_entries`

```sql
CREATE TABLE food_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,

    product_id INTEGER,
    product_name_snapshot TEXT,

    raw_item_text TEXT NOT NULL,
    weight_g REAL NOT NULL,

    calories REAL NOT NULL,
    protein REAL NOT NULL,
    fat REAL NOT NULL,
    carbs REAL NOT NULL,

    consumed_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Why `product_name_snapshot` is useful

If product names or aliases are later changed in the database, old food entries still display correctly.

Example:

```text
product_name_snapshot = "гречка вареная"
```

---

## Product Lookup Rules

### v1 Lookup Behavior

Use exact or normalized match only:

1. Normalize user input.
2. Try `products.normalized_name_ru`.
3. Try `product_aliases.normalized_alias`.
4. If multiple matches exist, choose the one with best `priority`.
5. If no match exists, mark item as unrecognized.
6. Do not use fuzzy guessing in v1.

### Normalization

Recommended normalization:

- lowercase
- trim spaces
- replace `ё` with `е`
- collapse multiple spaces
- remove punctuation around words
- optionally remove common suffix dots

Example:

```text
"Гречка   варёная" -> "гречка вареная"
"120 г. гречки" -> parser should extract grams first, then normalize product text
```

---

## Parser Requirements

### Supported in v1

```text
гречка 120
гречка 120г
гречка 120 г
гречка 120 гр
гречка 120 грамм
```

Recommended item split:

- commas
- newlines
- mixed commas + newlines

Example:

```text
гречка 120, курица 180
помидор 80
```

Should produce:

```text
гречка 120
курица 180
помидор 80
```

### Optional but useful

Support reversed order:

```text
120 г гречка
120 грамм гречки
```

This can be added in v1.1 if needed.

---

## Parser Edge Cases

Handle safely:

```text
гречка
гречка 0
гречка -100
гречка 999999
гречка сто грамм
,,
гречка 120,, курица 180
```

Recommended validation:

```text
weight_g > 0
weight_g <= 5000
```

If the item has no grams, return it as unrecognized or ask for grams.

Do not crash on empty fragments.

---

## Calculation Formula

All values in the product database are stored per 100 g.

Formula:

```python
calories = product.calories_per_100g * weight_g / 100
protein = product.protein_per_100g * weight_g / 100
fat = product.fat_per_100g * weight_g / 100
carbs = product.carbs_per_100g * weight_g / 100
```

Round output for readability:

```text
calories: nearest integer
protein/fat/carbs: 1 decimal
```

Example:

```text
Гречка вареная — 120 г:
110 ккал
Б: 4.1 г / Ж: 0.7 г / У: 23.9 г
```

---

## Reply Modes

## Calc Mode Reply

Show:

1. recognized items
2. unrecognized items, if any
3. message total

Example:

```text
Рассчитано:

• гречка вареная — 120 г: 110 ккал, Б 4.1 / Ж 0.7 / У 23.9
• куриная грудка приготовленная — 180 г: 297 ккал, Б 55.8 / Ж 6.5 / У 0.0

Не распознано:
• авкадо 50

Итого:
407 ккал
Б: 59.9 г / Ж: 7.2 г / У: 23.9 г
```

Important: always show which product was selected.

---

## Assistant Mode Reply

Show:

1. recognized items
2. unrecognized items, if any
3. message total
4. Today totals
5. BMR

Example:

```text
Рассчитано:

• гречка вареная — 120 г: 110 ккал, Б 4.1 / Ж 0.7 / У 23.9
• куриная грудка приготовленная — 180 г: 297 ккал, Б 55.8 / Ж 6.5 / У 0.0

Итого за сообщение:
407 ккал
Б: 59.9 г / Ж: 7.2 г / У: 23.9 г

Сегодня:
1320 ккал
Б: 104.3 г / Ж: 42.1 г / У: 128.9 г

Профиль:
BMR: 1780 ккал
```

No “remaining calories” in prototype.

No “daily norm” claims.

No “you should eat X more” claims.

---

## Commands

### `/start`

Offers two paths:

```text
1. Start calculating now
2. Set up profile
```

The user should be able to calculate immediately without profile.

---

### `/help`

Shows examples:

```text
Примеры:
гречка 120
гречка 120, курица 180, помидор 80

Можно писать через запятую или с новой строки.
```

Also explain:

```text
/profile — заполнить профиль
/assistant_on — включить режим дневника
/assistant_off — выключить режим дневника
/today — итоги за сегодня
/search — найти продукт в базе
```

---

### `/calc`

Optional.

It can simply show instructions:

```text
Отправьте продукты в формате:
гречка 120, курица 180
```

Since the bot already treats normal text messages as calculation input, `/calc` does not need a separate state in v1.

---

### `/profile`

Collects:

- sex
- age
- height_cm
- weight_kg

Profile can be implemented with aiogram FSM.

Validation:

```text
age: 10–120
height_cm: 80–250
weight_kg: 20–300
sex: male/female
```

---

### `/assistant_on`

Requires complete profile.

If profile incomplete:

```text
Чтобы включить режим дневника, сначала заполните профиль:
/profile
```

If profile complete:

```text
Режим дневника включен.
Теперь продукты будут сохраняться, а ответы будут включать итоги за сегодня и BMR.
```

---

### `/assistant_off`

Disables assistant mode.

Important: it should stop saving new food entries. Existing old entries can remain in DB.

Reply:

```text
Режим дневника выключен.
Теперь я буду только считать сообщение, без сохранения и итогов за день.
```

---

### `/today`

Shows totals for current app calendar day.

Example:

```text
Сегодня:

1320 ккал
Б: 104.3 г
Ж: 42.1 г
У: 128.9 г
```

If no entries:

```text
Сегодня пока нет сохраненных приемов пищи.
```

---

### `/search`

Recommended addition.

Even without fuzzy search, `/search` helps users discover valid product names.

Example:

```text
/search греч
```

Reply:

```text
Найдено:
• гречка вареная
• гречка сухая
```

Search can use simple `LIKE` over `normalized_name_ru` and `normalized_alias`.

Limit results:

```text
max 10
```

---

## BMR Logic

Use Mifflin-St Jeor.

### Male

```text
BMR = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
```

### Female

```text
BMR = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
```

Compute BMR on demand from stored profile data.

Do not store BMR permanently unless there is a specific reason. If profile changes, BMR should update automatically.

---

## Daily Aggregation

Today is based on configured app timezone:

```env
APP_TIMEZONE=Europe/Kyiv
```

For `/today`, select entries where `consumed_at` falls inside the current local calendar day.

Recommended logic:

1. Get current datetime in app timezone.
2. Calculate start of today: `00:00:00`.
3. Calculate start of tomorrow.
4. Query entries between these two timestamps.

Do not use naive UTC day if the bot is meant for local daily tracking.

---

## Food Entry Storage Rules

### Plain Calc Mode

Do not save entries.

Flow:

1. Parse message.
2. Lookup products.
3. Calculate.
4. Reply.
5. No DB insert into `food_entries`.

### Assistant Mode

Save only recognized items.

Flow:

1. Parse message.
2. Lookup products.
3. Calculate.
4. Insert recognized items into `food_entries`.
5. Reply with message total + Today + BMR.
6. Show unrecognized items if any.

Unrecognized items should not be saved.

---

## Public Behavior

### Supported Input

```text
гречка 120, курица 180, помидор 80
```

```text
гречка 120
курица 180
помидор 80
```

```text
гречка 120г, курица 180 г
```

### Partial Success

Input:

```text
гречка 120, непонятнаяеда 50
```

Reply should still calculate recognized items and show:

```text
Не распознано:
• непонятнаяеда 50
```

---

## Recommended Product Data Improvements

The current seed is good for MVP, but before launch it is worth adding:

### 1. More Russian aliases

Examples:

```text
картофель вареный:
- картошка
- вареная картошка
- картоха

куриная грудка:
- курица
- грудка
- курогрудь
- филе куриное

макароны вареные:
- макароны
- макарошки
- паста
- спагетти

творог:
- творог
- творожок
```

---

### 2. Rename overly foreign names

Better user-facing names:

```text
фасоль navy сухая -> фасоль белая мелкая сухая
фасоль navy вареная -> фасоль белая мелкая вареная
дыня канталупа -> дыня
```

Keep original English names in aliases.

---

### 3. Add basic prepared foods

Add a small category:

```text
готовые блюда
```

Recommended first additions:

```text
борщ
суп куриный
суп овощной
омлет
сырники
плов
котлета куриная
котлета мясная
картофельное пюре
картошка жареная
греческий салат
оливье
гречка с курицей
рис с курицей
```

Even approximate values are useful if marked as approximate.

---

### 4. Add sweets and snacks

Recommended:

```text
шоколад молочный
шоколад темный
печенье
конфета
мороженое
вафли
чипсы
сухарики
мед
сахар
```

---

### 5. Add drinks

Recommended:

```text
вода
чай без сахара
кофе без сахара
кофе с молоком
кола
сок апельсиновый
сок яблочный
кефир
какао
```

---

## Test Plan

## Parser Scenarios

- one product
- multiple products via commas
- multiple products via newlines
- mixed delimiters
- one recognized + one unrecognized item
- empty fragments like doubled commas or blank lines
- grams with `г`
- grams with `гр`
- grams with `грамм`
- invalid grams
- very large grams

---

## Lookup Scenarios

- exact `name_ru` match
- alias match
- cooked/default product names such as `рис`, `гречка`, `макароны`
- unknown product returns partial-success response
- ambiguous base alias picks configured default by priority
- `/search` returns relevant product names

---

## Profile Scenarios

- user can calculate food without a profile
- `/profile` completes successfully
- invalid profile values are rejected
- `/assistant_on` fails clearly if profile is incomplete
- `/assistant_on` succeeds after profile completion
- `/assistant_off` removes Today and BMR from food replies
- profile update changes shown BMR

---

## BMR Scenarios

Test male formula:

```text
10 * kg + 6.25 * cm - 5 * age + 5
```

Test female formula:

```text
10 * kg + 6.25 * cm - 5 * age - 161
```

Check that BMR changes after profile update.

---

## Daily Aggregation Scenarios

- entries created on the same day are summed in `/today`
- assistant mode food reply includes current-day totals
- calc mode food reply does not include Today or BMR
- entries from previous day are not included
- timezone boundary works according to `APP_TIMEZONE`

---

## Security / Privacy Notes

- Bot token must be stored only in `.env`.
- If the token was exposed anywhere, rotate it in BotFather.
- Plain calc mode should remain stateless.
- Assistant mode should clearly tell users that food entries are saved.
- Do not expose raw internal IDs to users.
- Do not log full user food messages in production unless needed.

---

## Suggested Development Stages

### v1.0 — Calculator Core

- Runtime skeleton
- SQLite
- Product seed import
- Parser
- Exact alias lookup
- Calculation replies
- Partial success
- `/help`

### v1.1 — Product UX

- `/search`
- Better Russian aliases
- Priority/default aliases
- More user-friendly names
- More prepared foods, sweets, drinks

### v1.2 — Assistant Mode

- `/profile`
- `/assistant_on`
- `/assistant_off`
- food entry persistence
- `/today`
- BMR

### v2.0 — Smart Features

Out of scope for prototype:

- fuzzy search
- TDEE
- goals
- remaining calories
- edit/delete entries
- meal history
- Ukrainian/English aliases
- barcode lookup
- food suggestions
- nutrition recommendations

---

## Final Recommendation

The prototype plan is strong and should stay narrow.

The most important additions before coding:

1. Keep `state` in `products`.
2. Add `priority` or `is_default` for aliases.
3. Always show the selected product name in replies.
4. Add `/search`.
5. Store food entries only in assistant mode.
6. Use `APP_TIMEZONE=Europe/Kyiv`.
7. Avoid TDEE, remaining calories, goals, and diet advice in the prototype.

This keeps the first version simple, useful, and much easier to debug.
