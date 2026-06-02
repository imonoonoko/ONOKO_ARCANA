# Requirements

## Runtime Requirements For Phase 4

1. Phase 4 shall introduce a spread-aware session rather than rewriting the one-card session.
2. A spread reading shall own a question, spread id, deck id, card states, selected slot, summary note, and guide state.
3. Each card state shall bind exactly one spread slot to zero or one drawn card.
4. Draw spread shall draw one unique card per slot from the deck runtime.
5. Cards shall begin face-down unless explicitly revealed.
6. Reveal next shall reveal the lowest unrevealed reveal order.
7. Reveal selected shall reveal only the selected slot.
8. Guide text shall remain locked per slot until that slot is revealed.
9. User notes shall be storable per slot and at spread summary level.
10. The first executable spread shall be `three_card_past_present_future`.
11. Non-one-card spreads beyond the first executable spread may remain metadata-only until their placement and review proof is ready.
12. Existing one-card draw/reveal/save/history behavior shall continue to pass its commandlet tests.

## Save Requirements For Phase 4

1. Existing one-card saves shall remain readable.
2. A spread reading save shall store an array of card states.
3. Each saved card state shall include position key, position label, reveal order, card id, card names, orientation, active keywords, study focus, user note, revealed state, and guide revealed state.
4. SaveGame schema version shall be explicit.
5. History ViewModel shall expose spread summary and selected-card detail.

## Acceptance Criteria For First Phase 4 Slice

- Commandlet can create a three-card spread session.
- It can draw exactly three unique cards.
- Reveal-next reveals slots in order 1, 2, 3.
- Selected slot changes guide/detail output.
- Saved spread reading reloads with three card states.
- Existing Phase 1 tests still pass.
