# Requirements

## Functional Requirements

- User can select `three_card_past_present_future`.
- Starting a reading creates a spread session with three positions.
- Drawing creates three unique cards and places three visible card actors on the table.
- Drawn cards initially show the card back.
- Repeated reveal reveals `past`, then `present`, then `future`.
- Revealed cards show their front texture and reversed rotation when applicable.
- Guide text is available only for a revealed selected card.
- Saving stores all three card states.
- Reset returns all spread cards to back-facing or hidden state.
- One-card flow continues to work.

## Acceptance Criteria

- Game and Editor targets build successfully.
- Existing Phase 4 runtime check remains OK.
- New table-controller commandlet result is `ok=true`.
- Preflight remains OK except the existing `.git` warning.
- A screenshot under `reports/` or `assets/generated/reports/` shows a running UE window with the table HUD and multiple cards, if visual capture succeeds.
