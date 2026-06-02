# ONOKO ARCANA Web MVP Pivot

Date: 2026-06-02

## Decision

The immediate MVP direction has moved from Unreal-first wiring to a Web/Electron-ready 2D tarot table. Unreal remains in the project as a future premium 3D layer, but it is no longer the shortest path for proving the product loop.

## Why

The project already has strong V5 major arcana assets, Unreal import evidence, deck metadata, SaveGame-oriented concepts, and spread definitions. The current risk is not card quality. The risk is spending more time on UE-specific lighting, UMG wiring, map actor setup, and Editor automation before the core reading loop has been proven as a usable product.

The Web MVP lets the project validate the actual table workflow faster:

- choose a spread,
- draw cards,
- reveal cards in order,
- inspect the selected card,
- write a reader note,
- open guidance after the user's own interpretation,
- save the reading,
- revisit history.

## Web App

Prototype:

```text
prototype/onoko-arcana-web-mvp-v1.html
```

Production-oriented Web app:

```text
web-app/index.html
```

Characteristics:

- direct-open Web app with separated HTML/CSS/JS,
- no package manager required for the Web runtime,
- no build step required for the Web runtime,
- uses V5 card PNG alpha assets directly,
- supports all six spread definitions currently in `data/spread-definitions-v1.json`,
- stores saved readings in browser `localStorage`,
- exports reading history as JSON,
- can later be wrapped by Electron or Tauri.

Electron-ready shell:

```text
web-app/electron/main.cjs
```

Electron is installed as a development dependency under `web-app/`, and the shell has been smoke-tested through Playwright's Electron launcher. Distribution packaging is still a later task.

## Requirement Artifact

```text
.agent/requirements/20260602-0432-web-mvp-pivot/
```

Key files:

- `1_purpose.md`
- `2_alternatives.md`
- `3_scope.md`
- `4_requirements.md`
- `5_ui_prompt.md`
- `6_implementation_brief.md`

## Verification

Static check:

```text
python scripts/check_web_app.py
python scripts/check_web_mvp_prototype.py
```

Latest passing report:

```text
reports/web-app-check-20260602-051246.json
```

Browser smoke test performed with Playwright:

- opened the static HTML file,
- selected all six spreads,
- selected relationship line,
- entered a question,
- drew the spread,
- revealed all six relationship cards,
- verified guide stays disabled before a reader note,
- entered a note,
- opened guidance,
- saved the reading,
- selected Celtic cross,
- drew and revealed all ten cards,
- entered a note,
- opened guidance,
- saved the reading,
- captured a screenshot.

Screenshot:

```text
reports/onoko-arcana-web-app-celtic-20260602-051246.png
```

Observed state:

- spread: ケルト十字,
- spread choices: 6,
- revealed: 10 / 10,
- cards on table: 10,
- guide rows: 3,
- saved readings: 2,
- history items: 2,
- export enabled: true,
- console errors: 0.

Mobile smoke screenshot:

```text
reports/onoko-arcana-web-app-mobile-20260602-051246.png
```

Mobile observed state:

- viewport: 390 x 900,
- spread: 関係性ライン,
- revealed: 6 / 6,
- guide rows: 3,
- scroll width: 390,
- console errors: 0.

Repeatable smoke command used in this environment:

```text
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_web_app.cjs
```

Latest smoke report:

```text
reports/web-app-smoke-20260602-051246.json
```

Electron smoke command used in this environment:

```text
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_app.cjs
```

Latest Electron smoke report:

```text
reports/electron-app-smoke-20260602-051246.json
```

## Next Work

1. Add distribution packaging after the current Electron shell is accepted.
2. Add import for exported reading history after the export format is accepted.
3. Decide whether Tauri is still worth comparing after a few real reading sessions in Electron.
4. Move from major-arcana-only to minor arcana only after the current table remains readable with higher card counts.
5. Revisit Unreal only after the Web app loop is stable and the desired 3D value is specific.
