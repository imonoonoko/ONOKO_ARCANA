import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase1DeckRuntimeTestResult.json")


def unpack_bool_error(value):
    if value is None:
        return True, ""
    if isinstance(value, str):
        return value == "", value
    return bool(value), str(value)


def unpack_draw(value):
    if isinstance(value, tuple):
        if len(value) >= 2:
            return bool(value[0]), value[1]
        if len(value) == 1:
            return bool(value[0]), None
    if value is None:
        return False, None
    return bool(get_field(value, "success", True)), value


def get_field(obj, name, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        return default


def main():
    deck_class = unreal.OnokoArcanaDeckRuntime
    deck = unreal.new_object(deck_class)

    ok, error = unpack_bool_error(deck.load_major_arcana_v5_manifest())
    result = {
        "ok": False,
        "loadOk": ok,
        "loadError": error,
        "cardCount": len(deck.cards) if ok else 0,
        "deckId": deck.deck_id if ok else None,
        "initialRemaining": deck.get_remaining_count() if ok else None,
        "draws": [],
        "duplicates": [],
    }

    if ok:
        deck.reset_draw_state(12345, True)
        seen = set()
        for _index in range(22):
            draw_ok, draw_result = unpack_draw(deck.draw_one(True))
            card = get_field(draw_result, "card")
            card_id = get_field(card, "id") if card is not None else None
            orientation = str(get_field(draw_result, "orientation", ""))
            active_keywords = list(get_field(draw_result, "active_keywords", []) or [])
            if card_id in seen:
                result["duplicates"].append(card_id)
            if card_id:
                seen.add(card_id)
            result["draws"].append(
                {
                    "ok": draw_ok,
                    "id": card_id,
                    "orientation": orientation,
                    "activeKeywordCount": len(active_keywords),
                    "remaining": deck.get_remaining_count(),
                }
            )

        final_ok, _final_result = unpack_draw(deck.draw_one(True))
        result["extraDrawAfterDeckEmpty"] = final_ok
        result["finalRemaining"] = deck.get_remaining_count()
        result["uniqueDrawCount"] = len(seen)
        result["ok"] = (
            result["loadOk"]
            and result["cardCount"] == 22
            and result["initialRemaining"] == 22
            and result["uniqueDrawCount"] == 22
            and len(result["duplicates"]) == 0
            and result["finalRemaining"] == 0
            and not result["extraDrawAfterDeckEmpty"]
            and all(item["ok"] and item["activeKeywordCount"] > 0 for item in result["draws"])
        )

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 1 deck runtime test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE1_DECK_RUNTIME_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
