# Discussion Log

## 2026-06-02 03:12 JST

User reported that UE lighting makes the cards look thin/faded and asked to continue the next work while improving/optimizing.

Baseline verified:

- `python scripts/check_phase1_preflight.py`
- Result: OK
- Report: `reports/phase1-preflight-check-20260601-181128.json`
- Warning: `.git` missing

- `python scripts/check_phase4_play_surface.py`
- Result: OK
- Report: `reports/phase4-play-surface-check-20260601-181128.json`

Finding:

- Runtime card actors use `/Game/ONOKOArcana/Phase1/Materials/M_Phase1_CardMasked_TextureParam`.
- The material creation script connected the texture RGB to `BaseColor`, so the visible card body can be affected by scene lighting/exposure.
- Existing roadmap material policy already recommends `Unlit Masked` for alpha/debug isolation.

Decision:

- Keep the masked alpha silhouette.
- Move the runtime card material to Unlit Masked with texture RGB driving Emissive Color.
- Continue the next visible improvement by adding Past / Present / Future table labels near the three cards.

Implemented:

- `Unreal/ONOKO_ARCANA/Scripts/ensure_phase1_runtime_materials.py` now normalizes the runtime card material to Unlit Masked and writes `Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json`.
- `AOnokoArcanaTableController` now spawns and syncs `SpreadSlotLabelActors` for `PAST`, `PRESENT`, and `FUTURE`.
- The first label pass exposed default TextRender Japanese font limitations, so table labels were switched to English until a designed UMG/world-widget label layer exists.

Final evidence:

- Screenshot: `reports/onoko-arcana-card-visibility-labels-printwindow-20260602-031850.png`
- `Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json`: `ok=true`, `BLEND_MASKED`, `MSM_UNLIT`
- `Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json`: `ok=true`
- `Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json`: `ok=true`
- `reports/phase4-play-surface-check-20260601-182133.json`: `ok=true`
- `reports/phase1-preflight-check-20260601-182133.json`: `ok=true`, warning: missing `.git`
