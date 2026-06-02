# UI Audit Fixes Final Report

Completed: 2026-06-02 21:47 JST

## Implemented

- Switched five-card and larger spreads from full in-card inscriptions to readable slot markers.
- Kept full in-card text for one-card and three-card layouts where it remains readable.
- Removed external board slot plaques for dense spreads to eliminate label/card collisions.
- Moved spread count into the mini spread diagram and removed the right-end count column.
- Reduced inactive spread-row decoration opacity and removed the large side pip overlay.
- Made progress chips wrap instead of requiring horizontal scrolling.
- Increased mobile dense-board card size and table height.
- Moved guide/export actions into their own vertical action rows.
- Updated disabled button contrast.
- Updated `scripts/audit_web_ui_visual.cjs` so it matches the new dense-board design.

## Verification

Static:

```text
reports/web-app-check-20260602-214641.json
```

Visual audit:

```text
reports/ui-visual-audit-20260602-214512/report.json
```

Result:

```text
P1: 0
P2: 0
P3: 51 card-card-overlap
```

The remaining P3 entries are informational: card overlap is intentional in dense tarot spreads such as Celtic cross and arc-shaped layouts.

Web smoke:

```text
reports/web-app-smoke-20260602-214641.json
reports/onoko-arcana-web-app-celtic-20260602-214641.png
reports/onoko-arcana-web-app-mobile-20260602-214641.png
```

Electron smoke:

```text
reports/electron-app-smoke-20260602-214739.json
reports/onoko-arcana-electron-smoke-20260602-214739.png
```

Manual screenshots reviewed:

```text
reports/ui-visual-audit-20260602-214512/desktop-seven-horseshoe.png
reports/ui-visual-audit-20260602-214512/mobile-relationship-line.png
reports/onoko-arcana-web-app-celtic-20260602-214641.png
reports/onoko-arcana-electron-smoke-20260602-214739.png
```
