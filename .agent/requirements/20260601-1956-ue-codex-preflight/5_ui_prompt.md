# 5. UI Prompt

## WBP_TableHUD 作成指示

`WBP_TableHUD` は、学習と占いの両方を邪魔しない実用UIとして作る。親クラスは `UOnokoArcanaTableHudWidget`。カード自体は3D卓上の主役として扱い、HUDは入力、状態、解釈、履歴確認に集中する。

## 画面構成

- 左側または上部: 問い入力と操作ボタン。
- 中央: 3Dカード卓を見せるため、HUDで覆いすぎない。
- 右側または下部: カード名、正逆、キーワード、学習ガイド、自分の解釈。
- 履歴: Phase 1では最小表示でよい。件数、最新概要、選択詳細が読めれば合格。

## 必須Widget

親C++が `BindWidgetOptional` で拾うため、必要Widgetは以下の名前を厳密に使う。

| Widget名 | 推奨型 | 役割 |
|---|---|---|
| `QuestionTextBox` | EditableTextBox | 問い入力 |
| `StartReadingButton` | Button | 問いをSessionへ反映 |
| `DrawButton` | Button | カードを引く |
| `RevealCardButton` | Button | カード表面を公開 |
| `UserInterpretationTextBox` | MultiLineEditableTextBox | ユーザー解釈 |
| `RevealGuideButton` | Button | 学習ガイド公開 |
| `SaveReadingButton` | Button | 現在の読みを保存 |
| `RefreshHistoryButton` | Button | 保存履歴再読込 |
| `ResetButton` | Button | 現在の読みを初期化 |
| `CardTitleText` | TextBlock | カード名 |
| `OrientationText` | TextBlock | 正位置/逆位置 |
| `KeywordsText` | TextBlock | キーワード |
| `StudyFocusText` | TextBlock | 学習ガイド |
| `ErrorText` | TextBlock | エラー |
| `StateText` | TextBlock | 現在状態 |
| `HistoryCountText` | TextBlock | 履歴件数 |
| `HistoryLatestSummaryText` | TextBlock | 最新履歴概要 |
| `HistorySelectedTitleText` | TextBlock | 選択履歴タイトル |
| `HistorySelectedDetailText` | TextBlock | 選択履歴詳細 |
| `HistoryEmptyStateText` | TextBlock | 履歴なし表示 |

## UI上の注意

- 初期状態で学習ガイドは主張しすぎない。ユーザーが自分の解釈を書いてから表示する流れを守る。
- ボタンの有効/無効はC++親の `RefreshFromController()` に合わせる。
- Phase 1では装飾よりも、押した結果が読めること、保存履歴が見えることを優先する。
- テキストは日本語が折り返しても破綻しない幅を確保する。
