# Orchestration: ONOKO ARCANA critical roadmap alignment and history filters

## Execution Rules

- Keep the original objective intact.
- Ask for approval before risky, expensive, external, or destructive actions.
- Keep immediate blocking work local.
- Delegate only bounded, disjoint, materially useful packets.
- Integrate packet results before final verification.

## Branching Rules
- If clean Windows/VM is unavailable, mark manual installer smoke as pending and continue only with local checks.
- If filter implementation causes restore/delete index ambiguity, stop and preserve source history indexes before continuing.
- If visual or keyboard checks fail after adding filters, prefer reducing filter UI before adding more conditions.

## Packet Prompts
Packet A:
Review plan, overall roadmap, implementation kanban, and residual risk register for overclaiming around installer evidence. Output exact wording changes that distinguish automated verification from manual external smoke.

Packet B:
Define the first history filter expansion slice. Include goal, scope, non-goals, acceptance criteria, and implementation notes. Do not include broad search/date filters in this slice.

Packet C:
Implement spread and note-presence filters in the existing history panel. Preserve card filter behavior and original history indexes for restore/delete.

Packet D:
Run checks matched to risk and summarize accepted changes, skipped checks, and remaining risks.

## Completion Audit
- Workflow artifacts exist and pass verify_workflow.py.
- Requirements artifact exists under .agent/requirements.
- Docs no longer imply clean Windows installer behavior is verified.
- History filter smoke covers card, spread, note-with, note-without, and clear behavior.
