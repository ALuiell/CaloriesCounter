# Implementation Plan

## Purpose

This document describes the recommended implementation order for the current state of the project.

The original Level 1 runtime path is already implemented, along with profile and assistant foundations.

## Current Baseline

Already implemented:

- project structure
- `.env`-based configuration
- bot initialization
- SQLite connection and schema bootstrap
- starter seed import
- line-by-line and comma-split food parsing
- normalized lookup by Russian product name and aliases
- calorie and macro calculation
- user profile onboarding
- profile editing
- BMR and TDEE calculation
- today-specific activity override
- assistant mode
- persisted food entries for daily totals
- `/today` and `/search`
- personal user-added products and prepared meals
- category browsing
- listing and deleting personal products

## Recommended Next Build Order

Build next:

1. developer tooling reliability
2. parsing and lookup reliability
3. richer diary behavior
4. goal-aware targets

### 1. Developer Tooling Reliability

- make test runs work without manual `PYTHONPATH` setup
- standardize local run instructions
- keep test and runtime entrypoints simple

### 2. Parsing and Lookup Reliability

- expand parser coverage for common Russian input variants
- improve user-facing failure messages
- expand alias coverage in the curated seed
- strengthen search usefulness for product discovery

### 3. Richer Diary Behavior

- decide whether assistant mode remains the only entry-storage path
- add clearer history UX beyond `/today`
- prepare edit/delete behavior for stored entries

### 4. Goal-Aware Targets

- add `maintenance`, `gain`, and `diet` goal modes
- derive target calories from the selected goal mode
- compare current intake against the selected target without turning the bot into coaching software

## Current Expected Result

At the current stage, the bot should:

- start successfully
- respond to `/start`
- calculate calories and macros from Russian-first `product + grams` input
- tolerate partially valid food messages
- guide the user through profile completion
- calculate BMR and TDEE from a completed profile
- allow today's activity override
- show `/today` totals for stored entries
- search products with `/search`

## Later Work

Still planned after the current baseline:

- edit/delete flows for stored entries
- broader history
- broader alias coverage, including possible English and Ukrainian additions
- richer unit and portion understanding
- edit flows for personal products

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Parsing Strategy](F:\Python\CaloriesCounter\docs\parsing-strategy.md)
