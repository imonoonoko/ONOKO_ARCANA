# ONOKO ARCANA Unreal Roadmap UI Prompt

## Screen: ONOKO Cyber Divination Table

### Purpose
ユーザーがPC上でタロットを引き、自分の解釈を書き、ONOKO風の補助解釈を見て、履歴として残せるメイン画面。

### Layout Diagram
```text
+--------------------------------------------------------------------------------+
| Reading mode tabs: One Card | Three Cards | Study                               |
+---------------------------+--------------------------------------+-------------+
| Session / History         | 3D ONOKO Divination Table            | Card Guide  |
| - current question        | - deck on left rear                  | - card name |
| - recent readings         | - active spread slots in center      | - keywords  |
| - saved notes             | - blue observation rings             | - meaning   |
|                           | - card flip and hover interaction    | - symbols   |
+---------------------------+--------------------------------------+-------------+
| User interpretation note field                         | Shuffle | Draw | Save |
+--------------------------------------------------------------------------------+
```

### Primary Components
- 3D Table Scene: dark wood, black acrylic mat, electric-blue observation rings, subtle crystals, cat icon accents.
- Deck Mesh: stacked cards using production back texture.
- Spread Slots: one-card and three-card positions, visible as thin blue holographic guides.
- Card Detail Panel: selected card name, upright/reversed state, keywords, study focus.
- User Note Panel: user's own interpretation first, guide interpretation second.
- History Rail: previous readings with date, spread type, question, drawn cards.
- Action Controls: shuffle, draw, flip/detail, reset, save.

### User Flow
1. User starts on the table.
2. User chooses one-card reading or three-card reading.
3. User enters a question if desired.
4. User shuffles and draws.
5. Card lands in slot and flips.
6. User writes their interpretation.
7. User opens guide interpretation.
8. User saves the reading.
9. User can review it from history or move to study mode.

### Design Tone
- Style: ONOKO's cyber divination desk, not generic fantasy tarot.
- Color: ink black, electric blue, white, ivory, muted gold. Avoid one-note purple or brown-only occult palettes.
- Density: rich but operational. The table is the primary surface; panels should feel like tools attached to the desk.
- Motion: short, readable, repeat-friendly. Card motion should feel physical, but not slow.

### Implementation Prompt
Build a Windows desktop Unreal Engine scene for ONOKO ARCANA. Use a 3D table as the primary first screen. Place a deck, spread slots, and holographic blue observation rings in the scene. Overlay UMG/Common UI panels for current question, user note, card guide, and history. Use the existing `1024x1536px` card PNGs as card front textures and `card-back-b-production-v1.png` as the deck back. Text must be rendered in UI, not baked into card art. The first vertical slice should support one-card draw, upright/reversed state, selected card detail, user note entry, and local save/load. Preserve the ONOKO identity from the kanban: black hair/blue eye influence, black-white-blue contrast, cat icon, crystal, observation lines, night room, hologram, quiet guide feeling.
