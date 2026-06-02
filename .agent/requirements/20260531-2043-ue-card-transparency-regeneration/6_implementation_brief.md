# UE Card Transparency Regeneration Implementation Brief

## Current Evidence

- Failed old alpha audit: `assets/generated/reports/ue-card-alpha-audit-2026-05-31.json`
- Passing corrected v3 audit: `assets/generated/reports/ue-card-alpha-audit-v3-connected-2026-05-31.json`
- Character damage proof: `assets/generated/card-fronts/ue-v3-reports/source-vs-alpha-character-damage-check.png`
- Corrected character crop proof: `assets/generated/card-fronts/ue-v3-reports/ue-v3-character-crop-quality-check-fixed.png`
- Full plan: `docs/design/ue-card-transparency-regeneration-plan-2026-05-31.md`

## Scripts

- `scripts/prepare_ue_card_png.py`
  - Locates the card using connected chroma-key background.
  - Fits the card to fixed rect `(54, 32, 970, 1514)`.
  - Applies a fixed binary rounded alpha mask.
  - Converts visible magenta edge spill to black instead of punching holes.
- `scripts/audit_ue_card_alpha.py`
  - Verifies size, alpha bbox, alpha binaryness, and visible key-color residue.

## Next Steps

1. Build a UE Alpha QA map that disables card shadows.
2. Reimport only corrected v3 test cards: back, 00, 01, 02.
3. Confirm in UE that alpha leakage is gone.
4. Only then continue generating 03-21.
5. After 22+back pass audit, import all to Unreal in one manifest.

