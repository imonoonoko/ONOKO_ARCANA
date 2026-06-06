# ONOKO ARCANA v0.1.0 Post-Release Review

Date: 2026-06-07
Release: `v0.1.0`
Release URL: https://github.com/imonoonoko/ONOKO_ARCANA/releases/tag/v0.1.0

## Outcome

`v0.1.0` was successfully published as the first GitHub Release.

- Release commit: `bfeaecb6fdac7b6c4ba1cfc7a7ef95c3a639e1cc`
- CI run: `27070066993`
- CI conclusion: success
- Published assets:
  - `onoko-arcana-v0.1.0-local.zip`
  - `onoko-arcana-v0.1.0-local.zip.sha256`

## Critical Follow-Up

The release was valid as a first public package, but the post-release review found issues to correct before recommending the app broadly:

- The readiness report still used pre-publication wording.
- The package was generated locally, not from a tag CI artifact.
- The package included non-runtime app-icon source material.
- The release notes needed clearer Japanese quick-start, unsigned-package explanation, and use-disclaimer text.

These are corrected in the `v0.1.1` release path.
