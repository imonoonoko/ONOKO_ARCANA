from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB_APP = ROOT / "web-app"
INDEX = WEB_APP / "index.html"
DATA = WEB_APP / "src" / "data.js"
APP = WEB_APP / "src" / "app.js"
STYLES = WEB_APP / "src" / "styles.css"
ELECTRON_MAIN = WEB_APP / "electron" / "main.cjs"
REPORTS = ROOT / "reports"

REQUIRED_IDS = [
    "questionInput",
    "spreadControls",
    "spreadBoard",
    "drawButton",
    "revealButton",
    "saveReadingButton",
    "resetButton",
    "progressTrack",
    "selectedCard",
    "noteInput",
    "toggleGuideButton",
    "guidePanel",
    "historyList",
    "exportHistoryButton",
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
    required_files = [INDEX, DATA, APP, STYLES, ELECTRON_MAIN]
    missing_files = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
    if missing_files:
        fail("required web app files are missing", {"missingFiles": missing_files})

    index = INDEX.read_text(encoding="utf-8")
    data = DATA.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    styles = STYLES.read_text(encoding="utf-8")
    electron = ELECTRON_MAIN.read_text(encoding="utf-8")

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
        "exportHistory",
        "localStorage",
    ]
    missing_runtime_terms = [term for term in required_runtime_terms if term not in app]
    if missing_runtime_terms:
        fail("required runtime behavior is missing", {"missingRuntimeTerms": missing_runtime_terms})

    if "contextIsolation: true" not in electron or "nodeIntegration: false" not in electron:
        fail("electron shell must keep renderer isolated", {"path": str(ELECTRON_MAIN.relative_to(ROOT))})

    card_root = ROOT / "assets" / "generated" / "card-production-v5-full" / "alpha"
    expected_assets = [card_root / "card-back-onoko-v5-alpha.png"]
    expected_assets.extend(
        card_root / f"major-{number}-{slug}-onoko-v5-alpha.png"
        for number, slug in CARD_SLUGS
    )
    missing_assets = [str(path.relative_to(ROOT)) for path in expected_assets if not path.exists()]
    if missing_assets:
        fail("required card assets are missing", {"missingAssets": missing_assets})

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
        "hudAssets": len(expected_hud_assets),
        "electronShell": str(ELECTRON_MAIN.relative_to(ROOT)),
        "checkedAt": datetime.now().isoformat(timespec="seconds"),
    }
    report_path = REPORTS / f"web-app-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({**report, "report": str(report_path.relative_to(ROOT))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
