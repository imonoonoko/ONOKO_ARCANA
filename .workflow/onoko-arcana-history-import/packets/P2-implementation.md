Packet ID: P2
Objective: Add history import behavior to the Web/Electron MVP.
Context: Current export is JSON and history is stored under `onoko-arcana:desktop:history:v1`.
Files / sources: `web-app/index.html`, `web-app/src/app.js`, `web-app/src/styles.css`, possibly `scripts/check_web_app.py`.
Ownership: Web app UI and import logic.
Do: Add import control, parse and validate JSON, merge without repeated duplicates, update status text, keep export behavior.
Do not: Add package dependencies, change deck/spread semantics, or rework unrelated UI.
Expected output: Focused code diff.
Verification: Static check passes.
