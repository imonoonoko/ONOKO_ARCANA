# UE Card Transparency Regeneration Requirements

## Goal

Regenerate ONOKO ARCANA card assets for Unreal Engine without background leakage, card-width mismatch, or character damage.

## Scope

- Major Arcana 22 front cards.
- One shared card back.
- UE-ready PNG outputs with fixed card silhouette.
- Alpha QA before Unreal import.
- Character fidelity QA for face, hands, skin, and costume detail.

## Non-Goals

- Do not generate Minor Arcana until the Major Arcana pipeline is stable.
- Do not rely on Unreal materials to hide image defects.
- Do not accept card images that only look correct on a white or black background.

## Acceptance Criteria

- Every UE-ready PNG is `1024x1536`.
- Every UE-ready PNG has binary alpha only: `0` or `255`.
- Every UE-ready PNG has alpha bbox `(54, 32, 970, 1514)`.
- Visible chroma-key magenta pixels are `0`.
- ONOKO skin, hands, face, and clothing are not damaged by alpha cleanup.
- ONOKO character detail is checked at actual crop size, not only in a contact sheet.
- Card names, numbers, and keywords are not baked into the image.
- UE Alpha QA map shows no rectangular background leakage.

## Risks

- Full-card generation can reduce ONOKO character fidelity because the character occupies only part of the frame.
- A separated frame + character/scene composition pipeline may be required for production quality.
- Chroma-key cleanup can destroy character pixels if it operates globally.
- UE card shadows can be mistaken for alpha leakage unless checked in a shadow-disabled QA map.
