# Changelog

All notable release changes are tracked here.

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
