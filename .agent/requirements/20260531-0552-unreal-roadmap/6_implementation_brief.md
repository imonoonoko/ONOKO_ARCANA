# ONOKO ARCANA Unreal Roadmap Implementation Brief

## Existing Patterns
- `docs/design/overall-design-kanban.md`: design direction and kanban.
- `docs/design/card-front-production-v1.md`: card asset policy and generated card status.
- `data/major-arcana-cards.json`: current card dataset.
- `reports/onoko-arcana-major-arcana-gallery.html`: current visual gallery.
- `reports/onoko-arcana-major-arcana-visual-check-2026-05-31.md`: current QA notes.
- `prototype/onoko-arcana-table-v0.html`: draft interaction reference, not final architecture.

## Likely Touch Points
- `Unreal/ONOKO_ARCANA/`: proposed future Unreal project root.
- `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Cards/Textures/`: card front/back textures.
- `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Cards/Materials/`: card front/back materials.
- `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Data/`: DataTable/DataAsset equivalents of `major-arcana-cards.json`.
- `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/UI/`: UMG widgets and Common UI patterns.
- `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Maps/`: main table scene.
- `docs/roadmap/`: durable planning and research reports.

## Technical Assumptions
- Unreal Engine 5.7系 is the preferred target because the user asked for the latest Unreal Engine direction.
- Blueprint should drive early interaction and scene behavior.
- C++ should be introduced only for stable reusable systems, asset import helpers, save/export, or performance-sensitive logic.
- The first build should prioritize one-card reading before three-card reading.
- The existing PNG assets are sufficient for a vertical slice.

## Risks
- Unreal Engine is not yet confirmed installed under `C:\Program Files\Epic Games\UE_*`.
- The PC may feel heavy when Unreal, browser, and image tools run together.
- Card textures at `1024x1536px` are appropriate for quality, but texture settings and memory should be checked in Unreal.
- JSON-to-Unreal data conversion needs a consistent pipeline.
- If UI panels become too decorative, the app may lose learning usability.

## Test Plan
- Verify all referenced card image paths exist before import.
- Import a small subset first: back, 00, 01, 07 v2.
- Confirm card aspect ratio in mesh material matches `2:3`.
- Build a one-card table scene and visually inspect from desktop resolution.
- Draw cards repeatedly and confirm no missing image/data mismatch.
- Save one reading, restart, and verify recovery.
- Package a Windows development build only after the editor vertical slice works.

## Open Questions
- Whether to create the Unreal project as Blueprint-only or C++ starter.
- Whether the initial card data should be converted manually into DataTables or imported through an editor utility script.
- Whether the guide panel should remain 2D UMG or include a 3D/2D ONOKO guide early.

## Phase 0 Update - 2026-05-31

- Unreal Engine 5.7.4 was detected at `C:\Program Files\Epic Games\UE_5.7`.
- Created `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject` as a minimal Blueprint-first project with Common UI enabled and an empty C++ runtime module for UnrealBuildTool/project-file validation.
- Created the planned Content folder structure under `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/`.
- Staged four import samples under `Unreal/ONOKO_ARCANA/ImportStaging/Phase0_CardTextures/`.
- Created `Unreal/ONOKO_ARCANA/Docs/PHASE0_IMPORT_CHECKLIST.md`.
- Verified project files generation, editor target build, commandlet load, and `1024x1536` dimensions for all four staged sample textures.
- Imported the four Phase 0 sample textures into `/Game/ONOKOArcana/Cards/Textures` using `Scripts/import_phase0_textures.py`.
- Created and opened `/Game/ONOKOArcana/Maps/L_Phase0_CardPlane_Check` in Unreal Editor GUI, confirming visible 2:3 card planes.
- Rejected old back `card-back-b-production-v1.png` after visual inspection because the card body looked wrong from generation, not just from UE placement.
- Generated the new ONOKO ARCANA back source `assets/generated/card-backs/card-back-onoko-production-v2-source.png`.
- Created alpha-ready card textures, including `assets/generated/card-backs/card-back-onoko-production-v2-transparent.png` and front-card alpha variants under `assets/generated/card-fronts/ue-alpha/`.
- Imported the alpha-ready Phase 0 textures using `Scripts/import_phase0_alpha_textures.py`; all imported as `1024x1536`.
- Updated `Scripts/create_phase0_card_plane_scene.py` to use alpha textures and Masked materials with Texture Alpha connected to Opacity Mask.
- Updated the card-plane map rebuild flow to clear existing actors instead of deleting the loaded map asset, avoiding the UE access violation encountered during map replacement.
- Captured the corrected GUI screenshot at `assets/generated/reports/phase0-unreal-editor-alpha-fixed-2026-05-31.png`.
