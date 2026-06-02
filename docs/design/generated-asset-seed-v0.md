# ONOKO ARCANA 生成素材シード v0

作成日: 2026-05-31

## 目的

`imagegen` で生成した ONOKO ARCANA 用の素材シード画像を元に、カード裏面、UI装飾、アイコン、占い卓、質感素材を段階的に切り出していく。

この版は最終素材ではなく、実装に使うビジュアル言語を固めるための初期素材集として扱う。

## 生成元

- 素材シード: `assets/source/onoko-arcana-asset-seed-sheet-v0.png`
- 切り出しプレビュー: `assets/generated/asset-crops-preview-v0.png`
- 参照デザイン: `assets/design/onoko-arcana-design-kanban-v1-onoko.png`

## 切り出し済み素材

### Card Fronts

- `assets/generated/card-fronts/card-front-template-production-v1.png`
- `assets/generated/card-fronts/major-00-fool-onoko-concept-v1.png`
- `assets/generated/card-fronts/major-01-magician-onoko-concept-v1.png` から `assets/generated/card-fronts/major-21-world-onoko-concept-v1.png`
- `assets/generated/card-fronts/major-07-chariot-onoko-concept-v2.png`
- `assets/generated/card-fronts/major-12-hanged-man-onoko-concept-v2.png`
- `assets/generated/card-fronts/major-15-devil-onoko-concept-v2.png`
- `assets/generated/card-fronts/major-20-judgement-onoko-concept-v2.png`
- `assets/generated/reports/major-arcana-contact-sheet-v1.png`
- `assets/generated/reports/major-arcana-contact-sheet-v2.png`
- `assets/generated/reports/major-arcana-v2-regeneration-comparison.png`
- `data/major-arcana-cards.json`
- `reports/onoko-arcana-major-arcana-gallery.html`

カード表面は最初から単体生成の `1024x1536px` を基準にする。文字は画像に焼き込まず、アプリ側で重ねる。カード比率は元の `major-00-fool-onoko-concept-v1.png` と同じ `2:3` で統一し、これ以上細長い比率にはしない。大アルカナ 22 枚の v1 生成は完了済み。確認後、07、12、15、20 は比較再生成した v2 を採用側に切り替えた。

### Card Backs

- `assets/generated/card-backs/card-back-a.png`
- `assets/generated/card-backs/card-back-b.png`
- `assets/generated/card-backs/card-back-c.png`
- `assets/generated/card-backs/card-back-b-production-v1.png`

シート切り出し版のカード裏面は約 `205x378px` で、方向性確認用として扱う。本番候補は単体生成した `card-back-b-production-v1.png`。`1024x1536px` で、中央の結晶、上下の猫、青い観測線が入り、ONOKOらしさと逆位置判定を邪魔しない上下対称性のバランスが良い。

### UI Sheets

- `assets/generated/ui/icons-sheet.png`
- `assets/generated/ui/frames-sheet.png`
- `assets/generated/ui/table-rings-sheet.png`
- `assets/generated/ui/textures-sheet.png`

## 次に素材化する単位

- 大アルカナ 22 枚を目視で採用、再生成、修正候補に分類する
- カード裏面の正式版 1 枚を `card-back-b-production-v1.png` 起点で調整する
- 猫、結晶、星、月、鍵、杯、剣、目、シャッフル、ドロー、リヴィールの個別アイコン
- 占い卓の円形リング
- 1枚引き用カードスロット
- 3枚引き用カードスロット
- 黒アクリル、青いホログラム、アイボリー紙、真鍮、深緑布のテクスチャ

## 生成プロンプト要点

- ONOKO ARCANA v1 カンバンを参照
- 黒、白、エレクトリックブルー、鈍い金を中心にする
- 猫、結晶、月、星、観測線、ホログラムを繰り返し使う
- 古典的な茶色のタロットではなく、ONOKO のサイバー占い卓に寄せる
- 実装素材化しやすいよう、文字を最小にして前面正対の構図にする
