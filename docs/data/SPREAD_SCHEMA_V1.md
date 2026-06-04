# ONOKO ARCANA Spread Schema v1

Updated: 2026-06-05

## Runtime Source

現行Web/Electron版のスプレッド定義は `web-app/src/data.js` の `spreads` 配列で管理する。

## Spread Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | stable identity。履歴の `spreadId` と照合する |
| `label` | string | yes | UI表示名 |
| `description` | string | yes | 左パネルに出す短い説明 |
| `layoutType` | string | yes | CSS class / rendering behavior の分類 |
| `slots` | array | yes | 1件以上 |

## Slot Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `key` | string | yes | spread内で一意。履歴の `slotKey` と照合する |
| `label` | string | yes | 卓と復習UIに表示 |
| `revealOrder` | number | yes | 1始まり。重複不可 |
| `prompt` | string | yes | slotごとの読みの観点 |
| `x` | number | yes | board内の%位置 |
| `y` | number | yes | board内の%位置 |
| `rot` | number | yes | 表示回転角度 |

## Current Spread IDs

- `one_card`
- `three_card_past_present_future`
- `five_card_cross`
- `seven_card_horseshoe`
- `celtic_cross`
- `relationship_line`

## Change Rules

- `id` と `slot.key` は保存履歴の互換性に直結するため、変更時はhistory fixtureとimport smokeを更新する。
- `revealOrder` は1からslot数まで重複なしにする。
- 新spread追加時は、CSS layout、Web smoke、visual audit、Card/History schemaへの影響を同時に確認する。
- Custom spreadはv1.0後の拡張候補とし、現行v1では固定6spreadを安定させる。
