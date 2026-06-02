# Unreal Engine Study Notes for ONOKO_ARCANA

Date: 2026-06-01

## 学習対象

ONOKO_ARCANAの直近実装に必要なUE領域を、Codex連携前提で整理した。

## 重要結論

- CodexからUEを触る最短経路は、MCP stdioサーバーからUE Python Remote Executionへ橋渡しする方式。
- UE PythonはEditor自動化専用として扱う。ゲーム実行中のロジックはC++、Blueprint、UMG、SaveGameで完結させる。
- Phase 1の完成証跡は、PythonでMapを書き換えるのではなく、Editor/PIE上の実操作とC++ runtime fallbackで取る。
- Remote Controlは将来の外部Web UI、タブレット操作、専用操作パネルには有効だが、今回の最小Codex接続では過剰。

## 操作領域別メモ

### Editor Automation

UEのEditor自動化は大きく3経路に分かれる。

1. Editor Python: Asset、Level、Actor、Project設定などをPython APIから扱う。Codex連携の主経路。
2. Editor Utility Blueprint/Widget: UE内で人間が押す専用ツールを作る。将来的な制作支援UI向け。
3. Commandlet / `UnrealEditor-Cmd.exe`: CIや一回限りの検証向け。UIを開かずに走らせやすい。

ONOKO_ARCANAでは、状態確認はMCPの `ue_get_editor_snapshot`、バッチ検証はCommandlet、実装の最終確認はPIE目視に分ける。

### Level / Actor

Phase 1では既存Map `L_Phase1_OneCard_Table` を起点にする。Map上のQA用StaticMeshActorは消さず、PIE中のみ非表示にする現在のC++方針を維持する。これにより検証用素材を破壊せず、プレイ時の見た目だけ整えられる。

Actorは「Mapに保存される設計用Actor」と「PIE中だけ生成されるruntime補助Actor」を分ける。今回のTable/Card/Camera/Light runtime補完は後者であり、Map資産を汚さずにプレイ可能性を確保するための措置。

### GameMode / PlayerController

`OnokoArcanaGameMode` と `OnokoArcanaPlayerController` がPhase 1の入口。PlayerControllerがHUD、TableController、CardActor、Camera、Lightをruntime補完できるため、Blueprint/UMG未完成でもプレイ可能な最低線を維持できる。

GameModeはLevel読み込み後にそのプレイセッションのルール役として立ち上がる。PlayerControllerは人間プレイヤーの入力、HUD、Camera視点に近いため、ONOKO_ARCANAの一人用卓上UIではPlayerController中心の配線が自然。

### UMG

現在は `UOnokoArcanaTableHudWidget` のnative fallbackが機能している。今後 `WBP_TableHUD` を作る場合は、C++親クラスを維持し、`BindWidgetOptional` 名を変えない。UMGを作ってもC++ fallbackを削らないことで、Widget破損時の復旧性を残す。

UIは、C++で状態とイベントを保持し、UMG/Blueprintは見た目と入力導線に寄せる。これにより、見た目の試行錯誤がSaveGameやDraw/Revealロジックに波及しにくい。

### SaveGame

既定slotは `ONOKO_ARCANA_Readings`。既存セーブを削除せず、履歴の読み書きのみ検証する。Phase 2以降で履歴UIを拡張する場合も、slot互換性を優先する。

SaveGameは複数slotや複数SaveGame classを扱えるが、Phase 1ではslotを増やさない。保存形式の変更が必要になった場合は、読み込み時の移行処理を先に決めてから実装する。

### Build / Live Coding

UE EditorのLive Codingが有効な状態では通常ビルドが止まることがある。C++ビルド確認はEditor終了後、またはLive Codingを無効化してから実行する。これはコンパイル失敗ではなくUE側の保護動作として扱う。

Live Codingは小さなC++反復には有効だが、UCLASS/USTRUCTの大きな構造変更やコンストラクタ初期値変更は既存instanceに反映されないことがある。Phase 1のような基盤配線では、最終確認に通常ビルドを挟む。

### CommonUI

現在のHUDはnative `UUserWidget` fallbackのため、CommonUI警告はPhase 1のブロッカーではない。将来CommonUIへ寄せる場合はGameViewportClientをCommonUI対応にする必要がある。

### Remote Control

Remote ControlはUE内のHTTP/WebSocketサーバーを外部アプリから叩く設計で、専用Web UIやタブレット操作には向く。一方、Codexのローカル自動化ではMCP stdioからPython Remote Executionへ渡すほうが、公開ポートやブラウザUIを増やさずに済む。

## Codex連携ベストプラクティス

- まず `ue_status` で接続状態だけ確認する。
- 状態把握は `ue_get_editor_snapshot` を優先し、任意Python実行を減らす。
- 変更系Pythonは、実行前に対象Asset/Map/Actorを明示し、実行後にsnapshotを取る。
- MapやAsset保存を伴う操作は、ユーザーのUE画面確認後に限定する。
- UEがクラッシュした経路は完成証跡に使わない。

## 追加で学習すべきUE領域

- Enhanced Input: 今後キーボード/マウス/ゲームパッドを正式に扱う時点で確認する。
- Asset Registry / Data Assets: 大アルカナ/小アルカナのカード定義をAsset化する段階で確認する。
- Slate/UMG最適化: 履歴リスト、カード一覧、解説パネルが増えた時点で確認する。
- Packaging: Phase 1では不要。配布ビルドを作る段階でSaveGame場所、CommonUI、起動Mapを再確認する。

## 参考にした一次情報

- Epic Developer Community: Scripting the Unreal Editor Using Python: https://dev.epicgames.com/documentation/unreal-engine/scripting-the-unreal-editor-using-python
- Epic Developer Community: Remote Control for Unreal Engine: https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-for-unreal-engine
- Epic Developer Community: Gameplay Framework: https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine
- Epic Developer Community: Creating User Interfaces: https://dev.epicgames.com/documentation/unreal-engine/creating-user-interfaces-with-umg-and-slate-in-unreal-engine
- Epic Developer Community: Saving and Loading Your Game: https://dev.epicgames.com/documentation/unreal-engine/saving-and-loading-your-game-in-unreal-engine
- Epic Developer Community: Live Coding: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-live-coding-to-recompile-unreal-engine-applications-at-runtime
- Model Context Protocol: Tools specification: https://modelcontextprotocol.io/specification/2024-11-05/server/tools
- OpenAI Developers: Codex configuration reference: https://developers.openai.com/codex/config-reference
