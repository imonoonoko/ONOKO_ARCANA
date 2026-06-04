# ONOKO ARCANA カード表面 v1

作成日: 2026-05-31

## 目的

ONOKO ARCANA の大アルカナ用カード表面の基準を作る。画像内にカード名や意味を焼き込まず、アプリ側で番号、カード名、正位置キーワード、逆位置キーワードを重ねる前提にする。

## 作成済み素材

- 表面テンプレート: `assets/generated/card-fronts/card-front-template-production-v1.png`
- 0番試作: `assets/generated/card-fronts/major-00-fool-onoko-concept-v1.png`
- 大アルカナ 01-21: `assets/generated/card-fronts/major-01-...-onoko-concept-v1.png` から `major-21-world-onoko-concept-v1.png`
- 比較再生成 v2: `major-07-chariot-onoko-concept-v2.png`, `major-12-hanged-man-onoko-concept-v2.png`, `major-15-devil-onoko-concept-v2.png`, `major-20-judgement-onoko-concept-v2.png`
- 裏面本命: `assets/generated/card-backs/card-back-b-production-v1.png`
- 表裏プレビュー: `assets/generated/card-production-preview-v1.png`
- 大アルカナ一覧コンタクトシート: `assets/generated/reports/major-arcana-contact-sheet-v1.png`
- v2採用後コンタクトシート: `assets/generated/reports/major-arcana-contact-sheet-v2.png`
- v1/v2比較シート: `assets/generated/reports/major-arcana-v2-regeneration-comparison.png`
- 大アルカナ定義: `data/major-arcana-cards.json`
- 大アルカナHTMLレポート: `reports/onoko-arcana-major-arcana-gallery.html`

すべて `1024x1536px`。実装での表示、縮小、カード拡大ビューに使える基準解像度として扱う。

## カードサイズ基準

ONOKO ARCANA のカード画像は、元の `major-00-fool-onoko-concept-v1.png` に合わせて `1024x1536px`、比率 `2:3` で統一する。

一般的なタロットカード風にさらに細長くする案は採用しない。ONOKO ARCANA では、キャラクター、UIパネル、学習用テキスト領域を見やすく残すため、現行の `2:3` を正式比率にする。

## 表面デザイン基準

- 黒アクリルのカード本体
- エレクトリックブルーの観測線と星光
- 鈍い金のフレーム
- 上部にカード番号・カード名を重ねるための空白パネル
- 下部に正位置、逆位置、学習メモを重ねるための空白パネル
- 中央にカード固有イラストを置く
- 猫、結晶、観測盤を共通モチーフとして残す

## 0番カードの方向性

0番は「愚者」をそのまま中世風にせず、ONOKO風の「最初の一歩」「観測を始める者」として表現する。

- 黒髪と青い差し色
- 青い瞳
- 黒、白、青の衣装
- 夜のサイバー都市
- 光る観測盤
- 足元の猫型ガイド
- 星へ続く青い道

## 大アルカナ v1 生成状況

大アルカナ 22 枚の v1 コンセプト生成は完了。各画像は `1024x1536px`、比率 `2:3` で統一した。

2026-05-31 の確認後、07、12、15、20 は比較再生成した v2 を採用側に切り替えた。v1画像は比較用として残す。

- 00 愚者: 作成済み
- 01 魔術師: 作成済み
- 02 女教皇: 作成済み
- 03 女帝: 作成済み
- 04 皇帝: 作成済み
- 05 教皇: 作成済み
- 06 恋人: 作成済み
- 07 戦車: v2採用
- 08 力: 作成済み
- 09 隠者: 作成済み
- 10 運命の輪: 作成済み
- 11 正義: 作成済み
- 12 吊された男: v2採用
- 13 死神: 作成済み
- 14 節制: 作成済み
- 15 悪魔: v2採用
- 16 塔: 作成済み
- 17 星: 作成済み
- 18 月: 作成済み
- 19 太陽: 作成済み
- 20 審判: v2採用
- 21 世界: 作成済み

## 次に確認すること

- 個別カードごとの疑似文字、手指、顔、重要モチーフの崩れを目視で採用判定する
- UI上で重ねるカード番号、カード名、正位置/逆位置キーワードの表示位置を決める
- 小アルカナへ進む前に、今回の大アルカナ v1 を「採用」「再生成」「修正候補」に分類する

## V4 Phase 0B 試作

2026-05-31に、Windows標準フォトで背景削除した `<local-downloads>\\Image.png` を基準maskにして、00/01/02/裏面のV4試作を作成した。

詳細: `docs/design/card-production-v4-phase0b.md`

## V5 Clean Start 方針

2026-06-01に、V4の旧カード再合成ルートを停止した。理由は、UE上で拡大すると、旧カードから切り出した中央絵に旧フレーム要素が混入し、イラストが横長に見え、新フレーム下へ潜って見えるため。

以降は、まず1枚の完成カードを新規生成し、クロマキー除去、alpha監査、UE import、2:3 Plane表示を通してから量産へ進む。

V5基準:

- `1024x1536`
- `2:3`
- カード外のみフラットなクロマキー背景
- 画像内テキストなし
- 中央イラストがフレームやパネルに被らない
- 1枚ごとに目視QAしてから採用

詳細: `docs/design/card-production-v5-clean-start.md`
