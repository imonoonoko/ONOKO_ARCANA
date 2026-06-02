# ONOKO_ARCANA Codex Handoff

このファイルは、このリポジトリ固有の短い入口だけを置く。全体運用ルールは上位のCodex共通ルールに従う。

## 現在の最優先タスク

- Phase 1は `L_Phase1_OneCard_Table` 上で、実際のUE Editor/Blueprint/UMG配線を完成させる段階。
- 入口文書は `plan.md`、`docs/implementation/PHASE1_ONE_CARD_TABLE_WIRING.md`、`docs/implementation/PHASE1_UE_CODEX_PREFLIGHT_2026-06-01.md`。
- 作業前に `python scripts/check_phase1_preflight.py` を実行し、結果JSONを `reports/` に残す。

## UE環境

- Unreal project: `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject`
- Engine: `C:\Program Files\Epic Games\UE_5.7`
- Editor: `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe`
- Commandlet: `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe`
- Codex MCP bridge: `tools/unreal_mcp/server.py`。Codex再起動後に `unrealMCP` として使う。
- UE Remote Executionが見えない場合は、Editor再起動またはProject Settings > Plugins > Python > Enable Remote Executionを確認する。

## Phase 1の安全ルール

- 既存C++層を優先して使う。新規C++追加は、UMG/Blueprint配線だけでは足りない場合に限定する。
- `AOnokoArcanaCardActor` と `AOnokoArcanaTableController` は手動配置を優先する。
- Pythonによるmap actor spawn経路は過去に `EXCEPTION_ACCESS_VIOLATION` を起こしているため、完成証跡に使わない。
- UE PythonはImport、Reflection、Commandlet smoke、検証スクリプトに限定する。
- `WBP_TableHUD` を作る場合は `UOnokoArcanaTableHudWidget` を親にし、既存の `BindWidgetOptional` 名をそのまま使う。
- ただし現在は、`WBP_TableHUD` 未作成でも `UOnokoArcanaTableHudWidget` のネイティブfallback HUDが起動する。
- `AOnokoArcanaPlayerController` はPIE時にTable/Card Actorをランタイム補完できる。手動配置したActorがあればそちらを優先する。
- PIE中はQA用 `StaticMeshActor` 群を隠し、簡易table surfaceとtop-down cameraをランタイム生成する。Map上のActorは削除しない。
- SaveGameの既定slotは `ONOKO_ARCANA_Readings`。既存セーブを削除しない。

## 完了証跡

- Editor上で `draw -> reveal -> note -> guide -> save -> history refresh -> reset` を通す。
- カード裏面、表面、逆位置回転、学習ガイド非表示/表示、履歴表示を目視確認する。
- 完成画面スクリーンショットを `assets/generated/reports/` または `reports/` に保存する。
