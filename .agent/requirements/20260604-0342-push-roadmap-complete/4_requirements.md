# Requirements

## Functional Requirements

- The current working tree must be captured in a normal Git commit.
- The commit must be pushed to `origin/main`.
- The roadmap must include current status, phases, quality gates, risks, and next actions.
- The roadmap must treat Web/Electron as the current mainline and Unreal as a held premium lane.
- The workflow final report must include the commit hash and verification summary.

## Acceptance Criteria

- `git push origin main` succeeds.
- `git status --short` is clean after push.
- `docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md` exists.
- The roadmap references existing current evidence reports.
- Workflow verification passes for `.workflow/onoko-arcana-push-and-roadmap-complete`.

## Risks

- Remote push may fail if credentials are unavailable.
- Remote push may fail if `origin/main` moved.
- Generated report files may make the checkpoint large or noisy, but they are
  intentionally part of the current evidence set.
