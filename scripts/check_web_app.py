from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB_APP = ROOT / "web-app"
PACKAGE_JSON = WEB_APP / "package.json"
INDEX = WEB_APP / "index.html"
DATA = WEB_APP / "src" / "data.js"
APP = WEB_APP / "src" / "app.js"
STYLES = WEB_APP / "src" / "styles.css"
ELECTRON_MAIN = WEB_APP / "electron" / "main.cjs"
HISTORY_SCHEMA = ROOT / "docs" / "data" / "HISTORY_SCHEMA_V1.md"
CARD_SCHEMA = ROOT / "docs" / "data" / "CARD_SCHEMA_V1.md"
SPREAD_SCHEMA = ROOT / "docs" / "data" / "SPREAD_SCHEMA_V1.md"
LEARNING_SCHEMA = ROOT / "docs" / "data" / "LEARNING_SCHEMA_V1_DRAFT.md"
REPORTS = ROOT / "reports"
HISTORY_FIXTURE_VALID = ROOT / "tests" / "fixtures" / "history" / "history-valid-v1.json"
HISTORY_FIXTURE_DUPLICATE = ROOT / "tests" / "fixtures" / "history" / "history-duplicate-v1.json"
HISTORY_FIXTURE_CARD_NOTE_ONLY = ROOT / "tests" / "fixtures" / "history" / "history-card-note-only-v1.json"
HISTORY_FIXTURE_INVALID_JSON = ROOT / "tests" / "fixtures" / "history" / "invalid-json.json"
LEARNING_FIXTURE_VALID = ROOT / "tests" / "fixtures" / "learning" / "learning-valid-v1.json"
REPORT_POLICY = REPORTS / "README.md"
INSTALLER_MANUAL_SMOKE_CHECKLIST = ROOT / "docs" / "release" / "INSTALLER_MANUAL_SMOKE_CHECKLIST.md"
PACKAGE_SCRIPT = ROOT / "scripts" / "package_electron_local.cjs"
PACKAGE_SMOKE = ROOT / "scripts" / "smoke_electron_package.cjs"
INSTALLER_SMOKE = ROOT / "scripts" / "smoke_electron_installer_app.cjs"
ROOT_README = ROOT / "README.md"
APP_ICON_ROOT = ROOT / "assets" / "generated" / "app-icons"
APP_ICON_PNG = APP_ICON_ROOT / "onoko-arcana-app-icon-v1.png"
APP_ICON_ICO = APP_ICON_ROOT / "onoko-arcana-app-icon-v1.ico"

REQUIRED_IDS = [
    "questionInput",
    "spreadControls",
    "spreadBoard",
    "drawButton",
    "revealButton",
    "saveReadingButton",
    "resetButton",
    "progressTrack",
    "inspectorTabs",
    "inspectorTabCard",
    "inspectorTabStudy",
    "inspectorTabHistory",
    "cardTabPanel",
    "studyTabPanel",
    "historyTabPanel",
    "selectedCard",
    "noteInput",
    "cardStudySheetPanel",
    "toggleStudySheetButton",
    "studySheetPanel",
    "historyList",
    "historyReview",
    "studyLens",
    "historyFilterBar",
    "importHistoryButton",
    "importHistoryInput",
    "exportHistoryButton",
    "clearHistoryButton",
    "historyBackupCue",
    "openSettingsButton",
    "settingsDialog",
    "closeSettingsButton",
    "settingsStatus",
    "settingsHistoryCount",
    "settingsHistoryUpdated",
    "settingsLearningCount",
    "settingsLearningUpdated",
    "settingsImportHistoryButton",
    "settingsExportHistoryButton",
    "settingsClearHistoryButton",
    "importLearningButton",
    "importLearningInput",
    "exportLearningButton",
    "clearLearningButton",
    "compactLearningToggle",
    "settingsAppVersion",
    "settingsReleaseWarning",
    "settingsBackupCue",
    "settingsLatestReleaseLink",
    "settingsProjectLink",
    "settingsSecurityLink",
    "settingsLicenseLink",
    "settingsLicenseCue",
    "settingsLocalKeys",
]

SPREAD_IDS = [
    "one_card",
    "three_card_past_present_future",
    "five_card_cross",
    "seven_card_horseshoe",
    "celtic_cross",
    "relationship_line",
]

