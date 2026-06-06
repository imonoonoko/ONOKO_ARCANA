# ONOKO ARCANA GUI Optimization Kanban

Updated: 2026-06-07

このカンバンは、タロット学習強化ロードマップを実装する時に GUI が重くなりすぎないよう、画面構造、学習導線、復習 UI、アクセシビリティ、配布時の見え方を運用カードとして管理するためのボードである。

## Lane Decision

- Active MVP lane: Web/Electron 2D tabletop.
- Design lane: visual polish, information architecture, learning UX, and asset presentation.
- Future lane: UE/3D expression after the Web/Electron learning loop is stable.

## Board Rules

- 既存の ONOKO cyber divination table の第一印象を維持する。
- 学習情報は「自分の読みを書く前」に答えとして出しすぎない。
- 新しい学習 UI は、右パネルに詰め込むだけでなく、カード別復習、比較、進捗、初回導線に分けて配置する。
- `検証済み` はスクリーンショット、smoke、visual audit、keyboard smoke、または手動確認メモがある場合だけ使う。
- UE/3D 表現は現行 v1.x の GUI 最適化をブロックしない。

## Initial Design Anchor

- Reference image: `../../assets/design/onoko-arcana-design-kanban-v1-onoko.png`.
- Original idea: ONOKO ARCANA is a cyber divination table for people who do not have physical tarot cards yet, where reading, note-taking, study-sheet reference, and review happen on the same desk.
- GUI optimization must preserve the desk/tool feeling from the reference image: dark table, electric-blue observation light, restrained gold frames, cards, study notes, and small symbolic accents.
- New learning UI should feel like cards and notebook pages placed on the table, not like a separate analytics dashboard.

## Next 1-3 Cards

| card | why now | proof needed |
| --- | --- | --- |
| GUI-FILTER-SEARCH-001 | 履歴が学習素材として増えるため、カード以外の spread/date/question/note filter が必要になる。 | Filter smoke, screenshot |
| GUI-MOBILE-REVIEW-001 | Inspector がタブ化されたため、モバイル幅でタブと復習導線を継続確認する。 | Mobile screenshot, visual audit issue 0 |
| GUI-LOCAL-PRIVACY-001 | 学習履歴、スロット練習、復習予定が増えたため、package版でも保存場所と復旧導線が読める必要がある。 | Package smoke, settings screenshot |

## GUI Optimization Kanban

