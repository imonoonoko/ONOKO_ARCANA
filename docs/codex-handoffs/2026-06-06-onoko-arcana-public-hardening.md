# Codex Session Handoff: ONOKO ARCANA Public Hardening

## Reactivation Prompt

```text
We are continuing from this handoff:
C:\ONOKO_PROJECT\ONOKO_ARCANA\docs\codex-handoffs\2026-06-06-onoko-arcana-public-hardening.md

Read that document first, then inspect the current repo state. Do not assume the old chat context is available. Continue from the Next Steps section, verifying what still applies before changing files or global config.
```

## Context

- Repo/path: `C:\ONOKO_PROJECT\ONOKO_ARCANA`
- Branch: `main`
- Latest verified local commit at handoff time: `01407b4 Harden history restore and keyboard edge cases`
- Remote state observed at handoff time: `main...origin/main`, no ahead/behind
- Current goal: finish ONOKO ARCANA v1.x as a Web/Electron 2D tarot reading table, with public GitHub hygiene, history safety, package smoke coverage, and practical next-feature hardening.
- Primary app path: `web-app/index.html`
- Electron shell: `web-app/electron/main.cjs`
- History key: `onoko-arcana:desktop:history:v1`
- User constraints:
  - Read the actual repo state before deciding.
  - Prefer small, verified changes over broad rewrites.
  - Keep durable docs/fixtures/smokes when a lesson or regression risk is found.
  - Do not revert unrelated user changes.
  - Do not mix archived Unreal work into the current v1.x Web/Electron lane.
  - Do not break existing localStorage history without migration docs and fixtures.
  - Cap potentially large command output.

## What Changed

- Public GitHub readiness was added and pushed:
  - Windows CI workflow at `.github/workflows/ci.yml`
  - bug report issue template and issue template config
  - `CONTRIBUTING.md`
  - `SECURITY.md`
  - asset/license attribution doc at `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`
  - README public-repo notes and CI badge
- CI/package hardening was completed:
  - `scripts/package_electron_local.cjs` now resolves/downloads Electron robustly after `npm ci`.
  - Electron smoke scripts avoid false failures when CI opens a smaller-than-expected window.
  - GitHub Actions runtime versions were refreshed.
- Preemptive bug-risk audit was performed and fixed:
  - Imported histories that only had `cards[].note` now restore notes into the editor.
  - Legacy note-key shapes are normalized into current `revealIndex:slotKey` keys such as `1:present`.
  - Hidden/unrevealed card buttons are no longer reachable by Tab.
  - Imported history review labels fall back from `cardId` to current card metadata instead of showing `undefined`.
- Durable regression coverage was added:
  - `tests/fixtures/history/history-card-note-only-v1.json`
  - new assertions in `scripts/smoke_web_app.cjs`
  - new hidden-card focus assertion in `scripts/smoke_keyboard_focus.cjs`
  - fixture coverage in `scripts/check_web_app.py`
  - schema notes in `docs/data/HISTORY_SCHEMA_V1.md`
- A bug-risk audit record was added at `docs/implementation/PREEMPTIVE_BUG_RISK_AUDIT_2026-06-05.md`.

## Files Touched Or Investigated

- `web-app/src/app.js`
- `web-app/index.html`
- `web-app/electron/main.cjs`
- `scripts/check_web_app.py`
- `scripts/smoke_web_app.cjs`
- `scripts/smoke_keyboard_focus.cjs`
- `scripts/smoke_electron_app.cjs`
- `scripts/smoke_electron_package.cjs`
- `scripts/package_electron_local.cjs`
- `.github/workflows/ci.yml`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`
- `docs/data/HISTORY_SCHEMA_V1.md`
- `docs/data/CARD_SCHEMA_V1.md`
- `docs/data/SPREAD_SCHEMA_V1.md`
- `docs/implementation/IMPLEMENTATION_KANBAN.md`
- `docs/design/DESIGN_KANBAN.md`
- `docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md`
- `docs/implementation/PREEMPTIVE_BUG_RISK_AUDIT_2026-06-05.md`
- `tests/fixtures/history/history-valid-v1.json`
- `tests/fixtures/history/history-duplicate-v1.json`
- `tests/fixtures/history/history-card-note-only-v1.json`

## Commands And Checks Already Run

Current handoff verification, 2026-06-06:

```powershell
git status --short --branch
git log --oneline --decorate -8
python scripts/check_web_app.py
gh run list --limit 5 --json databaseId,headSha,status,conclusion,workflowName,createdAt,displayTitle
```

Observed current results:

- `python scripts/check_web_app.py`: success, `checkedAt` `2026-06-06T12:52:07`, report `reports\web-app-check-20260606-125207.json`.
- GitHub Actions latest run for `01407b4`: `CI`, databaseId `26966955970`, conclusion `success`.
- Working tree was clean before this handoff file was added.

Previously completed full local verification, recorded in `docs/implementation/PREEMPTIVE_BUG_RISK_AUDIT_2026-06-05.md`:

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

Representative prior reports:

- `reports/web-app-check-20260605-020131.json`
- `reports/web-app-smoke-20260605-020132.json`
- `reports/keyboard-focus-smoke-20260605-020138.json`
- `reports/ui-visual-audit-20260605-020139/report.json`
- `reports/electron-app-smoke-20260605-020202.json`
- `reports/electron-package-smoke-20260605-020206.json`

## Known Issues

- History count is capped, but extremely long per-reading notes are not capped. This can still create localStorage quota or rendering pressure.
- The current package target is a local folder package. Signed installer, `.ico`, auto-update, and user-data migration are still separate distribution tasks.
- `prototype/` and Unreal-related docs/assets are historical evidence. They are not the active v1.x implementation path.
- Any history schema v2 work needs migration fixtures before runtime behavior changes.
- `reports/` is generated evidence. Do not start tracking every report file; use `reports/README.md` and selected docs to point to representative output.

## Open Decisions

- Exact UX for history review filters: card, spread, question text, date, keyword, or a combined segmented/search UI.
- Whether settings should be a modal, side panel section, or dedicated view.
- Whether to add a per-note character limit now, and what limit is acceptable for real use.
- Whether public distribution should remain source/local-package only or move to signed installer.
- When, if ever, to start Minor Arcana expansion. Current rule: do not start until Major Arcana history/review/package flow is stable.

## Next Steps

1. Re-run `git status --short --branch` and `python scripts/check_web_app.py` before feature work.
2. Design the history review filter contract first: filter fields, empty results state, import compatibility, and smoke assertions.
3. Implement the smallest history filter slice in `web-app/src/app.js`, likely starting with spread/card/date or query text, then add Playwright smoke coverage.
4. Add settings screen requirements for history/export/import/display controls before coding the settings UI.
5. Improve first-run empty state and save-complete next actions after the filter direction is stable.
6. Add a long-note/quota guard if history filters or settings touch persistence behavior.
7. Only after the local package flow remains stable, define external distribution polish: installer, `.ico`, signing, auto-update, and migration behavior.

## Do Not Touch / Be Careful

- Do not make Unreal Engine the active path for v1.x.
- Do not delete archived Unreal/prototype evidence unless the user explicitly asks.
- Do not start Minor Arcana until the Major Arcana review, persistence, package, and distribution decisions are stable.
- Do not discard or auto-migrate existing localStorage history without a documented migration path and fixtures.
- Do not commit ignored `reports/` outputs unless a specific representative evidence file is intentionally promoted.
- Do not expose private session IDs or unrelated local metadata in public docs.
