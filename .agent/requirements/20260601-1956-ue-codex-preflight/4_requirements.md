# 4. Requirements

## Functional Requirements

### FR-1: Codex再開入口

Codexは、作業開始時に `AGENTS.md` と `docs/implementation/PHASE1_UE_CODEX_PREFLIGHT_2026-06-01.md` を読めば、Phase 1の次作業、禁止経路、検証基準を把握できなければならない。

### FR-2: UE接続前プリフライト

`python scripts/check_phase1_preflight.py` は、少なくとも以下を確認しなければならない。

- UE 5.7 project fileとEngine実体。
- 必要Pluginの有効化。
- Phase 1/Phase 2 C++ source files。
- V5 deck manifestの22枚構成と全カード採用状態。
- V5Full texture uasset 23件。
- Phase 1 mapとmasked material。
- Phase 1/2 smoke test result JSONの `ok: true`。
- 既存docsと作業入口。

### FR-3: UMG配線契約

`WBP_TableHUD` は `UOnokoArcanaTableHudWidget` を親にし、以下のWidget名を必要に応じて同名で配置する。

- `QuestionTextBox`
- `StartReadingButton`
- `DrawButton`
- `RevealCardButton`
- `UserInterpretationTextBox`
- `RevealGuideButton`
- `SaveReadingButton`
- `RefreshHistoryButton`
- `ResetButton`
- `CardTitleText`
- `OrientationText`
- `KeywordsText`
- `StudyFocusText`
- `ErrorText`
- `StateText`
- `HistoryCountText`
- `HistoryLatestSummaryText`
- `HistorySelectedTitleText`
- `HistorySelectedDetailText`
- `HistoryEmptyStateText`

### FR-4: Editor配線手順

次工程では、`L_Phase1_OneCard_Table` に `AOnokoArcanaCardActor` と `AOnokoArcanaTableController` を手動配置し、`ReadingCardActor` を設定する。`AOnokoArcanaPlayerController` はHUD Classへ `WBP_TableHUD` を指定し、TableController取得または明示設定でHUDとControllerを接続する。

### FR-5: 完了フロー

実画面では、次の順序を通せなければならない。

1. 問いを入力する。
2. 読みを開始する。
3. カードを引く。
4. まず裏面が表示される。
5. カードを公開する。
6. 表面、正逆、キーワードが表示される。
7. 自分の解釈を書く。
8. 学習ガイドを表示する。
9. 保存する。
10. 履歴を更新する。
11. 最新履歴が表示される。
12. リセットする。

## Non-Functional Requirements

- NFR-1: UE PythonはEditor検証とCommandlet smokeに限定し、map actor spawn自動生成を完成証跡にしない。
- NFR-2: 既存C++層を壊さず、Blueprint/UMGで完結できる範囲に留める。
- NFR-3: 既存SaveGame slotを削除しない。
- NFR-4: 公式情報と現行repoの事実が食い違う場合は、repoの実装を優先し、公式情報は判断補助に使う。

## Acceptance Criteria

- `python scripts/check_phase1_preflight.py` が失敗なしで終了し、`reports/phase1-preflight-check-*.json` を出力する。
- `AGENTS.md` に次回作業入口、UE環境、禁止経路、完了証跡が記載されている。
- `docs/implementation/PHASE1_UE_CODEX_PREFLIGHT_2026-06-01.md` に、公式参照、接続手順、検証順、失敗時の切り分けが記載されている。
- 次工程の担当者が、追加質問なしでUE Editorを開き、手動配線に着手できる。
