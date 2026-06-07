# Discussion Log

## 2026-06-06

User request: タロットカードの勉強要素をさらに強化するため、ネット上の占い情報、タロットカード情報、学習に関する情報を徹底リサーチし、ロードマップを作成する。`$define-requirements` 指定あり。

Current baseline confirmed from repo:

- ONOKO ARCANA v1.x is Web/Electron only.
- Current learning loop is: question -> draw -> reveal -> write own note -> reveal guide -> save -> review history.
- Existing card data includes Major Arcana 22 cards with upright keywords, reversed keywords, and `studyFocus`.
- Study lens has already been added in the current worktree to summarize saved readings, note count, seen/unseen cards, frequent cards, and next observation candidates.

Research themes:

- Tarot historical structure and source-of-truth content model.
- Tarot learning app patterns: card library, journaling, patterns/stats, spreads, reflection prompts.
- Evidence-based learning techniques: retrieval practice, spacing, interleaving, guided reflection.

## 2026-06-06 Implementation Start

- Implemented the first Phase L2 slice: Study Lens card clickthrough to card-specific history review filter.
- Added a dedicated filter bar between Study Lens and history list so the filtered study state stays visible.
- Added Web smoke assertions proving filtered rows all contain the selected card and clearing returns to all history.
- Next recommended slice: note-vs-guide comparison inside the filtered card review flow.

## 2026-06-06 Implementation Update

- Added note-vs-guide comparison inside the card-specific review flow.
- The filtered review card now shows the saved user reading, the card guide, and the spread slot prompt together.
- Tightened the filtered history layout so the comparison block is visible in the right panel without burying the table.
- Verification evidence: `reports/web-app-smoke-20260606-134209.json`, `reports/ui-visual-audit-20260606-134209/report.json`, `reports/keyboard-focus-smoke-20260606-134210.json`, and `reports/onoko-arcana-card-review-compare-20260606-1342-compare-visible.png`.

## 2026-06-06 Recall Practice Implementation

- Added a Study Lens practice mode that asks the user to recall card keywords before revealing guide text.
- Added upright/reversed practice switching and hard/ok/easy confidence saving.
- Added separate local learning storage at `onoko-arcana:desktop:learning:v1`, plus `docs/data/LEARNING_SCHEMA_V1_DRAFT.md` and `tests/fixtures/learning/learning-valid-v1.json`.
- Tightened the right panel layout so the active recall card, guide, and confidence buttons fit without compressing the history list.
- Verification evidence: `reports/web-app-check-20260606-140226.json`, `reports/web-app-smoke-20260606-140227.json`, `reports/ui-visual-audit-20260606-140228/report.json`, `reports/keyboard-focus-smoke-20260606-140258.json`, and `reports/onoko-arcana-recall-practice-20260606-1403-recall.png`.

## 2026-06-06 Settings And Learning Data Controls

- Added a settings modal that separates reading history, learning attempts, display preference, and local storage keys.
- Added learning data export/import/clear separately from reading history.
- Added compact learning panel setting stored under `onoko-arcana:desktop:settings:v1`.
- Updated the GUI optimization kanban so settings learning controls are evidence-backed and the next GUI cards are first-launch guidance, due-card queue, and deeper a11y.
- Verification evidence: `reports/web-app-check-20260606-193148.json`, `reports/web-app-smoke-20260606-192417.json`, `reports/electron-app-smoke-20260606-193341.json`, `reports/onoko-arcana-settings-20260606-192417.png`, `reports/onoko-arcana-learning-export-20260606-192417.json`, `reports/ui-visual-audit-20260606-192637/report.json`, and `reports/keyboard-focus-smoke-20260606-192637.json`.

## 2026-06-06 First Launch And Due Review Update

- Added a first-launch learning guide for the empty history state.
- Added after-save actions so the user can start review immediately or move to the next question.
- Added a minimal due-card cue derived from latest hard/ok/easy learning attempts without changing reading history.
- Updated `docs/design/GUI_OPTIMIZATION_KANBAN_2026-06-06.md`, implementation/design kanbans, roadmap, workflow state, and learning schema with the new evidence.
- Verification evidence: `reports/web-app-check-20260606-195432.json`, `reports/web-app-smoke-20260606-194424.json`, `reports/electron-app-smoke-20260606-194716.json`, `reports/onoko-arcana-first-launch-20260606-194424.png`, `reports/onoko-arcana-settings-20260606-194424.png`, `reports/onoko-arcana-learning-export-20260606-194424.json`, `reports/ui-visual-audit-20260606-194648/report.json`, and `reports/keyboard-focus-smoke-20260606-194648.json`.
