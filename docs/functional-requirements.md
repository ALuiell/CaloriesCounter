# Functional Requirements

## Purpose

This document defines the required user-facing behavior for the current implemented scope.

## Current Scope

The current bot must support:

- one or more food items in a single message
- Russian-first `product + grams` input
- product lookup by imported product names and aliases
- calories and macros for recognized items
- totals for the current message
- profile onboarding and profile editing
- BMR and TDEE calculation from profile data
- per-day activity override
- optional assistant mode
- current-day totals through `/today`
- product discovery through `/search`
- user-scoped personal products and prepared meals
- category browsing for shared products
- listing and deleting personal products

The current scope does not yet require:

- goal modes
- remaining intake coaching
- edit/delete flows for food entries
- history beyond the current day
- edit flows for personal products
- free-form portion understanding

## Food Input Expectations

Supported examples:

```text
гречка 100
рис 120 г
курица 150 грамм
гречка 120, курица 180
рис 100
помидор 80
```

Input rules:

- one item must contain a product name and a numeric gram value
- comma-separated and newline-separated input are both accepted
- the numeric value is interpreted as grams
- each item is parsed independently

## Recognition and Error Handling

If an item is recognized, the bot must:

- calculate calories
- calculate protein
- calculate fat
- calculate carbs
- include that item in the total

If an item is not recognized, the bot must:

- keep processing the rest of the message
- show that the item could not be recognized
- preserve partial success for the overall message

If nothing can be calculated, the bot must return a short format reminder with a `product + grams` example.

## Message Output Requirements

After processing a food message, the bot must return:

- recognized items
- unrecognized items, if any
- total calories and macros for recognized items only

If assistant mode is disabled, the reply should stay focused on the current message.

If assistant mode is enabled and the user has a complete profile, the food reply must also include:

- current-day totals
- BMR
- TDEE
- effective activity level for today
- approximate daily macro targets
- non-medical wording

## Profile Requirements

The bot must support a profile with these fields:

- sex
- age
- height in centimeters
- weight in kilograms
- default activity level

Profile behavior:

- an incomplete profile should trigger onboarding instead of full profile output
- a completed profile should be viewable
- a completed profile should be editable field by field
- assistant mode must not enable successfully until the profile is complete

## Activity Requirements

The bot must support:

- a default activity level stored in the profile
- a temporary activity override for the current local day
- clearing the current-day override

Daily targets must use:

- the override when it exists for today
- otherwise the default profile activity level

## Daily Totals Requirements

The bot must support stored food entries for assistant mode flows.

Behavior:

- recognized food items should be stored when assistant mode is enabled
- `/today` should sum entries for the current local calendar day only
- entries from previous days must not appear in `/today`

## Search Requirements

The bot must support product search by partial normalized query.

Search behavior:

- it should return matching database product names
- it should search both product names and aliases
- it should avoid duplicates
- it should cap the returned list to a small result set
- it should allow browsing shared products by category
- category product lists should include calories and macros per 100 grams

## Personal Product Requirements

The bot must support personal products and prepared meals.

Behavior:

- the user can add a product with name, calories, protein, fat, and carbs per 100 grams
- personal products must be scoped to the Telegram user
- one user's personal products must not affect lookup or search results for another user
- personal products should be available for normal food calculation
- personal products should be stored in `/today` totals when assistant mode stores recognized entries
- the user can list active personal products
- the user can delete personal products from their active lookup set

## Commands

Current command set:

- `/start` - start the bot and show the main menu
- `/help` - usage help
- `/calc` - food input help
- `/profile` - show or create profile
- `/edit_profile` - edit profile fields
- `/activity_today` - set today's activity
- `/activity_reset` - clear today's activity override
- `/assistant_on` - enable assistant mode
- `/assistant_off` - disable assistant mode
- `/today` - show current-day totals and targets
- `/search` - search products
- `/terms` - explain BMR and TDEE

## Non-Functional Requirements

- Bot responses must stay fast and understandable.
- The system must handle Cyrillic input correctly.
- The product database must remain easy to expand.
- The system must tolerate partially valid food messages.
- The design should support later additions such as goal modes, broader alias coverage, and richer food parsing.

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Parsing Strategy](F:\Python\CaloriesCounter\docs\parsing-strategy.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
