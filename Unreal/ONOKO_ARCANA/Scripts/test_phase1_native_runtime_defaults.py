import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, "..", ".."))
DEFAULT_ENGINE_PATH = os.path.join(PROJECT_DIR, "Config", "DefaultEngine.ini")
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase1NativeRuntimeDefaultsTestResult.json")


def read_default_engine():
    with open(DEFAULT_ENGINE_PATH, "r", encoding="utf-8") as fp:
        return fp.read()


def has_text(value, needle):
    return needle in (value or "")


def safe_get_default_object(cls):
    try:
        return unreal.get_default_object(cls)
    except Exception as exc:
        return {"error": str(exc)}


def get_property(obj, name):
    try:
        return obj.get_editor_property(name)
    except Exception as exc:
        return f"<error: {exc}>"


def main():
    default_engine = read_default_engine()
    controller_doc = getattr(unreal.OnokoArcanaPlayerController, "__doc__", "")
    hud_doc = getattr(unreal.OnokoArcanaTableHudWidget, "__doc__", "")

    controller_cdo = safe_get_default_object(unreal.OnokoArcanaPlayerController)
    if isinstance(controller_cdo, dict):
        controller_defaults = controller_cdo
    else:
        controller_defaults = {
            "tableHudWidgetClass": str(get_property(controller_cdo, "table_hud_widget_class")),
            "autoCreateTableHud": bool(get_property(controller_cdo, "auto_create_table_hud")),
            "autoSpawnPhase1Actors": bool(get_property(controller_cdo, "auto_spawn_phase1_actors")),
            "hideExistingStaticMeshActorsForPhase1": bool(get_property(controller_cdo, "hide_existing_static_mesh_actors_for_phase1")),
            "autoSpawnPhase1TableSurface": bool(get_property(controller_cdo, "auto_spawn_phase1_table_surface")),
            "autoSpawnPhase1Camera": bool(get_property(controller_cdo, "auto_spawn_phase1_camera")),
            "useGameAndUiInputMode": bool(get_property(controller_cdo, "use_game_and_ui_input_mode")),
        }

    checks = {
        "hasHudClass": hasattr(unreal, "OnokoArcanaTableHudWidget"),
        "hudClassExposesQuestionTextBox": has_text(hud_doc, "question_text_box"),
        "hasPlayerControllerClass": hasattr(unreal, "OnokoArcanaPlayerController"),
        "playerControllerExposesAutoSpawn": has_text(controller_doc, "auto_spawn_phase1_actors"),
        "defaultMapIsPhase1": "GameDefaultMap=/Game/ONOKOArcana/Maps/L_Phase1_OneCard_Table" in default_engine,
        "startupMapIsPhase1": "EditorStartupMap=/Game/ONOKOArcana/Maps/L_Phase1_OneCard_Table" in default_engine,
        "defaultGameModeIsOnoko": "GlobalDefaultGameMode=/Script/ONOKO_ARCANA.OnokoArcanaGameMode" in default_engine,
        "autoHudEnabled": controller_defaults.get("autoCreateTableHud") is True,
        "autoSpawnEnabled": controller_defaults.get("autoSpawnPhase1Actors") is True,
        "hideExistingStaticMeshesEnabled": controller_defaults.get("hideExistingStaticMeshActorsForPhase1") is True,
        "autoTableEnabled": controller_defaults.get("autoSpawnPhase1TableSurface") is True,
        "autoCameraEnabled": controller_defaults.get("autoSpawnPhase1Camera") is True,
        "hudClassDefaultAssigned": "OnokoArcanaTableHudWidget" in controller_defaults.get("tableHudWidgetClass", ""),
    }

    result = {
        "ok": all(checks.values()),
        "checks": checks,
        "controllerDefaults": controller_defaults,
        "defaultEnginePath": DEFAULT_ENGINE_PATH,
    }

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 1 native runtime defaults test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE1_NATIVE_RUNTIME_DEFAULTS_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
