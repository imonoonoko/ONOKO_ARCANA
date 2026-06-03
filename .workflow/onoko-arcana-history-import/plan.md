# ONOKO ARCANA history import

## Goal

Implement and verify history import for the ONOKO ARCANA Web/Electron MVP.
The app should read a previously exported reading-history JSON file, validate
it, merge valid readings into the existing local history without obvious
duplicates, and keep the current reading loop stable.

## Success Criteria

- The export format is treated as a stable import source.
- The Web app exposes an import action for saved reading history.
- Invalid JSON, wrong schema, and empty imports produce clear UI feedback.
- Imported readings merge with existing `localStorage` history.
- Duplicate readings from the same export are not repeatedly appended.
- Static check, Web smoke, and Electron smoke pass.
- `docs/implementation/IMPLEMENTATION_KANBAN.md` reflects the completed import work.

## Current Context

- Main app: `web-app/index.html`
- JS state: `web-app/src/app.js`
- Data source: `web-app/src/data.js`
- Styling: `web-app/src/styles.css`
- Current persistence key: `onoko-arcana:desktop:history:v1`
- Current export exists; import is marked Active in the implementation kanban.
- Latest baseline reports are under `reports/*20260603-002749*`.

## Constraints

- Preserve existing user work and unrelated uncommitted changes.
- Keep the app direct-open friendly; no build step should be required.
- Do not add dependencies unless the existing code clearly requires them.
- Keep exported/imported history local; do not use network services.
- Use focused changes and update tests/smokes with the same behavior contract.

## Risks

- Malformed or incompatible JSON could corrupt saved history.
- Import could duplicate the same reading repeatedly.
- File input UI could break the compact/mobile layout.
- Smoke tests may need deterministic control over `localStorage`.

## Approval Required

No approval is required for this pass. The work is local, non-destructive, and
does not touch credentials, billing, deployment, or external systems.

## Work Packets

- P1 discovery: inspect current history storage, export format, and smoke coverage.
- P2 implementation: add import UI, validation, merge, duplicate handling, and feedback.
- P3 verification: extend checks/smoke tests and run Web/Electron proof.
- P4 docs: update implementation kanban and final workflow report.

## Integration Policy

Keep all edits in the Web/Electron MVP surface and related docs/tests. If a
packet reveals a broader product question, record it as backlog rather than
expanding the implementation scope.

## Verification

- `python scripts/check_web_app.py`
- bundled Node `scripts/smoke_web_app.cjs`
- bundled Node `scripts/smoke_electron_app.cjs`
- workflow completeness check

## Reusable Artifacts

The workflow plan and final report should remain under
`.workflow/onoko-arcana-history-import/` as the import feature handoff.
