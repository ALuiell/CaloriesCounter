# Parsing Strategy

## Purpose

This document defines the Level 1 parsing contract for user-entered food messages.

## Current Parsing Scope

The MVP parser is intentionally narrow:

- Russian-first input
- one product per line
- one numeric gram value per line
- `product + grams` as the supported contract

Supported examples:

```text
гречка 100
жареная курица 150 г
помидор 78
```

## Parsing Algorithm

1. Split the message into lines.
2. Remove extra whitespace.
3. Skip empty lines.
4. Extract the numeric value from each line.
5. Treat that value as grams.
6. Treat the remaining text as the product name.
7. Normalize the product text:
   - convert to lowercase
   - normalize whitespace
   - normalize common Russian variants and abbreviations if supported
8. Try exact product-name match or alias match.
9. If the product is found, calculate calories and macros.
10. If the product is not found, mark that line as unrecognized.

## Message-Level Behavior

The parser and response flow should support partial success.

That means:

- recognized lines are still calculated
- unrecognized lines are reported separately
- totals use recognized lines only

## First-Version Limits

The first version should not support:

- `2 eggs`
- `half a bowl of soup`
- `a slice of pizza`
- `a spoon of oil`
- composite recipes without explicit ingredients
- free-form multilingual understanding

## Error Handling

Recommended response pattern:

```text
Calculated:
- гречка 100 г
- помидор 78 г

Could not recognize:
- домашняя курица большая порция

Please use:
product name + weight in grams
Example: гречка 120 г
```

## Future Improvements

- English and Ukrainian aliases
- broader normalization rules
- fuzzy search
- clarification questions
- recipes and prepared dishes
- units and portions beyond grams

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Starter Products](F:\Python\CaloriesCounter\docs\starter-products.md)
