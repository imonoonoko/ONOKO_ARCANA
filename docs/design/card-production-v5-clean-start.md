# ONOKO ARCANA Card Production V5 Clean Start

Date: 2026-06-01

## Decision

V4の旧カード再合成ルートは停止する。

理由:

- 旧カード画像にはフレーム、中央絵、装飾が一体で焼き込まれている。
- 中央絵だけを切り出して新フレームへ貼ると、旧フレーム要素が混入しやすい。
- UE側で拡大確認すると、イラストが横長に見え、フレームの下に潜って見える。
- この問題は透過処理ではなく、素材構造の問題なので、合成調整を続けるより新規生成の方が速い。

## V5 Rule

1枚のカード表面を、最初から完成カードとして生成する。

- Canvas: `1024x1536`
- Aspect: `2:3`
- Background outside the card: flat chroma key green
- Final UE texture: PNG with alpha after local chroma-key removal
- No readable text in the image
- Empty top nameplate and bottom description plate are allowed
- The central illustration must stay inside the inner artwork area
- The illustration must not slide under side rails, top nameplate, bottom plate, or corner ornaments

## Golden Sample

Generated source:

- `assets/generated/card-production-v5-clean-start/major-01-magician-onoko-v5-clean-source.png`

Alpha output:

- `assets/generated/card-production-v5-clean-start/major-01-magician-onoko-v5-clean-alpha.png`

Checker preview:

- `assets/generated/card-production-v5-clean-start/major-01-magician-v5-clean-checker-preview.png`

Unreal staging copy:

- `Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V5/major-01-magician-onoko-v5-clean-alpha.png`

## Alpha QA

- Size: `1024x1536`
- Alpha bbox: `(103, 35, 921, 1504)`
- Alpha extrema: `0..255`
- Visible green pixels: `0`
- Visible strong key pixels: `0`

## Aspect Decision

2026-06-01 decision:

- The V5 golden sample's visibly slender card silhouette is acceptable.
- This taller visible silhouette gives the card a stronger tarot-card feel.
- Do not force the V5 sample to the older wider bbox just to match V3/V4 debug geometry.
- Unreal validation should use the original V5 alpha output, not the normalized experiment.

Rejected experiment:

- `assets/generated/card-production-v5-clean-start/major-01-magician-onoko-v5-clean-alpha-normalized.png`
- Reason: technically matches the older wider bbox, but the user prefers the taller V5 silhouette.

## Prompt Baseline

Use a new full-card generation prompt per card. Do not reuse old full-card concepts as central art crops.

Core constraints:

- full card object, centered
- no cropped card edges
- flat `#00ff00` background outside the card only
- no shadow or floor plane
- no text, letters, numbers, watermark, or logo
- no wide horizontal distortion
- frame and character art integrated cleanly
- central illustration not hidden under ornamental rails

## Next Gate

Before producing all 22 major arcana cards:

1. User visually approves the V5 golden sample.
2. Import one V5 card into Unreal.
3. Verify the card plane uses a real `2:3` canvas scale such as `x=1.4, y=2.1`, while preserving the V5 card's taller visible silhouette.
4. Confirm no chroma-key fringe appears on a checkerboard or dark table.
5. Only then generate the remaining 21 fronts and a matching back.

## Full Major Arcana Draft

2026-06-01 status:

- V5 clean-start generation was expanded to the card back plus all 22 major arcana fronts.
- These are draft candidates for visual review, not final locked production assets.
- The user approved the visibly taller/slender V5 tarot silhouette, so this batch keeps that shape instead of normalizing to the older wider V3/V4 bbox.

Generated asset roots:

- Raw chroma-key source PNGs: `assets/generated/card-production-v5-full/raw/`
- Alpha PNGs: `assets/generated/card-production-v5-full/alpha/`
- Unreal staging copies: `Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V5_Full/`
- Prompt manifest: `assets/generated/card-production-v5-full/prompts/v5-major-arcana-generation-manifest.json`

