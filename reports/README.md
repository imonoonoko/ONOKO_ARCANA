# ONOKO ARCANA Report Policy

Updated: 2026-06-07

`reports/` is the generated verification output area. Do not treat every run as a source artifact.

Only this README is tracked in Git by default. Timestamped JSON files, screenshots, exported histories, and visual-audit directories are local run output.

## Representative Proof

The current representative proof set is recorded from roadmap references but not committed by default:

- `reports/web-app-check-20260607-014605.json`
- `reports/web-app-smoke-20260607-011915.json`
- `reports/onoko-arcana-card-tab-study-sheet-20260607-0120.png`
- `reports/onoko-arcana-app-icon-preview-20260607-0143.png`
- `reports/electron-app-smoke-20260607-014422.json`
- `reports/electron-package-smoke-20260607-014620.json`
- `reports/keyboard-focus-smoke-20260607-012201.json`
- `reports/ui-visual-audit-20260607-012023/report.json`

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
