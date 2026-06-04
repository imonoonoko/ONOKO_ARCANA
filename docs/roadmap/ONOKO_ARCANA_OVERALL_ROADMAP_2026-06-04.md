# ONOKO ARCANA 全体ロードマップ

Updated: 2026-06-05

この文書は、ONOKO ARCANA を「画像素材と試作がある状態」から「日常的に使えるデスクトップ占い学習アプリ」へ進めるための全体ロードマップである。既存の研究ロードマップは履歴として保持し、現時点の本線は Web/Electron-ready な 2D 占い卓とする。Unreal Engine 化は v1.x ロードマップでは完全に見送り、既存UE成果はアーカイブ証跡として保持する。

## 1. 現在地

| 領域 | 現在 |
|---|---|
| Product | PC上でタロットカードを持たずに占い、読み、記録し、学習できるアプリ |
| Main runtime | `web-app/index.html` |
| Desktop shell | `web-app/electron/main.cjs` |
| Runtime direction | Web/Electron only |
| Visual direction | ONOKO 風 cyber divination table |
| Card scope | V5 大アルカナ 22 枚 + 裏面 1 枚 |
| Spread scope | 1枚引き、3枚、五枚クロス、七枚ホースシュー、ケルト十字、関係性ライン |
| Learning loop | 自分の読みを書く -> guide を開く -> 保存 -> 履歴で見返す |
| Persistence | `localStorage` history v1 |
| Data portability | history JSON export / import |
| Latest proof | `reports/web-app-check-20260605-004943.json`, `reports/web-app-smoke-20260605-004943.json`, `reports/electron-app-smoke-20260605-004947.json`, `reports/electron-package-smoke-20260605-005006.json`, `reports/keyboard-focus-smoke-20260605-005005.json`, `reports/ui-visual-audit-20260605-004949/report.json` |

## 2. 製品ゴール

ONOKO ARCANA の v1.0 ゴールは、次の状態である。

- 起動直後に占い卓として使える。
- ユーザーが問いを書き、スプレッドを選び、カードを引き、順番にめくれる。
- guide は答えを先に与えず、ユーザーの解釈入力後に開ける。
- 過去の読みを失わず、書き出し、読み込み、削除、復習ができる。
- Web版の動作と Electron デスクトップ版の動作が同じ検証で追える。
- ONOKO らしい雰囲気を維持しつつ、日本語テキストが読める。
- 大アルカナ学習アプリとして安定してから、小アルカナや3D表現へ進む。

## 3. ロードマップの判断原則

- カード再生成より、実際に使える読解・保存・復習ループを優先する。
- 追加機能は、保存データを壊さないことを最優先にする。
- 画面の装飾は、カード、問い、メモ、guide、履歴の可読性を妨げない範囲にする。
- Web/Electron 本線の学習体験を完成させ、Unreal には戻らない。
- 小アルカナは、履歴/復習/配布/検証が安定するまで着手しない。

## 4. フェーズ計画

### Phase A: MVP Core Stabilization

Status: Web/Electron local package gate complete

目的は、現行の Web/Electron 版を「日常的に試用できる最小プロダクト」にすることである。

完了済み:

- 6種類のスプレッド選択。
- ドロー、順番 reveal、選択カード Inspector。
- note 入力後の guide 表示。
- localStorage 保存。
- history JSON export / import。
- Web smoke、Electron smoke、package smoke、keyboard smoke、visual audit。

残作業:

| Item | Priority | Done |
|---|---|---|
| 履歴の単体削除 | P1 | Verified: 確認つき削除、件数/一覧/復習パネル更新をWeb smokeで確認 |
| 履歴の全削除 | P1 | Verified: 確認つき全消去、empty state、export/clear disabledをWeb smokeで確認 |
| 保存/読み込み schema note | P1 | Verified: `docs/data/HISTORY_SCHEMA_V1.md` |
| storage failure 表示 | P2 | Verified: 保存/読み込み/削除失敗時と破損localStorageのメッセージをWeb smokeで確認 |
| 初回起動の空状態改善 | P2 | 初回でも次の操作が分かる |

推奨順:

1. 履歴の単体削除。
2. 全削除と確認UI。
3. import/export schema note。
4. 保存失敗表示。
5. 初回空状態の文言調整。

### Phase B: Usability And Accessibility

Status: Web-only gate complete / deeper a11y remains

目的は、画面が美しいだけでなく、繰り返し使える操作面にすることである。

| Item | Priority | Done |
|---|---|---|
| キーボード操作 smoke | P1 | Verified: `reports/keyboard-focus-smoke-20260604-041422.json` |
| Focus visual alignment | P1 | Verified: focus outlineとvisual audit issueCount 0 |
| ARIA label 整理 | P2 | Implemented: 履歴復元/削除にaria-label追加。全体監査は継続 |
| 低縦幅 viewport 監査 | P2 | Verified: visual auditに1280x720を追加 |
| 長文履歴/guide overflow 監査 | P2 | Verified: 新しい履歴/復習/ノート要素をvisual audit対象に追加 |

