# Documentation Standard

## Purpose

This document defines the documentation style and document ownership model used in the project.

## Language

- All Markdown documentation must be written in English.

## Structure

Most documents should follow this order:

1. `# Title`
2. `## Purpose`
3. Main content sections
4. `## Related Files` or `## Next Steps`

## Style Rules

- Use short, direct section names.
- Prefer flat bullet lists.
- Use fenced code blocks for commands and examples.
- Keep naming and terminology consistent across documents.
- Avoid duplicating current-state information across many files.
- Keep implementation-ready detail focused on the current active scope.

## Document Ownership

- `README.md` - short repository entry and navigation
- `handover.md` - current operational source of truth
- `product-vision.md` - product intent and boundaries
- `functional-requirements.md` - current expected behavior
- `implementation-plan.md` - current build order
- `roadmap.md` - future sequence only

Other documents should support these core files rather than repeat them.

## Document Groups

Core working documents:

- `handover.md`
- `functional-requirements.md`
- `implementation-plan.md`
- `roadmap.md`
- `product-vision.md`

Technical support documents:

- `architecture.md`
- `data-model.md`
- `parsing-strategy.md`

Data and analysis documents:

- `starter-products.md`
- `usda-analysis.md`
- `seed-expansion-candidates.md`

Project support documents:

- `README.md`
- `progress-levels.md`
