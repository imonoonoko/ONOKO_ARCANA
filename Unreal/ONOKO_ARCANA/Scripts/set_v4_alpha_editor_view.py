import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "V4AlphaEditorViewResult.json")
MAP_PATH = "/Game/ONOKOArcana/Maps/L_QA_CardAlpha_Check"


def main():
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    unreal.EditorLevelLibrary.load_level(MAP_PATH)

    location = unreal.Vector(0.0, 120.0, 620.0)
    rotation = unreal.Rotator(-90.0, 0.0, 0.0)
    viewport_set = False
    error = None
    try:
        unreal.EditorLevelLibrary.set_level_viewport_camera_info(location, rotation)
        viewport_set = True
    except Exception as exc:
        error = str(exc)

    try:
        unreal.EditorLevelLibrary.editor_invalidate_viewports()
    except Exception:
        pass

    result = {
        "ok": viewport_set,
        "mapPath": MAP_PATH,
        "camera": {
            "location": [location.x, location.y, location.z],
            "rotation": [rotation.roll, rotation.pitch, rotation.yaw],
        },
        "error": error,
        "hasSetLevelViewportCameraInfo": hasattr(unreal.EditorLevelLibrary, "set_level_viewport_camera_info"),
    }
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    unreal.log("[ONOKO_ARCANA_V4_ALPHA_VIEW] " + json.dumps(result, ensure_ascii=False))


try:
    main()
except Exception as exc:
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump({"ok": False, "mapPath": MAP_PATH, "error": str(exc)}, fp, ensure_ascii=False, indent=2)
    unreal.log_error("[ONOKO_ARCANA_V4_ALPHA_VIEW] " + str(exc))
    print("[ONOKO_ARCANA_V4_ALPHA_VIEW_ERROR] " + str(exc), file=sys.stderr)
    raise
