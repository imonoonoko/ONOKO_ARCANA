import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase4ThreeCardSpreadSessionTestResult.json")
SLOT_NAME = "ONOKO_ARCANA_Phase4ThreeCardSpreadSmokeTest"
USER_INDEX = 0


def get_field(obj, name, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        try:
            return obj.get_editor_property(name)
        except Exception:
            return default


def get_any_field(obj, names, default=None):
    for name in names:
        value = get_field(obj, name, None)
        if value is not None:
            return value
    return default


def to_string(value):
    return str(value).strip()


def unpack_error(value):
    if value is None:
        return True, ""
    if isinstance(value, bool):
        return value, ""
    if isinstance(value, str):
        return value == "", value
    if isinstance(value, tuple):
        result = True
        error = ""
        for item in value:
            if isinstance(item, bool):
                result = item
            elif isinstance(item, str):
                error = item
        return result and error == "", error
    return bool(value), str(value)


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


def find_spread(spread_id):
    registry = unreal.new_object(unreal.OnokoArcanaSpreadRegistry)
    registry.initialize_built_in_spreads()
    for spread in list(get_field(registry, "spreads", []) or []):
        if to_string(get_field(spread, "spread_id", "")) == spread_id:
            return spread
    return None


def card_state_summary(state):
    draw = get_field(state, "draw")
    card = get_field(draw, "card") if draw else None
    return {
        "positionKey": to_string(get_field(state, "position_key", "")),
        "positionLabel": get_field(state, "position_label", ""),
        "revealOrder": int(get_field(state, "reveal_order", 0)),
        "hasDraw": bool(get_any_field(state, ["has_draw", "b_has_draw"], False)),
        "revealed": bool(get_any_field(state, ["revealed", "b_revealed"], False)),
        "selected": bool(get_any_field(state, ["selected", "b_selected"], False)),
        "guideRevealed": bool(get_any_field(state, ["guide_revealed", "b_guide_revealed"], False)),
        "cardId": get_field(card, "id", ""),
        "cardNumber": get_field(card, "number", ""),
    }


def session_states(session):
    return [card_state_summary(state) for state in list(get_field(session, "card_states", []) or [])]


def main():
    unreal.OnokoArcanaReadingSaveLibrary.delete_readings_slot(SLOT_NAME, USER_INDEX)
    spread = find_spread("three_card_past_present_future")
    session = unreal.new_object(unreal.OnokoArcanaSpreadReadingSession)

    result = {
        "ok": False,
        "slotName": SLOT_NAME,
        "steps": [],
        "spreadFound": spread is not None,
    }

    if spread is None:
        result["steps"].append({"step": "find_three_card_spread", "ok": False})
    else:
        result["steps"].append({"step": "find_three_card_spread", "ok": True, "slotCount": len(list(get_field(spread, "slots", []) or []))})

        init_ok, init_error = unpack_error(session.initialize_major_arcana_v5())
        result["steps"].append({"step": "initialize", "ok": init_ok, "error": init_error})

        start_ok, start_error = unpack_error(session.start_new_reading("Phase 4 three-card spread test", spread, 4242, True))
        result["steps"].append(
            {
                "step": "start_three_card_reading",
                "ok": start_ok and int(session.get_card_count()) == 3 and to_string(get_field(session, "selected_position_key", "")) == "present",
                "error": start_error,
                "cardCount": int(session.get_card_count()),
                "selectedPositionKey": to_string(get_field(session, "selected_position_key", "")),
                "states": session_states(session),
            }
        )

        draw_ok, draw_error = unpack_error(session.draw_spread(True))
        states_after_draw = session_states(session)
        drawn_card_ids = [state["cardId"] for state in states_after_draw]
        all_face_down = all(state["hasDraw"] and not state["revealed"] for state in states_after_draw)
        unique_cards = len(drawn_card_ids) == len(set(drawn_card_ids))
        result["steps"].append(
            {
                "step": "draw_spread",
                "ok": draw_ok and len(states_after_draw) == 3 and unique_cards and all_face_down,
                "error": draw_error,
                "drawnCardIds": drawn_card_ids,
                "uniqueCards": unique_cards,
                "allFaceDown": all_face_down,
                "states": states_after_draw,
            }
        )

        can_reveal_guide_before = bool(session.can_reveal_selected_guide())
        _, guide_before_error = unpack_error(session.reveal_selected_guide())
        selected_before_reveal = next((state for state in session_states(session) if state["selected"]), {})
        result["steps"].append(
            {
                "step": "guide_locked_before_reveal",
                "ok": not can_reveal_guide_before and selected_before_reveal.get("guideRevealed") is False,
                "error": guide_before_error,
                "attemptedGuideReveal": True,
                "canRevealBefore": can_reveal_guide_before,
                "selectedState": selected_before_reveal,
            }
        )

        reveal_sequence = []
        for expected_position in ["past", "present", "future"]:
            reveal_ok, reveal_error = unpack_error(session.reveal_next())
            selected_position = to_string(get_field(session, "selected_position_key", ""))
            reveal_sequence.append(selected_position)
            result["steps"].append(
                {
                    "step": f"reveal_next_{expected_position}",
                    "ok": reveal_ok and selected_position == expected_position,
                    "error": reveal_error,
                    "selectedPositionKey": selected_position,
                    "revealedCount": int(session.get_revealed_count()),
                    "states": session_states(session),
                }
            )

        note_ok, note_error = unpack_error(session.submit_selected_slot_interpretation("Future slot interpretation from commandlet."))
        guide_after_ok, guide_after_error = unpack_error(session.reveal_selected_guide())
        selected_state = next((state for state in session_states(session) if state["selected"]), {})
        result["steps"].append(
            {
                "step": "selected_note_and_guide",
                "ok": note_ok and guide_after_ok and selected_state.get("guideRevealed") is True,
                "noteError": note_error,
                "guideError": guide_after_error,
                "selectedState": selected_state,
            }
        )

        session.submit_summary_note("Three-card spread summary note.")
        make_ok, reading, make_error = unpack_saved_reading(
            unreal.OnokoArcanaReadingSaveLibrary.make_saved_reading_from_spread_session(session)
        )
        saved_card_states = list(get_field(reading, "card_states", []) or []) if reading else []
        result["steps"].append(
            {
                "step": "make_saved_spread_reading",
                "ok": make_ok
                and get_field(reading, "spread_id", "") == "three_card_past_present_future"
                and int(get_field(reading, "card_count", 0)) == 3
                and len(saved_card_states) == 3,
                "error": make_error,
                "spreadId": get_field(reading, "spread_id", ""),
                "cardCount": get_field(reading, "card_count", 0),
                "savedCardStateCount": len(saved_card_states),
            }
        )

        save_ok, save_error = unpack_error(
            unreal.OnokoArcanaReadingSaveLibrary.save_reading_to_slot(reading, SLOT_NAME, USER_INDEX)
        )
        result["steps"].append({"step": "save_spread_reading", "ok": save_ok, "error": save_error})

        load_ok, save_game, load_error = unpack_save_game(
            unreal.OnokoArcanaReadingSaveLibrary.load_readings_from_slot(SLOT_NAME, USER_INDEX)
        )
        readings = list(get_field(save_game, "readings", []) or [])
        loaded = readings[0] if readings else None
        loaded_states = list(get_field(loaded, "card_states", []) or []) if loaded else []
        result["steps"].append(
            {
                "step": "load_saved_spread_reading",
                "ok": load_ok
                and len(readings) == 1
                and get_field(loaded, "spread_id", "") == "three_card_past_present_future"
                and int(get_field(loaded, "card_count", 0)) == 3
                and len(loaded_states) == 3,
                "error": load_error,
                "readingCount": len(readings),
                "spreadId": get_field(loaded, "spread_id", ""),
                "cardCount": get_field(loaded, "card_count", 0),
                "loadedCardStateCount": len(loaded_states),
            }
        )

        view_model = unreal.new_object(unreal.OnokoArcanaSpreadReadingViewModel)
        vm_init_ok, vm_init_error = unpack_error(view_model.initialize())
        vm_start_ok, vm_start_error = unpack_error(view_model.start_reading("ViewModel three-card test", spread, 5150, True))
        vm_draw_ok, vm_draw_error = unpack_error(view_model.draw_spread(True))
        vm_reveal_ok, vm_reveal_error = unpack_error(view_model.reveal_next())
        vm_note_ok, vm_note_error = unpack_error(view_model.submit_selected_slot_interpretation("ViewModel note."))
        vm_guide_ok, vm_guide_error = unpack_error(view_model.reveal_selected_guide())
        result["steps"].append(
            {
                "step": "spread_view_model_surface",
                "ok": vm_init_ok
                and vm_start_ok
                and vm_draw_ok
                and vm_reveal_ok
                and vm_note_ok
                and vm_guide_ok
                and view_model.get_selected_card_title() != ""
                and view_model.get_selected_guide_text() != "",
                "errors": [vm_init_error, vm_start_error, vm_draw_error, vm_reveal_error, vm_note_error, vm_guide_error],
                "progressText": view_model.get_progress_text(),
                "selectedPosition": view_model.get_selected_position_label(),
                "selectedTitle": view_model.get_selected_card_title(),
                "selectedGuideText": view_model.get_selected_guide_text(),
            }
        )

        session.reset_reading()
        result["steps"].append(
            {
                "step": "reset_session",
                "ok": int(session.get_card_count()) == 0 and not bool(get_any_field(session, ["has_active_reading", "b_has_active_reading"], False)),
                "cardCount": int(session.get_card_count()),
                "hasActiveReading": bool(get_any_field(session, ["has_active_reading", "b_has_active_reading"], False)),
            }
        )

        delete_ok = bool(unreal.OnokoArcanaReadingSaveLibrary.delete_readings_slot(SLOT_NAME, USER_INDEX))
        result["steps"].append({"step": "delete_test_slot", "ok": delete_ok})

    result["ok"] = all(step["ok"] for step in result["steps"])

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 4 three-card spread session test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE4_THREE_CARD_SPREAD_SESSION_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
