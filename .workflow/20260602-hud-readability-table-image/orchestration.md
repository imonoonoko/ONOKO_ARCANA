# Orchestration

1. Freeze the visible UI defects from the user's annotated screenshots.
2. Modify the smallest set of Web app files needed for the defects:
   - `web-app/src/styles.css`
   - `web-app/src/app.js`
   - `scripts/check_web_app.py`
3. Run static validation.
4. Run browser and Electron smoke tests to produce screenshots.
5. Inspect screenshots and apply one readability pass if needed.
6. Update implementation notes and close the workflow state.

No external writes, deployments, or destructive filesystem operations are required.
