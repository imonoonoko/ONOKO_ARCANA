# Discussion Log

## Roadmap Reset - 2026-05-31 22:45

### User Input
> では改めて論文レベルでロードマップ作成。`define-requirements`、`orchestrate-skills`、`image-first-frontend` を使う。

### Codex Proposal Or Discovery
既存Phase 0、透過再計画、カード生成失敗、UE 5.7.4検出、OpenAI/Unreal公式情報を読み直し、v1ロードマップを置き換えるのではなくv2として再計画する。

### Decisions
- Accepted: ロードマップは単なる工程表ではなく、証拠、失敗原因、仮説、受け入れ条件、品質ゲートを含む研究仕様にする。
- Accepted: 本番カードは一枚絵大量生成ではなく、固定テンプレート、中央アート、合成、固定alpha、監査のV4 pipelineを推奨する。
- Accepted: 大アルカナ22枚を初期正式スコープとし、小アルカナ56枚はExpansion Gate後に扱う。
- Rejected: 22枚や78枚を先に一括再生成する。
- Open: native transparent API経路を採用するかは、APIキー、モデル、検証可否を確認してから決める。

### Rationale
Phase 0の目視で透過漏れと裏面幅差が発覚し、その後のv3後処理でONOKO人物部が破壊された。大量生成より先に、生成段階と後処理段階の責務を分離する必要がある。

---

## Phase 0B Card Creation Start - 2026-05-31 23:00

### User Input
> ではカード作成をお願いします。`define-requirements` を使う。

### Codex Proposal Or Discovery
直前に作成した研究水準ロードマップv2のImmediate Work Ordersに従い、全22枚ではなく、まず00/01/02/裏面の4枚でV4 layered card pipeline prototypeを作る。

### Decisions
- Accepted: Phase 0Bの最小スコープは `00 Fool`, `01 Magician`, `02 High Priestess`, `Card back`。
- Accepted: 既存の大アルカナv1素材は品質基準の比較対象として使い、V4では枠、中央アート、alpha、レポートを分ける。
- Accepted: 生成結果はUnreal投入前にcontact sheet、character crop、alpha auditで止める。
- Rejected: この段階で22枚または78枚を一括生成する。

### Rationale
ユーザーが指摘した通り、v3のONOKO人物部は画質が悪く、透明化も漏れた。まず小さい4枚で作成手順そのものを固定しないと、量産時の手戻りが大きくなる。

---

## Phase 0B Prototype Result - 2026-05-31 23:20

### User Input
> Windows標準の フォト で背景綺麗に透過できたよ。`<local-downloads>\\Image.png`

### Codex Proposal Or Discovery
`Image.png` を実測したところ、`1024x1536`、RGBA、alpha bbox `(111,77,914,1456)`、外周border alpha 0であり、V4の前面mask sourceとして使えることを確認した。

### Decisions
- Accepted: `Image.png` を `assets/generated/card-production-v4/templates/card-frame-front-v4-photos-cutout-source.png` にコピーしてV4前面テンプレートの基準にする。
- Accepted: 00/01/02は既存高品質v1カードから中央絵を切り出し、Photos切り抜きフレームへ合成する。
- Accepted: 裏面はPhotos mask bboxへfitして、前面と同じ見かけ外形にする。
- Accepted: V4 prototype outputsを `assets/generated/card-production-v4/` と `Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V4/` に置く。

### Verification
- `scripts/audit_ue_card_alpha.py --expected-bbox 111,77,914,1456` で4枚すべてOK。
- Contact sheet: `assets/generated/card-production-v4/reports/v4-alpha-contact-sheet-00-02-back.png`
- Character crop report: `assets/generated/card-production-v4/reports/v4-character-crop-report-00-02.png`
- Alpha audit: `assets/generated/card-production-v4/reports/v4-alpha-audit-photos-mask.json`

### Rationale
ユーザー側でWindows Photosによる切り抜き品質が実証されたため、V4ではPhotos cutoutを外形基準として採用する。これにより、生成段階の疑似透明やクロマキー漏れに依存しない。

---

## Phase 0B V5 Pivot - 2026-06-01 00:40

### User Input
> もはや新規作成した方が速いかもしれない

### Codex Proposal Or Discovery
V4の旧カード再合成結果をUE上で拡大確認したところ、透過ではなく素材構造の問題が残った。中央絵切り出しに旧フレーム要素が混入し、カードPlane側でも横長に見え、中央絵が新フレームの下に潜って見えた。

### Decisions
- Accepted: V4の旧素材再合成ルートは停止する。
- Accepted: V5では、1枚の完成カードを最初から新規生成し、カード外だけをクロマキー背景にしてローカルalpha化する。
- Accepted: 22枚量産前に、V5 golden sampleを1枚だけUEへimportして、2:3 Plane、Masked Material、QA Mapで確認する。
- Rejected: 旧カード中央絵の切り出し矩形をさらに調整して量産へ進む。

### Verification
- V5 golden sample: `assets/generated/card-production-v5-clean-start/major-01-magician-onoko-v5-clean-alpha.png`
- Size: `1024x1536`
- Alpha bbox: `(103,35,921,1504)`
- Visible green pixels: `0`
- Visible strong key pixels: `0`

### Rationale
今回の問題はalpha漏れではなく、旧カードを素材として再利用する設計の限界である。量産前に、完成カードを新規生成するV5方式を1枚だけUEで通す方が手戻りが小さい。

---

## V5 Aspect Decision - 2026-06-01

### User Input
> 縦長で問題ありません。むしろそのサイズの方がタロットカード感があって良い

### Decisions
- Accepted: V5 golden sampleの細めで縦長な可視カード外形を採用する。
- Accepted: UE検証では `major-01-magician-onoko-v5-clean-alpha.png` を本命として使う。
- Rejected: 古いV3/V4 bboxへ合わせるために横幅を広げた normalized 版を本命にする。

### Rationale
V5の目的は既存デバッグbboxへの機械的な一致ではなく、ONOKO ARCANAとして見栄えの良いタロットカードを安定して作ることである。ユーザーは細めの可視外形を望んでいるため、量産基準もそれに合わせる。
