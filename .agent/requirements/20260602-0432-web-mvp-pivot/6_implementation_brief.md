# Implementation Brief

## Target

Create `web-app/index.html` as the production-oriented Web app and keep `prototype/onoko-arcana-web-mvp-v1.html` as historical evidence.

## Architecture

- Direct-open static Web app.
- Separated HTML, CSS, data, and app runtime files.
- No build step.
- Relative asset references so the app can be opened locally and later moved into Electron/Tauri.
- Local state only:
  - current spread,
  - drawn cards,
  - reveal index,
  - selected slot,
  - per-slot notes,
  - `localStorage` history.

## Data

Use an inline major arcana list with V5 alpha image paths derived from:

- `data/major-arcana-v5-deck.json`
- `assets/generated/card-production-v5-full/alpha/`

Use spread definitions matching every spread currently in `data/spread-definitions-v1.json`.

## Verification

Add `scripts/check_web_app.py` to verify:

- Web app files exist,
- required UI ids exist,
- required asset paths exist,
- all card image paths referenced by the app exist,
- all spread ids are present,
- Electron shell keeps renderer isolation enabled.

Add `scripts/smoke_web_app.cjs` to verify:

- all spread choices render,
- relationship line reveals six cards,
- guide is disabled until a note exists,
- Celtic cross reveals ten cards,
- readings save to history,
- desktop and mobile screenshots can be captured without console errors.

Add `scripts/smoke_electron_app.cjs` to verify:

- Electron launches `web-app/electron/main.cjs`,
- relationship line can be drawn and revealed in the Electron window,
- guide remains disabled until a note exists,
- history save works inside Electron,
- an Electron screenshot can be captured without console errors.
