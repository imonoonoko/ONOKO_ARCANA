# Spread System Visual Direction

Updated: 2026-06-02

## Purpose

This note extends `docs/design/multi-spread-visual-direction-2026-06-02.md` with implementation-ready references for the spread-selection layer.

The immediate product goal is not to make the current Phase 1 screen visually crowded. The goal is to make spread choice, slot order, and selected-card guidance feel like first-class parts of ONOKO ARCANA before multi-card runtime work begins.

## New Generated References

Generated with `image-first-frontend` plus `imagegen` and copied into:

`assets/generated/reports/20260602-spread-system-assets/`

| File | Use |
|---|---|
| `spread-system-01-selector-screen.png` | Best reference for a future spread-selection screen: left spread list, center table preview, right learning flow, bottom action dock. |
| `spread-system-02-layout-icon-sheet.png` | Best reference for compact spread icons and card-slot decals. Do not use its text directly; recreate labels in UMG. |
| `spread-system-03-three-card-in-progress.png` | Best reference for the in-reading state: selected card outline, reveal progress, note-first guide unlock, and future face-down slot. |

## Adopted Details

- A spread list should show card count and a tiny layout diagram.
- The table should show ghost slots before reveal, not just cards after draw.
- Reveal order should be visible as small numbered markers.
- The selected card or selected slot should drive the right-side guide panel.
- The bottom action dock should read as the future flow: shuffle, draw, reveal next, guide, save, reset.
- ONOKO identity should stay in materials and small motifs: black acrylic, electric-blue rings, restrained gold, blue crystals, and cat emblems.

## Excluded Details

- Generated English labels are reference-only.
- Generated handwritten notes are mood-only; user note text must be real editable UI.
- Large decorative portraits remain out of the default reading screen.
- Raster spread icons are not imported into Unreal in this pass. Rebuild the final icons as UMG/vector/material assets when polishing the WBP.

## Implementation Implication

The first C++ pass introduces a spread catalog and HUD metadata display. Full multi-card rendering should then reuse the same definitions for actor placement and reveal order:

- `SpreadId`
- `DisplayName`
- `LayoutType`
- `Slots`
- `PositionKey`
- `RevealOrder`
- `TableLocationCm`
- `TableYawDegrees`
