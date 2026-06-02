# Phase 4 Spread Play Surface

Updated: 2026-06-02

## Purpose

This slice connects the commandlet-proven spread runtime to the running Unreal play window.

The first visible multi-card target is:

```text
three_card_past_present_future
```

## Implemented

`AOnokoArcanaTableController` now routes the existing table commands through the spread runtime when `ActiveSpreadId != one_card`:

- `StartReading`
- `DrawCard`
- `RevealCard`
- `RevealGuide`
- `SubmitUserInterpretation`
- `ResetTable`
- `SaveCurrentReading`
- `HasCurrentDraw`
- `GetCurrentDraw`

The one-card path remains in place for `one_card`.

New table-controller state:

- `UOnokoArcanaSpreadReadingViewModel* SpreadViewModel`
- `TArray<AOnokoArcanaCardActor*> SpreadCardActors`
- `SpreadCardSpacingCentimeters`
- `SpreadCardCenterYOffsetCentimeters`

The controller spawns runtime `AOnokoArcanaCardActor` instances in C++ for the active spread and syncs each actor from `FOnokoArcanaReadingCardState`.

## HUD Behavior

The native fallback HUD now reads spread state when a multi-card spread is active:

- active spread name and slot list
- selected slot text such as `選択位置: 未来 [future]`
- Past / Present / Future slot buttons
- progress text such as `3/3 revealed`
- selected card title/orientation/keywords
- guide text after guide reveal

The `Reveal` button advances through the spread reveal order. The slot buttons select the interpretation target without changing reveal state.

## Demo Capture Flag

`AOnokoArcanaPlayerController` supports this command-line flag:

```text
-ONOKOArcanaAutoThreeCardDemo
```

When present, the game window starts a three-card reading, draws the spread, reveals all three cards, writes a selected-slot note, reveals guide text, and refreshes the HUD. This is only a local proof path for screenshots.

## Evidence

Latest screenshot:

```text
reports/onoko-arcana-hud-generated-overlay-printwindow-20260602-040336.png
```

Current checks:

- Game target build: OK
- Editor target build: OK
- `Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json`: `ok=true`, `BLEND_MASKED`, `MSM_UNLIT`
- `Unreal/ONOKO_ARCANA/Saved/Phase4HudTextureImportResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json`: `ok=true`
- `reports/phase4-play-surface-check-20260601-190614.json`: `ok=true`
- `reports/phase4-spread-runtime-check-20260601-174457.json`: `ok=true`
- `reports/phase1-preflight-check-20260601-190614.json`: `ok=true`, warning: missing `.git`

## Fixed During This Slice

The first runtime spawn attempt crashed because the spread actor spawn path supplied an explicit actor name that UE could not uniquify. The fix is to let `SpawnActor` generate runtime names automatically.

The first visible spread layout used the world X axis and appeared vertical in the top-down camera. The fix is to lay out spread cards along world Y, then offset the center away from the HUD.

## Remaining Work

- Replace the native fallback HUD with a designed `WBP_TableHUD`.
- Add direct table-card click selection.
- Replace the current `TextRenderActor` table labels with designed UMG/world-widget labels when Japanese labels are required.
- Add flip animation and clearer unrevealed/revealed visual states.
- Extend layout rules for five-card, seven-card, Celtic Cross, and relationship spreads.
