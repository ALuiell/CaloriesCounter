# Functional Requirements

## Purpose

This document defines the required user-facing behavior for the current MVP scope.

The detailed implementation scope is Level 1 only.

## Level 1 Scope

At Level 1, the bot must:

- accept one or more food lines in a single message
- support the format `product name + grams`
- treat Russian as the primary input language
- parse each line independently
- find products in the database by imported product names and aliases
- calculate calories and macros for the entered weight
- sum recognized lines from the current message
- return a short result for the current message

Level 1 does not require:

- user profiles
- daily targets
- goal modes
- saved history
- daily totals
- remaining intake output

## Input Expectations

Supported examples:

```text
гречка 100
рис 120 г
курица 150 грамм
```

Input rules:

- one line represents one product
- each line must contain a numeric gram value
- the numeric value is interpreted as grams
- the remaining text is interpreted as the product name

## Recognition and Error Handling

If a line is recognized, the bot must:

- calculate calories
- calculate protein
- calculate fat
- calculate carbs
- include that line in the total

If a line is not recognized, the bot must:

- keep processing the rest of the message
- show that the line could not be recognized
- remind the user to use the `product + grams` format when helpful

The whole message should not fail because one line failed.

## Output Requirements

After processing a message, the bot must return:

- recognized lines
- unrecognized lines, if any
- the total calories and macros for recognized lines only

Example response:

```text
Calculated:
- гречка 100 г
- курица 150 г

Could not recognize:
- домашний пирог кусок

Total:
410 kcal
Protein: 36 g
Fat: 8 g
Carbs: 43 g
```

## Commands

Minimum command set:

- `/start` - start the bot
- `/help` - usage help
- `/calc` - input format help

## Future Levels

Later planned work:

- Level 2: profile data and base daily target calculation
- Level 3: goal modes and target comparison
- after Level 3: stored entries, daily totals, history, editing, and richer reporting

These are future capabilities and are not part of the current Level 1 requirements.

## Non-Functional Requirements

- Bot responses must be fast and understandable.
- The system must handle Cyrillic input correctly.
- The product database must be easy to expand.
- The system should tolerate partially valid messages.
- The architecture should support later additions such as broader alias coverage, recipes, and portion handling.

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Parsing Strategy](F:\Python\CaloriesCounter\docs\parsing-strategy.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
