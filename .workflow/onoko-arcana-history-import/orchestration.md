# Orchestration: ONOKO ARCANA history import

## Execution Rules

- Keep the original objective intact.
- Ask for approval before risky, expensive, external, or destructive actions.
- Keep immediate blocking work local.
- Delegate only bounded, disjoint, materially useful packets.
- Integrate packet results before final verification.

## Branching Rules

- If the exported payload lacks a wrapper schema, support the existing exported
  array/object shape first and add minimal metadata only if export already has it.
- If duplicate identity is ambiguous, use a stable composite key from saved
  reading fields rather than adding IDs retroactively.
- If Electron file import differs from browser import, keep browser behavior
  authoritative and smoke Electron for startup/regression.

## Packet Prompts

### P1 discovery

Inspect `web-app/src/app.js`, `web-app/index.html`, `web-app/src/styles.css`,
and current smoke scripts. Identify the exact export payload shape and where
import behavior should be inserted without changing the reading loop.

### P2 implementation

Add import behavior to the smallest stable surface. Prefer native browser file
input handling, schema validation, deterministic merge, and clear status text.
Do not add dependencies.

### P3 verification

Extend static and smoke checks only where behavior is now part of the product
contract. Prove export -> import -> history restoration and invalid import
feedback where feasible.

### P4 docs

Update the implementation kanban, record accepted decisions, and summarize
final verification evidence.

## Completion Audit

- Gate 1: static check passes after implementation.
- Gate 2: Web smoke proves import behavior.
- Gate 3: Electron smoke still passes.
- Accepted implementation decisions are recorded in `results/`.
- `IMPLEMENTATION_KANBAN.md` import row is updated.
- Final report lists checks, report paths, and residual risks.
