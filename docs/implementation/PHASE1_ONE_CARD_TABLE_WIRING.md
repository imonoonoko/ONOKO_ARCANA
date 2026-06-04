# Phase 1 One-Card Table Wiring

> Archive notice (2026-06-05): This UE/UMG note is historical evidence. The active v1.x lane is Web/Electron; do not use this document as current next work.

Updated: 2026-06-01

This note defines the next Unreal Editor wiring pass for the one-card vertical slice. The C++ runtime is now ready. A native fallback HUD and runtime actor bootstrap now allow PIE validation before the polished `WBP_TableHUD` pass.

## Current C++ Surface

Use these classes for the Phase 1 Blueprint layer:

| Class | Role |
|---|---|
| `UOnokoArcanaDeckRuntime` | Loads `data/major-arcana-v5-deck.json` and draws Major Arcana cards without duplicates. |
| `UOnokoArcanaOneCardSession` | Owns one reading session: question, current draw, user interpretation, guide reveal state. |
| `UOnokoArcanaOneCardViewModel` | Blueprint/UMG-friendly facade for card title, orientation label, keywords, study focus, and user note. |
| `AOnokoArcanaCardActor` | Displays a single tarot card plane with the shared masked material and `CardTexture` parameter. |
| `AOnokoArcanaTableController` | Connects `UOnokoArcanaOneCardViewModel` to an assigned `AOnokoArcanaCardActor`. |
| `UOnokoArcanaTableHudWidget` | C++ parent class for `WBP_TableHUD`; binds optional buttons/text fields by widget name. |
| `AOnokoArcanaPlayerController` | Creates the table HUD, connects it to `AOnokoArcanaTableController`, and can runtime-spawn missing Phase 1 actors. |
| `AOnokoArcanaGameMode` | Phase 1 game mode using `AOnokoArcanaPlayerController`. |

## Required Assets

| Asset | Status |
|---|---|
| `/Game/ONOKOArcana/Phase1/Materials/M_Phase1_CardMasked_TextureParam` | Created. Runtime texture parameter is `CardTexture`. |
| `/Game/ONOKOArcana/Cards/Textures/V5Full/T_Card_Back_ONOKO_V5_Alpha` | Adopted V5 back texture. |
| `/Game/ONOKOArcana/Maps/L_Phase1_OneCard_Table` | Exists, but not visually accepted. Treat as a workspace map only until manually checked. |

## Editor Wiring Steps

1. Open `/Game/ONOKOArcana/Maps/L_Phase1_OneCard_Table`.
2. Press PIE once with the native fallback HUD. Existing QA `StaticMeshActor` cards are hidden in-game, and `AOnokoArcanaPlayerController` creates the minimum runtime table, card, controller, and camera if map actors are missing.
3. Validate the functional path with the native HUD: Start, Draw, Reveal, note entry, Guide, Save, History, Reset.
4. For the polished Editor pass, place one `AOnokoArcanaCardActor` at the central reading slot.
5. Set the card actor material to `/Game/ONOKOArcana/Phase1/Materials/M_Phase1_CardMasked_TextureParam` if it is not already assigned.
6. Set its back texture to `/Game/ONOKOArcana/Cards/Textures/V5Full/T_Card_Back_ONOKO_V5_Alpha`.
7. Place one `AOnokoArcanaTableController` in the map.
8. Assign `ReadingCardActor` on the controller to the placed card actor.
9. Set `DefaultQuestion` to a short placeholder such as `今の自分に必要な視点は？`.
10. Use `DrawCard(false)` for a draw that stays face-down.
11. Use `RevealCard()` to flip to the selected front texture.
12. Use `RevealGuide()` only after the user has written or explicitly skipped their own interpretation.

## HUD Contract

`WBP_TableHUD` should talk to `AOnokoArcanaTableController` or directly to `UOnokoArcanaOneCardViewModel`.

Minimum controls:

