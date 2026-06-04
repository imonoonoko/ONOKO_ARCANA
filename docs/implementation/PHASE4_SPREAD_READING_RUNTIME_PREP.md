# Phase 4 Spread Reading Runtime Prep

> Archive notice (2026-06-05): This UE runtime-prep note is historical evidence. The active v1.x lane is Web/Electron; do not use this document as current next work.

Updated: 2026-06-02

## Purpose

This note is the entry gate for implementing actual multi-card spread readings after Phase 3 spread selection.

Phase 3 made spreads selectable and commandlet-proven as metadata. Phase 4 should make `three_card_past_present_future` executable first, then generalize the same runtime to larger spreads.

## Required Prep Artifacts

| Artifact | Role |
|---|---|
| `.agent/requirements/20260602-0155-spread-runtime-prep/` | Requirements and implementation handoff for the next runtime slice. |
| `data/spread-definitions-v1.json` | Machine-checkable spread fixture mirroring the current built-in spread catalog. |
| `scripts/check_phase4_spread_runtime_prep.py` | Read-only prep gate before writing Phase 4 C++ runtime code. |

## Run Before Phase 4 Work

```text
python scripts/check_phase1_preflight.py
python scripts/check_phase4_spread_runtime_prep.py
```

Both should pass before adding `UOnokoArcanaSpreadReadingSession`.

## Frozen Phase 4 Contracts

The first C++ runtime implementation should add:

- `FOnokoArcanaReadingCardState`
- `FOnokoArcanaSpreadReadingState`
- `UOnokoArcanaSpreadReadingSession`
- `UOnokoArcanaSpreadReadingViewModel`

The first executable multi-card target is:

```text
three_card_past_present_future
```

The first commandlet proof should verify:

- session initializes from the V5 major arcana deck.
- spread starts with 3 slots.
- draw creates 3 unique drawn cards.
- all cards start face-down.
- reveal-next reveals order 1, then 2, then 3.
- selected slot controls title, keywords, note, and guide text.
- reset clears the spread reading.

## SaveGame Direction

Do not remove the existing one-card fields in `FOnokoArcanaSavedReading`. Add an array field for future spread card states, and keep one-card defaults readable.

Recommended future struct:

```text
FOnokoArcanaSavedReadingCardState
```

Minimum fields:

- Position key
- Position label
- Reveal order
- Card id/number/names
- Orientation label
- Active keywords
- Study focus
- User interpretation
- Revealed flag
- Guide revealed flag

## Stop Conditions

Stop and fix before visual/UMG work if:

- `Phase3SpreadRegistryTestResult.json` is not `ok=true`.
- `data/spread-definitions-v1.json` fails fixture validation.
- one-card commandlets fail after adding spread runtime.
- three-card draw duplicates card ids.
- Python map actor spawn is required to produce proof.

## Current Prep Status

The prep checker writes:

```text
reports/phase4-spread-runtime-prep-check-*.json
```

Current result:

- `reports/phase4-spread-runtime-prep-check-20260601-170018.json`
- `ok=true`
- failures: `0`
- warnings: `0`

Current companion preflight:

- `reports/phase1-preflight-check-20260601-170018.json`
- `ok=true`
- only warning: missing `.git`
