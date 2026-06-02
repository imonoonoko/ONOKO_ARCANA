import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANIFEST_PATH = os.path.join(
    PROJECT_DIR,
    "ImportStaging",
    "Phase0_CardTextures",
    "phase0-card-import-manifest.json",
)
RESULT_PATH = os.path.join(
    PROJECT_DIR,
    "ImportStaging",
    "Phase0_CardTextures",
    "phase0-import-result.json",
)


def log(message):
    unreal.log("[ONOKO_ARCANA_PHASE0] " + message)
    print("[ONOKO_ARCANA_PHASE0] " + message)


def load_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as fp:
        return json.load(fp)


def import_textures(manifest):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    tasks = []

    staging_dir = os.path.dirname(MANIFEST_PATH)
    for item in manifest["items"]:
        filename = os.path.abspath(os.path.join(staging_dir, item["stagedRelative"]))
        if not os.path.exists(filename):
            raise RuntimeError(f"Missing staged texture: {filename}")

        destination_name = item["targetObjectPath"].rstrip("/").split("/")[-1]

        task = unreal.AssetImportTask()
        task.filename = filename
        task.destination_path = manifest["targetContentRoot"]
        task.destination_name = destination_name
        task.automated = True
        task.replace_existing = True
        task.save = True
        tasks.append(task)

    asset_tools.import_asset_tasks(tasks)
    return tasks


def validate_imports(tasks, manifest):
    results = []
    expected_size = (1024, 1536)

    for task, item in zip(tasks, manifest["items"]):
        imported_paths = list(task.imported_object_paths)
        if not imported_paths:
            raise RuntimeError(f"Import produced no asset for {item['id']}")

        asset_path = imported_paths[0]
        texture = unreal.load_asset(asset_path)
        if texture is None:
            raise RuntimeError(f"Imported asset could not be loaded: {asset_path}")

        width = int(texture.blueprint_get_size_x())
        height = int(texture.blueprint_get_size_y())
        expected = (width, height) == expected_size

        texture.srgb = True
        texture.modify()
        unreal.EditorAssetLibrary.save_loaded_asset(texture, only_if_is_dirty=False)

        results.append(
            {
                "id": item["id"],
                "assetPath": asset_path,
                "width": width,
                "height": height,
                "expected1024x1536": expected,
            }
        )

    return results


def main():
    manifest = load_manifest()
    log(f"Import target: {manifest['targetContentRoot']}")
    tasks = import_textures(manifest)
    results = validate_imports(tasks, manifest)

    ok = all(item["expected1024x1536"] for item in results)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(
            {
                "ok": ok,
                "manifest": os.path.relpath(MANIFEST_PATH, PROJECT_DIR),
                "results": results,
            },
            fp,
            ensure_ascii=False,
            indent=2,
        )

    if not ok:
        raise RuntimeError("One or more imported textures did not match 1024x1536")

    log(f"Imported {len(results)} textures")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_PHASE0] " + str(exc))
    print("[ONOKO_ARCANA_PHASE0_ERROR] " + str(exc), file=sys.stderr)
    raise