CARD_SLUGS = [
    ("00", "fool"),
    ("01", "magician"),
    ("02", "high-priestess"),
    ("03", "empress"),
    ("04", "emperor"),
    ("05", "hierophant"),
    ("06", "lovers"),
    ("07", "chariot"),
    ("08", "strength"),
    ("09", "hermit"),
    ("10", "wheel-of-fortune"),
    ("11", "justice"),
    ("12", "hanged-man"),
    ("13", "death"),
    ("14", "temperance"),
    ("15", "devil"),
    ("16", "tower"),
    ("17", "star"),
    ("18", "moon"),
    ("19", "sun"),
    ("20", "judgement"),
    ("21", "world"),
]


def fail(message: str, details: dict | None = None) -> None:
    print(json.dumps({
        "ok": False,
        "message": message,
        "details": details or {},
        "checkedAt": datetime.now().isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=2))
    raise SystemExit(1)


def main() -> None:
    required_files = [
        PACKAGE_JSON,
        INDEX,
        DATA,
        APP,
        STYLES,
        ELECTRON_MAIN,
        HISTORY_SCHEMA,
        CARD_SCHEMA,
        SPREAD_SCHEMA,
        LEARNING_SCHEMA,
        HISTORY_FIXTURE_VALID,
        HISTORY_FIXTURE_DUPLICATE,
        HISTORY_FIXTURE_CARD_NOTE_ONLY,
        HISTORY_FIXTURE_INVALID_JSON,
        LEARNING_FIXTURE_VALID,
        REPORT_POLICY,
        INSTALLER_MANUAL_SMOKE_CHECKLIST,
        PACKAGE_SCRIPT,
        PACKAGE_SMOKE,
        INSTALLER_SMOKE,
        ROOT_README,
        APP_ICON_PNG,
        APP_ICON_ICO,
    ]
    missing_files = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
    if missing_files:
        fail("required web app files are missing", {"missingFiles": missing_files})

    index = INDEX.read_text(encoding="utf-8")
    data = DATA.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    styles = STYLES.read_text(encoding="utf-8")
    electron = ELECTRON_MAIN.read_text(encoding="utf-8")
    package_script = PACKAGE_SCRIPT.read_text(encoding="utf-8")
    package_json = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))

    missing_ids = [item for item in REQUIRED_IDS if f'id="{item}"' not in index]
    if missing_ids:
        fail("required UI ids are missing", {"missingIds": missing_ids})

    missing_spreads = [item for item in SPREAD_IDS if f'id: "{item}"' not in data]
    if missing_spreads:
        fail("required spread ids are missing", {"missingSpreadIds": missing_spreads})

    missing_layouts = [item for item in SPREAD_IDS if f".layout-{item}" not in styles]
    if missing_layouts:
        fail("required spread layout classes are missing", {"missingLayouts": missing_layouts})

    required_runtime_terms = [
        "drawSpread",
        "revealNext",
        "selectedNote",
        "saveReading",
        "restoreHistory",
        "renderHistoryReview",
        "deleteHistory",
        "clearHistory",
        "exportHistory",
        "importHistoryFile",
        "mergeImportedHistory",
        "reviewedHistoryKey",
        "historyReadFailed",
        "learningKey",
        "onoko-arcana:desktop:learning:v1",
        "settingsKey",
        "onoko-arcana:desktop:settings:v1",
        "appVersion",
        "latestReleaseUrl",
        "projectRepositoryUrl",
        "securityPolicyUrl",
        "assetLicenseUrl",
        "ONOKO_ARCANA/releases/latest",
        "readLearningState",
        "writeLearningState",
        "importedLearningFromPayload",
        "mergeImportedLearning",
        "exportLearning",
        "importLearningFile",
        "clearLearning",
        "readSettings",
        "writeSettings",
        "renderSettings",
        "renderRecallPractice",
        "renderCardStudySheet",
        "renderStudySheets",
        "renderStudySheet",
        "selectedStudySheetContext",
        "renderSlotInterpretationDrill",
        "saveSlotInterpretationAttempt",
        "openStudySheet",
        "data-study-sheet-card-id",
        "data-study-sheet-open",
        "data-slot-drill",
        "studyDetails",
        "commonMisreads",
        "reflectionQuestions",
        "renderFirstLaunchGuide",
        "inspectorTab",
        "renderInspectorTabs",
        "setInspectorTab",
        "data-inspector-tab",
        "data-inspector-panel",
        "renderDueReviewCue",
        "learningDueSummary",
        "confidenceIntervalDays",
        "afterSaveKey",
        "data-after-save-next",
        "data-first-launch-guide",
        "data-due-review-cue",
        "keyword_recall",
        "slot_interpretation",
        "履歴データを読めません",
        "localStorage",
    ]
    missing_runtime_terms = [term for term in required_runtime_terms if term not in app]
    if missing_runtime_terms:
        fail("required runtime behavior is missing", {"missingRuntimeTerms": missing_runtime_terms})

    if "contextIsolation: true" not in electron or "nodeIntegration: false" not in electron:
        fail("electron shell must keep renderer isolated", {"path": str(ELECTRON_MAIN.relative_to(ROOT))})

    if "setAppUserModelId" not in electron or "com.onoko.arcana" not in electron:
        fail("electron shell must set a Windows AppUserModelID for taskbar icon grouping", {
            "path": str(ELECTRON_MAIN.relative_to(ROOT)),
        })

    if "onoko-arcana-app-icon-v1.ico" not in electron or "onoko-arcana-app-icon-v1.png" not in electron:
        fail("electron shell must reference the generated app icon PNG/ICO", {
            "path": str(ELECTRON_MAIN.relative_to(ROOT)),
        })

    external_link_requirements = [
        "setWindowOpenHandler",
        "will-navigate",
        "shell.openExternal",
        "isAllowedExternalUrl",
        "github.com",
        "/imonoonoko/ONOKO_ARCANA",
    ]
    missing_external_link_terms = [
        term for term in external_link_requirements if term not in electron
    ]
    if missing_external_link_terms:
        fail("electron shell must restrict official external release/support links", {
            "path": str(ELECTRON_MAIN.relative_to(ROOT)),
            "missing": missing_external_link_terms,
        })

    if APP_ICON_PNG.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        fail("app icon PNG signature is invalid", {"path": str(APP_ICON_PNG.relative_to(ROOT))})

    if APP_ICON_ICO.read_bytes()[:4] != b"\x00\x00\x01\x00":
        fail("app icon ICO signature is invalid", {"path": str(APP_ICON_ICO.relative_to(ROOT))})

    if '"assets", "generated", "app-icons"' not in package_script or "appIcon" not in package_script:
        fail("local package must copy and declare app icon assets", {
            "path": str(PACKAGE_SCRIPT.relative_to(ROOT)),
        })

    package_scripts = package_json.get("scripts", {})
    build_config = package_json.get("build", {})
    win_config = build_config.get("win", {})
    nsis_config = build_config.get("nsis", {})
    win_targets = win_config.get("target", [])
    has_nsis_target = any(
        target == "nsis" or (isinstance(target, dict) and target.get("target") == "nsis")
        for target in win_targets
    )
    installer_requirements = {
        "package:installer": "electron-builder" in package_scripts.get("package:installer", ""),
        "smoke:installer": "smoke_electron_installer_app.cjs" in package_scripts.get("smoke:installer", ""),
        "electron-builder": "electron-builder" in package_json.get("devDependencies", {}),
        "appId": build_config.get("appId") == "com.onoko.arcana",
        "productName": build_config.get("productName") == "ONOKO ARCANA",
        "artifactName": build_config.get("artifactName") == "onoko-arcana-v${version}-setup.${ext}",
        "winIcon": str(win_config.get("icon", "")).endswith("onoko-arcana-app-icon-v1.ico"),
        "nsisTarget": has_nsis_target,
        "desktopShortcut": nsis_config.get("createDesktopShortcut") == "always",
        "startMenuShortcut": nsis_config.get("createStartMenuShortcut") is True,
        "shortcutName": nsis_config.get("shortcutName") == "ONOKO ARCANA",
    }
    missing_installer_requirements = [
        name for name, ok in installer_requirements.items() if not ok
    ]
    if missing_installer_requirements:
        fail("installer release configuration is incomplete", {
            "path": str(PACKAGE_JSON.relative_to(ROOT)),
            "missing": missing_installer_requirements,
        })

    valid_fixture = json.loads(HISTORY_FIXTURE_VALID.read_text(encoding="utf-8"))
    duplicate_fixture = json.loads(HISTORY_FIXTURE_DUPLICATE.read_text(encoding="utf-8"))
    card_note_only_fixture = json.loads(HISTORY_FIXTURE_CARD_NOTE_ONLY.read_text(encoding="utf-8"))
    learning_fixture = json.loads(LEARNING_FIXTURE_VALID.read_text(encoding="utf-8"))
    invalid_json = HISTORY_FIXTURE_INVALID_JSON.read_text(encoding="utf-8")
    try:
        json.loads(invalid_json)
    except json.JSONDecodeError:
        invalid_fixture_rejected = True
    else:
        invalid_fixture_rejected = False
    if not invalid_fixture_rejected:
        fail("invalid history fixture must stay invalid JSON", {"path": str(HISTORY_FIXTURE_INVALID_JSON.relative_to(ROOT))})

    for fixture_path, fixture in [
        (HISTORY_FIXTURE_VALID, valid_fixture),
        (HISTORY_FIXTURE_DUPLICATE, duplicate_fixture),
        (HISTORY_FIXTURE_CARD_NOTE_ONLY, card_note_only_fixture),
    ]:
        if fixture.get("app") != "ONOKO_ARCANA" or fixture.get("schemaVersion") != 1:
            fail("history fixture wrapper is invalid", {"path": str(fixture_path.relative_to(ROOT))})
        history = fixture.get("history")
        if not isinstance(history, list) or not history:
            fail("history fixture must contain at least one reading", {"path": str(fixture_path.relative_to(ROOT))})
        first = history[0]
        cards_payload = first.get("cards") if isinstance(first, dict) else None
        if not isinstance(cards_payload, list) or not cards_payload:
            fail("history fixture must contain card entries", {"path": str(fixture_path.relative_to(ROOT))})
        if any("reversed" not in entry for entry in cards_payload):
            fail("history fixture card entries must include reversed boolean", {"path": str(fixture_path.relative_to(ROOT))})

    if learning_fixture.get("app") != "ONOKO_ARCANA" or learning_fixture.get("schemaVersion") != 1:
        fail("learning fixture wrapper is invalid", {"path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT))})
    attempts = learning_fixture.get("attempts")
    if not isinstance(attempts, list) or not attempts:
        fail("learning fixture must contain at least one attempt", {"path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT))})
    valid_card_ids = {f"major-{number}-{slug}" for number, slug in CARD_SLUGS}
    prompt_types = set()
    for attempt in attempts:
        if not isinstance(attempt, dict):
            fail("learning attempt must be an object", {"path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT))})
        prompt_types.add(attempt.get("promptType"))
        if attempt.get("cardId") not in valid_card_ids:
            fail("learning fixture cardId must exist in card data", {"path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT))})
        if attempt.get("orientation") not in ["upright", "reversed"]:
            fail("learning fixture orientation is invalid", {"path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT))})
        if attempt.get("promptType") not in ["keyword_recall", "slot_interpretation"]:
            fail("learning fixture promptType is invalid", {"path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT))})
        if attempt.get("confidence") not in ["hard", "ok", "easy"]:
            fail("learning fixture confidence is invalid", {"path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT))})
        if attempt.get("promptType") == "slot_interpretation":
            for field in ["spreadId", "spreadLabel", "slotKey", "slotLabel", "slotPrompt"]:
                if not isinstance(attempt.get(field), str) or not attempt.get(field).strip():
                    fail("slot interpretation fixture must include spread and slot fields", {
                        "path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT)),
                        "field": field,
                    })
    if not {"keyword_recall", "slot_interpretation"}.issubset(prompt_types):
        fail("learning fixture must cover keyword recall and slot interpretation", {
            "path": str(LEARNING_FIXTURE_VALID.relative_to(ROOT)),
            "promptTypes": sorted(prompt_types),
        })

    card_root = ROOT / "assets" / "generated" / "card-production-v5-full" / "alpha"
    expected_assets = [card_root / "card-back-onoko-v5-alpha.png"]
    expected_assets.extend(
        card_root / f"major-{number}-{slug}-onoko-v5-alpha.png"
        for number, slug in CARD_SLUGS
    )
    missing_assets = [str(path.relative_to(ROOT)) for path in expected_assets if not path.exists()]
    if missing_assets:
        fail("required card assets are missing", {"missingAssets": missing_assets})

    web_labeled_root = ROOT / "assets" / "generated" / "card-production-v5-full" / "web-labeled" / "alpha"
    expected_web_labeled_assets = [web_labeled_root / "card-back-onoko-v5-alpha.png"]
    expected_web_labeled_assets.extend(
        web_labeled_root / f"major-{number}-{slug}-onoko-v5-alpha.png"
        for number, slug in CARD_SLUGS
    )
    missing_web_labeled_assets = [str(path.relative_to(ROOT)) for path in expected_web_labeled_assets if not path.exists()]
    if missing_web_labeled_assets:
        fail("required web labeled card assets are missing", {"missingWebLabeledAssets": missing_web_labeled_assets})

    if "WEB_CARD_ROOT" not in data or "web-labeled/alpha" not in data:
        fail("web app must use labeled card derivatives for front-card images", {"path": str(DATA.relative_to(ROOT))})

    hud_root = ROOT / "assets" / "generated" / "hud-elements" / "20260602-astra-modular-kit" / "components"
    expected_hud_assets = [
        hud_root / "panels" / "panel-02.png",
        hud_root / "panels" / "panel-05.png",
        hud_root / "panels" / "panel-13.png",
        hud_root / "controls" / "control-16.png",
        hud_root / "controls" / "control-20.png",
        hud_root / "card-slots" / "slot-06.png",
        hud_root / "card-slots" / "slot-20.png",
    ]
    nine_slice_root = ROOT / "assets" / "generated" / "hud-elements" / "20260602-astra-nine-slice-kit" / "nine-slice"
    expected_hud_assets.extend([
        nine_slice_root / "content-panel-frame-alpha-v1.png",
        nine_slice_root / "title-plaque-frame-alpha-v1.png",
        nine_slice_root / "command-button-frame-alpha-v1.png",
        nine_slice_root / "tarot-slot-frame-alpha-v1.png",
    ])
    expected_hud_assets.append(
        ROOT / "assets" / "generated" / "hud-candidates" / "20260602-named-hud-sets" / "astra-nocturne-background-v1.png"
    )
    missing_hud_assets = [str(path.relative_to(ROOT)) for path in expected_hud_assets if not path.exists()]
    if missing_hud_assets:
        fail("required modular HUD assets are missing", {"missingHudAssets": missing_hud_assets})

    card_rows = re.findall(r'\["\d{2}",\s*"[^"]+",', data)
    if len(card_rows) != 22:
        fail("expected 22 major arcana rows", {"found": len(card_rows)})

    REPORTS.mkdir(exist_ok=True)
    report = {
        "ok": True,
        "app": str(INDEX.relative_to(ROOT)),
        "requiredIds": len(REQUIRED_IDS),
        "spreads": SPREAD_IDS,
        "cardAssets": len(expected_assets),
        "webLabeledCardAssets": len(expected_web_labeled_assets),
        "hudAssets": len(expected_hud_assets),
        "electronShell": str(ELECTRON_MAIN.relative_to(ROOT)),
        "schemas": [
            str(HISTORY_SCHEMA.relative_to(ROOT)),
            str(CARD_SCHEMA.relative_to(ROOT)),
            str(SPREAD_SCHEMA.relative_to(ROOT)),
            str(LEARNING_SCHEMA.relative_to(ROOT)),
        ],
        "historyFixtures": [
            str(HISTORY_FIXTURE_VALID.relative_to(ROOT)),
            str(HISTORY_FIXTURE_DUPLICATE.relative_to(ROOT)),
            str(HISTORY_FIXTURE_CARD_NOTE_ONLY.relative_to(ROOT)),
            str(HISTORY_FIXTURE_INVALID_JSON.relative_to(ROOT)),
            str(LEARNING_FIXTURE_VALID.relative_to(ROOT)),
        ],
        "packageScripts": [
            str(PACKAGE_SCRIPT.relative_to(ROOT)),
            str(PACKAGE_SMOKE.relative_to(ROOT)),
            str(INSTALLER_SMOKE.relative_to(ROOT)),
        ],
        "appIcons": [
            str(APP_ICON_PNG.relative_to(ROOT)),
            str(APP_ICON_ICO.relative_to(ROOT)),
        ],
        "reportPolicy": str(REPORT_POLICY.relative_to(ROOT)),
        "checkedAt": datetime.now().isoformat(timespec="seconds"),
    }
    report_path = REPORTS / f"web-app-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({**report, "report": str(report_path.relative_to(ROOT))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
