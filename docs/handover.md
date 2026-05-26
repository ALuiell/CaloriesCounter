# Handover

## Purpose

This document is the current operational source of truth for the project.

Use it to understand what the project is building now, what assets already exist, and what the next implementation task should be.

## Current Product Focus

The active implementation scope is Level 1 only.

Level 1 means:

- the bot accepts one or more food lines in a message
- the expected format is `product + grams`
- the primary input language is Russian
- product lookup is based on the curated starter seed
- the bot returns calories, protein, fat, and carbs for recognized lines
- the bot returns a message-level total

Level 1 does not include:

- profile onboarding
- personal daily targets
- goal modes
- day history
- saved food entries
- daily totals
- remaining intake calculations
- free-form portion understanding such as `2 eggs` or `a slice of pizza`

## Language and Input Policy

Current MVP language policy:

- Russian is the primary supported input language
- Russian names and Russian aliases are the main lookup path
- English and Ukrainian aliases may be added later
- the MVP should not promise multilingual parity yet

Current MVP input policy:

- one line describes one product entry
- each line must contain a product name and a gram value
- the parser treats the numeric value as grams
- partially successful messages are allowed

Example:

```text
гречка 120
курица 150 г
помидор 80
```

## What Already Exists

### Documentation

- [README.md](F:\Python\CaloriesCounter\README.md)
- [Product Vision](F:\Python\CaloriesCounter\docs\product-vision.md)
- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Roadmap](F:\Python\CaloriesCounter\docs\roadmap.md)
- [Architecture](F:\Python\CaloriesCounter\docs\architecture.md)
- [Data Model](F:\Python\CaloriesCounter\docs\data-model.md)
- [Parsing Strategy](F:\Python\CaloriesCounter\docs\parsing-strategy.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)

### Data Assets

- starter seed:
  - [starter_products_usda_sr_legacy.json](F:\Python\CaloriesCounter\data\seeds\starter_products_usda_sr_legacy.json)
- USDA analysis report:
  - [usda_sr_legacy_analysis.json](F:\Python\CaloriesCounter\data\analysis\usda_sr_legacy_analysis.json)
- local USDA source dataset:
  - `FoodData_Central_sr_legacy_food_json_2018-04.json`

### Scripts

- [analyze_usda_sr_legacy.py](F:\Python\CaloriesCounter\scripts\analyze_usda_sr_legacy.py)
- [find_usda_candidates.py](F:\Python\CaloriesCounter\scripts\find_usda_candidates.py)
- [validate_starter_seed.py](F:\Python\CaloriesCounter\scripts\validate_starter_seed.py)
- [fix_starter_seed.py](F:\Python\CaloriesCounter\scripts\fix_starter_seed.py)

### Starter Seed Status

The current starter seed contains `178` curated products with:

- Russian names
- Russian aliases
- category labels
- explicit product state
- USDA references
- macros per 100 grams

The seed is intended for Level 1 lookup and calculation, not for direct end-user editing.

## Current Product Behavior

For Level 1, the bot should behave as follows:

1. Split the incoming message into lines.
2. Parse each line independently.
3. Normalize the product text.
4. Look up the product by the imported product name and aliases.
5. Calculate calories and macros for recognized lines.
6. Return a message response that:
   - lists recognized lines
   - lists unrecognized lines
   - shows total calories and macros for recognized lines only

If one line fails, the whole message should not fail.

## Next Implementation Step

The next practical build step is the Level 1 runtime path:

1. create the SQLite schema
2. create the `products` and `product_aliases` tables
3. import the starter seed into SQLite
4. implement normalized lookup by Russian product name and aliases
5. implement `product + grams` parsing
6. implement message-level calorie and macro calculation
7. return a user-facing response for recognized and unrecognized lines

## Future Direction

Later product growth is still planned in this order:

1. Level 2: user profile data and base target calculation
2. Level 3: goal modes and target comparison
3. after that: history, stored entries, daily totals, editing, richer parsing, and broader alias coverage

These later stages are intentionally not part of the current implementation-ready scope.

## Related Files

- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
- [Starter Products](F:\Python\CaloriesCounter\docs\starter-products.md)
