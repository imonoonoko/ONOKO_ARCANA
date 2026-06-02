import json
import os

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "EditorLoadingDocsProbeResult.json")


def doc(name):
    obj = getattr(unreal.EditorLoadingAndSavingUtils, name)
    return getattr(obj, "__doc__", "")


result = {
    "new_blank_map": doc("new_blank_map"),
    "save_map": doc("save_map"),
    "load_map": doc("load_map"),
    "save_current_level": doc("save_current_level"),
}
os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
with open(RESULT_PATH, "w", encoding="utf-8") as fp:
    json.dump(result, fp, ensure_ascii=False, indent=2)
print(json.dumps(result, ensure_ascii=False, indent=2))
