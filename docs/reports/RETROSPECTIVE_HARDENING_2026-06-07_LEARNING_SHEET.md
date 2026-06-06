# ONOKO ARCANA Retrospective Hardening: Card-Tab Study Sheet

作成日: 2026-06-07

## Current Truth

- 現行本線は `web-app/index.html` + `web-app/electron/main.cjs` の Web/Electron 2D 占い卓。
- 今回の受け入れ仕様は、`カード` タブで自分の読みを書きながら同じカードのフル学習シートを参照できること。
- 旧 `ガイド` UI は置換済み。`#toggleGuideButton` と `#guidePanel` は DOM から外し、smoke でも存在しないことを確認する。
- `学習` タブは Study Lens、想起練習、スロット練習の深掘り面として維持する。
- Unreal 関連成果はアーカイブであり、現行 v1.x の実装対象ではない。

## Accepted Proof

- Static check: `reports/web-app-check-20260607-013152.json`
- Web smoke: `reports/web-app-smoke-20260607-011915.json`
- Card-tab screenshot: `reports/onoko-arcana-card-tab-study-sheet-20260607-0120.png`
- Visual audit: `reports/ui-visual-audit-20260607-012023/report.json`
- Keyboard smoke: `reports/keyboard-focus-smoke-20260607-012201.json`
- Electron smoke: `reports/electron-app-smoke-20260607-012214.json`
- Package smoke: `reports/electron-package-smoke-20260607-012237.json`

## Findings And Hardening

P1 - Representative proof drift
Evidence: `reports/README.md` still pointed to the 2026-06-05 proof set while the accepted UI changed on 2026-06-07.
Impact: a future handoff could treat the old guide-era UI as the latest proven state.
Fix: promote the 2026-06-07 card-tab study sheet proof set in `reports/README.md`.
Verification: `python scripts/check_web_app.py` and `git diff --check`.

P1 - Completion report evidence drift
Evidence: `docs/reports/MULTI_TAB_INTERFACE_COMPLETION_REPORT_2026-06-07.md` listed the first multi-tab proof set, before the card-tab guide replacement.
Impact: the report title sounded complete while missing the actual final acceptance screenshot and smoke set.
Fix: update the evidence list to the post-replacement proof set.
Verification: `python scripts/check_web_app.py`.

P2 - Terminology drift around guide
Evidence: the learning roadmap still used `guide` for the old learning surface.
Impact: future UI work could reintroduce a separate guide panel instead of using the study sheet as the learning reference.
Fix: reserve `study sheet` for the card-tab reference surface and `answer/explanation` for gated drill reveals.
Verification: `rg -n "Read before guide|Reveal guide|Note vs Guide|revealing guide|deeper guide" docs/roadmap/TAROT_LEARNING_ENHANCEMENT_ROADMAP_2026-06-06.md` returns no matches.

P2 - Completion criteria needed an explicit repeated check
Evidence: the user asked for repeated confirmation before treating the goal as complete.
Impact: a green smoke run alone does not prove that the original idea, UI replacement, docs, and evidence all align.
Fix: add the completion gate below and use it before closing future learning UI slices.
Verification: rerun the listed command set and confirm each gate has a concrete artifact.

## Completion Gate For Future Learning UI Slices

Do not mark a learning UI slice complete until all checks pass:

1. Original idea check: the first screen remains a usable ONOKO cyber divination table, not a dashboard.
2. Learning order check: normal reading supports write-first comparison, while drills still require user input before answer/explanation reveal.
3. Data safety check: reading history and learning state remain separate and exportable.
4. GUI check: desktop, compact, and mobile visual audit have `issueCount: 0`.
5. Keyboard check: tab panels, study sheet actions, recall, slot drill, settings, and history review remain reachable.
6. Package check: Electron app smoke and local package smoke pass after Web smoke.
7. Evidence check: `reports/README.md`, implementation kanban, design kanban, and the relevant completion report point to the same accepted proof set.

## Next Safe Slice

Proceed with package版 settings local data confirmation and history filter expansion. Keep the card-tab study sheet behavior as a regression gate: a user must be able to write their own reading while the selected card's full study sheet stays visible.
