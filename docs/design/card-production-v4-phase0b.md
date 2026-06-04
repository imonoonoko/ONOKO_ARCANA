# ONOKO ARCANA Card Production V4 Phase 0B

作成日: 2026-05-31  
対象: 00 Fool / 01 Magician / 02 High Priestess / Card Back  
目的: Windows Photosで切り抜いた前面フレームを基準に、Unreal向けカード外形を統一する。

## 結論

ユーザーが `<local-downloads>\\Image.png` で作成したWindows標準フォトの背景削除結果を、V4前面カードのmask sourceとして採用した。

このPNGは `1024x1536`、RGBA、alpha bbox `(111, 77, 914, 1456)` で、外周borderは不透明ではなく透明化されている。V4 Phase 0Bでは、このbboxを前面・裏面共通の見かけ外形として使う。

## 入力

| Role | Path |
|---|---|
| Photos cutout source | `<local-downloads>\\Image.png` |
| Project copy | `assets/generated/card-production-v4/templates/card-frame-front-v4-photos-cutout-source.png` |
| 00 source | `assets/generated/card-fronts/major-00-fool-onoko-concept-v1.png` |
| 01 source | `assets/generated/card-fronts/major-01-magician-onoko-concept-v1.png` |
| 02 source | `assets/generated/card-fronts/major-02-high-priestess-onoko-concept-v1.png` |
| Back source | `assets/generated/card-backs/card-back-onoko-production-v3-alpha.png` |

## 生成物

| Role | Path |
|---|---|
| Transparent front frame | `assets/generated/card-production-v4/templates/card-frame-front-v4-transparent.png` |
| Alpha mask | `assets/generated/card-production-v4/templates/card-alpha-mask-photos-v4.png` |
| Central art crops | `assets/generated/card-production-v4/central-art-approved/*.png` |
| Composed cards | `assets/generated/card-production-v4/composed/*.png` |
| UE alpha cards | `assets/generated/card-production-v4/ue-alpha/*.png` |
| UE staging | `Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V4/*.png` |
| Contact sheet | `assets/generated/card-production-v4/reports/v4-alpha-contact-sheet-00-02-back.png` |
| Character crop report | `assets/generated/card-production-v4/reports/v4-character-crop-report-00-02.png` |
| Alpha audit | `assets/generated/card-production-v4/reports/v4-alpha-audit-photos-mask.json` |

## 監査結果

`scripts/audit_ue_card_alpha.py` を `--expected-bbox 111,77,914,1456` で実行し、4枚すべてOK。

- `1024x1536`: OK
- alpha bbox `(111,77,914,1456)`: OK
- alpha values `{0,255}`: OK
- visible magenta/key pixels: 0

## 実装メモ

追加したスクリプト:

- `scripts/extract_card_central_art.py`
- `scripts/compose_onoko_card_layers.py`
- `scripts/build_card_contact_sheet.py`
- `scripts/export_character_crop_report.py`

調整点:

- 前面はPhotos切り抜きのalphaを最終カードmaskとして使用。
- 中央絵は既存高品質カードから切り出し、フレーム下へ合成。
- 裏面は既存v3裏面をPhotos mask bboxへfitしてから同じalphaで切り抜き。
- alpha境界の色漏れを避けるため、最外周数pxは黒へ固定。

## 目視メモ

00/01/02は、v3のような人物破壊は見られない。これは新規一枚生成ではなく、既存の比較的高品質なv1カードから中央絵を切り出しているためである。

裏面は前面と同じ見かけ外形に揃った。次の検証はUnreal Engine内のAlpha QA Mapで行う。

