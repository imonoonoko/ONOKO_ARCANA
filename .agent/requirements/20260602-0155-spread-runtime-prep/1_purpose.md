# Purpose

Prepare the project for the next implementation step: actual multi-card spread readings.

Phase 3 made spreads selectable as metadata. Phase 4 should make at least the three-card past-present-future spread executable: draw multiple cards, place them in slots, select a slot, reveal cards in order, write notes, unlock guide text, save the reading, and review it later.

This prep pass freezes the contracts, fixtures, verification gates, and order of work so Phase 4 can start without reshaping the runtime halfway through.

## Success Criteria

- The next runtime contracts are documented.
- A machine-checkable spread-definition fixture exists.
- A dedicated prep checker validates required Phase 3 evidence and Phase 4 fixture invariants.
- The prep checker writes a JSON report under `reports/`.
- The existing Phase 1 preflight still passes.
