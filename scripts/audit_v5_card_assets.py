import argparse
import json
from pathlib import Path

from PIL import Image


EXPECTED_SIZE = (1024, 1536)


def parse_args():
    parser = argparse.ArgumentParser(description="Audit V5 ONOKO ARCANA chroma-keyed card PNG assets.")
    parser.add_argument("--out", required=True)
    parser.add_argument("images", nargs="+")
    return parser.parse_args()


def border_alpha_zero(alpha):
    width, height = alpha.size
    pixels = alpha.load()
    for x in range(width):
        if pixels[x, 0] != 0 or pixels[x, height - 1] != 0:
            return False
    for y in range(height):
        if pixels[0, y] != 0 or pixels[width - 1, y] != 0:
            return False
    return True


def audit(path):
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    pixels = image.tobytes()
    visible_green = 0
    visible_strong_key = 0
    visible_pixels = 0
    for index in range(0, len(pixels), 4):
        r = pixels[index]
        g = pixels[index + 1]
        b = pixels[index + 2]
        a = pixels[index + 3]
        if a == 0:
            continue
        visible_pixels += 1
        if g > 180 and r < 80 and b < 80:
            visible_green += 1
        if g > 220 and r < 40 and b < 40:
            visible_strong_key += 1

    if bbox:
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
    else:
        width = height = 0

    size_ok = image.size == EXPECTED_SIZE
    bbox_plausible = bool(
        bbox
        and 650 <= width <= 900
        and 1250 <= height <= 1510
        and 40 <= bbox[0] <= 180
        and 20 <= bbox[1] <= 120
        and 850 <= bbox[2] <= 980
        and 1420 <= bbox[3] <= 1535
    )
    green_ok = visible_green == 0 and visible_strong_key == 0
    border_ok = border_alpha_zero(alpha)
    ok = size_ok and bbox_plausible and green_ok and border_ok

    return {
        "path": str(path),
        "size": list(image.size),
        "sizeOk": size_ok,
        "alphaBbox": list(bbox) if bbox else None,
        "alphaBboxSize": [width, height],
        "alphaBboxPlausible": bbox_plausible,
        "alphaExtrema": list(alpha.getextrema()),
        "alphaValueCount": len(set(alpha.tobytes())),
        "borderAlphaZero": border_ok,
        "visiblePixels": visible_pixels,
        "visibleGreenPixels": visible_green,
        "visibleStrongKeyPixels": visible_strong_key,
        "greenOk": green_ok,
        "ok": ok,
    }


def main():
    args = parse_args()
    results = [audit(Path(path)) for path in args.images]
    payload = {
        "ok": all(item["ok"] for item in results),
        "count": len(results),
        "expectedSize": list(EXPECTED_SIZE),
        "policy": "V5 accepts a taller, slender visible card silhouette. Bbox is checked for plausibility, not exact equality.",
        "results": results,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": payload["ok"], "count": payload["count"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
