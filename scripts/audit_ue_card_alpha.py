import argparse
import json
import warnings
from pathlib import Path

from PIL import Image


warnings.filterwarnings("ignore", category=DeprecationWarning)

EXPECTED_SIZE = (1024, 1536)
EXPECTED_BBOX = (54, 32, 970, 1514)


def parse_bbox(value):
    parts = [int(part.strip()) for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox must be x0,y0,x1,y1")
    return tuple(parts)


def audit(path, expected_bbox):
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    alpha_values = set(alpha.getdata())
    visible_magenta = 0
    visible_key_like = 0
    for r, g, b, a in image.getdata():
        if a and r > 120 and b > 120 and g < 80:
            visible_magenta += 1
        if a and (r > 220 and b > 220 and g < 120):
            visible_key_like += 1
    bbox = alpha.getbbox()
    size_ok = image.size == EXPECTED_SIZE
    bbox_ok = tuple(bbox) == expected_bbox if bbox else False
    alpha_binary = alpha_values <= {0, 255}
    key_clean = visible_magenta == 0 and visible_key_like == 0
    return {
        "path": str(path),
        "size": list(image.size),
        "sizeOk": size_ok,
        "alphaBbox": list(bbox) if bbox else None,
        "alphaBboxOk": bbox_ok,
        "alphaIsBinary": alpha_binary,
        "alphaValueCount": len(alpha_values),
        "visibleMagentaPixels": visible_magenta,
        "visibleStrongKeyPixels": visible_key_like,
        "ok": size_ok and bbox_ok and alpha_binary and key_clean,
    }


def main():
    parser = argparse.ArgumentParser(description="Audit UE-ready ONOKO ARCANA card alpha PNGs.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--out")
    parser.add_argument("--expected-bbox", type=parse_bbox, default=EXPECTED_BBOX)
    args = parser.parse_args()

    results = []
    for pattern in args.paths:
        matches = sorted(Path().glob(pattern))
        if not matches:
            path = Path(pattern)
            if path.exists():
                matches = [path]
        for path in matches:
            if path.suffix.lower() == ".png":
                results.append(audit(path, args.expected_bbox))

    payload = {
        "ok": all(item["ok"] for item in results),
        "count": len(results),
        "expectedBbox": list(args.expected_bbox),
        "results": results,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
