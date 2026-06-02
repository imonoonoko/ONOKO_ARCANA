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
- export reading history as JSON.

Verification:

```text
python scripts/check_web_app.py
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
