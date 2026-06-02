# ONOKO ARCANA Research-Grade Roadmap Implementation Brief

## Existing Patterns

- Unreal project: `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject`
- Phase 0 report: `docs/unreal/PHASE0_BASELINE_2026-05-31.md`
- Card transparency plan: `docs/design/ue-card-transparency-regeneration-plan-2026-05-31.md`
- Card data: `data/major-arcana-cards.json`
- Alpha preparation: `scripts/prepare_ue_card_png.py`
- Alpha audit: `scripts/audit_ue_card_alpha.py`

## Likely Touch Points

- `scripts/compose_onoko_card_layers.py`
- `scripts/build_card_contact_sheet.py`
- `scripts/export_character_crop_report.py`
- `Unreal/ONOKO_ARCANA/Scripts/import_major_arcana_v4_textures.py`
- `Unreal/ONOKO_ARCANA/Scripts/create_card_alpha_qa_map.py`
- `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Cards/`
- `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Maps/`
- `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/UI/`

## Technical Assumptions

- UE 5.7.4 remains the active local engine.
- Blueprint-first is preferred until runtime logic becomes too large.
- Python scripts can continue handling editor automation and import.
- Major Arcana 22 cards are the first production deck.
- Minor Arcana is not implemented until the expansion gate.

## Risks

- The user may prefer immediate visual regeneration, but current evidence shows that pipeline quality must come first.
- Native transparent generation may reduce some background work but does not solve character detail or template consistency.
- UE viewport screenshots can mislead if captured through invalid D3D methods; normal screen capture or engine-level screenshots should be used.

## Test Plan

1. Run alpha audit on every UE-ready PNG.
2. Generate contact sheet and character crop report for visual QA.
3. Import only audited assets into UE.
4. Open Alpha QA Map and capture a screenshot.
5. Open Production Preview Map and evaluate table lighting/shadows separately.
6. For runtime phases, run one-card and three-card manual smoke tests.
7. For build phases, package Windows development build and run a save/restore smoke test.

## Next Implementation Step

Implement Phase 0B: V4 layered card pipeline prototype for 00, 01, 02, and card back. Do not regenerate all 22 cards until the four-asset prototype passes automated and visual QA.

