# ONOKO ARCANA v0.1.0

ONOKO ARCANA v0.1.0 is the first formal GitHub Release candidate for the local-first Web/Electron tarot study app.

## Highlights

- 2D Web/Electron tarot reading table is the active app runtime.
- Major Arcana reading flow supports question entry, spread selection, draw, ordered reveal, upright/reversed state, interpretation notes, study sheet comparison, history save, review, import, export, and delete.
- Learning tools include study lens, slot interpretation drill, recall practice, and learning-state fixture coverage.
- Six spreads are available: one card, three card, five card cross, seven card horseshoe, Celtic cross, and relationship line.
- Local Electron folder package is available for Windows local use through `START_ONOKO_ARCANA.cmd`.

## Download

Attach these files to the GitHub Release:

- `onoko-arcana-v0.1.0-local.zip`
- `onoko-arcana-v0.1.0-local.zip.sha256`

SHA256:

```text
B5D6F11623BFD6DCD69C400B1FAD773DF489059CC289CD57106E593289DC3787  onoko-arcana-v0.1.0-local.zip
```

After downloading, compare the zip against the `.sha256` file when possible.

## Verification

The release candidate was checked locally on 2026-06-07 with:

- `python scripts/check_web_app.py`
- `cd web-app && npm ci`
- `cd web-app && npm run smoke:web`
- `cd web-app && npm run smoke:keyboard`
- `cd web-app && npm run audit:visual`
- `cd web-app && npm run smoke:electron`
- `cd web-app && npm run package:local`
- `cd web-app && npm run smoke:package`
- `cd web-app && npm audit --audit-level=high`

## Known Limitations

- This release provides an unsigned local Electron folder package, not a signed installer.
- Auto update is not included.
- Minor Arcana cards are not included.
- Unreal Engine files remain archive evidence and are not the active v0.1.x runtime.
- Saved readings are local-first. Use export/import JSON for backup and migration.

## License Notes

Source code, scripts, tests, and Markdown documentation are MIT-licensed. Tarot artwork, generated HUD images, app icons, ONOKO ARCANA visual identity, and other non-code visual assets are not covered by the MIT license and are not granted for reuse outside this project.

The local package includes `LICENSE`, `DISTRIBUTION_NOTICE.md`, `SECURITY.md`, and `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`.
