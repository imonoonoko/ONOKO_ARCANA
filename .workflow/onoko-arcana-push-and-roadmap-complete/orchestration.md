# Orchestration: ONOKO ARCANA push and roadmap complete

## Execution Rules

- Keep the original objective intact.
- Ask for approval before risky, expensive, external, or destructive actions.
- Keep immediate blocking work local.
- Delegate only bounded, disjoint, materially useful packets.
- Integrate packet results before final verification.

## Branching Rules

- If `main` has no upstream or push target, push explicitly to `origin main`.
- If remote rejects a normal push, do not force-push; inspect and report.
- If roadmap references a missing report, fix the roadmap reference before commit.
- If verification reports are missing, regenerate only the narrow relevant checks.

## Packet Prompts

### P1 requirements

Create a compact requirements artifact defining success criteria, scope,
non-goals, acceptance criteria, risks, and implementation steps.

### P2 preflight

Inspect Git state, branch, remote, roadmap references, and report existence.
Summarize anything that should influence staging.

### P3 commit/push

Stage the current state, commit with a clear message, and push to `origin/main`.
Never force-push.

### P4 roadmap completion

Confirm `docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md` is complete
relative to the post-import state. Patch only if a real gap is found.

### P5 final audit

Verify workflow completeness, pushed commit, and clean working tree.

## Completion Audit

- Requirements artifact exists.
- Workflow final report lists commit hash and push result.
- `origin/main` contains the checkpoint commit.
- Roadmap file exists and references existing evidence.
- No required local changes remain after push.
