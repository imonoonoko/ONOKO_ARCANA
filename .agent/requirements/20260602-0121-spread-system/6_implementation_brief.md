# Implementation Brief

## First Code Slice

Add a small C++ spread catalog foundation:

- `OnokoArcanaSpreadDefinition.h/.cpp`
  - `EOnokoArcanaSpreadLayoutType`
  - `FOnokoArcanaSpreadSlotDefinition`
  - `FOnokoArcanaSpreadDefinition`
  - `UOnokoArcanaSpreadRegistry`
- `AOnokoArcanaTableController`
  - Owns `SpreadRegistry`
  - Owns `ActiveSpreadId`
  - Owns `ActiveSpreadDefinition`
  - Exposes `InitializeSpreadRegistry`, `SelectSpread`, `GetAvailableSpreads`, `GetActiveSpreadDisplayText`, `GetActiveSpreadSlotListText`, and `GetAvailableSpreadListText`
- `UOnokoArcanaTableHudWidget`
  - Optional `SpreadSelectorComboBox`
  - Optional `ActiveSpreadText`
  - Optional `SpreadSlotsText`
  - Native fallback creation of the selector and display rows
- `FOnokoArcanaSavedReading`
  - Add spread metadata fields while keeping existing fields intact

## Test Slice

Add a commandlet smoke script:

- `Unreal/ONOKO_ARCANA/Scripts/test_phase3_spread_registry.py`

The script should verify:

- Registry initializes.
- At least six spreads exist.
- Default id is `one_card`.
- `celtic_cross` has 10 slots.
- Table controller initializes and selects `three_card_past_present_future`.
- Invalid spread selection fails.

## Later Slices

- Replace single `CurrentDraw` with spread-aware card state.
- Add table actor/widget placement for all slots.
- Add reveal-next and selected-slot behavior.
- Extend SaveGame from single-card fields to a card-state array.
- Build polished `WBP_TableHUD` from the same widget names and contracts.
