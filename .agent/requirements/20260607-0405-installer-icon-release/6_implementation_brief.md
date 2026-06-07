# Implementation Brief

Use `electron-builder` with the NSIS target for Windows. Configure:

- `appId`: `com.onoko.arcana`
- `productName`: `ONOKO ARCANA`
- `win.icon`: `../assets/generated/app-icons/onoko-arcana-app-icon-v1.ico`
- `nsis.createDesktopShortcut`: `always`
- `nsis.createStartMenuShortcut`: `true`
- `nsis.shortcutName`: `ONOKO ARCANA`
- unsigned build mode until a signing certificate is available

Keep the existing local folder package as a fallback. Update CI release artifacts to upload both installer and fallback zip with matching `.sha256` files.
