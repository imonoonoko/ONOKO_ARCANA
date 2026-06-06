# ONOKO ARCANA v0.1.2 Release Checklist

Date: 2026-06-07
Target tag: `v0.1.2`
Target repository: `imonoonoko/ONOKO_ARCANA`
Release type: public preview GitHub Release with CI-generated artifact

## Required Gates

- [ ] Static app check: `python scripts/check_web_app.py`
- [ ] Dependency install: `cd web-app && npm ci`
- [ ] Browser smoke: `cd web-app && npm run smoke:web`
- [ ] Keyboard focus smoke: `cd web-app && npm run smoke:keyboard`
- [ ] Visual audit: `cd web-app && npm run audit:visual`
- [ ] Electron smoke: `cd web-app && npm run smoke:electron`
- [ ] Local package build: `cd web-app && npm run package:local`
- [ ] Package smoke: `cd web-app && npm run smoke:package`
- [ ] Release artifact creation: `cd web-app && npm run release:artifact`
- [ ] High-severity dependency audit: `cd web-app && npm audit --audit-level=high`
- [ ] Temporary shortcut smoke: run `dist/onoko-arcana-local/CREATE_DESKTOP_SHORTCUT.ps1` against a temporary Desktop path and verify `IconLocation` uses `onoko-arcana-app-icon-v1.ico`.
- [ ] GitHub Actions success on the release commit.
- [ ] GitHub Actions success on the `v0.1.2` tag.
- [ ] Release zip and `.sha256` downloaded from the tag CI artifact.
- [ ] GitHub Release created as a pre-release/public preview.

## Artifact Rules

- Do not commit generated zip files.
- Do not attach local-only release artifacts when a tag CI artifact is available.
- The zip must include `START_ONOKO_ARCANA.cmd`, `CREATE_DESKTOP_SHORTCUT.ps1`, `LICENSE`, `SECURITY.md`, `DISTRIBUTION_NOTICE.md`, and `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`.
- The Desktop shortcut helper must set `IconLocation` to `assets/generated/app-icons/onoko-arcana-app-icon-v1.ico`.
- The zip must not include non-runtime icon source files such as `onoko-arcana-app-icon-v1-alpha-raw.png` or `onoko-arcana-app-icon-v1-source-chromakey.png`.

## Stop Conditions

- Do not tag from a dirty tracked working tree.
- Do not publish if GitHub Actions fails on the release commit or release tag.
- Do not call the package a signed installer.
- Do not describe Unreal Engine as the active runtime.
- Do not imply third-party reuse rights for generated tarot, HUD, app icon, or ONOKO identity assets.
