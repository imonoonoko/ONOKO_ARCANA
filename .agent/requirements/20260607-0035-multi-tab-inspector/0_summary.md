# ONOKO ARCANA Multi-Tab Inspector Requirements

作成日: 2026-06-07

## 背景

タロット学習強化により、右 inspector に選択カード、ノート、Card Study Sheet、Slot Drill、Study Lens、Recall Practice、履歴、復習ノートが集中した。現行の思想である「同じ占い卓で読む、書く、比べる、復習する」は維持しつつ、作業面をタブで分けて情報密度を下げる。

## 決定

右 inspector を `カード`、`学習`、`履歴` の3タブに分ける。

- `カード`: 選択カード、自分の読み、同じカードのフル Card Study Sheet。
- `学習`: Card Study Sheet、Slot Drill、Study Lens、Recall Practice。
- `履歴`: 履歴操作、backup cue、履歴 filter、履歴一覧、復習ノート。

## 完了条件

- タブは常時見える。
- 既存の reading/study/history/settings flow が smoke で通る。
- 視覚監査で desktop/mobile の重なり、横スクロール、パネル clipping が出ない。
- 新しい UI 契約と証跡を Kanban と completion report に残す。
