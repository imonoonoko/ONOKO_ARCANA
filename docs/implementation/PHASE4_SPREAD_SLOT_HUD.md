# Phase 4 Spread Slot HUD

> Archive notice (2026-06-05): This UE slot HUD note is historical evidence. The active v1.x lane is Web/Electron; do not use this document as current next work.

Updated: 2026-06-02

## Purpose

This slice makes the visible three-card spread screen operable beyond reveal order.

The player can now select the spread position they want to interpret:

- Past
- Present
- Future

## Implemented

`AOnokoArcanaTableController` adds:

- `SelectSpreadSlot(FName PositionKey)`
- `GetSelectedSpreadSlotText()`

Selecting a slot routes through `UOnokoArcanaSpreadReadingViewModel::SelectSlot`, refreshes table state, and re-syncs spread card actors. The selected actor is slightly larger so the active interpretation target is visible on the table.

`UOnokoArcanaTableHudWidget` adds optional native/Blueprint-bindable widgets:

- `SelectedSpreadSlotText`
- `PastSlotButton`
- `PresentSlotButton`
- `FutureSlotButton`

The native fallback HUD now displays:

```text
選択位置: 未来 [future]
Past / Present / Future
```

## Evidence

Latest screenshot:

```text
reports/onoko-arcana-three-card-slot-hud-printwindow-20260602-030423.png
```

Current checks:

- Game target build: OK
- Editor target build: OK
- `Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json`: `ok=true`
- `reports/phase4-play-surface-check-20260601-180622.json`: `ok=true`
- `reports/phase1-preflight-check-20260601-180622.json`: `ok=true`, warning: missing `.git`

## Remaining Work

- Promote the native fallback slot controls into `WBP_TableHUD`.
- Add direct table-card click selection.
- Add persistent Past / Present / Future labels near the cards.
- Add clearer selected-card focus styling beyond scale change.
