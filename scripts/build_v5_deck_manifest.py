import json
from pathlib import Path


DATA = Path("data/major-arcana-cards.json")
QA = Path("assets/generated/card-production-v5-full/reports/v5-major-arcana-visual-qa.json")
IMPORT_RESULT = Path("Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V5_Full/v5-full-import-result.json")
OUT = Path("data/major-arcana-v5-deck.json")

RAW_ROOT = Path("../assets/generated/card-production-v5-full/raw")
ALPHA_ROOT = Path("../assets/generated/card-production-v5-full/alpha")


def load_imports():
    payload = json.loads(IMPORT_RESULT.read_text(encoding="utf-8"))
    if not payload.get("ok"):
        raise RuntimeError(f"Unreal import result is not ok: {IMPORT_RESULT}")
    return {item["id"]: item for item in payload["results"]}


def load_qa():
    payload = json.loads(QA.read_text(encoding="utf-8"))
    return {item["id"]: item for item in payload["items"]}


def main():
    cards = json.loads(DATA.read_text(encoding="utf-8"))
    imports = load_imports()
    qa = load_qa()

    back_import = imports["card-back"]
    back_qa = qa["card-back"]
    manifest = {
        "version": "v5-full-major-arcana-candidate-2026-06-01",
        "deckId": "onoko-arcana-major-v5",
        "scope": "Major Arcana 00-21 plus card back",
        "status": "candidate",
        "promotionPolicy": {
            "requiresAlphaAuditOk": True,
            "requiresVisualQaAdopted": True,
            "minorArcanaBlockedUntilMajorRuntimeStable": True,
        },
        "evidence": {
            "alphaAudit": "../assets/generated/card-production-v5-full/reports/v5-alpha-audit.json",
            "visualQa": "../assets/generated/card-production-v5-full/reports/v5-major-arcana-visual-qa.json",
            "contactSheet": "../assets/generated/card-production-v5-full/reports/v5-alpha-contact-sheet-major-00-21-back.png",
            "characterCropSheet": "../assets/generated/card-production-v5-full/reports/v5-character-crop-report-major-00-21.png",
            "ueImportResult": "../Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V5_Full/v5-full-import-result.json",
            "ueAlphaQaMapResult": "../Unreal/ONOKO_ARCANA/Saved/V5FullAlphaQAMapResult.json",
        },
        "back": {
            "id": "card-back",
            "rawImage": str(RAW_ROOT / "card-back-onoko-v5-source.png").replace("\\", "/"),
            "alphaImage": str(ALPHA_ROOT / "card-back-onoko-v5-alpha.png").replace("\\", "/"),
            "unrealTexture": back_import["assetPath"],
            "qaStatus": back_qa["qa"]["status"],
        },
        "cards": [],
    }

    for card in cards:
        card_id = f"major-{card['number']}-{card['slug']}"
        imported = imports[card_id]
        visual_qa = qa[card_id]
        manifest["cards"].append(
            {
                "id": card_id,
                "number": card["number"],
                "slug": card["slug"],
                "englishName": card["englishName"],
                "japaneseName": card["japaneseName"],
                "uprightKeywords": card["uprightKeywords"],
                "reversedKeywords": card["reversedKeywords"],
                "studyFocus": card["studyFocus"],
                "rawImage": str(RAW_ROOT / f"{card_id}-onoko-v5-source.png").replace("\\", "/"),
                "alphaImage": str(ALPHA_ROOT / f"{card_id}-onoko-v5-alpha.png").replace("\\", "/"),
                "unrealTexture": imported["assetPath"],
                "qaStatus": visual_qa["qa"]["status"],
            }
        )

    not_adopted = [
        item["id"]
        for item in [manifest["back"], *manifest["cards"]]
        if item["qaStatus"] != "Adopted"
    ]
    manifest["summary"] = {
        "cardCount": len(manifest["cards"]),
        "assetCountIncludingBack": len(manifest["cards"]) + 1,
        "notAdopted": not_adopted,
        "readyForPhase1DataImport": not not_adopted,
    }

    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
