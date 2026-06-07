# KPI And Guardrails

## Product KPIs

| KPI | Target | Measurement |
| --- | --- | --- |
| Task separation | 3 primary inspector tasks are separated into visible tabs | DOM has exactly 3 `data-inspector-tab` controls and 3 panels |
| Learning access | Study Sheet, Slot Drill, Study Lens, Recall Practice remain reachable | `npm run smoke:web` study assertions pass |
| Review access | History list, filter, restore, delete, clear remain reachable | `npm run smoke:web` history assertions pass |
| Visual stability | No P1/P2 visual audit issues | `npm run audit:visual` ok |
| Storage safety | No schema/storage migration | static check and smoke import/export pass |

## Complexity Guardrails

- Add one small tab state (`state.inspectorTab`) instead of splitting the app into new modules in this slice.
- Keep existing render functions (`renderInspector`, `renderStudySheet`, `renderStudyLens`, `renderHistory`) and add a thin tab renderer around them.
- Do not duplicate selected card, study lens, or history DOM.
- Update tests to open tabs before interacting with hidden content.

## Stop Conditions

- Visual audit reports desktop panel clipping caused by tab layout.
- Smoke cannot complete history import/export or learning export/import.
- A storage schema change becomes necessary. In that case, stop and write a migration requirement first.
