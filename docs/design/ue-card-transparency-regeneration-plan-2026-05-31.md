# ONOKO ARCANA UE Card Transparency Regeneration Plan

作成日: 2026-05-31  
対象: Unreal Engine向けONOKO ARCANAカード画像

## 結論

背景透過の失敗原因は、単純な「PNGにalphaがない」ではない。主因は次の3つである。

1. 生成画像のカード外周に、影、ハロー、背景色、疑似透明の縁が焼き込まれている。
2. 後処理がカードごとの外形を推定していたため、alpha bboxがカードごとにバラついた。
3. 初期v3の後処理は、画像全体からマゼンタ類似色を消していたため、ONOKOの肌や手まで透明穴として壊した。
4. UE確認画面ではalpha漏れとカードPlaneの影が混ざって見え、原因判定が難しくなっていた。

したがって、以後は「透明背景をお願いする」方式ではなく、生成段階から分離可能な背景にし、最終的に固定カード外形マスクでUE用PNGを作る。

## 調査結果

### 旧alpha素材の問題

`assets/generated/card-fronts/ue-alpha/*.png` の監査結果:

| Asset | alpha bbox | 判定 |
|---|---:|---|
| `major-00-fool-onoko-concept-v1-alpha.png` | `(46, 12, 976, 1530)` | NG |
| `major-01-magician-onoko-concept-v1-alpha.png` | `(44, 10, 978, 1534)` | NG |
| `major-07-chariot-onoko-concept-v2-alpha.png` | `(46, 10, 976, 1534)` | NG |

これらは二値alphaではあるが、外形がカードごとに違う。UE上で並べると、カード外側の残りや太さの差として見える。

### v3処理済み素材の状態

`scripts/prepare_ue_card_png.py` の修正版で処理したv3素材:

| Asset | alpha bbox | alpha | visible magenta | 判定 |
|---|---:|---|---:|---|
| `card-back-onoko-production-v3-alpha.png` | `(54, 32, 970, 1514)` | 0/255 only | 0 | OK |
| `major-00-fool-onoko-ue-v3-alpha.png` | `(54, 32, 970, 1514)` | 0/255 only | 0 | OK |
| `major-01-magician-onoko-ue-v3-alpha.png` | `(54, 32, 970, 1514)` | 0/255 only | 0 | OK |
| `major-02-high-priestess-onoko-ue-v3-alpha.png` | `(54, 32, 970, 1514)` | 0/255 only | 0 | OK |

監査結果:

- 旧監査: `assets/generated/reports/ue-card-alpha-audit-2026-05-31.json`
- 修正版監査: `assets/generated/reports/ue-card-alpha-audit-v3-connected-2026-05-31.json`

プレビュー: `assets/generated/card-fronts/ue-v3-reports/ue-v3-alpha-preview-current.png`

人物破壊の比較:

- 破壊確認: `assets/generated/card-fronts/ue-v3-reports/source-vs-alpha-character-damage-check.png`
- 修正版確認: `assets/generated/card-fronts/ue-v3-reports/ue-v3-character-crop-quality-check-fixed.png`

## 失敗した処理方式

失敗した方式:

```text
全画素について「マゼンタ背景に近い色」を透明化する
```

この方式はカード外周のマゼンタ残りを消せるが、ONOKOの肌、指、明るい衣装、白いハイライトも巻き込む。結果として、顔や手に白い粒状ノイズ、透明穴、欠けが出た。

採用する方式:

```text
生成画像の外周から背景に連結しているクロマキー領域だけを検出してカードbboxを取る
カード画像RGBは保持する
最終alphaは固定丸角マスクで作る
外形内に残る極端なマゼンタ縁だけ黒へ置換する
```

この方式では、肌や手の内部色を透明化しない。カード外形は全カード同一になり、UE上の太さ差も出にくい。

## 外部仕様メモ

- OpenAI Images APIは、GPT Image系で `background: transparent` を指定できる。ただし現在のCodex内蔵 `image_gen` では出力先や透明背景パラメータを直接制御できないため、API透明背景を使うならCLI/API経路へ切り替える必要がある。
- Unreal EngineのMasked MaterialはOpacity Maskを二値で扱う。半透明の中間値は「透ける」のではなく、Opacity Mask Clip Valueの閾値で描画/破棄に分かれる。

## 新しい生成仕様

### キャラクター品質の再計画

全カードを1枚絵として一括生成すると、ONOKOの人物部分がカード全体の一部に圧縮される。結果として、顔、手、肌、衣装のディテールが本番カードとして弱くなる。

