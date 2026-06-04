# ONOKO ARCANA Unreal Roadmap Discussion Log

## Phase 0 Back And Alpha Correction - 2026-05-31 14:48

### User Input
> そもそも裏面画像は生成段階からおかしいと思う

### Codex Proposal Or Question
旧裏面をUE側のスケール問題ではなく生成素材そのものの問題として扱い、新しいONOKO ARCANA裏面v2を生成した。front/backのカード外側も透過PNGへ加工し、UEでMasked Materialとして再配置した。

### Decisions
- Accepted: `card-back-b-production-v1.png` is deprecated for production use.
- Accepted: `card-back-onoko-production-v2-source.png` and `card-back-onoko-production-v2-transparent.png` are the current Phase 0 back baseline.
- Accepted: UE card plane materials should use alpha-aware Masked materials instead of opaque rectangular PNG display.
- Accepted: `L_Phase0_CardPlane_Check` should be updated in place by clearing actors, not by deleting the loaded map asset.
- Open: Replace the placeholder white table with the ONOKO-style rich dark divination table.

### Rationale
The first UE screenshot showed two separate problems: the old back design looked too narrow from the generated image itself, and the non-alpha card textures produced black rectangular backgrounds. Regenerating the back and importing alpha-ready textures fixes the visual baseline before table-polish work begins.

---

## Initial Roadmap Definition - 2026-05-31 05:52

### User Input
> カンバンボードや作成した素材をまとめた今後のロードマップを論文レベルで作成

### Codex Proposal Or Question
既存のカンバン、生成素材、大アルカナJSON、HTML一覧、確認レポート、試作HTMLを棚卸しし、Unreal Engine版へ進むための研究ロードマップとして永続文書化する。

### Decisions
- Accepted: ONOKO ARCANAは「タロット学習と占いに特化したPCソフト」として、ONOKO ORACLEとは分ける。
- Accepted: カード画像は `1024x1536px`、比率 `2:3` を正式基準にする。
- Accepted: カード名、番号、正位置/逆位置キーワードは画像に焼き込まず、アプリ側UIで重ねる。
- Accepted: 次の開発本線は、最新Unreal Engine系での3D占い卓プロトタイプを前提に整理する。
- Open: Unreal Engineの実インストール、プロジェクト雛形作成、カードTexture2D取り込みの実測は次工程で行う。

### Rationale
現在は素材が大アルカナ22枚まで揃い、ONOKOらしい全体デザインも固まってきた段階である。ここで小アルカナ量産へ進む前に、アプリ体験、3D卓、学習導線、カードデータ構造、品質基準をまとめることで、生成素材と実装が別方向へ進むリスクを下げる。

---

## Phase 0 GUI Operation - 2026-05-31 14:20

### User Input
> UE実際に操作して

### Codex Proposal Or Question
Unreal Editorを実際に起動し、Phase 0確認Mapを開いた。画面キャプチャで、Fool、Magician、Chariot v2、Card Back が2:3 Plane上に表示されていることを確認した。

### Decisions
- Accepted: `L_Phase0_CardPlane_Check` is the first real UE visual confirmation map.
- Accepted: Current table surface is a placeholder and should be replaced with ONOKO-style dark table material in the next step.
- Open: Rich table material, camera polish, and viewport/detail screenshots after visual polish.

### Rationale
The project has moved from commandlet-only setup to a visible Unreal Editor scene. This validates that the imported Texture2D assets and basic 2:3 mesh presentation are usable inside UE 5.7.

---

## Phase 0 Texture Import - 2026-05-31 06:45

### User Input
> Phase 0に取り掛かって

### Codex Proposal Or Question
Editor GUIを開く前に、Unreal PythonでPhase 0サンプル4枚をTexture2Dとして自動Importした。

### Decisions
- Accepted: Enable `PythonScriptPlugin` and `EditorScriptingUtilities` for Editor-only automation.
- Accepted: Keep imported test textures under `/Game/ONOKOArcana/Cards/Textures`.
- Accepted: Store import results in `phase0-import-result.json`.
- Open: Card plane and viewport screenshot are still pending.

### Rationale
Texture import can be verified mechanically without waiting for GUI操作. This reduces the remaining Phase 0 risk to viewport/material/aspect confirmation.

---

## Phase 0 Validation - 2026-05-31 06:35

### User Input
> Phase 0に取り掛かって

### Codex Proposal Or Question
Phase 0 scaffoldの検証として、JSON構文、staged PNG寸法、UnrealBuildToolのprojectfiles生成、Editor target build、UnrealEditor-Cmd commandlet loadを実行した。

### Decisions
- Accepted: Project must include a minimal empty C++ runtime module so UBT can generate project files and validate editor target builds.
- Accepted: Gameplay and UI design remain Blueprint-first; the C++ module is infrastructure for buildability and future stable runtime code.
- Open: Interactive editor import and viewport screenshot are still pending.

### Rationale
Blueprint-only project scaffold can be valid for the editor, but UBT validation failed without a `Source` folder. Adding a minimal module makes the Phase 0 baseline mechanically testable before asset import work begins.

---

## Phase 0 Started - 2026-05-31 06:20

### User Input
> Phase 0に取り掛かって

### Codex Proposal Or Question
Unreal Engine 5.7の実体を確認し、ONOKO ARCANA用の最小Unrealプロジェクト、ImportStaging、サンプルカード取り込みマニフェスト、チェックリストを作成した。

### Decisions
- Accepted: Engine install path is `<UE_5.7>`.
- Accepted: Detected engine version is `5.7.4-51494982+++UE5+Release-5.7-Windows`.
- Accepted: Phase 0 first import set is card back, 00 Fool, 01 Magician, and 07 Chariot v2.
- Accepted: Unreal project root is `Unreal/ONOKO_ARCANA/`.
- Open: Actual Texture2D import and viewport screenshots require launching Unreal Editor interactively.

### Rationale
The fastest useful Phase 0 result is to verify the real engine installation and prepare a minimal project that can open cleanly, without importing all 22 cards before the `2:3` mesh and texture readability checks are complete.

---
