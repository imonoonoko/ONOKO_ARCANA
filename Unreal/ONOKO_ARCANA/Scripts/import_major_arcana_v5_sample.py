import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAGING_DIR = os.path.join(PROJECT_DIR, "ImportStaging", "MajorArcana_V5")
RESULT_PATH = os.path.join(STAGING_DIR, "v5-sample-import-result.json")

CARD_TARGET_ROOT = "/Game/ONOKOArcana/Cards/Textures/V5"
QA_TARGET_ROOT = "/Game/ONOKOArcana/QA/Textures"

ITEMS = [
    {
        "id": "major-01-magician-v5-clean",
        "file": "major-01-magician-onoko-v5-clean-alpha.png",
        "destinationPath": CARD_TARGET_ROOT,
        "destinationName": "T_Major_01_Magician_ONOKO_V5_Clean_Alpha",
        "expectedSize": (1024, 1536),
    },
    {
        "id": "qa-checkerboard",
        "file": "qa-checkerboard-v1.png",
        "destinationPath": QA_TARGET_ROOT,
        "destinationName": "T_QA_Checkerboard_V1",
        "expectedSize": (1024, 1024),
    },
]


def log(message):
    unreal.log("[ONOKO_ARCANA_V5_IMPORT] " + message)
    print("[ONOKO_ARCANA_V5_IMPORT] " + message)


def main():
    os.makedirs(STAGING_DIR, exist_ok=True)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    tasks = []

    for item in ITEMS:
        filename = os.path.abspath(os.path.join(STAGING_DIR, item["file"]))
        if not os.path.exists(filename):
            raise RuntimeError(f"Missing staged texture: {filename}")
        task = unreal.AssetImportTask()
        task.filename = filename
        task.destination_path = item["destinationPath"]
        task.destination_name = item["destinationName"]
        task.automated = True
        task.replace_existing = True
        task.save = True
        tasks.append(task)

    asset_tools.import_asset_tasks(tasks)

    results = []
    for task, item in zip(tasks, ITEMS):
        imported_paths = list(task.imported_object_paths)
        if not imported_paths:
            raise RuntimeError(f"Import produced no asset for {item['id']}")

        texture = unreal.load_asset(imported_paths[0])
        if texture is None:
            raise RuntimeError(f"Imported asset could not be loaded: {imported_paths[0]}")

        texture.srgb = True
        texture.modify()
        unreal.EditorAssetLibrary.save_loaded_asset(texture, only_if_is_dirty=False)
        width = int(texture.blueprint_get_size_x())
        height = int(texture.blueprint_get_size_y())
        expected_size = item["expectedSize"]
        results.append(
            {
                "id": item["id"],
                "assetPath": imported_paths[0],
                "width": width,
                "height": height,
                "expectedSize": list(expected_size),
                "sizeOk": (width, height) == expected_size,
            }
        )

    payload = {"ok": all(item["sizeOk"] for item in results), "results": results}
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)

    if not payload["ok"]:
        raise RuntimeError("One or more V5 textures did not match expected dimensions")
    log(f"Imported {len(results)} V5/QA textures")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_V5_IMPORT] " + str(exc))
    print("[ONOKO_ARCANA_V5_IMPORT_ERROR] " + str(exc), file=sys.stderr)
    raise
