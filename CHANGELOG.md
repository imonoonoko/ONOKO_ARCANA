# Changelog

All notable release changes are tracked here.

## v0.1.2 - 2026-06-07

Desktop shortcut icon patch for the public preview package.

### Fixed

- Added `CREATE_DESKTOP_SHORTCUT.ps1` to the local Electron package so Windows Desktop shortcuts can target the app directly while using the generated ONOKO ARCANA `.ico`.
- Updated package smoke and release artifact validation so the shortcut script and `.ico` icon assignment are checked before release.
- Updated the local `ONOKO ARCANA.lnk` shortcut on this machine to use `assets/generated/app-icons/onoko-arcana-app-icon-v1.ico`.

## v0.1.1 - 2026-06-07

Corrective public preview release after the first GitHub Release.

### Fixed

- Updated release documentation so the readiness report no longer contradicts the published `v0.1.0` state.
- Added Japanese quick-start and clearer unsigned-package guidance to release notes.
- Added explicit use-disclaimer language for medical, legal, financial, safety, and mental-health decisions.
- Removed non-runtime app-icon source files from the generated local package.
- Added a reproducible release-artifact script and tag CI artifact upload path.

## v0.1.0 - 2026-06-07

Initial formal GitHub Release candidate for the ONOKO ARCANA Web/Electron v1.x line.

### Added

- Web/Electron 2D tarot reading table as the active runtime.
- Major Arcana deck support with 23 card assets, including the shared back card.
- Six spreads: one card, three card, five card cross, seven card horseshoe, Celtic cross, and relationship line.
- Reading flow with question entry, card draw, reveal order, upright/reversed state, user notes, study sheet, save, review, export, import, and delete.
- Learning support with study lens, slot interpretation drill, recall practice, and learning state fixture coverage.
- Local Electron package output with app icon and Windows launcher.
- Public repository hygiene: README, contributing notes, security policy, split license, issue templates, and CI.

### Verification

- `python scripts/check_web_app.py`
- `cd web-app && npm ci`
- `cd web-app && npm run smoke:web`
- `cd web-app && npm run smoke:keyboard`
- `cd web-app && npm run audit:visual`
- `cd web-app && npm run smoke:electron`
- `cd web-app && npm run package:local`
- `cd web-app && npm run smoke:package`
- `cd web-app && npm audit --audit-level=high`

### Known Limitations

- The packaged app is an unsigned local Electron folder package, not a signed installer.
- Auto update is not included.
- Minor Arcana cards are intentionally out of scope for this release.
- Unreal Engine work remains archived evidence and is not part of the v0.1.x runtime.
