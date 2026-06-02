# Scope

## In Scope

- Static Web prototype under `prototype/`.
- No package manager and no new runtime dependency for the first proof.
- Use V5 major arcana alpha PNG assets from `assets/generated/card-production-v5-full/alpha/`.
- Support multiple spread layouts from the start:
  - one-card observation,
  - three-card past/present/future,
  - five-card cross,
  - seven-card horseshoe,
  - Celtic cross.
- Draw unique cards from the 22-card major arcana deck.
- Assign upright/reversed state.
- Reveal cards one at a time.
- Select any revealed card.
- Store note text per reading slot.
- Save readings to `localStorage`.
- Show reading history.
- Capture a browser screenshot as evidence.

## Out of Scope

- Replacing the Unreal project.
- Electron/Tauri packaging.
- Backend accounts, cloud sync, or paid AI guidance.
- Minor arcana production.
- New image generation.
- Medical, legal, or financial fortune claims.

## Reuse Boundaries

The prototype may reuse card art, spread names, Japanese labels, and guidance text. It must not depend on Unreal assets, commandlets, or Editor state.
