# Implementation Brief

## C++ Changes

- Add `UOnokoArcanaSpreadReadingViewModel* SpreadViewModel` to `AOnokoArcanaTableController`.
- Add `TArray<AOnokoArcanaCardActor*> SpreadCardActors`.
- Add helpers:
  - `IsOneCardSpread`
  - `IsSpreadReadingActive`
  - `EnsureSpreadViewModel`
  - `EnsureSpreadCardActors`
  - `SyncSpreadCardActors`
  - `PlaceSpreadCardActors`
  - `CaptureLastSpreadError`
- Update existing commands:
  - `StartReading`
  - `DrawCard`
  - `RevealCard`
  - `RevealGuide`
  - `SubmitUserInterpretation`
  - `ResetTable`
  - `SaveCurrentReading`
  - `HasCurrentDraw`

## Verification

- Build game target.
- Build editor target.
- Add and run `test_phase4_table_controller_spread_surface.py`.
- Run:

```text
python scripts/check_phase4_spread_runtime.py
python scripts/check_phase1_preflight.py
```

## Stop Conditions

- If one-card commandlets regress, stop and fix the one-card path.
- If runtime actor spawning in C++ crashes in commandlet, keep the state/HUD bridge and defer visual actor proof to Editor/PIE.
- Do not use Python map actor spawn as the completion proof.
