# Architecture

## Purpose

This document describes the recommended project structure and responsibility split for the MVP foundation.

## Architectural Approach

For MVP, a simple modular architecture is recommended:

- `bot` - Telegram handlers and flows
- `services` - business logic
- `repositories` - database access
- `models` - ORM models
- `schemas` - input and output schemas
- `parsers` - text message parsing
- `utils` - shared helper functions

## Proposed Project Structure

```text
CaloriesCounter/
  app/
    bot/
      handlers/
      keyboards/
      middlewares/
    core/
      config.py
      logging.py
    db/
      models/
      repositories/
      migrations/
    services/
      nutrition_service.py
      profile_service.py
      diary_service.py
    parsers/
      food_parser.py
    schemas/
      user.py
      food_entry.py
      nutrition.py
    main.py
  docs/
  tests/
```

## Main Modules

### Nutrition Service

Current Level 1 priority:

- product lookup
- calorie and macro calculation
- result aggregation for the current message

### Food Parser

Current Level 1 priority:

- splitting messages into lines
- extracting product name and weight
- text normalization
- returning structured parse results

### Profile Service

Planned for later levels:

- profile creation
- profile updates
- daily target calculation

### Diary Service

Planned for later levels:

- saving entries
- daily totals
- entry editing
- entry deletion

## Why This Structure Works

- it is easy to test by module
- it keeps Telegram-specific code separate from business logic
- it supports later database changes
- it makes future feature growth easier

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Data Model](F:\Python\CaloriesCounter\docs\data-model.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
