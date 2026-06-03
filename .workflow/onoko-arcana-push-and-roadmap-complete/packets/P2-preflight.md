Packet ID: P2
Objective: Check Git and evidence state before pushing.
Context: Push should preserve the current state without force-push or deletion.
Files / sources: Git status, branch, remote, roadmap/report references.
Ownership: Read-only preflight.
Do: Verify branch, remote, evidence paths, and diff check.
Do not: Stage or commit during this packet.
Expected output: `results/P2-preflight.md`.
Verification: Report documents no blocking issues.
