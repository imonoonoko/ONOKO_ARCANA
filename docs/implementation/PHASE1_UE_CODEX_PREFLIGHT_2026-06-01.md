# Phase 1 UE / Codex Preflight

作成日: 2026-06-01  
対象: `C:\ONOKO_PROJECT\ONOKO_ARCANA`

## 結論

次に進めるべき作業は、`L_Phase1_OneCard_Table` 上でのUE Editor/Blueprint/UMG配線である。C++ Runtime、Deck、OneCard Session、ViewModel、HUD親、SaveGame、History ViewModelはすでに存在し、Commandlet smoke結果も残っている。

2026-06-01の実作業で、`WBP_TableHUD` が未作成でもPIEで検証を始められるネイティブfallback HUDと、Table/Card Actorのランタイム自動補完を追加した。手動配置したActorがある場合はそれを優先し、未配置の場合だけ `AOnokoArcanaPlayerController` がPhase 1用の最小Actorを生成する。さらに、PIE中だけ既存QAカードGridを隠し、簡易table surfaceとtop-down cameraを自動生成する。

Pythonによるmap actor spawnは過去に `EXCEPTION_ACCESS_VIOLATION` を起こしているため、今回の完成証跡には使わない。Pythonは、Import、Reflection、既存test smoke、プリフライト確認に限定する。

## 2026-06-01時点の公式参照

