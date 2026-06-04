# ONOKO ARCANA 実装カンバン

Updated: 2026-06-05

この文書は、ONOKO ARCANA の現行 Web/Electron MVP を前に進めるための実装カンバンである。Unreal 関連の成果は履歴として保持するが、v1.x の実装対象からは完全に外す。最短 MVP は `web-app/index.html` と Electron shell で「スプレッド選択、ドロー、順番めくり、解釈メモ、guide 照合、履歴保存、履歴復習」を安定させることとする。

## ステータス

| Status | 意味 |
|---|---|
| Verified | 実装済みで、関連チェックとスモークが通っている |
| Implemented | 実装済みだが、追加検証または改善余地がある |
| Active | 次に進める実装対象 |
| Backlog | 後続タスク |
| Hold | 現時点では保留 |
| Archived | 現行ロードマップ外。証跡だけ保持する |

## 現在のベースライン

| 項目 | 現在 |
|---|---|
| Main app | `web-app/index.html` |
| Runtime | 直接 open 可能な HTML/CSS/JS |
| Runtime direction | Web/Electron only |
| Desktop shell | `web-app/electron/main.cjs` |
| Local package | `dist/onoko-arcana-local/` from `scripts/package_electron_local.cjs` |
| Cards | V5 大アルカナ 22 枚 + 裏面 1 枚 |
| Spreads | `one_card`, `three_card_past_present_future`, `five_card_cross`, `seven_card_horseshoe`, `celtic_cross`, `relationship_line` |
| Persistence | Browser `localStorage` |
| Export / Import | Saved readings JSON export and import |
| Latest static check | `reports/web-app-check-20260605-004943.json` |
| Latest visual audit | `reports/ui-visual-audit-20260605-004949/report.json` |
| Latest web smoke | `reports/web-app-smoke-20260605-004943.json` |
| Latest electron smoke | `reports/electron-app-smoke-20260605-004947.json` |
| Latest package smoke | `reports/electron-package-smoke-20260605-005006.json` |
| Latest keyboard smoke | `reports/keyboard-focus-smoke-20260605-005005.json` |

## 検証コマンド

```powershell
python scripts/check_web_app.py
```

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_web_app.cjs
```

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_app.cjs
```

