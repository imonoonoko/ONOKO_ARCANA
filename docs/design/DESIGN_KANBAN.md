# ONOKO ARCANA デザインカンバン

Updated: 2026-06-07

この文書は、初期の全体デザインカンバンを現行の Web/Electron MVP に合わせて整理したデザイン判断ボードである。初期世界観資料は `docs/design/overall-design-kanban.md` と `assets/design/onoko-arcana-design-kanban-v1-onoko.png` を参照し、この文書では「何を残すか」「何を改善するか」「どの証跡で判断するか」を管理する。

学習強化アップデート時の GUI 最適化は `docs/design/GUI_OPTIMIZATION_KANBAN_2026-06-06.md` で運用する。カード別復習、学習シート、比較 UI、初回導線、アクセシビリティをこの専用ボードで管理し、既存の占い卓表現を崩さないようにする。

## ステータス

| Status | 意味 |
|---|---|
| Verified | 実装と目視確認が済み、現時点の基準として採用する |
| Implemented | 実装済みだが、継続的な目視改善余地がある |
| Active | 次の改善対象 |
| Backlog | 後続で扱う |
| Hold | 現時点では保留 |

## 固定方針

- 第一画面はダッシュボードではなく、ONOKO 風の cyber divination table にする。
- カード、卓、選択状態、学習シート、履歴を同じプレイ面の中で扱う。
- 文字情報は画像に焼き込まず、HTML/UMG などの実テキストとして表示する。
- 青は観測、選択、reveal、学習参照の光に使う。
- 金は枠、ラベル、重要な読み状態に絞る。
- Web/Electron 2D 卓を MVP 表現として固定する。Unreal 化は現行 v1.x では完全に見送り、既存UE成果はアーカイブ扱いにする。
- 初期カンバンの「学習ノート」要素は、右パネルの自分の読みと履歴復習に取り込む。

## 現在の採用基準

| 領域 | 採用基準 | 現在の証跡 |
|---|---|---|
| ONOKO らしさ | 黒、白、電気的な青、静かな観測感、猫/結晶/星の控えめな記号 | `PRODUCT.md`, `DESIGN.md` |
| 卓の印象 | UI パネルではなく、机上の占い道具として読める | `reports/onoko-arcana-initial-history-fit-20260604-054738.png` |
| カード表示 | 1枚/3枚はカード名とキーワードを読める。密集スプレッドは番号/位置マーカーを優先する | `reports/ui-visual-audit-20260603-002707/report.json` |
| スプレッド | 6種類の配置が横幅破綻なく読める | `data/spread-definitions-v1.json` |
| モバイル/狭幅 | 横スクロールを出さず、縦スクロールで完結する | `reports/onoko-arcana-web-app-mobile-20260606-194424.png` |
| 監査状態 | P1/P2/P3 の視覚問題を 0 件に保つ | `reports/ui-visual-audit-20260607-012023/report.json` |

## UI TABLE

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| ONOKO 占い卓の第一印象 | Verified | P0 | 中央卓背景、金枠、青い観測光が成立 | 大きく崩さず、実使用で読みにくい部分だけ調整 | Desktop/Mobile screenshot |
| 左右パネルの役割 | Verified | P0 | 左が問い/スプレッド、右が `カード`、`学習`、`履歴` タブ付き inspector | 履歴 filter 拡張時にタブ内の高さ配分を見直す | `reports/ui-visual-audit-20260607-012023/report.json` |
| Inspector tab structure | Verified | P0 | `カード` タブで選択カード、メモ、フル学習シートを同時に扱い、`学習` と `履歴` は深掘り/復習に分ける | 追加 filter と settings polish 時にタブ遷移を再確認 | `reports/onoko-arcana-card-tab-study-sheet-20260607-0120.png`, `reports/keyboard-focus-smoke-20260607-012201.json` |
| コマンド配置 | Implemented | P1 | Draw/Reveal/Save/Reset が上部またはモバイルでは専用ブロックにある | キーボード操作とフォーカス順を追加確認 | Browser smoke |
| 物理卓らしさ | Implemented | P1 | 透明 HUD 感を減らし、画像ベースの卓に寄せた | 卓の明暗差とカード視認性のバランスを維持 | Screenshot review |
| 初回起動の空状態 | Verified | P1 | 履歴 0 件時に、問いを書く、1枚引きで始める、保存後に復習する流れを案内できる | 実使用メモから文言だけを磨く | `reports/onoko-arcana-first-launch-20260606-194424.png`, `reports/web-app-smoke-20260606-194424.json` |

