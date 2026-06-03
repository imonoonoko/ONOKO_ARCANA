Accepted:
- Generated Web-only labeled derivatives for all 22 major arcana cards plus the shared card back.
- Switched Web front-card image paths to `assets/generated/card-production-v5-full/web-labeled/alpha/`.
- Updated `scripts/check_web_app.py` to require the labeled derivatives.
- Updated `scripts/audit_web_ui_visual.cjs` for the current `.card-table-caption` and `.spread-mini-count` UI contracts.
- Updated card-facing and Web-facing display numbers to tarot-style Roman numerals (`XVIII 月` instead of `18 月`).
- Rebuilt the card label layout with wider internal margins around the title and keyword text.
- Switched card-label rendering to a bolder Japanese font and anchor-based vertical centering to reduce blur and top/bottom drift.
- Re-centered the red-boxed Web/Electron controls: topbar content, spread mini diagrams, slot labels, table captions, selected-card badges, guide/export buttons, and bottom status.
- Increased the one-card table card size so baked card text is clearer in the main reading view.
- Switched card-label text placement to visual-bounds centering so title and keyword lines sit optically centered inside the parchment plaques.

Rejected:
- No mutation of the approved V5 source alpha card images.
- No UE import path changes in this slice.
- No new dependencies.

Verification:
- `scripts/build_web_labeled_cards.py`: generated 22 labeled fronts plus card back.
- `python scripts/check_web_app.py`: OK, 23 source assets and 23 Web-labeled assets found.
- `node scripts/audit_web_ui_visual.cjs`: OK, 13 cases, issueCount 0.
- `node scripts/smoke_web_app.cjs`: OK, desktop and mobile screenshots, no console errors.
- Position pass `python scripts/check_web_app.py`: OK, report `reports/web-app-check-20260603-022941.json`.
- Position pass `node scripts/audit_web_ui_visual.cjs`: OK, 13 cases, issueCount 0, report `reports/ui-visual-audit-20260603-022941/report.json`.
- Position pass `node scripts/smoke_web_app.cjs`: OK, report `reports/web-app-smoke-20260603-022941.json`.
- Position pass desktop screenshot: `reports/onoko-arcana-web-app-one-card-upright-position-fix-2026-06-02T1732.png`.
- Offset pass adjusted spread mini diagram backing so the left selector icons no longer visually merge with the row/background frame.
- Offset pass moved the Web-only baked top title text upward and the lower keyword block downward.
- Offset pass regenerated all Web-only labeled cards.
- Offset pass `python scripts/check_web_app.py`: OK, report `reports/web-app-check-20260603-024204.json`.
- Offset pass `node scripts/audit_web_ui_visual.cjs`: OK, 13 cases, issueCount 0, report `reports/ui-visual-audit-20260603-024205/report.json`.
- Offset pass `node scripts/smoke_web_app.cjs`: OK, report `reports/web-app-smoke-20260603-024205.json`.
- Offset pass Lovers screenshot: `reports/onoko-arcana-web-app-lovers-offset-fix-2026-06-02T1743.png`.
- Browser loopback check: labeled 1024x1536 card image loaded from `web-labeled/alpha`, mini count contained, no console warnings/errors.
- Moon fixed-state screenshot: `XVIII 月` restored and displayed from `major-18-moon-onoko-v5-alpha.png`.
- Tower fixed-state screenshot: `XVI 塔` verified with the revised bold, centered label layout.

Remaining risks:
- This is deterministic text overlay on the current V5 art. It improves text accuracy and display quality, but does not regenerate or repaint the underlying card illustrations.
