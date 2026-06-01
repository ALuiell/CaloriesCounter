# Seed Expansion Candidates

## Purpose

This document explains how USDA expansion candidates are generated and how to use that workflow to grow the starter seed further.

## Status

The starter seed has already been expanded to `372` products. This document is now a workflow reference rather than a pending to-do list.

## Expansion Method

The expansion workflow uses:

- [find_usda_candidates.py](F:\Python\CaloriesCounter\scripts\find_usda_candidates.py)
- [validate_starter_seed.py](F:\Python\CaloriesCounter\scripts\validate_starter_seed.py)
- the local USDA SR Legacy source file

Candidate selection rules:

- prefer generic USDA SR Legacy records
- exclude brands
- exclude restaurant and fast-food records
- exclude baby-food records
- prefer raw, cooked, plain, or simple baseline variants
- avoid noisy canned, salted, flavored, or overly prepared variants when a simpler equivalent exists

## Example Workflow

1. Search USDA candidates by category or keyword.
2. Review returned records for simple generic variants.
3. Add chosen records to the seed with:
   - `slug`
   - `name_ru`
   - `aliases`
   - `category`
   - `state`
   - USDA references
   - macros per 100 grams
4. Run seed validation.

Example commands:

```powershell
python scripts/find_usda_candidates.py --category vegetables --keyword spinach --limit 20
python scripts/find_usda_candidates.py --category legumes --keyword beans --limit 20
python scripts/validate_starter_seed.py
```

## Good Expansion Targets

Useful categories for future expansion:

- vegetables
- fruits and berries
- grains and side dishes
- legumes
- dairy products
- fish and seafood
- meat and poultry
- oils, nuts, and seeds

## Practical Rule

The goal is not to import USDA at full size. The goal is to continue growing a clean, user-friendly seed, even when some additions come from other reliable nutrition references.

That means:

- fewer noisy records
- more common foods
- better Russian aliases
- clear raw/cooked/dry state handling

## Related Files

- [Starter Products](F:\Python\CaloriesCounter\docs\starter-products.md)
- [USDA Analysis](F:\Python\CaloriesCounter\docs\usda-analysis.md)
- [Documentation Standard](F:\Python\CaloriesCounter\docs\documentation-standard.md)
