# Implementation Brief

## Material

- Update `ensure_phase1_runtime_materials.py` so existing material assets are normalized, not just created.
- Set:
  - `blend_mode = BLEND_MASKED`
  - `shading_model = MSM_UNLIT`
  - `two_sided = true`
  - `opacity_mask_clip_value = 0.333`
- Connect texture RGB through a brightness multiply into `MP_EMISSIVE_COLOR`.
- Keep texture alpha connected to `MP_OPACITY_MASK`.

## Labels

- Add text-render labels owned by `AOnokoArcanaTableController`.
- Sync labels from spread slot display names.
- Place labels near card actors along the same Y layout.

## Verification

- Run material commandlet.
- Build Game and Editor targets.
- Run HUD/runtime commandlets.
- Run preflight and play-surface checks.
- Capture screenshot.
