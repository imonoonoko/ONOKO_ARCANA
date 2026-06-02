# UI Audit Fix Requirements

## Goal

Improve readability, overlap behavior, and perceived image quality of the current ONOKO ARCANA play screen.

## Acceptance Criteria

- One-card remains rich and uses the card art's label plates.
- Three-card remains readable without external zoom.
- Five-card, seven-card, Celtic cross, and relationship-line no longer show full keyword text inside tiny cards.
- Dense spread board labels do not visually collide with cards as large plaques.
- Mobile dense spread boards are not the only readable source of information.
- Right-side guide/export buttons are visually separated from section frames.
- The visual audit script and smoke tests run after implementation.
- All visual audit severities, including P3 card-card-overlap, are zero for the audited desktop, compact, and mobile cases.

## Non-Goals

- Do not change tarot card data.
- Do not add minor arcana.
- Do not redesign generated card art.
- Do not revisit Unreal.
