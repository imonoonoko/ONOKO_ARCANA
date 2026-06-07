# ONOKO ARCANA multi tab interface

## Goal
右 inspector に混在している `選択カード / 自分の読み / guide / カード学習 / 学習レンズ / 履歴 / 復習ノート` を、既存の占い卓体験を保ったまま複数タブで扱える構造に更新する。

## Success Criteria
- 右 inspector に `カード`、`学習`、`履歴` の3タブがあり、現在の作業文脈に合わせて切り替えられる。
- 既存 DOM 契約 (`selectedCard`, `studySheetPanel`, `studyLens`, `historyList`, `historyReview`, settings 関連 ID) は維持する。
- 既存の「自分の読み -> guide -> 保存 -> 復習/学習」ループを壊さない。
- desktop / compact / low-height / mobile の visual audit で P1/P2 issue 0。
- `check_web_app.py` と `smoke:web` が通る。

## Current Context
- 現行本体は `web-app/index.html`、ロジックは `web-app/src/app.js`、スタイルは `web-app/src/styles.css`。
- 2026-06-07 編集前 baseline: `reports/web-app-check-20260607-003541.json` が `ok: true`。
- 右 inspector は学習機能追加で情報密度が高くなっている。タブ化は GUI 最適化カンバンの次カードとして扱う。

## Constraints
- Web/Electron v1.x の 2D 卓を維持し、UE/3D 再開は混ぜない。
- 履歴 localStorage schema は変更しない。
- 学習 localStorage schema は変更しない。
- カード画像再生成と小アルカナ追加は対象外。

## Risks
- hidden tab panel により既存 smoke のクリック対象が不可視になる。
- 右パネルの高さ再配分で desktop low-height が clipping する。
- 自動タブ切替が多すぎると、利用者が今いる場所を見失う。

## Approval Required
不要。外部公開、削除、依存追加、破壊的 migration は行わない。

## Work Packets
- P0 Requirements: `.agent/requirements/20260607-0035-multi-tab-inspector/` に要件、受け入れ条件、KPI、GUI方針を残す。
- P0 Implementation: inspector tab shell、タブ状態、キーボード操作、文脈別自動切替を実装する。
- P0 Test Contract: static check、web smoke、visual audit をタブ操作前提へ更新する。
- P1 Documentation: design/implementation kanban と completion report を更新する。

## Integration Policy
- 既存 ID を移動しても削除しない。
- 新規 UI 契約は `data-inspector-tab` / `data-inspector-panel` と `role=tablist/tab/tabpanel` に集約する。
- タブの初期値は `card`。学習ボタンは `study`、履歴操作は `history` に明示移動する。

## Verification
- `python scripts/check_web_app.py`
- `cd web-app; npm run smoke:web`
- `cd web-app; npm run audit:visual`
- 必要に応じて `npm run smoke:electron` または package smoke。

## Reusable Artifacts
- `.agent/requirements/20260607-0035-multi-tab-inspector/`
- `.workflow/onoko-arcana-multi-tab-interface/results/`
- `design-qa.md`
- `docs/reports/MULTI_TAB_INTERFACE_COMPLETION_REPORT_2026-06-07.md`
