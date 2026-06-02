import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, "..", ".."))
DECK_MANIFEST_PATH = os.path.join(REPO_ROOT, "data", "major-arcana-v5-deck.json")
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "V5DeckManifestValidationResult.json")

EXPECTED_TEXTURE_SIZE = (1024, 1536)
EXPECTED_CARD_COUNT = 22


def log(message):
    unreal.log("[ONOKO_ARCANA_V5_DECK_VALIDATE] " + message)
    print("[ONOKO_ARCANA_V5_DECK_VALIDATE] " + message)


def load_texture(path):
    texture = unreal.load_asset(path)
    if texture is not None:
        return texture
    if "." in path:
        return unreal.load_asset(path.split(".", 1)[0])
    return None


def texture_size(texture):
    return int(texture.blueprint_get_size_x()), int(texture.blueprint_get_size_y())


def validate_card(card, index, seen_ids):
    required = [
        "id",
        "number",
        "slug",
        "englishName",
        "japaneseName",
        "uprightKeywords",
        "reversedKeywords",
        "studyFocus",
        "unrealTexture",
        "qaStatus",
    ]
    errors = []
    for key in required:
        if key not in card:
            errors.append(f"missing field: {key}")

    card_id = card.get("id", f"index-{index}")
    if card_id in seen_ids:
        errors.append("duplicate id")
    seen_ids.add(card_id)

    if card.get("qaStatus") != "Adopted":
        errors.append(f"qaStatus is not Adopted: {card.get('qaStatus')}")

    if not isinstance(card.get("uprightKeywords"), list) or len(card.get("uprightKeywords", [])) == 0:
        errors.append("uprightKeywords must be a non-empty list")
    if not isinstance(card.get("reversedKeywords"), list) or len(card.get("reversedKeywords", [])) == 0:
        errors.append("reversedKeywords must be a non-empty list")

    texture_path = card.get("unrealTexture")
    texture = None
    size = None
    if texture_path:
        texture = load_texture(texture_path)
        if texture is None:
            errors.append(f"texture not loadable: {texture_path}")
        else:
            size = texture_size(texture)
            if size != EXPECTED_TEXTURE_SIZE:
                errors.append(f"texture size mismatch: {size[0]}x{size[1]}")

    return {
        "id": card_id,
        "number": card.get("number"),
        "englishName": card.get("englishName"),
        "japaneseName": card.get("japaneseName"),
        "texture": texture_path,
        "textureLoaded": texture is not None,
        "textureSize": list(size) if size else None,
        "qaStatus": card.get("qaStatus"),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def validate_back(back):
    errors = []
    for key in ("id", "unrealTexture", "qaStatus"):
        if key not in back:
            errors.append(f"missing field: {key}")
    if back.get("qaStatus") != "Adopted":
        errors.append(f"qaStatus is not Adopted: {back.get('qaStatus')}")

    texture_path = back.get("unrealTexture")
    texture = load_texture(texture_path) if texture_path else None
    size = None
    if texture is None:
        errors.append(f"texture not loadable: {texture_path}")
    else:
        size = texture_size(texture)
        if size != EXPECTED_TEXTURE_SIZE:
            errors.append(f"texture size mismatch: {size[0]}x{size[1]}")

    return {
        "id": back.get("id"),
        "texture": texture_path,
        "textureLoaded": texture is not None,
        "textureSize": list(size) if size else None,
        "qaStatus": back.get("qaStatus"),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def main():
    if not os.path.exists(DECK_MANIFEST_PATH):
        raise RuntimeError(f"Missing deck manifest: {DECK_MANIFEST_PATH}")

    with open(DECK_MANIFEST_PATH, "r", encoding="utf-8") as fp:
        manifest = json.load(fp)

    cards = manifest.get("cards", [])
    back = manifest.get("back", {})
    global_errors = []

    if manifest.get("deckId") != "onoko-arcana-major-v5":
        global_errors.append(f"unexpected deckId: {manifest.get('deckId')}")
    if manifest.get("status") != "candidate":
        global_errors.append(f"unexpected status: {manifest.get('status')}")
    if len(cards) != EXPECTED_CARD_COUNT:
        global_errors.append(f"expected {EXPECTED_CARD_COUNT} cards, got {len(cards)}")

    policy = manifest.get("promotionPolicy", {})
    if not policy.get("minorArcanaBlockedUntilMajorRuntimeStable"):
        global_errors.append("minorArcanaBlockedUntilMajorRuntimeStable must stay true")

    seen_ids = set()
    back_result = validate_back(back)
    card_results = [validate_card(card, index, seen_ids) for index, card in enumerate(cards)]

    bad = []
    if not back_result["ok"]:
        bad.append(back_result)
    bad.extend([item for item in card_results if not item["ok"]])

    payload = {
        "ok": len(global_errors) == 0 and len(bad) == 0,
        "deckManifest": DECK_MANIFEST_PATH,
        "deckId": manifest.get("deckId"),
        "version": manifest.get("version"),
        "status": manifest.get("status"),
        "expectedTextureSize": list(EXPECTED_TEXTURE_SIZE),
        "cardCount": len(cards),
        "assetCountIncludingBack": len(cards) + 1,
        "globalErrors": global_errors,
        "back": back_result,
        "cards": card_results,
        "badCount": len(bad),
        "bad": bad,
        "phase1DataBridge": {
            "sourceOfTruth": "data/major-arcana-v5-deck.json",
            "readyForOneCardSlice": len(global_errors) == 0 and len(bad) == 0,
            "dataAssetDeferred": "Use JSON until the one-card runtime data shape stabilizes.",
        },
    }

    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)

    if not payload["ok"]:
        raise RuntimeError(f"V5 deck manifest validation failed: {RESULT_PATH}")
    log(f"Validated V5 deck manifest: {len(cards)} cards plus back")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_V5_DECK_VALIDATE] " + str(exc))
    print("[ONOKO_ARCANA_V5_DECK_VALIDATE_ERROR] " + str(exc), file=sys.stderr)
    raise
