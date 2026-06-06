# ONOKO ARCANA Residual Risk Register

Date: 2026-06-07
Scope: GitHub Release distribution after `v0.1.2`
Target release: `v0.1.3`

## Current Decision

`v0.1.3` changes the recommended GitHub Release artifact from a local zip package to an unsigned Windows installer.

This resolves the practical icon problem for normal users: a GitHub Release downloader should be able to run `onoko-arcana-v0.1.3-setup.exe` and launch ONOKO ARCANA from Desktop or Start Menu shortcuts that use the generated `.ico` icon automatically.

The local zip remains as a fallback artifact for users whose environment blocks the installer.

## Risk Register

| Risk | Prior State | Current State | Owner Action |
|---|---|---|---|
| Desktop shortcut icon not applied for Release users | Users had to run `CREATE_DESKTOP_SHORTCUT.ps1` manually from the zip | Progressed for normal path: installer creates Desktop/Start Menu shortcuts with `onoko-arcana-app-icon-v1.ico` | Verify `npm run package:installer` and `npm run smoke:installer` before publishing |
| Release artifact is only a local folder zip | GitHub Release attached only zip + SHA256 | Progressed: CI now uploads setup executable, fallback zip, and matching SHA256 files | Publish setup executable as primary artifact |
| Unsigned Windows warning | Present | Still present | Do not claim signed distribution; decide later whether to buy/use a code-signing certificate |
| Auto update | Not included | Still intentionally excluded | Do not add auto update before signing/update trust model is defined |
| MSIX/Microsoft Store | Not included | Still excluded | Treat as later channel work after installer feedback |
| Asset reuse ambiguity | Split license docs existed | Maintained: installer/fallback package includes license and attribution docs | Keep `DISTRIBUTION_NOTICE.md` and `docs/legal/` in packaged resources |
| Local history migration | Export/import supported | Still local-first only | Keep export/import as supported backup path; do not promise cloud sync |

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

## Stop Conditions Before v0.1.3 Publication

- Do not publish if `npm run smoke:installer` fails.
- Do not publish if the tag CI artifact lacks `onoko-arcana-v0.1.3-setup.exe`.
- Do not describe the installer as signed.
- Do not enable or advertise auto update.
- Do not remove the fallback zip until the installer path has real user feedback.