```powershell
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/package_electron_local.cjs
```

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_package.cjs
```

## MVP CORE

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Web app entry | Verified | P0 | `web-app/index.html` が直接起動できる | 変更時は static check と smoke を通す | `web-app-check` |
| Deck load | Verified | P0 | V5 カード 23 assets を参照 | Deck schema を変える時だけ manifest check を拡張 | Static check |
| Spread selection | Verified | P0 | 6 spread を選択可能 | 選択維持と履歴復元時の扱いを検討 | Web smoke |
| Draw / reveal | Verified | P0 | ドロー、順番 reveal、選択カード表示が成立 | reveal animation は後回し。状態の安定を優先 | Web smoke |
| User note first | Verified | P0 | 自分の読みを書いてから guide を表示する流れ | 空 note 時の guide 制御を regression check に残す | Web smoke |
| Save reading | Verified | P0 | localStorage に保存 | 保存失敗時のエラー表示を追加検討 | Web smoke |
| History display | Verified | P0 | 右パネルで保存済みリーディングと復習ノートを表示 | filter/比較学習へ拡張 | Web smoke |

## SPREAD RUNTIME

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| One card | Verified | P0 | 実行可能 | Regression only | Smoke |
| Three card | Verified | P0 | 実行可能 | Regression only | Smoke |
| Five card cross | Verified | P0 | 実行可能、視覚監査済み | 低解像度追加確認 | Visual audit |
| Seven horseshoe | Verified | P0 | 実行可能、視覚監査済み | 低解像度追加確認 | Visual audit |
| Celtic cross | Verified | P0 | 実行可能、2D向けに交差を分離 | 伝統配置との差分説明を必要なら追加 | Visual audit |
| Relationship line | Verified | P0 | 2段配置で実行可能 | 実使用時のラベル文言を磨く | Visual audit |
| Custom spread | Backlog | P3 | 未実装 | 保存/復習/配布が安定してから検討 | Requirements |

## DATA / PERSISTENCE

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| localStorage schema | Verified | P0 | `onoko-arcana:desktop:history:v1` を使用 | v2以降はmigration方針に従う | `docs/data/HISTORY_SCHEMA_V1.md` |
| Export history | Verified | P1 | JSON 書き出し可能 | Export format の固定とサンプル保存 | Smoke |
| Import history | Verified | P1 | exported JSON を読み戻し、既存履歴へ重複なしで merge できる | raw array 互換は維持 | `reports/web-app-smoke-20260605-004943.json` |
| Delete single reading | Verified | P1 | 確認つきで履歴から削除 | Regression only | `reports/web-app-smoke-20260605-004943.json` |
| Clear all history | Verified | P2 | 確認つき全消去を実装 | Regression only | `reports/web-app-smoke-20260605-004943.json` |
| Corrupt storage display | Verified | P1 | 壊れたlocalStorageを空履歴として黙殺しない | Regression only | `reports/web-app-smoke-20260605-004943.json` |
| Backup location guidance | Verified | P2 | export JSONを正式backup/restore経路として説明 | 実配布前にsettingsへ昇格検討 | `README.md`, `web-app/README.md` |
| Card schema | Verified | P1 | `docs/data/CARD_SCHEMA_V1.md` | Card追加時はcheck/smoke更新 | Static check |
| Spread schema | Verified | P1 | `docs/data/SPREAD_SCHEMA_V1.md` | Spread追加時はlayout/fixture更新 | Static check |
| History fixtures | Verified | P2 | 正常/重複/invalid JSON fixtureあり | Regression only | `tests/fixtures/history/` |

## UI / UX IMPLEMENTATION

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Modular HUD assets | Verified | P0 | 9-slice と modular kit を導入 | 新規 UI surface 追加時は asset check に追加 | Static check |
| Dense spread layout | Verified | P0 | P3 overlap まで解消済み | 主要変更時に visual audit を再実行 | `issueCount: 0` |
| Mobile layout | Verified | P0 | 390px 幅 smoke 済み | 低縦幅 viewport を追加確認 | Mobile screenshot |
| Keyboard flow | Verified | P1 | Tab order, focus, Enter/Space の smoke 済み | 追加a11y監査は後続 | `reports/keyboard-focus-smoke-20260604-041422.json` |
| Accessibility labels | Implemented | P2 | 履歴復元/削除にaria-labelを追加 | Button/slot全体監査は後続 | Static check |
| Error states | Implemented | P2 | import失敗、history保存/削除失敗を表示 | asset load失敗は後続 | Static check |

## LEARNING / REVIEW

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Guide after note | Verified | P0 | 現行 MVP の核として成立 | Regression check を維持 | Web smoke |
| Reading history | Verified | P0 | 保存済み一覧、要約、復習ノートを表示 | filter/比較へ拡張 | Screenshot |
| Review mode | Implemented | P1 | 履歴1件を復習ノートで読める | カード別/問い別filterを設計 | Web smoke |
| Search / filter | Backlog | P2 | 未実装 | スプレッド、カード、日付、キーワードで絞る | Search smoke |
| Study progress | Backlog | P2 | 未実装 | 引いた回数、未復習カード、自己解釈の変化を見る | Study report |

## ELECTRON / DISTRIBUTION

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Electron shell | Verified | P0 | `npm run desktop` 相当の shell がある | 変更時に electron smoke を通す | `reports/electron-app-smoke-20260605-004947.json` |
| Packaging | Verified | P1 | `dist/onoko-arcana-local/` を作成できる | 外部配布時はinstallerを別定義 | `reports/electron-package-smoke-20260605-005006.json` |
| App icon | Implemented | P1 | Electron window iconにカード裏面PNGを設定 | installer用 `.ico` は配布時に対応 | `web-app/electron/main.cjs` |
| Auto update | Hold | P3 | 未検討 | 配布方式が決まるまで保留 | Distribution plan |
| Settings screen | Backlog | P2 | 未実装 | 保存場所、履歴操作、表示設定を整理 | Settings smoke |

## UNREAL ARCHIVE

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Unreal project evidence | Archived | P3 | UE 5.7 project と C++ runtime 成果あり | 実装タスクには混ぜない | `plan.md` |
| Native fallback HUD | Archived | P3 | 1枚引き proof あり | Web/Electron本線へ戻す作業はしない | Phase proof |
| UE Python actor spawn | Archived | P3 | 過去に crash あり | 完成証跡には使わない | AGENTS rule |
| Premium 3D table | Archived | P3 | 構想のみ | 現行v1.xロードマップ外 | Scope lock |

## QA / TOOLING

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Static app check | Verified | P0 | `scripts/check_web_app.py` が schema/fixture/package/README も確認 | 新規契約時だけ拡張 | `reports/web-app-check-20260605-004943.json` |
| Web smoke | Verified | P0 | `scripts/smoke_web_app.cjs` が export/import/delete/clear/corrupt storage と desktop panel fit も確認 | keyboard/a11y 深掘りは別 smoke | `reports/web-app-smoke-20260605-004943.json` |
| Electron smoke | Verified | P0 | `scripts/smoke_electron_app.cjs` が desktop panel fit も確認 | Shell変更時に維持 | `reports/electron-app-smoke-20260605-004947.json` |
| Package smoke | Verified | P1 | `scripts/smoke_electron_package.cjs` がpackage起動、保存、import、invalid importを確認 | package方式変更時に維持 | `reports/electron-package-smoke-20260605-005006.json` |
| Visual audit | Verified | P0 | `scripts/audit_web_ui_visual.cjs` は desktop overflow/panel clipping を含め issueCount 0 | viewport とケースを増やす | `reports/ui-visual-audit-20260605-004949/report.json` |
| Regression snapshots | Implemented | P2 | `reports/README.md` で代表証跡と一時runを分離 | 必要時のみ代表proofをpromote | Report policy |

## 次に進める順序

1. 復習ビューをカード別/問い別/スプレッド別filterへ進める。
2. settings screenで保存、履歴、表示設定を整理する。
3. 初回起動empty stateと保存後の次アクションを磨く。
4. 外部配布する場合だけinstaller、`.ico`、署名、auto updateを別スコープで定義する。

## 完了報告に含めるもの

- 変更したファイル。
- 実行した検証コマンド。
- 生成された `reports/` の JSON とスクリーンショット。
- 未検証の場合は、理由と代替確認。
- デザインに影響する場合は `docs/design/DESIGN_KANBAN.md` の該当項目更新。
