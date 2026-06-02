# Implementation Brief

## Target Files

- `web-app/src/styles.css`
- `web-app/src/app.js`
- `scripts/check_web_app.py`

## Asset Source

```text
assets/generated/hud-elements/20260602-astra-modular-kit/components/
```

Recommended first-pass assets:

- `panels/panel-02.png`: side panel frame accent
- `panels/panel-05.png`: content panel accent
- `panels/panel-13.png`: bottom rail accent
- `controls/control-16.png`: compact status pip
- `controls/control-20.png`: pill command frame cue
- `card-slots/slot-06.png`: selected/focus ring
- `card-slots/slot-20.png`: spread connector line

## Implementation Notes

- Prefer CSS custom properties for asset URLs.
- Use pseudo-elements for ornament where possible.
- Keep hit areas and readable text in native HTML.
- Avoid changing core state or spread data in this slice.

## Verification

Run:

```text
python scripts/check_web_app.py
$env:NODE_PATH='C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_web_app.cjs
C:\Users\Humin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe scripts/smoke_electron_app.cjs
```
