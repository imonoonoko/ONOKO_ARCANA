# ONOKO ARCANA Astra Nine-Slice HUD Kit - 2026-06-02

Dedicated `border-image` source frames generated for the Web/Electron HUD.

The previous modular kit remains useful for pips, rings, and decorative accents. This kit is for stretchable UI surfaces where a full image overlay would be too rigid.

## Files

- `astra-nine-slice-source-sheet-chroma-v1.png`: original chroma-key source generated with `imagegen`.
- `astra-nine-slice-source-sheet-alpha-v1.png`: transparent source sheet after green-key removal.
- `nine-slice/content-panel-frame-alpha-v1.png`: large panel frame.
- `nine-slice/title-plaque-frame-alpha-v1.png`: title/topbar plaque frame.
- `nine-slice/command-button-frame-alpha-v1.png`: command and spread-row frame.
- `nine-slice/tarot-slot-frame-alpha-v1.png`: empty tarot slot frame.
- `nine-slice-manifest.json`: crop metadata and recommended CSS slice values.
- `nine-slice-contact-sheet-v1.png`: visual review sheet.

## CSS Usage

These assets are intended for CSS `border-image` or low-opacity pseudo-element frame layers.

Current Web app variables:

```css
--hud-9-panel
--hud-9-plaque
--hud-9-button
--hud-9-slot
```

Keep labels and localized text in HTML. Do not bake text into these images.

## Validation

- Four alpha PNGs created.
- No visible chroma-green pixels detected.
- Integrated into `web-app/src/styles.css`.
- Verified by `scripts/check_web_app.py`, `scripts/smoke_web_app.cjs`, and `scripts/smoke_electron_app.cjs`.
