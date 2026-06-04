# Phase 2 Reading SaveGame

> Archive notice (2026-06-05): This UE SaveGame note is historical evidence. The active v1.x persistence path is Web/Electron `localStorage` history v1; do not use this document as current next work.

Updated: 2026-06-01

This note defines the first durable reading-history layer for ONOKO ARCANA. It is intentionally UI-independent so the one-card table HUD can save readings before the final history screen exists.

## Current C++ Surface

| Class / Struct | Role |
|---|---|
| `FOnokoArcanaSavedReading` | Serializable record for one tarot reading. |
| `UOnokoArcanaReadingSaveGame` | SaveGame object containing saved readings and schema version. |
| `UOnokoArcanaReadingSaveLibrary` | Blueprint-callable functions for making, saving, loading, and deleting readings. |
| `UOnokoArcanaReadingHistoryViewModel` | Loads saved readings and exposes count, latest summary, selected title, selected detail, and empty state text for UI. |
| `AOnokoArcanaTableController::SaveCurrentReading()` | Saves the current one-card table reading to the configured slot. |
| `AOnokoArcanaTableController::LoadReadingHistory()` | Loads the current reading history slot. |
| `AOnokoArcanaTableController::RefreshReadingHistory()` | Refreshes `HistoryViewModel` from the current slot. |
| `AOnokoArcanaTableController::SelectHistoryReading()` | Selects a saved reading by index for detail display. |

## Stored Fields

Each saved reading currently stores:

- Reading id
- Created UTC timestamp
- Question
- Card id, number, English name, Japanese name
- Orientation label
- Active keywords for the drawn orientation
- Study focus
- User interpretation
- Guide revealed flag

## Default Slot

If the caller passes an empty slot name, the save library uses:

```text
ONOKO_ARCANA_Readings
```

`AOnokoArcanaTableController` also defaults to that slot through `SaveSlotName`.

## Acceptance Evidence

Commandlet result:

```text
Unreal/ONOKO_ARCANA/Saved/Phase2ReadingSaveGameTestResult.json
```

Current result: `ok: true`

The test creates a one-card session, draws a card, adds a user interpretation, reveals the guide, converts the session into `FOnokoArcanaSavedReading`, saves it to a temporary slot, loads it back, verifies card id and user interpretation, then deletes the temporary slot.

Additional commandlet result:

```text
Unreal/ONOKO_ARCANA/Saved/Phase2ReadingHistoryViewModelTestResult.json
```

Current result: `ok: true`

The history test saves two readings, loads them through `UOnokoArcanaReadingHistoryViewModel`, verifies the count, latest summary, initial selection detail, manual selection, and then deletes the temporary slot.

## Next UI Work

`WBP_TableHUD` should include `SaveReadingButton` and `RefreshHistoryButton` bound through `UOnokoArcanaTableHudWidget`.

Minimum history text widgets:

| Widget Name | Purpose |
|---|---|
| `HistoryCountText` | Shows saved reading count. |
| `HistoryLatestSummaryText` | Shows the newest saved reading summary. |
| `HistorySelectedTitleText` | Shows selected reading card title. |
| `HistorySelectedDetailText` | Shows selected reading details. |
| `HistoryEmptyStateText` | Shows no-history state. |

Later, replace the simple latest/selected text surface with a real scrollable list that calls `SelectHistoryReading(Index)`.
