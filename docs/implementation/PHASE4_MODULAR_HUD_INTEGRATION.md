# Phase 4 Modular HUD Integration

> Archive notice (2026-06-05): This UE HUD integration note is historical evidence. The active v1.x lane is Web/Electron; do not use this document as current next work.

Date: 2026-06-02

## Summary

The generated full-screen HUD direction was split into smaller reusable UI assets and integrated into the Web/Electron play surface as decorative layers.

This keeps the verified reading loop intact while making the screen feel more like an ONOKO oracle instrument.

## Requirement Artifact

```text
.agent/requirements/20260602-1330-modular-hud-integration/
```

## Asset Kit

```text
assets/generated/hud-elements/20260602-astra-modular-kit/
```

Generated and cropped assets:

- `components/panels/`: 14 PNGs
- `components/controls/`: 37 PNGs
- `components/card-slots/`: 24 PNGs

Implementation uses a small first-pass subset:

- `panels/panel-02.png`
- `panels/panel-05.png`
- `panels/panel-13.png`
- `controls/control-16.png`
- `controls/control-20.png`
- `card-slots/slot-06.png`
- `card-slots/slot-20.png`

## Implemented Changes

- Added CSS asset tokens for modular HUD PNGs.
- Added ONOKO-style plaque treatment to the brand block and topbar.
- Added side-panel frame accents without baking text into images.
- Added mini spread diagrams to every spread selector row.
- Added generated gem pips to stats, slot labels, and reveal progress.
- Added selected-card and card-slot decorative layers.
- Added bottom command rail ornament to the progress/status footer.
- Extended `scripts/check_web_app.py` to verify required modular HUD assets.

## Verification

Static check:

```text
python scripts/check_web_app.py
```

Latest report:

```text
reports/web-app-check-20260602-134738.json
```

Web smoke:

```text
cd web-app
npm run smoke:web
```

Latest report:

```text
reports/web-app-smoke-20260602-133704.json
```

Screenshots:

```text
reports/onoko-arcana-web-app-celtic-20260602-133704.png
reports/onoko-arcana-web-app-mobile-20260602-133704.png
```

Electron smoke:

```text
cd web-app
npm run smoke:electron
```

Latest report:

```text
reports/electron-app-smoke-20260602-133824.json
```

Screenshot:

```text
reports/onoko-arcana-electron-smoke-20260602-133824.png
```

## Remaining UI Risks

- Dedicated 9-slice source frames were added after the first modular integration pass:

```text
assets/generated/hud-elements/20260602-astra-nine-slice-kit/
```

- The Web/Electron HUD now uses these assets for panel, plaque, command, spread-row, selected-card, and empty-slot frame treatment.
- The older modular kit remains in use for pips, rings, connectors, and decorative accents.
- The button frame treatment is now richer, but active/disabled variants can still be tuned.
- Future UE/UMG import should use the same modular asset naming, not a full-screen overlay.

## 2026-06-02 Nine-Slice Verification

Static check:

```text
reports/web-app-check-20260602-195003.json
```

Web smoke:

```text
reports/web-app-smoke-20260602-195055.json
reports/onoko-arcana-web-app-celtic-20260602-195055.png
reports/onoko-arcana-web-app-mobile-20260602-195055.png
```

Electron smoke:

```text
reports/electron-app-smoke-20260602-195216.json
reports/onoko-arcana-electron-smoke-20260602-195216.png
```

## 2026-06-02 Image-Based HUD Switch

The HUD was switched from mostly semi-transparent window surfaces to image-backed HUD surfaces.

Changed surfaces:

- main side panels and inspector,
- brand plaque,
- question and note fields,
- spread selector rows,
- status counters,
- topbar and command buttons,
- selected-card panel,
- guide rows,
- history rows,
- progress chips,
- empty tarot slots.

Implementation notes:

- Removed the glass-window feel by replacing the old translucent panel base with solid HUD surface tokens.
- Kept the 9-slice frame assets as the primary visual source for stretchable HUD surfaces.
- Kept text, labels, notes, and guide content as real HTML text.
- Kept decorative pips/rings as secondary image accents.

Latest verification:

```text
reports/web-app-check-20260602-201703.json
reports/web-app-smoke-20260602-201756.json
reports/onoko-arcana-web-app-celtic-20260602-201756.png
reports/onoko-arcana-web-app-mobile-20260602-201756.png
reports/electron-app-smoke-20260602-201918.json
reports/onoko-arcana-electron-smoke-20260602-201918.png
```

## 2026-06-02 Readability / Table Image Follow-Up

