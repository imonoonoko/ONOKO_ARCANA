# ONOKO ARCANA v0.1.0 Release Checklist

Date: 2026-06-07
Target tag: `v0.1.0`
Target repository: `imonoonoko/ONOKO_ARCANA`
Release type: first formal GitHub Release for the Web/Electron v1.x line

## Scope

- Include the active Web/Electron app under `web-app/`.
- Include local package support under `scripts/package_electron_local.cjs` and `dist/onoko-arcana-local/` as generated output.
- Include Major Arcana assets, app icons, schemas, fixtures, public docs, and smoke/audit scripts.
- Exclude Unreal Engine runtime completion from the release promise. UE files remain archive evidence only.
- Exclude signed installer, auto update, and Minor Arcana support.

## Required Local Gates

- [x] Static app check: `python scripts/check_web_app.py`
- [x] Dependency install: `cd web-app && npm ci`
- [x] Browser smoke: `cd web-app && npm run smoke:web`
- [x] Keyboard focus smoke: `cd web-app && npm run smoke:keyboard`
- [x] Visual audit: `cd web-app && npm run audit:visual`
- [x] Electron smoke: `cd web-app && npm run smoke:electron`
- [x] Local package build: `cd web-app && npm run package:local`
- [x] Package smoke: `cd web-app && npm run smoke:package`
- [x] High-severity dependency audit: `cd web-app && npm audit --audit-level=high`

## Local Evidence

- Static check report: `reports/web-app-check-20260607-030637.json`
- Web smoke report: `reports/web-app-smoke-20260607-021607.json`
- Keyboard smoke report: `reports/keyboard-focus-smoke-20260607-021627.json`
- Visual audit report: `reports/ui-visual-audit-20260607-021627/report.json`
- Electron smoke report: `reports/electron-app-smoke-20260607-021627.json`
- Package smoke report: `reports/electron-package-smoke-20260607-030701.json`
- Release zip: `dist/release-artifacts/onoko-arcana-v0.1.0-local.zip`
- SHA256: `B5D6F11623BFD6DCD69C400B1FAD773DF489059CC289CD57106E593289DC3787`

## GitHub Gates

- [x] GitHub CLI authentication confirmed with `repo` and `workflow` scopes.
- [x] Repository resolved as `imonoonoko/ONOKO_ARCANA`.
- [x] No existing GitHub Release found.
- [x] Open PR list is empty.
- [ ] Commit the release-prep changes.
- [ ] Push to `main` or a release branch.
- [ ] Confirm GitHub Actions CI passes on the pushed commit.
- [ ] Rebuild the local package after `DISTRIBUTION_NOTICE.md`, `LICENSE`, `SECURITY.md`, and `docs/legal/` are included.
- [ ] Confirm the package contains `LICENSE`, `SECURITY.md`, `DISTRIBUTION_NOTICE.md`, and `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`.
- [ ] Create annotated tag `v0.1.0` from the CI-green commit.
- [ ] Publish GitHub Release with `dist/release-artifacts/onoko-arcana-v0.1.0-local.zip` and its `.sha256` file attached.

## Release Commands

Run only after the working tree is intentionally staged and the current commit has green CI.

```powershell
git tag -a v0.1.0 -m "ONOKO ARCANA v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 `
  dist/release-artifacts/onoko-arcana-v0.1.0-local.zip `
  dist/release-artifacts/onoko-arcana-v0.1.0-local.zip.sha256 `
  --title "ONOKO ARCANA v0.1.0" `
  --notes-file docs/release/RELEASE_NOTES_v0.1.0.md
```

## Stop Conditions

- Do not tag from a dirty working tree.
- Do not publish if GitHub Actions fails on the release commit.
- Do not call the package a signed installer.
- Do not describe Unreal Engine as the active runtime.
- Do not imply third-party reuse rights for generated tarot, HUD, app icon, or ONOKO identity assets.
- Do not publish a package that omits the release distribution notice or split-license files.
