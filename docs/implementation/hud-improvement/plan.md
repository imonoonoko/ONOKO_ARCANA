# ONOKO ARCANA HUD Improvement Plan

Date: 2026-06-02

## 2026-06-02 Modular HUD Integration Update

The first modular generated-HUD pass is implemented in the Web/Electron app.

Handoff:

```text
docs/implementation/PHASE4_MODULAR_HUD_INTEGRATION.md
.agent/requirements/20260602-1330-modular-hud-integration/
assets/generated/hud-elements/20260602-astra-modular-kit/
```

The implementation uses the generated assets as modular decorative layers, not a fixed full-screen overlay. Current verified surfaces include spread mini diagrams, panel/plaque treatment, command/status accents, card slot focus rings, and progress pips.

Follow-up completed:

```text
assets/generated/hud-elements/20260602-astra-nine-slice-kit/
```

Dedicated 9-slice source frames were generated and integrated for stretchable panels, plaques, command buttons, spread rows, selected-card framing, and empty tarot slots.

Latest follow-up:

```text
docs/implementation/PHASE4_MODULAR_HUD_INTEGRATION.md
reports/onoko-arcana-web-app-celtic-20260602-201756.png
reports/onoko-arcana-electron-smoke-20260602-201918.png
```

The HUD is now image-backed rather than transparent-window-led. Real text remains native HTML.

## Goal

Improve the current Web/Electron HUD into a richer ONOKO-style 2D divination table while preserving the verified reading loop:

- choose a spread,
- enter a question,
- draw cards face down,
- reveal cards in order,
- write the user's own interpretation first,
- open guide text after the note exists,
- save and revisit readings.

The target is not a decorative skin. The HUD should feel like a precise cyber-oracle instrument where the table, cards, and reading state are always clearer than the ornament.

## Reference Images Reviewed

### Current Electron HUD

Path:

```text
reports/onoko-arcana-electron-smoke-20260602-051246.png
```

Takeaways:

- Strong functional structure: left setup, center table, right selected card/history.
- Cards are readable and all six spreads already work.
- The UI still reads like a dark productivity app more than a bespoke ONOKO oracle device.
- Bottom progress bar is useful but visually weaker than the generated command dock concepts.
- Panels are consistent, but the edge treatment is too plain compared with the card art.

### Generated HUD Overlay

Path:

```text
assets/generated/hud/20260602-onoko-hud-overlay-v1/onoko-hud-overlay-v1-source-chroma.png
```

Takeaways:

- Gold/black ornamental side frames and bottom rail fit the ONOKO card frame language.
- Blue gem accents are useful for active/reveal states.
- The asset is too literal to use as the only HUD structure. It should inform CSS/vector ornament and panel edge treatments.
- The side frames should become lightweight decorative frame layers behind code-native controls.

### UE Frame-Aligned HUD Screenshot

Path:

```text
reports/onoko-arcana-hud-frame-aligned-printwindow-20260602-041640.png
```

Takeaways:

- Strong ONOKO identity through the framed left/right HUD columns and bottom rail.
- Problems to avoid: text appears squeezed into ornamental frames, controls become small, and the visual hierarchy competes with the cards.
- Useful direction: ornate frame layer plus functional inner panel.

### ONOKO Strong One-Card Concept

Path:

```text
assets/generated/reports/20260602-onoko-strong-play-screen-concepts/onoko-strong-01-oracle-portrait-table.png
```

Takeaways:

- Strongest "ONOKO presence" reference: portrait, table, guide, history, and command dock feel like one product.
- The bottom command dock with large icon commands is a clear target.
- The table surface has better material richness than the current CSS table.
- Character portrait can be considered later, but should not enter the HUD until the reading loop remains uncluttered.

### Future Celtic Cross Concept

Path:

```text
assets/generated/reports/20260602-future-multi-spread-concepts/future-02-celtic-cross-table.png
```

Takeaways:

- The spread table is visually richer because the table surface carries rings, props, glow, and card labels.
- Left panel can show spread progress as a sequence, not just a spread selector.
- Right panel should distinguish unopened card guide, selected card meaning, and reading note.
- Bottom command dock should stay available for repeated actions.

### Spread Selection Concept

Path:

```text
assets/generated/reports/20260602-spread-system-assets/spread-system-01-selector-screen.png
```

Takeaways:

- Spread selection benefits from small layout diagrams and a "selected spread" summary.
- The current list is compact but visually flat. Add mini spread diagrams before adding more text.
- The large central table preview is useful, but in the app the first screen must still be the playable table, not a separate selection page.

## Design Direction

Use a layered HUD model:

1. **Functional layer**: code-native controls, inputs, card state, note, guide, history.
2. **Instrument layer**: panel borders, dividers, badges, progress dock, command dock, active states.
3. **Ornament layer**: gold corner caps, blue gem highlights, subtle circular table markings, frame silhouettes.

Rules:

- Keep cards and table as the visual priority.
- Use ornament at edges and state anchors, not behind text-heavy areas.
- Keep Japanese text high contrast and compact.
- Use blue for active/reveal/selected states.
- Use gold for frame, labels, and important reading state.
- Keep controls familiar. Do not turn standard form controls into hard-to-read fantasy widgets.

## HUD Problems To Fix

### P1. Brand Presence

Current brand block is serviceable but small. It lacks the generated concept's title plaque and ONOKO frame language.

Planned fix:

- Replace plain brand header with a compact title plaque style.
- Add subtle gold corner/line ornament to side panels.
- Keep app title readable at 18-20px.

### P2. Spread Selector

Current selector is usable, but all spreads look similar and require reading text.