## CARDS

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| 大アルカナ 22 枚 | Verified | P0 | V5 素材 22 枚と裏面 1 枚を採用 | 再生成は品質問題が出た時だけ行う | `v5-major-arcana-visual-qa.md` |
| カード裏面 | Verified | P0 | 表面と可視サイズを合わせた裏面を採用 | reveal 前後の見え方だけ維持確認 | Web smoke screenshot |
| 逆位置表示 | Implemented | P0 | 逆位置カードは回転とラベルで判別できる | 色だけに頼らない状態表現を継続 | Visual audit |
| 密集スプレッドの可読性 | Verified | P0 | 5枚以上はカード内小文字を減らし、番号/位置で読む | Inspector 側の詳細導線をより明確にする | `issueCount: 0` |
| 小アルカナ | Hold | P3 | 未着手 | MVP の履歴/復習/配布が安定してから検討 | 新スコープ定義 |

## STUDY

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| 学習シートを見ながら読む | Verified | P0 | `カード` タブで自分の読みを書きながら、同じカードの正逆、焦点、象徴、誤読、内省質問を確認できる | 情報量が増えた時は card tab の高さを再監査 | `reports/onoko-arcana-card-tab-study-sheet-20260607-0120.png`, `reports/web-app-smoke-20260607-011915.json` |
| 過去メモの復習 | Verified | P1 | 履歴選択後に復習ノートで問い、カード、保存メモを見返せ、カード別にも絞り込める | スプレッド別、問い別、日付別filterへ拡張 | `reports/web-app-smoke-20260606-140227.json` |
| 学習ノート質感 | Verified | P1 | 自分の読み欄と履歴復習が白枠のない暗い観測ノート風になった | 濃いONOKO UI内で可読性を維持 | `reports/onoko-arcana-initial-history-fit-20260604-054738.png` |
| 学習レンズ | Verified | P1 | 履歴欄に保存数、メモ数、既出/未出カード、よく出るカード、次の観測候補、想起練習入口、復習予定数を表示し、カード別復習filterへ接続できる | 履歴filter拡張時に情報量を再調整 | `reports/web-app-smoke-20260606-203136.json`, `reports/onoko-arcana-recall-practice-20260606-1403-recall.png` |
| 学習進捗 | Verified | P2 | 学習レンズで大アルカナの既出数、未出カード、想起/スロット練習回数、次に復習するカードが見え、settings で compact 表示へ切り替えられる | 7日/14日 interval を入れるなら fixture と copy review を先に行う | `reports/web-app-smoke-20260606-203136.json`, `reports/onoko-arcana-settings-20260606-203136.png` |
| 暗記ではなく比較 | Verified | P2 | カード別復習中に、自分の過去読み、学習シート要点、スロットpromptを同じ履歴カード内で比較できる | 比較結果を自動採点しない。自分の解釈の変化を見える化する | `reports/web-app-smoke-20260607-011915.json` |
| 想起練習 | Verified | P1 | 学習シートを見る前にキーワードや逆位置傾向を入力し、答え合わせ後に hard/ok/easy を保存し、due 復習キューへ反映できる | 7日/14日 interval は fixture 追加後に扱う | `reports/web-app-smoke-20260607-011915.json` |
| スロット解釈練習 | Verified | P1 | Card Study Sheet 内で、選択中カード + スプレッド位置 + 正逆を自分の言葉で読み、解説表示後に hard/ok/easy を保存できる | 履歴filterとSpread Tutorで探しやすくする | `reports/web-app-smoke-20260607-011915.json`, `reports/ui-visual-audit-20260607-012023/report.json` |

