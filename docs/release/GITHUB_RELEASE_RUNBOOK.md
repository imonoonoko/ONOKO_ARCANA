# GitHub Release Runbook

This runbook keeps ONOKO ARCANA GitHub Releases reproducible and avoids publishing from an unverified local state.

## Target

- Repository: `imonoonoko/ONOKO_ARCANA`
- Current preview release tag: `v0.1.3`
- Release type: GitHub Release pre-release with attached unsigned Windows installer and fallback local Electron package
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
npm run package:installer
npm run smoke:installer
npm run release:artifact
npm audit --audit-level=high
```

Stop if any check fails.

## Artifact Rules

- Keep generated packages under `dist/`.
- Do not commit generated installer or zip files.
- Prefer the setup executable, fallback zip, and matching `.sha256` files downloaded from the tag CI artifact.
- The setup executable is the primary Windows user artifact.
- The setup executable must be built by `electron-builder` with `win.icon` set to `assets/generated/app-icons/onoko-arcana-app-icon-v1.ico`.
- The installer must create Start Menu/Desktop shortcuts named `ONOKO ARCANA`.
- The fallback zip must include `LICENSE`, `SECURITY.md`, `DISTRIBUTION_NOTICE.md`, and `docs/legal/`.
- The fallback zip must not include non-runtime icon source material.
- Do not describe the package as signed, auto-updating, store-reviewed, or MSIX-distributed.

## Commit And CI Gate

Commit the intended release candidate first, then push and wait for GitHub Actions on that exact commit.

```powershell
git add README.md CHANGELOG.md LICENSE SECURITY.md docs/release docs/legal scripts .github/workflows/ci.yml web-app/package.json web-app/package-lock.json
git commit -m "Prepare ONOKO ARCANA v0.1.3 release"
git push origin main
gh run list --branch main --limit 5
```

Publish only after the release commit has a passing CI run.

## Tag And Release

Create the annotated tag from the CI-green commit. The tag push triggers CI and uploads the release artifact.

```powershell
$tag = "v0.1.3"
git tag -a $tag -m "ONOKO ARCANA $tag"
git push origin $tag

gh run list --workflow CI --limit 10
gh run watch <tag-run-id> --exit-status
gh run download <tag-run-id> `
  --name "onoko-arcana-$tag-release-artifacts" `
  --dir "dist/ci-release-artifacts/$tag"

gh release create $tag `
  "dist/ci-release-artifacts/$tag/onoko-arcana-$tag-setup.exe" `
  "dist/ci-release-artifacts/$tag/onoko-arcana-$tag-setup.exe.sha256" `
  "dist/ci-release-artifacts/$tag/onoko-arcana-$tag-local.zip" `
  "dist/ci-release-artifacts/$tag/onoko-arcana-$tag-local.zip.sha256" `
  --title "ONOKO ARCANA $tag" `
  --notes-file "docs/release/RELEASE_NOTES_$tag.md" `
  --prerelease
```

## Post-Release Check

```powershell
gh release view v0.1.3 --json tagName,name,isDraft,isPrerelease,assets,url
```

Confirm:

- Release is attached to the intended tag.
- Setup executable, fallback zip, and matching `.sha256` files are present.
- Release notes include known limitations and license notes.
- The tag points to the CI-green release commit.

## Manual Installer Path

For release promotion or installer behavior changes, run `docs/release/INSTALLER_MANUAL_SMOKE_CHECKLIST.md` on a clean Windows user or VM. Automated smokes verify packaged resources and launch behavior, but SmartScreen reputation, real shortcut shell display, uninstall cleanup, and antivirus policy are environment-dependent.
