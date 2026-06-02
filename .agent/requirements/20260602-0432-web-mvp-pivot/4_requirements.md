# Requirements

## Functional Requirements

FR-01: The user can select from all spreads currently defined in `data/spread-definitions-v1.json`.

FR-02: The user can enter a question before drawing.

FR-03: Drawing a spread assigns unique major arcana cards to all spread slots.

FR-04: Cards start unrevealed and use the ONOKO card back.

FR-05: The user can reveal the next unrevealed card in spread order.

FR-06: The user can click any revealed card to inspect it.

FR-07: The selected-card panel shows card name, number, upright/reversed state, keywords, study focus, and slot guidance.

FR-08: The user can write a memo for the selected slot.

FR-09: The user can save the current reading after at least one card is revealed.

FR-10: Saved readings appear in a local history list.

FR-11: The user can reset the table without deleting history.

FR-12: The guide is unavailable until the selected slot has the user's own note.

FR-13: The user can export saved readings as JSON.

## Non-Functional Requirements

NFR-01: The prototype opens directly as an HTML file.

NFR-02: Card art remains readable on a dark ONOKO-style table.

NFR-03: Controls must be compact enough for repeated use, not a landing page.

NFR-04: Layout must work at desktop widths and degrade acceptably on narrow screens.

NFR-05: Missing image paths should be catchable by a lightweight verification script.

## Acceptance Criteria

AC-01: Opening the prototype displays a usable tarot table, left controls, right inspector/history, and card deck visuals.

AC-02: Selecting the Celtic cross spread and drawing produces ten slots.

AC-03: Pressing reveal repeatedly flips cards in order and updates the selected-card panel.

AC-04: Notes can be entered for a selected revealed card.

AC-05: Saving a reading adds a history entry without clearing the table.

AC-06: A screenshot is saved under `reports/`.

AC-07: A local verification script passes for required app paths, referenced card assets, spread ids, Electron shell, and required UI ids.

AC-08: Relationship line can be selected, drawn, revealed, guided, and displayed on mobile without horizontal overflow.

## Risks And Open Questions

- Electron versus Tauri should remain undecided until the Web loop is stable.
- The static prototype stores history in browser `localStorage`; production desktop storage needs a migration plan.
- All-spread support currently uses major arcana only. Minor arcana changes deck size, balance, and UI density.
- If 3D table presence is still desired, it should be evaluated after the 2D reading loop is usable.
