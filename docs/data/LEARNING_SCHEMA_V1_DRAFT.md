# ONOKO ARCANA Learning Schema v1 Draft

Updated: 2026-06-06

This draft schema stores optional tarot study practice results separately from saved reading history.

## Storage

- Key: `onoko-arcana:desktop:learning:v1`
- Owner: Web/Electron renderer
- Format: JSON object
- Scope: local-only browser or Electron storage

The learning key must not replace or migrate `onoko-arcana:desktop:history:v1`.

## Object Shape

```json
{
  "app": "ONOKO_ARCANA",
  "schemaVersion": 1,
  "attempts": [
    {
      "attemptedAt": "2026-06-06T04:54:00.000Z",
      "cardId": "major-09-hermit",
      "cardLabel": "IX 隠者",
      "orientation": "upright",
      "promptType": "keyword_recall",
      "answer": "内省、探求、孤独、導き",
      "confidence": "ok"
    },
    {
      "attemptedAt": "2026-06-06T05:12:00.000Z",
      "cardId": "major-09-hermit",
      "cardLabel": "IX 隠者",
      "orientation": "reversed",
      "promptType": "slot_interpretation",
      "answer": "課題の位置では、孤立が深まりすぎて助言を受け取れない状態として読む。",
      "confidence": "hard",
      "spreadId": "celtic_cross",
      "spreadLabel": "ケルト十字",
      "slotKey": "challenge",
      "slotLabel": "課題",
      "slotPrompt": "今ぶつかっている葛藤や抵抗。"
    }
  ]
}
```

## Attempt Fields

| field | type | required | notes |
| --- | --- | --- | --- |
| `attemptedAt` | string | yes | ISO timestamp. |
| `cardId` | string | yes | Must match a Major Arcana card id from `web-app/src/data.js`. |
| `cardLabel` | string | recommended | Human-readable snapshot for export/debug. |
| `orientation` | string | yes | `upright` or `reversed`. |
| `promptType` | string | yes | `keyword_recall` or `slot_interpretation`. |
| `answer` | string | yes | User's own recall before guide reveal. |
| `confidence` | string | yes | `hard`, `ok`, or `easy`. |
| `spreadId` | string | slot optional | Spread id snapshot for `slot_interpretation`. |
| `spreadLabel` | string | slot optional | Human-readable spread label snapshot. |
| `slotKey` | string | slot optional | Spread slot key snapshot. |
| `slotLabel` | string | slot optional | Human-readable slot label snapshot. |
| `slotPrompt` | string | slot optional | Slot guide prompt shown after the user's answer. |

## Export Shape

The settings screen exports learning data as a wrapper object so future exports can carry app metadata without changing the inner learning state.

```json
{
  "app": "ONOKO_ARCANA",
  "schemaVersion": 1,
  "exportedAt": "2026-06-06T10:24:17.000Z",
  "learning": {
    "app": "ONOKO_ARCANA",
    "schemaVersion": 1,
    "attempts": []
  }
}
```

Runtime import accepts either this wrapper shape or a bare learning-state object with `attempts`.

## Derived Due Review Rules

Due review dates are derived at runtime and are not stored in v1.

| confidence | initial interval | notes |
| --- | --- | --- |
| `hard` | same day | Keep the card in today's review cue. |
| `ok` | 1 day | Return tomorrow after a successful but uncertain recall. |
| `easy` | 3 days | Delay the next prompt for a short initial spacing interval. |

The runtime uses the latest valid attempt per `cardId` + `orientation` + `promptType` when building the Study Lens due cue. Future 7-day and 14-day intervals should be added only after fixture coverage exists.

## Rules

- Keep learning attempts optional and local.
- Keep learning attempts separate from reading history.
- Invalid learning entries may be dropped during runtime normalization.
- Limit stored attempts to the latest 128 entries.
- Import merges valid attempts and deduplicates by timestamp, card, orientation, prompt type, spread id, slot key, answer, and confidence.
- Clear learning data removes `onoko-arcana:desktop:learning:v1` only. It must not delete saved readings.
- Spaced review derives due dates from `attemptedAt`, `cardId`, `orientation`, `promptType`, and `confidence`.
- `slot_interpretation` attempts should be created only from an active table card so the spread and slot fields describe a real reading context.
