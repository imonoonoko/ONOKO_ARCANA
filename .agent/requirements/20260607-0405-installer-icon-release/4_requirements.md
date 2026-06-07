# Requirements

## User Stories

- As a GitHub Release downloader, I can download one installer file, run it, and get ONOKO ARCANA in the Start Menu with the correct app icon.
- As a Windows desktop user, I can use the installer-created Desktop shortcut and see the ONOKO ARCANA icon without running a separate helper.
- As the project maintainer, I can reproduce installer artifacts from CI and verify their hashes before attaching them to a Release.

## Acceptance Criteria

- The recommended GitHub Release artifact is named like `onoko-arcana-vX.Y.Z-setup.exe`.
- The installer configuration sets the Windows app icon to `onoko-arcana-app-icon-v1.ico`.
- The installer creates Desktop and Start Menu shortcuts.
- The Electron main process sets the same app ID used by the installer.
- The release artifact script emits `.sha256` files for installer and fallback zip artifacts.
- Release notes state that the installer is unsigned until code signing is configured.

## Open Risks

- A real Windows install/uninstall smoke is stronger than artifact inspection, but may require an interactive or disposable Windows profile.
- SmartScreen warnings remain until code signing and reputation are established.
