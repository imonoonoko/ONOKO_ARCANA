# UI Visual Audit Requirements

## Goal

Find the current UI defects that would make ONOKO ARCANA hard to read or feel visually unfinished.

## Acceptance Criteria

- Audit at least all six spreads on desktop.
- Audit representative mobile layouts.
- Check the latest image-based HUD state, including card inscriptions and table image background.
- Save screenshots and a JSON report under `reports/`.
- Produce a prioritized list of findings with evidence paths.

## Non-Goals

- Do not implement fixes in this pass.
- Do not change card generation assets.
- Do not change reading flow logic.

## Risk Areas

- Card text is now inside the artwork and can become too small on dense spreads.
- Decorative image frames can crowd Japanese text.
- Right inspector section buttons can visually collide with panel frames.
- Mobile stacks can hide overlap problems behind vertical scrolling.
