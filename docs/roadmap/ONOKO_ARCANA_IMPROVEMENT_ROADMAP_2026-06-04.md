# ONOKO ARCANA 改善ロードマップ

Updated: 2026-06-05

この文書は、初期カンバン `docs/design/overall-design-kanban.md` を起点に、現行の Web/Electron 版で足りていない要素、改善すべき要素、アップデートすべき文書と検証をロードマップ化したものである。親ロードマップは `docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md` とし、この文書は改善項目の実行順と完了条件を管理する。

## 1. 改善方針

- まず保存済みリーディングを壊さない。
- 画面の雰囲気より、問い、カード、メモ、guide、履歴の可読性を優先する。
- 追加機能は Web smoke / Electron smoke / visual audit のいずれかで証明できる形にする。
- Unreal 化は現行 v1.x では完全に見送り、既存成果はアーカイブする。小アルカナは Web/Electron 版の保存、復習、配布が安定するまで Hold とする。
- 初期カンバンは世界観の基準として残し、実行管理はこの改善ロードマップ、デザインカンバン、実装カンバンで行う。

## 2. 改善項目の全体優先度

| Priority | 意味 |
|---|---|
| P0 | 壊すと現行MVPの信頼性が落ちる。すぐ対応する |
| P1 | v1.0 の実用性に必要。次の実装スライス候補 |
| P2 | 体験品質、保守性、配布品質を上げる |
| P3 | 安定後の拡張。今は着手条件だけ決める |

## 3. Phase 1: 履歴安全性とデータ保護

目的: 保存済みの読みを安全に管理し、失わず、戻せる状態にする。

| Item | Priority | 現在 | 改善内容 | Done | 検証 |
|---|---|---|---|---|---|
| 履歴単体削除 | P0 | Verified | 履歴1件を削除できる。誤操作防止を入れる | 削除後に件数、一覧、選択状態が正しい | `reports/web-app-smoke-20260605-004943.json` |
| 履歴全削除 | P0 | Verified | 確認つきで全履歴を消す | 全削除後にempty stateとexport disabledが正しい | `reports/web-app-smoke-20260605-004943.json` |
| 削除前backup導線 | P1 | Verified | 削除前に書き出しを促す | 削除UIにbackup注意がある | `reports/onoko-arcana-initial-history-fit-20260604-054738.png` |
| import/export schema note | P1 | Verified | `localStorage` と export JSON v1 を文書化 | schema、必須フィールド、互換方針がある | `docs/data/HISTORY_SCHEMA_V1.md` |
| migration policy | P1 | Verified | history v2以降の移行方針を決める | 破壊的変更時の手順がある | `docs/data/HISTORY_SCHEMA_V1.md` |
| storage failure表示 | P2 | Verified | localStorage保存/読込失敗時に表示 | 破損JSONをUIに出せる | `reports/web-app-smoke-20260605-004943.json` |
| fixture JSON | P2 | Verified | 正常/重複/壊れた履歴fixtureを置く | smokeで使える代表fixtureがある | `tests/fixtures/history/`, `reports/web-app-check-20260605-004943.json` |

更新対象:

- `web-app/src/app.js`
- `web-app/index.html`
- `web-app/src/styles.css`
- `scripts/smoke_web_app.cjs`
- `scripts/check_web_app.py`
- `docs/implementation/IMPLEMENTATION_KANBAN.md`
- `docs/data/HISTORY_SCHEMA_V1.md` 新規候補

## 4. Phase 2: 操作性とアクセシビリティ

目的: 見た目だけでなく、繰り返し使いやすい操作面にする。

| Item | Priority | 現在 | 改善内容 | Done | 検証 |
|---|---|---|---|---|---|
| keyboard smoke | P1 | Verified | Tab順、Enter/Space、focus遷移を検証 | 主要操作がマウスなしで完了 | `reports/keyboard-focus-smoke-20260605-005005.json` |
| focus表示整理 | P1 | Verified | 選択中、focus、disabledの意味を分ける | 見た目と状態が矛盾しない | `reports/ui-visual-audit-20260605-004949/report.json` |
| ARIA label | P1 | Implemented | ボタン、カードslot、履歴項目にlabelを付与 | 履歴復元/削除が判別できる | Static check |
| 低縦幅viewport | P2 | Verified | 1280x720、1366x768を監査 | 主要操作が折り返し/重なりなし | Visual audit |
| 長文overflow | P2 | Verified | 長い問い、メモ、履歴、guideを監査 | テキストが枠外へ破綻しない | Visual audit |
| 初回起動empty state | P2 | 最小 | 次に押すべき操作が分かる | 初回画面で迷いが少ない | Screenshot review |

更新対象:

