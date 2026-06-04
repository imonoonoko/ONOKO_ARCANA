# ONOKO ARCANA Web App

This is the active Web/Electron 2D desktop reading table.

## Run

Open directly from the repository root:

```text
web-app/index.html
```

Run the Electron shell:

```powershell
npm install
npm run desktop
```

## Current Reading Loop

- choose any spread,
- enter a question,
- draw cards face down,
- reveal cards in order,
- select a revealed card,
- write the user's own interpretation first,
- open guide text after the note exists,
- save the reading to local history,
- restore saved readings,
- export reading history as JSON,
- delete one reading or clear all readings after confirmation.

## Data Contracts

History storage key:

```text
onoko-arcana:desktop:history:v1
```

Schema and fixture docs:

```text
docs/data/HISTORY_SCHEMA_V1.md
docs/data/CARD_SCHEMA_V1.md
docs/data/SPREAD_SCHEMA_V1.md
tests/fixtures/history/
```

## Verification

From the repository root:

```powershell
python scripts/check_web_app.py
```

From this directory after `npm install`:

```powershell
npm run check
npm run smoke:web
npm run smoke:electron
npm run smoke:keyboard
npm run audit:visual
```

## Local Package

Create the local folder package:

```powershell
npm run package:local
```

Output:

```text
dist/onoko-arcana-local/START_ONOKO_ARCANA.cmd
```

Smoke the packaged app:

```powershell
npm run smoke:package
```

## Generated Card Derivatives

Regenerate the Web-only labeled card derivatives from the repository root:

```powershell
python scripts/build_web_labeled_cards.py
```

The generated front-card images live under:

```text
assets/generated/card-production-v5-full/web-labeled/alpha/
```

## Backup And Restore

- Use the in-app export button before deleting history or moving machines.
- Keep the exported JSON as the supported backup.
- Use the in-app import button to restore.
- Do not rely on manually editing Electron localStorage files.
