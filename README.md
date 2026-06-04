# ONOKO ARCANA

ONOKO ARCANA is a local Web/Electron tarot study app. The active v1.x lane is the 2D Web/Electron reading table in `web-app/`; Unreal Engine work is archived evidence and is not the current implementation path.

## Current Entry

| Item | Path |
|---|---|
| Web app | `web-app/index.html` |
| Electron shell | `web-app/electron/main.cjs` |
| Plan | `plan.md` |
| Roadmap | `docs/roadmap/ONOKO_ARCANA_OVERALL_ROADMAP_2026-06-04.md` |
| Implementation kanban | `docs/implementation/IMPLEMENTATION_KANBAN.md` |
| Data schemas | `docs/data/` |

## Run

Open `web-app/index.html` directly, or run the Electron shell from `web-app/`:

```powershell
npm run desktop
```

## Verify

```powershell
python scripts/check_web_app.py
```

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_web_app.cjs
```

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_app.cjs
```

## Local Package

Create a local Electron folder package:

```powershell
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/package_electron_local.cjs
```

Output:

```text
dist/onoko-arcana-local/
dist/onoko-arcana-local/START_ONOKO_ARCANA.cmd
```

Smoke the package:

```powershell
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_package.cjs
```

This package is for local use and verification. Signed installer, auto update, and public distribution are separate v1.0+ tasks.

## History And Backup

Saved readings use browser/Electron `localStorage` key:

```text
onoko-arcana:desktop:history:v1
```

Before deleting history or moving machines, use the in-app export button and keep the JSON file as the backup. Restore with the in-app import button. The JSON contract is documented in `docs/data/HISTORY_SCHEMA_V1.md`.

Electron `localStorage` is stored in Electron's app data area for `ONOKO ARCANA`; treat export JSON as the supported backup and migration path rather than editing storage files directly.

## Evidence Policy

Generated run output goes under `reports/` and is ignored by default. Keep only durable policy/index files or intentionally promoted representative evidence in Git. See `reports/README.md`.