QA artifacts:

- Alpha audit JSON: `assets/generated/card-production-v5-full/reports/v5-alpha-audit.json`
- Contact sheet: `assets/generated/card-production-v5-full/reports/v5-alpha-contact-sheet-major-00-21-back.png`
- Character crop QA: `assets/generated/card-production-v5-full/reports/v5-character-crop-report-major-00-21.png`
- HTML review report: `assets/generated/card-production-v5-full/reports/v5-full-major-review.html`

Alpha audit result:

- Count: `23`
- Canvas: `1024x1536`
- Border alpha: zero at the sampled outer border
- Visible green pixels: `0`
- Strong chroma-key leak pixels: `0`
- Result: `ok: true`

Remaining acceptance gates:

1. Human visual pass on face, hands, motif fit, and frame overlap at card-level scale.
2. Bulk import the 23 V5 alpha PNGs into Unreal.
3. Build a QA level that lays the full set on checkerboard and dark table surfaces.
4. Capture Unreal evidence before promoting V5 to the active card set.

## Card Back Size Correction

2026-06-01 correction:

- UE full-set QA showed the card back visible silhouette was shorter than the front cards.
- Root cause was not the Unreal plane scale. The source alpha bbox differed:
  - Back before correction: `(99, 38, 920, 1449)` / `821x1411`
  - Major 00 reference: `(103, 38, 921, 1504)` / `818x1466`
- The back alpha was fitted to the Major 00 bbox so the back/front visible card sizes match in Unreal.

Correction artifacts:

- Original backup: `assets/generated/card-production-v5-full/reports/card-back-onoko-v5-alpha-before-bbox-fit.png`
- Fit report: `assets/generated/card-production-v5-full/reports/card-back-bbox-fit-report.json`
- Updated alpha: `assets/generated/card-production-v5-full/alpha/card-back-onoko-v5-alpha.png`
- Updated Unreal staging copy: `Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V5_Full/card-back-onoko-v5-alpha.png`
- Updated UE evidence screenshot: `assets/generated/reports/v5-full-alpha-qa-map-unreal-editor-back-size-fixed-2026-06-01.png`

Current corrected bbox:

- Back after correction: `(103, 38, 921, 1504)` / `818x1466`
- Major 00 reference: `(103, 38, 921, 1504)` / `818x1466`

## Visual QA And Phase 1 Data Manifest

2026-06-01 status:

- V5 full-set visual QA was recorded for the card back plus all 22 major arcana fronts.
- The first V5 `07 Chariot` read too close to a dual-beast Strength motif, so it was regenerated.
- The regenerated `07 Chariot` uses a clear arcane vehicle, wheels, and reins of light.
- After regeneration, all 23 assets are classified as `Adopted`.
- V5 is now ready for Phase 1 data import as a candidate major-arcana deck.

QA and regeneration artifacts:

- Visual QA JSON: `assets/generated/card-production-v5-full/reports/v5-major-arcana-visual-qa.json`
- Visual QA markdown: `assets/generated/card-production-v5-full/reports/v5-major-arcana-visual-qa.md`
- 07 before/after comparison: `assets/generated/card-production-v5-full/reports/major-07-chariot-before-after-regeneration.png`
- 07 old alpha backup: `assets/generated/card-production-v5-full/reports/major-07-chariot-onoko-v5-alpha-before-regeneration.png`
- 07 old raw backup: `assets/generated/card-production-v5-full/reports/major-07-chariot-onoko-v5-source-before-regeneration.png`
- 07 bbox fit report: `assets/generated/card-production-v5-full/reports/major-07-chariot-regeneration-bbox-fit-report.json`

Candidate deck manifest:

- `data/major-arcana-v5-deck.json`

Manifest summary:

- Cards: `22`
- Assets including back: `23`
- Not adopted: `0`
- Ready for Phase 1 data import: `true`
