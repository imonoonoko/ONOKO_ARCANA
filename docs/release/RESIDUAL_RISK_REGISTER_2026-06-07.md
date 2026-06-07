# ONOKO ARCANA Residual Risk Register

Date: 2026-06-07
Scope: GitHub Release distribution after `v0.1.3` and post-release support hardening
Target release: `v0.1.3`

## Current Decision

`v0.1.3` changes the recommended GitHub Release artifact from a local zip package to an unsigned Windows installer.

This is expected to resolve the practical icon problem for the normal installer path: a GitHub Release downloader should be able to run `onoko-arcana-v0.1.3-setup.exe` and launch ONOKO ARCANA from Desktop or Start Menu shortcuts that use the generated `.ico` icon automatically. Clean Windows user/VM confirmation is still pending.

The local zip remains as a fallback artifact for users whose environment blocks the installer.

## v0.1.3 Outcome

Published GitHub Release:

```text
https://github.com/imonoonoko/ONOKO_ARCANA/releases/tag/v0.1.3
```

Evidence:

- Release commit: `27b4435dd84d652bf9ef6ec72d55b211ac130e3e`
- Main CI: `27071854833`, success
- Tag CI: `27071948735`, success
- Setup artifact: `onoko-arcana-v0.1.3-setup.exe`
- Setup SHA-256: `209930B6168ED965EBF0C418548286471B64F3B7006070AC9EDBFDC4DBE3051A`
- Fallback zip: `onoko-arcana-v0.1.3-local.zip`
- Fallback zip SHA-256: `5797BD67B784D38757B802F4072ECC3A6191DE1F993FBFF7D74D989BEC1DCA02`
- Post-release support hardening commit: `9a4b0420dfc9c31862d51618bd63e628b1967a6c`
- Post-release support hardening CI: `27072878818`, success

The setup executable was confirmed `NotSigned` by Authenticode inspection, matching the release notes.

Manual clean Windows install/uninstall smoke has not been run in the current environment. Treat the installer path as automated-verified public preview until `docs/release/INSTALLER_MANUAL_SMOKE_CHECKLIST.md` is completed on a clean Windows user or VM.

## Risk Register

| Risk | Prior State | Current State | Owner Action |
|---|---|---|---|
| Desktop shortcut icon not applied for Release users | Users had to run `CREATE_DESKTOP_SHORTCUT.ps1` manually from the zip | Automated verified for packaged installer config; clean Windows shortcut display pending | Keep manual checklist open until Desktop/Start Menu icon is confirmed on clean Windows |
| Release artifact is only a local folder zip | GitHub Release attached only zip + SHA256 | Progressed: CI now uploads setup executable, fallback zip, and matching SHA256 files | Publish setup executable as primary artifact |
| Unsigned Windows warning | Present | Still present | Do not claim signed distribution; decide later whether to buy/use a code-signing certificate |
| Auto update | Not included | Still intentionally excluded | Do not add auto update before signing/update trust model is defined |
| MSIX/Microsoft Store | Not included | Still excluded | Treat as later channel work after installer feedback |
| Asset reuse ambiguity | Split license docs existed | Maintained: installer/fallback package includes license and attribution docs | Keep `DISTRIBUTION_NOTICE.md` and `docs/legal/` in packaged resources |
| Local history migration | Export/import supported | Still local-first only | Keep export/import as supported backup path; do not promise cloud sync |

## Immediate Mitigations Added After v0.1.3

These are low-cost mitigations that can be shipped before code signing, MSIX, Microsoft Store, or auto update work.

- Settings now exposes the current app version, official latest GitHub Release URL, repository URL, security policy URL, and license/asset attribution URL.
- Settings now warns that the installer is unsigned and that auto update is not included.
- Settings now tells users to export history and learning data before updating, moving PCs, uninstalling, or deleting local data.
- Electron opens only `https://github.com/imonoonoko/ONOKO_ARCANA` links externally; other new-window or external navigation attempts are denied.
- Browser, Electron, local package, and installer smokes now assert the Release/Support settings remain present.
- Manual install/uninstall verification is tracked in `docs/release/INSTALLER_MANUAL_SMOKE_CHECKLIST.md` and remains pending until a clean Windows user/VM is available.

## Verification Added

- `web-app/package.json`
  - `package:installer`
  - `smoke:installer`
  - `build.win.icon`
  - `build.nsis.createDesktopShortcut`
  - `build.nsis.createStartMenuShortcut`

- `scripts/smoke_electron_installer_app.cjs`
  - Confirms installer artifacts exist.
  - Confirms packaged resources include app icon, card assets, distribution notice, and license attribution.
  - Launches `dist/installer/win-unpacked/ONOKO ARCANA.exe`.
  - Confirms app flow and image loading work from the packaged executable.

- `.github/workflows/ci.yml`
  - Builds and smokes installer package before tag artifact upload.
  - Uploads setup executable, fallback zip, and matching SHA256 files on tag builds.

## Stop Conditions For Future Release Publication

- Do not publish if `npm run smoke:installer` fails.
- Do not publish if the tag CI artifact lacks the expected setup executable.
- Do not describe the installer as signed.
- Do not enable or advertise auto update.
- Do not remove the fallback zip until the installer path has real user feedback.
- Do not promote the installer out of public preview language until clean Windows manual smoke has been completed.
