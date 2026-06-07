# ONOKO ARCANA Tarot Learning Final Report

Date: 2026-06-06

## Result

The current verified slice turns ONOKO ARCANA from saved-reading review into an active tarot study loop:

1. Write or recall before guide.
2. Reveal guide after the user's attempt.
3. Compare the user's note with guide and slot prompt.
4. Open a compact card study sheet with upright/reversed keywords, symbols, common misreads, and reflection questions.
5. Practice card + spread slot + orientation interpretation before revealing slot guide.
6. Save practice confidence separately from reading history.
7. Manage history data, learning data, display preference, and local storage keys from settings.
8. Guide first-time users into the learning loop and show a quiet due-review cue after practice attempts.

## Implemented

- Card-specific review from Study Lens.
- Note-vs-guide comparison in filtered history.
- Card Study Sheet from selected cards and Study Lens.
- Major Arcana `studyDetails` for symbols, common misreads, and reflection questions.
- Recall Practice with upright/reversed switching.
- Slot Interpretation Drill inside Card Study Sheet for the selected table card.
- hard/ok/easy confidence saved to `onoko-arcana:desktop:learning:v1`.
- Settings modal for reading history, learning attempts, display preference, and local storage keys.
- Separate learning export/import/clear flow.
- First-launch guide for `問いを書く -> 引く -> 自分の読みを書く -> guide -> 保存/復習`.
- After-save actions for starting review or beginning the next question.
- Minimal due-card queue from hard/ok/easy learning attempts.
- Learning schema draft and fixture.
- GUI optimization kanban for learning updates.

## Verified

- `python scripts/check_web_app.py` -> `reports/web-app-check-20260606-203719.json`
- `cd web-app; npm run smoke:web` -> `reports/web-app-smoke-20260606-203136.json`
- `cd web-app; npm run audit:visual` -> `reports/ui-visual-audit-20260606-203150/report.json`
- `cd web-app; npm run smoke:keyboard` -> `reports/keyboard-focus-smoke-20260606-203220.json`
- `cd web-app; npm run smoke:electron` -> `reports/electron-app-smoke-20260606-203227.json`
- `cd web-app; npm run package:local` -> `dist/onoko-arcana-local/package-manifest.json`
- `cd web-app; npm run smoke:package` -> `reports/electron-package-smoke-20260606-203245.json`
- Recall screenshot: `reports/onoko-arcana-recall-practice-20260606-1403-recall.png`
- Settings screenshot: `reports/onoko-arcana-settings-20260606-203136.png`
- First-launch screenshot: `reports/onoko-arcana-first-launch-20260606-203136.png`
- Card Study Sheet and Slot Drill screenshot set: `reports/ui-visual-audit-20260606-203150/`
- Learning export sample: `reports/onoko-arcana-learning-export-20260606-203136.json`

## Recheck 2026-06-07

- `python scripts/check_web_app.py` -> `reports/web-app-check-20260607-001413.json`
- `cd web-app; npm run smoke:web` -> `reports/web-app-smoke-20260607-001121.json`
- `cd web-app; npm run audit:visual` -> `reports/ui-visual-audit-20260607-001202/report.json`
- The recheck fixed a smoke-only flaky assumption: Study Lens now chooses a non-active card for the Slot Drill disabled case instead of depending on random spread contents.

## Remaining

- Package settings visual check for local data location and recovery wording.
- History filters by spread, date, question, and note presence.
- Spread Tutor and story synthesis requirements.
