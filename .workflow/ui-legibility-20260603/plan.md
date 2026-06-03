Goal:
Improve the Web/Electron reading table legibility defects reported from screenshots: inaccurate-looking card text, spread icon overflow, low perceived card/text quality, and text sitting too close to decorative frames.

Success criteria:
- Revealed table cards no longer rely on tiny overlaid title/keyword text that can misread card names or numbers.
- Exact card name, number, orientation, slot, keywords, and study focus remain visible in the inspector/guide.
- Spread selector mini icons and count badges stay inside their button column at desktop and mobile widths.
- Text fields, guide rows, history rows, badges, and compact buttons have enough inset from nine-slice decorative borders.
- Existing static and browser smoke checks pass.

Current context:
- Target surface is `web-app/index.html` with `web-app/src/app.js`, `web-app/src/data.js`, and `web-app/src/styles.css`.
- The app is static HTML and can be verified via `python scripts/check_web_app.py` and `scripts/smoke_web_app.cjs`.

Constraints:
- Keep the existing ONOKO dark/gold/blue HUD direction.
- Avoid new dependencies.
- Do not regenerate card assets in this pass.
- Keep changes scoped to Web/Electron UI behavior and polish.

Risks:
- Card art PNGs include their own generated visual details; this pass can improve display quality but cannot fix baked-in image artifacts.
- Dense spreads need small cards, so card-level readable text should live in the inspector instead of the physical card face.

Workflow:
1. Inspect current JS/CSS contracts.
2. Remove misleading tiny table-card inscriptions and surface exact metadata in inspector/guide.
3. Tighten spread chooser icon layout and increase readable content padding around ornate frames.
4. Run static and rendered smoke checks, then inspect screenshots.

Continuation 2026-06-03:
- Generate Web-only labeled card derivatives from the approved V5 alpha cards.
- Keep original V5 source/alpha files untouched for UE and asset QA continuity.
- Switch the Web app front-card image paths to the labeled derivatives after generation passes.
- Update Web checks so missing labeled derivatives fail early.
- Re-run static, visual audit, smoke, and screenshots.

Continuation 2026-06-03 position pass:
- Re-center the red-boxed Web/Electron UI controls against their ornate frames.
- Pull spread mini diagrams, compact action buttons, selected-card badges, and bottom status text away from panel edges.
- Tighten the central one-card stack so the slot label, card, and table caption read as one aligned unit.
- Adjust Web-only baked card label coordinates so title and keyword text sit optically centered inside the parchment plaques.
- Verify with static checks, visual audit, smoke, and a desktop screenshot that waits for card images to load.

Continuation 2026-06-03 offset pass:
- Remove the visible overlap between spread mini diagrams and the decorative/background imagery in the left spread selector.
- Move the baked top card title text slightly upward inside the parchment title plaque.
- Move the baked bottom keyword block slightly downward inside the lower parchment plaque.
- Regenerate Web-only labeled cards and verify with static checks, visual audit, smoke, and an upright one-card screenshot.
