# ONOKO ARCANA V5 Major Arcana Visual QA

Date: 2026-06-01

## Summary

- Total assets: `23`
- Adopted: `23`
- Needs Regeneration: `0`
- Blocked: `0`

## Evidence Used

- `assets/generated/card-production-v5-full/reports/v5-alpha-audit.json`
- `assets/generated/card-production-v5-full/reports/v5-alpha-contact-sheet-major-00-21-back.png`
- `assets/generated/card-production-v5-full/reports/v5-character-crop-report-major-00-21.png`
- `assets/generated/reports/v5-full-alpha-qa-map-unreal-editor-back-size-fixed-2026-06-01.png`

## Gate Criteria

1. ONOKO face is not visibly low quality.
2. Hands are not obviously broken at review scale.
3. Tarot-specific motif is readable.
4. Empty panels do not contain pseudo text.
5. Frame width, blue/gold balance, and glow are consistent.
6. Front/back visible size matches in Unreal.
7. Runtime text panel areas remain usable.

## Results

| ID | Card | Status | Reason |
|---|---|---|---|
| `card-back` | Card Back | Adopted | Back/front alpha bbox was corrected to match Major 00; no current size mismatch remains. |
| `major-00-fool` | 00 The Fool / 愚者 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-01-magician` | 01 The Magician / 魔術師 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-02-high-priestess` | 02 The High Priestess / 女教皇 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-03-empress` | 03 The Empress / 女帝 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-04-emperor` | 04 The Emperor / 皇帝 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-05-hierophant` | 05 The Hierophant / 教皇 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-06-lovers` | 06 The Lovers / 恋人 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-07-chariot` | 07 The Chariot / 戦車 | Adopted | Regenerated after the first V5 Chariot read too close to a dual-beast Strength motif. The current version has a clear arcane vehicle, wheels, and reins of light. |
| `major-08-strength` | 08 Strength / 力 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-09-hermit` | 09 The Hermit / 隠者 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-10-wheel-of-fortune` | 10 Wheel of Fortune / 運命の輪 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-11-justice` | 11 Justice / 正義 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-12-hanged-man` | 12 The Hanged Man / 吊された男 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-13-death` | 13 Death / 死神 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-14-temperance` | 14 Temperance / 節制 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-15-devil` | 15 The Devil / 悪魔 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-16-tower` | 16 The Tower / 塔 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-17-star` | 17 The Star / 星 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-18-moon` | 18 The Moon / 月 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-19-sun` | 19 The Sun / 太陽 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-20-judgement` | 20 Judgement / 審判 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |
| `major-21-world` | 21 The World / 世界 | Adopted | No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass. |

## Next Action

No visual blockers remain. Promote V5 into an active candidate deck manifest.
