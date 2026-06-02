#!/usr/bin/env python3
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
UPROJECT = ROOT / "Unreal" / "ONOKO_ARCANA" / "ONOKO_ARCANA.uproject"
REPORT_DIR = ROOT / "reports"


REQUIRED_PLUGINS = {
    "PythonScriptPlugin": True,
    "EditorScriptingUtilities": True,
}

REQUIRED_SOURCE_FILES = [
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaDeckRuntime.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaCardActor.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaOneCardSession.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaOneCardViewModel.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableController.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaTableHudWidget.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaPlayerController.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaGameMode.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaReadingSaveGame.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaReadingSaveLibrary.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaReadingHistoryViewModel.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadDefinition.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadReadingSession.h",
    "Unreal/ONOKO_ARCANA/Source/ONOKO_ARCANA/OnokoArcanaSpreadReadingViewModel.h",
]

REQUIRED_CONTENT_FILES = [
    "Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Maps/L_Phase1_OneCard_Table.umap",
    "Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Phase1/Materials/M_Phase1_CardMasked_TextureParam.uasset",
    "Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Cards/Textures/V5Full/T_Card_Back_ONOKO_V5_Alpha.uasset",
    "Unreal/ONOKO_ARCANA/Content/ONOKOArcana/UI/HUD/Textures/T_HUD_ONOKO_Overlay_V1.uasset",
]

REQUIRED_DOCS = [
    "AGENTS.md",
    "PRODUCT.md",
    "DESIGN.md",
    "plan.md",
    "docs/implementation/PHASE1_ONE_CARD_TABLE_WIRING.md",
    "docs/implementation/PHASE2_READING_SAVE_GAME.md",
    "docs/implementation/PHASE1_UE_CODEX_PREFLIGHT_2026-06-01.md",
    "docs/implementation/PHASE3_SPREAD_SELECTION_FOUNDATION.md",
    "docs/implementation/PHASE4_SPREAD_READING_RUNTIME.md",
    "docs/implementation/PHASE4_SPREAD_PLAY_SURFACE.md",
    "docs/implementation/PHASE4_SPREAD_SLOT_HUD.md",
    "docs/implementation/PHASE4_CARD_VISIBILITY_LABELS.md",
    "docs/implementation/PHASE4_RICH_NATIVE_UI.md",
    "docs/implementation/PHASE4_HUD_GENERATED_OVERLAY.md",
    "docs/design/spread-system-visual-direction-2026-06-02.md",
]

REQUIRED_UE_SCRIPTS = [
    "Unreal/ONOKO_ARCANA/Scripts/test_phase1_deck_runtime.py",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase1_hud_reflection_surface.py",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase1_one_card_session.py",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase1_one_card_view_model.py",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase1_native_runtime_defaults.py",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase2_reading_save_game.py",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase2_reading_history_view_model.py",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase3_spread_registry.py",
    "Unreal/ONOKO_ARCANA/Scripts/test_phase4_three_card_spread_session.py",
    "Unreal/ONOKO_ARCANA/Scripts/import_phase4_hud_textures.py",
]

