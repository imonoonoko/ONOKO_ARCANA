import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAGING_DIR = os.path.join(PROJECT_DIR, "ImportStaging", "MajorArcana_V5_Full")
RESULT_PATH = os.path.join(STAGING_DIR, "v5-full-import-result.json")

TARGET_ROOT = "/Game/ONOKOArcana/Cards/Textures/V5Full"

CARDS = [
    ("card-back", "card-back-onoko-v5-alpha.png", "T_Card_Back_ONOKO_V5_Alpha"),
    ("major-00-fool", "major-00-fool-onoko-v5-alpha.png", "T_Major_00_Fool_ONOKO_V5_Alpha"),
    ("major-01-magician", "major-01-magician-onoko-v5-alpha.png", "T_Major_01_Magician_ONOKO_V5_Alpha"),
    ("major-02-high-priestess", "major-02-high-priestess-onoko-v5-alpha.png", "T_Major_02_High_Priestess_ONOKO_V5_Alpha"),
    ("major-03-empress", "major-03-empress-onoko-v5-alpha.png", "T_Major_03_Empress_ONOKO_V5_Alpha"),
    ("major-04-emperor", "major-04-emperor-onoko-v5-alpha.png", "T_Major_04_Emperor_ONOKO_V5_Alpha"),
    ("major-05-hierophant", "major-05-hierophant-onoko-v5-alpha.png", "T_Major_05_Hierophant_ONOKO_V5_Alpha"),
    ("major-06-lovers", "major-06-lovers-onoko-v5-alpha.png", "T_Major_06_Lovers_ONOKO_V5_Alpha"),
    ("major-07-chariot", "major-07-chariot-onoko-v5-alpha.png", "T_Major_07_Chariot_ONOKO_V5_Alpha"),
    ("major-08-strength", "major-08-strength-onoko-v5-alpha.png", "T_Major_08_Strength_ONOKO_V5_Alpha"),
    ("major-09-hermit", "major-09-hermit-onoko-v5-alpha.png", "T_Major_09_Hermit_ONOKO_V5_Alpha"),
    ("major-10-wheel-of-fortune", "major-10-wheel-of-fortune-onoko-v5-alpha.png", "T_Major_10_Wheel_Of_Fortune_ONOKO_V5_Alpha"),
    ("major-11-justice", "major-11-justice-onoko-v5-alpha.png", "T_Major_11_Justice_ONOKO_V5_Alpha"),
    ("major-12-hanged-man", "major-12-hanged-man-onoko-v5-alpha.png", "T_Major_12_Hanged_Man_ONOKO_V5_Alpha"),
    ("major-13-death", "major-13-death-onoko-v5-alpha.png", "T_Major_13_Death_ONOKO_V5_Alpha"),
    ("major-14-temperance", "major-14-temperance-onoko-v5-alpha.png", "T_Major_14_Temperance_ONOKO_V5_Alpha"),
    ("major-15-devil", "major-15-devil-onoko-v5-alpha.png", "T_Major_15_Devil_ONOKO_V5_Alpha"),
    ("major-16-tower", "major-16-tower-onoko-v5-alpha.png", "T_Major_16_Tower_ONOKO_V5_Alpha"),
    ("major-17-star", "major-17-star-onoko-v5-alpha.png", "T_Major_17_Star_ONOKO_V5_Alpha"),
    ("major-18-moon", "major-18-moon-onoko-v5-alpha.png", "T_Major_18_Moon_ONOKO_V5_Alpha"),
    ("major-19-sun", "major-19-sun-onoko-v5-alpha.png", "T_Major_19_Sun_ONOKO_V5_Alpha"),
    ("major-20-judgement", "major-20-judgement-onoko-v5-alpha.png", "T_Major_20_Judgement_ONOKO_V5_Alpha"),
    ("major-21-world", "major-21-world-onoko-v5-alpha.png", "T_Major_21_World_ONOKO_V5_Alpha"),
]


def log(message):
    unreal.log("[ONOKO_ARCANA_V5_FULL_IMPORT] " + message)
    print("[ONOKO_ARCANA_V5_FULL_IMPORT] " + message)


def main():
    os.makedirs(STAGING_DIR, exist_ok=True)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    tasks = []

    for card_id, filename, destination_name in CARDS:
        source = os.path.abspath(os.path.join(STAGING_DIR, filename))
        if not os.path.exists(source):
            raise RuntimeError(f"Missing staged texture for {card_id}: {source}")
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
    for task, (card_id, filename, destination_name) in zip(tasks, CARDS):
        imported_paths = list(task.imported_object_paths)
        if not imported_paths:
            raise RuntimeError(f"Import produced no asset for {card_id}")

        texture = unreal.load_asset(imported_paths[0])
        if texture is None:
            raise RuntimeError(f"Imported asset could not be loaded: {imported_paths[0]}")

        texture.srgb = True
        texture.modify()
        unreal.EditorAssetLibrary.save_loaded_asset(texture, only_if_is_dirty=False)

        width = int(texture.blueprint_get_size_x())
        height = int(texture.blueprint_get_size_y())
        results.append(
            {
                "id": card_id,
                "sourceFile": filename,
                "destinationName": destination_name,
                "assetPath": imported_paths[0],
                "width": width,
                "height": height,
                "expectedSize": [1024, 1536],
                "sizeOk": (width, height) == (1024, 1536),
            }
        )

    payload = {
        "ok": all(item["sizeOk"] for item in results),
        "targetRoot": TARGET_ROOT,
        "count": len(results),
        "results": results,
    }
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)

    if not payload["ok"]:
        raise RuntimeError("One or more V5 full textures did not match 1024x1536")
    log(f"Imported {len(results)} V5 full textures")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_V5_FULL_IMPORT] " + str(exc))
    print("[ONOKO_ARCANA_V5_FULL_IMPORT_ERROR] " + str(exc), file=sys.stderr)
    raise
