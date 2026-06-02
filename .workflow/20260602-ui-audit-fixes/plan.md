# UI Audit Fixes

Goal:
- Fix the visual issues found by the 2026-06-02 UI visual audit.

Success criteria:
- Dense spreads no longer rely on unreadably small in-card text.
- Slot labels no longer visibly collide with cards or other labels in normal desktop/mobile layouts.
- Mobile dense spreads are readable enough to operate without inspecting tiny card text.
- Right inspector action buttons do not sit on top of section frame borders.
- Spread selector rows keep the ONOKO style but reduce ornamental pressure.
- Static checks, visual audit, web smoke, Electron smoke, and screenshot inspection pass.

Constraints:
- Keep the reading loop and spread data unchanged.
- Reuse existing generated assets.
- Avoid unrelated refactors.

Implementation policy:
- One-card keeps full in-card name/orientation/keywords.
- Three-card keeps readable in-card labels.
- Five or more cards use board markers and external readable text instead of full in-card inscriptions.
- Dense board labels become compact markers; progress/inspector remain the readable detail surfaces.
