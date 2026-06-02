# ONOKO ARCANA Unreal Roadmap Alternatives

## Codebase Findings
- `docs/design/overall-design-kanban.md` に、ONOKOサイバー占い卓、学習導線、大アルカナ22枚、ONOKO ORACLEとの分離が記録済み。
- `docs/design/card-front-production-v1.md` に、カード画像 `1024x1536px`、比率 `2:3`、画像内テキスト非焼き込みが記録済み。
- `data/major-arcana-cards.json` に大アルカナ22枚のカード名、画像、正位置/逆位置キーワード、学習焦点が存在する。
- `reports/onoko-arcana-major-arcana-gallery.html` と `assets/generated/reports/major-arcana-contact-sheet-v2.png` に、v2採用後の大アルカナ一覧が存在する。
- `prototype/onoko-arcana-table-v0.html` は、操作フローを考えるためのHTML試作として扱えるが、最終技術基盤ではない。

## Options

### Option A: HTMLプロトタイプを先に完成させる
Effort: Medium  
Value: Medium

Summary:
現在のHTML試作を拡張し、1枚引き、3枚引き、メモ保存、カード一覧をブラウザで先に完成させる。

Benefits:
- 最短で操作感を確認できる。
- UI情報設計とカードデータ構造を軽く試せる。
- Unreal Engine導入前にユーザーフローの粗を見つけやすい。

Tradeoffs:
- 立体的なPCソフトとしての最終体験からは遠い。
- 3D卓、カード物理配置、カメラ、ライティングの検証が後回しになる。
- HTML実装に作り込みすぎると、Unreal側で再実装が必要になる。

### Option B: Unreal Engine縦断スライスを先に作る
Effort: Large  
Value: High

Summary:
Unreal Engineで、3D占い卓、カード1枚、シャッフル/ドロー、カード拡大表示、意味パネル、メモ保存までを最小構成で作る。

Benefits:
- 最終目標である立体的PCソフトに最も近い。
- カード画像をTexture2Dとして使う時の品質、サイズ、読み込み負荷を早期に検証できる。
- UIと3D演出の責任分界を早めに固定できる。

Tradeoffs:
- Unreal Engineのインストールとプロジェクト作成が必要。
- HTMLより検証サイクルが重い。
- Blueprint、UMG、アセット管理の初期設計を誤ると後から直しにくい。

### Option C: 追加カード素材を先に量産する
Effort: Large  
Value: Medium

Summary:
小アルカナ、追加背景、アイコン、テーブル素材などを先に大量生成する。

Benefits:
- 世界観素材は増える。
- 後でカード総数を増やす時の素材不足を減らせる。

Tradeoffs:
- 実装で必要な比率、UI余白、Texture制約、ファイル命名が固まる前に量産すると手戻りが大きい。
- 大アルカナ22枚だけでも縦断スライスは作れる。
- 追加生成の前に、現行素材がUnreal内でどう見えるか確認する方が合理的。

## Recommendation
Option Bを本線にする。理由は、ユーザーの現在の方向性が「立体的なPCソフト」「できれば最新Unreal Engine」であり、ONOKO ARCANAの価値はカード画像単体ではなく、3D占い卓、学習UI、カード操作、記録が一体になった体験にあるため。

ただし、Option AのHTML試作は捨てず、Unreal実装前の情報設計メモ、カードデータ確認、UI文言検討の補助資料として残す。
