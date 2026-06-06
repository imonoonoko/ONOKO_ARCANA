# ONOKO ARCANA v0.1.2

ONOKO ARCANA v0.1.2 is a public preview GitHub Release for the local-first Web/Electron tarot study app.

This release replaces v0.1.1 as the recommended download.

## What Changed Since v0.1.1

- The local package now includes `CREATE_DESKTOP_SHORTCUT.ps1`.
- The shortcut helper creates or updates `ONOKO ARCANA.lnk` on the Windows Desktop.
- The Desktop shortcut targets the packaged Electron app directly and uses `assets/generated/app-icons/onoko-arcana-app-icon-v1.ico`.
- Package smoke and release zip validation now require the shortcut helper and `.ico` assignment.

## Download

Download both files from the GitHub Release:

- `onoko-arcana-v0.1.2-local.zip`
- `onoko-arcana-v0.1.2-local.zip.sha256`

## Quick Start

1. Download `onoko-arcana-v0.1.2-local.zip`.
2. Extract the zip to a normal user folder such as `Downloads` or `Documents`.
3. Open the extracted folder.
4. Run `START_ONOKO_ARCANA.cmd`.
5. Optional: run `CREATE_DESKTOP_SHORTCUT.ps1` to create or update the Windows Desktop shortcut with the ONOKO ARCANA `.ico` icon.

Windows may show a warning because this is an unsigned local package, not a signed installer.

To check the download hash in PowerShell:

```powershell
Get-FileHash .\onoko-arcana-v0.1.2-local.zip -Algorithm SHA256
Get-Content .\onoko-arcana-v0.1.2-local.zip.sha256
```

## Japanese Quick Start

1. `onoko-arcana-v0.1.2-local.zip` をダウンロードします。
2. zipを `Downloads` や `Documents` などの通常フォルダへ展開します。
3. 展開したフォルダの `START_ONOKO_ARCANA.cmd` を実行します。
4. 任意で `CREATE_DESKTOP_SHORTCUT.ps1` を実行すると、作成済み `.ico` を使う `ONOKO ARCANA.lnk` がデスクトップに作成または更新されます。
5. Windowsの警告が出る場合があります。これは未署名のローカルパッケージであり、署名済みインストーラーではありません。

## Verification

The release commit must pass GitHub Actions before the tag is published. The release zip and `.sha256` should be taken from the tag CI artifact, then attached to this GitHub Release.

Local verification path:

- `python scripts/check_web_app.py`
- `cd web-app && npm ci`
- `cd web-app && npm run smoke:web`
- `cd web-app && npm run smoke:keyboard`
- `cd web-app && npm run audit:visual`
- `cd web-app && npm run smoke:electron`
- `cd web-app && npm run package:local`
- `cd web-app && npm run smoke:package`
- `cd web-app && npm run release:artifact`
- `cd web-app && npm audit --audit-level=high`

## Known Limitations

- This release is a public preview.
- It provides an unsigned local Electron folder package, not a signed installer.
- Auto update is not included.
- Minor Arcana cards are not included.
- Unreal Engine files remain archive evidence and are not the active v0.1.x runtime.
- Saved readings are local-first. Use export/import JSON for backup and migration.

## Use Disclaimer

ONOKO ARCANA is a tarot study, self-reflection, and entertainment tool.

Do not use it as a substitute for professional medical, legal, financial, safety, or mental-health advice. It does not predict guaranteed outcomes and should not be used as the sole basis for important decisions.

## License Notes

Source code, scripts, tests, and Markdown documentation are MIT-licensed. Tarot artwork, generated HUD images, app icons, ONOKO ARCANA visual identity, and other non-code visual assets are not covered by the MIT license and are not granted for reuse outside this project.

The local package includes `LICENSE`, `DISTRIBUTION_NOTICE.md`, `SECURITY.md`, and `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`.
