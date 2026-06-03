# P1 Discovery Result

## Export Shape

`exportHistory()` writes a JSON object with:

- `app: "ONOKO_ARCANA"`
- `schemaVersion: 1`
- `exportedAt: ISO timestamp`
- `history: readHistory()`

Each saved reading currently stores `savedAt`, `question`, `spreadId`,
`spreadLabel`, `revealedCount`, `notes`, `cards`, and `summary`.

## Storage

History is stored in browser `localStorage` under
`onoko-arcana:desktop:history:v1`. `writeHistory()` truncates to the newest 48
items, so import must preserve that cap.

## UI Hooks

History controls currently expose only `exportHistoryButton`. The least
disruptive import UI is a second compact button plus a hidden file input in the
history section.

## Validation Needs

Import should accept the current wrapper object. For robustness it can also
accept a raw array of readings, but invalid JSON, wrong app/schema, missing
history array, empty valid history, or readings without restorable card/spread
data should produce clear status feedback.

## Duplicate Handling

Saved readings do not have durable IDs. Use a stable composite key from
`savedAt`, `spreadId`, `question`, `summary`, and the cards list to avoid
re-appending the same export.

## Smoke Extension

`scripts/smoke_web_app.cjs` already controls `localStorage`, saves two readings,
and checks export is enabled. Extend desktop smoke to trigger download capture,
clear history, import the captured JSON through a file chooser, and verify two
history items are restored.
