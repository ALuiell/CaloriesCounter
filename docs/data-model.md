# Data Model

## Purpose

This document defines the data structures used by the current bot and the main expected expansion points.

## Current Core Entities

### Product

Imported product record used for lookup and macro calculation.

Current fields:

- `id`
- `slug`
- `name_ru`
- `normalized_name_ru`
- `category`
- `state`
- `usda_description`
- `fdc_id`
- `usda_category`
- `calories_per_100g`
- `protein_per_100g`
- `fat_per_100g`
- `carbs_per_100g`
- `is_active`
- `created_at`
- `updated_at`

Notes:

- `name_ru` is the main display and lookup name
- normalized fields are used for exact normalized matching
- macros are stored per 100 grams

### ProductAlias

Lookup variants for products.

Current fields:

- `id`
- `product_id`
- `alias`
- `normalized_alias`
- `language`
- `created_at`

Notes:

- current primary language is Russian
- normalized aliases are indexed for fast lookup

### User

Current profile and assistant-mode user record.

Current fields:

- `id`
- `telegram_id`
- `username`
- `assistant_enabled`
- `sex`
- `age`
- `height_cm`
- `weight_kg`
- `activity_level`
- `created_at`
- `updated_at`

Notes:

- the profile is considered complete only when all profile fields are filled
- `assistant_enabled` controls whether diary-style replies and entry storage are active

### UserProduct

User-scoped product or prepared meal added by a Telegram user.

Current fields:

- `id`
- `user_id`
- `name_ru`
- `normalized_name_ru`
- `calories_per_100g`
- `protein_per_100g`
- `fat_per_100g`
- `carbs_per_100g`
- `is_active`
- `created_at`
- `updated_at`

Notes:

- personal products are unique by user and normalized name
- personal products are visible only to their owner
- lookup checks personal products before the shared curated database
- deletion is currently a soft delete through `is_active`

### FoodEntry

Stored recognized food item used for daily totals.

Current fields:

- `id`
- `user_id`
- `product_source`
- `product_id`
- `user_product_id`
- `raw_item_text`
- `product_text`
- `weight_g`
- `calories`
- `protein_g`
- `fat_g`
- `carbs_g`
- `consumed_at`
- `created_at`

Notes:

- entries are currently used for `/today`
- storage is tied to assistant-mode flows
- entries can point to either a shared product or a personal product

### UserActivityOverride

Temporary activity selection for the current day.

Current fields:

- `id`
- `user_id`
- `activity_level`
- `activity_date`
- `created_at`
- `updated_at`

Notes:

- one override is allowed per user per date
- if no override exists for today, the profile activity level is used

## Derived Domain Objects

The service layer also uses derived objects:

- `UserProfile` - read model for current profile state
- `DailyNutritionTargets` - BMR, TDEE, macro targets, and effective activity metadata

These are runtime objects, not database tables.

## Recommended Indexes

Current indexes:

- `products.normalized_name_ru`
- `product_aliases.normalized_alias`
- `users.telegram_id`
- `user_products.user_id + normalized_name_ru`
- `food_entries.user_id + consumed_at`
- `user_activity_overrides.user_id + activity_date`

## Expansion Points

Likely later additions:

- goal fields for target adjustment
- richer history queries
- personal product aliases and edit/delete flows
- optional parse logging if operational visibility becomes necessary

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Starter Products](F:\Python\CaloriesCounter\docs\starter-products.md)
- [Architecture](F:\Python\CaloriesCounter\docs\architecture.md)
