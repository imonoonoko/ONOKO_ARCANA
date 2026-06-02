# ONOKO ARCANA UI Prompt

## Screen: 3D Divination Table

### Purpose

The user draws tarot cards, writes their interpretation, and reveals study guidance while staying in a rich ONOKO cyber-divination table scene.

### Layout Diagram

```text
+--------------------------------------------------------------------------------+
| [Top status: spread / date]                                      [Study][History]|
+--------------------------------------------------------------------------------+
|                                                                                |
|  [Left compact history rail]     [3D ONOKO divination table]     [Card detail]  |
|                                  [deck] [spread slots]                         |
|                                  [blue observation ring]                        |
|                                                                                |
+--------------------------------------------------------------------------------+
| [Question input] [User interpretation note] [Draw] [Reveal Guide] [Save] [Reset]|
+--------------------------------------------------------------------------------+
```

### Primary Components

- 3D Table: dark wood or black acrylic, electric-blue observation rings, muted gold trim.
- Deck Stack: card backs with fixed 2:3 aspect and matching visible width.
- Spread Slots: one-card and three-card modes, visible but not decorative-heavy.
- Card Detail Panel: card name, Japanese name, upright/reversed keywords, study focus.
- User Note: primary learning input, visible before guide reveal.
- Guide Reveal: optional assistance, not shown before user note by default.
- History Rail: recent readings, compact and readable.

### Design Tone

- Style: ONOKO cyber divination table, not a generic fantasy tarot UI.
- Color: ink black, electric blue, white/ivory text, muted gold accents.
- Density: tool-like and readable; avoid landing-page composition.
- Motion: short, restrained draw/flip effects.

### Implementation Prompt

Build the actual usable first screen of ONOKO ARCANA in Unreal Engine. The screen opens directly on a 3D divination table. Keep cards as code/data-driven actors and keep all text as UI overlays, not baked into card images. The table should feel like ONOKO's working divination desk: dark, precise, luminous, and practical. Use clear icon buttons for draw/reset/save/study/history, readable panels for card meaning and user notes, and a flow where the user writes first and reveals guidance second.