Planned fix:

- Add code-native mini layout diagrams for each spread.
- Keep the count badge.
- Emphasize selected spread with blue edge light and gold label.
- Avoid a separate spread selection page for now.

### P3. Central Table

Current table is readable but visually flat compared with references.

Planned fix:

- Add richer table rings and faint etched marks using CSS pseudo-elements.
- Add a subtle radial blue "observation light" under selected/revealed cards.
- Improve card slot labels so they feel attached to the table, not floating UI tags.
- Keep high-card-count spreads readable.

### P4. Command Dock

Current top command group is functional but the references strongly favor a bottom command dock.

Planned fix:

- Convert bottom progress area into a two-tier dock:
  - reveal progress chips,
  - primary command buttons with icon-like glyphs and labels.
- Keep topbar for title and spread description only.
- Commands: Draw, Reveal Next, Save, Reset. Optional future: Guide, Export.

### P5. Right Inspector

Current inspector works but visually stacks equally weighted sections.

Planned fix:

- Make selected card the anchor section.
- Move note and guide into a clearer sequence:
  - selected card,
  - reader note,
  - guide locked/unlocked,
  - history.
- Strengthen "guide locked until note exists" as an intentional state, not just a disabled button.

### P6. History

Current history is usable after the scroll fix. It still lacks a reading-review feel.

Planned fix:

- Add compact card/count/status row per history item.
- Keep summary wrapping and no horizontal scroll.
- Add restored state styling when a history item is loaded.

## Implementation Phases

### Phase 1: HUD Token And Frame System

Files:

```text
web-app/src/styles.css
web-app/index.html
```

Work:

- Add HUD tokens for frame gold, inner line, active glow, table ring, command dock.
- Add reusable classes:
  - `hud-frame`
  - `hud-plaque`
  - `hud-divider`
  - `command-dock`
  - `spread-mini`
  - `state-lock`
- Keep the current CSS palette, but refine panel edges.

Acceptance:

- No layout behavior changes yet.
- Existing web/electron smoke tests still pass.

### Phase 2: Spread Selector With Mini Diagrams

Files:

```text
web-app/src/app.js
web-app/src/styles.css
```

Work:

- Render a mini diagram from each spread's slot coordinates.
- Add the diagram to every spread choice.
- Keep spread count and description.

Acceptance:

- All six spread choices remain visible.
- Selector remains usable at 390px width.
- `relationship_line` and `celtic_cross` are visually distinguishable before reading text.

### Phase 3: Bottom Command Dock

Files:

```text
web-app/index.html
web-app/src/app.js
web-app/src/styles.css
scripts/smoke_web_app.cjs
scripts/smoke_electron_app.cjs
```

Work:

- Move primary repeated commands into a stronger bottom command dock.
- Keep progress chips adjacent to the dock.
- Preserve keyboard/focus behavior.
- Use code-native symbols or short labels, not image-only buttons.

Acceptance:

- Draw/reveal/save/reset still work in browser and Electron.
- No command text overflows.
- Mobile layout stacks cleanly.

### Phase 4: Table Material And Selected State

Files:

```text
web-app/src/styles.css
web-app/src/app.js
```

Work:

- Add richer table rings, etched guide marks, selected-card glow, and revealed-card state.
- Make unrevealed cards look intentionally face down.
- Keep card labels readable.

Acceptance:

- Celtic cross 10-card table remains readable at desktop width.
- Relationship line 6-card table remains readable at mobile width.
- Screenshot comparison shows richer ONOKO mood without hiding cards.

### Phase 5: Inspector State Polish

Files:

```text
web-app/src/app.js
web-app/src/styles.css
```

Work:

- Add a "note first" locked-guide state.
- Distinguish selected card, reader note, guide, and history with stronger hierarchy.
- Add restored-reading state styling.

Acceptance:

- Guide remains disabled before note.
- Guide unlocks after note.
- Save and restore history still pass.

### Phase 6: Verification And Evidence

Commands:

```text
python scripts/check_web_app.py
cd web-app
npm run smoke:web
npm run smoke:electron
```

Screenshots to produce:

```text
reports/onoko-arcana-hud-improvement-desktop-*.png
reports/onoko-arcana-hud-improvement-mobile-*.png
reports/onoko-arcana-hud-improvement-electron-*.png
```

Acceptance:

- Console errors: 0.
- Desktop scroll width does not exceed viewport.
- Mobile scroll width does not exceed viewport.
- Electron launches and completes one relationship-line reading.
- Current reading loop is not regressed.

## Non-Goals

- Do not rework the deck data model.
- Do not add minor arcana in this HUD pass.
- Do not replace code-native controls with a full bitmap overlay.
- Do not add a character portrait until the table HUD is stable.
- Do not revisit Unreal HUD wiring in this phase.
- Do not create an installer in this phase.

## Risks

- Overusing the generated frame asset could make the HUD harder to read.
- Large ornamental frames can consume too much space on mobile.
- Celtic cross and relationship line have different density needs; one card size system may not satisfy both.
- More visual richness can reduce performance if implemented with heavy blur or large shadows.
- If bottom commands move too far from current DOM semantics, tests may need updates.

## Done Criteria

The HUD improvement pass is done when:

- current app behavior is preserved,
- all six spreads remain supported,
- the first screen still opens as the playable table,
- the HUD visibly inherits ONOKO gold/blue frame language from the references,
- the bottom command dock and side panels feel intentionally designed,
- note-before-guide behavior is visually clear,
- browser desktop, browser mobile, and Electron smoke tests pass,
- final screenshots are saved under `reports/`.