- `web-app/src/styles.css`
- `web-app/index.html`
- `scripts/audit_web_ui_visual.cjs`
- `scripts/smoke_web_app.cjs`
- `docs/design/DESIGN_KANBAN.md`

## 5. Phase 3: 読みの完了感と復習体験

目的: 保存履歴を単なる一覧から、タロット学習に使える復習体験へ拡張する。

| Item | Priority | 現在 | 改善内容 | Done | 検証 |
|---|---|---|---|---|---|
| 保存後の次アクション | P1 | Implemented | 次の読み、履歴復習、書き出しを自然に案内 | 保存後の履歴復習導線が明確 | Web smoke / screenshot |
| 履歴詳細ビュー | P1 | Verified | 1件の読みを詳細表示する | 問い、全カード、noteが見返せる | `reports/web-app-smoke-20260605-004943.json` |
| カード別復習 | P1 | 未実装 | 同じカードの過去読みを比較 | カード別に履歴が引ける | Review smoke |
| 問い/スプレッドfilter | P2 | 未実装 | 日付、スプレッド、カード、キーワードで絞る | 履歴が増えても探せる | Search smoke |
| 学習進捗 | P2 | 未実装 | よく引いたカード、未復習カードを表示 | 学習状態が分かる | Study report |
| guide比較改善 | P2 | guide表示あり | 自分の読みとguideを並べて比較 | 暗記でなく比較学習できる | Screenshot |

更新対象:

- `web-app/src/app.js`
- `web-app/src/styles.css`
- `data/major-arcana-v5-deck.json`
- `scripts/smoke_web_app.cjs`
- `docs/design/DESIGN_KANBAN.md`
- `docs/implementation/IMPLEMENTATION_KANBAN.md`

## 6. Phase 4: Desktop packaging とローカル運用

目的: 直接HTMLではなく、ローカルデスクトップアプリとして使いやすくする。

| Item | Priority | 現在 | 改善内容 | Done | 検証 |
|---|---|---|---|---|---|
| packaging方式決定 | P1 | Verified | electron-builder等を比較し採用判断 | 依存追加なしのlocal folder packageを採用 | `README.md`, `scripts/package_electron_local.cjs` |
| Windows local package | P1 | Verified | ローカルで起動できるpackageを作る | packageから起動できる | `dist/onoko-arcana-local/`, `reports/electron-package-smoke-20260605-005006.json` |
| app icon | P1 | Implemented | ONOKO ARCANA iconを設定 | Electron window iconにカード裏面を使用 | `web-app/electron/main.cjs` |
| 保存場所説明 | P1 | Verified | Electronでの履歴保存/backup場所を説明 | READMEに運用説明がある | `README.md`, `web-app/README.md` |
| package smoke | P1 | Verified | package後の起動、保存、import/exportを検証 | packaged appで主要loopが通る | `reports/electron-package-smoke-20260605-005006.json` |
| settings screen | P2 | 未実装 | 保存、履歴、表示設定を整理 | 基本設定が操作可能 | Settings smoke |

更新対象:

- `web-app/package.json`
- `web-app/electron/main.cjs`
- `web-app/README.md`
- `README.md` 新規または既存更新候補
- `scripts/smoke_electron_app.cjs`
- `docs/implementation/IMPLEMENTATION_KANBAN.md`

## 7. Phase 5: デザインシステムと素材管理

目的: 初期カンバンの世界観を維持しつつ、素材とUI状態を管理しやすくする。

| Item | Priority | 現在 | 改善内容 | Done | 検証 |
|---|---|---|---|---|---|
| component state set | P1 | 部分対応 | active/disabled/focus/errorを揃える | 状態差が一貫する | Visual audit |
| 操作icon体系 | P1 | 装飾icon中心 | 操作iconと装飾iconを分ける | 意味のあるiconだけ操作に使う | Design review |
| asset manifest | P1 | Implemented | 本番採用素材と実験素材を分ける | package scriptが採用素材のみコピーし、static checkが必須素材を確認 | `scripts/package_electron_local.cjs`, `scripts/check_web_app.py` |
| screenshot index | P2 | Implemented | reportsに蓄積 | 代表証跡と一時runの扱いを分ける | `reports/README.md` |
| copy調整 | P2 | 短文あり | 操作明瞭性と占いらしさを調整 | 日本語UIが自然 | Copy review |
| reveal motion | P2 | 最小 | 低モーション対応込みで演出追加 | motion offでも破綻しない | Visual smoke |

更新対象:

- `docs/design/DESIGN_KANBAN.md`
- `DESIGN.md`
- `assets/generated/`
- `scripts/check_web_app.py`
- `scripts/audit_web_ui_visual.cjs`
- `reports/INDEX.md` 新規候補

## 8. Phase 6: コンテンツ/データの堅牢化

