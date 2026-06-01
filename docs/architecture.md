# Architecture

## Purpose

This document describes the current project structure and responsibility split.

## Architectural Approach

The project uses a compact modular structure:

- `handlers` - Telegram command, button, and FSM flows
- `services` - business logic for nutrition, parsing, normalization, and profile behavior
- `db` - SQLite schema bootstrap and seed import
- `schemas` - structured nutrition result models
- `core` - configuration and logging

## Current Project Structure

```text
CaloriesCounter/
  app/
    core/
      config.py
      logging.py
    db/
      database.py
      seed.py
    handlers/
      bot.py
    schemas/
      nutrition.py
    services/
      normalization.py
      nutrition.py
      parser.py
      profile.py
    bot.py
    main.py
  data/
  docs/
  scripts/
  tests/
```

## Main Modules

### Nutrition Service

Current responsibilities:

- parse food messages through the parser service
- resolve products by normalized Russian name or alias
- calculate calories and macros
- format calc and assistant replies
- persist recognized items for assistant-mode diary behavior
- aggregate current-day totals
- search products
- create and resolve personal user-scoped products

### Food Parser

Current responsibilities:

- split messages into independent items
- accept comma-separated and newline-separated input
- extract product name and weight
- return structured parse results even for partially invalid input

### Profile Service

Current responsibilities:

- ensure user records exist
- create and update profile fields
- validate activity levels
- calculate BMR and TDEE
- derive approximate daily macro targets
- manage current-day activity overrides
- expose complete-profile checks for assistant mode

### Database Layer

Current responsibilities:

- initialize SQLite schema
- apply lightweight legacy migration support
- expose timezone-aware timestamps and current local date
- support tables for products, aliases, users, food entries, and activity overrides
- support personal products without exposing them to other users

## Why This Structure Works

- it is easy to test by service
- it keeps Telegram-specific code separate from business logic
- it keeps the SQLite MVP lightweight
- it supports further growth into goals, history, and richer parsing

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Data Model](F:\Python\CaloriesCounter\docs\data-model.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
