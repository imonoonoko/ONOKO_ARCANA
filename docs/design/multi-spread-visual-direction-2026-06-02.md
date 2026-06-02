# Multi-Spread Visual Direction

Updated: 2026-06-02

## Purpose

This note captures the visual direction for the future complete ONOKO ARCANA play screen after reviewing the one-card concepts and the multi-card spread concepts generated on 2026-06-02.

Phase 1 can remain a one-card vertical slice, but the UI and runtime concepts should avoid assuming that a reading has only one card. The finished product should support spreads where cards are laid out, selected, revealed in order, interpreted one by one, and then reviewed as a whole.

## Reference Sets

Generated concept folders:

- `assets/generated/reports/20260602-play-screen-concepts/`
- `assets/generated/reports/20260602-onoko-strong-play-screen-concepts/`
- `assets/generated/reports/20260602-future-multi-spread-concepts/`
- `assets/generated/reports/20260602-spread-system-assets/`

Most useful references:

- `onoko-strong-03-card-back-reveal-ready.png`: best Phase 1-compatible table and reveal-ready state.
- `onoko-strong-04-reading-review-magician.png`: best single-card review and guide density.
- `future-01-three-card-past-present-future.png`: best near-term multi-card progression from one-card to three-card spread.
- `future-02-celtic-cross-table.png`: best proof that the table can scale to large spreads.
- `future-03-sequential-reveal-flow.png`: best reveal-order and selected-card interaction model.
- `future-04-saved-spread-review.png`: best saved multi-card review and learning summary model.
- `spread-system-01-selector-screen.png`: best spread-selection and table-preview reference.
- `spread-system-02-layout-icon-sheet.png`: best compact spread icon and slot decal reference.
- `spread-system-03-three-card-in-progress.png`: best near-term in-reading multi-card HUD reference.

## Adopted Visual Ingredients

- ONOKO identity: black acrylic table, electric blue observation rings, restrained gold filigree, blue crystal motifs, and small cat emblems.
- Cards: 2:3 vertical ONOKO tarot cards with black-gold frames, blue constellation circuitry, cat medallions, and clear face-down backs.
- Table layout: card slots should be visible on the table before cards are revealed. Each slot has a position label and reveal order index.
- Selection model: the selected card gets a bright blue outline and drives the right-side guide panel.
- Reveal model: unrevealed cards stay face-down; guide content remains locked until the relevant card is revealed.
- Study mood: handwritten notes, cat doodles, and desk objects are useful as environmental context, especially in review and study modes.
- Assistant: ONOKO assistant works best as a small guide bubble or optional side panel. Avoid making the assistant the main gameplay surface.
- HUD structure: top bar for spread/deck/guide state, center for physical cards, left for question/progress/note, right for selected-card guide, bottom for actions.

## Excluded Or Risky Elements

- Do not adopt fake gem, coin, or currency counters from the generated images unless the product later gains a real progression system.
- Do not overcrowd Phase 1 with every future panel. The one-card slice should prove the same interaction grammar at smaller scale.
- Do not rely on generated Japanese microcopy. Keep final UI copy code-native and reviewed.
- Avoid large decorative side portraits in the default reading screen; they compete with the cards.
- Avoid layouts where card labels are only embedded inside art. Runtime labels must remain UI-driven.

## Implementation Shape To Preserve

The future spread screen should be data-driven:

- `SpreadDefinition`: spread id, display name, slot list, reveal order, and layout type.
- `SpreadSlot`: position key, display label, table transform, guide prompt, and order index.
- `ReadingCardState`: card id, orientation, revealed state, selected state, user note, and guide reveal state.
- `ReadingSession`: question, spread id, deck id, card states, selected slot, saved timestamp, and summary note.

UI components should map cleanly to this model:

- `SpreadTableView`: owns card actor/widget placement for all slots.
- `SpreadProgressPanel`: shows reveal order and completed/unrevealed states.
- `SelectedCardGuidePanel`: shows the selected card meaning, orientation, keywords, and learning hint.
- `ReadingNotePanel`: records user interpretation for the spread or selected card.
- `ActionDock`: shuffle, draw spread, reveal selected, reveal next, guide, save, reset.
- `ReadingReviewPanel`: shows saved readings, spread thumbnails, card-by-card details, timeline, and learning summary.

## Phase 1 Translation

For the current one-card phase, implement the same grammar with one slot:

- One `SpreadDefinition` equivalent: `one_card`.
- One center slot with label such as `現在` or `一枚引き`.
- One selected card by default.
- Guide locked while face-down, unlocked after reveal.
- The bottom dock should already read like the future flow: draw, reveal, note, guide, save, reset.

This keeps the current work small while preventing the interface from becoming a dead end when three-card and larger spreads are added.
