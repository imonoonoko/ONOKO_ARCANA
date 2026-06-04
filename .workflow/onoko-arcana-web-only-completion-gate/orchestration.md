# Orchestration: ONOKO ARCANA web-only completion gate

## Execution Rules

- Keep the original objective intact.
- Ask for approval before risky, expensive, external, or destructive actions.
- Keep immediate blocking work local.
- Delegate only bounded, disjoint, materially useful packets.
- Integrate packet results before final verification.

## Branching Rules

- If UE references appear as future active work, rewrite them to "shelved" or
  "archived evidence" while preserving old evidence.
- If history delete is implemented, require `confirm()` before destructive
  deletion and keep export available before deletion.
- If a full installer is too large for this pass, do not add a packaging
  dependency; make Web/Electron local runtime the completion target.

## Packet Prompts

### P1 scope lock

Update roadmap wording so Web/Electron is the final mainline for now and UE is
fully shelved. Define the adjusted completion gate.

### P2 implementation

Add history single-delete and clear-all controls. Add a notebook-style visual
surface for user interpretation notes. Preserve import/export.

### P3 schema/docs

Create `docs/data/HISTORY_SCHEMA_V1.md` and update kanbans/roadmaps to match.

### P4 verification

Run static, Web smoke, Electron smoke, keyboard/focus smoke, and visual audit.
Patch focused regressions only.

### P5 closeout

Record results, report paths, and remaining risks in final report.

## Completion Audit

- Roadmap no longer presents UE conversion as a future active lane.
- History delete and clear are verified.
- Notebook UI is visible in screenshots.
- Schema doc exists.
- Verification reports are current.
