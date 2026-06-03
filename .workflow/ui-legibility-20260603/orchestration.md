Goal:
Finish the next UI legibility slice by producing accurate high-resolution Web card labels without mutating the approved V5 card source assets.

Success criteria:
- 22 labeled front cards plus the back card are present under `assets/generated/card-production-v5-full/web-labeled/alpha/`.
- Labeled cards retain `1024x1536` size and non-empty alpha.
- Web front-card paths use the labeled derivatives; card back remains available.
- Static and rendered Web checks pass with no console errors.
- Final screenshots show the card text, spread icons, and panel text are readable and contained.

Constraints:
- Do not overwrite `assets/generated/card-production-v5-full/alpha/`.
- Do not change UE import paths in this slice.
- Do not add dependencies.

Packets:
- P1 asset-label pipeline: add deterministic Python generator and derived image report.
- P2 Web integration: point Web cards/checks at derived labeled assets.
- P3 QA: run static, visual, smoke, and screenshot verification.

Integration policy:
Accept deterministic generated assets and narrow code changes only. Reject broad visual redesign, UE edits, or source asset mutation.