| id | lane | area | status | priority | done | evidence | next | blocker | resume_condition | updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GUI-BASELINE-001 | design | UI TABLE | 検証済み | P0 | 現行の占い卓、左右パネル、履歴欄、学習レンズ、想起練習、settings、初回導線、Card Study Sheet、Slot Interpretation Drill が desktop/mobile で破綻なく表示される。 | `../../reports/onoko-arcana-web-app-celtic-20260606-203136.png`, `../../reports/onoko-arcana-first-launch-20260606-203136.png`, `../../reports/onoko-arcana-settings-20260606-203136.png`, `../../reports/ui-visual-audit-20260606-203150/report.json` | package版 settings と mobile review を追加確認する。 |  |  | 2026-06-06 |
| GUI-INSPECTOR-TABS-001 | implementation | UI TABLE | 検証済み | P0 | 右 inspector を `カード`、`学習`、`履歴` の3タブに分離し、`カード` タブでは選択カード/ノート/フル学習シートを同時に扱える。 | `../../reports/onoko-arcana-card-tab-study-sheet-20260607-0120.png`, `../../reports/ui-visual-audit-20260607-012023/report.json`, `../../reports/web-app-smoke-20260607-011915.json`, `../../reports/keyboard-focus-smoke-20260607-012201.json` | 履歴 filter 拡張時に、各タブの自動遷移と高さ配分を再確認する。 |  |  | 2026-06-07 |
| GUI-STUDY-REVIEW-001 | implementation | STUDY | 検証済み | P0 | Study Lens のカード名、既出カード、未出カード、次の観測候補から、該当カードを含む保存履歴だけに絞って復習できる。 | `../../reports/web-app-smoke-20260606-140227.json`, `../../reports/onoko-arcana-card-review-compare-20260606-1342-compare-visible.png`, `../../reports/ui-visual-audit-20260606-140228/report.json` | スプレッド別、問い別、日付別の追加 filter は後続カードで扱う。 |  |  | 2026-06-06 |
| GUI-INFO-DENSITY-001 | design | STUDY | 検証済み | P0 | Card Study Sheet、Slot Interpretation Drill、ユーザーメモ、履歴比較が、右パネル内で見出しとスクロール境界を持ち、読解を邪魔しない。 | `../../reports/ui-visual-audit-20260607-012023/report.json`, `../../reports/onoko-arcana-card-tab-study-sheet-20260607-0120.png`, `../../reports/web-app-smoke-20260607-011915.json` | 追加 filter 時も右パネルの最大高と折りたたみ順を先に決める。 |  |  | 2026-06-07 |
| GUI-CARD-STUDY-SHEET-001 | implementation | STUDY | 検証済み | P1 | 選択カードまたは Study Lens から、正位置、逆位置、象徴、よくある読み違い、振り返り問いを小さな学習シートとして開ける。 | `../../reports/web-app-smoke-20260606-203136.json`, `../../reports/ui-visual-audit-20260606-203150/report.json`, `../../reports/web-app-check-20260606-203719.json` | 歴史メモとカード系譜は後続の content fixture で扱う。 |  |  | 2026-06-06 |
| GUI-NOTE-STUDY-COMPARE-001 | implementation | STUDY | 検証済み | P1 | カード別復習中の履歴カードで、保存済みの自分の読み、学習シート要点、スロット prompt を同時に確認できる。 | `../../reports/web-app-smoke-20260607-011915.json` | 比較結果を confidence や学習メモとして残す設計は Recall Practice 後に分ける。 |  |  | 2026-06-07 |
| GUI-RECALL-PRACTICE-001 | implementation | STUDY | 検証済み | P1 | 学習シートを見る前にカードのキーワードや逆位置傾向を自分で入力し、答え合わせ後に hard/ok/easy の手応えを保存できる。 | `../../reports/web-app-smoke-20260607-011915.json`, `../../tests/fixtures/learning/learning-valid-v1.json` | スロット解釈 drill は検証済み。7日/14日 interval は fixture 追加後に扱う。 |  |  | 2026-06-07 |
| GUI-SLOT-DRILL-001 | implementation | STUDY | 検証済み | P1 | Card Study Sheet 内で、選択中のカード + スプレッド位置 + 正逆の組み合わせを自分の言葉で書き、解説と比べて hard/ok/easy を保存できる。 | `../../reports/web-app-smoke-20260607-011915.json`, `../../reports/ui-visual-audit-20260607-012023/report.json`, `../../reports/web-app-check-20260607-011909.json`, `../../tests/fixtures/learning/learning-valid-v1.json` | 後続は spread tutor と履歴 filter で、保存済みスロット練習を探しやすくする。 |  |  | 2026-06-07 |
| GUI-FIRST-LAUNCH-001 | design | POLISH | 検証済み | P1 | 初回起動時に、問いを書く、スプレッドを選ぶ、カードを引く、保存して復習する流れが迷わず見える。 | `../../reports/onoko-arcana-first-launch-20260606-194424.png`, `../../reports/web-app-smoke-20260606-194424.json`, `../../reports/ui-visual-audit-20260606-194648/report.json` | 実使用メモから文言だけを磨く。 |  |  | 2026-06-06 |
| GUI-FILTER-SEARCH-001 | implementation | READING | 未着手 | P1 | 履歴をカード、スプレッド、問い、保存日、メモ有無で絞り込み、復習対象をすぐ見つけられる。 | Filter smoke, screenshot | まずカード別 filter だけを実装し、他条件は後続に分ける。 |  |  | 2026-06-06 |
| GUI-A11Y-LEARNING-001 | implementation | A11Y | 検証済み | P1 | 学習レンズ、履歴 filter、比較 UI、Card Study Sheet、Slot Interpretation Drill、想起練習、settings がキーボードだけで操作でき、フォーカス位置が見える。 | `../../reports/keyboard-focus-smoke-20260607-012201.json`, `../../reports/web-app-smoke-20260607-011915.json` | 追加 filter 時に focus order を再検査する。 |  |  | 2026-06-07 |
| GUI-MOBILE-REVIEW-001 | design | UI TABLE | 検証済み | P1 | モバイル幅で、卓、選択カード、メモ、学習シート、履歴復習が縦に自然につながり、横スクロールが出ない。 | `../../reports/ui-visual-audit-20260607-012023/mobile-relationship-line.png`, `../../reports/ui-visual-audit-20260607-012023/report.json` | Card review filter 実装後に mobile screenshot を追加する。 |  |  | 2026-06-07 |
| GUI-PROGRESS-SIGNAL-001 | design | STUDY | 検証済み | P2 | 学習進捗は大きなダッシュボードではなく、既出数、未出カード、想起/スロット練習回数、次に復習するカードだけを静かに表示する。 | `../../reports/web-app-smoke-20260606-203136.json`, `../../reports/ui-visual-audit-20260606-203150/report.json` | 7日/14日 interval を入れる場合は fixture を先に追加する。 |  |  | 2026-06-06 |
| GUI-SETTINGS-LEARNING-001 | implementation | DATA | 検証済み | P2 | 学習データ、履歴データ、表示設定、バックアップ導線が settings 画面で分かれている。 | `../../reports/onoko-arcana-settings-20260606-203136.png`, `../../reports/web-app-smoke-20260606-203136.json`, `../../reports/onoko-arcana-learning-export-20260606-203136.json`, `../../reports/web-app-check-20260606-203719.json` | package版で settings を開いた時の保存場所説明を確認する。 |  |  | 2026-06-06 |
| GUI-LOCAL-PRIVACY-001 | implementation | DISTRIBUTION | 実装済み | P2 | 学習履歴がローカル保存であること、export/import/clear の意味、復旧方法が UI とドキュメントから分かる。 | `../../reports/onoko-arcana-settings-20260606-203136.png`, `../../reports/onoko-arcana-learning-export-20260606-203136.json`, `../../reports/electron-package-smoke-20260606-203245.json` | package版で settings 文言と保存場所説明を目視確認する。 |  |  | 2026-06-06 |
| GUI-VISUAL-REGRESSION-001 | implementation | POLISH | 検証済み | P2 | 学習 UI 追加後も desktop/mobile/celtic cross/初回起動/Card Study Sheet/Slot Interpretation Drill の代表スクリーンショットで重なり、切れ、横スクロールを検出できる。 | `../../reports/ui-visual-audit-20260606-203150/report.json`, `../../reports/ui-visual-audit-20260606-203150/mobile-relationship-line.png`, `../../reports/onoko-arcana-first-launch-20260606-203136.png`, `../../reports/onoko-arcana-settings-20260606-203136.png` | 次のGUI追加時も visual audit の全ケースを維持する。 |  |  | 2026-06-06 |
| GUI-UE3D-EXPRESSION-001 | future-ue3d | ASSETS | 後回し | P3 | Web/Electron の保存、復習、学習、配布が安定した後に 3D/UE 表現を再評価する。 | Web Electron v1.x verification summary | 再開条件を満たすまで現行 GUI 最適化には混ぜない。 |  | Web/Electron の学習 loop、history review、import/export、package smoke が検証済みになる。 | 2026-06-06 |

