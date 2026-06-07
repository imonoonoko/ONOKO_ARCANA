# ONOKO ARCANA 実装カンバン

Updated: 2026-06-07

この文書は、ONOKO ARCANA の現行 Web/Electron MVP を前に進めるための実装カンバンである。Unreal 関連の成果は履歴として保持するが、v1.x の実装対象からは完全に外す。最短 MVP は `web-app/index.html` と Electron shell で「スプレッド選択、ドロー、順番めくり、解釈メモ、学習シート参照、履歴保存、履歴復習」を安定させることとする。

学習強化の詳細ロードマップは `docs/roadmap/TAROT_LEARNING_ENHANCEMENT_ROADMAP_2026-06-06.md` を参照する。Study Lens からつながるカード別復習filter、スプレッドfilter、メモ有無filter、note-vs-study-sheet 比較、Card Study Sheet、Recall Practice、Slot Interpretation Drill、learning state を扱う settings、初回導線、保存後アクション、最小 due card queue は検証済みである。Release後のsupport hardeningとして、Settings内の最新版Release/Security/License/backup導線、Electron外部リンクallowlist、installer/package smokeの固定も完了済みで、次の推奨実装は clean Windows manual installer smoke と、質問/日付filterを追加するかのUI密度判断である。

学習強化アップデート時の GUI 最適化は `docs/design/GUI_OPTIMIZATION_KANBAN_2026-06-06.md` を参照する。実装を進める時は、カード別復習 filter と同時に情報密度、モバイル表示、キーボード操作の証跡を残す。

## ステータス

| Status | 意味 |
|---|---|
| Verified | 実装済みで、関連チェックとスモークが通っている |
| Implemented | 実装済みだが、追加検証または改善余地がある |
| Active | 次に進める実装対象 |
| Backlog | 後続タスク |
| Hold | 現時点では保留 |
| Archived | 現行ロードマップ外。証跡だけ保持する |

## 現在のベースライン

| 項目 | 現在 |
|---|---|
| Main app | `web-app/index.html` |
| Runtime | 直接 open 可能な HTML/CSS/JS |
| Runtime direction | Web/Electron only |
| Desktop shell | `web-app/electron/main.cjs` |
| Local package | `dist/onoko-arcana-local/` from `scripts/package_electron_local.cjs` |
| Cards | V5 大アルカナ 22 枚 + 裏面 1 枚 |
| Spreads | `one_card`, `three_card_past_present_future`, `five_card_cross`, `seven_card_horseshoe`, `celtic_cross`, `relationship_line` |
| Persistence | Browser `localStorage` |
| Export / Import | Saved readings JSON export and import |
| Latest static check | `reports/web-app-check-20260607-061238.json` |
| Latest visual audit | `reports/ui-visual-audit-20260607-061249/report.json` |
| Latest web smoke | `reports/web-app-smoke-20260607-061029.json` |
| Latest electron smoke | `reports/electron-app-smoke-20260607-061249.json` |
| Latest package smoke | `reports/electron-package-smoke-20260607-061337.json` |
| Latest installer smoke | `reports/onoko-arcana-installer-smoke-20260607-052003.json` |
| Latest keyboard smoke | `reports/keyboard-focus-smoke-20260607-051742.json` |
| Latest CI | `27072878818` / `9a4b0420dfc9c31862d51618bd63e628b1967a6c` |

## 検証コマンド

```powershell
python scripts/check_web_app.py
```

```powershell
cd web-app
npm run smoke:web
```

```powershell
cd web-app
npm run smoke:electron
```

```powershell
cd web-app
npm run package:local
```

```powershell
cd web-app
npm run smoke:package
```

```powershell
cd web-app
npm run package:installer
```

```powershell
cd web-app
npm run smoke:installer
```

