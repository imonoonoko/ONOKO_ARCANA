# ONOKO ARCANA 実装カンバン

Updated: 2026-06-04

この文書は、ONOKO ARCANA の現行 Web/Electron MVP を前に進めるための実装カンバンである。Unreal 関連の成果は保持するが、当面の最短 MVP は `web-app/index.html` と Electron shell で「スプレッド選択、ドロー、順番めくり、解釈メモ、guide 照合、履歴保存、履歴復習」を安定させることとする。

## ステータス

| Status | 意味 |
|---|---|
| Verified | 実装済みで、関連チェックとスモークが通っている |
| Implemented | 実装済みだが、追加検証または改善余地がある |
| Active | 次に進める実装対象 |
| Backlog | 後続タスク |
| Hold | 現時点では保留 |

## 現在のベースライン

| 項目 | 現在 |
|---|---|
| Main app | `web-app/index.html` |
| Runtime | 直接 open 可能な HTML/CSS/JS |
| Desktop shell | `web-app/electron/main.cjs` |
| Cards | V5 大アルカナ 22 枚 + 裏面 1 枚 |
| Spreads | `one_card`, `three_card_past_present_future`, `five_card_cross`, `seven_card_horseshoe`, `celtic_cross`, `relationship_line` |
| Persistence | Browser `localStorage` |
| Export / Import | Saved readings JSON export and import |
| Latest static check | `reports/web-app-check-20260604-033125.json` |
| Latest visual audit | `reports/ui-visual-audit-20260604-033211/report.json` |
| Latest web smoke | `reports/web-app-smoke-20260604-033139.json` |
| Latest electron smoke | `reports/electron-app-smoke-20260604-033157.json` |

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

## MVP CORE

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Web app entry | Verified | P0 | `web-app/index.html` が直接起動できる | 変更時は static check と smoke を通す | `web-app-check` |
| Deck load | Verified | P0 | V5 カード 23 assets を参照 | Deck schema を変える時だけ manifest check を拡張 | Static check |
| Spread selection | Verified | P0 | 6 spread を選択可能 | 選択維持と履歴復元時の扱いを検討 | Web smoke |
| Draw / reveal | Verified | P0 | ドロー、順番 reveal、選択カード表示が成立 | reveal animation は後回し。状態の安定を優先 | Web smoke |
| User note first | Verified | P0 | 自分の読みを書いてから guide を表示する流れ | 空 note 時の guide 制御を regression check に残す | Web smoke |
| Save reading | Verified | P0 | localStorage に保存 | 保存失敗時のエラー表示を追加検討 | Web smoke |
| History display | Implemented | P0 | 右パネルで保存済みリーディングを表示 | 復習しやすい詳細表示に改善 | Screenshot |

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
| localStorage schema | Implemented | P0 | `onoko-arcana:desktop:history:v1` を使用 | schema version と migration 方針を文書化 | Schema note |
| Export history | Verified | P1 | JSON 書き出し可能 | Export format の固定とサンプル保存 | Smoke |
| Import history | Verified | P1 | exported JSON を読み戻し、既存履歴へ重複なしで merge できる | raw array 互換は維持しつつ、必要ならschema文書を追加 | `reports/web-app-smoke-20260604-033139.json` |
| Delete single reading | Backlog | P1 | 未実装 | 誤削除防止つきで履歴から削除 | Browser smoke |
| Clear all history | Backlog | P2 | 未実装 | 設定画面または確認付き操作で実装 | Browser smoke |
| Backup location guidance | Backlog | P2 | 未整理 | Electron 配布時の保存場所を説明 | README |

