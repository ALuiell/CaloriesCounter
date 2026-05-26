# Implementation Plan

## Purpose

This document describes the recommended implementation order for the current active scope.

The implementation-ready scope is Level 1 only.

## Recommended Stack

- Python 3.12+
- `aiogram` or `python-telegram-bot`
- SQLite for MVP
- SQLAlchemy or SQLModel
- Pydantic for schemas
- Alembic for migrations

## Level 1 Build Order

Build:

- project structure
- `.env`-based configuration
- bot initialization
- database connection
- basic logging
- `products` table
- `product_aliases` table
- product import from the starter seed
- line-by-line message parsing
- product and gram extraction
- Russian-first product lookup
- calorie and macro calculation
- response formatting for recognized and unrecognized lines

## Level 1 Expected Result

After Level 1:

- the bot starts
- the bot responds to `/start`
- the bot explains the expected input format
- the bot accepts Russian-first `product + grams` messages
- the bot calculates calories and macros for recognized lines
- the bot reports unrecognized lines without failing the whole message
- the bot returns totals for the current message only

## Later Work

Planned after Level 1:

- profile onboarding
- base daily target calculation
- goal modes
- stored food entries
- daily totals
- history view
- editing and deletion
- broader alias coverage, including possible English and Ukrainian aliases
- better parsing hints and richer food input

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Parsing Strategy](F:\Python\CaloriesCounter\docs\parsing-strategy.md)