完了条件:

- `scripts/smoke_web_app.cjs` または新規 smoke がキーボード操作を検証する。
- `scripts/audit_web_ui_visual.cjs` が追加viewportでも issueCount 0 を保つ。
- 視覚的なONOKO感より、操作可能性と可読性を優先できている。

### Phase C: Desktop Packaging

Status: Verified for local package

目的は、開発用HTMLから、実際にローカルで起動しやすいデスクトップアプリへ進めることである。

| Item | Priority | Done |
|---|---|---|
| packaging方式決定 | P1 | Verified: 依存追加なしの `dist/onoko-arcana-local/` 方式を採用 |
| Windows local package | P1 | Verified: `scripts/package_electron_local.cjs` |
| app icon | P1 | Implemented: Electron window iconに既存カード裏面PNGを使用。installer用 `.ico` は後続 |
| 保存場所の説明 | P1 | Verified: `README.md`, `web-app/README.md` |
| package smoke | P1 | Verified: `reports/electron-package-smoke-20260605-005006.json` |

保留:

- Auto update は v1.0 前には必須ではない。
- 外部公開、署名、配布サイトは、ローカルpackage確認後に判断する。

### Phase D: Review And Study Mode

Status: Active

目的は、保存履歴を単なる一覧ではなく、タロット学習に使える復習体験へ進めることである。

| Item | Priority | Done |
|---|---|---|
| 履歴詳細ビュー | P1 | Verified: 履歴選択後に復習ノートで問い、カード、noteを表示 |
| カード別復習 | P1 | 同じカードが出た過去の読みを比較できる |
| 問い/スプレッド別filter | P2 | 日付、カード、スプレッド、キーワードで絞れる |
| 学習進捗 | P2 | よく引いたカード、未復習カード、自分の解釈変化が見える |
| guide比較改善 | P2 | 自分の読みとguideを比較しやすい |

完了条件:

- ユーザーが「過去の自分の読み」を探して学べる。
- 履歴が増えても右パネルだけに詰め込まない。
- 復習体験が占い卓の第一体験を邪魔しない。

### Phase E: Content And Data Hardening

Status: Active

目的は、データ定義、カード意味、スプレッド定義、保存形式を長期運用に耐える形にすることである。

| Item | Priority | Done |
|---|---|---|
| Card data schema | P1 | Verified: `docs/data/CARD_SCHEMA_V1.md` |
| Spread schema | P1 | Verified: `docs/data/SPREAD_SCHEMA_V1.md` |
| History schema v1 | P1 | Verified: `docs/data/HISTORY_SCHEMA_V1.md` |
| Migration policy | P2 | Verified: `docs/data/HISTORY_SCHEMA_V1.md` にv2以降の方針を記載 |
| Sample fixtures | P2 | Verified: `tests/fixtures/history/` |

完了条件:

- 将来の復習ビュー、packaging、小アルカナ追加でデータ構造が迷子にならない。
- 破壊的な保存形式変更を避ける判断材料がある。

### Phase F: Visual Polish And Motion

Status: Backlog

目的は、現行の読みやすさを維持したまま、占い卓としての手触りを上げることである。

| Item | Priority | Done |
|---|---|---|
| reveal motion | P2 | 低モーション設定を尊重しつつ、めくり感が出る |
| save/import feedback | P2 | 操作完了が視覚的に分かる |
| selected card feedback | P2 | 選択中カードが分かりやすく、過剰に光らない |
| component state set | P2 | active/disabled/focus/errorの見た目が揃う |
| representative screenshot index | P2 | 代表スクショと監査結果を一覧できる |

完了条件:

- 見た目の強化後も `visual audit` が issueCount 0 を保つ。
- 装飾の追加でカードや日本語説明が読みにくくならない。

### Phase G: Unreal Archive

Status: Archived

目的は、過去のUE調査と試作を失わず、現行MVPの判断材料としてアーカイブすることである。UE化は現行ロードマップから除外し、Web/Electron v1.x の完了条件には含めない。

運用:

- UE関連文書と証跡は削除しない。
- UE作業は新規実装タスクに混ぜない。
- UE再開条件は設定しない。必要になった場合は別プロジェクトまたは別ロードマップとして新規定義する。

アーカイブ対象:

| Item | Priority | Done |
|---|---|---|
| UE project evidence | P3 | 既存UE projectとPhase 1文書は履歴として保持 |
| UE safety notes | P3 | Python actor spawn crashなどの注意をAGENTS/文書に残す |
| Web-only scope lock | P0 | v1.x実装はWeb/Electronのみで進める |

### Phase H: Expansion Gate

Status: Hold

目的は、小アルカナ、追加スプレッド、カスタムデッキなどの拡張を、MVP安定後に判断することである。

