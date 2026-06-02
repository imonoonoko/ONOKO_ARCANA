import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase1OneCardViewModelTestResult.json")


def main():
    view_model = unreal.new_object(unreal.OnokoArcanaOneCardViewModel)
    result = {
        "ok": False,
        "classDoc": getattr(unreal.OnokoArcanaOneCardViewModel, "__doc__", ""),
        "tableControllerClassDoc": getattr(unreal.OnokoArcanaTableController, "__doc__", ""),
        "steps": [],
    }

    init_ok = bool(view_model.initialize())
    result["steps"].append(
        {
            "step": "initialize",
            "ok": init_ok,
            "lastError": view_model.last_error_message,
            "canDraw": view_model.can_draw(),
        }
    )

    start_ok = bool(view_model.start_reading("ViewModel smoke test", 12345, True))
    result["steps"].append(
        {
            "step": "start_reading",
            "ok": start_ok,
            "lastError": view_model.last_error_message,
            "canDraw": view_model.can_draw(),
            "hasCurrentDraw": view_model.has_current_draw(),
        }
    )

    draw_ok = bool(view_model.draw_one(True))
    title_after_draw = view_model.get_card_title()
    orientation_after_draw = view_model.get_orientation_label()
    keywords_after_draw = view_model.get_active_keywords_text()
    study_before_reveal = view_model.get_study_focus_text()
    result["steps"].append(
        {
            "step": "draw_one",
            "ok": draw_ok,
            "lastError": view_model.last_error_message,
            "hasCurrentDraw": view_model.has_current_draw(),
            "title": title_after_draw,
            "orientation": orientation_after_draw,
            "keywords": keywords_after_draw,
            "studyFocusBeforeGuideReveal": study_before_reveal,
        }
    )

    view_model.submit_user_interpretation("まず自分の解釈を書く。")
    result["steps"].append(
        {
            "step": "submit_user_interpretation",
            "ok": view_model.get_user_interpretation() != "",
            "userInterpretation": view_model.get_user_interpretation(),
        }
    )

    reveal_ok = bool(view_model.reveal_guide())
    study_after_reveal = view_model.get_study_focus_text()
    result["steps"].append(
        {
            "step": "reveal_guide",
            "ok": reveal_ok and view_model.is_guide_revealed() and study_after_reveal != "",
            "lastError": view_model.last_error_message,
            "guideRevealed": view_model.is_guide_revealed(),
            "studyFocusAfterGuideReveal": study_after_reveal,
        }
    )

    view_model.reset_reading()
    result["steps"].append(
        {
            "step": "reset_reading",
            "ok": not view_model.has_current_draw()
            and not view_model.is_guide_revealed()
            and view_model.get_user_interpretation() == "",
            "hasCurrentDraw": view_model.has_current_draw(),
            "guideRevealed": view_model.is_guide_revealed(),
            "userInterpretation": view_model.get_user_interpretation(),
        }
    )

    draw_step = next(step for step in result["steps"] if step["step"] == "draw_one")
    result["ok"] = (
        all(step["ok"] for step in result["steps"])
        and draw_step["title"] != ""
        and draw_step["orientation"] in ["正位置", "逆位置"]
        and draw_step["keywords"] != ""
        and draw_step["studyFocusBeforeGuideReveal"] == ""
    )

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 1 one-card view model test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE1_ONE_CARD_VIEW_MODEL_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
