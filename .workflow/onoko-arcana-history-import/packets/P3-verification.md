Packet ID: P3
Objective: Prove import behavior and regression safety.
Context: Smoke tests already cover reading, guide, save, export, and Electron startup.
Files / sources: `scripts/smoke_web_app.cjs`, `scripts/smoke_electron_app.cjs`, `reports/`.
Ownership: Test/smoke updates and report capture.
Do: Extend Web smoke for export -> clear -> import -> restore if feasible; run static, Web smoke, Electron smoke.
Do not: Over-broaden tests beyond the import contract.
Expected output: New report paths and result note.
Verification: Passing reports.
