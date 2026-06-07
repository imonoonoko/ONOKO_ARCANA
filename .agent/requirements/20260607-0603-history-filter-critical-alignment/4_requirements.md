# Requirements

## Goal

Saved readings can be narrowed by card, spread, and whether a saved card note exists, so the user can review learning evidence without turning the right inspector into a broad dashboard.

## User Stories

- As a learner, I can narrow saved readings to one spread type when I want to compare how a spread pattern reads over time.
- As a learner, I can show only readings with notes when I want useful review material.
- As a learner, I can show readings without notes when I want to find incomplete saved work.
- As a learner, I can clear filters and return to all history.

## Acceptance Criteria

- Existing card-specific filter still shows comparison blocks for matching cards.
- Spread filter limits visible rows to the selected spread.
- Note filter supports all, with notes, and without notes.
- Filter clear resets card, spread, and note filters together.
- Restore and delete still affect the intended original history item after filtering.
- Empty filtered results show a neutral message.
- Web smoke records the new filter behavior.
- Visual and keyboard checks are run after the UI change.

## Risks

- Too many controls can crowd the inspector.
- Filtered row indexes can point to the wrong history item if original indexes are lost.
- Manual installer evidence must not be overstated as verified.