以後の本命生成は次のどちらかに切り替える。

#### A案: 分離生成 + 合成

1. カードフレームを固定テンプレートとして作る。
2. ONOKO人物/カード固有シーンを、中央アート枠用に大きく生成する。
3. 人物/シーンを高解像度で確認してからカードテンプレートへ合成する。
4. 最後に固定alphaマスクを適用する。

メリット: 顔と手の品質を見てから採用できる。カード外形も固定しやすい。  
デメリット: 合成スクリプトとテンプレート設計が必要。

#### B案: 1枚生成だが人物を大きく指定

1. カード全体は従来通り1枚で生成する。
2. プロンプトで「ONOKO upper body / face large and sharp / hands clear」を強く指定する。
3. 生成後に人物部分の実寸cropを必ず確認する。

メリット: 作業が速い。  
デメリット: カードによって人物品質が揺れやすく、再生成回数が増える。

現時点の推奨はA案。UEアプリ用の長期素材としては、フレーム、人物/場面、UI空白パネルを分けたほうが品質管理しやすい。

### 生成プロンプト必須条件

全カード共通:

- Canvas: `1024x1536`, 2:3。
- 背景: 完全フラットなクロマキー `#ff00ff`。
- カード本体: 中央配置、四辺に十分なマゼンタ余白。
- 禁止: 外側ドロップシャドウ、外側グロー、白/灰色ハロー、床、壁、背景テクスチャ、疑似透明チェッカー。
- 禁止: 文字、数字、カード名、ラベル、ウォーターマーク。
- 表面: 上下の羊皮紙パネルは空白。
- 裏面: 表面カードと同じ外形幅。太らせない。

### ローカル後処理

生成直後の画像はそのままUEへ入れない。必ず次の処理を通す。

1. `assets/generated/card-fronts/ue-v3-source-chromakey/` へsourceをコピー。
2. `scripts/prepare_ue_card_png.py` で以下を実行。
   - 画像外周から背景に連結しているクロマキー領域だけを検出。
   - 背景に連結していない人物内部の肌色や白ハイライトは消さない。
   - カード本体を固定矩形 `(54, 32, 970, 1514)` へフィット。
   - 固定丸角マスク `radius=52` を適用。
   - alphaは0/255のみ。
   - 可視マゼンタは0ピクセルにする。外形内のマゼンタ縁は透明化ではなく黒置換。
3. `scripts/audit_ue_card_alpha.py` で監査。
4. OKのみ `Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V3/` へ入れる。

## UE確認計画

### Alpha QA Map

本番卓とは別に、alphaだけを見るMapを作る。

- Unlitまたは影の影響が少ないMaterial。
- カードStaticMeshは `cast_shadow=False`。
- 背景はチェッカーまたは濃淡のある平面。
- カメラは正面寄り。
- このMapでは「外形漏れ」「太さ差」「マゼンタ残り」だけを判定する。

### Production Preview Map

Alpha QA合格後に、本番寄りのライティングで確認する。

- 影はここで初めて有効化。
- 影が矩形に見える場合は、Planeではなく丸角カードMeshへ移行する。
- 画像alpha問題と影問題を混同しない。

## 受け入れ条件

1. 全カードPNGが `1024x1536`。
2. alpha bboxが全カードで `(54, 32, 970, 1514)`。
3. alpha値は0または255のみ。
4. 可視状態のマゼンタ/クロマキー色が0ピクセル。
5. UE Alpha QA Mapでカード外側に矩形、白/灰色ハロー、背景色残りが見えない。
6. 裏面の見かけ幅が表面カードと一致する。
7. Production Preview Mapで影が必要以上に矩形化しない。矩形化する場合は画像ではなくMesh/Shadowの課題として扱う。

## 再生成手順

1. 既存の途中生成v3は、00/01/02/裏面だけ参考として残す。
2. 03以降を同じプロンプト仕様で生成する。
3. 各カードごとに即座に `prepare_ue_card_png.py` と `audit_ue_card_alpha.py` を通す。
4. 22枚+裏面の監査が全OKになるまでUE Importしない。
5. 全OK後にUE import manifestを作り、まとめてTexture2D化する。
6. Alpha QA Mapでスクリーンショットを取り、合格後にProduction Previewへ進む。

## 現時点の判断

大量生成を続ける前に、alpha QA pipelineを固定する。  
現状のv3処理済み4枚は監査上OKだが、UE上では影や表示条件の影響が混ざるため、専用のAlpha QA Mapを先に作る。
