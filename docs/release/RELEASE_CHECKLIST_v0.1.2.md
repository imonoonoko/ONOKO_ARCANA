# ONOKO ARCANA v0.1.2 Release Checklist

Date: 2026-06-07
Target tag: `v0.1.2`
Target repository: `imonoonoko/ONOKO_ARCANA`
Release type: public preview GitHub Release with CI-generated artifact

## Required Gates

- [x] Static app check: `python scripts/check_web_app.py`
- [x] Dependency install: `cd web-app && npm ci`
- [x] Browser smoke: `cd web-app && npm run smoke:web`
- [x] Keyboard focus smoke: `cd web-app && npm run smoke:keyboard`
- [x] Visual audit: `cd web-app && npm run audit:visual`
- [x] Electron smoke: `cd web-app && npm run smoke:electron`
- [x] Local package build: `cd web-app && npm run package:local`
- [x] Package smoke: `cd web-app && npm run smoke:package`
- [x] Release artifact creation: `cd web-app && npm run release:artifact`
- [x] High-severity dependency audit: `cd web-app && npm audit --audit-level=high`
- [x] Temporary shortcut smoke: run `dist/onoko-arcana-local/CREATE_DESKTOP_SHORTCUT.ps1` against a temporary Desktop path and verify `IconLocation` uses `onoko-arcana-app-icon-v1.ico`.
- [x] GitHub Actions success on the release commit.
- [x] GitHub Actions success on the `v0.1.2` tag.
- [x] Release zip and `.sha256` downloaded from the tag CI artifact.
- [x] GitHub Release created as a pre-release/public preview.

## Completion Evidence

- Release commit: `b3bcbe0592fbeb39f2dfff7b9338a9e9f75d32f1`
- Main CI: `27070913513`, success
- Tag CI: `27070996926`, success
- GitHub Release: `https://github.com/imonoonoko/ONOKO_ARCANA/releases/tag/v0.1.2`
- Release zip: `onoko-arcana-v0.1.2-local.zip`
- Release zip SHA-256: `8ADD96A30C2BE47A27E0F816B31A94768FB76D9EF58D0798754F230083AA9FC0`
- GitHub asset digest: `sha256:8add96a30c2be47a27e0f816b31a94768fb76d9ef58d0798754f230083aa9fc0`

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
