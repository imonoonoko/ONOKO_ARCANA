# ONOKO ARCANA Phase 0 Baseline Report

作成日: 2026-05-31  
対象: `C:\ONOKO_PROJECT\ONOKO_ARCANA`

## 結論

Phase 0を開始し、Unreal Engine 5.7.4のローカル実体を確認した。ONOKO ARCANA用の最小Unrealプロジェクト、Unreal向けフォルダ構成、カード4枚のImportStaging、取り込みマニフェスト、Importチェックリストを作成した。

プロジェクトはBlueprint-firstで進めるが、UnrealBuildToolでプロジェクトファイル生成を検証できるよう、空のC++ Runtimeモジュールを持たせている。

Editor GUIでPhase 0確認Mapを開き、初期表示の問題として「旧裏面画像が生成段階から細く見える」「各カードの外側に黒い非透過矩形が出る」ことを確認した。そのため旧裏面 `card-back-b-production-v1.png` は廃止し、新しい2:3裏面v2と透過済みfront/back画像をUEへ再Importした。

現在のPhase 0基準は、`1024x1536px` / `2:3` / アルファ付きPNG / Masked Materialである。

## 検出したUnreal環境

| Item | Value |
|---|---|
| Install path | `C:\Program Files\Epic Games\UE_5.7` |
| AppName | `UE_5.7` |
| AppVersion | `5.7.4-51494982+++UE5+Release-5.7-Windows` |
| UnrealEditor | `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe` |
| UnrealEditor-Cmd | `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe` |

## 作成したプロジェクト準備物

| Artifact | Path |
|---|---|
| Unreal project | `Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject` |
| Config | `Unreal/ONOKO_ARCANA/Config/` |
| Minimal C++ module | `Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/` |
| Content root | `Unreal/ONOKO_ARCANA/Content/ONOKOArcana/` |
| Texture staging | `Unreal/ONOKO_ARCANA/ImportStaging/Phase0_CardTextures/` |
| Alpha texture staging | `Unreal/ONOKO_ARCANA/ImportStaging/Phase0_CardTexturesAlpha/` |
| Import manifest | `Unreal/ONOKO_ARCANA/ImportStaging/Phase0_CardTextures/phase0-card-import-manifest.json` |
| Alpha import manifest | `Unreal/ONOKO_ARCANA/ImportStaging/Phase0_CardTexturesAlpha/phase0-alpha-card-import-manifest.json` |
| Import checklist | `Unreal/ONOKO_ARCANA/Docs/PHASE0_IMPORT_CHECKLIST.md` |
| Unreal ignore rules | `Unreal/.gitignore` |

## Phase 0 Sample Assets

| Asset | Role |
|---|---|
| `card-back-b-production-v1.png` | 旧裏面。生成段階でカード本体が細く見えるため廃止 |
| `card-back-onoko-production-v2-source.png` | 新しい2:3裏面ソース |
| `card-back-onoko-production-v2-transparent.png` | UE採用中の透過済み裏面 |
| `major-00-fool-onoko-concept-v1.png` | 00 愚者、基準カード比率 |
| `major-01-magician-onoko-concept-v1.png` | 01 魔術師、通常カード表面サンプル |
| `major-07-chariot-onoko-concept-v2.png` | v2採用カードの代表 |

## 次の操作

1. プレースホルダーの白いテーブル面を、ONOKOサイバー占い卓の黒アクリル/青い観測リング/控えめな金装飾へ置き換える。
2. カードPlaneの厚み、縁、影、接地感を追加し、平面画像貼り付け感を減らす。
3. 卓上カメラとカード詳細カメラを分け、学習UIの読みやすさを確認する。
4. 確認スクリーンショットを `assets/generated/reports/` に保存し、Phase 1へ進む前の基準画像にする。

## Phase 0 Status

