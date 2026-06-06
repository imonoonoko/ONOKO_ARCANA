# GitHub Release Runbook

This runbook keeps ONOKO ARCANA GitHub Releases reproducible and avoids publishing from an unverified local state.

## Target

- Repository: `imonoonoko/ONOKO_ARCANA`
- Current preview release tag: `v0.1.1`
- Release type: GitHub Release pre-release with attached unsigned local Electron package
- Artifact source: GitHub Actions tag artifact

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
npm run release:artifact
npm audit --audit-level=high
```

Stop if any check fails.

## Artifact Rules

- Keep generated packages under `dist/`.
- Do not commit generated zip files.
- Prefer the zip and `.sha256` downloaded from the tag CI artifact.
- The package must include `LICENSE`, `SECURITY.md`, `DISTRIBUTION_NOTICE.md`, and `docs/legal/`.
- The package must not include non-runtime icon source material.
- Do not describe the package as signed, installed, auto-updating, or store-reviewed.

## Commit And CI Gate

Commit the intended release candidate first, then push and wait for GitHub Actions on that exact commit.

```powershell
git add README.md CHANGELOG.md LICENSE SECURITY.md docs/release docs/legal scripts .github/workflows/ci.yml web-app/package.json web-app/package-lock.json
git commit -m "Prepare ONOKO ARCANA v0.1.1 release"
git push origin main
gh run list --branch main --limit 5
```

Publish only after the release commit has a passing CI run.

## Tag And Release

Create the annotated tag from the CI-green commit. The tag push triggers CI and uploads the release artifact.

```powershell
$tag = "v0.1.1"
git tag -a $tag -m "ONOKO ARCANA $tag"
git push origin $tag

gh run list --workflow CI --limit 10
gh run watch <tag-run-id> --exit-status
gh run download <tag-run-id> `
  --name "onoko-arcana-$tag-release-artifacts" `
  --dir "dist/ci-release-artifacts/$tag"

gh release create $tag `
  "dist/ci-release-artifacts/$tag/onoko-arcana-$tag-local.zip" `
  "dist/ci-release-artifacts/$tag/onoko-arcana-$tag-local.zip.sha256" `
  --title "ONOKO ARCANA $tag" `
  --notes-file "docs/release/RELEASE_NOTES_$tag.md" `
  --prerelease
```

## Post-Release Check

```powershell
gh release view v0.1.1 --json tagName,name,isDraft,isPrerelease,assets,url
```

Confirm:

- Release is attached to the intended tag.
- Zip and `.sha256` are present.
- Release notes include known limitations and license notes.
- The tag points to the CI-green release commit.