The screenshot review found that the left spread/status area was visually crowded, the center still felt like a transparent grid HUD, and revealed cards still had extra blue wrapper styling around the card art.

Implemented changes:

- Reduced decoration opacity and side ornament pressure in spread selector rows.
- Added a stronger text backing layer for spread labels/descriptions.
- Simplified status counters by removing the extra pip overlap and tightening text sizing.
- Added `astra-nocturne-background-v1.png` as the central table background image.
- Removed slot-ring rendering around filled/revealed cards.
- Removed the selected card's rectangular blue outline and used card-image glow instead.
- Replaced `.card-chip` overlays with `.card-inscription` labels aligned to the card art's own top/bottom plates.
- Added the table background image to `scripts/check_web_app.py` required asset validation.

Latest verification:

```text
reports/web-app-check-20260602-204212.json
reports/web-app-smoke-20260602-204247.json
reports/onoko-arcana-web-app-one-card-20260602114212.png
reports/onoko-arcana-web-app-celtic-20260602-204247.png
reports/onoko-arcana-web-app-mobile-20260602-204247.png
reports/electron-app-smoke-20260602-204403.json
reports/onoko-arcana-electron-smoke-20260602-204403.png
```

Visual result:

- The red-frame target area is readable on desktop and mobile screenshots.
- The table reads as a physical ONOKO-style arcana board rather than a transparent window.
- Revealed cards no longer carry a separate transparent HUD panel around them.
- Card names, orientations, and keywords now use the card art's built-in label areas.

## 2026-06-02 UI Audit Fixes

The visual audit found unreadable dense-spread card text, slot label collisions, mobile compression, inspector button/frame collision, and remaining spread-row ornament pressure.

Implemented fixes:

- One-card and three-card layouts retain in-card inscriptions.
- Five-card and larger layouts now use slot-number/position markers on cards instead of tiny in-card keyword text.
- Dense spread external board slot plaques were removed; readable slot names remain in the progress rail and inspector.
- Spread count moved into each mini spread diagram, freeing text space in the spread selector list.
- Progress chips now wrap instead of requiring a single horizontal row.
- Mobile dense boards use a taller table area and slightly larger cards.
- Guide/export compact buttons moved into vertical action rows away from section frame edges.
- Disabled button contrast increased.
- The visual audit script now distinguishes readable in-card layouts from marker-mode board previews.

Latest verification:

```text
reports/web-app-check-20260602-214641.json
reports/ui-visual-audit-20260602-214512/report.json
reports/web-app-smoke-20260602-214641.json
reports/electron-app-smoke-20260602-214739.json
```

Latest screenshots:

```text
reports/ui-visual-audit-20260602-214512/desktop-seven-horseshoe.png
reports/ui-visual-audit-20260602-214512/mobile-relationship-line.png
reports/onoko-arcana-web-app-celtic-20260602-214641.png
reports/onoko-arcana-electron-smoke-20260602-214739.png
```

Audit status:

```text
P1: 0
P2: 0
P3: 51 card-card-overlap
```

The remaining P3 records were addressed in the 2026-06-03 P3 closure pass below.

## 2026-06-03 P3 Card Overlap Closure

The user requested completing all remaining P3 work instead of keeping dense-layout card overlap as informational.

Implemented changes:

- Spaced out three-card, five-card cross, seven-card horseshoe, Celtic cross, and relationship-line slot coordinates.
- Reduced dense spread card widths while keeping marker-mode card previews identifiable.
- Changed Celtic cross crossing from a literal overlap to a separate readable card slot for the 2D tabletop UI.
- Reworked relationship-line into a balanced two-row spread.

Latest verification:

```text
reports/web-app-check-20260603-002748.json
reports/ui-visual-audit-20260603-002707/report.json
reports/web-app-smoke-20260603-002749.json
reports/electron-app-smoke-20260603-002749.json
```

Latest screenshots:

```text
reports/ui-visual-audit-20260603-002707/desktop-seven-horseshoe.png
reports/ui-visual-audit-20260603-002707/desktop-celtic-cross.png
reports/ui-visual-audit-20260603-002707/compact-five-cross.png
reports/ui-visual-audit-20260603-002707/compact-relationship-line.png
reports/ui-visual-audit-20260603-002707/mobile-seven-horseshoe.png
reports/onoko-arcana-web-app-celtic-20260603-002749.png
reports/onoko-arcana-web-app-mobile-20260603-002749.png
reports/onoko-arcana-electron-smoke-20260603-002749.png
```

Audit status:

```text
issueCount: 0
P1: 0
P2: 0
P3: 0
```
