# Scope

## In Scope For Preparation

- Contract for spread-aware session state.
- Contract for per-slot card state.
- Contract for selected slot and reveal-next behavior.
- SaveGame v2 shape for spread readings.
- First executable spread choice.
- Test and proof gates.
- External spread-definition fixture for validation.

## Out Of Scope For Preparation

- Implementing `UOnokoArcanaSpreadReadingSession`.
- Spawning or placing multiple card actors.
- Building polished `WBP_TableHUD`.
- Saving real multi-card readings.
- Importing generated image references into Unreal.

## First Executable Target

The first executable multi-card spread should be:

`three_card_past_present_future`

Reasons:

- It is easy to visually verify.
- It validates multiple slots, reveal order, selected-card guide, and face-down future card.
- It is a direct bridge from one-card to larger spreads.
- It avoids the complexity of Celtic Cross while proving the same data model.
