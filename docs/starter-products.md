# Starter Products

## Purpose

This document describes the curated starter seed used for Level 1 product lookup and macro calculation.

## Source Files

- [starter_products_usda_sr_legacy.json](F:\Python\CaloriesCounter\data\seeds\starter_products_usda_sr_legacy.json)
- [products_international_sources.json](F:\Python\CaloriesCounter\data\products_international_sources.json)
- source dataset: `FoodData_Central_sr_legacy_food_json_2018-04.json`

## Current Scope

The current starter seed contains `372` curated products.

Category coverage:

- vegetables - `32`
- grains and side dishes - `28`
- legumes - `22`
- fruits and berries - `27`
- dairy products - `21`
- meat and poultry - `26`
- fish and seafood - `23`
- bread and baked products - `12`
- bakery - `17`
- cakes and desserts - `23`
- soups - `10`
- salads and snacks - `11`
- sweets - `32`
- drinks - `30`
- nuts and seeds - `11`
- fats and oils - `7`
- eggs - `6`
- sauces - `5`

## Role in the MVP

The starter seed is the Level 1 lookup foundation.

It is still mostly USDA-based, but now also includes a larger layer of curated external-source products, prepared dishes, sweets, and drinks where USDA coverage is awkward or too noisy.

It exists to provide:

- Russian product names for primary lookup
- Russian aliases for user-entered variants
- explicit product states where nutrition differs materially
- practical product coverage without full USDA runtime noise

The current seed should not be treated as a multilingual product catalog.

## Record Structure

Each product entry contains:

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

## Recommended Import Model

For Level 1, this seed should be imported into:

- a `products` table for the main product record
- a `product_aliases` table for imported aliases

Recommended lookup order:

1. exact normalized `name_ru` match
2. normalized alias match
3. later: clarification when multiple candidates match

## Important Modeling Rule

Some products vary significantly by preparation state.

Recommended defaults:

- treat `rice`, `buckwheat`, `pasta`, `lentils`, and `chickpeas` as cooked by default
- only use dry or raw variants when the user explicitly says `dry`, `raw`, or an equivalent form
- keep meat and fish in a small number of clear default forms instead of trying to cover every cooking method immediately

## Expansion Direction

Later improvements may include:

- English aliases
- Ukrainian aliases
- additional common Russian variants
- gradual seed expansion from USDA and other reliable nutrition sources

The goal is still a clean user-facing seed, not a full USDA mirror.

## Related Files

- [Data Model](F:\Python\CaloriesCounter\docs\data-model.md)
- [USDA Analysis](F:\Python\CaloriesCounter\docs\usda-analysis.md)
- [Seed Expansion Candidates](F:\Python\CaloriesCounter\docs\seed-expansion-candidates.md)
