# ONOKO ARCANA v0.1.3 Release Checklist

Date: 2026-06-07
Target tag: `v0.1.3`
Target repository: `imonoonoko/ONOKO_ARCANA`
Release type: public preview GitHub Release with CI-generated unsigned installer and fallback local package

## Required Gates

- [x] Static app check: `python scripts/check_web_app.py`
- [x] Dependency install: `cd web-app && npm ci`
- [x] Browser smoke: `cd web-app && npm run smoke:web`
- [x] Keyboard focus smoke: `cd web-app && npm run smoke:keyboard`
- [x] Visual audit: `cd web-app && npm run audit:visual`
- [x] Electron smoke: `cd web-app && npm run smoke:electron`
- [x] Local package build: `cd web-app && npm run package:local`
- [x] Package smoke: `cd web-app && npm run smoke:package`
- [x] Installer package build: `cd web-app && npm run package:installer`
- [x] Installer package smoke: `cd web-app && npm run smoke:installer`
- [x] Release artifact creation: `cd web-app && npm run release:artifact`
- [x] High-severity dependency audit: `cd web-app && npm audit --audit-level=high`
- [x] GitHub Actions success on the release commit.
- [x] GitHub Actions success on the `v0.1.3` tag.
- [x] Installer, fallback zip, and matching `.sha256` files downloaded from the tag CI artifact.
- [x] GitHub Release created as a pre-release/public preview.

## Local Evidence

- Static check report: `reports/web-app-check-20260607-042415.json`
- Browser smoke report: `reports/web-app-smoke-20260607-042438.json`
- Keyboard smoke report: `reports/keyboard-focus-smoke-20260607-042457.json`
- Visual audit report: `reports/ui-visual-audit-20260607-042457/report.json`, `issueCount: 0`
- Electron smoke report: `reports/electron-app-smoke-20260607-042457.json`
- Local package smoke report: `reports/electron-package-smoke-20260607-042539.json`
- Installer smoke report: `reports/onoko-arcana-installer-smoke-20260607-042713.json`
- Installer artifact: `dist/release-artifacts/onoko-arcana-v0.1.3-setup.exe`
- Installer SHA-256: `396D24FD19ED5537A071A16E9892EBB50A8FF9B4B8611FB3D27319CEF4841F5D`
- Installer Authenticode status: `NotSigned`
- Fallback zip artifact: `dist/release-artifacts/onoko-arcana-v0.1.3-local.zip`
- Fallback zip SHA-256: `9B235354851D98B20B3D9EB4E45488CBFE4D72B8CF5DDA2E87DE21E60FBAB9D0`

## Completion Evidence

- Release commit: `27b4435dd84d652bf9ef6ec72d55b211ac130e3e`
- Main CI: `27071854833`, success
- Tag CI: `27071948735`, success
- GitHub Release: `https://github.com/imonoonoko/ONOKO_ARCANA/releases/tag/v0.1.3`
- Release setup artifact: `onoko-arcana-v0.1.3-setup.exe`
- Release setup SHA-256: `209930B6168ED965EBF0C418548286471B64F3B7006070AC9EDBFDC4DBE3051A`
- Release setup GitHub asset digest: `sha256:209930b6168ed965ebf0c418548286471b64f3b7006070ac9edbfdc4dbe3051a`
- Release fallback zip: `onoko-arcana-v0.1.3-local.zip`
- Release fallback zip SHA-256: `5797BD67B784D38757B802F4072ECC3A6191DE1F993FBFF7D74D989BEC1DCA02`
- Release fallback zip GitHub asset digest: `sha256:5797bd67b784d38757b802f4072ecc3a6191de1f993fbff7d74d989bec1dca02`
- Release type: pre-release/public preview

## Artifact Rules

- Do not commit generated installer or zip files.
- Do not attach local-only release artifacts when a tag CI artifact is available.
- The installer must be named `onoko-arcana-v0.1.3-setup.exe`.
- The installer must create Desktop and Start Menu shortcuts named `ONOKO ARCANA`.
- The installer must use `assets/generated/app-icons/onoko-arcana-app-icon-v1.ico` as the app icon.
- The fallback zip must include `START_ONOKO_ARCANA.cmd`, `CREATE_DESKTOP_SHORTCUT.ps1`, `LICENSE`, `SECURITY.md`, `DISTRIBUTION_NOTICE.md`, and `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`.
- The fallback zip must not include non-runtime icon source files such as `onoko-arcana-app-icon-v1-alpha-raw.png` or `onoko-arcana-app-icon-v1-source-chromakey.png`.

## Stop Conditions

- Do not tag from a dirty tracked working tree.
- Do not publish if GitHub Actions fails on the release commit or release tag.
- Do not call the installer signed.
- Do not enable or advertise auto update before code signing is decided.
- Do not call this an MSIX or Microsoft Store release.
- Do not describe Unreal Engine as the active runtime.
- Do not imply third-party reuse rights for generated tarot, HUD, app icon, or ONOKO identity assets.

## Residual Risks After This Release

- The installer remains unsigned until a code-signing certificate and signing workflow are added.
- Auto update remains intentionally disabled because unsigned update channels would create avoidable trust and tampering risk.
- MSIX/Microsoft Store distribution remains a separate packaging and identity task.
- Minor Arcana content remains out of scope for this preview.
