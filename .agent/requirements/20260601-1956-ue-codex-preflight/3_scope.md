# 3. Scope

## In Scope

- Phase 1 UE Editor配線前の前提整理。
- `WBP_TableHUD` のWidget名、親クラス、ボタン/テキスト責務の固定。
- `AOnokoArcanaCardActor`、`AOnokoArcanaTableController`、`AOnokoArcanaPlayerController`、`AOnokoArcanaGameMode` の接続順整理。
- Codex用の短いプロジェクト入口 `AGENTS.md`。
- プリフライト検査スクリプトと結果JSON。
- 2026年6月1日時点で参照できる公式情報に基づくUE/Codexベストプラクティス。

## Out of Scope

- 新規カード生成。
- Major Arcana V5の再QA。
- Minor Arcana制作。
- UE Python actor spawn crashの根本調査。
- CommonUIへの全面移行。
- 公式UMG MVVM Pluginへの設計変更。
- Steam/配布/課金/クラウド連携。

## 前提

- Unreal Engine 5.7は `<UE_5.7>` に存在する。
- `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject` はEngineAssociation `5.7`。
- `PythonScriptPlugin` と `EditorScriptingUtilities` はEditor targetで有効。
- `L_Phase1_OneCard_Table`、Phase 1 masked material、V5Full Texture2D群はContent内に存在する。
- このワークツリーはgit repositoryではないため、変更管理はファイル単位で慎重に行う。