- Done: Unreal Engine 5.7.4検出。
- Done: Project scaffold作成。
- Done: ImportStaging作成。
- Done: sample texture existence確認。
- Done: `.uproject` とImport manifestのJSON構文確認。
- Done: staged sample textures 4枚がすべて `1024x1536px`、比率 `2:3` であることを確認。
- Done: `UnrealBuildTool -projectfiles` 成功。
- Done: `ONOKO_ARCANAEditor Win64 Development` ビルド成功。
- Done: `UnrealEditor-Cmd.exe -run=ResavePackages -ProjectOnly -SkipSave -Unattended -NullRHI` でプロジェクトロード成功。
- Done: Unreal PythonでPhase 0サンプル4枚をTexture2DとしてImport。
- Done: UE内にPhase 0確認Map `L_Phase0_CardPlane_Check` を作成。
- Done: 4つのカードMaterialを作成し、2:3 card plane scaleを `x=0.70`, `y=1.05` として配置。
- Done: GUI Editorで `L_Phase0_CardPlane_Check` を開き、2:3カードPlane表示を目視確認。
- Done: Editor表示スクリーンショットを `assets/generated/reports/phase0-unreal-editor-visible-2026-05-31.png` に保存。
- Done: 旧裏面 `card-back-b-production-v1.png` を廃止判断。
- Done: 新しい2:3裏面 `card-back-onoko-production-v2-source.png` を生成し、透過版 `card-back-onoko-production-v2-transparent.png` を作成。
- Done: front/back 4枚の透過版を `ImportStaging/Phase0_CardTexturesAlpha/` に配置。
- Done: 透過版4枚をUnrealへImportし、すべて `1024x1536px` と確認。
- Done: Materialを `BLEND_MASKED` + `Opacity Mask` 接続に変更し、カード外側の黒い矩形を除去。
- Done: 既存Map削除時のUEクラッシュを避けるため、確認Map更新方式を「Map削除」から「Actor削除後に再配置」へ変更。
- Done: GUI Editorで修正版 `L_Phase0_CardPlane_Check` を開き、裏面比率と背景透過の改善を目視確認。
- Done: 修正版スクリーンショットを `assets/generated/reports/phase0-unreal-editor-alpha-fixed-2026-05-31.png` に保存。
- Pending: ONOKO占い卓としてのテーブル材質、照明、カメラ構図のリッチ化。

## 検証メモ

### JSON / 素材

- `ONOKO_ARCANA.uproject`: JSON valid。
- `phase0-card-import-manifest.json`: JSON valid、4 items。
- ImportStaging内PNG:
  - `card-back-b-production-v1.png`: `1024x1536`
  - `major-00-fool-onoko-concept-v1.png`: `1024x1536`
  - `major-01-magician-onoko-concept-v1.png`: `1024x1536`
  - `major-07-chariot-onoko-concept-v2.png`: `1024x1536`
- Alpha ImportStaging内PNG:
  - `card-back-onoko-production-v2-transparent.png`: `1024x1536`
  - `major-00-fool-onoko-concept-v1-alpha.png`: `1024x1536`
  - `major-01-magician-onoko-concept-v1-alpha.png`: `1024x1536`
  - `major-07-chariot-onoko-concept-v2-alpha.png`: `1024x1536`

### UnrealBuildTool

- Project files generation: succeeded。
- Editor target build: succeeded。
- Generated module DLL: `Unreal/ONOKO_ARCANA/Binaries/Win64/UnrealEditor-ONOKO_ARCANA.dll`

### Commandlet Load

`UnrealEditor-Cmd.exe` でプロジェクトをロードし、終了コード0で完了した。ログ上でCommonUI pluginのmount、Engine Version `5.7.4-51494982+++UE5+Release-5.7` を確認した。

非致命的なログとして `aqProf.dll`、`VtuneApi.dll`、`WinPixGpuCapturer.dll` の未検出が出ている。これらはプロファイラ/PIX関連の補助DLLであり、今回のプロジェクトロード失敗要因ではない。

### Texture2D Import

Unreal Python script `Unreal/ONOKO_ARCANA/Scripts/import_phase0_textures.py` で4枚をImportした。結果は `Unreal/ONOKO_ARCANA/ImportStaging/Phase0_CardTextures/phase0-import-result.json` に保存されている。

