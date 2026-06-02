# Discussion Log

## 2026-06-02 04:32 JST

User concern: the current Unreal Engine plus generated HUD direction started to feel unrealistic as the shortest path to a usable ONOKO ARCANA experience.

Decision captured for this slice:

- Treat Unreal Engine as a future premium 3D/PV target, not the immediate MVP dependency.
- Prove the core tarot reading loop in a lightweight Web prototype first.
- Keep existing V5 card art, spread metadata, Japanese study copy, memo, reveal, and history behavior as reusable product contracts.
- Avoid new build dependencies in this slice. A static HTML prototype is enough to validate the play surface and can later be wrapped by Electron or Tauri.

Implementation target:

- Create a new Web/Electron-ready prototype rather than replacing the previous Unreal plan.
- Preserve existing UE artifacts and generated image assets.
- Produce a screenshot and lightweight verification evidence.

## 2026-06-02 05:05 JST

Implementation was promoted from a single prototype file to a structured Web app:

- `web-app/index.html`
- `web-app/src/data.js`
- `web-app/src/app.js`
- `web-app/src/styles.css`
- `web-app/electron/main.cjs`

The app now supports all six spread definitions currently present in `data/spread-definitions-v1.json`, including `relationship_line`. The guide remains disabled until the selected slot has a reader note, which enforces the intended "read by yourself first" loop.

Verification added:

- `scripts/check_web_app.py`
- `scripts/smoke_web_app.cjs`

Latest evidence:

- `reports/web-app-check-20260602-051246.json`
- `reports/web-app-smoke-20260602-051246.json`
- `reports/electron-app-smoke-20260602-051246.json`
- `reports/onoko-arcana-web-app-celtic-20260602-051246.png`
- `reports/onoko-arcana-web-app-mobile-20260602-051246.png`
- `reports/onoko-arcana-electron-smoke-20260602-051246.png`
