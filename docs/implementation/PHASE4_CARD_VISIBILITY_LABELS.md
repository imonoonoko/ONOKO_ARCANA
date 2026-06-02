# Phase 4 Card Visibility And Labels

Updated: 2026-06-02

## Purpose

This slice fixes the faded-card look in the running UE play screen and adds table labels for the three-card spread.

## Card Visibility Fix

Runtime cards use:

```text
/Game/ONOKOArcana/Phase1/Materials/M_Phase1_CardMasked_TextureParam
```

The material is now normalized by:

```text
Unreal/ONOKO_ARCANA/Scripts/ensure_phase1_runtime_materials.py
```

Current material policy:

- `BlendMode = BLEND_MASKED`
- `ShadingModel = MSM_UNLIT`
- texture RGB drives `Emissive Color`
- texture alpha drives `Opacity Mask`
- `CardTexture` remains the runtime texture parameter

Result:

```text
Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json
```

## Table Labels

`AOnokoArcanaTableController` now owns:

```text
SpreadSlotLabelActors
```

The controller spawns `ATextRenderActor` labels and syncs them with the active spread slots:

- `PAST`
- `PRESENT`
- `FUTURE`

The selected slot label is highlighted in warm gold. English labels are used for the table actors because the default UE text-render font did not reliably render Japanese glyphs.

## Evidence

Latest screenshot:

```text
reports/onoko-arcana-card-visibility-labels-printwindow-20260602-031850.png
```

Latest checks:

- `Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json`: `ok=true`, `BLEND_MASKED`, `MSM_UNLIT`
- `Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json`: `ok=true`
- `reports/phase4-play-surface-check-20260601-182133.json`: `ok=true`
- `reports/phase1-preflight-check-20260601-182133.json`: `ok=true`, warning: missing `.git`

Current visible result:

- card faces are much stronger and no longer washed out by table lighting
- three cards remain visible on the table
- table labels are readable
- selected slot remains available in the HUD

## Remaining Work

- Replace native TextRender labels with designed UMG/world widgets if Japanese table labels are required.
- Add direct click/pick selection on card actors.
- Add final presentation material if a more physically lit card surface is desired later.
