# Requirements

## Functional Requirements

- When a three-card spread is active, the HUD shows the currently selected position.
- Past / Present / Future controls are visible in the native fallback HUD.
- Selecting a slot updates selected card title, orientation, keywords, guide eligibility, and user note target.
- Revealed state and saved spread state remain unchanged by selection.
- One-card mode continues to work.

## Acceptance Criteria

- Game and Editor targets build.
- Existing Phase 4 runtime checks remain OK.
- Phase 1 HUD reflection result remains OK.
- New or updated play-surface check confirms the slot HUD surface exists.
- A screenshot shows the updated HUD with slot controls and three visible cards.
