# ONOKO ARCANA

[![CI](https://github.com/imonoonoko/ONOKO_ARCANA/actions/workflows/ci.yml/badge.svg)](https://github.com/imonoonoko/ONOKO_ARCANA/actions/workflows/ci.yml)

ONOKO ARCANA is a local-first Web/Electron tarot study app. The active v1.x app is the 2D reading table in `web-app/`; Unreal Engine work is kept as archived technical evidence and is not the current implementation path.

## What It Does

- Choose a tarot spread.
- Enter a question.
- Draw cards face down.
- Reveal cards in order.
- Write your own interpretation before opening guidance.
- Save readings to local history.
- Export/import history JSON for backup and migration.

## Current Entry Points

| Item | Path |
|---|---|
| Web app | `web-app/index.html` |
| Electron shell | `web-app/electron/main.cjs` |
| Plan | `plan.md` |
| Roadmap | `docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md` |
| Implementation kanban | `docs/implementation/IMPLEMENTATION_KANBAN.md` |
| Data schemas | `docs/data/` |

## Requirements

- Node.js 22+ and npm
- Python 3 for static checks

The plain Web app can be opened directly without a build step. Electron and Playwright checks require installing the `web-app` dev dependencies.

## Run

Open the static app directly:

```text
web-app/index.html
```

Run the Electron shell:

```powershell
cd web-app
npm install
npm run desktop
```

## Verify

From the repository root:

```powershell
python scripts/check_web_app.py
```

After `npm install` in `web-app/`, run browser/Electron checks:

```powershell
cd web-app
npm run smoke:web
npm run smoke:electron
npm run smoke:keyboard
npm run audit:visual
```

## Local Package

Create a local Electron folder package:

```powershell
cd web-app
npm run package:local
```

Output:

```text
dist/onoko-arcana-local/
dist/onoko-arcana-local/START_ONOKO_ARCANA.cmd
dist/onoko-arcana-local/CREATE_DESKTOP_SHORTCUT.ps1
```

Smoke the package:

```powershell
cd web-app
npm run smoke:package
```

This package is for local use and fallback verification. GitHub Releases should use the Windows installer as the primary download when available. Code signing, auto update, and store distribution remain separate v1.0+ tasks.

## GitHub Release Download

GitHub Releases attach:

- `onoko-arcana-v0.1.3-setup.exe`
- `onoko-arcana-v0.1.3-setup.exe.sha256`
- `onoko-arcana-v0.1.3-local.zip`
- `onoko-arcana-v0.1.3-local.zip.sha256`

The setup executable is the recommended Windows download. It installs ONOKO ARCANA and creates Start Menu/Desktop shortcuts with the generated `onoko-arcana-app-icon-v1.ico` icon. The zip remains as an unsigned local Electron folder fallback and should include `LICENSE`, `SECURITY.md`, `DISTRIBUTION_NOTICE.md`, and `docs/legal/` so the split license and asset reuse restrictions remain visible outside the repository checkout.

Quick start:

```text
1. Download onoko-arcana-v0.1.3-setup.exe.
2. Run the setup executable.
3. Launch ONOKO ARCANA from the Desktop or Start Menu shortcut.
4. If setup is blocked, use onoko-arcana-v0.1.3-local.zip as the fallback: extract it and run START_ONOKO_ARCANA.cmd.
```

Windows may show a warning because the installer is unsigned.

After launch, open Settings to check the official latest GitHub Release, review the security/license links, and export history or learning data before updating, moving PCs, or uninstalling. ONOKO ARCANA does not include auto update in this unsigned preview channel.

Before publishing a Release, follow `docs/release/GITHUB_RELEASE_RUNBOOK.md`, use the tag CI artifacts for the setup executable and fallback zip, and confirm GitHub Actions passes on the exact tagged commit.

ONOKO ARCANA is a tarot study, self-reflection, and entertainment tool. Do not use it as a substitute for professional medical, legal, financial, safety, or mental-health advice.

## History And Backup

Saved readings use browser/Electron `localStorage` key:

```text
onoko-arcana:desktop:history:v1
```

Before deleting history or moving machines, use the in-app export button and keep the JSON file as the backup. Restore with the in-app import button. The JSON contract is documented in `docs/data/HISTORY_SCHEMA_V1.md`.

Electron `localStorage` is stored in Electron's app data area for `ONOKO ARCANA`; treat export JSON as the supported backup and migration path rather than editing storage files directly.

## Evidence Policy

Generated run output goes under `reports/` and is ignored by default. Keep only durable policy/index files or intentionally promoted representative evidence in Git. See `reports/README.md`.

## Public Repository Notes

- Contribution setup and verification commands are in `CONTRIBUTING.md`.
- Vulnerability reporting and local data handling notes are in `SECURITY.md`.
- Asset reuse restrictions are detailed in `docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md`.
- Release operation steps are in `docs/release/GITHUB_RELEASE_RUNBOOK.md`.

## License

This repository uses a split license:

- Source code, scripts, tests, and Markdown documentation are MIT-licensed.
- Tarot artwork, generated HUD images, reference images, ONOKO ARCANA visual identity, and other non-code visual assets are not covered by the MIT license and are not granted for reuse outside this project.

See `LICENSE` for details.
