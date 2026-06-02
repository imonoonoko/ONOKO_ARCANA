# ONOKO ARCANA Research-Grade Roadmap Alternatives

## Codebase Findings

- `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject` はUE 5.7プロジェクトで、CommonUIとEditor/Python系Pluginが有効。
- `data/major-arcana-cards.json` は大アルカナ22枚のみ。小アルカナ定義はない。
- `scripts/prepare_ue_card_png.py` は固定alpha方式に近いが、最終本番用には合成パイプラインがまだない。
- `scripts/audit_ue_card_alpha.py` はサイズ、bbox、binary alpha、key spillを検査できる。
- `docs/design/ue-card-transparency-regeneration-plan-2026-05-31.md` はv3失敗と修正方針を記録している。

## Options

### Option A: Continue One-Pass Full Card Regeneration

Effort: Medium  
Value: Low for production

Summary:
カード全体を一枚絵で再生成し、後処理で透明化してUEへ入れる。

Benefits:
- 生成が速い。
- 1カード単位では見た目の完成度を出しやすい。

Tradeoffs:
- ONOKO人物が小さくなり画質確認が難しい。
- 枠、空白パネル、外形、裏面幅が揺れる。
- NG時に全体を再生成する必要がある。

### Option B: Layered V4 Pipeline

Effort: Large  
Value: High

Summary:
固定フレーム、中央アート、固定alpha mask、合成、監査、UE QA Mapを分ける。

Benefits:
- 顔と手の品質をカード化前に確認できる。
- カード外形と裏面幅を固定できる。
- NG箇所だけ作り直せる。
- 小アルカナ展開時も再利用できる。

Tradeoffs:
- 最初に合成スクリプトとテンプレート設計が必要。
- 作業工程が増える。

### Option C: Use Native Transparent Image API First

Effort: Medium  
Value: Medium

Summary:
OpenAI Image APIのtransparent background機能を使い、最初から透明画像を得る。

Benefits:
- クロマキー除去の一部を省ける可能性がある。
- 背景処理が単純化する可能性がある。

Tradeoffs:
- Codex内蔵 `image_gen` ではパラメータ制御ができない。
- APIキー、Organization Verification、モデル、コスト、出力一貫性を別途確認する必要がある。
- 透明背景が得られても、カード外形と人物品質は別問題として残る。

## Recommendation

Option Bを採用する。Option Cは、V4 pipeline内の生成手段候補として検証してよいが、ロードマップの中核にはしない。透過だけを改善しても、人物品質と外形揺れが解決しないためである。

