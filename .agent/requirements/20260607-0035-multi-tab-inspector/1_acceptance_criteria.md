# Acceptance Criteria

## Functional

- 初期表示は `カード` タブで、めくったカード、ノート、同じカードのフル学習シートを操作できる。
- `学習` タブでは選択カードの学習シート、スロット練習、学習レンズ、想起練習を操作できる。
- `履歴` タブでは設定、読込、書出、消去、履歴一覧、復習ノート、カード別履歴 filter を操作できる。
- 学習シートを開く、想起練習を開始する、Study Lens からカードを選ぶ操作は `学習` タブに移動する。
- カード別履歴 filter、履歴復元、履歴削除、保存後の復習ノート確認は `履歴` タブに移動する。
- Settings modal は既存通り inspector 内の履歴操作から開ける。

## Accessibility

- タブリストは `role="tablist"`、各タブは `role="tab"`、各面は `role="tabpanel"` を持つ。
- `aria-selected`、`aria-controls`、`aria-labelledby`、`tabindex` が状態に合わせて更新される。
- ArrowLeft / ArrowRight / Home / End でタブ移動できる。
- フォーカスリングは既存 button focus と同じ青で見える。

## Visual

- ONOKO の dark table / blue observation / restrained gold frame を維持する。
- 右 inspector の中で一度に見える高密度面は1タブ分だけにする。
- desktop で body scroll と inspector clipping を出さない。
- mobile で横スクロールを出さず、タブは押しやすい高さを保つ。

## Data

- `onoko-arcana:desktop:history:v1` は変更しない。
- `onoko-arcana:desktop:learning:v1` は変更しない。
- 新しいタブ状態は session UI state とし、localStorage 永続化はしない。
