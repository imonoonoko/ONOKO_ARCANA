from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "prototype" / "onoko-arcana-web-mvp-v1.html"
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
]

SPREAD_IDS = [
    "one_card",
    "three_card_past_present_future",
    "five_card_cross",
    "seven_card_horseshoe",
    "celtic_cross",
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
    payload = {
        "ok": False,
        "message": message,
        "details": details or {},
        "checkedAt": datetime.now().isoformat(timespec="seconds"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(1)


def main() -> None:
    if not PROTOTYPE.exists():
        fail("prototype file is missing", {"path": str(PROTOTYPE)})

    html = PROTOTYPE.read_text(encoding="utf-8")
    missing_ids = [item for item in REQUIRED_IDS if f'id="{item}"' not in html]
    if missing_ids:
        fail("required UI ids are missing", {"missingIds": missing_ids})

    missing_spreads = [item for item in SPREAD_IDS if f'id: "{item}"' not in html]
    if missing_spreads:
        fail("required spread ids are missing", {"missingSpreadIds": missing_spreads})

    card_root = ROOT / "assets" / "generated" / "card-production-v5-full" / "alpha"
    expected_assets = [card_root / "card-back-onoko-v5-alpha.png"]
    expected_assets.extend(
        card_root / f"major-{number}-{slug}-onoko-v5-alpha.png"
        for number, slug in CARD_SLUGS
    )
    missing_assets = [str(path.relative_to(ROOT)) for path in expected_assets if not path.exists()]
    if missing_assets:
        fail("required card assets are missing", {"missingAssets": missing_assets})

    required_handlers = [
        "drawSpread",
        "revealNext",
        "saveReading",
        "restoreHistory",
        "localStorage",
    ]
    missing_handlers = [handler for handler in required_handlers if handler not in html]
    if missing_handlers:
        fail("required runtime handlers are missing", {"missingHandlers": missing_handlers})

    card_rows = re.findall(r'\["\d{2}",\s*"[^"]+",', html)
    if len(card_rows) != 22:
        fail("expected 22 major arcana rows", {"found": len(card_rows)})

    REPORTS.mkdir(exist_ok=True)
    report = {
        "ok": True,
        "prototype": str(PROTOTYPE.relative_to(ROOT)),
        "requiredIds": len(REQUIRED_IDS),
        "spreads": SPREAD_IDS,
        "cardAssets": len(expected_assets),
        "checkedAt": datetime.now().isoformat(timespec="seconds"),
    }
    report_path = REPORTS / f"web-mvp-prototype-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({**report, "report": str(report_path.relative_to(ROOT))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
