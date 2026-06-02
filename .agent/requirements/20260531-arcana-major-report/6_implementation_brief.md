# ONOKO ARCANA 大アルカナ実装ブリーフ

## Implementation Steps

1. 既存の `major-00-fool-onoko-concept-v1.png` を基準に、01-21 のカード画像を生成する。
2. 生成画像を `assets/generated/card-fronts/major-XX-<slug>-onoko-concept-v1.png` に保存する。
3. 画像寸法を検査し、必要なら `1024x1536px` に正規化する。
4. `data/major-arcana-cards.json` を作成する。
5. 静的HTMLレポート `reports/onoko-arcana-major-arcana-gallery.html` を作成する。
6. HTML用のサムネイルまたは一覧プレビューを必要に応じて生成する。
7. docs に今回の完成状態と残るリスクを反映する。

## Visual Rules

- 画像比率は `2:3`。既存00番より縦長にしない。
- 黒、白、エレクトリックブルー、鈍い金を主軸にする。
- 猫、結晶、観測線、星、夜景、ホログラムをONOKO ARCANA共通要素にする。
- 上部と下部にはアプリ側テキストを重ねられる余白を残す。
- 画像内の文字は避ける。

## Report Rules

- レポートはブラウザで直接開ける単体HTMLにする。
- 各カードに画像、番号、名前、正位置、逆位置、学習メモ観点を並べる。
- 00番から21番まで番号順に一覧する。
- 今回の生成方法、寸法検証、残リスクを冒頭に記載する。