REQUIRED_TEST_RESULTS = [
    "Unreal/ONOKO_ARCANA/Saved/Phase1DeckRuntimeTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase1HudReflectionSurfaceTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase1OneCardSessionTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase1OneCardViewModelTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase1NativeRuntimeDefaultsTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase2ReadingSaveGameTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase2ReadingHistoryViewModelTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase3SpreadRegistryTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase4ThreeCardSpreadSessionTestResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase1RuntimeMaterialsResult.json",
    "Unreal/ONOKO_ARCANA/Saved/Phase4HudTextureImportResult.json",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def check_file(path: Path) -> dict[str, Any]:
    return {
        "name": rel(path),
        "status": "pass" if path.exists() else "fail",
        "detail": "exists" if path.exists() else "missing",
    }


def add(checks: list[dict[str, Any]], name: str, ok: bool, detail: str, status_if_false: str = "fail") -> None:
    checks.append(
        {
            "name": name,
            "status": "pass" if ok else status_if_false,
            "detail": detail,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []

    add(checks, "workspace", ROOT.exists(), str(ROOT))
    add(checks, "git metadata", (ROOT / ".git").exists(), "This project currently has no .git directory.", "warn")

    if UPROJECT.exists():
        uproject = load_json(UPROJECT)
        engine_association = uproject.get("EngineAssociation")
        add(checks, "uproject", True, f"EngineAssociation={engine_association}")
        add(checks, "engine association", engine_association == "5.7", f"expected 5.7, got {engine_association!r}")

        plugins = {plugin.get("Name"): plugin for plugin in uproject.get("Plugins", [])}
        for plugin_name in REQUIRED_PLUGINS:
            plugin = plugins.get(plugin_name)
            enabled = bool(plugin and plugin.get("Enabled"))
            add(checks, f"plugin:{plugin_name}", enabled, "enabled" if enabled else "not enabled")

        common_ui = plugins.get("CommonUI")
        add(
            checks,
            "plugin:CommonUI",
            bool(common_ui and common_ui.get("Enabled")),
            "enabled; keep optional for Phase 1 UUserWidget HUD",
            "warn",
        )
    else:
        add(checks, "uproject", False, f"missing {rel(UPROJECT)}")
        engine_association = None

    engine_dir = Path("C:/Program Files/Epic Games/UE_5.7")
    add(checks, "engine dir", engine_dir.exists(), str(engine_dir))
    add(
        checks,
        "UnrealEditor.exe",
        (engine_dir / "Engine/Binaries/Win64/UnrealEditor.exe").exists(),
        str(engine_dir / "Engine/Binaries/Win64/UnrealEditor.exe"),
    )
    add(
        checks,
        "UnrealEditor-Cmd.exe",
        (engine_dir / "Engine/Binaries/Win64/UnrealEditor-Cmd.exe").exists(),
        str(engine_dir / "Engine/Binaries/Win64/UnrealEditor-Cmd.exe"),
    )

    for group_name, paths in [
        ("source", REQUIRED_SOURCE_FILES),
        ("content", REQUIRED_CONTENT_FILES),
        ("docs", REQUIRED_DOCS),
        ("ue_scripts", REQUIRED_UE_SCRIPTS),
    ]:
        missing = [path for path in paths if not (ROOT / path).exists()]
        add(checks, f"{group_name} files", not missing, "all present" if not missing else "missing: " + ", ".join(missing))

    deck_path = ROOT / "data/major-arcana-v5-deck.json"
    if deck_path.exists():
        deck = load_json(deck_path)
        cards = deck.get("cards", [])
        adopted_cards = [card for card in cards if card.get("qaStatus") == "Adopted"]
        add(checks, "v5 deck manifest", True, f"version={deck.get('version')}")
        add(checks, "v5 major count", len(cards) == 22, f"cards={len(cards)}")
        add(checks, "v5 adopted count", len(adopted_cards) == 22, f"adopted={len(adopted_cards)}")
        add(checks, "v5 card back", deck.get("back", {}).get("qaStatus") == "Adopted", f"back qa={deck.get('back', {}).get('qaStatus')}")
    else:
        add(checks, "v5 deck manifest", False, f"missing {rel(deck_path)}")

    texture_dir = ROOT / "Unreal/ONOKO_ARCANA/Content/ONOKOArcana/Cards/Textures/V5Full"
    texture_count = len(list(texture_dir.glob("*.uasset"))) if texture_dir.exists() else 0
    add(checks, "v5 texture uassets", texture_count >= 23, f"uasset_count={texture_count}")

    for result_rel in REQUIRED_TEST_RESULTS:
        result_path = ROOT / result_rel
        if not result_path.exists():
            add(checks, f"test result:{Path(result_rel).name}", False, f"missing {result_rel}")
            continue
        try:
            result = load_json(result_path)
            add(checks, f"test result:{Path(result_rel).name}", result.get("ok") is True, f"ok={result.get('ok')}")
        except json.JSONDecodeError as exc:
            add(checks, f"test result:{Path(result_rel).name}", False, f"invalid json: {exc}")

    plan_path = ROOT / "plan.md"
    if plan_path.exists():
        plan_text = plan_path.read_text(encoding="utf-8", errors="replace")
        add(
            checks,
            "known actor spawn crash noted",
            "EXCEPTION_ACCESS_VIOLATION" in plan_text,
            "plan.md records Python map actor spawn crash",
            "warn",
        )

    add(
        checks,
        "manual editor gate",
        True,
        "Next proof must be manual UE Editor/Blueprint wiring plus screenshot, not Python actor spawn.",
    )

    fail_count = sum(1 for check in checks if check["status"] == "fail")
    warn_count = sum(1 for check in checks if check["status"] == "warn")

    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    report = {
        "ok": fail_count == 0,
        "generatedAtUtc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "workspace": str(ROOT),
        "uproject": str(UPROJECT),
        "failCount": fail_count,
        "warnCount": warn_count,
        "checks": checks,
        "nextTask": "Open UE Editor and manually wire AOnokoArcanaCardActor, AOnokoArcanaTableController, and WBP_TableHUD in L_Phase1_OneCard_Table.",
    }

    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / f"phase1-preflight-check-{now}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"ONOKO ARCANA Phase 1 preflight: {'OK' if report['ok'] else 'FAILED'}")
    print(f"Report: {report_path}")
    print(f"Failures: {fail_count}  Warnings: {warn_count}")
    for check in checks:
        if check["status"] != "pass":
            print(f"- {check['status'].upper()}: {check['name']} :: {check['detail']}")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
