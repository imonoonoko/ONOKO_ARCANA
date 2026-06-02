# Discussion Log

## 2026-06-02 02:29 JST

User asked to continue the next implementation work as far as possible after seeing the current UE play-window screenshot.

Baseline verified before this slice:

- `python scripts/check_phase1_preflight.py`
- Result: OK
- Report: `reports/phase1-preflight-check-20260601-172736.json`
- Warning: `.git` missing

- `python scripts/check_phase4_spread_runtime.py`
- Result: OK
- Report: `reports/phase4-spread-runtime-check-20260601-172736.json`

Decision:

- Implement the next slice as the first play-surface connection for `three_card_past_present_future`.
- Preserve the existing one-card path.
- Add multi-card behavior only when `ActiveSpreadId != one_card`.
- Prefer C++ runtime actor spawning/placement for proof; do not use Python map actor spawn as completion evidence.
- Keep UMG changes limited to the native fallback HUD until a proper designed `WBP_TableHUD` is introduced.

## 2026-06-02 02:45 JST

Implementation progress:

- `AOnokoArcanaTableController` now owns `SpreadViewModel` and runtime `SpreadCardActors`.
- Existing table commands branch to spread runtime when a multi-card spread is selected.
- `AOnokoArcanaTableHudWidget` reads spread ViewModel text for active multi-card spreads.
- `AOnokoArcanaPlayerController` supports `-ONOKOArcanaAutoThreeCardDemo` for local visual proof.
- Three runtime card actors are visible in the game window for `three_card_past_present_future`.

Fixes made during the slice:

- Removed explicit spread actor spawn names after UE crashed while trying to uniquify `BP_Auto_SpreadCard_0`.
- Switched spread layout from world X to world Y so the top-down camera shows Past / Present / Future horizontally.
- Added a center offset so the left card does not sit under the native HUD panel.

Evidence:

- Screenshot: `reports/onoko-arcana-three-card-demo-printwindow-20260602-024341.png`
- Phase 4 play-surface check: `reports/phase4-play-surface-check-20260601-174703.json`
- Phase 4 runtime check: `reports/phase4-spread-runtime-check-20260601-174457.json`
- Phase 1 preflight: `reports/phase1-preflight-check-20260601-174703.json`