| Asset | Imported Object Path | Size |
|---|---|---|
| Card back | `/Game/ONOKOArcana/Cards/Textures/T_CardBack_B_Production_V1` | `1024x1536` |
| 00 Fool | `/Game/ONOKOArcana/Cards/Textures/T_Major_00_Fool_V1` | `1024x1536` |
| 01 Magician | `/Game/ONOKOArcana/Cards/Textures/T_Major_01_Magician_V1` | `1024x1536` |
| 07 Chariot v2 | `/Game/ONOKOArcana/Cards/Textures/T_Major_07_Chariot_V2` | `1024x1536` |

Importログには `LogAutomationTest: Error: Condition failed` が複数出ているが、スクリプトは成功し、`phase0-import-result.json` は `ok: true`、各Texture寸法も期待値一致だった。現時点ではUnreal Editor起動時のAutomation系ノイズとして扱い、次回GUI確認時に同じエラーが操作へ影響するかだけ見る。

旧裏面と非透過frontは初期検証用として残すが、Phase 0の表示基準からは外す。

### Alpha Texture2D Import

Unreal Python script `Unreal/ONOKO_ARCANA/Scripts/import_phase0_alpha_textures.py` で透過版4枚をImportした。結果は `Unreal/ONOKO_ARCANA/ImportStaging/Phase0_CardTexturesAlpha/phase0-alpha-import-result.json` に保存されている。

| Asset | Imported Object Path | Size |
|---|---|---|
| Card back v2 alpha | `/Game/ONOKOArcana/Cards/Textures/T_CardBack_ONOKO_Production_V2_Alpha` | `1024x1536` |
| 00 Fool alpha | `/Game/ONOKOArcana/Cards/Textures/T_Major_00_Fool_V1_Alpha` | `1024x1536` |
| 01 Magician alpha | `/Game/ONOKOArcana/Cards/Textures/T_Major_01_Magician_V1_Alpha` | `1024x1536` |
| 07 Chariot v2 alpha | `/Game/ONOKOArcana/Cards/Textures/T_Major_07_Chariot_V2_Alpha` | `1024x1536` |

### Phase 0 Card Plane Scene

Unreal Python script `Unreal/ONOKO_ARCANA/Scripts/create_phase0_card_plane_scene.py` で確認用Mapを作成した。結果は `Unreal/ONOKO_ARCANA/Saved/Phase0CardPlaneSceneResult.json` に保存されている。

| Asset | Path |
|---|---|
| Map | `/Game/ONOKOArcana/Maps/L_Phase0_CardPlane_Check` |
| Fool material | `/Game/ONOKOArcana/Cards/Materials/M_Phase0_Major_00_Fool` |
| Magician material | `/Game/ONOKOArcana/Cards/Materials/M_Phase0_Major_01_Magician` |
| Chariot v2 material | `/Game/ONOKOArcana/Cards/Materials/M_Phase0_Major_07_Chariot_V2` |
| Card back material | `/Game/ONOKOArcana/Cards/Materials/M_Phase0_CardBack_ONOKO_Production_V2` |

カードPlaneはUnreal標準Planeを `x=0.70`, `y=1.05` に拡大し、`2:3` 比率の確認対象として配置した。MaterialはTexture RGBをBase Color、Texture AlphaをOpacity Maskへ接続し、Blend ModeはMaskedに設定した。

### GUI Editor Confirmation

Unreal Editor GUIを起動し、`ONOKO_ARCANA - Unreal Editor` ウィンドウが応答していることを確認した。起動時Mapは `L_Phase0_CardPlane_Check` で、Fool、Magician、Chariot v2、Card Back の4枚が2:3比率のPlaneとして表示された。

初期確認スクリーンショット:

```text
assets/generated/reports/phase0-unreal-editor-visible-2026-05-31.png
```

修正版確認スクリーンショット:

```text
assets/generated/reports/phase0-unreal-editor-alpha-fixed-2026-05-31.png
```

現状のテーブル面は白いプレースホルダーである。次工程では、ONOKOサイバー占い卓に近づけるため、黒アクリル/ダークテーブルMaterial、青い観測リング、カード用フレーム、カメラ構図を追加する。
