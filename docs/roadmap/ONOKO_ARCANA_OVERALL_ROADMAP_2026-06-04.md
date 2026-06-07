# ONOKO ARCANA 全体ロードマップ

Updated: 2026-06-07

この文書は、ONOKO ARCANA を「画像素材と試作がある状態」から「日常的に使えるデスクトップ占い学習アプリ」へ進めるための全体ロードマップである。既存の研究ロードマップは履歴として保持し、現時点の本線は Web/Electron-ready な 2D 占い卓とする。Unreal Engine 化は v1.x ロードマップでは完全に見送り、既存UE成果はアーカイブ証跡として保持する。

学習強化の詳細ロードマップは `docs/roadmap/TAROT_LEARNING_ENHANCEMENT_ROADMAP_2026-06-06.md` を参照する。この文書はネット調査と `$define-requirements` に基づき、カード別復習、カード学習シート、想起練習、間隔復習、スプレッド学習、Minor Arcana 準備を段階化したものである。

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
| Learning loop | 初回導線 -> 自分の読みを書く -> 同じカードの学習シートを参照する -> 保存 -> 履歴で見返す -> 学習シート前に想起練習する -> スロット解釈を練習する -> due 復習に戻る |
| Persistence | `localStorage` history v1 + learning v1 draft |
| Data portability | history JSON export / import + learning JSON export / import / clear |
| Latest proof | `reports/web-app-check-20260607-061238.json`, `reports/web-app-smoke-20260607-061029.json`, `reports/keyboard-focus-smoke-20260607-061239.json`, `reports/ui-visual-audit-20260607-061249/report.json`, `reports/electron-app-smoke-20260607-061249.json`, `reports/electron-package-smoke-20260607-061337.json`, `reports/onoko-arcana-installer-smoke-20260607-052003.json`, CI `27072878818` success |

## 2. 製品ゴール

ONOKO ARCANA の v1.0 ゴールは、次の状態である。

- 起動直後に占い卓として使える。
- ユーザーが問いを書き、スプレッドを選び、カードを引き、順番にめくれる。
- `カード` タブで、ユーザーが自分の読みを書きながら同じカードのフル学習シートを参照できる。
- 過去の読みを失わず、書き出し、読み込み、削除、復習ができる。
- Web版の動作と Electron デスクトップ版の動作が同じ検証で追える。
- ONOKO らしい雰囲気を維持しつつ、日本語テキストが読める。
- 大アルカナ学習アプリとして安定してから、小アルカナや3D表現へ進む。

## 3. ロードマップの判断原則

- カード再生成より、実際に使える読解・保存・復習ループを優先する。
- 追加機能は、保存データを壊さないことを最優先にする。
- 画面の装飾は、カード、問い、メモ、学習シート、履歴の可読性を妨げない範囲にする。
- Web/Electron 本線の学習体験を完成させ、Unreal には戻らない。
- 小アルカナは、履歴/復習/配布/検証が安定するまで着手しない。

## 4. フェーズ計画

### Phase A: MVP Core Stabilization

Status: Web/Electron local package gate complete

目的は、現行の Web/Electron 版を「日常的に試用できる最小プロダクト」にすることである。

完了済み:

- 6種類のスプレッド選択。
- ドロー、順番 reveal、選択カード Inspector。
- note 入力中に同じカードの学習シートを参照できるカードタブ。
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
| 初回起動の空状態改善 | P2 | Verified: 履歴 0 件時に問いを書く、1枚引きで始める、保存後に復習する流れを案内 |

推奨順:

1. 履歴の単体削除。
2. 全削除と確認UI。
3. import/export schema note。
4. 保存失敗表示。
5. 初回空状態は検証済み。以後は実使用メモから文言だけ調整する。

### Phase B: Usability And Accessibility

Status: Web-only gate complete / deeper a11y remains

目的は、画面が美しいだけでなく、繰り返し使える操作面にすることである。

| Item | Priority | Done |
|---|---|---|
| キーボード操作 smoke | P1 | Verified: `reports/keyboard-focus-smoke-20260604-041422.json` |
| Focus visual alignment | P1 | Verified: focus outlineとvisual audit issueCount 0 |
| ARIA label 整理 | P2 | Implemented: 履歴復元/削除にaria-label追加。全体監査は継続 |
| 低縦幅 viewport 監査 | P2 | Verified: visual auditに1280x720を追加 |
| 長文履歴/学習シート overflow 監査 | P2 | Verified: 新しい履歴/復習/ノート/学習シート要素をvisual audit対象に追加 |

