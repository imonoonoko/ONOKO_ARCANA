# ONOKO ARCANA web-only completion gate

## Goal

Move ONOKO ARCANA to a Web/Electron-only direction, fully shelve Unreal work,
and advance the improvement roadmap to its practical completion gate with
history safety, schema documentation, keyboard/focus verification, and a
notebook-style reading UI inspired by the first design kanban board.

## Success Criteria

- Roadmaps state that UE conversion is fully shelved, not a future active lane.
- Web/Electron remains the product mainline.
- History can be deleted one item at a time and cleared with confirmation.
- History export/import/localStorage schema is documented.
- Keyboard/focus smoke exists and passes.
- The user's interpretation area reads visually as an ONOKO study notebook.
- Existing static, Web, Electron, and visual checks pass.

## Current Context

- Branch: `main`
- Existing uncommitted docs: improvement roadmap and overall roadmap reference.
- Main app: `web-app/index.html`
- Runtime state: `web-app/src/app.js`
- Styling: `web-app/src/styles.css`
- Current proof reports: `reports/*20260604-033*`

## Constraints

- Do not delete UE project/history; mark it shelved in docs.
- Keep all changes local and non-destructive.
- Preserve existing history import/export behavior.
- Avoid adding package dependencies unless unavoidable.
- Keep the notebook design readable and within the current ONOKO dark UI.

## Risks

- Delete/clear history can destroy user data; require confirmation and backup cue.
- Notebook styling can reduce contrast; verify visually.
- Keyboard smoke can be brittle if selectors are not stable.

## Approval Required

No additional approval required. The user explicitly requested progressing this
roadmap gate and fully shelving UE conversion.

## Work Packets

- P1 scope lock: record Web-only / UE-shelved decision and completion gate.
- P2 implementation: history delete/clear and notebook UI.
- P3 schema/docs: history schema and roadmap updates.
- P4 verification: static, Web, Electron, keyboard/focus, visual audit.
- P5 closeout: workflow final report and remaining risks.

## Integration Policy

Prefer focused changes to app, scripts, and docs. If packaging becomes too large
for this slice, document it as optional after Web/Electron local runtime and
do not block the Web-only completion gate on installer generation.

## Verification

- `python scripts/check_web_app.py`
- `scripts/smoke_web_app.cjs`
- `scripts/smoke_electron_app.cjs`
- keyboard/focus smoke
- `scripts/audit_web_ui_visual.cjs`
- workflow verification

## Reusable Artifacts

Keep the workflow directory as the handoff for why UE is shelved and how the
Web-only completion gate was satisfied.
