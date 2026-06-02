import json
import os
import sys
import time

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_DIR = os.path.abspath(os.path.join(PROJECT_DIR, "..", ".."))
MAP_PATH = "/Game/ONOKOArcana/Maps/L_QA_CardAlpha_V5_Full"
OUTPUT_DIR = os.path.join(REPO_DIR, "assets", "generated", "reports")
OUTPUT_NAME = "v5-full-alpha-qa-map-unreal-render-2026-06-01.png"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "V5FullAlphaQARenderResult.json")


def log(message):
    unreal.log("[ONOKO_ARCANA_V5_FULL_ALPHA_RENDER] " + message)
    print("[ONOKO_ARCANA_V5_FULL_ALPHA_RENDER] " + message)


def set_property_if_available(obj, prop, value):
    try:
        obj.set_editor_property(prop, value)
        return True
    except Exception:
        return False


def get_capture_component(actor):
    for prop in ("scene_capture_component2d", "capture_component2d"):
        try:
            component = getattr(actor, prop)
            if component is not None:
                return component
        except Exception:
            pass
    try:
        components = actor.get_components_by_class(unreal.SceneCaptureComponent2D)
        if components:
            return components[0]
    except Exception:
        pass
    raise RuntimeError("Could not find SceneCaptureComponent2D on SceneCapture2D actor.")


def create_render_target(width, height):
    render_target = unreal.TextureRenderTarget2D()
    try:
        render_target.init_custom_format(width, height, unreal.PixelFormat.PF_B8G8R8A8, False)
    except Exception:
        try:
            render_target.init_auto_format(width, height)
        except Exception:
            set_property_if_available(render_target, "size_x", width)
            set_property_if_available(render_target, "size_y", height)
    set_property_if_available(render_target, "clear_color", unreal.LinearColor(0.0, 0.0, 0.0, 1.0))
    set_property_if_available(render_target, "force_linear_gamma", True)
    return render_target


def export_render_target(world, render_target):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
    unreal.RenderingLibrary.export_render_target(world, render_target, OUTPUT_DIR, OUTPUT_NAME)
    deadline = time.time() + 30.0
    while time.time() < deadline:
        if os.path.exists(OUTPUT_PATH) and os.path.getsize(OUTPUT_PATH) > 0:
            return
        time.sleep(0.25)
    raise RuntimeError(f"Render target export did not create {OUTPUT_PATH}")


def main():
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    unreal.EditorLevelLibrary.load_level(MAP_PATH)
    world = unreal.EditorLevelLibrary.get_editor_world()
    if world is None:
        raise RuntimeError("Could not access editor world.")

    render_target = create_render_target(2048, 1152)
    capture_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SceneCapture2D,
        unreal.Vector(0.0, 300.0, 1600.0),
        unreal.Rotator(-90.0, 0.0, 0.0),
    )
    try:
        capture_actor.set_actor_label("V5_Full_QA_Topdown_RenderCapture")
    except Exception:
        pass

    capture = get_capture_component(capture_actor)
    set_property_if_available(capture, "texture_target", render_target)
    set_property_if_available(capture, "projection_type", unreal.CameraProjectionMode.ORTHOGRAPHIC)
    set_property_if_available(capture, "ortho_width", 1280.0)
    set_property_if_available(capture, "capture_source", unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
    set_property_if_available(capture, "capture_every_frame", False)
    set_property_if_available(capture, "capture_on_movement", False)

    try:
        capture.capture_scene()
    except Exception as exc:
        raise RuntimeError(f"capture_scene failed: {exc}") from exc

    export_render_target(world, render_target)
    unreal.EditorLevelLibrary.destroy_actor(capture_actor)

    result = {
        "ok": True,
        "mapPath": MAP_PATH,
        "outputPath": OUTPUT_PATH,
        "outputSize": [2048, 1152],
        "capture": {
            "location": [0.0, 300.0, 1600.0],
            "rotation": [-90.0, 0.0, 0.0],
            "projection": "orthographic",
            "orthoWidth": 1280.0,
        },
    }
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    log(f"Rendered {OUTPUT_PATH}")


try:
    main()
except Exception as exc:
    error = {
        "ok": False,
        "mapPath": MAP_PATH,
        "outputPath": OUTPUT_PATH,
        "error": str(exc),
    }
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(error, fp, ensure_ascii=False, indent=2)
    unreal.log_error("[ONOKO_ARCANA_V5_FULL_ALPHA_RENDER] " + str(exc))
    print("[ONOKO_ARCANA_V5_FULL_ALPHA_RENDER_ERROR] " + str(exc), file=sys.stderr)
    raise