## UI / UX IMPLEMENTATION

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Modular HUD assets | Verified | P0 | 9-slice と modular kit を導入 | 新規 UI surface 追加時は asset check に追加 | Static check |
| Dense spread layout | Verified | P0 | P3 overlap まで解消済み | 主要変更時に visual audit を再実行 | `issueCount: 0` |
| Mobile layout | Verified | P0 | 390px 幅 smoke 済み | 低縦幅 viewport を追加確認 | Mobile screenshot |
| Keyboard flow | Active | P1 | 未監査 | Tab order, focus, Enter/Space の smoke を作る | Keyboard smoke |
| Accessibility labels | Backlog | P2 | 未整理 | Button/slot/history に aria-label を付ける | Accessibility check |
| Error states | Backlog | P2 | import 失敗は表示済み。asset load / storage 失敗は最小 | asset load 失敗、storage 失敗を表示 | Error smoke |

## LEARNING / REVIEW

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Guide after note | Verified | P0 | 現行 MVP の核として成立 | Regression check を維持 | Web smoke |
| Reading history | Implemented | P0 | 保存済み一覧と要約を表示 | 選択時の詳細を読み返しやすくする | Screenshot |
| Review mode | Active | P1 | 未実装 | 履歴からカード別/問い別に復習する画面を設計 | Requirements |
| Search / filter | Backlog | P2 | 未実装 | スプレッド、カード、日付、キーワードで絞る | Search smoke |
| Study progress | Backlog | P2 | 未実装 | 引いた回数、未復習カード、自己解釈の変化を見る | Study report |

## ELECTRON / DISTRIBUTION

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Electron shell | Verified | P0 | `npm run desktop` 相当の shell がある | 変更時に electron smoke を通す | Electron smoke |
| Packaging | Active | P1 | 未実装 | electron-builder などの採用判断と Windows package 作成 | Local package smoke |
| App icon | Backlog | P1 | 未設定 | ONOKO ARCANA 用 icon を作る | Packaged app |
| Auto update | Hold | P3 | 未検討 | 配布方式が決まるまで保留 | Distribution plan |
| Settings screen | Backlog | P2 | 未実装 | 保存場所、履歴操作、表示設定を整理 | Settings smoke |

## UNREAL LANE

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Unreal project | Hold | P2 | UE 5.7 project と C++ runtime 成果あり | Web MVP 安定後に再評価 | `plan.md` |
| Native fallback HUD | Hold | P2 | 1枚引き proof あり | 2D MVP で必要価値が明確になってから続行 | Phase proof |
| UE Python actor spawn | Hold | P3 | 過去に crash あり | 完成証跡には使わない | AGENTS rule |
| Premium 3D table | Backlog | P3 | 構想のみ | Web卓で欲しい 3D 価値を具体化後 | New requirements |

## QA / TOOLING

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Static app check | Verified | P0 | `scripts/check_web_app.py` が import UI/runtime terms も確認 | schema checks をさらに厳密化する場合だけ拡張 | `reports/web-app-check-20260604-033125.json` |
| Web smoke | Verified | P0 | `scripts/smoke_web_app.cjs` が export/import/duplicate/invalid JSON も確認 | delete/keyboard が入ったら拡張 | `reports/web-app-smoke-20260604-033139.json` |
| Electron smoke | Verified | P0 | `scripts/smoke_electron_app.cjs` | packaging 後の起動確認を追加 | JSON report |
| Visual audit | Verified | P0 | `scripts/audit_web_ui_visual.cjs` は import ボタン追加後も issueCount 0 | viewport とケースを増やす | `reports/ui-visual-audit-20260604-033211/report.json` |
| Regression snapshots | Backlog | P2 | reports に蓄積 | 代表スクショだけを index 化する | Report index |

## 次に進める順序

1. 履歴の単体削除と clear all の方針を決める。
2. キーボード操作と focus 表示の smoke を追加する。
3. Electron packaging の採用方式を決め、Windows ローカル package を作る。
4. 復習ビューの要件を切り、カード別/問い別の再読みに進む。
5. localStorage schema / import schema の短い仕様書を残す。

## 完了報告に含めるもの

- 変更したファイル。
- 実行した検証コマンド。
- 生成された `reports/` の JSON とスクリーンショット。
- 未検証の場合は、理由と代替確認。
- デザインに影響する場合は `docs/design/DESIGN_KANBAN.md` の該当項目更新。
