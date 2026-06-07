# ONOKO ARCANA Installer Release Workflow

Goal:
Ship a GitHub Release artifact that a Windows user can download and run with the ONOKO ARCANA icon automatically applied to the installed app and shortcuts.

Success criteria:
- The primary release artifact is a Windows installer, not only a zip plus `.cmd`.
- The installed executable, Desktop shortcut, Start Menu shortcut, and Electron window use `onoko-arcana-app-icon-v1.ico`.
- The release artifact is produced by GitHub Actions tag CI.
- The unsigned state is still described honestly.
- Code signing and auto update are not claimed unless actually configured and verified.

Current context:
- v0.1.2 ships a local Electron folder zip and optional `CREATE_DESKTOP_SHORTCUT.ps1`.
- The optional helper fixes local shortcuts, but users must run it manually.
- CI currently uploads only the local folder zip and `.sha256`.

Constraints:
- Do not delete user/untracked `.agent`, `.workflow`, `docs/strategy`, or handoff files.
- Do not claim signed installer without a Windows code-signing certificate.
- Keep Unreal Engine out of the active runtime.
- Preserve local-first storage and export/import backup guidance.

Risks:
- Installer packaging can miss runtime assets if resource paths are wrong.
- Unsigned installer may still show Windows SmartScreen warnings.
- Auto update without signing would add update trust risk.
- Public release replacement should use a new tag rather than mutating old assets.

Approval required:
- Publishing a new GitHub Release.
- Any destructive cleanup or force-push.
- Enabling auto update or code signing secrets.

Work packets:
- Requirements: define installer behavior, non-goals, and acceptance criteria.
- Implementation: add electron-builder NSIS packaging with icon resources and installer artifact generation.
- Verification: build installer locally, inspect installer/exe resources where possible, run smoke tests, and verify CI artifacts.
- Docs/release: update runbook, release notes, limitations, and checklist.

Integration policy:
- Commit public release changes only.
- Keep generated dist outputs uncommitted.
- Keep local workflow/private planning artifacts uncommitted unless explicitly requested.

Verification:
- `python scripts/check_web_app.py`
- `cd web-app && npm ci`
- `cd web-app && npm run smoke:web`
- `cd web-app && npm run smoke:electron`
- `cd web-app && npm run package:local`
- `cd web-app && npm run package:installer`
- installer artifact smoke/check script
- `cd web-app && npm run release:artifact`
- main CI and tag CI green before release.

Reusable artifacts:
- Installer release checklist and runbook updates under `docs/release/`.
