# ONOKO_ARCANA Codex Handoff

このファイルは、このリポジトリ固有の短い入口だけを置く。全体運用ルールは上位のCodex共通ルールに従う。

## 現在の最優先タスク

- ONOKO ARCANA v1.x は Web/Electron の 2D 占い卓として完成させる。
- 現行本体は `web-app/index.html`、Electron shell は `web-app/electron/main.cjs`。
- 入口文書は `plan.md`、`docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md`、`docs/implementation/IMPLEMENTATION_KANBAN.md`、`docs/design/DESIGN_KANBAN.md`。
- 次の実装順は、履歴復習filter、settings画面、初回起動empty state、配布polish。
- 作業前は `python scripts/check_web_app.py` を実行し、変更内容に応じて Web smoke、Electron smoke、visual audit、package smoke を通す。

## Web/Electron環境

- Web entry: `web-app/index.html`
- Electron entry: `web-app/electron/main.cjs`
- Local package output: `dist/onoko-arcana-local/`
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
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_web_app.cjs
```

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_app.cjs
```

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/audit_web_ui_visual.cjs
```

```powershell
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/package_electron_local.cjs
```

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_package.cjs
```

## UEアーカイブ情報

- Unreal project: `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject`
- Engine: `C:\Program Files\Epic Games\UE_5.7`
- 過去にPython map actor spawn経路で `EXCEPTION_ACCESS_VIOLATION` が発生している。UE Python actor spawnを完成証跡に使わない。
- UEを再開する場合は、現行v1.x完了後に新しい要件定義と再開条件を作る。
