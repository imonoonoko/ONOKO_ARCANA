# Alternatives

## Option A: Full Multi-Card Runtime Now

Implement multi-card sessions, multiple card actors, per-slot notes, reveal-next, saved spread records, and review UI immediately.

Rejected for this pass. It would touch the card actor, table controller, save model, HUD, and map proof at once, making Phase 1 harder to validate.

## Option B: UI Mockups Only

Generate spread-selection imagery and leave code unchanged.

Rejected for this pass. The user asked to start implementation, and the current one-card model needs an early escape hatch before more UI is built around it.

## Option C: Spread Catalog And Selection Foundation

Add a data-driven spread registry, show active spread metadata in HUD, and save spread metadata with the existing one-card reading.

Chosen. This is small enough to verify with commandlet tests, while establishing the names, slot ordering, and UI surface required for multi-card runtime later.
