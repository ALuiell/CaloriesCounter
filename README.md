# CaloriesCounter

## Purpose

CaloriesCounter is a Telegram bot project for calorie and macro tracking from plain text food messages.

The current implementation target is a clean Level 1 MVP:

- Russian-first food input
- `product + grams` parsing
- lookup in a curated starter database
- calories, protein, fat, and carbs per message

## Current State

The documentation source of truth for active work is:

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)

Use it first to understand:

- what the project is building now
- what is already prepared
- what is explicitly out of scope
- what the next implementation step is

## Documentation Map

Core entry and current-state document:

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)

Product documents:

- [Product Vision](F:\Python\CaloriesCounter\docs\product-vision.md)
- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Roadmap](F:\Python\CaloriesCounter\docs\roadmap.md)

Technical documents:

- [Architecture](F:\Python\CaloriesCounter\docs\architecture.md)
- [Data Model](F:\Python\CaloriesCounter\docs\data-model.md)
- [Parsing Strategy](F:\Python\CaloriesCounter\docs\parsing-strategy.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
- [GCP Deployment Recommendations](F:\Python\CaloriesCounter\docs\gcp-deployment-recommendations.md)

Data and analysis documents:

- [Starter Products](F:\Python\CaloriesCounter\docs\starter-products.md)
- [USDA Analysis](F:\Python\CaloriesCounter\docs\usda-analysis.md)
- [Seed Expansion Candidates](F:\Python\CaloriesCounter\docs\seed-expansion-candidates.md)

## Data Assets

- starter seed:
  - [starter_products_usda_sr_legacy.json](F:\Python\CaloriesCounter\data\seeds\starter_products_usda_sr_legacy.json)
- USDA analysis report:
  - [usda_sr_legacy_analysis.json](F:\Python\CaloriesCounter\data\analysis\usda_sr_legacy_analysis.json)
- local USDA source dataset:
  - `FoodData_Central_sr_legacy_food_json_2018-04.json`

The large USDA source file is intentionally excluded from git.
