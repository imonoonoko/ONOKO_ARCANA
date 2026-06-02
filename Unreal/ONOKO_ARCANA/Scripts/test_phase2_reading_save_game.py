import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase2ReadingSaveGameTestResult.json")
SLOT_NAME = "ONOKO_ARCANA_CommandletSaveSmokeTest"
USER_INDEX = 0


def get_field(obj, name, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        return default


def unpack_error(value):
    if value is None:
        return True, ""
    if isinstance(value, str):
        return value == "", value
    if isinstance(value, tuple):
        error = ""
        for item in value:
            if isinstance(item, str):
                error = item
        return error == "", error
    return bool(value), str(value)


def unpack_draw(value, session):
    error = ""
    draw = None
    if isinstance(value, tuple):
        for item in value:
            if isinstance(item, str):
                error = item
            elif get_field(item, "card") is not None:
                draw = item
    else:
        draw = get_field(session, "current_draw")
    return error == "" and draw is not None and bool(get_field(draw, "success", False)), draw, error


def unpack_saved_reading(value):
    error = ""
    reading = None
    if isinstance(value, tuple):
        for item in value:
            if isinstance(item, str):
                error = item
            elif get_field(item, "card_id") is not None:
                reading = item
    elif get_field(value, "card_id") is not None:
        reading = value
    return error == "" and reading is not None and get_field(reading, "card_id", "") != "", reading, error


def unpack_save_game(value):
    error = ""
    save_game = None
    if isinstance(value, tuple):
        for item in value:
            if isinstance(item, str):
                error = item
            elif get_field(item, "readings") is not None:
                save_game = item
    elif get_field(value, "readings") is not None:
        save_game = value
    return error == "" and save_game is not None, save_game, error


def main():
    unreal.OnokoArcanaReadingSaveLibrary.delete_readings_slot(SLOT_NAME, USER_INDEX)

    session = unreal.new_object(unreal.OnokoArcanaOneCardSession)
    result = {
        "ok": False,
        "slotName": SLOT_NAME,
        "steps": [],
        "saveLibraryDoc": getattr(unreal.OnokoArcanaReadingSaveLibrary, "__doc__", ""),
        "saveGameDoc": getattr(unreal.OnokoArcanaReadingSaveGame, "__doc__", ""),
    }

    init_ok, init_error = unpack_error(session.initialize_major_arcana_v5())
    result["steps"].append({"step": "initialize", "ok": init_ok, "error": init_error})

    start_ok, start_error = unpack_error(session.start_new_reading("保存テスト用の問い", 777, True))
    result["steps"].append({"step": "start", "ok": start_ok, "error": start_error})

    draw_ok, draw, draw_error = unpack_draw(session.draw_one(True), session)
    result["steps"].append(
        {
            "step": "draw",
            "ok": draw_ok,
            "error": draw_error,
            "cardId": get_field(get_field(draw, "card"), "id"),
        }
    )

    session.submit_user_interpretation("保存対象のユーザー解釈。")
    reveal_ok, reveal_error = unpack_error(session.reveal_guide())
    result["steps"].append({"step": "reveal_guide", "ok": reveal_ok, "error": reveal_error})

    make_ok, reading, make_error = unpack_saved_reading(
        unreal.OnokoArcanaReadingSaveLibrary.make_saved_reading_from_session(session)
    )
    result["steps"].append(
        {
            "step": "make_saved_reading",
            "ok": make_ok,
            "error": make_error,
            "cardId": get_field(reading, "card_id"),
            "userInterpretation": get_field(reading, "user_interpretation"),
            "guideRevealed": get_field(reading, "guide_revealed"),
        }
    )

    save_ok, save_error = unpack_error(
        unreal.OnokoArcanaReadingSaveLibrary.save_reading_to_slot(reading, SLOT_NAME, USER_INDEX)
    )
    result["steps"].append({"step": "save_to_slot", "ok": save_ok, "error": save_error})

    load_ok, save_game, load_error = unpack_save_game(
        unreal.OnokoArcanaReadingSaveLibrary.load_readings_from_slot(SLOT_NAME, USER_INDEX)
    )
    readings = list(get_field(save_game, "readings", []) or [])
    loaded_reading = readings[0] if readings else None
    result["steps"].append(
        {
            "step": "load_from_slot",
            "ok": load_ok and len(readings) == 1,
            "error": load_error,
            "readingCount": len(readings),
            "loadedCardId": get_field(loaded_reading, "card_id"),
            "loadedUserInterpretation": get_field(loaded_reading, "user_interpretation"),
        }
    )

    delete_ok = bool(unreal.OnokoArcanaReadingSaveLibrary.delete_readings_slot(SLOT_NAME, USER_INDEX))
    result["steps"].append({"step": "delete_test_slot", "ok": delete_ok})

    result["ok"] = all(step["ok"] for step in result["steps"])

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 2 reading SaveGame test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE2_READING_SAVE_GAME_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
