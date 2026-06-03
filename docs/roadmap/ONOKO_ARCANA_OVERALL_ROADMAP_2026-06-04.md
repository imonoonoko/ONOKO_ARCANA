# ONOKO ARCANA 全体ロードマップ

Updated: 2026-06-04

この文書は、ONOKO ARCANA を「画像素材と試作がある状態」から「日常的に使えるデスクトップ占い学習アプリ」へ進めるための全体ロードマップである。既存の研究ロードマップは履歴として保持し、現時点の本線は Web/Electron-ready な 2D 占い卓とする。Unreal Engine は破棄せず、Web/Electron の学習ループが安定した後の高級 3D 表現レーンとして扱う。

## 1. 現在地

| 領域 | 現在 |
|---|---|
| Product | PC上でタロットカードを持たずに占い、読み、記録し、学習できるアプリ |
| Main runtime | `web-app/index.html` |
| Desktop shell | `web-app/electron/main.cjs` |
| Visual direction | ONOKO 風 cyber divination table |
| Card scope | V5 大アルカナ 22 枚 + 裏面 1 枚 |
| Spread scope | 1枚引き、3枚、五枚クロス、七枚ホースシュー、ケルト十字、関係性ライン |
| Learning loop | 自分の読みを書く -> guide を開く -> 保存 -> 履歴で見返す |
| Persistence | `localStorage` history v1 |
| Data portability | history JSON export / import |
| Latest proof | `reports/web-app-smoke-20260604-033139.json`, `reports/electron-app-smoke-20260604-033157.json`, `reports/ui-visual-audit-20260604-033211/report.json` |

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
- Web/Electron 本線で学習体験を固めてから、Unreal で高級表現を検討する。
- 小アルカナは、履歴/復習/配布/検証が安定するまで着手しない。

## 4. フェーズ計画

### Phase A: MVP Core Stabilization

Status: Active

目的は、現行の Web/Electron 版を「日常的に試用できる最小プロダクト」にすることである。

完了済み:

- 6種類のスプレッド選択。
- ドロー、順番 reveal、選択カード Inspector。
- note 入力後の guide 表示。
- localStorage 保存。
- history JSON export / import。
- Web smoke、Electron smoke、visual audit。

残作業:

| Item | Priority | Done |
|---|---|---|
| 履歴の単体削除 | P1 | 保存済みリーディングを1件ずつ削除でき、誤操作を防げる |
| 履歴の全削除 | P1 | 確認つきで全履歴を消せる |
| 保存/読み込み schema note | P1 | export/import JSON の短い仕様書がある |
| storage failure 表示 | P2 | 保存できない時にユーザーへ理由を出す |
| 初回起動の空状態改善 | P2 | 初回でも次の操作が分かる |

推奨順:

1. 履歴の単体削除。
2. 全削除と確認UI。
3. import/export schema note。
4. 保存失敗表示。
5. 初回空状態の文言調整。

### Phase B: Usability And Accessibility

Status: Active

目的は、画面が美しいだけでなく、繰り返し使える操作面にすることである。

| Item | Priority | Done |
|---|---|---|
| キーボード操作 smoke | P1 | Tab順、Enter/Space、focus表示が検証される |
| Focus visual alignment | P1 | 青い選択光とキーボードfocusの意味が矛盾しない |
| ARIA label 整理 | P2 | 主要ボタン、スロット、履歴項目が読み上げ可能 |
| 低縦幅 viewport 監査 | P2 | 1280x720級でも主要操作が破綻しない |
| 長文履歴/guide overflow 監査 | P2 | 長い問い、長いメモでもUIが壊れない |

完了条件:

- `scripts/smoke_web_app.cjs` または新規 smoke がキーボード操作を検証する。
- `scripts/audit_web_ui_visual.cjs` が追加viewportでも issueCount 0 を保つ。
- 視覚的なONOKO感より、操作可能性と可読性を優先できている。

### Phase C: Desktop Packaging

Status: Active

目的は、開発用HTMLから、実際にローカルで起動しやすいデスクトップアプリへ進めることである。

| Item | Priority | Done |
|---|---|---|
| packaging方式決定 | P1 | electron-builder等の採用/不採用理由が残る |
| Windows local package | P1 | ローカルで起動できる成果物が作れる |
| app icon | P1 | ONOKO ARCANA用iconが入る |
| 保存場所の説明 | P1 | Electron時の履歴保存/バックアップ方針がREADMEにある |
| package smoke | P1 | package後の起動、保存、履歴、import/exportを確認する |

