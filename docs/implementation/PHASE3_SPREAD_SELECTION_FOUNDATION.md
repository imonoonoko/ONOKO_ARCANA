# Phase 3 Spread Selection Foundation

> Archive notice (2026-06-05): This UE spread note is historical evidence. The active v1.x lane is Web/Electron; do not use this document as current next work.

Updated: 2026-06-02

## Goal

Start the future "all product-supported spreads are selectable" path without destabilizing the Phase 1 one-card proof.

The first implementation slice adds spread metadata and selection. Multi-card draw state, multiple card actors, per-slot notes, and spread review are intentionally deferred.

## New Runtime Surface

| Class / Struct | Role |
|---|---|
| `EOnokoArcanaSpreadLayoutType` | Blueprint-visible layout family for one-card, linear, cross, horseshoe, Celtic cross, and relationship layouts. |
| `FOnokoArcanaSpreadSlotDefinition` | One slot in a spread: key, label, reveal order, guide prompt, logical table location, and yaw. |
| `FOnokoArcanaSpreadDefinition` | A complete spread: id, display name, description, layout type, and ordered slots. |
| `UOnokoArcanaSpreadRegistry` | Built-in spread catalog exposed to Blueprint/UMG. |

## Built-In Spread Catalog

| SpreadId | Display | Cards | Status |
|---|---:|---:|---|
| `one_card` | 一枚引き | 1 | Executable in Phase 1 |
| `three_card_past_present_future` | 過去・現在・未来 | 3 | Metadata/selectable |
| `five_card_cross` | 五枚クロス | 5 | Metadata/selectable |
| `seven_card_horseshoe` | 七枚ホースシュー | 7 | Metadata/selectable |
| `celtic_cross` | ケルト十字 | 10 | Metadata/selectable |
| `relationship_line` | 関係性ライン | 6 | Metadata/selectable |

## Table Controller Additions

`AOnokoArcanaTableController` now owns:

- `SpreadRegistry`
- `ActiveSpreadId`
- `ActiveSpreadDefinition`

It exposes:

- `InitializeSpreadRegistry()`
- `SelectSpread(FName SpreadId)`
- `GetAvailableSpreads()`
- `GetActiveSpread()`
- `GetActiveSpreadDisplayText()`
- `GetActiveSpreadSlotListText()`
- `GetAvailableSpreadListText()`

Phase 1 draw remains guarded to `one_card`. Selecting another spread changes metadata and HUD display, but attempting to draw it reports that multi-card runtime is not implemented yet.

## HUD Contract Additions

`UOnokoArcanaTableHudWidget` now accepts optional widgets:

| Widget Name | Type |
|---|---|
| `SpreadSelectorComboBox` | `ComboBoxString` |
| `ActiveSpreadText` | `TextBlock` |
| `SpreadSlotsText` | `TextBlock` |

The native fallback HUD creates these widgets automatically when no Blueprint widget tree exists.

## SaveGame Compatibility

`FOnokoArcanaSavedReading` now includes forward-compatible spread metadata:

- `SpreadId`
- `SpreadDisplayName`
- `CardCount`
- `PositionKey`
- `PositionLabel`

Existing one-card saves remain readable because the fields have one-card defaults.

## Verification Status

Pre-edit preflight:

- `python scripts/check_phase1_preflight.py`
- OK
- Report: `reports/phase1-preflight-check-20260601-161331.json`

Post-edit preflight:

- `python scripts/check_phase1_preflight.py`
- OK
- Report: `reports/phase1-preflight-check-20260601-164925.json`

Build status:

- Game target compile succeeded:
  - `UnrealBuildTool.exe ONOKO_ARCANA Win64 Development -Project=... -WaitMutex -NoLiveCoding`
- Editor target compile and link succeeded after closing the running editor:
  - `UnrealBuildTool.exe ONOKO_ARCANAEditor Win64 Development -Project=... -WaitMutex -FromMsBuild -NoLiveCoding`

Commandlet smoke results:

- `Unreal/ONOKO_ARCANA/Scripts/test_phase3_spread_registry.py`
- Result: `Unreal/ONOKO_ARCANA/Saved/Phase3SpreadRegistryTestResult.json`
- Current `ok`: `true`
- Verified:
  - six built-in spreads are exposed.
  - default spread is `one_card`.
  - `celtic_cross` has 10 slots.
  - `three_card_past_present_future` reveal order is 1, 2, 3.
  - `AOnokoArcanaTableController` can select `three_card_past_present_future`.
  - invalid spread ids are rejected with an error.
  - a saved one-card reading records `SpreadId=one_card`, `SpreadDisplayName=一枚引き`, `CardCount=1`, `PositionKey=present`, and `PositionLabel=一枚引き`.

Regression commandlets rerun:

- `Unreal/ONOKO_ARCANA/Scripts/test_phase1_hud_reflection_surface.py`: `ok=true`
- `Unreal/ONOKO_ARCANA/Scripts/test_phase2_reading_save_game.py`: `ok=true`
- `Unreal/ONOKO_ARCANA/Scripts/test_phase2_reading_history_view_model.py`: `ok=true`
