import json
import os

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "DeckRuntimeBindingProbeResult.json")


def stringify(value):
    try:
        return str(value)
    except Exception as exc:
        return f"<stringify failed: {exc}>"


def call_variant(label, func, *args):
    try:
        value = func(*args)
        return {
            "label": label,
            "ok": True,
            "type": type(value).__name__,
            "repr": repr(value),
            "str": stringify(value),
        }
    except Exception as exc:
        return {
            "label": label,
            "ok": False,
            "errorType": type(exc).__name__,
            "error": str(exc),
        }


def main():
    deck = unreal.new_object(unreal.OnokoArcanaDeckRuntime)
    manifest_path = os.path.abspath(os.path.join(PROJECT_DIR, "..", "..", "data", "major-arcana-v5-deck.json"))
    result = {
        "classDoc": getattr(unreal.OnokoArcanaDeckRuntime, "__doc__", ""),
        "loadMajorDoc": getattr(deck.load_major_arcana_v5_manifest, "__doc__", ""),
        "loadFromFileDoc": getattr(deck.load_from_manifest_file, "__doc__", ""),
        "drawOneDoc": getattr(deck.draw_one, "__doc__", ""),
        "manifestPath": manifest_path,
        "manifestExists": os.path.exists(manifest_path),
        "calls": [
            call_variant("load_major_no_args", deck.load_major_arcana_v5_manifest),
            call_variant("load_major_empty_string", deck.load_major_arcana_v5_manifest, ""),
            call_variant("load_from_file_path_only", deck.load_from_manifest_file, manifest_path),
            call_variant("load_from_file_path_empty_string", deck.load_from_manifest_file, manifest_path, ""),
            call_variant("draw_one_no_args", deck.draw_one),
            call_variant("draw_one_true", deck.draw_one, True),
            call_variant("draw_one_false", deck.draw_one, False),
        ],
        "deckId": deck.deck_id,
        "cardCount": len(deck.cards),
        "remaining": deck.get_remaining_count(),
    }

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


main()