目的: カード、スプレッド、履歴を長期運用できるデータ構造にする。

| Item | Priority | 現在 | 改善内容 | Done | 検証 |
|---|---|---|---|---|---|
| card data schema | P1 | Verified | カード定義の必須項目を明記 | schema文書がある | `docs/data/CARD_SCHEMA_V1.md` |
| spread schema | P1 | Verified | slot/reveal/guide/layout規約を明記 | 新spread追加手順がある | `docs/data/SPREAD_SCHEMA_V1.md` |
| history schema | P1 | Verified | 保存履歴形式を明記 | import/export互換が説明される | `docs/data/HISTORY_SCHEMA_V1.md` |
| sample fixtures | P2 | Verified | 代表fixtureを固定 | regressionに使える | `tests/fixtures/history/`, `reports/web-app-smoke-20260605-004943.json` |
| custom spread準備 | P3 | 未実装 | 保存/復習/配布後に検討 | 要件だけある | Requirements |

更新対象:

- `docs/data/CARD_SCHEMA.md` 新規候補
- `docs/data/SPREAD_SCHEMA.md` 新規候補
- `docs/data/HISTORY_SCHEMA_V1.md` 新規候補
- `data/spread-definitions-v1.json`
- `web-app/src/data.js`
- `scripts/check_web_app.py`

## 9. Phase 7: Unreal Archive / 小アルカナ / 拡張ゲート

目的: UE化を現行ロードマップ外へ出し、拡張を急がず、安定後の判断材料を残す。

| Item | Priority | 現在 | 改善内容 | Done | 検証 |
|---|---|---|---|---|---|
| UE scope archive | P0 | Verified | UE再開条件を設定せず、既存成果を履歴として保持 | v1.xはWeb/Electron onlyと明記 | Doc review |
| Web parity checklist | P3 | 不要 | UE移植対象表は作らない | 移植前提を消す | Checklistなし |
| 3D premium prototype | P3 | 見送り | 現行ロードマップから除外 | 実装タスクに混ぜない | UE proofなし |
| 小アルカナ設計 | P3 | Hold | 56枚追加のコストを見積もる | asset/QA計画がある | Requirements |
| 複数デッキ/カスタムデッキ | P3 | 未着手 | データ構造だけ検討 | v1.0後の候補に留める | Requirements |

着手条件:

- 履歴削除、schema、復習、packagingが完了している。
- Web/Electron版を日常使用できる。
- 拡張によって現行履歴やカード表示が壊れない。
- UEについては着手条件を置かない。必要なら別ロードマップで新規定義する。

## 10. アップデートすべき文書一覧

| Document | 更新目的 | タイミング |
|---|---|---|
| `docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md` | 全体方針とフェーズの親管理 | 大きな方針変更時 |
| `docs/roadmap/ONOKO_ARCANA_IMPROVEMENT_ROADMAP_2026-06-04.md` | 改善項目の実行管理 | 改善スライス完了時 |
| `docs/design/DESIGN_KANBAN.md` | デザイン状態、可読性、UI方針 | UI/UX変更時 |
| `docs/implementation/IMPLEMENTATION_KANBAN.md` | 実装状態、証跡、次順序 | 機能実装/検証時 |
| `PRODUCT.md` | 製品目的と境界 | ユーザー体験やv1.0定義が変わる時 |
| `DESIGN.md` | 色、レイアウト、コンポーネント方針 | UI基準が変わる時 |
| `web-app/README.md` | 実行、検証、Electron操作 | runtimeやpackaging変更時 |
| `README.md` | プロジェクト入口 | package/配布段階で作成または更新 |
| `docs/data/*.md` | schemaとmigration | データ形式を固定する時 |
| `reports/INDEX.md` | 代表証跡索引 | visual/smoke証跡が増えた時 |

## 11. 次に着手する実装順

1. カード別/問い別/スプレッド別の復習filter設計。
2. settings screenで保存、履歴、表示設定を整理する。
3. 初回起動empty stateと保存後の次アクションを磨く。
4. 外部配布する場合のみ、署名installer、`.ico`、auto updateを別スコープで定義する。

## 12. 完了ゲート

この改善ロードマップの Web-only completion gate は 2026-06-04 時点で完了した。v1.0 準備完了には、次の条件を満たす必要がある。

- 履歴の保存、import/export、削除、backup方針が揃っている。
- キーボード操作と主要focus状態が検証済み。
- Electron packageで主要loopが通る。
- 履歴を学習に使う復習ビューがある。
- データschema、fixture、migration方針が文書化されている。
- visual auditが主要viewportで issueCount 0 を維持している。
- Unreal化が現行ロードマップ外であることと、小アルカナの再開条件が文書上で明確である。
