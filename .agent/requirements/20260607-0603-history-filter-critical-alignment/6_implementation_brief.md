# Implementation Brief

## Files

- `web-app/src/app.js`
- `web-app/src/styles.css`
- `scripts/smoke_web_app.cjs`
- `docs/implementation/IMPLEMENTATION_KANBAN.md`
- `docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md`
- `docs/release/RESIDUAL_RISK_REGISTER_2026-06-07.md`
- `plan.md`

## Approach

- Extend state with `historySpreadFilter` and `historyNoteFilter`.
- Add a compact filter control inside the existing `historyFilterBar` slot.
- Keep card filter as a status/control row inside the same filter panel.
- Preserve original history indexes in `visibleRows` and use them for restore/delete.
- Add smoke assertions for spread, note-with, note-without, and clear behavior.

## Verification

Run:

```powershell
python scripts/check_web_app.py
cd web-app
npm run smoke:web
npm run smoke:keyboard
npm run audit:visual
npm run smoke:electron
npm run package:local
npm run smoke:package
```
