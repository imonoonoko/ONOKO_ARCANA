# Implementation Brief

## C++ Plan

- `AOnokoArcanaTableController`
  - Add `SelectSpreadSlot(FName PositionKey)`.
  - Add `GetSelectedSpreadSlotText()`.
  - Call `SyncSpreadCardActors()` after selection to visually emphasize the selected card.

- `UOnokoArcanaTableHudWidget`
  - Add `SelectedSpreadSlotText`.
  - Add `PastSlotButton`, `PresentSlotButton`, `FutureSlotButton`.
  - Add click handlers for each slot.
  - Enable buttons only for active non-one-card spreads.

## Verification

- Build game target.
- Build editor target.
- Run Phase 4 commandlets/checkers.
- Capture a new three-card demo screenshot.
