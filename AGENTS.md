# ONOKO_ARCANA Codex Handoff

このファイルは、このリポジトリ固有の短い入口だけを置く。全体運用ルールは上位のCodex共通ルールに従う。

## 現在の最優先タスク

- ONOKO ARCANA v1.x は Web/Electron の 2D 占い卓として完成させる。
- 現行本体は `web-app/index.html`、Electron shell は `web-app/electron/main.cjs`。
- 入口文書は `plan.md`、`docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md`、`docs/implementation/IMPLEMENTATION_KANBAN.md`、`docs/design/DESIGN_KANBAN.md`。
- 現在の公開基準は GitHub Release `v0.1.3` public preview。主導線は unsigned NSIS installer、fallback は local zip。
- clean Windows user/VM での manual installer smoke は未完了ゲートとして残す。ローカルで進める次順は、履歴filter follow-up、復習UIの過密化抑制、質問/日付filter判断であり、署名installer/MSIX/Store/小アルカナは別ゲートまで進めない。
- 作業前は `python scripts/check_web_app.py` を実行し、変更内容に応じて Web smoke、Electron smoke、visual audit、package smoke、release artifact smoke を通す。

## Web/Electron環境

- Web entry: `web-app/index.html`
- Electron entry: `web-app/electron/main.cjs`
- Local package output: `dist/onoko-arcana-local/`
- Release artifact output: `dist/release-artifacts/onoko-arcana-vX.Y.Z-local.zip`
- Desktop shortcut helper: `dist/onoko-arcana-local/CREATE_DESKTOP_SHORTCUT.ps1`
- History storage key: `onoko-arcana:desktop:history:v1`
- History schema: `docs/data/HISTORY_SCHEMA_V1.md`
- Card schema: `docs/data/CARD_SCHEMA_V1.md`
- Spread schema: `docs/data/SPREAD_SCHEMA_V1.md`
- Fixed history fixtures: `tests/fixtures/history/`

## 現行v1.xの安全ルール

- Unreal Engine 化は現行v1.xでは完全に見送る。既存UE成果は削除せずアーカイブ証跡として保持する。
- UE関連の `PHASE1_*` 文書、`L_Phase1_OneCard_Table`、`WBP_TableHUD`、Commandlet結果は履歴資料であり、現行実装タスクに混ぜない。
- カード再生成は、現行Web/Electron runtimeでhard blockerが出るまで行わない。
- 小アルカナ56枚は、Major Arcana版の保存、復習、配布、検証が安定するまで着手しない。
- 履歴削除やschema変更では、既存localStorage履歴を自動破棄しない。破壊的変更はmigration docとfixtureを先に用意する。
- `reports/` は生成証跡置き場であり、全runを追跡対象にしない。代表証跡はロードマップまたは `reports/README.md` に明示する。

## 検証コマンド

```powershell
python scripts/check_web_app.py
```

```powershell
cd web-app
npm install
npm run smoke:web
```

```powershell
cd web-app
npm run smoke:electron
```

```powershell
cd web-app
npm run audit:visual
```

```powershell
cd web-app
npm run package:local
```

```powershell
cd web-app
npm run smoke:package
```

```powershell
cd web-app
npm run release:artifact
```

## UEアーカイブ情報

- Unreal project: `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject`
- Engine: `<UE_5.7>`
- 過去にPython map actor spawn経路で `EXCEPTION_ACCESS_VIOLATION` が発生している。UE Python actor spawnを完成証跡に使わない。
- UEを再開する場合は、現行v1.x完了後に新しい要件定義と再開条件を作る。