## MVP CORE

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Web app entry | Verified | P0 | `web-app/index.html` が直接起動できる | 変更時は static check と smoke を通す | `web-app-check` |
| Deck load | Verified | P0 | V5 カード 23 assets を参照 | Deck schema を変える時だけ manifest check を拡張 | Static check |
| Spread selection | Verified | P0 | 6 spread を選択可能 | 選択維持と履歴復元時の扱いを検討 | Web smoke |
| Draw / reveal | Verified | P0 | ドロー、順番 reveal、選択カード表示が成立 | reveal animation は後回し。状態の安定を優先 | Web smoke |
| User note with study sheet | Verified | P0 | `カード` タブで自分の読みを書きながら、同じ選択カードのフル学習シートを参照できる | 学習シートの高さ配分を主要UI変更時に再監査する | `reports/web-app-smoke-20260607-011915.json`, `reports/onoko-arcana-card-tab-study-sheet-20260607-0120.png` |
| Save reading | Verified | P0 | localStorage に保存 | 保存失敗時のエラー表示を追加検討 | Web smoke |
| History display | Verified | P0 | 右パネルで保存済みリーディング、復習ノート、カード/スプレッド/メモ有無filterを表示 | 質問/日付filterはUI密度を見て別スライス判断 | `reports/web-app-smoke-20260607-061029.json` |

## SPREAD RUNTIME

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| One card | Verified | P0 | 実行可能 | Regression only | Smoke |
| Three card | Verified | P0 | 実行可能 | Regression only | Smoke |
| Five card cross | Verified | P0 | 実行可能、視覚監査済み | 低解像度追加確認 | Visual audit |
| Seven horseshoe | Verified | P0 | 実行可能、視覚監査済み | 低解像度追加確認 | Visual audit |
| Celtic cross | Verified | P0 | 実行可能、2D向けに交差を分離 | 伝統配置との差分説明を必要なら追加 | Visual audit |
| Relationship line | Verified | P0 | 2段配置で実行可能 | 実使用時のラベル文言を磨く | Visual audit |
| Custom spread | Backlog | P3 | 未実装 | 保存/復習/配布が安定してから検討 | Requirements |

## DATA / PERSISTENCE

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| localStorage schema | Verified | P0 | `onoko-arcana:desktop:history:v1` を使用 | v2以降はmigration方針に従う | `docs/data/HISTORY_SCHEMA_V1.md` |
| Export history | Verified | P1 | JSON 書き出し可能 | Export format の固定とサンプル保存 | Smoke |
| Import history | Verified | P1 | exported JSON を読み戻し、既存履歴へ重複なしで merge できる | raw array 互換は維持 | `reports/web-app-smoke-20260605-004943.json` |
| Delete single reading | Verified | P1 | 確認つきで履歴から削除 | Regression only | `reports/web-app-smoke-20260605-004943.json` |
| Clear all history | Verified | P2 | 確認つき全消去を実装 | Regression only | `reports/web-app-smoke-20260605-004943.json` |
| Corrupt storage display | Verified | P1 | 壊れたlocalStorageを空履歴として黙殺しない | Regression only | `reports/web-app-smoke-20260605-004943.json` |
| Backup location guidance | Verified | P2 | export JSONを正式backup/restore経路として説明し、Settingsに更新前/PC移動前/削除前のbackup cueを表示 | Manual installer smokeで実配布環境の見え方を確認 | `README.md`, `web-app/README.md`, `reports/web-app-smoke-20260607-051723.json` |
| Card schema | Verified | P1 | `docs/data/CARD_SCHEMA_V1.md` | Card追加時はcheck/smoke更新 | Static check |
| Spread schema | Verified | P1 | `docs/data/SPREAD_SCHEMA_V1.md` | Spread追加時はlayout/fixture更新 | Static check |
| History fixtures | Verified | P2 | 正常/重複/invalid JSON fixtureあり | Regression only | `tests/fixtures/history/` |
| Learning state v1 draft | Verified | P1 | `onoko-arcana:desktop:learning:v1` を履歴とは別に保存し、`keyword_recall` と `slot_interpretation` attempts を最大件数で保持し、hard/ok/easy から due card を導出する | 7日/14日 interval を入れる場合は fixture を先に追加する | `docs/data/LEARNING_SCHEMA_V1_DRAFT.md`, `tests/fixtures/learning/learning-valid-v1.json`, `reports/web-app-check-20260606-203719.json` |
| Learning data controls | Verified | P1 | settings で学習データ件数、最終更新、export/import/clear を履歴データと分けて操作できる | 7日/14日 interval 追加時はfixtureとsmokeを先に増やす | `reports/web-app-smoke-20260607-051723.json`, `reports/onoko-arcana-settings-20260607-051723.png`, `reports/onoko-arcana-learning-export-20260607-051723.json` |

