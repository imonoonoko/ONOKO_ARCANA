import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase3SpreadRegistryTestResult.json")
SLOT_NAME = "ONOKO_ARCANA_Phase3SpreadMetadataSmokeTest"
USER_INDEX = 0


def get_field(obj, name, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        try:
            return obj.get_editor_property(name)
        except Exception:
            return default


def safe_get_default_object(cls):
    try:
        return unreal.get_default_object(cls)
    except Exception as exc:
        return {"error": str(exc)}


def spread_id_to_string(value):
    return str(value).strip()


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


def find_spread_in_list(spreads, spread_id):
    for spread in spreads:
        if spread_id_to_string(get_field(spread, "spread_id", "")) == spread_id:
            return spread
    return None


def main():
    registry = unreal.new_object(unreal.OnokoArcanaSpreadRegistry)
    registry.initialize_built_in_spreads()
    spreads = list(get_field(registry, "spreads", []) or [])
    spread_ids = [spread_id_to_string(get_field(spread, "spread_id", "")) for spread in spreads]

    celtic_spread = find_spread_in_list(spreads, "celtic_cross")
    celtic_slots = list(get_field(celtic_spread, "slots", []) or []) if celtic_spread else []

    three_spread = find_spread_in_list(spreads, "three_card_past_present_future")
    three_slots = list(get_field(three_spread, "slots", []) or []) if three_spread else []
    three_orders = [int(get_field(slot, "reveal_order", 0)) for slot in three_slots]

    controller_cdo = safe_get_default_object(unreal.OnokoArcanaTableController)
    controller_steps = []
    controller_save_steps = []
    if isinstance(controller_cdo, dict):
        controller_steps.append({"step": "get_default_object", "ok": False, "error": controller_cdo["error"]})
        controller_save_steps.append({"step": "get_default_object", "ok": False, "error": controller_cdo["error"]})
    else:
        init_ok = bool(controller_cdo.initialize_spread_registry())
        controller_steps.append(
            {
                "step": "initialize_spread_registry",
                "ok": init_ok,
                "activeSpreadId": spread_id_to_string(get_field(controller_cdo, "active_spread_id", "")),
                "error": get_field(controller_cdo, "last_error_message", ""),
            }
        )
        select_ok = bool(controller_cdo.select_spread("three_card_past_present_future"))
        controller_steps.append(
            {
                "step": "select_three_card",
                "ok": select_ok,
                "activeSpreadId": spread_id_to_string(get_field(controller_cdo, "active_spread_id", "")),
                "activeSpreadText": controller_cdo.get_active_spread_display_text(),
                "slotText": controller_cdo.get_active_spread_slot_list_text(),
                "error": get_field(controller_cdo, "last_error_message", ""),
            }
        )
        invalid_ok = bool(controller_cdo.select_spread("not_a_spread"))
        controller_steps.append(
            {
                "step": "reject_invalid_spread",
                "ok": invalid_ok is False and "Unknown spread id" in str(get_field(controller_cdo, "last_error_message", "")),
                "activeSpreadId": spread_id_to_string(get_field(controller_cdo, "active_spread_id", "")),
                "error": get_field(controller_cdo, "last_error_message", ""),
            }
        )
        controller_cdo.select_spread("one_card")

        unreal.OnokoArcanaReadingSaveLibrary.delete_readings_slot(SLOT_NAME, USER_INDEX)
        try:
            controller_cdo.set_editor_property("save_slot_name", SLOT_NAME)
            controller_cdo.set_editor_property("save_user_index", USER_INDEX)
            controller_cdo.reset_table()
            controller_cdo.select_spread("one_card")

            start_ok = bool(controller_cdo.start_reading("Phase 3 spread metadata save test"))
            draw_return_ok = bool(controller_cdo.draw_card(False))
            draw_state_ok = draw_return_ok or bool(controller_cdo.has_current_draw())
            controller_cdo.submit_user_interpretation("Spread metadata should be saved with this one-card reading.")
            guide_ok = bool(controller_cdo.reveal_guide())
            save_ok = bool(controller_cdo.save_current_reading())
            controller_save_steps.extend(
                [
                    {"step": "start_reading", "ok": start_ok, "error": get_field(controller_cdo, "last_error_message", "")},
                    {
                        "step": "draw_card_session_state",
                        "ok": draw_state_ok,
                        "drawReturn": draw_return_ok,
                        "hasCurrentDraw": bool(controller_cdo.has_current_draw()),
                        "note": "CDO test has no ReadingCardActor, so DrawCard may return false after creating session draw state.",
                        "error": get_field(controller_cdo, "last_error_message", ""),
                    },
                    {"step": "reveal_guide", "ok": guide_ok, "error": get_field(controller_cdo, "last_error_message", "")},
                    {"step": "save_current_reading", "ok": save_ok, "error": get_field(controller_cdo, "last_error_message", "")},
                ]
            )

            load_ok, save_game, load_error = unpack_save_game(
                unreal.OnokoArcanaReadingSaveLibrary.load_readings_from_slot(SLOT_NAME, USER_INDEX)
            )
            readings = list(get_field(save_game, "readings", []) or [])
            saved_reading = readings[0] if readings else None
            metadata_ok = (
                load_ok
                and len(readings) == 1
                and get_field(saved_reading, "spread_id", "") == "one_card"
                and get_field(saved_reading, "spread_display_name", "") == "一枚引き"
                and int(get_field(saved_reading, "card_count", 0)) == 1
                and get_field(saved_reading, "position_key", "") == "present"
                and get_field(saved_reading, "position_label", "") == "一枚引き"
            )
            controller_save_steps.append(
                {
                    "step": "load_saved_spread_metadata",
                    "ok": metadata_ok,
                    "error": load_error,
                    "readingCount": len(readings),
                    "spreadId": get_field(saved_reading, "spread_id", ""),
                    "spreadDisplayName": get_field(saved_reading, "spread_display_name", ""),
                    "cardCount": get_field(saved_reading, "card_count", 0),
                    "positionKey": get_field(saved_reading, "position_key", ""),
                    "positionLabel": get_field(saved_reading, "position_label", ""),
                }
            )
        finally:
            delete_ok = bool(unreal.OnokoArcanaReadingSaveLibrary.delete_readings_slot(SLOT_NAME, USER_INDEX))
            controller_save_steps.append({"step": "delete_test_slot", "ok": delete_ok})
            controller_cdo.reset_table()

    checks = {
        "hasRegistryClass": hasattr(unreal, "OnokoArcanaSpreadRegistry"),
        "spreadCountAtLeastSix": len(spreads) >= 6,
        "defaultSpreadIsOneCard": spread_id_to_string(registry.get_default_spread_id()) == "one_card",
        "hasOneCard": "one_card" in spread_ids,
        "hasThreeCard": "three_card_past_present_future" in spread_ids,
        "celticCrossHasTenSlots": celtic_spread is not None and len(celtic_slots) == 10,
        "threeCardRevealOrder": three_spread is not None and three_orders == [1, 2, 3],
        "controllerStepsOk": all(step["ok"] for step in controller_steps),
        "controllerSaveSpreadMetadataOk": all(step["ok"] for step in controller_save_steps),
    }

    result = {
        "ok": all(checks.values()),
        "checks": checks,
        "spreadIds": spread_ids,
        "celticSlotCount": len(celtic_slots),
        "threeRevealOrders": three_orders,
        "controllerSteps": controller_steps,
        "controllerSaveSteps": controller_save_steps,
        "registryDoc": getattr(unreal.OnokoArcanaSpreadRegistry, "__doc__", ""),
        "tableControllerDoc": getattr(unreal.OnokoArcanaTableController, "__doc__", ""),
    }

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 3 spread registry test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE3_SPREAD_REGISTRY_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
