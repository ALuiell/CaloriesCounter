# Roadmap

## Purpose

This document gives a high-level sequence for product growth after the current implemented baseline.

It is intentionally brief and should not duplicate current functional requirements.

## Current Baseline

The current product baseline already includes:

- reliable Russian-first `product + grams` calorie counting
- curated product lookup with aliases
- profile onboarding and editing
- BMR and TDEE calculation
- daily targets from profile data
- optional assistant mode
- `/today` daily totals
- `/search` product discovery
- per-day activity override
- personal user-added products and prepared meals
- category browsing
- listing and deleting personal products

## Planned Growth Sequence

### Next Priority

- make the current scope more reliable and easier to maintain
- improve parser and alias coverage
- improve developer tooling and run/test ergonomics

### Goal Layer

- add goal modes
- support `maintenance`
- support `gain`
- support `diet`
- compare intake against the selected target

### Diary Layer

- add history beyond the current day
- support editing and deletion of stored entries
- improve daily review UX

### Data and Input Layer

- improve search and alias coverage
- support editing personal products
- add recipes and richer units
- add freer AI-assisted input later if needed

## Success Direction

- The current bot feels dependable for the implemented profile and assistant flows.
- Goal features are layered on top of the existing target calculations.
- Diary and parsing improvements expand capability without breaking the simple core flow.

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
