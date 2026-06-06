# ONOKO ARCANA Release Readiness Report

Date: 2026-06-07
Target: `v0.1.0`
Audience: project owner / release operator

## Decision

The current checkout is locally release-ready for a first GitHub Release candidate after the existing working-tree changes are intentionally committed and CI is rerun on the pushed commit.

Do not publish the GitHub Release yet from the current dirty tree. The local gates are green, but GitHub Actions has not run against the current uncommitted release candidate.

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
| GitHub Release state | Ready | No existing release found |
| Open PR state | Ready | No open PRs found |
| Current-commit CI | Blocked | Must push the release commit and wait for CI |

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
- The package must be rebuilt after release notice and license-file inclusion changes so the published zip contains `LICENSE`, `SECURITY.md`, `DISTRIBUTION_NOTICE.md`, and `docs/legal/`.
- CI must run after committing because the latest remote CI success is from commit `01407b4`, before the current working-tree changes.

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

## Required Next Step

1. Review and commit the release candidate changes.
2. Push the release commit.
3. Confirm GitHub Actions CI passes on that exact commit.
4. Create annotated tag `v0.1.0`.
5. Publish GitHub Release using `docs/release/RELEASE_NOTES_v0.1.0.md` and attach the zip plus SHA256 file.
