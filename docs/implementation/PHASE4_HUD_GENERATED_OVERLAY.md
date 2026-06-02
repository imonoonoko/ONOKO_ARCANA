# Phase 4 Generated HUD Overlay

Updated: 2026-06-02

## Purpose

This slice turns an `imagegen` HUD concept asset into a real transparent Unreal UI texture and applies it to the running ONOKO ARCANA native fallback HUD.

## Generated Asset

Source prompt target:

- 16:9 ONOKO cyber-oracle HUD ornament overlay
- pure chroma green background for local alpha removal
- no readable text
- left/right panel frames, top nameplate frame, bottom command bar frame
- gold linework, blue glow accents, crystal corners, and cat-oracle medallions

Local files:

```text
assets/generated/hud/20260602-onoko-hud-overlay-v1/onoko-hud-overlay-v1-source-chroma.png
assets/generated/hud/20260602-onoko-hud-overlay-v1/onoko-hud-overlay-v1-alpha.png
```

The alpha version was produced with:

```text
C:\Users\Humin\.codex\skills\.system\imagegen\scripts\remove_chroma_key.py
```

using the bundled Codex Python runtime because the shell default Python did not have Pillow installed.

## Unreal Import

Staged file:

```text
Unreal/ONOKO_ARCANA/ImportStaging/HUD/onoko-hud-overlay-v1-alpha.png
```

Imported texture:

```text
/Game/ONOKOArcana/UI/HUD/Textures/T_HUD_ONOKO_Overlay_V1
```

Import proof:

```text
Unreal/ONOKO_ARCANA/Saved/Phase4HudTextureImportResult.json
```

## Runtime Use

`UOnokoArcanaTableHudWidget` now loads the generated texture and adds it as `NativeFallbackHudGeneratedOverlay` across the full screen. The generated ornament layer sits under the functional panels so it adds ONOKO framing without blocking existing controls.

## Evidence

Latest screenshot:

```text
reports/onoko-arcana-hud-generated-overlay-printwindow-20260602-040336.png
```

Latest checks:

- Game target build: OK
- Editor target build: OK
- `Unreal/ONOKO_ARCANA/Saved/Phase4HudTextureImportResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json`: `ok=true`
- `reports/phase4-play-surface-check-20260601-190614.json`: `ok=true`
- `reports/phase1-preflight-check-20260601-190614.json`: `ok=true`, warning: missing `.git`

Current visible result:

- generated left/right frames are visible behind the HUD panels
- generated top nameplate frame aligns with the ONOKO title area
- generated bottom ornament frame sits behind the command bar
- central cards and PAST / PRESENT / FUTURE table labels remain readable
- UI controls still use the existing native fallback logic

## Remaining Work

- Split the overlay into individual 9-slice or UMG-friendly panel textures.
- Replace text buttons with generated or vector icon buttons.
- Tune per-panel alignment after the designed `WBP_TableHUD` exists.
