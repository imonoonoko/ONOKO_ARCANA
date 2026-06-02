#!/usr/bin/env python3
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
SCREENSHOT_GLOBS = [
    "onoko-arcana-hud-generated-overlay-printwindow-*.png",
    "onoko-arcana-rich-ui-printwindow-*.png",
    "onoko-arcana-card-visibility-labels-printwindow-*.png",
    "onoko-arcana-three-card-*-printwindow-*.png",
]


REQUIRED_FILES = [
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableController.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableController.cpp",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaPlayerController.cpp",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableHudWidget.cpp",
    "Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase4HudTextureImportResult.json",
    "Unreal/ONOKO_ARCANA/Scripts/import_phase4_hud_textures.py",
    "Unreal/ONOKO_ARCANA/ImportStaging/HUD/onoko-hud-overlay-v1-alpha.png",
    "Unreal/ONOKO_ARCANA/Content/ONOKOArcana/UI/HUD/Textures/T_HUD_ONOKO_Overlay_V1.uasset",
    "docs/implementation/PHASE4_SPREAD_PLAY_SURFACE.md",
    "docs/implementation/PHASE4_SPREAD_SLOT_HUD.md",
    "docs/implementation/PHASE4_CARD_VISIBILITY_LABELS.md",
    "docs/implementation/PHASE4_RICH_NATIVE_UI.md",
    "docs/implementation/PHASE4_HUD_GENERATED_OVERLAY.md",
    "PRODUCT.md",
    "DESIGN.md",
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

    for rel_path in [
        "Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json",
        "Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json",
        "Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json",
        "Unreal/ONOKO_ARCANA/Saved/Phase4HudTextureImportResult.json",
    ]:
        path = ROOT / rel_path
        if path.exists():
            try:
                result = load_json(path)
                add(checks, f"result:{path.name}", result.get("ok") is True, f"ok={result.get('ok')}")
            except json.JSONDecodeError as exc:
                add(checks, f"result:{path.name}", False, f"invalid json: {exc}")

    screenshots = []
    for screenshot_glob in SCREENSHOT_GLOBS:
        screenshots.extend(REPORT_DIR.glob(screenshot_glob))
    screenshots = sorted(set(screenshots), key=lambda path: path.stat().st_mtime, reverse=True)
    latest_screenshot = screenshots[0] if screenshots else None
    add(
        checks,
        "three-card demo screenshot",
        latest_screenshot is not None and latest_screenshot.stat().st_size > 100_000,
        str(latest_screenshot) if latest_screenshot else "missing card visibility / three-card screenshot",
    )

    material_result_path = ROOT / "Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json"
    if material_result_path.exists():
        try:
            material_result = load_json(material_result_path)
            add(
                checks,
                "runtime card material unlit",
                material_result.get("ok") is True
                and "BLEND_MASKED" in material_result.get("blendMode", "")
                and "MSM_UNLIT" in material_result.get("shadingModel", ""),
                f"blend={material_result.get('blendMode')} shading={material_result.get('shadingModel')}",
            )
        except json.JSONDecodeError as exc:
            add(checks, "runtime card material unlit", False, f"invalid json: {exc}")

    controller_cpp = ROOT / "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableController.cpp"
    if controller_cpp.exists():
        text = controller_cpp.read_text(encoding="utf-8", errors="replace")
        add(checks, "spread view model routed", "EnsureSpreadViewModel" in text and "SyncSpreadCardActors" in text, "controller spread helpers present")
        add(checks, "spread slot selection routed", "SelectSpreadSlot" in text and "GetSelectedSpreadSlotText" in text, "controller slot selection helpers present")
        add(checks, "spread table labels routed", "SpreadSlotLabelActors" in text and "SyncSpreadSlotLabels" in text, "table label helpers present")
        add(checks, "auto demo flag referenced", "ONOKOArcanaAutoThreeCardDemo" in (ROOT / "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaPlayerController.cpp").read_text(encoding="utf-8", errors="replace"), "command-line demo flag present")

    hud_cpp = ROOT / "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableHudWidget.cpp"
    if hud_cpp.exists():
        text = hud_cpp.read_text(encoding="utf-8", errors="replace")
        add(
            checks,
            "native slot hud controls",
            "PastSlotButton" in text
            and "PresentSlotButton" in text
            and "FutureSlotButton" in text
            and "SelectedSpreadSlotText" in text,
            "native fallback slot controls present",
        )
        add(
            checks,
            "rich native hud layout",
            "NativeFallbackRightPanel" in text
            and "NativeFallbackBottomCommandBar" in text
            and "QuestionTextBoxStyle" in text
            and "OnokoPanelColor" in text,
            "left/right panels, bottom bar, and dark input styling present",
        )
        add(
            checks,
            "generated hud overlay applied",
            "NativeFallbackHudGeneratedOverlay" in text
            and "T_HUD_ONOKO_Overlay_V1" in text
            and "SetBrushFromTexture" in text,
            "imagegen transparent HUD overlay texture is loaded and applied",
        )

    controller_h = ROOT / "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableController.h"
    if controller_h.exists():
        text = controller_h.read_text(encoding="utf-8", errors="replace")
        add(
            checks,
            "compact spread spacing for side panels",
            "SpreadCardSpacingCentimeters = 100.0f" in text
            and "SpreadCardCenterYOffsetCentimeters = 0.0f" in text,
            "three-card spread fits between richer side panels",
        )

    fail_count = sum(1 for check in checks if check["status"] == "fail")
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    report = {
        "ok": fail_count == 0,
        "generatedAtUtc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "workspace": str(ROOT),
        "failCount": fail_count,
        "latestScreenshot": str(latest_screenshot) if latest_screenshot else None,
        "checks": checks,
        "nextTask": "Promote the rich native fallback HUD into a designed WBP_TableHUD and add direct table-card selection.",
    }

    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / f"phase4-play-surface-check-{now}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"ONOKO ARCANA Phase 4 play surface: {'OK' if report['ok'] else 'FAILED'}")
    print(f"Report: {report_path}")
    print(f"Failures: {fail_count}")
    if latest_screenshot:
        print(f"Screenshot: {latest_screenshot}")
    for check in checks:
        if check["status"] != "pass":
            print(f"- FAIL: {check['name']} :: {check['detail']}")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
