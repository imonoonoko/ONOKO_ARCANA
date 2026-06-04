# 6. Implementation Brief

## Skill Stack

- 使用: `$define-requirements`
  - 理由: Phase 1実装前の要件、スコープ、受け入れ条件、作業順を固定するため。
- 使用: `$orchestrate-skills`
  - 理由: Unreal特化Skillの有無と、Codex/Brain側の再開入口を確認するため。
- 採用しない: Web frontend/browser系Skill
  - 理由: 今回はUE Editor/UMG配線であり、localhostブラウザ検証ではないため。
- 採用しない: CommonUI移行Skill相当
  - 理由: Pluginは有効だが、現行HUDは `UUserWidget` 親で実装済み。Phase 1では不要な設計変更を避ける。

## 公式情報からの実務判断

- UE PythonはEditor自動化に有用だが、現行プロジェクトではmap actor spawn経路がクラッシュ済み。素材Import、Reflection、Commandlet smokeに限定する。
- UMGはWidget BlueprintとC++親クラスの組み合わせで進める。現行の `BindWidgetOptional` 契約を尊重する。
- SaveGameは既存 `UOnokoArcanaReadingSaveLibrary` と `ONOKO_ARCANA_Readings` slotを使う。
- CodexのAGENTSは短い常設入口として使い、長い計画はdocsとrequirementsに分離する。

## 作業前コマンド

PowerShell:

```powershell
cd <repo>
python scripts/check_phase1_preflight.py
```

UE Editor起動:

```powershell
& "<UE_5.7>\Engine\Binaries\Win64\UnrealEditor.exe" "<repo>\Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject"
```

Commandlet smokeの再実行が必要な場合:

```powershell
& "<UE_5.7>\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "<repo>\Unreal\ONOKO_ARCANA\ONOKO_ARCANA.uproject" -run=pythonscript -script="<repo>\Unreal\ONOKO_ARCANA\Scripts\test_phase1_hud_reflection_surface.py" -Unattended -NullRHI
```

## Editor内手順

1. `L_Phase1_OneCard_Table` を開く。
2. `AOnokoArcanaCardActor` を1体配置する。
3. `AOnokoArcanaTableController` を1体配置する。
4. TableControllerの `ReadingCardActor` に配置済みCardActorを指定する。
5. `WBP_TableHUD` を作成し、親を `UOnokoArcanaTableHudWidget` にする。
6. `WBP_TableHUD` に必要Widget名を配置する。
7. PlayerControllerまたはGameMode側でHUD Classに `WBP_TableHUD` を指定する。
8. Play In Editorで `draw -> reveal -> note -> guide -> save -> history refresh -> reset` を確認する。
9. スクリーンショットを保存する。

## Stop Conditions

- Editor起動時にproject loadが失敗する。
- `WBP_TableHUD` の親クラスとして `UOnokoArcanaTableHudWidget` が選べない。
- `AOnokoArcanaTableController` から `ReadingCardActor` を設定できない。
- `SaveCurrentReading()` が失敗し、`LastErrorMessage` が空でない。
- Python actor spawn crashを再現した場合は、その経路を中止し、手動Editor配線へ戻る。
