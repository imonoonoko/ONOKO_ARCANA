# ONOKO ARCANA v0.1.3

ONOKO ARCANA v0.1.3 is a public preview GitHub Release for the local-first Web/Electron tarot study app.

This release replaces v0.1.2 as the recommended download.

## What Changed Since v0.1.2

- Added an unsigned Windows installer built with `electron-builder`.
- The installer creates Desktop and Start Menu shortcuts named `ONOKO ARCANA`.
- Installed shortcuts use the generated `assets/generated/app-icons/onoko-arcana-app-icon-v1.ico` app icon automatically.
- The Release artifact flow now publishes the installer, fallback zip, and matching SHA256 files.
- CI now builds and smokes the packaged installer app before a tag artifact is uploaded.

## Download

Download the setup executable and its checksum from the GitHub Release:

- `onoko-arcana-v0.1.3-setup.exe`
- `onoko-arcana-v0.1.3-setup.exe.sha256`

Fallback files are also attached:

- `onoko-arcana-v0.1.3-local.zip`
- `onoko-arcana-v0.1.3-local.zip.sha256`

## Quick Start

1. Download `onoko-arcana-v0.1.3-setup.exe`.
2. Run the setup executable.
3. Launch `ONOKO ARCANA` from the Desktop or Start Menu shortcut.

Windows may show a warning because this is an unsigned installer.

To check the installer hash in PowerShell:

```powershell
Get-FileHash .\onoko-arcana-v0.1.3-setup.exe -Algorithm SHA256
Get-Content .\onoko-arcana-v0.1.3-setup.exe.sha256
```

## Japanese Quick Start

1. `onoko-arcana-v0.1.3-setup.exe` をダウンロードします。
2. setup executable を実行します。
3. デスクトップまたはスタートメニューの `ONOKO ARCANA` ショートカットから起動します。
4. Windowsの警告が出る場合があります。これは未署名インストーラーであり、署名済み配布ではありません。
5. インストーラーがブロックされる場合は、fallbackの `onoko-arcana-v0.1.3-local.zip` を展開し、`START_ONOKO_ARCANA.cmd` を実行してください。

## Verification

The release commit must pass GitHub Actions before the tag is published. The setup executable, fallback zip, and matching `.sha256` files should be taken from the tag CI artifact, then attached to this GitHub Release.

Local verification path:

- `python scripts/check_web_app.py`
- `cd web-app && npm ci`
- `cd web-app && npm run smoke:web`
- `cd web-app && npm run smoke:keyboard`
- `cd web-app && npm run audit:visual`
- `cd web-app && npm run smoke:electron`
- `cd web-app && npm run package:local`
- `cd web-app && npm run smoke:package`
- `cd web-app && npm run package:installer`
- `cd web-app && npm run smoke:installer`
- `cd web-app && npm run release:artifact`
- `cd web-app && npm audit --audit-level=high`

## Known Limitations

- This release is a public preview.
- The installer is unsigned.
- Auto update is not included.
- MSIX/Microsoft Store distribution is not included.
- Minor Arcana cards are not included.
- Unreal Engine files remain archive evidence and are not the active v0.1.x runtime.
- Saved readings are local-first. Use export/import JSON for backup and migration.

## Use Disclaimer

ONOKO ARCANA is a tarot study, self-reflection, and entertainment tool.

Do not use it as a substitute for professional medical, legal, financial, safety, or mental-health advice. It does not predict guaranteed outcomes and should not be used as the sole basis for important decisions.

## License Notes

Source code, scripts, tests, and Markdown documentation are MIT-licensed. Tarot artwork, generated HUD images, app icons, ONOKO ARCANA visual identity, and other non-code visual assets are not covered by the MIT license and are not granted for reuse outside this project.

The installer and fallback package include `LICENSE`, `DISTRIBUTION_NOTICE.md`, `SECURITY.md`, and `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`.
