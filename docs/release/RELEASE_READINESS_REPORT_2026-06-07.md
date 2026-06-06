# ONOKO ARCANA Release Readiness Report

Date: 2026-06-07
Target: `v0.1.0`
Audience: project owner / release operator

## Decision

`v0.1.0` was published successfully as the first GitHub Release.

This report is retained as the release-readiness record for that release. The post-release review is tracked separately in `docs/release/POST_RELEASE_REVIEW_v0.1.0.md`.

## Readiness Dashboard

| Area | Status | Evidence |
|---|---:|---|
| Static app structure | Pass | `reports/web-app-check-20260607-030637.json` |
| Browser app smoke | Pass | `reports/web-app-smoke-20260607-021607.json` |
| Keyboard accessibility smoke | Pass | `reports/keyboard-focus-smoke-20260607-021627.json` |
| Visual layout audit | Pass | `reports/ui-visual-audit-20260607-021627/report.json`, `issueCount: 0` |
| Electron runtime smoke | Pass | `reports/electron-app-smoke-20260607-021627.json` |
| Local package smoke | Pass | `reports/electron-package-smoke-20260607-030701.json` |
| Dependency audit | Pass | `npm audit --audit-level=high`, `found 0 vulnerabilities` |
| Release artifact | Pass | `dist/release-artifacts/onoko-arcana-v0.1.0-local.zip` |
| GitHub Release state | Pass | Published at `https://github.com/imonoonoko/ONOKO_ARCANA/releases/tag/v0.1.0` |
| Open PR state | Ready | No open PRs found |
| Current-commit CI | Pass | GitHub Actions run `27070066993`, commit `bfeaecb6fdac7b6c4ba1cfc7a7ef95c3a639e1cc` |

## Security And Attack-Path Notes

No validated repository security finding was provided for full attack-path analysis. A release-focused security pass was still applied to the active product surface:

- Product surface: local Web/Electron app and generated local package.
- Entry points: local HTML runtime, Electron shell, local import/export JSON, localStorage history and learning state.
- Sensitive data: user-entered questions, interpretation notes, and learning records stored locally.
- Trust boundary: imported JSON crosses from user-controlled file input into app state.
- Existing controls: fixture-backed import handling, invalid JSON smoke coverage, duplicate import handling, local-only storage, and no server-side data flow.
- Dependency check: `npm audit --audit-level=high` reported zero vulnerabilities.

Residual release risks:

- The Electron package is unsigned, so Windows may show trust warnings.
- Release assets are generated under `dist/` and should be attached to GitHub Releases, not committed unless the project intentionally changes generated-artifact policy.
- `v0.1.1` should use a tag CI artifact for the release zip and `.sha256`.
- `v0.1.1` should avoid packaging non-runtime icon source files.

## Release Artifact

Created:

```text
dist/release-artifacts/onoko-arcana-v0.1.0-local.zip
dist/release-artifacts/onoko-arcana-v0.1.0-local.zip.sha256
```

SHA256:

```text
B5D6F11623BFD6DCD69C400B1FAD773DF489059CC289CD57106E593289DC3787  onoko-arcana-v0.1.0-local.zip
```

## Completed Release Steps

1. Release candidate changes were reviewed and committed.
2. Commit `bfeaecb6fdac7b6c4ba1cfc7a7ef95c3a639e1cc` was pushed to `main`.
3. GitHub Actions run `27070066993` passed on that commit.
4. Annotated tag `v0.1.0` was created from that commit.
5. GitHub Release `v0.1.0` was published with the zip plus SHA256 file.
