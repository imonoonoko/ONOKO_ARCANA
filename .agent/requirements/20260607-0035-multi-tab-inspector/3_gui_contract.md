# GUI Contract

## Inspector Tabs

```text
Inspector
  Tablist: カード | 学習 | 履歴

  Card panel
    選択カード
    自分の読み
    full Card Study Sheet

  Study panel
    カード学習
    Study Lens
    Recall Practice

  History panel
    履歴 actions
    backup cue
    history filter
    history list
    review note
```

## Automatic Routing

- `draw`, `reveal`, `reset`, slot select: `カード`
- `学習シート`, Study Lens sheet link, recall start/next, after-save practice: `学習`
- Study Sheet `過去の読み`, Study Lens card filter, history item/delete/clear/import error/review: `履歴`

## Copy

- Tab labels are short: `カード`, `学習`, `履歴`。
- Do not add visible explanatory text about tab mechanics.
- Settings modal copy remains unchanged.
