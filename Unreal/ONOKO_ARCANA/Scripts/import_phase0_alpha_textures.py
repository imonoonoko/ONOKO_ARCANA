import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAGING_DIR = os.path.join(PROJECT_DIR, "ImportStaging", "Phase0_CardTexturesAlpha")
MANIFEST_PATH = os.path.join(STAGING_DIR, "phase0-alpha-card-import-manifest.json")
RESULT_PATH = os.path.join(STAGING_DIR, "phase0-alpha-import-result.json")


def log(message):
    unreal.log("[ONOKO_ARCANA_PHASE0_ALPHA_IMPORT] " + message)
    print("[ONOKO_ARCANA_PHASE0_ALPHA_IMPORT] " + message)


def main():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as fp:
        manifest = json.load(fp)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    tasks = []
    for item in manifest["items"]:
        filename = os.path.abspath(os.path.join(STAGING_DIR, item["stagedRelative"]))
        if not os.path.exists(filename):
            raise RuntimeError(f"Missing staged alpha texture: {filename}")

        task = unreal.AssetImportTask()
        task.filename = filename
        task.destination_path = manifest["targetContentRoot"]
        task.destination_name = item["targetObjectPath"].rstrip("/").split("/")[-1]
        task.automated = True
        task.replace_existing = True
        task.save = True
        tasks.append(task)

    asset_tools.import_asset_tasks(tasks)

    results = []
    for task, item in zip(tasks, manifest["items"]):
        imported_paths = list(task.imported_object_paths)
        if not imported_paths:
            raise RuntimeError(f"Import produced no asset for {item['id']}")
        texture = unreal.load_asset(imported_paths[0])
        if texture is None:
            raise RuntimeError(f"Imported asset could not be loaded: {imported_paths[0]}")

        texture.srgb = True
        texture.modify()
        unreal.EditorAssetLibrary.save_loaded_asset(texture, only_if_is_dirty=False)
        results.append({
            "id": item["id"],
            "assetPath": imported_paths[0],
            "width": int(texture.blueprint_get_size_x()),
            "height": int(texture.blueprint_get_size_y()),
            "expected1024x1536": int(texture.blueprint_get_size_x()) == 1024 and int(texture.blueprint_get_size_y()) == 1536,
        })

    ok = all(r["expected1024x1536"] for r in results)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump({"ok": ok, "results": results}, fp, ensure_ascii=False, indent=2)
    if not ok:
        raise RuntimeError("One or more alpha textures did not match 1024x1536")
    log(f"Imported {len(results)} alpha textures")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_PHASE0_ALPHA_IMPORT] " + str(exc))
    print("[ONOKO_ARCANA_PHASE0_ALPHA_IMPORT_ERROR] " + str(exc), file=sys.stderr)
    raise
