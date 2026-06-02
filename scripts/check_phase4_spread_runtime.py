#!/usr/bin/env python3
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
RESULT_PATH = ROOT / "Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json"


REQUIRED_FILES = [
    "data/spread-definitions-v1.json",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadDefinition.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadReadingSession.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadReadingViewModel.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaReadingSaveGame.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaReadingSaveLibrary.h",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase4_three_card_spread_session.py",
    "docs/implementation/PHASE4_SPREAD_READING_RUNTIME_PREP.md",
    "docs/implementation/PHASE4_SPREAD_READING_RUNTIME.md",
]

REQUIRED_STEPS = [
    "find_three_card_spread",
    "initialize",
    "start_three_card_reading",
    "draw_spread",
    "guide_locked_before_reveal",
    "reveal_next_past",
    "reveal_next_present",
    "reveal_next_future",
    "selected_note_and_guide",
    "make_saved_spread_reading",
    "save_spread_reading",
    "load_saved_spread_reading",
    "spread_view_model_surface",
    "reset_session",
    "delete_test_slot",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add(checks: list[dict[str, Any]], name: str, ok: bool, detail: str) -> None:
    checks.append({"name": name, "status": "pass" if ok else "fail", "detail": detail})


def main() -> int:
    checks: list[dict[str, Any]] = []

    for rel_path in REQUIRED_FILES:
        path = ROOT / rel_path
        add(checks, f"file:{rel_path}", path.exists(), "exists" if path.exists() else "missing")

    if RESULT_PATH.exists():
        try:
            result = load_json(RESULT_PATH)
            add(checks, "commandlet result exists", True, str(RESULT_PATH))
            add(checks, "commandlet ok", result.get("ok") is True, f"ok={result.get('ok')}")

            steps = result.get("steps", [])
            step_by_name = {step.get("step"): step for step in steps}
            missing_steps = [step for step in REQUIRED_STEPS if step not in step_by_name]
            failed_steps = [step.get("step") for step in steps if step.get("ok") is not True]
            add(checks, "required commandlet steps", not missing_steps, "all present" if not missing_steps else ", ".join(missing_steps))
            add(checks, "commandlet step status", not failed_steps, "all pass" if not failed_steps else ", ".join(map(str, failed_steps)))

            saved_step = step_by_name.get("make_saved_spread_reading", {})
            add(
                checks,
                "saved spread metadata",
                saved_step.get("spreadId") == "three_card_past_present_future"
                and int(saved_step.get("cardCount", 0)) == 3
                and int(saved_step.get("savedCardStateCount", 0)) == 3,
                f"spreadId={saved_step.get('spreadId')} cardCount={saved_step.get('cardCount')} states={saved_step.get('savedCardStateCount')}",
            )

            draw_step = step_by_name.get("draw_spread", {})
            add(
                checks,
                "drawn card uniqueness",
                draw_step.get("uniqueCards") is True and len(draw_step.get("drawnCardIds", [])) == 3,
                f"drawnCardIds={draw_step.get('drawnCardIds')}",
            )

            reveal_sequence = [
                step_by_name.get("reveal_next_past", {}).get("selectedPositionKey"),
                step_by_name.get("reveal_next_present", {}).get("selectedPositionKey"),
                step_by_name.get("reveal_next_future", {}).get("selectedPositionKey"),
            ]
            add(
                checks,
                "reveal sequence",
                reveal_sequence == ["past", "present", "future"],
                f"sequence={reveal_sequence}",
            )

            guide_lock_step = step_by_name.get("guide_locked_before_reveal", {})
            add(
                checks,
                "guide lock before reveal",
                guide_lock_step.get("canRevealBefore") is False
                and guide_lock_step.get("selectedState", {}).get("guideRevealed") is False,
                f"canRevealBefore={guide_lock_step.get('canRevealBefore')}",
            )
        except json.JSONDecodeError as exc:
            add(checks, "commandlet result json", False, f"invalid json: {exc}")
    else:
        add(checks, "commandlet result exists", False, str(RESULT_PATH))

    fail_count = sum(1 for check in checks if check["status"] == "fail")
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    report = {
        "ok": fail_count == 0,
        "generatedAtUtc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "workspace": str(ROOT),
        "failCount": fail_count,
        "checks": checks,
        "nextTask": "Wire the spread runtime into the UE Editor play surface and capture a completed three-card spread screenshot.",
    }

    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / f"phase4-spread-runtime-check-{now}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"ONOKO ARCANA Phase 4 spread runtime: {'OK' if report['ok'] else 'FAILED'}")
    print(f"Report: {report_path}")
    print(f"Failures: {fail_count}")
    for check in checks:
        if check["status"] != "pass":
            print(f"- FAIL: {check['name']} :: {check['detail']}")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
