import json
from pathlib import Path


ROOT = Path("assets/generated/card-production-v5-full")
DATA = Path("data/major-arcana-cards.json")

CARD_MOTIFS = {
    "fool": "first step, luminous path into the night city, small cat guide, open sky, beginning of observation",
    "magician": "one hand raised and one hand reaching toward a glowing magic circle table, wand, cup, sword, pentacle-like disc",
    "high-priestess": "moonlit archive, glowing blue book, veil, twin columns, quiet intuition and hidden records",
    "empress": "lush cyber botanical garden, blue luminous flowers, creative abundance, gentle sovereign presence",
    "emperor": "black-gold command throne, architectural grid, protective boundary, disciplined structure",
    "hierophant": "ritual classroom, glowing doctrine tablets, mentor-like guidance, sacred learning hall",
    "lovers": "two luminous paths crossing, twin silhouettes or mirrored panels, values choice, harmonious bond",
    "chariot": "sleek blue-black arcane vehicle or armored platform, reins of light, controlled forward motion",
    "strength": "calmly taming a luminous mechanical lion, soft courage, restraint over force",
    "hermit": "solitary lantern on a high cyber tower, inner light, quiet search, distant stars",
    "wheel-of-fortune": "large rotating astral wheel, clockwork rings, changing cycles, blue-gold fate mechanism",
    "justice": "balanced scales, luminous sword, clear judgment grid, symmetry and accountability",
    "hanged-man": "voluntary suspension in a glowing observation harness, inverted perspective, serene pause",
    "death": "black-blue transformation gate, fading old mask, white flower, ending and rebirth",
    "temperance": "mixing two streams of blue light between vessels, careful balance, healing integration",
    "devil": "shadow chains made of neon, temptation screen, self-made binding, dark glamour without horror",
    "tower": "black tower struck by blue lightning, shattered false structure, dramatic reset",
    "star": "starlight pool, pouring luminous water, hope and recovery, clear night sky",
    "moon": "large crescent moon, reflective water, uncertainty, dreamlike path, two watcher towers",
    "sun": "brilliant blue-white sun disc, joyful clarity, open courtyard, warm victory glow",
    "judgement": "resonant blue trumpet or signal beam, awakening figures as light silhouettes, response to calling",
    "world": "completed celestial ring, integrated city and stars, full cycle, elegant cosmic completion",
}


STYLE = (
    "ONOKO ARCANA premium tarot card, full card object, black and deep navy gothic-cyber frame, "
    "antique gold trim, electric blue star circuitry, subtle cat emblem motif, empty parchment top nameplate "
    "and empty parchment bottom description plate, no readable text."
)


BASE_CONSTRAINTS = (
    "Generate a vertical 2:3 portrait card at 1024x1536 composition. The card itself should have a slender tarot-card "
    "silhouette and fill most of the image, centered, with clean outer padding. The central illustration must be "
    "integrated inside the artwork window and must not overlap or hide under the side rails, top nameplate, bottom "
    "plate, corner ornaments, or arrow ornaments. Background outside the card only must be perfectly flat solid "
    "#00ff00 chroma-key green for removal, with no shadows, gradients, texture, reflections, or floor plane. Do not "
    "use #00ff00 anywhere on the card. No text, no letters, no numbers, no watermark, no logo, no cropped card edges, "
    "no horizontal distortion."
)


def prompt_for(card):
    number = card["number"]
    slug = card["slug"]
    return {
        "id": f"major-{number}-{slug}",
        "number": number,
        "slug": slug,
        "englishName": card["englishName"],
        "japaneseName": card["japaneseName"],
        "raw": f"raw/major-{number}-{slug}-onoko-v5-source.png",
        "alpha": f"alpha/major-{number}-{slug}-onoko-v5-alpha.png",
        "staging": f"Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V5_Full/major-{number}-{slug}-onoko-v5-alpha.png",
        "prompt": "\n".join(
            [
                "Use case: stylized-concept",
                "Asset type: ONOKO ARCANA Unreal Engine tarot card texture",
                f"Primary request: Create card {number}, {card['englishName']}, as a new complete ONOKO tarot card front.",
                f"Tarot motif: {CARD_MOTIFS[slug]}.",
                "Subject: ONOKO-style anime girl, black-blue hair, luminous blue eyes, black futuristic outfit with white and electric-blue accents, calm observational expression. Face and hands must be sharp and high quality.",
                f"Style/medium: {STYLE}",
                "Color palette: black, deep navy, electric blue, antique gold, parchment ivory panels.",
                f"Constraints: {BASE_CONSTRAINTS}",
                "Avoid: pseudo text, readable glyphs, low-resolution face, broken fingers, old card frame fragments, green spill, cast shadow, contact shadow.",
            ]
        ),
    }


def main():
    cards = json.loads(DATA.read_text(encoding="utf-8"))
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "raw").mkdir(exist_ok=True)
    (ROOT / "alpha").mkdir(exist_ok=True)
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "prompts").mkdir(exist_ok=True)

    items = [prompt_for(card) for card in cards]
    back = {
        "id": "card-back",
        "number": None,
        "slug": "card-back",
        "englishName": "Card Back",
        "japaneseName": "カード裏面",
        "raw": "raw/card-back-onoko-v5-source.png",
        "alpha": "alpha/card-back-onoko-v5-alpha.png",
        "staging": "Unreal/ONOKO_ARCANA/ImportStaging/MajorArcana_V5_Full/card-back-onoko-v5-alpha.png",
        "prompt": "\n".join(
            [
                "Use case: stylized-concept",
                "Asset type: ONOKO ARCANA Unreal Engine tarot card back texture",
                "Primary request: Create a new complete ONOKO tarot card back design, matching the V5 front card silhouette.",
                "Subject: symmetrical card back with no character, central blue crystal, concentric astral rings, cat emblem motif at top and bottom, black and deep navy gothic-cyber frame, antique gold trim, electric blue star circuitry.",
                "Composition/framing: vertical 2:3 portrait, slender tarot-card silhouette, centered, clean outer padding, same premium ONOKO ARCANA style as the front cards.",
                f"Constraints: {BASE_CONSTRAINTS}",
                "Avoid: text, letters, numbers, watermark, logo, face, hands, green on the card, cast shadow, contact shadow.",
            ]
        ),
    }
    payload = {
        "version": "v5-full-major-arcana",
        "scope": "major arcana 22 fronts plus one card back",
        "root": str(ROOT),
        "items": items,
        "back": back,
    }
    (ROOT / "prompts" / "v5-major-arcana-generation-manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for item in items + [back]:
        (ROOT / "prompts" / f"{item['id']}.txt").write_text(item["prompt"], encoding="utf-8")
    print(ROOT / "prompts" / "v5-major-arcana-generation-manifest.json")


if __name__ == "__main__":
    main()
