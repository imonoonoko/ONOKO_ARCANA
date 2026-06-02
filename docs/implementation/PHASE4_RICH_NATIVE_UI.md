# Phase 4 Rich Native UI

Updated: 2026-06-02

## Purpose

This slice gives the running Unreal play screen a stronger ONOKO visual direction using the existing native fallback HUD. It is intentionally visual-first and does not replace the future designed `WBP_TableHUD`.

Reference direction came from the generated concept images under:

```text
assets/generated/reports/20260602-onoko-strong-play-screen-concepts/
assets/generated/reports/20260602-future-multi-spread-concepts/
```

## Implemented

`UOnokoArcanaTableHudWidget` now builds a richer native fallback layout:

- top ONOKO ARCANA nameplate
- left reading setup panel for spread, question, note, and progress
- right selected-card guide and history panel
- bottom command bar for slot selection and repeated actions
- dark blue-black panel palette with gold labels and blue command surfaces
- dark text-entry styling for question and interpretation fields

`AOnokoArcanaTableController` also uses a more compact three-card spacing so the table cards remain visible between the left/right HUD panels.

The new root design context is captured in:

```text
PRODUCT.md
DESIGN.md
```

## Evidence

Latest screenshot:

```text
reports/onoko-arcana-hud-generated-overlay-printwindow-20260602-040336.png
```

Latest checks:

- Game target build: OK
- Editor target build: OK
- `Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase4HudTextureImportResult.json`: `ok=true`
- `reports/phase4-play-surface-check-20260601-190614.json`: `ok=true`
- `reports/phase1-preflight-check-20260601-190614.json`: `ok=true`, warning: missing `.git`

Current visible result:

- cards are not covered by the left/right HUD panels
- PAST / PRESENT / FUTURE labels remain readable
- selected-card guide is separated from setup controls
- command buttons are collected into a bottom bar
- generated transparent HUD frame artwork now sits behind the darker ONOKO-style surface

## Remaining Work

- Replace the native fallback UI with a designed `WBP_TableHUD`.
- Add icon-based buttons and hover/focus state polish in UMG.
- Add a designed world-widget label layer if Japanese table labels are required.
- Add actual table ring/crystal/ornament geometry instead of HUD-only atmosphere.
