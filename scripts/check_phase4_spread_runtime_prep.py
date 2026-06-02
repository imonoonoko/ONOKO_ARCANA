#!/usr/bin/env python3
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
SPREAD_FIXTURE = ROOT / "data" / "spread-definitions-v1.json"

REQUIRED_FILES = [
    ".agent/requirements/20260602-0155-spread-runtime-prep/1_purpose.md",
    ".agent/requirements/20260602-0155-spread-runtime-prep/3_scope.md",
    ".agent/requirements/20260602-0155-spread-runtime-prep/4_requirements.md",
    ".agent/requirements/20260602-0155-spread-runtime-prep/6_implementation_brief.md",
    "docs/implementation/PHASE3_SPREAD_SELECTION_FOUNDATION.md",
    "docs/design/spread-system-visual-direction-2026-06-02.md",
    "data/spread-definitions-v1.json",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadDefinition.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableController.h",
    "Unreal/ONOKO_ARCANA/Saved/Phase3SpreadRegistryTestResult.json",
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add(checks: list[dict[str, Any]], name: str, ok: bool, detail: str, status_if_false: str = "fail") -> None:
    checks.append(
        {
            "name": name,
            "status": "pass" if ok else status_if_false,
            "detail": detail,
        }
    )


def validate_spread_fixture(checks: list[dict[str, Any]]) -> None:
    if not SPREAD_FIXTURE.exists():
        add(checks, "spread fixture", False, f"missing {rel(SPREAD_FIXTURE)}")
        return

    try:
        fixture = load_json(SPREAD_FIXTURE)
    except json.JSONDecodeError as exc:
        add(checks, "spread fixture json", False, f"invalid json: {exc}")
        return

    spreads = fixture.get("spreads", [])
    spread_ids = [spread.get("spreadId") for spread in spreads]
    duplicate_spread_ids = sorted({spread_id for spread_id in spread_ids if spread_ids.count(spread_id) > 1})
    default_spread_id = fixture.get("defaultSpreadId")
    first_target_id = fixture.get("firstExecutableMultiCardSpreadId")

    add(checks, "spread fixture schema", fixture.get("schemaVersion") == 1, f"schemaVersion={fixture.get('schemaVersion')}")
    add(checks, "spread fixture count", len(spreads) >= 6, f"spreads={len(spreads)}")
    add(checks, "spread ids unique", not duplicate_spread_ids, f"duplicates={duplicate_spread_ids}")
    add(checks, "default spread exists", default_spread_id in spread_ids, f"defaultSpreadId={default_spread_id}")
    add(checks, "first target exists", first_target_id in spread_ids, f"firstExecutableMultiCardSpreadId={first_target_id}")
    add(checks, "first target is three card", first_target_id == "three_card_past_present_future", f"first target={first_target_id}")

    for spread in spreads:
        spread_id = spread.get("spreadId", "<missing>")
        slots = spread.get("slots", [])
        position_keys = [slot.get("positionKey") for slot in slots]
        reveal_orders = [slot.get("revealOrder") for slot in slots]
        default_selected_count = sum(1 for slot in slots if slot.get("defaultSelected") is True)

        expected_orders = list(range(1, len(slots) + 1))
        add(checks, f"spread:{spread_id}:has slots", len(slots) > 0, f"slots={len(slots)}")
        add(
            checks,
            f"spread:{spread_id}:position keys unique",
            len(position_keys) == len(set(position_keys)),
            f"positionKeys={position_keys}",
        )
        add(
            checks,
            f"spread:{spread_id}:reveal order contiguous",
            sorted(reveal_orders) == expected_orders,
            f"revealOrders={reveal_orders}",
        )
        add(
            checks,
            f"spread:{spread_id}:default selected one",
            default_selected_count == 1,
            f"defaultSelectedCount={default_selected_count}",
        )

        for slot in slots:
            slot_key = slot.get("positionKey", "<missing>")
            location = slot.get("tableLocationCm")
            add(
                checks,
                f"spread:{spread_id}:slot:{slot_key}:table location",
                isinstance(location, list) and len(location) == 3 and all(isinstance(value, (int, float)) for value in location),
                f"tableLocationCm={location}",
            )
            add(
                checks,
                f"spread:{spread_id}:slot:{slot_key}:guide prompt",
                bool(slot.get("guidePrompt")),
                "guidePrompt present" if slot.get("guidePrompt") else "guidePrompt missing",
            )

    by_id = {spread.get("spreadId"): spread for spread in spreads}
    one_card = by_id.get("one_card", {})
    three_card = by_id.get("three_card_past_present_future", {})
    celtic = by_id.get("celtic_cross", {})
    add(checks, "one_card slot count", len(one_card.get("slots", [])) == 1, f"slots={len(one_card.get('slots', []))}")
    add(checks, "three_card slot count", len(three_card.get("slots", [])) == 3, f"slots={len(three_card.get('slots', []))}")
    add(checks, "celtic_cross slot count", len(celtic.get("slots", [])) == 10, f"slots={len(celtic.get('slots', []))}")


def main() -> int:
    checks: list[dict[str, Any]] = []

    add(checks, "workspace", ROOT.exists(), str(ROOT))
    for required in REQUIRED_FILES:
        path = ROOT / required
        add(checks, f"file:{required}", path.exists(), "exists" if path.exists() else "missing")

    phase3_result_path = ROOT / "Unreal/ONOKO_ARCANA/Saved/Phase3SpreadRegistryTestResult.json"
    if phase3_result_path.exists():
        try:
            phase3_result = load_json(phase3_result_path)
            add(checks, "phase3 spread registry result", phase3_result.get("ok") is True, f"ok={phase3_result.get('ok')}")
            phase3_checks = phase3_result.get("checks", {})
            add(
                checks,
                "phase3 save metadata result",
                phase3_checks.get("controllerSaveSpreadMetadataOk") is True,
                f"controllerSaveSpreadMetadataOk={phase3_checks.get('controllerSaveSpreadMetadataOk')}",
            )
        except json.JSONDecodeError as exc:
            add(checks, "phase3 spread registry result", False, f"invalid json: {exc}")

    validate_spread_fixture(checks)

    fail_count = sum(1 for check in checks if check["status"] == "fail")
    warn_count = sum(1 for check in checks if check["status"] == "warn")

    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    report = {
        "ok": fail_count == 0,
        "generatedAtUtc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "workspace": str(ROOT),
        "spreadFixture": str(SPREAD_FIXTURE),
        "failCount": fail_count,
        "warnCount": warn_count,
        "checks": checks,
        "nextTask": "Implement UOnokoArcanaSpreadReadingSession for three_card_past_present_future using data/spread-definitions-v1.json as the fixture contract.",
    }

    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / f"phase4-spread-runtime-prep-check-{now}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"ONOKO ARCANA Phase 4 spread runtime prep: {'OK' if report['ok'] else 'FAILED'}")
    print(f"Report: {report_path}")
    print(f"Failures: {fail_count}  Warnings: {warn_count}")
    for check in checks:
        if check["status"] != "pass":
            print(f"- {check['status'].upper()}: {check['name']} :: {check['detail']}")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
