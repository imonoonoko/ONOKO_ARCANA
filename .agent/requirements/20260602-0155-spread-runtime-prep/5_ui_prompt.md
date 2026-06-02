# UI Prompt Notes

The visual source of truth for Phase 4 remains:

- `assets/generated/reports/20260602-spread-system-assets/spread-system-03-three-card-in-progress.png`
- `assets/generated/reports/20260602-future-multi-spread-concepts/future-01-three-card-past-present-future.png`
- `assets/generated/reports/20260602-future-multi-spread-concepts/future-03-sequential-reveal-flow.png`

## UI Contract For First Executable Multi-Card Slice

- Top/left display shows active spread: `過去・現在・未来`.
- Center table shows three slots: past, present, future.
- Each slot has a reveal order marker.
- One selected slot drives the right guide panel.
- Unrevealed slots show the card back.
- Revealed slots show front texture and orientation.
- Bottom action dock supports draw spread, reveal next, guide, save, reset.

## Native Fallback HUD Expectation

Before polished WBP work, the native fallback HUD may show this as text:

- Active spread display text.
- Slot list with reveal order.
- Selected slot label.
- Revealed count.
- Current selected card title/keywords/guide text.

The actual cards can be verified through runtime actors in a later visual proof.
