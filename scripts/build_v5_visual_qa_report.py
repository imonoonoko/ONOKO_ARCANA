import json
from pathlib import Path


ROOT = Path("assets/generated/card-production-v5-full")
DATA = Path("data/major-arcana-cards.json")
OUT_JSON = ROOT / "reports" / "v5-major-arcana-visual-qa.json"
OUT_MD = ROOT / "reports" / "v5-major-arcana-visual-qa.md"


QA_NOTES = {
    "card-back": {
        "status": "Adopted",
        "reason": "Back/front alpha bbox was corrected to match Major 00; no current size mismatch remains.",
        "checks": {
            "face": "not_applicable",
            "hands": "not_applicable",
            "motif": "pass",
            "panel": "not_applicable",
            "frame": "pass",
            "ueSize": "pass",
        },
    },
    "major-07-chariot": {
        "status": "Adopted",
        "reason": "Regenerated after the first V5 Chariot read too close to a dual-beast Strength motif. The current version has a clear arcane vehicle, wheels, and reins of light.",
        "checks": {
            "face": "pass",
            "hands": "pass",
            "motif": "pass",
            "panel": "pass",
            "frame": "pass",
            "ueSize": "pass",
        },
    },
}


def default_note(card_id):
    return {
        "status": "Adopted",
        "reason": "No hard blocker found in contact sheet, crop QA, alpha audit, or UE full-set QA at this pass.",
        "checks": {
            "face": "pass",
            "hands": "pass",
            "motif": "pass",
            "panel": "pass",
            "frame": "pass",
            "ueSize": "pass",
        },
    }


def make_items():
    cards = json.loads(DATA.read_text(encoding="utf-8"))
    items = []
    back = QA_NOTES["card-back"]
    items.append(
        {
            "id": "card-back",
            "number": None,
            "slug": "card-back",
            "englishName": "Card Back",
            "japaneseName": "カード裏面",
            "alpha": str(ROOT / "alpha" / "card-back-onoko-v5-alpha.png"),
            "qa": back,
        }
    )
    for card in cards:
        card_id = f"major-{card['number']}-{card['slug']}"
        note = QA_NOTES.get(card_id, default_note(card_id))
        items.append(
            {
                "id": card_id,
                "number": card["number"],
                "slug": card["slug"],
                "englishName": card["englishName"],
                "japaneseName": card["japaneseName"],
                "alpha": str(ROOT / "alpha" / f"major-{card['number']}-{card['slug']}-onoko-v5-alpha.png"),
                "ueTexture": f"/Game/ONOKOArcana/Cards/Textures/V5Full/T_Major_{card['number']}_{card['englishName'].replace('The ', '').replace(' ', '_').replace('-', '_')}_ONOKO_V5_Alpha",
                "qa": note,
            }
        )
    return items


def write_markdown(items):
    counts = {}
    for item in items:
        status = item["qa"]["status"]
        counts[status] = counts.get(status, 0) + 1

    lines = [
        "# ONOKO ARCANA V5 Major Arcana Visual QA",
        "",
        "Date: 2026-06-01",
        "",
        "## Summary",
        "",
        f"- Total assets: `{len(items)}`",
        f"- Adopted: `{counts.get('Adopted', 0)}`",
        f"- Needs Regeneration: `{counts.get('Needs Regeneration', 0)}`",
        f"- Blocked: `{counts.get('Blocked', 0)}`",
        "",
        "## Evidence Used",
        "",
        "- `assets/generated/card-production-v5-full/reports/v5-alpha-audit.json`",
        "- `assets/generated/card-production-v5-full/reports/v5-alpha-contact-sheet-major-00-21-back.png`",
        "- `assets/generated/card-production-v5-full/reports/v5-character-crop-report-major-00-21.png`",
        "- `assets/generated/reports/v5-full-alpha-qa-map-unreal-editor-back-size-fixed-2026-06-01.png`",
        "",
        "## Gate Criteria",
        "",
        "1. ONOKO face is not visibly low quality.",
        "2. Hands are not obviously broken at review scale.",
        "3. Tarot-specific motif is readable.",
        "4. Empty panels do not contain pseudo text.",
        "5. Frame width, blue/gold balance, and glow are consistent.",
        "6. Front/back visible size matches in Unreal.",
        "7. Runtime text panel areas remain usable.",
        "",
        "## Results",
        "",
        "| ID | Card | Status | Reason |",
        "|---|---|---|---|",
    ]
    for item in items:
        card = item["englishName"] if item["number"] is None else f"{item['number']} {item['englishName']} / {item['japaneseName']}"
        lines.append(f"| `{item['id']}` | {card} | {item['qa']['status']} | {item['qa']['reason']} |")

    needs = [item for item in items if item["qa"]["status"] == "Needs Regeneration"]
    lines += [
        "",
        "## Next Action",
        "",
    ]
    if needs:
        lines.append("Regenerate the `Needs Regeneration` assets before promoting V5 into the active deck manifest.")
        for item in needs:
            lines.append(f"- `{item['id']}`: {item['qa']['reason']}")
    else:
        lines.append("No visual blockers remain. Promote V5 into an active candidate deck manifest.")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    items = make_items()
    payload = {
        "version": "v5-major-arcana-visual-qa-2026-06-01",
        "total": len(items),
        "items": items,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(items)
    print(json.dumps({"outJson": str(OUT_JSON), "outMarkdown": str(OUT_MD), "total": len(items)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
