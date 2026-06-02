import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase1OneCardSessionTestResult.json")


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
    elif isinstance(value, str):
        error = value
        draw = get_field(session, "current_draw")
    elif get_field(value, "card") is not None:
        draw = value
    else:
        draw = get_field(session, "current_draw")

    success = bool(draw is not None and get_field(draw, "success", False) and error == "")
    return success, draw, error


def main():
    session = unreal.new_object(unreal.OnokoArcanaOneCardSession)
    result = {
        "ok": False,
        "classDoc": getattr(unreal.OnokoArcanaOneCardSession, "__doc__", ""),
        "initializeDoc": getattr(session.initialize_major_arcana_v5, "__doc__", ""),
        "startDoc": getattr(session.start_new_reading, "__doc__", ""),
        "drawDoc": getattr(session.draw_one, "__doc__", ""),
        "revealGuideDoc": getattr(session.reveal_guide, "__doc__", ""),
        "steps": [],
    }

    init_ok, init_error = unpack_error(session.initialize_major_arcana_v5())
    result["steps"].append({"step": "initialize", "ok": init_ok, "error": init_error})

    start_ok, start_error = unpack_error(session.start_new_reading("Phase 1 commandlet smoke test", 12345, True))
    result["steps"].append(
        {
            "step": "start_new_reading",
            "ok": start_ok,
            "error": start_error,
            "question": session.question,
            "canDraw": session.can_draw(),
        }
    )

    draw_ok, draw_result, draw_error = unpack_draw(session.draw_one(True), session)
    card = get_field(draw_result, "card")
    result["steps"].append(
        {
            "step": "draw_one",
            "ok": draw_ok,
            "error": draw_error,
            "hasCurrentDraw": session.has_current_draw,
            "cardId": get_field(card, "id"),
            "orientation": str(get_field(draw_result, "orientation", "")),
            "activeKeywordCount": len(get_field(draw_result, "active_keywords", []) or []),
            "canRevealGuide": session.can_reveal_guide(),
        }
    )

    session.submit_user_interpretation("カードの第一印象を先に記録する。")
    result["steps"].append(
        {
            "step": "submit_user_interpretation",
            "ok": session.user_interpretation != "",
            "userInterpretationLength": len(session.user_interpretation),
        }
    )

    reveal_ok, reveal_error = unpack_error(session.reveal_guide())
    result["steps"].append(
        {
            "step": "reveal_guide",
            "ok": reveal_ok and session.guide_revealed,
            "error": reveal_error,
            "guideRevealed": session.guide_revealed,
        }
    )

    session.reset_reading()
    result["steps"].append(
        {
            "step": "reset_reading",
            "ok": not session.has_current_draw and not session.guide_revealed and session.user_interpretation == "",
            "hasCurrentDraw": session.has_current_draw,
            "guideRevealed": session.guide_revealed,
            "userInterpretationLength": len(session.user_interpretation),
        }
    )

    result["ok"] = all(item["ok"] for item in result["steps"])

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["ok"]:
        raise RuntimeError(f"Phase 1 one-card session test failed: {RESULT_PATH}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


try:
    main()
except Exception as exc:
    print("[ONOKO_ARCANA_PHASE1_ONE_CARD_SESSION_TEST_ERROR] " + str(exc), file=sys.stderr)
    raise
