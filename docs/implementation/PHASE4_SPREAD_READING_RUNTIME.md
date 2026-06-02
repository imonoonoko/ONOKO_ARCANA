# Phase 4 Spread Reading Runtime

Updated: 2026-06-02

## Purpose

This implementation turns the Phase 3 spread catalog into the first executable multi-card reading flow.

The first target is:

```text
three_card_past_present_future
```

This is a runtime-state slice, not the final UMG/table presentation. It proves that the game can start a three-card spread, draw unique cards, reveal them in spread order, attach notes and guide visibility per slot, and save/load the full spread state.

## Added Runtime Surface

New C++ files:

- `Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadReadingSession.h`
- `Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadReadingSession.cpp`
- `Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadReadingViewModel.h`
- `Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadReadingViewModel.cpp`

New runtime structs:

- `FOnokoArcanaReadingCardState`
- `FOnokoArcanaSpreadReadingState`

Extended SaveGame:

- `FOnokoArcanaSavedReadingCardState`
- `FOnokoArcanaSavedReading::CardStates`
- `UOnokoArcanaReadingSaveGame::SchemaVersion = 2`

The old one-card save fields remain in place. Spread saves fill those summary fields from the selected card while storing every spread slot in `CardStates`.

## Supported Flow

`UOnokoArcanaSpreadReadingSession` supports:

- initialize V5 major arcana deck
- start a reading from any `FOnokoArcanaSpreadDefinition`
- draw all cards for the spread, face-down
- select a slot by `PositionKey`
- reveal selected slot
- reveal the next slot by `RevealOrder`
- store per-slot interpretation text
- store a spread summary note
- reveal guide text only after the selected card is revealed
- reset the reading

`UOnokoArcanaSpreadReadingViewModel` exposes the selected slot title, orientation, keywords, progress text, guide text, interpretation text, and reveal guards for UMG.

## Commandlet Proof

New script:

```text
Unreal/ONOKO_ARCANA/Scripts/test_phase4_three_card_spread_session.py
```

Result:

```text
Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json
```

The test verifies:

- built-in registry contains `three_card_past_present_future`
- start state has three slots and selects `present` by default
- draw creates three unique card ids and keeps all cards face-down
- guide reveal is unavailable before the selected card is revealed
- reveal sequence is `past -> present -> future`
- selected slot note and guide visibility are stored per card
- spread SaveGame conversion stores three card states
- save/load round trip preserves spread id and card count
- ViewModel exposes selected title, guide text, and progress
- reset clears the session
- temporary test save slot is deleted

## Verification

Commands run:

```text
UnrealBuildTool ONOKO_ARCANA Win64 Development -Project=Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject -WaitMutex -NoLiveCoding
UnrealBuildTool ONOKO_ARCANAEditor Win64 Development -Project=Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject -WaitMutex -FromMsBuild -NoLiveCoding
UnrealEditor-Cmd.exe Unreal/ONOKO_ARCANA/ONOKO_ARCANA.uproject -ExecutePythonScript=Unreal/ONOKO_ARCANA/Scripts/test_phase4_three_card_spread_session.py -Unattended -NullRHI -NoSplash -NoSound
```

Expected checker:

```text
python scripts/check_phase4_spread_runtime.py
python scripts/check_phase1_preflight.py
```

Current evidence:

- `Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json` (`ok=true`)
- `reports/phase4-spread-runtime-check-20260601-171741.json` (`ok=true`)
- `reports/phase4-spread-runtime-prep-check-20260601-171741.json` (`ok=true`)
- `reports/phase1-preflight-check-20260601-171749.json` (`ok=true`, warning: missing `.git`)

## Remaining Work

The next implementation slice after the current play-surface bridge should improve the designed UI:

- preserve the existing one-card fallback path
- add a proper `WBP_TableHUD`
- add table card labels and clickable spread-slot selection
- extend visual layouts beyond `three_card_past_present_future`

Do not use Python map actor spawn as the completion proof.

Current play-surface bridge details are tracked in:

```text
docs/implementation/PHASE4_SPREAD_PLAY_SURFACE.md
```
