Packet ID: P1
Objective: Inspect current Web app history storage, export shape, and smoke coverage.
Context: Import must preserve the existing reading loop and direct-open runtime.
Files / sources: `web-app/src/app.js`, `web-app/index.html`, `web-app/src/styles.css`, `scripts/check_web_app.py`, `scripts/smoke_web_app.cjs`, `scripts/smoke_electron_app.cjs`.
Ownership: Read-only discovery except for the result note.
Do: Identify export payload shape, relevant DOM hooks, validation needs, and smoke extension points.
Do not: Change implementation files in this packet.
Expected output: `results/P1-discovery.md`.
Verification: Discovery note has clear implementation constraints.