## UI / UX IMPLEMENTATION

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Modular HUD assets | Verified | P0 | 9-slice と modular kit を導入 | 新規 UI surface 追加時は asset check に追加 | Static check |
| Dense spread layout | Verified | P0 | P3 overlap まで解消済み | 主要変更時に visual audit を再実行 | `issueCount: 0` |
| Mobile layout | Verified | P0 | 390px 幅 smoke 済み | 低縦幅 viewport を追加確認 | Mobile screenshot |
| Keyboard flow | Verified | P1 | Tab order, focus, Enter/Space の smoke 済み | settings と学習UIの詳細focus記録は後続 | `reports/keyboard-focus-smoke-20260606-203220.json` |
| Accessibility labels | Implemented | P2 | 履歴復元/削除にaria-labelを追加 | Button/slot全体監査は後続 | Static check |
| Error states | Implemented | P2 | import失敗、history保存/削除失敗を表示 | asset load失敗は後続 | Static check |
| First-launch and after-save flow | Verified | P1 | 履歴 0 件時に学習 loop を案内し、保存後に復習開始または次の問いへ進める | 実使用メモから文言を磨く | `reports/onoko-arcana-first-launch-20260606-203136.png`, `reports/web-app-smoke-20260606-203136.json`, `reports/ui-visual-audit-20260606-203150/report.json` |
| Inspector multi-tabs | Verified | P0 | 右 inspector を `カード`、`学習`、`履歴` の3タブに分け、`カード` タブでは選択カード、ノート、フル学習シートを同時に扱える | 履歴 filter 拡張時にタブ内の高さ配分を再監査する | `reports/web-app-check-20260607-011909.json`, `reports/web-app-smoke-20260607-011915.json`, `reports/ui-visual-audit-20260607-012023/report.json`, `reports/keyboard-focus-smoke-20260607-012201.json`, `reports/electron-app-smoke-20260607-012214.json`, `reports/electron-package-smoke-20260607-012237.json` |

