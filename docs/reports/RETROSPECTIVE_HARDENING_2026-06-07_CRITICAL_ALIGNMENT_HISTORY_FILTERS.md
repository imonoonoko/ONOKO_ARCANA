# ONOKO ARCANA Retrospective Hardening: Critical Alignment And History Filters

作成日: 2026-06-07

## Current Truth

- 現行本線は `web-app/index.html` + `web-app/electron/main.cjs` の Web/Electron 2D 占い卓。
- GitHub Release `v0.1.3` は公開済みで、主導線は unsigned NSIS installer、fallback は local zip。
- clean Windows user/VM での manual installer smoke は未完了。SmartScreen、実ショートカットicon、uninstall cleanup、fallback zipの実ユーザー経路は外部環境待ち。
- ローカルで完了した履歴filterは、カード、スプレッド、メモ有無の複合filter。
- 質問文filterと保存日filterは、履歴inspectorの密度を見てから別スライスで判断する。
- Unreal 関連成果はアーカイブであり、現行 v1.x の実装対象ではない。

## Accepted Proof

- Static check: `reports/web-app-check-20260607-061238.json`
- Web smoke: `reports/web-app-smoke-20260607-061029.json`
- Keyboard smoke: `reports/keyboard-focus-smoke-20260607-061239.json`
- Visual audit: `reports/ui-visual-audit-20260607-061249/report.json`
- Electron smoke: `reports/electron-app-smoke-20260607-061249.json`
- Local package smoke: `reports/electron-package-smoke-20260607-061337.json`
- Workflow verification: `.workflow/onoko-arcana-critical-roadmap-alignment-and-history-filters/` passed `verify_workflow.py`.

## Findings And Hardening

P1 - Entry handoff drift can redirect future work
Evidence: `AGENTS.md` still named `v0.1.2` as the current public preview while `plan.md` and release docs named `v0.1.3`.
Impact: a future agent could spend time on already-completed release-support tasks or treat installer manual smoke as completed evidence.
Fix: update `AGENTS.md` so it names `v0.1.3`, keeps clean Windows manual smoke pending, and lists local follow-up work separately from signing/MSIX/Store/Minor Arcana.
Verification: read `AGENTS.md`, `plan.md`, release docs, and `reports/README.md` for the same release posture.

P1 - Installer evidence must not be described as user-environment proof
Evidence: automated local/package/installer smokes verify launch and resource wiring, but not a fresh Windows shell install path.
Impact: roadmap language can overstate readiness and hide SmartScreen, antivirus, shortcut rendering, uninstall, or real-user fallback issues.
Fix: keep the phrase "automated verified / clean Windows manual smoke pending" in roadmap, kanban, risk register, and handoff docs.
Verification: before any release promotion, run `docs/release/INSTALLER_MANUAL_SMOKE_CHECKLIST.md` on a clean Windows user or VM and record evidence.

P1 - Filtered history rows must preserve original history indexes
Evidence: filtered display order is not the same as persisted history array order.
Impact: restore/delete could target the wrong saved reading if UI rows are reindexed after filtering.
Fix: preserve `data-history-index` from the original history item while adding `data-history-spread-id` and `data-history-has-note` for assertions.
Verification: `npm run smoke:web` covers card, spread, note-with, note-without, clear, restore, and delete behavior.

P2 - History filter scope needs a UI density gate
Evidence: card + spread + note filters already add visible control density to the history inspector.
Impact: adding question text and date filters immediately could make the inspector harder to scan, especially before visual review.
Fix: defer question/date filters until the current compact controls are reviewed in normal use.
Verification: run `npm run audit:visual` and a manual browser pass before adding more controls.

P2 - Dynamic workflow artifacts need packet files, not only result summaries
Evidence: `verify_workflow.py` fails when `.workflow/.../packets/` is empty even if final results exist.
Impact: future continuation loses the intended work boundaries and cannot validate orchestration completeness.
Fix: create small packet definitions and matching result notes for docs, requirements, implementation, and verification.
Verification: run `python C:\Users\Humin\.codex\skills\codex-dynamic-workflows\scripts\verify_workflow.py .workflow\onoko-arcana-critical-roadmap-alignment-and-history-filters`.

P2 - Generated proof references need a representative index
Evidence: timestamped reports are ignored/local by default and easy to cite inconsistently.
Impact: future handoff may quote stale proof or force-add large generated evidence.
Fix: keep `reports/README.md` as the representative proof index and update roadmap/kanban references only when a newer run is accepted.
Verification: `git status --short` should not require generated report files unless deliberately promoted.

## Completion Gate For Similar Slices

1. Run `python scripts/check_web_app.py` before and after touching entry docs or app code.
2. If the work changes history UI, run `npm run smoke:web` and keep restore/delete assertions on original persisted indexes.
3. If the work changes desktop/release guidance, run Electron/package smokes and update the residual risk register.
4. If a workflow artifact is created, include both packet definitions and result notes, then run `verify_workflow.py`.
5. Update `plan.md`, roadmap, implementation kanban, and `reports/README.md` to one shared proof set.
6. Do not call installer readiness complete until clean Windows manual smoke has been recorded.

## Next Safe Slice

Review the current history inspector density after card/spread/note filters. If it remains readable, add either question text search or saved-date filter, not both at once. Keep clean Windows manual installer smoke as the release-gate task that cannot be closed from this workstation alone.
