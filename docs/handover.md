# Handover

## Purpose

This document is the current operational source of truth for the project.

Use it to understand what the bot already does, what assets already exist, and what the next implementation focus should be.

## Current Product Scope

The bot has moved beyond the original Level 1-only runtime path.

The current implemented scope includes:

- Russian-first food input in `product + grams` format
- parsing multiple items from one message
- lookup by curated product name and aliases
- calories, protein, fat, and carbs per recognized item
- totals for the current message
- user profile onboarding
- profile editing
- base daily target calculation from profile data
- per-day activity override
- optional assistant mode
- `/today` daily totals
- `/search` product search
- personal user-added products and prepared meals
- category browsing for shared products
- listing and deleting personal products

The current scope does not yet include:

- goal modes such as `maintenance`, `gain`, or `diet`
- remaining intake guidance against a selected goal
- entry editing or deletion
- history screens beyond today
- editing personal products
- rich portion parsing such as `2 eggs` or `a slice of pizza`

## Current User Experience

The current bot behavior is:

1. The user sends one or more food items in a single message.
2. The parser splits the message into independent items.
3. Each item is normalized and looked up by Russian product name or alias.
4. Recognized items are calculated from macros per 100 grams.
5. Unrecognized items are reported without failing the full message.
6. If assistant mode is off, the reply focuses on the current message only.
7. If assistant mode is on and the profile is complete, recognized items are stored and the reply also includes:
   - today totals
   - BMR
   - TDEE
   - approximate daily macro targets

## Implemented Commands and Flows

The current bot exposes these user-facing flows:

- `/start` - welcome text and main menu
- `/help` and `/calc` - usage help
- `/profile` - show profile or start onboarding
- `/edit_profile` - edit a completed profile
- `/activity_today` - choose activity for today
- `/activity_reset` - clear today's activity override
- `/assistant_on` - enable assistant mode
- `/assistant_off` - disable assistant mode
- `/today` - show current-day totals with targets
- `/search` - search products in the database
- `/terms` - explain BMR and TDEE

The same flows are also available through reply and inline keyboard actions.

## Data and Storage

The current SQLite schema includes:

- `products`
- `product_aliases`
- `users`
- `user_products`
- `food_entries`
- `user_activity_overrides`

The starter seed currently provides `372` curated products with Russian names, aliases, categories, states, source references, and macros per 100 grams.

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

## Next Implementation Focus

The next practical work should improve reliability and product clarity rather than add a large new feature tier.

Recommended focus:

1. align developer tooling so tests run without manual `PYTHONPATH` setup
2. keep documentation synchronized with the implemented profile and assistant scope
3. strengthen parsing, search coverage, and user-facing copy for Russian-first input
4. decide whether the next product step is:
   - goal modes and target comparison
   - broader history and stored-entry UX
   - richer alias and parsing coverage

## Future Direction

The likely next growth layers remain:

1. goal modes and comparison against targets
2. richer diary/history behavior
3. editing and deletion
4. broader alias coverage and richer portion understanding

## Related Files

- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
- [Starter Products](F:\Python\CaloriesCounter\docs\starter-products.md)
