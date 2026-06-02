# Requirements

## Functional Requirements

FR-01: The user can continue to select all six spreads.

FR-02: The user can draw, reveal, inspect, write notes, unlock guide text, save, restore from history, reset, and export history as before.

FR-03: The HUD can display selected generated assets as decorative UI parts without requiring runtime image generation.

FR-04: The spread selector shows clearer visual state while still preserving text labels and descriptions.

FR-05: The card table shows stronger slot/focus treatment without covering the cards.

## Non-Functional Requirements

NFR-01: Generated HUD assets must be optional decoration around code-native text and controls.

NFR-02: The center playfield and cards must remain the primary visual focus.

NFR-03: Japanese labels and notes must remain rendered as real text.

NFR-04: Desktop and mobile layouts must not create horizontal overflow.

NFR-05: The static checker should fail if required modular HUD assets are missing.

## Acceptance Criteria

AC-01: The app loads without console errors.

AC-02: `python scripts/check_web_app.py` passes and verifies modular HUD asset files.

AC-03: `scripts/smoke_web_app.cjs` passes for desktop and mobile.

AC-04: `scripts/smoke_electron_app.cjs` passes.

AC-05: A screenshot under `reports/` shows the richer HUD treatment using modular assets.

AC-06: No labels, card names, notes, or guide content are baked into generated images.
