# ONOKO ARCANA History Schema v1

Updated: 2026-06-05

この文書は、現行 Web/Electron 版の保存履歴形式を固定するための仕様である。v1 の目的は、読みの保存、復元、書き出し、読み込み、削除、復習表示を同じデータで扱うことにある。

## Storage

| Item | Value |
|---|---|
| Storage | Browser `localStorage` |
| Key | `onoko-arcana:desktop:history:v1` |
| Value | JSON array of reading items |
| Max items | 48 |
| Order | newest first |

## Export Payload

書き出しは次の wrapper を使う。読み込みは過去互換のため、reading item array だけの JSON も受け入れる。

```json
{
  "app": "ONOKO_ARCANA",
  "schemaVersion": 1,
  "exportedAt": "2026-06-04T00:00:00.000Z",
  "history": []
}
```

## Reading Item

| Field | Type | Required | Notes |
|---|---|---|---|
| `savedAt` | string | yes | UI表示用の保存日時。現在は `ja-JP` locale string |
| `question` | string | no | ユーザーが入力した問い |
| `spreadId` | string | yes | `web-app/src/data.js` の spread id |
| `spreadLabel` | string | yes | UI表示用スプレッド名 |
| `revealedCount` | number | no | 保存時点で開示済みの枚数 |
| `notes` | object | no | `1:present` のような `revealIndex:slotKey` 形式のメモ。復元互換用に保持 |
| `cards` | array | yes | 開示済みカードの配列 |
| `summary` | string | yes | 履歴一覧に表示する短い要約 |

## Card Entry

| Field | Type | Required | Notes |
|---|---|---|---|
| `cardId` | string | yes | `cards` data の id |
| `number` | number | no | 大アルカナ番号 |
| `displayNumber` | string | no | UI表示番号 |
| `japaneseName` | string | no | UI表示名 |
| `englishName` | string | no | 英名 |
| `reversed` | boolean | yes | 逆位置なら `true` |
| `slotKey` | string | yes | spread slot key |
| `slotLabel` | string | no | UI表示用slot名 |
| `note` | string | no | ユーザーの自分の読み |

## Import Rules

- `app` がある場合は `ONOKO_ARCANA` のみ受け入れる。
- `schemaVersion` がある場合は `1` のみ受け入れる。
- `spreadId`, `cardId`, `slotKey` は現行データ定義と照合する。
- 重複は `savedAt`, `spreadId`, `question`, `summary`, card entries から作る identity で除外する。
- 不正な item は読み飛ばし、有効な item だけを既存履歴へ merge する。
- 追加分は既存履歴の前に置き、最終的に 48 件へ丸める。
- 復元時は `notes` を優先しつつ、古い `slotKey-index` 形式や `cards[].note` だけの履歴もカード別メモへ戻す。

## Delete And Backup Policy

- 個別削除と全消去は確認つきで実行する。
- 削除前の復元手段は export JSON のみなので、UI は書き出しを促す。
- 削除操作は history v1 item だけを対象にし、カードデータや画像素材は変更しない。
- 既存セーブを自動削除する migration は v1 では行わない。

## Failure Display

- `localStorage` のJSON parseに失敗した場合、空履歴として黙殺しない。
- UIは「履歴データを読めません」と表示し、export済みJSONからのimport復元を案内する。
- 破損状態の検証は `scripts/smoke_web_app.cjs` が担当する。

## Fixtures

| Fixture | Purpose |
|---|---|
| `tests/fixtures/history/history-valid-v1.json` | wrapperつき正常履歴 |
| `tests/fixtures/history/history-duplicate-v1.json` | 重複merge確認用 |
| `tests/fixtures/history/history-card-note-only-v1.json` | `cards[].note` だけの復元互換確認用 |
| `tests/fixtures/history/invalid-json.json` | JSON parse失敗確認用 |

## Migration Policy

v2 以降へ変更する場合は、次を満たす。

- `schemaVersion` を export payload 上で上げる。
- v1 import を最低1世代は維持する。
- 破壊的変更は `docs/data/HISTORY_SCHEMA_V2.md` に差分を残す。
- migration で item を捨てる場合は、理由と対象条件を文書化し、smoke fixture を追加する。