着手条件:

- 大アルカナ版が日常使用できる。
- 履歴が増えても復習できる。
- package版で保存/復元が確認できる。
- データschemaとmigration方針がある。

候補:

| Item | Priority | Done |
|---|---|---|
| 小アルカナ設計 | P3 | 56枚追加の制作/検証コストが見積もられる |
| カスタムスプレッド | P3 | ユーザー定義slotと保存形式が決まる |
| カード検索/ギャラリー | P3 | 学習ビューとして必要な範囲が決まる |
| 複数デッキ | P3 | データ構造とasset管理が耐える |

## 5. 品質ゲート

| Gate | 実行タイミング | 必須証跡 |
|---|---|---|
| Static gate | Web app構造、ID、素材参照、runtime term変更時 | `python scripts/check_web_app.py` |
| Web smoke gate | 読み、保存、履歴、import/export変更時 | `scripts/smoke_web_app.cjs` |
| Electron smoke gate | shell、保存、packaging関連変更時 | `scripts/smoke_electron_app.cjs` |
| Package smoke gate | local package作成後、配布/保存導線変更時 | `scripts/smoke_electron_package.cjs` |
| Visual gate | UI、CSS、HUD asset、layout変更時 | `scripts/audit_web_ui_visual.cjs` |
| Workflow gate | 複数工程の実装/検証/文書更新時 | `.workflow/<slug>/final-report.md` |

## 6. リスク管理

| Risk | 影響 | 対策 |
|---|---|---|
| 履歴データ破損 | ユーザーの学習記録を失う | export/import、schema note、migration policy、削除確認 |
| UI過密 | ONOKO感より読みにくさが勝つ | visual audit、低解像度確認、右パネル肥大化の抑制 |
| Electron配布で保存場所が不明 | 実使用時にバックアップできない | READMEに保存/復元/バックアップ方針を明記済み。export JSONを正式backup経路にする |
| UE表現への回帰 | MVP完成が遅れる | UEはArchived、Web/Electron本線の完了条件を優先 |
| 小アルカナ追加の爆発 | asset数とQAが大幅増加 | Expansion Gateまで着手しない |

## 7. 現在の次アクション

次に進める順序は次の通り。

1. 履歴filter、カード別復習、問い別復習を設計する。
2. 初回起動empty stateと保存後の次アクションを磨く。
3. settings画面で保存、履歴、表示設定を整理する。
4. 外部配布する場合のみ、署名installer、`.ico`、auto updateを別スコープで定義する。
5. 小アルカナ拡張は、復習filterと配布判断が安定してから再評価する。

## 8. 完了チェックポイント

この全体ロードマップは、Web/Electron-only 完了ゲートを 2026-06-04 時点で通過し、local package/schema/fixture hardening gateを 2026-06-05 時点で通過した。v1.0全体では、復習filter、settings、配布polishが残る。

完了時点の判断:

- Web/Electron 2D占い卓を現在の本線とする。
- Unreal Engine 化は現行v1.xでは完全見送りとし、既存成果はアーカイブ証跡として保持する。
- 大アルカナ版の実使用安定化、履歴管理、配布、復習を小アルカナより優先する。
- 今回の完了ゲートでは、履歴削除、全消去、schema、fixture、破損履歴表示、local package、package smoke、キーボード/focus、復習ノート、ノート風UIが実装/検証済み。

完了時点の主要証跡:

- `reports/web-app-check-20260605-004943.json`
- `reports/web-app-smoke-20260605-004943.json`
- `reports/electron-app-smoke-20260605-004947.json`
- `reports/electron-package-smoke-20260605-005006.json`
- `reports/keyboard-focus-smoke-20260605-005005.json`
- `reports/ui-visual-audit-20260605-004949/report.json`

ロードマップ完了条件:

- 現在地、製品ゴール、判断原則、フェーズ、品質ゲート、リスク、次アクションが1文書で確認できる。
- 次に実装する順序が `docs/implementation/IMPLEMENTATION_KANBAN.md` と矛盾しない。
- 既存の研究ロードマップを消さず、Web/Electron 本線への方針変更を明示している。

## 9. 参照文書

- `PRODUCT.md`
- `DESIGN.md`
- `plan.md`
- `docs/design/DESIGN_KANBAN.md`
- `docs/implementation/IMPLEMENTATION_KANBAN.md`
- `docs/roadmap/ONOKO_ARCANA_IMPROVEMENT_ROADMAP_2026-06-04.md`
- `docs/design/overall-design-kanban.md`
- `docs/implementation/WEB_MVP_PIVOT_2026-06-02.md`
- `docs/roadmap/ONOKO_ARCANA_RESEARCH_GRADE_ROADMAP_V2_2026-05-31.md`
- `docs/roadmap/ONOKO_ARCANA_UNREAL_RESEARCH_ROADMAP_2026-05-31.md`
