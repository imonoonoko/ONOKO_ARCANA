# ONOKO ARCANA Card Schema v1

Updated: 2026-06-05

## Runtime Source

現行Web/Electron版のカード定義は `web-app/src/data.js` の `CARD_ROWS` から生成する。v1の対象は大アルカナ22枚と共通裏面1枚である。

## Card Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | `major-<number>-<slug>` |
| `number` | string | yes | `00` から `21` |
| `displayNumber` | string | yes | UI表示用。愚者は `0`、他はRoman numeral |
| `slug` | string | yes | file pathとidentityに使う英小文字slug |
| `japaneseName` | string | yes | UI表示名 |
| `englishName` | string | yes | 補助表示名 |
| `uprightKeywords` | string[] | yes | 正位置の短いキーワード |
| `reversedKeywords` | string[] | yes | 逆位置の短いキーワード |
| `studyFocus` | string | yes | guideで表示する学習観点 |
| `studyDetails.symbols` | string[] | yes | 学習シートで見るカード上の象徴、モチーフ、構図 |
| `studyDetails.commonMisreads` | string[] | yes | 初学者が短絡しやすい読みの注意点 |
| `studyDetails.reflectionQuestions` | string[] | yes | 自分の言葉で読み直すための内省質問 |
| `sourceImage` | string | yes | 元alpha asset path |
| `image` | string | yes | Web表示用labeled alpha asset path |

## Asset Rules

- Web runtimeは `assets/generated/card-production-v5-full/web-labeled/alpha/` を表示に使う。
- 表示用front cardは22枚、back cardは1枚必要。
- ファイル名は `major-<number>-<slug>-onoko-v5-alpha.png` を使う。
- 小アルカナを追加する場合は、Major runtime、履歴、復習、配布、検証が安定した後にschema v2または別schemaとして扱う。

## Change Rules

- `id`, `number`, `slug` を変える場合は、履歴import/export互換への影響を確認する。
- 既存履歴が参照する `cardId` を壊す変更は、migration方針とfixtureを先に追加する。
- Card追加時は `scripts/check_web_app.py` の期待数、visual audit、Web smokeを更新する。
