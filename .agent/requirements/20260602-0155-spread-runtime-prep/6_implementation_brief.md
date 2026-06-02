# Implementation Brief

## Add New Runtime Types

Recommended files:

- `OnokoArcanaSpreadReadingSession.h/.cpp`
- `OnokoArcanaSpreadReadingViewModel.h/.cpp`

Recommended structs:

- `FOnokoArcanaReadingCardState`
- `FOnokoArcanaSpreadReadingState`

## Suggested C++ Shape

`FOnokoArcanaReadingCardState`

- `PositionKey`
- `PositionLabel`
- `RevealOrder`
- `FOnokoArcanaDrawResult Draw`
- `bHasDraw`
- `bRevealed`
- `bSelected`
- `UserInterpretation`
- `bGuideRevealed`

`UOnokoArcanaSpreadReadingSession`

- `InitializeMajorArcanaV5()`
- `StartNewReading(Question, SpreadDefinition, Seed, bUseSeed)`
- `DrawSpread(bAllowReversed)`
- `SelectSlot(PositionKey)`
- `RevealSelected()`
- `RevealNext()`
- `SubmitSlotInterpretation(PositionKey, Text)`
- `RevealSelectedGuide()`
- `ResetReading()`

## Implementation Order

1. Add structs and session class with commandlet-only tests.
2. Draw three-card spread state without card actors.
3. Add view model text outputs for selected slot and progress.
4. Extend SaveGame with spread card-state array.
5. Add table-controller routing for `three_card_past_present_future`.
6. Add runtime actor placement only after state and save tests pass.
7. Add Editor/PIE visual proof.

## Stop Conditions

Stop and fix before continuing if:

- one-card commandlets fail.
- spread fixture validation fails.
- three-card draw duplicates cards.
- save migration breaks existing one-card load.
- Python map actor spawn is required for proof.

## Prep Checker

Run before Phase 4 work:

```text
python scripts/check_phase4_spread_runtime_prep.py
```

Expected output:

- `reports/phase4-spread-runtime-prep-check-*.json`

## Implementation Result

Completed in the first Phase 4 runtime slice:

- steps 1-4 are implemented and commandlet-proven.
- spread SaveGame state is additive and keeps one-card fields.
- `three_card_past_present_future` now supports draw, ordered reveal, per-slot notes, guide gating, reset, ViewModel display, and save/load round trip.

Still pending:

- table-controller routing for selected multi-card spreads.
- runtime actor/UMG slot presentation.
- Editor/PIE screenshot proof for a completed three-card spread.
