# HUD Readability And Table Image Pass

Goal:
- Improve the current Web/Electron play screen so the spread selector, table surface, and card presentation read clearly in the actual rendered game screen.

Success criteria:
- The left spread list and status counters remain readable at desktop and mobile widths.
- Card slots no longer show transparent blue HUD panels around revealed cards.
- Revealed card text uses the card art's own top and bottom label areas.
- The central table uses an image-based table background instead of a mostly transparent/grid HUD surface.
- Static checks, browser smoke, Electron smoke, and screenshot review pass.

Current context:
- The app already uses image-based 9-slice HUD frames.
- The user screenshot shows the red-framed left HUD area is cramped, the card keeps extra transparent blue framing, and the central area still reads as a HUD grid.

Constraints:
- Keep the verified reading loop unchanged.
- Reuse existing generated HUD/background assets.
- Avoid destructive edits and unrelated refactors.

Work packets:
- UI contract: capture concrete acceptance criteria.
- Implementation: CSS and render markup changes.
- QA: static check, Playwright screenshots, Electron screenshot, visual inspection, then iterate.

Verification:
- `python scripts/check_web_app.py`
- `node scripts/smoke_web_app.cjs`
- `node scripts/smoke_electron_app.cjs`
- Manual screenshot inspection with desktop, mobile, and Electron captures.
