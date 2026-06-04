# ONOKO ARCANA Report Policy

Updated: 2026-06-05

`reports/` is the generated verification output area. Do not treat every run as a source artifact.

Only this README is tracked in Git by default. Timestamped JSON files, screenshots, exported histories, and visual-audit directories are local run output.

## Representative Proof

The current representative proof set is recorded from roadmap references but not committed by default:

- `reports/web-app-check-20260605-004943.json`
- `reports/web-app-smoke-20260605-004943.json`
- `reports/electron-app-smoke-20260605-004947.json`
- `reports/electron-package-smoke-20260605-005006.json`
- `reports/keyboard-focus-smoke-20260605-005005.json`
- `reports/ui-visual-audit-20260605-004949/report.json`

Update the roadmap when a newer run becomes the accepted proof.

## Disposable Runs

New timestamped smoke screenshots, exported history files, invalid import files, and visual-audit directories are disposable unless explicitly promoted in a roadmap or handoff doc.

Invalid JSON test inputs belong in `tests/fixtures/history/`, not in this directory.

Do not force-add generated reports unless a release/handoff explicitly needs a small representative proof file.

## Promotion Rule

Promote only the smallest evidence set that proves the release gate:

- one static check JSON,
- one Web smoke JSON and required screenshots,
- one Electron or package smoke JSON,
- one visual audit report directory,
- any manually reviewed screenshot that captures a unique acceptance condition.
