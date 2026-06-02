import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase1HudReflectionSurfaceTestResult.json")


def has_text(value, needle):
    return needle in (value or "")


def main():
    hud_doc = getattr(unreal.OnokoArcanaTableHudWidget, "__doc__", "")
    controller_doc = getattr(unreal.OnokoArcanaPlayerController, "__doc__", "")
    game_mode_doc = getattr(unreal.OnokoArcanaGameMode, "__doc__", "")

    result = {
        "ok": False,
        "classes": {
            "OnokoArcanaTableHudWidget": {
                "hasClass": hasattr(unreal, "OnokoArcanaTableHudWidget"),
                "docChecks": {
                    "questionTextBox": has_text(hud_doc, "question_text_box"),
                    "drawButton": has_text(hud_doc, "draw_button"),
                    "revealGuideButton": has_text(hud_doc, "reveal_guide_button"),
                    "saveReadingButton": has_text(hud_doc, "save_reading_button"),
                    "refreshHistoryButton": has_text(hud_doc, "refresh_history_button"),
                    "spreadSelectorComboBox": has_text(hud_doc, "spread_selector_combo_box"),
                    "activeSpreadText": has_text(hud_doc, "active_spread_text"),
                    "spreadSlotsText": has_text(hud_doc, "spread_slots_text"),
                    "selectedSpreadSlotText": has_text(hud_doc, "selected_spread_slot_text"),
                    "pastSlotButton": has_text(hud_doc, "past_slot_button"),
                    "presentSlotButton": has_text(hud_doc, "present_slot_button"),
                    "futureSlotButton": has_text(hud_doc, "future_slot_button"),
                    "cardTitleText": has_text(hud_doc, "card_title_text"),
                    "historyCountText": has_text(hud_doc, "history_count_text"),
                    "historySelectedDetailText": has_text(hud_doc, "history_selected_detail_text"),
                    "tableController": has_text(hud_doc, "table_controller"),
                },
            },
            "OnokoArcanaPlayerController": {
                "hasClass": hasattr(unreal, "OnokoArcanaPlayerController"),
                "docChecks": {
                    "tableHudWidgetClass": has_text(controller_doc, "table_hud_widget_class"),
                    "tableController": has_text(controller_doc, "table_controller"),
                    "autoCreateHud": has_text(controller_doc, "auto_create_table_hud"),
                },
            },
            "OnokoArcanaGameMode": {
                "hasClass": hasattr(unreal, "OnokoArcanaGameMode"),
                "docChecks": {},
            },
        },
    }
    result["ok"] = all(
        class_result["hasClass"] and all(class_result["docChecks"].values())
        for class_result in result["classes"].values()
    )

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 1 HUD reflection surface test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE1_HUD_REFLECTION_SURFACE_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
