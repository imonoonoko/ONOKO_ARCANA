# ONOKO ARCANA Web App

This is the Web/Electron-ready 2D desktop reading table.

Open directly:

```text
web-app/index.html
```

Current implemented loop:

- choose any spread in `data/spread-definitions-v1.json`,
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

History storage:

```text
onoko-arcana:desktop:history:v1
```

The JSON contract is documented in:

```text
docs/data/HISTORY_SCHEMA_V1.md
docs/data/CARD_SCHEMA_V1.md
docs/data/SPREAD_SCHEMA_V1.md
tests/fixtures/history/
```

Verification:

```text
python scripts/check_web_app.py
```

From this directory:

```text
npm run check
```

Regenerate the Web-only labeled card derivatives:

```text
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/build_web_labeled_cards.py
```

The generated front-card images live under:

```text
assets/generated/card-production-v5-full/web-labeled/alpha/
```

Browser smoke, using the bundled Playwright runtime in this Codex environment:

```text
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_web_app.cjs
```

Electron shell:

```text
web-app/electron/main.cjs
```

Run the Electron shell:

```text
npm run desktop
```

Electron smoke, using the bundled Playwright runtime in this Codex environment:

```text
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_app.cjs
```

Create a local folder package:

```text
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/package_electron_local.cjs
```

Output:

```text
dist/onoko-arcana-local/START_ONOKO_ARCANA.cmd
```

Package smoke:

```text
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_package.cjs
```

Backup and restore:

- Use the in-app export button before deleting history or moving machines.
- Keep the exported JSON as the supported backup.
- Use the in-app import button to restore.
- Do not rely on manually editing Electron localStorage files.