## Execution Notes

- `GUI-STUDY-REVIEW-001` と `GUI-NOTE-STUDY-COMPARE-001` は `docs/roadmap/TAROT_LEARNING_ENHANCEMENT_ROADMAP_2026-06-06.md` の Phase L2 と対応し、Study Lens clickthrough、カード別履歴 filter、note-vs-study-sheet 比較まで検証済み。
- `GUI-RECALL-PRACTICE-001` は Phase L3 の最小版として、キーワード想起、正/逆位置切替、答え合わせ、confidence 保存まで検証済み。学習データは `onoko-arcana:desktop:learning:v1` として履歴とは別に保存する。
- `GUI-SETTINGS-LEARNING-001` は settings modal として実装済み。履歴データ、学習データ、表示設定、保存 key を分離し、学習データ export/import/clear と compact learning panel 設定を Web smoke で検証済み。
- `GUI-FIRST-LAUNCH-001` と `GUI-PROGRESS-SIGNAL-001` は 2026-06-06 に最小実装済み。履歴 0 件時の学習導線、保存後の復習/次の問いボタン、hard/ok/easy から導出する due count と due cue を Web smoke と visual audit で検証済み。
- `GUI-INFO-DENSITY-001` と `GUI-CARD-STUDY-SHEET-001` は 2026-06-06 に検証済み。右パネルは折りたたみ sheet と内部スクロールで情報密度を制御する。
- `GUI-SLOT-DRILL-001` は 2026-06-07 に検証済み。Card Study Sheet 内で選択カード、スロット、正逆を使い、ユーザー入力後に解説表示と confidence 保存を行う。
- `GUI-INSPECTOR-TABS-001` は 2026-06-07 に検証済み。右 inspector を `カード`、`学習`、`履歴` に分け、初回導線は履歴タブ、読み中はカードタブ、学習操作は学習タブ、保存/復習操作は履歴タブへ寄せる。
- 2026-06-07 の反復チェックで `reports/web-app-smoke-20260607-001121.json` と `reports/ui-visual-audit-20260607-001202/report.json` が通過。Study Lens から卓上選択外カードを開いた時の Slot Drill disabled ケースも smoke で決定的に検証する。
- `GUI-A11Y-LEARNING-001` はフィルターや比較 UI を追加するたびに更新する。
- `GUI-UE3D-EXPRESSION-001` はアーカイブ保持であり、現行 Web/Electron v1.x の作業順には入れない。
