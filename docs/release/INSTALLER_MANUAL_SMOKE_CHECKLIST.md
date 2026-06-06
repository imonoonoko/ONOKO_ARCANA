# ONOKO ARCANA Installer Manual Smoke Checklist

Date: 2026-06-07
Scope: GitHub Release installer user-path checks that are not fully covered by automated package smoke tests.

## When To Run

Run this checklist before promoting a GitHub Release from public preview to a normal release, after changing installer config, or after changing app icon/signing/update behavior.

## Test Inputs

- Release page: `https://github.com/imonoonoko/ONOKO_ARCANA/releases/latest`
- Primary artifact: `onoko-arcana-v0.1.3-setup.exe`
- Checksum file: `onoko-arcana-v0.1.3-setup.exe.sha256`
- Fallback artifact: `onoko-arcana-v0.1.3-local.zip`

## Clean Windows User Or VM

- [ ] Download the setup executable and matching `.sha256` from the GitHub Release page.
- [ ] Confirm the SHA-256 hash matches the published `.sha256`.
- [ ] Launch the setup executable.
- [ ] Record whether Windows SmartScreen or antivirus blocks the unsigned installer.
- [ ] Complete install without admin elevation.
- [ ] Confirm Desktop shortcut exists and shows the ONOKO ARCANA `.ico` icon.
- [ ] Confirm Start Menu shortcut exists and shows the ONOKO ARCANA `.ico` icon.
- [ ] Launch from Desktop shortcut.
- [ ] Launch from Start Menu shortcut.
- [ ] Draw, reveal, write a note, and save one reading.
- [ ] Open Settings and confirm `v0.1.3`, latest Release link, Security link, License link, unsigned warning, auto-update warning, and backup cue are visible.
- [ ] Export history data.
- [ ] Export learning data if learning records exist.
- [ ] Close and relaunch the app, then confirm the saved reading is still present.
- [ ] Uninstall ONOKO ARCANA from Windows Apps settings.
- [ ] Confirm Desktop and Start Menu shortcuts are removed.
- [ ] Reinstall ONOKO ARCANA and confirm behavior is unchanged.

## Fallback Zip Check

- [ ] Download the fallback zip and matching `.sha256`.
- [ ] Confirm the SHA-256 hash matches the published `.sha256`.
- [ ] Extract to a non-repository folder.
- [ ] Run `START_ONOKO_ARCANA.cmd`.
- [ ] Confirm the app opens and card assets render.
- [ ] Open Settings and confirm the same Release/Support/Backup guidance is visible.
- [ ] Run `CREATE_DESKTOP_SHORTCUT.ps1` only if the fallback shortcut path is being tested.
- [ ] Confirm the fallback shortcut uses `onoko-arcana-app-icon-v1.ico`.

## Stop Conditions

- Do not remove the fallback zip if the installer is blocked on a normal consumer Windows environment.
- Do not mark the release as signed unless Authenticode status is valid and publisher identity is expected.
- Do not enable auto update until signing and update-channel trust are implemented and tested.
- Do not publish Store/MSIX language unless that channel has been built and reviewed separately.
