# ONOKO ARCANA Astra Modular HUD Kit - 2026-06-02

This kit breaks the previous full-screen HUD direction into smaller game-ready UI parts.

Use the `*-alpha-v1.png` sheets for preview and the files under `components/` for implementation. The source `*-chroma-v1.png` files are kept as generation originals.

## Source Sheets

- `astra-modular-panels-alpha-v1.png`: large reusable panels, plaques, rails, dividers, and corner ornaments.
- `astra-micro-controls-alpha-v1.png`: buttons, pips, badges, small rails, seals, and ornamental caps.
- `astra-card-slots-alpha-v1.png`: tarot card slots, spread markers, reveal effects, connector lines, and spread progress bars.

## Split Components

- `components/panels/`: 14 cropped panel and frame parts.
- `components/controls/`: 37 cropped micro-control parts.
- `components/card-slots/`: 24 cropped spread and card-placement parts.
- `components-manifest.json`: crop metadata for every component.

## Practical Role Map

### Panels

- `panel-01`: compact title or action plaque.
- `panel-02`: vertical side panel frame for card detail or reading history.
- `panel-05`: medium content panel for guide text, note input, or spread summary.
- `panel-06`, `panel-07`: horizontal command/tab plaques.
- `panel-10`, `panel-11`: thin ornamental dividers.
- `panel-12`, `panel-14`: button or status capsule frames.
- `panel-03`, `panel-04`, `panel-08`, `panel-09`: corner ornaments for custom frames.
- `panel-13`: wide bottom rail base.

### Controls

- `control-01` to `control-06`: circular icon-button bezels.
- `control-07` to `control-11`: gem pips and status gems.
- `control-12` to `control-15`: tab/header caps.
- `control-16` to `control-19`: small medallion status buttons.
- `control-20` to `control-22`: pill button frames.
- `control-23` to `control-25`: thin horizontal rails or sliders.
- `control-26`, `control-27`: vertical rails.
- `control-28` to `control-31`: corner caps.
- `control-32` to `control-35`: diamond separators.
- `control-36`, `control-37`: round seal medallions.

### Card Slots

- `slot-01` to `slot-03`: vertical tarot card slot frames.
- `slot-04`, `slot-05`: horizontal card slot frames.
- `slot-06`, `slot-11`, `slot-12`, `slot-13`: card focus or selection rings.
- `slot-07` to `slot-10`: reversed-position or card-state markers.
- `slot-14`, `slot-21`, `slot-24`: spread progress bars.
- `slot-15` to `slot-19`: reveal sparkle effects.
- `slot-20`, `slot-22`, `slot-23`: spread connector lines.

## Implementation Recommendation

Build the live HUD from code-native layout first, then layer these PNG components as decorative surfaces:

- Use panel crops as `border-image` / 9-slice candidates where possible.
- Use buttons and pips as image-backed states, not as baked text.
- Keep all labels, numbers, and localized text in HTML/UMG so the UI remains readable and expandable.
- Prefer `Astra Nocturne` visual language as the base, with Kurogane-like layout density for real gameplay screens.

## Contact Sheets

- `panels-components-contact-sheet-v1.png`
- `controls-components-contact-sheet-v1.png`
- `card-slots-components-contact-sheet-v1.png`
