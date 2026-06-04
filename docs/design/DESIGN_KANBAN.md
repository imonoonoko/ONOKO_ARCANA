# ONOKO ARCANA デザインカンバン

Updated: 2026-06-05

この文書は、初期の全体デザインカンバンを現行の Web/Electron MVP に合わせて整理したデザイン判断ボードである。初期世界観資料は `docs/design/overall-design-kanban.md` と `assets/design/onoko-arcana-design-kanban-v1-onoko.png` を参照し、この文書では「何を残すか」「何を改善するか」「どの証跡で判断するか」を管理する。

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
- カード、卓、選択状態、学習ガイド、履歴を同じプレイ面の中で扱う。
- 文字情報は画像に焼き込まず、HTML/UMG などの実テキストとして表示する。
- 青は観測、選択、reveal、guide の光に使う。
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
| モバイル/狭幅 | 横スクロールを出さず、縦スクロールで完結する | `reports/onoko-arcana-web-app-mobile-20260605-004943.png` |
| 監査状態 | P1/P2/P3 の視覚問題を 0 件に保つ | `reports/ui-visual-audit-20260605-004949/report.json` |

## UI TABLE

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| ONOKO 占い卓の第一印象 | Verified | P0 | 中央卓背景、金枠、青い観測光が成立 | 大きく崩さず、実使用で読みにくい部分だけ調整 | Desktop/Mobile screenshot |
| 左右パネルの役割 | Verified | P0 | 左が問い/スプレッド、右が選択カード/メモ/guide/履歴 | パネル名と情報密度を実使用で見直す | Visual audit issue 0 |
| コマンド配置 | Implemented | P1 | Draw/Reveal/Save/Reset が上部またはモバイルでは専用ブロックにある | キーボード操作とフォーカス順を追加確認 | Browser smoke |
| 物理卓らしさ | Implemented | P1 | 透明 HUD 感を減らし、画像ベースの卓に寄せた | 卓の明暗差とカード視認性のバランスを維持 | Screenshot review |
| 初回起動の空状態 | Active | P1 | 空の問いと未保存履歴は表示できる | 初回でも次に押すボタンが自然に分かる状態へ調整 | One-card empty screenshot |

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
| 先に自分の読みを書く | Verified | P0 | note 入力後に guide を見る流れが成立 | note 未入力時の guide 制御を維持 | Web smoke |
| Guide の表示 | Implemented | P0 | 結果、逆位置、学習観点を表示 | guide の文量と比較しやすさを調整 | Guide rows screenshot |
| 過去メモの復習 | Implemented | P1 | 履歴選択後に復習ノートで問い、カード、保存メモを見返せる | カード別、スプレッド別、問い別に振り返る復習filterを検討 | Web smoke |
| 学習ノート質感 | Verified | P1 | 自分の読み欄と履歴復習が白枠のない暗い観測ノート風になった | 濃いONOKO UI内で可読性を維持 | `reports/onoko-arcana-initial-history-fit-20260604-054738.png` |
| 学習進捗 | Backlog | P2 | 未実装 | よく引いたカード、未復習カード、自己解釈の変化を出す | Study dashboard or report |
| 暗記ではなく比較 | Backlog | P2 | 右パネルで選択カードの意味を確認できる | 同カードの過去読み比較を追加する | Comparison UI screenshot |

## READING

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| 1枚引き | Verified | P0 | 実装、保存、履歴確認済み | 実使用でコピーや余白を微調整 | Smoke report |
| 複数スプレッド | Verified | P0 | 6種類を実装済み | スプレッドごとの説明文を磨く | `web-app-check-20260603-002748.json` |
| 順番めくり | Verified | P0 | reveal order に沿って開ける | reveal 済み/未 reveal の差を維持確認 | Browser smoke |
| 選択カード Inspector | Implemented | P0 | 選択カードの意味、note、guide、履歴を右に表示 | guide と履歴が縦に詰まりすぎる場合の調整 | Desktop screenshot |
| 読みの完了感 | Implemented | P1 | Save 後に履歴一覧と復習ノートへつながる | 次の読み、filter、比較学習への導線を強める | Save flow smoke |

## ASSETS

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| V5 カード素材 | Verified | P0 | 23 assets を使用 | 変更しない。新規生成は別ブランチ扱い | Asset audit |
| 卓背景 | Verified | P0 | `astra-nocturne-background-v1.png` を採用 | 暗すぎる/眩しすぎる箇所だけ調整 | Screenshot |
| 9-slice HUD | Implemented | P1 | パネル、ボタン、行、slot 装飾に使用 | active/disabled/focus の状態差を整理 | Visual audit |
| アイコン体系 | Implemented | P1 | Electron window iconはカード裏面PNGを使用。操作icon体系は後続で整理 | 操作アイコンと装飾アイコンを分ける | `web-app/electron/main.cjs` |
| 生成素材管理 | Implemented | P2 | 採用素材はpackage scriptとstatic checkで限定コピー/確認する | 本格manifestは外部配布時に検討 | `scripts/package_electron_local.cjs`, `scripts/check_web_app.py` |

## POLISH

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| 視覚監査 | Verified | P0 | 最新 audit は issueCount 0 | 主要変更ごとに再実行 | `reports/ui-visual-audit-20260605-004949/report.json` |
| ホバー/選択状態 | Verified | P1 | 青い選択光と金枠があり、keyboard focus smoke済み | より深い読み上げ監査は後続 | `reports/keyboard-focus-smoke-20260605-005005.json` |
| 低モーション | Implemented | P1 | `prefers-reduced-motion` 対応あり | reveal motion を入れる場合も低モーションを維持 | CSS check |
| レスポンシブ | Verified | P0 | Desktop, compact, mobile で監査済み | 1280x720 など低め画面を追加確認 | Additional audit |
| コピー調整 | Active | P1 | 日本語の短い説明で構成 | 占いらしさと操作明瞭性のバランスを改善 | Copy review |

## ACCESSIBILITY / USABILITY

| Item | Status | Priority | 現在 | 次の改善 | Done 証跡 |
|---|---|---|---|---|---|
| キーボード操作 | Verified | P1 | Tab 順、Enter/Space 操作、focus 表示を監査済み | 追加a11y監査で深掘り | `reports/keyboard-focus-smoke-20260605-005005.json` |
| 色以外の状態表現 | Implemented | P1 | ラベル、番号、位置名を併用 | disabled/revealed/selected の形状差を強める | Visual audit |
| 文字サイズ | Implemented | P1 | 密集カードは marker mode で対応 | 履歴と guide の長文折り返しを継続確認 | Text overflow check |
| 読み上げ | Backlog | P2 | 未検証 | aria-label と live region の要否を整理 | Accessibility check |

## 次回デザインレビューの観点

1. 初回起動時に、ユーザーが「問いを書く、スプレッドを選ぶ、ドローする」を迷わず行えるか。
2. 保存後に「次の読みへ進む」か「履歴で復習する」かが自然に分かるか。
3. 右パネルが guide、note、history を抱え込みすぎていないか。
4. キーボード操作時にも、青い選択光とフォーカスが矛盾しないか。
5. 実使用で読み返した時、ONOKO らしさよりも情報密度が勝ちすぎていないか。