## LEARNING / REVIEW

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Study sheet beside note | Verified | P0 | 現行 MVP の核として、ノート入力中にカードタブでフル学習シートを参照できる | Card Study Sheet 拡張時は card/study 両方の表示を smoke する | `reports/web-app-smoke-20260607-011915.json` |
| Reading history | Verified | P0 | 保存済み一覧、要約、復習ノート、カード/スプレッド/メモ有無filterを表示 | 質問/日付filterはUI密度を見て別スライス判断 | `reports/web-app-smoke-20260607-061029.json` |
| Review mode | Verified | P1 | 履歴1件を復習ノートで読み、カード別filter時は自分の読みと学習シート要点を比較できる。スプレッド/メモ有無filterも復習対象の絞り込みに使える | 質問/日付filterは後続 | `reports/web-app-smoke-20260607-061029.json` |
| Study lens | Verified | P1 | 履歴から保存数、メモ数、既出/未出カード、よく出るカード、次の観測候補、想起練習入口を自動表示 | 情報密度と初回導線を調整 | `reports/web-app-smoke-20260606-140227.json`, `reports/ui-visual-audit-20260606-140228/report.json` |
| Card/spread/note review filter | Verified | P1 | Study Lens のカード名、スプレッド、メモ有無で保存履歴を絞って復習できる | 質問/日付filterは後続 | `reports/web-app-smoke-20260607-061029.json`, `reports/onoko-arcana-card-review-compare-20260606-1342-compare-visible.png` |
| Note vs study sheet compare | Verified | P1 | カード別復習中に、保存済みの自分の読み、学習シート要点、スロットpromptを同じ履歴カード内で比較できる | 比較結果の分析は spaced review 後に分ける | `reports/web-app-smoke-20260607-011915.json` |
| Card Study Sheet | Verified | P1 | 選択カードまたは Study Lens から、正位置、逆位置、象徴、誤読しやすい点、内省質問を折りたたみシートとして開ける | 歴史メモとカード系譜は後続 content fixture | `reports/web-app-smoke-20260606-203136.json`, `reports/ui-visual-audit-20260606-203150/report.json`, `reports/web-app-check-20260606-203719.json` |
| Recall Practice | Verified | P1 | 学習シートを見る前にカードのキーワードや逆位置傾向を想起し、学習シートと比べて hard/ok/easy を learning state に保存できる | 7日/14日 interval は後続 | `reports/web-app-smoke-20260607-011915.json`, `tests/fixtures/learning/learning-valid-v1.json` |
| Slot Interpretation Drill | Verified | P1 | Study Sheet のカードが卓上選択カードと一致する時、カード + スロット + 正逆の解釈を自分で書いてから解説と比べ、hard/ok/easy を保存できる | spread tutor と履歴 filter で探しやすくする | `reports/web-app-smoke-20260607-011915.json`, `reports/ui-visual-audit-20260607-012023/report.json`, `tests/fixtures/learning/learning-valid-v1.json` |
| Due card queue | Verified | P1 | 最新 attempt の confidence から今日復習すべきカード数と due cue を Study Lens に表示し、対象カードの想起練習へ戻れる | 7日/14日 interval と fixture は後続 | `reports/web-app-smoke-20260606-203136.json`, `reports/ui-visual-audit-20260606-203150/report.json` |
| Search / filter | Implemented | P2 | カード別復習filterに加え、履歴タブでスプレッドとメモ有無を絞り込める | 次は問いテキスト、保存日filter。右パネル過密化を避ける | `reports/web-app-smoke-20260607-061029.json` |
| Study progress | Verified | P2 | 学習レンズで引いた回数、メモ数、未出カード、想起/スロット練習回数、次の復習数を表示し、compact 表示設定を settings で切り替えられる | 履歴 filter 追加時に情報密度を再確認 | `reports/web-app-smoke-20260606-203136.json` |

## ELECTRON / DISTRIBUTION

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Electron shell | Verified | P0 | `npm run desktop` 相当の shell がある | 変更時に electron smoke を通す | `reports/electron-app-smoke-20260606-203227.json` |
| Packaging | Verified | P1 | `dist/onoko-arcana-local/` fallback package と NSIS installer を作成できる | Release昇格時はtag CI artifactを使用 | `reports/electron-package-smoke-20260607-051835.json`, `reports/onoko-arcana-installer-smoke-20260607-052003.json` |
| App icon | Automated verified / manual pending | P1 | `imagegen` 生成の透明 PNG と Windows `.ico` を採用し、Electron window/taskbar、fallback shortcut、NSIS configへ接続済み | clean Windows user/VMで実Desktop/Start Menu shortcut iconを確認 | `assets/generated/app-icons/onoko-arcana-app-icon-v1.ico`, `reports/electron-package-smoke-20260607-051835.json`, `reports/onoko-arcana-installer-smoke-20260607-052003.json` |
| Installer release | Automated verified / manual pending | P1 | GitHub Release `v0.1.3` は unsigned setup.exe を主導線、fallback zipを副導線として公開済み。clean Windows manual smokeは未実施 | clean Windows user/VMでmanual smokeを実行 | `docs/release/RELEASE_CHECKLIST_v0.1.3.md`, `docs/release/INSTALLER_MANUAL_SMOKE_CHECKLIST.md` |
| Release/support settings | Verified | P1 | Settings に最新版Release、公式Repo、Security、License、未署名/自動更新なし、更新前backup cueを表示し、Electron外部リンクを公式repo配下に制限 | version更新時は `appVersion` とsmoke期待値も更新 | `reports/web-app-smoke-20260607-051723.json`, `reports/electron-package-smoke-20260607-051835.json`, `reports/onoko-arcana-installer-smoke-20260607-052003.json` |
| Auto update | Hold | P3 | 未実装。unsigned previewでは意図的に入れない | code signing/update trust modelを定義するまで保留 | `docs/release/RESIDUAL_RISK_REGISTER_2026-06-07.md` |
| Settings screen | Verified | P2 | 履歴データ、学習データ、表示設定、localStorage key、Release/support/backup導線を分けた modal を実装 | manual installer smokeで実環境表示を確認 | `reports/web-app-smoke-20260607-061029.json`, `reports/onoko-arcana-settings-20260607-061029.png`, `reports/electron-package-smoke-20260607-051835.json` |

