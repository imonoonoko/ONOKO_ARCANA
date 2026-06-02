# ONOKO ARCANA Phase 0 Import Checklist

Date: 2026-05-31  
Engine: Unreal Engine 5.7.4 at `C:\Program Files\Epic Games\UE_5.7`  
Project: `Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject`

## Goal

Confirm that the current ONOKO ARCANA card assets can become Unreal Texture2D assets without breaking the fixed `2:3` card format, losing readability, or showing non-transparent rectangular backgrounds.

## Phase 0 Sample Textures

Use these four alpha-ready staged PNGs as the current Phase 0 baseline:

- `ImportStaging/Phase0_CardTexturesAlpha/card-back-onoko-production-v2-transparent.png`
- `ImportStaging/Phase0_CardTexturesAlpha/major-00-fool-onoko-concept-v1-alpha.png`
- `ImportStaging/Phase0_CardTexturesAlpha/major-01-magician-onoko-concept-v1-alpha.png`
- `ImportStaging/Phase0_CardTexturesAlpha/major-07-chariot-onoko-concept-v2-alpha.png`

The old `ImportStaging/Phase0_CardTextures/card-back-b-production-v1.png` batch is retained only as early evidence. The old back design is deprecated because the card body looked wrong from generation, not just from UE scaling.

Target Unreal folder:

```text
/Game/ONOKOArcana/Cards/Textures
```

## Import Settings To Check

- Texture Group: UI or 2D Pixels while testing readability; revise after table-camera tests.
- Compression: preserve detail enough for card inspection.
- Mipmaps: check both table view and detail view before disabling globally.
- sRGB: enabled for normal color card textures.
- Dimensions: confirm `1024x1536`.
- Alpha: card outside area should be transparent in source PNG.
- Material: connect Texture RGB to Base Color and Texture Alpha to Opacity Mask.
- Blend Mode: Masked for the current card-plane check.

## Editor Smoke Test

1. Open `ONOKO_ARCANA.uproject`.
2. Confirm the editor starts without missing plugin or module errors.
3. Import the four alpha staged textures into `/Game/ONOKOArcana/Cards/Textures`.
4. Create a simple card plane with `2:3` proportions.
5. Apply the card back and one front texture.
6. View from a table-like camera distance and a detail distance.
7. Save a screenshot under `assets/generated/reports/` for visual evidence.

## Pass Criteria

- The project opens in Unreal Engine 5.7.4.
- All four sample textures import.
- The card plane keeps `2:3` proportions.
- Card art remains readable enough for table view and detail view.
- The card back uses the ONOKO production v2 design, not `card-back-b-production-v1`.
- The card outside area does not show a black rectangular background.
- No card name, number, or keyword is baked into the texture.

## Current Blockers

- None for project scaffolding.
- None for alpha texture import and current viewport screenshot.

## Verified Before GUI Import

- Unreal Engine 5.7.4 detected.
- Project files generated successfully.
- `ONOKO_ARCANAEditor Win64 Development` built successfully.
- Commandlet project load completed with exit code 0.
- All four staged PNG files exist and are `1024x1536`.
- Automated Python Texture2D import completed successfully.
- Imported result file: `ImportStaging/Phase0_CardTextures/phase0-import-result.json`.
- Imported `.uasset` files exist under `Content/ONOKOArcana/Cards/Textures/`.
- Phase 0 card plane map was created at `/Game/ONOKOArcana/Maps/L_Phase0_CardPlane_Check`.
- Unreal Editor GUI opened the Phase 0 map and displayed the four 2:3 card planes.
- Screenshot: `assets/generated/reports/phase0-unreal-editor-visible-2026-05-31.png`.
- Old back `card-back-b-production-v1.png` was rejected after visual inspection.
- New back source `assets/generated/card-backs/card-back-onoko-production-v2-source.png` and transparent back `assets/generated/card-backs/card-back-onoko-production-v2-transparent.png` were created.
- Alpha texture import completed successfully.
- Alpha imported result file: `ImportStaging/Phase0_CardTexturesAlpha/phase0-alpha-import-result.json`.
- Current Phase 0 card materials use Masked blend with Texture Alpha connected to Opacity Mask.
- Updated screenshot: `assets/generated/reports/phase0-unreal-editor-alpha-fixed-2026-05-31.png`.

## Automated Import

The original non-alpha textures can be imported without opening the GUI by running:

```powershell
& "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" `
  "C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject" `
  -ExecutePythonScript="C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\Scripts\import_phase0_textures.py" `
  -Unattended -NullRHI -NoSound -NoSplash -NoP4 -stdout -FullStdOutLogOutput
```

The current alpha-ready Phase 0 textures can be imported without opening the GUI by running:

```powershell
& "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" `
  "C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject" `
  -ExecutePythonScript="C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\Scripts\import_phase0_alpha_textures.py" `
  -Unattended -NullRHI -NoSound -NoSplash -NoP4 -stdout -FullStdOutLogOutput
```

The current card-plane check map can be rebuilt by running:

```powershell
& "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" `
  "C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject" `
  -ExecutePythonScript="C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\Scripts\create_phase0_card_plane_scene.py" `
  -Unattended -NullRHI -NoSound -NoSplash -NoP4 -stdout -FullStdOutLogOutput
```