| Control | Target |
|---|---|
| Question text box | `AOnokoArcanaTableController::StartReading` |
| Draw button | `AOnokoArcanaTableController::DrawCard(false)` |
| Reveal card button | `AOnokoArcanaTableController::RevealCard` |
| User interpretation text box | `AOnokoArcanaTableController::SubmitUserInterpretation` |
| Reveal guide button | `AOnokoArcanaTableController::RevealGuide` |
| Save reading button | `AOnokoArcanaTableController::SaveCurrentReading` |
| Refresh history button | `AOnokoArcanaTableController::RefreshReadingHistory` |
| Reset button | `AOnokoArcanaTableController::ResetTable` |

Minimum display bindings:

| UI Text | Source |
|---|---|
| Active spread | `AOnokoArcanaTableController::GetActiveSpreadDisplayText()` |
| Spread slots | `AOnokoArcanaTableController::GetActiveSpreadSlotListText()` |
| Card title | `UOnokoArcanaOneCardViewModel::GetCardTitle()` |
| Orientation | `UOnokoArcanaOneCardViewModel::GetOrientationLabel()` |
| Keywords | `UOnokoArcanaOneCardViewModel::GetActiveKeywordsText()` |
| Study focus | `UOnokoArcanaOneCardViewModel::GetStudyFocusText()` |
| History count | `UOnokoArcanaReadingHistoryViewModel::GetReadingCount()` or `HistoryCountText` binding in `UOnokoArcanaTableHudWidget` |
| Latest history summary | `UOnokoArcanaReadingHistoryViewModel::GetLatestReadingSummary()` |
| Selected history detail | `UOnokoArcanaReadingHistoryViewModel::GetSelectedDetailText()` |
| Error | `LastErrorMessage` on the controller or ViewModel |

Recommended `WBP_TableHUD` widget names when using `UOnokoArcanaTableHudWidget` as the parent class:

| Widget Name | Type |
|---|---|
| `SpreadSelectorComboBox` | `ComboBoxString` |
| `ActiveSpreadText` | `TextBlock` |
| `SpreadSlotsText` | `TextBlock` |
| `QuestionTextBox` | `EditableTextBox` |
| `StartReadingButton` | `Button` |
| `DrawButton` | `Button` |
| `RevealCardButton` | `Button` |
| `UserInterpretationTextBox` | `MultiLineEditableTextBox` |
| `RevealGuideButton` | `Button` |
| `SaveReadingButton` | `Button` |
| `RefreshHistoryButton` | `Button` |
| `ResetButton` | `Button` |
| `CardTitleText` | `TextBlock` |
| `OrientationText` | `TextBlock` |
| `KeywordsText` | `TextBlock` |
| `StudyFocusText` | `TextBlock` |
| `ErrorText` | `TextBlock` |
| `StateText` | `TextBlock` |
| `HistoryCountText` | `TextBlock` |
| `HistoryLatestSummaryText` | `TextBlock` |
| `HistorySelectedTitleText` | `TextBlock` |
| `HistorySelectedDetailText` | `TextBlock` |
| `HistoryEmptyStateText` | `TextBlock` |

## Acceptance Criteria

- Native fallback HUD appears in PIE when no `WBP_TableHUD` is assigned.
- Missing Phase 1 Table/Card actors are runtime-spawned only when no map actor exists.
- Existing QA static mesh card grids are hidden only during play, not deleted from the map.
- A top-down Phase 1 camera is assigned during play.
- Drawing a card changes the session state and stores the selected card.
- Before reveal, the card actor can show the V5 back texture.
- After reveal, the same actor shows the selected V5 front texture.
- Reversed cards display rotated 180 degrees through `AOnokoArcanaCardActor`.
- Keywords are visible after draw.
- Study focus remains hidden until `RevealGuide()` succeeds.
- Save reading writes the current reading through the SaveGame layer.
- History refresh loads saved readings and exposes latest/selected summary text.
- Reset clears current draw, user note, and guide state, and returns the card actor to back view.

## Runtime Proof

2026-06-01にUE Editor PIE上で、native fallback HUDによる `Start -> Draw -> Reveal -> note -> Guide -> Save -> History` を実操作確認した。詳細は `reports/phase1-runtime-proof-2026-06-01.md` を参照。

## Known Constraint

Do not use the previous Unreal Python map-generation path as acceptance evidence. It repeatedly hit editor actor-spawn crashes. Manual editor placement or a new automation path should be used for the next visual proof.