## UNREAL ARCHIVE

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Unreal project evidence | Archived | P3 | UE 5.7 project と C++ runtime 成果あり | 実装タスクには混ぜない | `plan.md` |
| Native fallback HUD | Archived | P3 | 1枚引き proof あり | Web/Electron本線へ戻す作業はしない | Phase proof |
| UE Python actor spawn | Archived | P3 | 過去に crash あり | 完成証跡には使わない | AGENTS rule |
| Premium 3D table | Archived | P3 | 構想のみ | 現行v1.xロードマップ外 | Scope lock |

## QA / TOOLING

| Item | Status | Priority | 現在 | 次の作業 | Done 証跡 |
|---|---|---|---|---|---|
| Static app check | Verified | P0 | `scripts/check_web_app.py` が history/learning/settings/release support/card study/slot drill schema、fixture、package、installer、README、初回/due runtime term も確認 | 新規契約時だけ拡張 | `reports/web-app-check-20260607-061238.json` |
| Web smoke | Verified | P0 | `scripts/smoke_web_app.cjs` が export/import/delete/clear/corrupt storage、card/spread/note history filter、Card Study Sheet、カードタブ学習シート、Slot Interpretation Drill 保存、Recall Practice 保存、settings learning export/import/clear、Release/support settings、初回導線、保存後アクション、due cue を確認 | keyboard/a11y 深掘りは別 smoke | `reports/web-app-smoke-20260607-061029.json` |
| Electron smoke | Verified | P0 | `scripts/smoke_electron_app.cjs` が desktop panel fit、app icon、外部リンクallowlistの静的契約も確認 | Shell変更時に維持 | `reports/electron-app-smoke-20260607-061249.json` |
| Package smoke | Verified | P1 | `scripts/smoke_electron_package.cjs` がpackage起動、保存、import、invalid import、Release/support settingsを確認 | package方式変更時に維持 | `reports/electron-package-smoke-20260607-061337.json` |
| Installer smoke | Verified | P1 | `scripts/smoke_electron_installer_app.cjs` がNSIS config、packaged resources、起動、画像、Release/support settingsを確認 | installer config変更時に維持 | `reports/onoko-arcana-installer-smoke-20260607-052003.json` |
| Visual audit | Verified | P0 | `scripts/audit_web_ui_visual.cjs` は desktop overflow/panel clipping と学習/settings/初回/due/Card Study Sheet/Slot Drill UI selector を含め issueCount 0 | 次のGUI追加時に対象を増やす | `reports/ui-visual-audit-20260607-061249/report.json` |
| Regression snapshots | Implemented | P2 | `reports/README.md` で代表証跡と一時runを分離 | 必要時のみ代表proofをpromote | Report policy |

## 次に進める順序

1. `docs/release/INSTALLER_MANUAL_SMOKE_CHECKLIST.md` は clean Windows user/VM が用意できるまで manual pending として残す。
2. 履歴filterの次スライスとして、問いテキストと保存日filterを追加するか判断する。
3. Spread Tutor と Story Synthesis の要件を、学習UIの密度を増やしすぎない形で定義する。
4. 7日/14日 interval を入れる場合は learning fixture と due smoke を先に増やす。
5. code signing、MSIX、Store、auto updateは、manual installer smokeと実ユーザー反応後に別スコープで定義する。

## 完了報告に含めるもの

- 変更したファイル。
- 実行した検証コマンド。
- 生成された `reports/` の JSON とスクリーンショット。
- 未検証の場合は、理由と代替確認。
- デザインに影響する場合は `docs/design/DESIGN_KANBAN.md` の該当項目更新。
