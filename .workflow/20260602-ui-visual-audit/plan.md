# UI Visual Audit

Goal:
- Find readability, image quality, overlap, clipping, and layout problems in the current ONOKO ARCANA Web/Electron UI.

Success criteria:
- Capture current rendered screenshots across all spreads and representative desktop/mobile viewports.
- Detect obvious DOM-level text overflow, small text, horizontal overflow, and element intersections.
- Manually inspect the most relevant screenshots and user-provided problem areas.
- Produce a prioritized issue list with reproduction evidence and suggested next fixes.

Scope:
- `web-app/index.html`
- `web-app/src/app.js`
- `web-app/src/styles.css`
- generated screenshots under `reports/`

Non-goals:
- Do not fix UI defects in this audit pass.
- Do not change tarot data or reading behavior.
- Do not revisit Unreal implementation.

Work packets:
- Requirements: define audit acceptance and severity.
- Instrumentation: create a reusable Playwright visual audit script.
- Evidence: run desktop/mobile captures.
- Review: inspect screenshots and integrate findings.
- Report: write a final audit with priorities.

Severity:
- P0: blocks use or prevents core reading.
- P1: visibly harms readability or causes clear overlap in normal use.
- P2: noticeable polish or dense-layout problem.
- P3: minor tuning or future scalability issue.
