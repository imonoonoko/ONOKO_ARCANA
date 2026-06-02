# Scope

## In Scope

- Built-in spread metadata for:
  - One card
  - Past-present-future
  - Five-card cross
  - Seven-card horseshoe
  - Celtic cross
  - Relationship line
- Slot metadata per spread:
  - Position key
  - Display label
  - Reveal order
  - Guide prompt
  - Logical table location
  - Logical yaw
- Table-controller active spread selection.
- Native fallback HUD spread selector display.
- SaveGame forward-compatible fields for spread id, spread display name, position key/label, and card count.
- Commandlet-level smoke test for spread registry and table-controller selection.
- Design documentation that maps generated assets to implementation choices.

## Out Of Scope For This Slice

- Multiple simultaneous card actors in the Phase 1 map.
- Multi-card draw state.
- Per-slot card notes and guide reveal state.
- Final WBP styling pass.
- Importing generated mockup images into Unreal as UI textures.
- Small Arcana deck production.

## Non-Goals

- Do not promise every historical tarot spread variant. "All spreads" means all product-supported spreads in the ONOKO ARCANA catalog, with the catalog designed for extension.
- Do not bake labels or interpretation text into card art.
- Do not replace the existing one-card proof path before the multi-card model is tested.