保留:

- Auto update は v1.0 前には必須ではない。
- 外部公開、署名、配布サイトは、ローカルpackage確認後に判断する。

### Phase D: Review And Study Mode

Status: Backlog

目的は、保存履歴を単なる一覧ではなく、タロット学習に使える復習体験へ進めることである。

| Item | Priority | Done |
|---|---|---|
| 履歴詳細ビュー | P1 | 1件の読みを読み返しやすい形で表示できる |
| カード別復習 | P1 | 同じカードが出た過去の読みを比較できる |
| 問い/スプレッド別filter | P2 | 日付、カード、スプレッド、キーワードで絞れる |
| 学習進捗 | P2 | よく引いたカード、未復習カード、自分の解釈変化が見える |
| guide比較改善 | P2 | 自分の読みとguideを比較しやすい |

完了条件:

- ユーザーが「過去の自分の読み」を探して学べる。
- 履歴が増えても右パネルだけに詰め込まない。
- 復習体験が占い卓の第一体験を邪魔しない。

### Phase E: Content And Data Hardening

Status: Backlog

目的は、データ定義、カード意味、スプレッド定義、保存形式を長期運用に耐える形にすることである。

| Item | Priority | Done |
|---|---|---|
| Card data schema | P1 | カード定義の必須フィールドと変更手順がある |
| Spread schema | P1 | スプレッド追加時のslot/reveal/guide規約がある |
| History schema v1 | P1 | localStorageとexport/import形式が文書化される |
| Migration policy | P2 | v2以降の履歴移行方針がある |
| Sample fixtures | P2 | テスト用の代表履歴JSONがある |

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

### Phase G: Unreal Premium Lane

Status: Hold

目的は、Web/Electronで確定した体験を、必要な部分だけUnrealの3D表現へ持ち込むことである。

再開条件:

- Web/Electron版の保存、復習、配布が安定している。
- 3D化する価値が「豪華だから」ではなく、体験上の必要として説明できる。
- Map actor spawn のクラッシュ経路を完成証跡に使わない方針を守れる。

候補:

| Item | Priority | Done |
|---|---|---|
| 3D table value definition | P2 | 何を3D化するかが1ページで説明できる |
| Web feature parity checklist | P2 | Web版の何をUEへ移植するか決まる |
| Native fallback HUD再評価 | P3 | 既存UE成果をどこまで使うか判断する |
| 3D premium prototype | P3 | 1つの具体的演出だけを検証する |

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
| Visual gate | UI、CSS、HUD asset、layout変更時 | `scripts/audit_web_ui_visual.cjs` |
| Workflow gate | 複数工程の実装/検証/文書更新時 | `.workflow/<slug>/final-report.md` |

## 6. リスク管理

| Risk | 影響 | 対策 |
|---|---|---|
| 履歴データ破損 | ユーザーの学習記録を失う | export/import、schema note、migration policy、削除確認 |
| UI過密 | ONOKO感より読みにくさが勝つ | visual audit、低解像度確認、右パネル肥大化の抑制 |
| Electron配布で保存場所が不明 | 実使用時にバックアップできない | READMEに保存/復元/バックアップ方針を明記 |
| 3D表現への早すぎる回帰 | MVP完成が遅れる | UnrealはHold、Web本線の完了条件を優先 |
| 小アルカナ追加の爆発 | asset数とQAが大幅増加 | Expansion Gateまで着手しない |

## 7. 現在の次アクション

次に進める順序は次の通り。

1. 履歴の単体削除と全削除を実装する。
2. import/export/localStorage schema note を作る。
3. キーボード操作とfocus表示の smoke を追加する。
4. Electron packaging方式を決め、Windowsローカルpackageを作る。
5. 履歴詳細/復習ビューの要件を切る。

## 8. 参照文書

- `PRODUCT.md`
- `DESIGN.md`
- `plan.md`
- `docs/design/DESIGN_KANBAN.md`
- `docs/implementation/IMPLEMENTATION_KANBAN.md`
- `docs/design/overall-design-kanban.md`
- `docs/implementation/WEB_MVP_PIVOT_2026-06-02.md`
- `docs/roadmap/ONOKO_ARCANA_RESEARCH_GRADE_ROADMAP_V2_2026-05-31.md`
- `docs/roadmap/ONOKO_ARCANA_UNREAL_RESEARCH_ROADMAP_2026-05-31.md`