## READING

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| 1枚引き | Verified | P0 | 実装、保存、履歴確認済み | 実使用でコピーや余白を微調整 | Smoke report |
| 複数スプレッド | Verified | P0 | 6種類を実装済み | スプレッドごとの説明文を磨く | `web-app-check-20260603-002748.json` |
| 順番めくり | Verified | P0 | reveal order に沿って開ける | reveal 済み/未 reveal の差を維持確認 | Browser smoke |
| 選択カード Inspector | Verified | P0 | `カード` タブ内で選択カード、note、フル学習シートを並べ、`学習` タブは学習レンズ/想起練習の深掘りに使う | 履歴 filter 拡張時にタブ遷移を再確認 | `reports/web-app-smoke-20260607-011915.json`, `reports/ui-visual-audit-20260607-012023/report.json` |
| 読みの完了感 | Verified | P1 | Save 後に履歴一覧、復習開始、次の問いへ進む導線が出る | 実使用で次アクションの文言を磨く | `reports/web-app-smoke-20260606-194424.json` |

## ASSETS

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| V5 カード素材 | Verified | P0 | 23 assets を使用 | 変更しない。新規生成は別ブランチ扱い | Asset audit |
| 卓背景 | Verified | P0 | `astra-nocturne-background-v1.png` を採用 | 暗すぎる/眩しすぎる箇所だけ調整 | Screenshot |
| 9-slice HUD | Implemented | P1 | パネル、ボタン、行、slot 装飾に使用 | active/disabled/focus の状態差を整理 | Visual audit |
| アイコン体系 | Verified | P1 | Electron app icon は `imagegen` 生成の透明 PNG / Windows `.ico` を使用。操作icon体系は後続で整理 | 操作アイコンと装飾アイコンを分ける | `assets/generated/app-icons/onoko-arcana-app-icon-v1.png`, `reports/onoko-arcana-app-icon-preview-20260607-0143.png`, `web-app/electron/main.cjs` |
| 生成素材管理 | Implemented | P2 | 採用素材はpackage scriptとstatic checkで限定コピー/確認する | 本格manifestは外部配布時に検討 | `scripts/package_electron_local.cjs`, `scripts/check_web_app.py` |

## POLISH

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| 視覚監査 | Verified | P0 | 最新 audit は issueCount 0 | 主要変更ごとに再実行 | `reports/ui-visual-audit-20260607-012023/report.json` |
| ホバー/選択状態 | Verified | P1 | 青い選択光と金枠があり、keyboard focus smoke済み | より深い読み上げ監査は後続 | `reports/keyboard-focus-smoke-20260606-194648.json` |
| 低モーション | Implemented | P1 | `prefers-reduced-motion` 対応あり | reveal motion を入れる場合も低モーションを維持 | CSS check |
| レスポンシブ | Verified | P0 | Desktop, compact, mobile で監査済み | 1280x720 など低め画面を追加確認 | Additional audit |
| コピー調整 | Active | P1 | 日本語の短い説明で構成 | 占いらしさと操作明瞭性のバランスを改善 | Copy review |

## ACCESSIBILITY / USABILITY

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| キーボード操作 | Verified | P1 | Tab 順、Enter/Space 操作、focus 表示を学習レンズ、履歴filter、想起練習、settings、Slot Drillまで監査済み | 追加 filter 時に focus order を再検査する | `reports/keyboard-focus-smoke-20260607-012201.json` |
| 色以外の状態表現 | Implemented | P1 | ラベル、番号、位置名を併用 | disabled/revealed/selected の形状差を強める | Visual audit |
| 文字サイズ | Implemented | P1 | 密集カードは marker mode で対応 | 履歴と学習シートの長文折り返しを継続確認 | Text overflow check |
| 読み上げ | Backlog | P2 | 未検証 | aria-label と live region の要否を整理 | Accessibility check |

## 次回デザインレビューの観点

1. Card Study Sheet と Slot Interpretation Drill 追加後も、右パネルが学習シート、note、history、recall practice、settings導線を抱え込みすぎていないか。
2. 学習シートを見ながら自分の読みを書ける一方で、想起練習とスロット練習では自分の入力 -> 答え合わせの順序を守れているか。
3. due 復習キューが目立ちすぎず、占い卓の第一印象を邪魔しないか。
4. キーボード操作時にも、青い選択光とフォーカスが矛盾しないか。
5. 実使用で読み返した時、ONOKO らしさよりも情報密度が勝ちすぎていないか。
