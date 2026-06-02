import json
import os

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "EditorSubsystemProbeResult.json")


def names(obj):
    return sorted([name for name in dir(obj) if not name.startswith("_")])


def main():
    level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    result = {
        "ok": True,
        "editorLoadingAndSavingUtils": [
            name
            for name in names(unreal.EditorLoadingAndSavingUtils)
            if "map" in name.lower() or "save" in name.lower() or "load" in name.lower() or "new" in name.lower()
        ],
        "levelEditorSubsystem": [name for name in names(level) if "level" in name.lower() or "save" in name.lower()],
        "editorActorSubsystem": [name for name in names(actor) if "spawn" in name.lower() or "actor" in name.lower() or "destroy" in name.lower()],
        "hasLevelNewLevel": hasattr(level, "new_level"),
        "hasLevelLoadLevel": hasattr(level, "load_level"),
        "hasLevelSaveCurrentLevel": hasattr(level, "save_current_level"),
        "hasActorSpawnObject": hasattr(actor, "spawn_actor_from_object"),
        "hasActorDestroy": hasattr(actor, "destroy_actor"),
    }
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


main()