- Epic Games: [Scripting the Unreal Editor Using Python](https://dev.epicgames.com/documentation/unreal-engine/scripting-the-unreal-editor-using-python)
- Epic Games: [UMG UI Designer](https://dev.epicgames.com/documentation/unreal-engine/umg-ui-designer-in-unreal-engine)
- Epic Games: [Saving and Loading Your Game](https://dev.epicgames.com/documentation/unreal-engine/saving-and-loading-your-game-in-unreal-engine)
- Epic Games: [Common UI Plugin](https://dev.epicgames.com/documentation/unreal-engine/common-ui-plugin-for-advanced-user-interfaces-in-unreal-engine)
- OpenAI: [AGENTS.md Guide](https://developers.openai.com/codex/guides/agents-md)

## ローカル確認済み前提

| 項目 | 状態 |
|---|---|
| UE Project | `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject` |
| EngineAssociation | `5.7` |
| Engine path | `C:\Program Files\Epic Games\UE_5.7` |
| PythonScriptPlugin | enabled, Editor target |
| EditorScriptingUtilities | enabled, Editor target |
| CommonUI | enabled |
| Phase 1 map | `Content/ONOKOArcana/Maps/L_Phase1_OneCard_Table.umap` |
| Phase 1 card material | `M_Phase1_CardMasked_TextureParam.uasset` |
| V5Full Texture2D | Major 22 + backがContent内に存在 |
| Deck manifest | `data/major-arcana-v5-deck.json` |
| Widget parent | `UOnokoArcanaTableHudWidget` |
| Save slot | `ONOKO_ARCANA_Readings` |
| Native fallback HUD | `UOnokoArcanaTableHudWidget` がWidgetTreeを自前構築 |
| Runtime actor fallback | `AOnokoArcanaPlayerController::EnsurePhase1RuntimeActors()` |
| Runtime visual cleanup | QA `StaticMeshActor` をPIE中だけ非表示、table surfaceとcameraを自動生成 |

## Codex連携

今回、rootに `AGENTS.md` を追加した。以後のCodexは、まずこのファイルを読み、次に以下を読む。

1. `plan.md`
2. `docs/implementation/PHASE1_ONE_CARD_TABLE_WIRING.md`
3. `docs/implementation/PHASE1_UE_CODEX_PREFLIGHT_2026-06-01.md`
4. `.agent/requirements/20260601-1956-ue-codex-preflight/`

これで、長い研究計画、実装手順、短い運用ルールを分離できる。

## 作業前プリフライト

PowerShell:

```powershell
cd C:\ONOKO_PROJECT\ONOKO_ARCANA
python scripts/check_phase1_preflight.py
```

成功時は `reports/phase1-preflight-check-*.json` が生成される。失敗が出た場合は、UE Editorを開く前に該当ファイルやPlugin設定を修正する。

## UE Editor接続手順

1. Unreal Editorを起動する。

```powershell
& "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe" "C:\ONOKO_PROJECT\ONOKO_ARCANA\Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject"
```

2. `L_Phase1_OneCard_Table` を開く。
3. `AOnokoArcanaCardActor` を1体配置する。
4. `AOnokoArcanaTableController` を1体配置する。
5. TableControllerのDetailsで `ReadingCardActor` にCardActorを指定する。
6. まずはPIEでネイティブfallback HUDを使って操作する。
7. 見た目を整える段階で `WBP_TableHUD` を作成し、Parent Classを `UOnokoArcanaTableHudWidget` にする。
8. `QuestionTextBox`、`DrawButton`、`RevealCardButton`、`UserInterpretationTextBox`、`RevealGuideButton`、`SaveReadingButton`、`RefreshHistoryButton`、`ResetButton`、各TextBlockを同名で配置する。
9. `AOnokoArcanaPlayerController` のHUD classに `WBP_TableHUD` を指定する。

## 操作検証順

1. 問いを入力する。
2. Start Readingを押す。
3. Drawを押す。
4. カード裏面が表示されることを確認する。
5. Reveal Cardを押す。
6. 表面、正逆、キーワードが表示されることを確認する。
7. 自分の解釈を書く。
8. Reveal Guideを押す。
9. 学習ガイドが表示されることを確認する。
10. Saveを押す。
11. Refresh Historyを押す。
12. 履歴件数、最新概要、選択詳細が表示されることを確認する。
13. Resetを押し、状態が初期化されることを確認する。

## ベストプラクティス

- C++は既存APIの接続に留める。Phase 1では新規抽象化より実画面証明を優先する。
- Blueprint UIの前に、ネイティブfallback HUDで `draw -> reveal -> note -> guide -> save -> history` の機能証明を先に済ませる。
- Widget名はC++の `BindWidgetOptional` 名と完全一致させる。
- `StudyFocusText` はユーザー解釈前に主張しすぎない。学習体験の順序を守る。
- SaveGame検証では本番slotを削除しない。Commandlet smoke用slotと区別する。
- CommonUIは有効だが、Phase 1では既存 `UUserWidget` 親のHUDを完成させる。ゲームパッド、複数メニュー層、入力抽象化が必要になった段階でCommonUI化を検討する。
- UE Pythonは公式にEditor自動化向けとして扱い、今回のクラッシュ済みActor spawn経路に戻らない。
- 完了報告には、スクリーンショット、プリフライト結果、PIE操作結果、SaveGame/Historyの可否を含める。

## 失敗時の切り分け

| 症状 | まず見る場所 | 対応 |
|---|---|---|
| HUD親クラスが選べない | C++ build / generated binaries | Editor targetをbuildし直す |
| ボタンを押しても反応しない | Widget名 / parent class | `UOnokoArcanaTableHudWidget` 親と同名Widgetを確認 |
| カードが表示されない | TableController `ReadingCardActor` | DetailsでActor参照を再設定 |
| HUDが出ない | `AOnokoArcanaPlayerController` defaults | `TableHudWidgetClass` が `UOnokoArcanaTableHudWidget` か確認 |
| 裏面だけ出る | Reveal flow / CardActor texture | `RevealCard()` 後のViewModel状態を確認 |
| Save失敗 | `LastErrorMessage` / slot名 | `ONOKO_ARCANA_Readings` とSaveGame libraryを確認 |
| Historyが空 | `RefreshReadingHistory()` | Save後にRefreshし、test slotと本番slotを混同していないか確認 |
| PythonでEditorが落ちる | map actor spawn経路 | その経路を中止し、手動Editor配線に戻る |

## 次の実作業

このプリフライトを通したあと、UE Editorを開いて `WBP_TableHUD` と2つのActorを接続する。Native fallback HUDでの実画面縦断フローと履歴保存は2026-06-01に確認済み。次工程では、機能証跡用fallbackから完成用Blueprint/UMG HUDと整理済みmapへ移行する。
