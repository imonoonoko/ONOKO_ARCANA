import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAGING_DIR = os.path.join(PROJECT_DIR, "ImportStaging", "HUD")
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase4HudTextureImportResult.json")

TARGET_ROOT = "/Game/ONOKOArcana/UI/HUD/Textures"

HUD_TEXTURES = [
    ("hud-overlay-v1", "onoko-hud-overlay-v1-alpha.png", "T_HUD_ONOKO_Overlay_V1"),
]


def log(message):
    unreal.log("[ONOKO_ARCANA_PHASE4_HUD_IMPORT] " + message)
    print("[ONOKO_ARCANA_PHASE4_HUD_IMPORT] " + message)


def main():
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    tasks = []

    for texture_id, filename, destination_name in HUD_TEXTURES:
        source = os.path.abspath(os.path.join(STAGING_DIR, filename))
        if not os.path.exists(source):
            raise RuntimeError(f"Missing staged HUD texture for {texture_id}: {source}")

        task = unreal.AssetImportTask()
        task.filename = source
        task.destination_path = TARGET_ROOT
        task.destination_name = destination_name
        task.automated = True
        task.replace_existing = True
        task.save = True
        tasks.append(task)

    asset_tools.import_asset_tasks(tasks)

    results = []
    for task, (texture_id, filename, destination_name) in zip(tasks, HUD_TEXTURES):
        imported_paths = list(task.imported_object_paths)
        if not imported_paths:
            raise RuntimeError(f"Import produced no asset for {texture_id}")

        texture = unreal.load_asset(imported_paths[0])
        if texture is None:
            raise RuntimeError(f"Imported HUD texture could not be loaded: {imported_paths[0]}")

        texture.srgb = True
        if hasattr(unreal.TextureCompressionSettings, "TC_USER_INTERFACE_2D"):
            texture.compression_settings = unreal.TextureCompressionSettings.TC_USER_INTERFACE_2D
        elif hasattr(unreal.TextureCompressionSettings, "TC_EDITOR_ICON"):
            texture.compression_settings = unreal.TextureCompressionSettings.TC_EDITOR_ICON
        if hasattr(unreal.TextureMipGenSettings, "TMGS_NO_MIPMAPS"):
            texture.mip_gen_settings = unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS
        texture.modify()
        unreal.EditorAssetLibrary.save_loaded_asset(texture, only_if_is_dirty=False)

        width = int(texture.blueprint_get_size_x())
        height = int(texture.blueprint_get_size_y())
        results.append(
            {
                "id": texture_id,
                "sourceFile": filename,
                "destinationName": destination_name,
                "assetPath": imported_paths[0],
                "width": width,
                "height": height,
                "sizeOk": width >= 1200 and height >= 675,
            }
        )

    payload = {
        "ok": all(item["sizeOk"] for item in results),
        "targetRoot": TARGET_ROOT,
        "count": len(results),
        "results": results,
    }
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)

    if not payload["ok"]:
        raise RuntimeError("One or more HUD textures did not meet the expected screen overlay size")
    log(f"Imported {len(results)} HUD texture(s)")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_PHASE4_HUD_IMPORT] " + str(exc))
    print("[ONOKO_ARCANA_PHASE4_HUD_IMPORT_ERROR] " + str(exc), file=sys.stderr)
    raise
