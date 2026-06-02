# UI Prompt And Visual Inventory

## Generated References

Stored in:

`assets/generated/reports/20260602-spread-system-assets/`

Files:

- `spread-system-01-selector-screen.png`
- `spread-system-02-layout-icon-sheet.png`
- `spread-system-03-three-card-in-progress.png`

## Adopted UI Ingredients

- Left spread list with compact layout diagrams and card counts.
- Center table with visible ghost slots before reveal.
- Bright electric-blue outline for the selected spread/card.
- Slot order markers that make reveal sequence clear.
- Right panel for selected spread or selected card guidance.
- Bottom action dock with shuffle/draw/reveal next/guide/save/reset.
- Black acrylic table, electric blue rings, restrained gold trim, blue crystals, and small cat emblems.

## Implementation Translation

- Layout preview diagrams should become code-native UMG or material/icon assets later, not raster text copied from the mockup.
- The native fallback HUD only needs clear metadata now: active spread, available spreads, and slot list.
- Final WBP should use a proper combo/list view for spread selection and a slot preview panel.
- Card labels, spread names, reveal order, notes, guide locks, and history summaries remain runtime text.
