# Preemptive Bug Risk Audit 2026-06-05

目的: 公開後や配布前に不具合化しやすい経路を、通常CIだけでなく手動エッジケースも含めて事前調査する。

## 調査対象

- Web/Electron runtime: `web-app/src/app.js`
- 履歴保存/import/export/復元: `docs/data/HISTORY_SCHEMA_V1.md`, `tests/fixtures/history/`
- キーボード操作: `scripts/smoke_keyboard_focus.cjs`
- Web/Electron/package smoke: `scripts/smoke_web_app.cjs`, `scripts/smoke_electron_app.cjs`, `scripts/smoke_electron_package.cjs`
- Local package generation: `scripts/package_electron_local.cjs`

## 見つけて修正したリスク

| Risk | Symptom | Fix | Regression proof |
|---|---|---|---|
| Imported card notes were not restored | `cards[].note` だけを持つ履歴を復元すると、復習表示にはメモが出るが編集欄が空になる | `normalizeReadingNotes()` を追加し、現行 `1:slotKey`、旧 `slotKey-index`、`cards[].note` を復元時に正規化 | `history-card-note-only-v1.json`, `smoke:web` |
| Hidden card buttons were keyboard-focusable | ドロー直後、未開示カード裏面がTab順に入り、押しても何も起きない | 未開示/空スロットのカードbuttonに `tabindex="-1"` を付与 | `smoke:keyboard` の `focusableHiddenCards === 0` |
| Imported history review could show incomplete labels | `displayNumber` / `japaneseName` がないimport履歴で `undefined major-00-fool` と表示される | review表示時に `cardId` から現行カード定義を補完し、`cardName` もfallbackに使用 | `smoke:web` で `0 愚者` と `!undefined` を確認 |

## 残る監視ポイント

- 大量履歴や極端に長いメモでの容量上限/描画負荷。現状は48件上限だが、1件あたりの文字数上限は未設定。
- Electron package の配布品質。現状はlocal folder packageで、署名installer、自動更新、ユーザーデータ移行は別タスク。
- 旧prototype配下は現行v1.x対象外。公開ツリーには残るため、今後の変更で誤って現行経路へ戻さない。
- 履歴schema v2を作る場合、migration fixtureを先に追加する。

## Verification

2026-06-05 に以下を実行し、全て成功:

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

代表run output:

- `reports/web-app-check-20260605-020131.json`
- `reports/web-app-smoke-20260605-020132.json`
- `reports/keyboard-focus-smoke-20260605-020138.json`
- `reports/ui-visual-audit-20260605-020139/report.json`
- `reports/electron-app-smoke-20260605-020202.json`
- `reports/electron-package-smoke-20260605-020206.json`
