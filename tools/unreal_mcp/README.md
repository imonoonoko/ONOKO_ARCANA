# ONOKO_ARCANA Unreal MCP

CodexからUnreal Editorを操作するための、プロジェクト専用stdio MCPサーバー。

## 接続方式

- Codex MCP transport: stdio
- UE側: Python Script PluginのRemote Execution
- 対象: `C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject`
- Engine: `C:\Program Files\Epic Games\UE_5.7`

## UE側の前提

`Unreal/ONOKO_ARCANA/Config/DefaultEngine.ini` に以下を置く。

```ini
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
bRemoteExecution=True
RemoteExecutionMulticastGroupEndpoint=239.0.0.1:6766
RemoteExecutionMulticastBindAddress=127.0.0.1
RemoteExecutionMulticastTtl=0
```

Editorを既に起動していた場合、この設定は即時反映されないことがある。その場合はEditorを再起動するか、Project Settings > Plugins > Python > Enable Remote Executionを一度確認する。

## Codex側

`C:\Users\Humin\.codex\config.toml` に `unrealMCP` を追加済み。
現在のCodexセッションに新しいMCPツールが出ない場合は、Codexを再起動してから `/mcp` で確認する。

## ローカル検証

```powershell
python tools\unreal_mcp\test_mcp_stdio.py
python tools\unreal_mcp\test_remote_connection.py
```

`ue_status` が `node_count: 0` の場合、UE Editor側のRemote Executionがまだ動いていない。

## 公開ツール

- `ue_status`: UE Editorノード検出と設定確認
- `ue_execute_python`: UE Editor Pythonを実行
- `ue_get_editor_snapshot`: 現在のWorld/選択Actor/選択Assetの安全なJSON概要
- `ue_run_phase1_smoke`: Phase 1向けのMap/Class存在確認
- `ue_launch_editor`: ONOKO_ARCANAのUE Editor起動

`ue_execute_python` はEditor内で任意Pythonを実行できる強い権限を持つ。実行内容は `reports/unreal-mcp-audit.jsonl` に先頭500文字まで記録する。
