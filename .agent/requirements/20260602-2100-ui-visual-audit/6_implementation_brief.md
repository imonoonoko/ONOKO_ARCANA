# Implementation Brief After UI Visual Audit

## Highest Priority Fixes

1. Dense-spread card text policy:
   - One-card: keep full in-card name and keywords.
   - Three-card: keep short in-card name, shorten or hide keywords if needed.
   - Five or more cards: replace in-card text with card number/glyph only.
   - Put readable card name/orientation/keywords in slot callouts, progress rail, selected inspector, or a zoom view.

2. Slot label policy:
   - Avoid rotating long Japanese slot labels with the card in dense spreads.
   - For seven-horseshoe and relationship-line, use a board legend or small numbered markers.
   - Reserve decorative plaques for active/selected markers only.

3. Mobile policy:
   - Treat six or more card spreads as guided sequence views.
   - Keep the board preview as visual context, but do not require users to read all cards directly on the board.

4. Inspector polish:
   - Move `ガイド表示` and `書き出し` out of frame edges.
   - Keep disabled text legible and reduce decorative image frame opacity in disabled actions.

## Validation To Run After Fixes

```text
python scripts/check_web_app.py
$env:NODE_PATH='<playwright-node-modules>'
node scripts/audit_web_ui_visual.cjs
node scripts/smoke_web_app.cjs
node scripts/smoke_electron_app.cjs
```
