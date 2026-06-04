# Security Policy

## Supported Scope

Security reports should target the current v1.x Web/Electron app and local package flow.

The Unreal Engine files are archive evidence. Security reports for those files are welcome, but fixes may be deferred unless the Unreal path is reopened.

## Reporting A Vulnerability

Please report suspected vulnerabilities through GitHub private vulnerability reporting when available:

https://github.com/imonoonoko/ONOKO_ARCANA/security/advisories/new

If private reporting is unavailable, open a minimal public issue without exploit details and ask for a private contact path.

## What To Include

Include:

- Affected commit, release, or package date.
- Runtime: static web app, Electron shell, or local package.
- Reproduction steps.
- Impact.
- Suggested fix, if known.

Do not include private tarot questions, reading history, exported history JSON containing personal data, secrets, tokens, or machine-specific local paths.

## Local Data Model

ONOKO ARCANA stores reading history locally using browser/Electron `localStorage` under:

```text
onoko-arcana:desktop:history:v1
```

History export/import JSON is user-controlled backup data. Treat exported history as private user data.

## Dependency Updates

Dependency updates should keep the existing verification path green:

```powershell
python scripts/check_web_app.py
cd web-app
npm run smoke:web
npm run smoke:keyboard
npm run audit:visual
npm run smoke:electron
npm run package:local
npm run smoke:package
```
