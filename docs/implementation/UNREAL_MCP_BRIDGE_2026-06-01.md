# Unreal MCP Bridge 2026-06-01

## 目的

ONOKO_ARCANAのPhase 1以降で、CodexがUnreal Editorの状態確認、Actor/Asset検査、軽量なEditor Python自動化を安全に行えるようにする。

## 採用方式

Codex側はstdio MCPサーバー、UE側はPython Script PluginのRemote Executionを採用した。Epic公式ドキュメント上、PythonはEditor自動化・Asset制作パイプライン向けであり、PIEやパッケージ済みゲーム内のゲームプレイスクリプト用途ではない。この性質は、今回の「EditorをCodexから補助操作する」用途に合っている。

Remote Control APIも候補だが、WebSocket/HTTPサーバーをUE内に立てる外部アプリ連携向けであり、今回の最小要件ではPython Remote Executionのほうが小さく閉じる。

## 作成物

- `tools/unreal_mcp/server.py`
- `tools/unreal_mcp/ue_remote.py`
- `tools/unreal_mcp/test_mcp_stdio.py`
- `tools/unreal_mcp/test_remote_connection.py`
- `tools/unreal_mcp/README.md`

## Codex設定

`C:\Users\Humin\.codex\config.toml` に以下のMCPサーバーを追加した。

```toml
[mcp_servers.unrealMCP]
command = 'C:\Users\Humin\AppData\Local\Programs\Python\Python312\python.exe'
args = ['C:\ONOKO_PROJECT\ONOKO_ARCANA\tools\unreal_mcp\server.py']
enabled = true
startup_timeout_sec = 30

[mcp_servers.unrealMCP.env]
ONOKO_UNREAL_ENGINE = 'C:\Program Files\Epic Games\UE_5.7'
ONOKO_UNREAL_PROJECT = 'C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject'
```

既存Codexプロセスは起動時にMCP設定を読むため、現在のセッションで即座にツールが出ない場合はCodexの再起動が必要。

## UE設定

`Unreal/ONOKO_ARCANA/Config/DefaultEngine.ini` にPython Remote Execution設定を追加した。

```ini
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
bRemoteExecution=True
RemoteExecutionMulticastGroupEndpoint=239.0.0.1:6766
RemoteExecutionMulticastBindAddress=127.0.0.1
RemoteExecutionMulticastTtl=0
```

この設定は `UPythonScriptPluginSettings` が `config=Engine` として定義している値である。Editorが既に起動している場合は反映されないことがあるため、Editor再起動またはProject Settings上での確認が必要。

## ツール設計

| MCP tool | 用途 | 破壊性 |
|---|---|---|
| `ue_status` | UE Remote Executionノード検出 | なし |
| `ue_get_editor_snapshot` | 現在World、選択Actor、選択AssetのJSON概要 | なし |
| `ue_run_phase1_smoke` | Phase 1 Map/Class存在確認 | なし |
| `ue_execute_python` | Editor Python任意実行 | 高い |
| `ue_launch_editor` | UE Editor起動 | 低い |

`ue_execute_python` は任意PythonをEditorプロセス内で実行できる。Asset削除、Level変更、保存なども可能なため、実行前に目的と対象を明確にする。MCPサーバーは実行プレビューを `reports/unreal-mcp-audit.jsonl` に保存する。

## 2026-06-01時点のUE操作学習ノート

### Editor Python

- Python Script Pluginをプロジェクトごとに有効化する必要がある。
- Editor Scripting Utilitiesは一般的なEditor作業の簡易APIを提供するため併用が望ましい。
- PythonはEditor専用の自動化手段で、PIE、Standalone、Cooked Runtimeのゲームプレイロジックには使わない。
- コマンドラインからは `UnrealEditor-Cmd.exe <uproject> -ExecutePythonScript=<script>` または `-run=pythonscript -script=...` が使える。
- Editor起動時にProject SettingsのStartup Scriptsを実行できるが、常駐フックはトラブル時の切り分けを難しくするため、ONOKO_ARCANAでは必要最小限に留める。

### Remote Control

- UE内にWebサーバーを立て、HTTP/WebSocket経由でBlueprint/Python相当の関数呼び出しやプロパティ操作を行う仕組み。
- カスタムWeb UIや外部端末からの遠隔操作には有効。
- 今回のCodex接続ではMCP stdioとUE Python Remote Executionのほうがネットワーク面を小さくできる。

### ONOKO_ARCANAでの使い分け

- 安全な既定: `ue_status`、`ue_get_editor_snapshot`、`ue_run_phase1_smoke`
- 実装補助: C++/Config編集、Commandlet smoke、Editor上の目視確認
- 注意して使う: `ue_execute_python` によるActor生成、Asset保存、Level保存
- 避ける: Pythonでの大量Actor spawnを完成証跡にすること。過去にこの経路でEditorクラッシュがあったため、Phase 1の完成証跡はPIEの目視操作を優先する。

## 次の運用

1. UE Editorを再起動する。
2. Codexを再起動してMCP設定を再読込する。
3. Codex側で `/mcp` を確認し、`unrealMCP` が見えることを確認する。
4. `ue_status` で `node_count >= 1` を確認する。
5. `ue_get_editor_snapshot`、`ue_run_phase1_smoke` を実行してPhase 1作業に入る。

## 参照した一次情報

- Epic: Scripting the Unreal Editor Using Python: https://dev.epicgames.com/documentation/unreal-engine/scripting-the-unreal-editor-using-python
- Epic: Remote Control for Unreal Engine: https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-for-unreal-engine
- Epic: Gameplay Framework: https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine
- Epic: Creating User Interfaces: https://dev.epicgames.com/documentation/unreal-engine/creating-user-interfaces-with-umg-and-slate-in-unreal-engine
- Epic: Saving and Loading Your Game: https://dev.epicgames.com/documentation/unreal-engine/saving-and-loading-your-game-in-unreal-engine
- Epic: Live Coding: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-live-coding-to-recompile-unreal-engine-applications-at-runtime
- Model Context Protocol: Tools: https://modelcontextprotocol.io/specification/2024-11-05/server/tools
- OpenAI Developers: Codex Config Reference: https://developers.openai.com/codex/config-reference