完了条件:

- `scripts/smoke_web_app.cjs` または新規 smoke がキーボード操作を検証する。
- `scripts/audit_web_ui_visual.cjs` が追加viewportでも issueCount 0 を保つ。
- 視覚的なONOKO感より、操作可能性と可読性を優先できている。

### Phase C: Desktop Packaging

Status: Verified for GitHub public preview installer v0.1.3 and post-release support hardening

目的は、開発用HTMLから、実際にローカルで起動しやすいデスクトップアプリへ進めることである。

| Item | Priority | Done |
|---|---|---|
| packaging方式決定 | P1 | Verified: 依存追加なしの `dist/onoko-arcana-local/` 方式を採用 |
| Windows local package | P1 | Verified: `scripts/package_electron_local.cjs` |
| app icon | P1 | Verified: `imagegen` 生成の透明 PNG と Windows `.ico` を採用し、Electron window/taskbar 用に `AppUserModelID` も設定 |
| Desktop shortcut helper | P1 | Verified: `CREATE_DESKTOP_SHORTCUT.ps1` が `ONOKO ARCANA.lnk` を作成/更新し、`IconLocation` に `onoko-arcana-app-icon-v1.ico` を設定 |
| 保存場所の説明 | P1 | Verified: `README.md`, `web-app/README.md` |
| package smoke | P1 | Verified: `reports/electron-package-smoke-20260607-061337.json` |
| NSIS installer | P1 | Verified: `onoko-arcana-v0.1.3-setup.exe` をGitHub Releaseの主導線にし、CI/tagでsetup.exe、fallback zip、SHA256を配布 |
| Release/support settings | P1 | Verified: Settings に最新版Release、公式Repo、Security、License、未署名/自動更新なし、更新前backup cueを追加し、Web/Electron/package/installer smokeで確認 |
| External link allowlist | P1 | Verified: Electron外部リンクは `https://github.com/imonoonoko/ONOKO_ARCANA` 配下のみ許可 |

保留:

- Auto update は v1.0 前には必須ではない。
- GitHub Release public preview は `v0.1.3` でunsigned installer主導線まで実施済み。code signing、MSIX、store distribution は別ゲートで判断する。

### Phase D: Review And Study Mode

Status: Active

目的は、保存履歴を単なる一覧ではなく、タロット学習に使える復習体験へ進めることである。

| Item | Priority | Done |
|---|---|---|
| 履歴詳細ビュー | P1 | Verified: 履歴選択後に復習ノートで問い、カード、noteを表示 |
| カード別復習 | P1 | Verified: 同じカードが出た過去の読みをカード別に絞り込める |
| 問い/スプレッド別filter | P2 | 日付、カード、スプレッド、キーワードで絞れる |
| 学習レンズ | P1 | Verified: 履歴から保存数、メモ数、既出/未出カード、よく出るカード、次の観測候補を表示 |
| 学習進捗 | P2 | Verified: よく引いたカード、未出カード、想起練習回数、compact表示設定、due card 数と cue を表示/操作済み |
| 学習シート比較改善 | P2 | Verified: カード別復習中に、自分の読み、学習シート要点、slot prompt を同じ履歴カード内で比較できる |
| 想起練習 | P1 | Verified: 学習シートを見る前にキーワードや逆位置傾向を入力し、答え合わせ後に hard/ok/easy を保存できる |
| 学習データ管理 | P1 | Verified: settings で履歴データ、学習データ、表示設定、保存keyを分け、学習データのexport/import/clearをWeb smokeで確認 |
| 初回/保存後学習導線 | P1 | Verified: 初回は学習 loop を案内し、保存後は復習開始または次の問いへ進める |

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
| Learning schema v1 draft | P1 | Verified: `docs/data/LEARNING_SCHEMA_V1_DRAFT.md`, `tests/fixtures/learning/learning-valid-v1.json` |
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
| Installer smoke gate | installer作成後、Release主導線、icon、packaged resource、Release/support settings変更時 | `scripts/smoke_electron_installer_app.cjs` |
| Manual installer gate | GitHub Release昇格、installer config、署名、uninstall、実ショートカット表示変更時 | `docs/release/INSTALLER_MANUAL_SMOKE_CHECKLIST.md` |
| Visual gate | UI、CSS、HUD asset、layout変更時 | `scripts/audit_web_ui_visual.cjs` |
| Workflow gate | 複数工程の実装/検証/文書更新時 | `.workflow/<slug>/final-report.md` |

