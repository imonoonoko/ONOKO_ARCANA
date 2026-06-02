# UI Visual Audit Final Report

Completed: 2026-06-02 21:00 JST

## Evidence

Audit script:

```text
scripts/audit_web_ui_visual.cjs
```

Report:

```text
reports/ui-visual-audit-20260602-210323/report.json
```

Screenshots:

```text
reports/ui-visual-audit-20260602-210323/desktop-one-card.png
reports/ui-visual-audit-20260602-210323/desktop-seven-horseshoe.png
reports/ui-visual-audit-20260602-210323/desktop-celtic-cross.png
reports/ui-visual-audit-20260602-210323/desktop-relationship-line.png
reports/ui-visual-audit-20260602-210323/mobile-seven-horseshoe.png
reports/ui-visual-audit-20260602-210323/mobile-relationship-line.png
reports/ui-visual-audit-20260602-210323/compact-celtic-cross.png
```

The audit captured 13 rendered cases. Console errors: 0. Horizontal overflow: 0.

## Programmatic Findings

```text
P1 text-overflow: 24
P1 slot-label-card-overlap: 30
P1 slot-label-label-overlap: 7
P2 tiny-text: 124
P2 card-rendered-small: 41
P2 slot-label-other-card-overlap: 46
P3 card-card-overlap: 52
```

## Confirmed Issues

### P1: Card inscriptions are unreadable in dense spreads

Card labels/keywords become 6-7.5px in five-card, seven-card, Celtic cross, and relationship-line layouts. Mobile relationship-line and seven-horseshoe also produce actual inscription overflow.

Evidence:

- `desktop-celtic-cross.png`
- `mobile-seven-horseshoe.png`
- `mobile-relationship-line.png`

Cause:

- Dense layouts set card width as low as 64-118px.
- In-card text is forced to remain inside the card art's small label plates.

Recommendation:

- Keep in-card labels only for one-card and maybe three-card layouts.
- For dense layouts, show only a short card number/glyph on the card and move readable name/keywords to slot labels, hover/zoom, or inspector.

### P1: Slot labels overlap cards and other labels

Programmatic overlap detected:

- own-card overlap: 30
- label-label overlap: 7
- label-other-card overlap: 46

The most visible cases are seven-horseshoe and relationship-line, especially mobile.

Recommendation:

- Stop rotating the slot label with the card in dense layouts, or anchor labels to fixed board callouts.
- Use smaller numeric markers on cards and move long slot labels to a legend/progress rail.

### P1: Mobile dense spreads are too compressed

Mobile seven-horseshoe and relationship-line show small cards, crowded slot labels, and progress chips that require horizontal scanning. The layout technically avoids page-level horizontal overflow, but the play surface is visually too dense.

Recommendation:

- On mobile, switch dense spreads to a guided sequence/scroll list or zoomable board.
- Keep the board as a preview, not the primary reading surface, for 6+ card spreads.

### P2: Right inspector compact buttons visually collide with frames

`ガイド表示` and `書き出し` are image-framed buttons placed on section rows. In screenshots they look like they float on top of panel borders, and disabled states are too dim.

Recommendation:

- Move section actions into a small command row below the section title.
- Use clearer disabled styling with text contrast preserved.

### P2: Spread selector rows are readable but still visually crowded

The current rows are improved, but left mini diagrams and right number endcaps still consume too much horizontal space. Long Japanese descriptions wrap awkwardly on mobile.

Recommendation:

- Move the count into the mini diagram or remove the right endcap.
- Give text a wider column and reduce side ornaments for inactive rows.

### P2: Image quality problem is mostly display scale, not source resolution

Card sources report natural width around 1024px, so the assets are not low resolution. The perceived blur/readability loss comes from rendering detailed cards at 70-106px widths, then expecting labels/details to remain legible.

Recommendation:

- Add click/hover zoom or selected-card enlargement.
- Avoid putting essential reading text inside tiny rendered cards.

## Non-Issues

- One-card desktop, compact, and mobile had 0 programmatic issues.
- No console errors were detected.
- No page-level horizontal overflow was detected.
- The table background image loads and does not appear pixelated at tested sizes.

## Suggested Fix Order

1. Replace dense-spread in-card text with card number/glyph plus inspector/legend text.
2. Rework dense-spread slot labels into fixed callouts or a separate legend.
3. Add mobile-specific sequence mode for six or more cards.
4. Clean up right inspector section buttons.
5. Reduce remaining spread-selector ornament pressure.
