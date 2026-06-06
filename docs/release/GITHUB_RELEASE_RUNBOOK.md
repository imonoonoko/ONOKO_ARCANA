# GitHub Release Runbook

This runbook keeps ONOKO ARCANA GitHub Releases reproducible and avoids publishing from an unverified local state.

## Target

- Repository: `imonoonoko/ONOKO_ARCANA`
- First release tag: `v0.1.0`
- Release type: GitHub Release with attached unsigned local Electron package
- Artifact source: `dist/release-artifacts/onoko-arcana-v0.1.0-local.zip`

## Preflight

Run from the repository root unless noted.

```powershell
git status --short
python scripts/check_web_app.py
cd web-app
npm ci
npm run smoke:web
npm run smoke:keyboard
npm run audit:visual
npm run smoke:electron
npm run package:local
npm run smoke:package
npm audit --audit-level=high
```

Stop if any check fails.

## Artifact Rules

- Keep generated packages under `dist/`.
- Do not commit generated zip files.
- Attach the zip and `.sha256` file to the GitHub Release.
- The package must include `LICENSE`, `SECURITY.md`, `DISTRIBUTION_NOTICE.md`, and `docs/legal/`.
- Do not describe the package as signed, installed, auto-updating, or store-reviewed.

## Commit And CI Gate

Commit the intended release candidate first, then push and wait for GitHub Actions on that exact commit.

```powershell
git add README.md LICENSE SECURITY.md docs/release docs/legal scripts/package_electron_local.cjs
git commit -m "Prepare v0.1.0 GitHub release"
git push origin main
gh run list --branch main --limit 5
```

Publish only after the release commit has a passing CI run.

## Tag And Release

Create the annotated tag from the CI-green commit.

```powershell
git tag -a v0.1.0 -m "ONOKO ARCANA v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 `
  dist/release-artifacts/onoko-arcana-v0.1.0-local.zip `
  dist/release-artifacts/onoko-arcana-v0.1.0-local.zip.sha256 `
  --title "ONOKO ARCANA v0.1.0" `
  --notes-file docs/release/RELEASE_NOTES_v0.1.0.md
```

## Post-Release Check

```powershell
gh release view v0.1.0 --json tagName,name,isDraft,isPrerelease,assets,url
```

Confirm:

- Release is attached to `v0.1.0`.
- Zip and `.sha256` are present.
- Release notes include known limitations and license notes.
- The tag points to the CI-green release commit.