## 6. リスク管理

| Risk | 影響 | 対策 |
|---|---|---|
| 履歴データ破損 | ユーザーの学習記録を失う | export/import、schema note、migration policy、削除確認 |
| UI過密 | ONOKO感より読みにくさが勝つ | visual audit、低解像度確認、右パネル肥大化の抑制 |
| Electron配布で保存場所が不明 | 実使用時にバックアップできない | READMEに保存/復元/バックアップ方針を明記済み。export JSONを正式backup経路にする |
| Release版ユーザーが最新版/License/Supportへ戻れない | 古いinstallerや権利誤解が残る | Settingsにlatest Release、Repo、Security、License、未署名/自動更新なし、backup cueを表示し、smokeで固定 |
| 未署名installerの実環境ブロック | SmartScreen/AV/企業ポリシーで導入できない | fallback zipを維持し、clean Windows user/VMでmanual installer smokeを実行する |
| UE表現への回帰 | MVP完成が遅れる | UEはArchived、Web/Electron本線の完了条件を優先 |
| 小アルカナ追加の爆発 | asset数とQAが大幅増加 | Expansion Gateまで着手しない |

## 7. 現在の次アクション

次に進める順序は次の通り。

1. `docs/release/INSTALLER_MANUAL_SMOKE_CHECKLIST.md` は clean Windows user/VM が用意できるまで manual pending として残す。SmartScreen、実ショートカットicon、uninstall、fallback zipはまだ外部環境未確認。
2. 履歴filterはカード、スプレッド、メモ有無まで実装済み。次に進めるなら問いテキストと保存日filterを小スライスで追加する。
3. Spread Tutor と Story Synthesis の要件を、学習UIの密度を増やしすぎない形で定義する。
4. 7日/14日 interval を入れる場合は learning fixture と due smoke を先に増やす。
5. code signing、MSIX、Store、auto updateは、manual installer smokeと実ユーザー反応後に別スコープで定義する。
6. 小アルカナ拡張は、復習filterと配布判断が安定してから再評価する。

## 8. 完了チェックポイント

この全体ロードマップは、Web/Electron-only 完了ゲートを 2026-06-04 時点で通過し、local package/schema/fixture hardening gateを 2026-06-05 時点で通過した。2026-06-06 時点では、カード別復習、Card Study Sheet、Recall Practice、Slot Interpretation Drill、settings learning data controls、初回導線、保存後アクション、最小 due card queue が検証済み。2026-06-07 時点では、GitHub Release `v0.1.3` のunsigned installer配布、自動installer/package smoke、Release/support settings、Electron外部リンクallowlist、CI `27072878818` が検証済みで、clean Windows manual installer smoke は未実施である。同日、履歴filterはカード、スプレッド、メモ有無までWeb smokeで検証済み。v1.0全体では、manual installer smoke、問い/日付filter判断、Spread Tutor要件、配布polishが残る。

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
- `reports/web-app-check-20260606-195432.json`
- `reports/web-app-smoke-20260606-194424.json`
- `reports/electron-app-smoke-20260606-194716.json`
- `reports/keyboard-focus-smoke-20260606-194648.json`
- `reports/ui-visual-audit-20260606-194648/report.json`
- `reports/onoko-arcana-first-launch-20260606-194424.png`
- `reports/web-app-check-20260607-061238.json`
- `reports/web-app-smoke-20260607-061029.json`
- `reports/keyboard-focus-smoke-20260607-061239.json`
- `reports/ui-visual-audit-20260607-061249/report.json`
- `reports/electron-app-smoke-20260607-061249.json`
- `reports/electron-package-smoke-20260607-061337.json`
- `reports/onoko-arcana-installer-smoke-20260607-052003.json`
- GitHub Actions CI `27072878818`

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
