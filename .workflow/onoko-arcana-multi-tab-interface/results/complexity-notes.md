# Complexity Notes

作成日: 2026-06-07

## Risk

`web-app/src/app.js` は単一ファイル内に reading、history、learning、settings の状態と描画を持つ。今回の目的は情報構造の整理であり、同時に大きな分割を行うと regression risk が増える。

## Constraint

- 既存 render 関数を維持する。
- 新規追加は inspector tab state、tab renderer、tab event binding に限定する。
- Hidden panel による Playwright click failure を避けるため、smoke は操作前に対象タブを開く。

## Follow-Up

タブ化が安定した後、`renderHistory` と learning-related rendering を小モジュールへ分割する余地がある。ただし今回の完了条件には含めない。

## Scan Result

`complexity-optimizer/scripts/analyze_complexity.py web-app --format markdown` は `web-app/src/app.js` の既存単一ファイル構造に多数の nested loop / sort 警告を出した。今回追加した `inspectorTabIds` 周辺も固定3件の走査として検出されたが、実行時の性能リスクは低い。次の大きな機能追加前に、履歴/学習/settings rendering の分割を検討する。
