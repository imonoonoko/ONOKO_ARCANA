# Contributing

ONOKO ARCANA is currently a local-first Web/Electron tarot study app. The Unreal Engine files are preserved as archive evidence and are not the active v1.x implementation path.

## Development Setup

Requirements:

- Node.js 22+
- npm
- Python 3

Install dependencies:

```powershell
cd web-app
npm install
```

Run the Electron shell:

```powershell
cd web-app
npm run desktop
```

## Required Checks

Run the static check from the repository root:

```powershell
python scripts/check_web_app.py
```

Run browser and Electron checks after installing `web-app` dependencies:

```powershell
cd web-app
npm run smoke:web
npm run smoke:keyboard
npm run audit:visual
npm run smoke:electron
npm run package:local
npm run smoke:package
```

## Contribution Boundaries

- Keep v1.x changes focused on `web-app/`, `scripts/`, `tests/fixtures/`, and the relevant docs unless a task explicitly reopens the Unreal archive.
- Do not commit timestamped run output from `reports/`. Only `reports/README.md` is tracked by default.
- Do not commit `dist/`, `node_modules/`, local Electron packages, or machine-specific settings.
- Do not include private tarot questions, reading history, exported user history JSON, local absolute paths, or secrets in issues or commits.
- Treat artwork, generated images, brand visuals, and Unreal binary assets as project-owned assets. They are not MIT-licensed for reuse outside this project.

## Pull Request Notes

For a useful PR, include:

- What changed.
- Which runtime was affected: static web app, Electron shell, local package, docs, or Unreal archive.
- Which checks passed.
- Any remaining risk or manual review needed.
