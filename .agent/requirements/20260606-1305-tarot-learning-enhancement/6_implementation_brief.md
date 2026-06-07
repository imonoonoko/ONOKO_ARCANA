# Implementation Brief

## Recommended Implementation Order

1. Card Study Sheet
   - Add static Major Arcana detail view.
   - Extend card data in `web-app/src/data.js` conservatively.
   - No storage migration.

2. Card-Specific Review Filter
   - Click a Study Lens card to filter history review by card.
   - Reuse `readHistory()` and existing history row rendering.
   - Add smoke assertions for filtered review.
   - Status 2026-06-06: implemented and still covered by `reports/web-app-smoke-20260606-140227.json` and `reports/onoko-arcana-card-review-compare-20260606-1342-compare-visible.png`.

3. Note-vs-Guide Comparison
   - In the filtered card review flow, show the saved user note, card guide, and spread slot prompt together.
   - Keep comparison read-only for this slice; confidence and new learning notes belong to Recall Practice.
   - Status 2026-06-06: implemented and still covered by `reports/web-app-smoke-20260606-140227.json`, `reports/ui-visual-audit-20260606-140228/report.json`, and `reports/keyboard-focus-smoke-20260606-140258.json`.

4. Recall Practice
   - Add a practice mode that shows a card and asks the user to type keywords before revealing guide text.
   - Store attempts in `onoko-arcana:desktop:learning:v1`.
   - Status 2026-06-06: minimal practice loop implemented and verified with `reports/web-app-smoke-20260606-140227.json`, `reports/onoko-arcana-recall-practice-20260606-1403-recall.png`, and `tests/fixtures/learning/learning-valid-v1.json`.

5. Spaced Review Queue
   - Use simple intervals at first: same day, 1 day, 3 days, 7 days, 14 days.
   - Track confidence: hard / ok / easy.
   - Keep export/import of learning state separate from reading history.
   - Status 2026-06-06: settings/data controls are implemented and verified with `reports/web-app-smoke-20260606-192417.json`, `reports/onoko-arcana-settings-20260606-192417.png`, and `reports/onoko-arcana-learning-export-20260606-192417.json`.
   - Status 2026-06-06 update: first-launch learning guidance, after-save next actions, and minimal due-card queue are implemented and verified with `reports/web-app-smoke-20260606-194424.json`, `reports/onoko-arcana-first-launch-20260606-194424.png`, and `reports/ui-visual-audit-20260606-194648/report.json`.
   - Next recommended slice: Card Study Sheet plus GUI information density guardrail.

6. Spread Tutor
   - Teach slot purpose before card meaning.
   - Start with one-card and three-card before Celtic Cross.

## Verification

- `python scripts/check_web_app.py`
- `cd web-app; npm run smoke:web`
- `cd web-app; npm run smoke:keyboard`
- `cd web-app; npm run audit:visual`

Latest verified slice 2026-06-06:

- `python scripts/check_web_app.py` -> `reports/web-app-check-20260606-195432.json`
- `cd web-app; npm run smoke:web` -> `reports/web-app-smoke-20260606-194424.json`
- `cd web-app; npm run smoke:electron` -> `reports/electron-app-smoke-20260606-194716.json`
- `cd web-app; npm run audit:visual` -> `reports/ui-visual-audit-20260606-194648/report.json`
- `cd web-app; npm run smoke:keyboard` -> `reports/keyboard-focus-smoke-20260606-194648.json`
- Settings screenshot: `reports/onoko-arcana-settings-20260606-194424.png`
- First-launch screenshot: `reports/onoko-arcana-first-launch-20260606-194424.png`
- Learning export sample: `reports/onoko-arcana-learning-export-20260606-194424.json`

New contract artifacts:

- `docs/data/LEARNING_SCHEMA_V1_DRAFT.md`
- `tests/fixtures/learning/learning-valid-v1.json`

## Risk Controls

- Do not rewrite history schema for study metrics.
- Keep learning state optional and recoverable.
- Avoid filling the reading table with too much text.
- Treat tarot meanings as interpretive study content, not objective predictions.
