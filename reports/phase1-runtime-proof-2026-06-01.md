# Phase 1 Runtime Proof

作成日: 2026-06-01

## 結論

Phase 1の一枚引き縦断フローは、UE EditorのPIE上で実操作確認まで到達した。

確認済みフロー:

1. Native fallback HUD表示。
2. 問い入力。
3. Start。
4. Draw。
5. Reveal。
6. ユーザー解釈入力。
7. Guide表示。
8. Save。
9. History更新。
10. SaveGame file更新。

## 実画面で確認した状態

- QAカードGridはPIE中に非表示化された。
- Runtime card actorが中央に表示された。
- Card frontは縦向きに表示された。
- HUDにカード名、向き、キーワード、学習ガイド、履歴件数、最新履歴詳細が表示された。
- `ONOKO_ARCANA_Readings.sav` が更新された。

## 検証証跡

| Item | Result |
|---|---|
| Runtime proof screenshot | User-provided screenshot in chat, 2026-06-01 |
| Final preflight | `reports/phase1-preflight-check-20260601-114304.json` |
| SaveGame file | `Unreal/ONOKO_ARCANA/Saved/SaveGames/ONOKO_ARCANA_Readings.sav` |
| Native runtime defaults smoke | `Unreal/ONOKO_ARCANA/Saved/Phase1NativeRuntimeDefaultsTestResult.json` |
| HUD reflection smoke | `Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json` |
| SaveGame commandlet smoke | `Unreal/ONOKO_ARCANA/Saved/Phase2ReadingSaveGameTestResult.json` |
| History commandlet smoke | `Unreal/ONOKO_ARCANA/Saved/Phase2ReadingHistoryViewModelTestResult.json` |

## 実装メモ

- `UOnokoArcanaTableHudWidget` にnative fallback widget treeを追加した。
- `AOnokoArcanaPlayerController` にPIE用runtime bootstrapを追加した。
- Runtime bootstrapは、既存QA `StaticMeshComponent` をPIE中だけ非表示化する。
- Runtime bootstrapは、card actor、table controller、orthographic camera、phase lightを生成する。
- `DefaultEngine.ini` はPhase 1 mapと `AOnokoArcanaGameMode` を既定にした。

## 残課題

- Native fallback HUDは機能証跡用であり、最終UIではない。
- `WBP_TableHUD` を作り、余白、文字サイズ、履歴リスト、操作状態を整える必要がある。
- Map上にはQAカードGridが残っている。次工程で、完成用mapまたはsublevelへ整理する。
- CommonUI plugin由来の警告がPIEログに出ている。Phase 1の `UUserWidget` fallback HUDでは非致命的だが、CommonUIを本格採用するなら `CommonGameViewportClient` 設定を検討する。
