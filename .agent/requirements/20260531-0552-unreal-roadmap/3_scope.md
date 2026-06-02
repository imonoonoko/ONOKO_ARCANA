# ONOKO ARCANA Unreal Roadmap Scope

## MVP
- Windows PCで起動できるUnreal Engine版ONOKO ARCANAの縦断スライス。
- 3D占い卓にカードデッキ、カードスロット、ONOKO風ホログラムUIが表示される。
- 大アルカナ22枚を `data/major-arcana-cards.json` 相当の構造から読み込める。
- 1枚引きができ、正位置/逆位置、カード名、キーワード、学習焦点が表示される。
- ユーザーが先に自分の解釈メモを書き、その後に補助解釈を見る流れを持つ。
- セッション履歴がローカルに保存される。

## Nice To Have
- 3枚引き「過去、現在、未来」。
- カード一覧/学習モード。
- カード拡大ビュー。
- シャッフル、ドロー、フリップの短い演出。
- ONOKOのガイド的コメント枠。
- HTMLレポートからUnreal実装進捗へリンクする開発用ダッシュボード。

## Future
- 小アルカナ56枚。
- スプレッドエディタ。
- 質問テンプレート。
- 解釈メモの検索、タグ付け、エクスポート。
- 音、環境光、Niagara演出、カメラワークの強化。
- ONOKOガイドのボイス、表情、3D/2Dアバター。

## Out Of Scope
- 宗教的、医療的、法律的、金融的な断定助言。
- 外部課金、オンラインアカウント、クラウド同期。
- ONOKO ORACLEの判断支援機能との統合。
- 最初から全78枚を完成させること。
- 画像生成そのものをUnreal内で行うこと。

## Constraints
- Deadline: 未設定。まずは縦断スライスを完成させる。
- Team/resources: ローカルPC、既存ONOKO素材、Codexによる実装支援。
- Technology: Unreal Engine 5.7系を第一候補。未インストールの場合はEpic Games Launcherから導入する。
- Budget/cost: 追加有料アセットを前提にしない。
- Compatibility/compliance: Windows PC向け。ローカル保存を基本にし、個人情報や占い結果の外部送信を初期スコープに入れない。
