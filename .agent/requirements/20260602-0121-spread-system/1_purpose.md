# Purpose

ONOKO ARCANA should eventually let the user select from all product-supported tarot spreads, lay cards into visible slots, reveal them in order, write their own interpretation, then unlock guide text and save the reading.

The purpose of this slice is to start that future without breaking the current Phase 1 proof. The current one-card table remains the only fully executable reading flow, but the code and HUD should gain a spread catalog and selection surface so that one-card is just one `SpreadDefinition`, not a hard-coded product shape.

## Success Criteria

- A durable requirement and implementation handoff exists under `.agent/requirements/`.
- New generated visual references exist for spread selection and slot/layout previews.
- C++ exposes built-in spread definitions to Blueprint/UMG.
- The table controller can initialize and select an active spread id.
- The native fallback HUD can show the active spread and available spread list.
- Saving a one-card reading records spread metadata for forward compatibility.
- Existing one-card draw, reveal, guide, save, and history behavior remains intact.
