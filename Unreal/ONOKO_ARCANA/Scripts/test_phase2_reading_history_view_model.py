import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase2ReadingHistoryViewModelTestResult.json")
SLOT_NAME = "ONOKO_ARCANA_CommandletHistorySmokeTest"
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


def create_and_save_reading(question, seed, note):
    session = unreal.new_object(unreal.OnokoArcanaOneCardSession)
    ok, error = unpack_error(session.initialize_major_arcana_v5())
    if not ok:
        return False, None, f"initialize failed: {error}"
    ok, error = unpack_error(session.start_new_reading(question, seed, True))
    if not ok:
        return False, None, f"start failed: {error}"
    ok, draw, error = unpack_draw(session.draw_one(True), session)
    if not ok:
        return False, None, f"draw failed: {error}"
    session.submit_user_interpretation(note)
    ok, error = unpack_error(session.reveal_guide())
    if not ok:
        return False, None, f"reveal failed: {error}"
    ok, reading, error = unpack_saved_reading(
        unreal.OnokoArcanaReadingSaveLibrary.make_saved_reading_from_session(session)
    )
    if not ok:
        return False, None, f"make reading failed: {error}"
    ok, error = unpack_error(
        unreal.OnokoArcanaReadingSaveLibrary.save_reading_to_slot(reading, SLOT_NAME, USER_INDEX)
    )
    if not ok:
        return False, None, f"save failed: {error}"
    return True, reading, ""


def main():
    unreal.OnokoArcanaReadingSaveLibrary.delete_readings_slot(SLOT_NAME, USER_INDEX)

    first_ok, first_reading, first_error = create_and_save_reading(
        "最初の保存テスト",
        101,
        "最初の履歴メモ。",
    )
    second_ok, second_reading, second_error = create_and_save_reading(
        "二つ目の保存テスト",
        202,
        "二つ目の履歴メモ。",
    )

    history = unreal.new_object(unreal.OnokoArcanaReadingHistoryViewModel)
    load_ok = bool(history.load_from_slot(SLOT_NAME, USER_INDEX))
    latest_summary = history.get_latest_reading_summary()
    selected_title_initial = history.get_selected_title_text()
    selected_detail_initial = history.get_selected_detail_text()
    select_second_ok = bool(history.select_reading(1))
    selected_detail_second = history.get_selected_detail_text()

    result = {
        "ok": False,
        "slotName": SLOT_NAME,
        "steps": [
            {"step": "save_first", "ok": first_ok, "error": first_error},
            {"step": "save_second", "ok": second_ok, "error": second_error},
            {
                "step": "load_history",
                "ok": load_ok,
                "error": history.last_error_message,
                "readingCount": history.get_reading_count(),
                "hasHistory": history.has_history(),
                "selectedIndex": history.get_selected_index(),
            },
            {
                "step": "latest_summary",
                "ok": "二つ目の保存テスト" in latest_summary,
                "latestSummary": latest_summary,
            },
            {
                "step": "initial_selection",
                "ok": selected_title_initial != "" and "二つ目の履歴メモ。" in selected_detail_initial,
                "selectedTitle": selected_title_initial,
                "selectedDetail": selected_detail_initial,
            },
            {
                "step": "select_second_index",
                "ok": select_second_ok and "最初の履歴メモ。" in selected_detail_second,
                "selectedIndex": history.get_selected_index(),
                "selectedDetail": selected_detail_second,
            },
        ],
        "firstCardId": get_field(first_reading, "card_id"),
        "secondCardId": get_field(second_reading, "card_id"),
        "historyClassDoc": getattr(unreal.OnokoArcanaReadingHistoryViewModel, "__doc__", ""),
    }

    delete_ok = bool(unreal.OnokoArcanaReadingSaveLibrary.delete_readings_slot(SLOT_NAME, USER_INDEX))
    result["steps"].append({"step": "delete_test_slot", "ok": delete_ok})
    result["ok"] = all(step["ok"] for step in result["steps"])

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 2 reading history view model test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE2_READING_HISTORY_VIEW_MODEL_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
