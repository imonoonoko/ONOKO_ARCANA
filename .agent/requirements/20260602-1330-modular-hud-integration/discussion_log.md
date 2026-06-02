# Discussion Log

## 2026-06-02

- The previous full-screen generated HUD looked strong but was too rigid for real gameplay layouts.
- The user requested finer HUD elements generated with `imagegen`.
- A modular Astra Nocturne HUD kit was generated and split into 75 transparent PNG components:
  - `components/panels/`: 14 parts
  - `components/controls/`: 37 parts
  - `components/card-slots/`: 24 parts
- This pass defines and implements the next slice: integrate selected modular HUD parts into the existing Web/Electron game screen without changing the verified reading loop.

## 2026-06-02 Nine-Slice Follow-Up

- The user agreed to replace rigid/stretched modular parts with dedicated 9-slice source frames.
- A new `imagegen` source sheet was generated, chroma-keyed, and split into:
  - `content-panel-frame-alpha-v1.png`
  - `title-plaque-frame-alpha-v1.png`
  - `command-button-frame-alpha-v1.png`
  - `tarot-slot-frame-alpha-v1.png`
- The Web/Electron HUD now uses the 9-slice kit for stretchable panel, plaque, command, spread-row, selected-card, and empty-slot framing.

## 2026-06-02 Image-Based HUD Switch

- The user requested switching the HUD fully away from transparent-window styling to image-based HUD styling.
- Main HUD surfaces now use solid surface tokens and 9-slice image frames instead of glass-like translucent panel backgrounds.
- Web and Electron smoke checks passed after the switch.

## 2026-06-02 Readability / Table Image Follow-Up

- The user pointed out four visible issues in screenshots:
  - The left spread selector and status area are hard to read because decorative HUD pieces crowd the text.
  - Revealed cards still carry extra transparent/blue HUD framing around the card art.
  - Card art includes built-in top/bottom text plates that the UI was not using.
  - The central board should feel more like a physical table, using an image background inspired by the kanban-board reference.
- Acceptance criteria for this pass:
  - Reduce left-side decoration density and preserve text contrast.
  - Remove the transparent card wrapper effect around revealed cards.
  - Move revealed card labels/keywords into the card's own label plate areas.
  - Use an existing generated background image for the central table surface.
  - Verify the result by inspecting actual desktop, mobile, and Electron screenshots.
- Implementation completed in the Web/Electron app:
  - `web-app/src/styles.css`
  - `web-app/src/app.js`
  - `scripts/check_web_app.py`
- Visual evidence:
  - `reports/onoko-arcana-web-app-one-card-20260602114212.png`
  - `reports/onoko-arcana-web-app-celtic-20260602-204247.png`
  - `reports/onoko-arcana-web-app-mobile-20260602-204247.png`
  - `reports/onoko-arcana-electron-smoke-20260602-204403.png`
