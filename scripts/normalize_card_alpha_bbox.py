import argparse
import json
from pathlib import Path

from PIL import Image


CANVAS_SIZE = (1024, 1536)


def parse_bbox(raw):
    parts = [int(part.strip()) for part in raw.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox must be x0,y0,x1,y1")
    x0, y0, x1, y1 = parts
    if not (0 <= x0 < x1 <= CANVAS_SIZE[0] and 0 <= y0 < y1 <= CANVAS_SIZE[1]):
        raise argparse.ArgumentTypeError(f"bbox out of range for {CANVAS_SIZE}: {raw}")
    return x0, y0, x1, y1


def parse_args():
    parser = argparse.ArgumentParser(description="Fit a transparent card's visible alpha bbox to a target bbox.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--target-bbox", type=parse_bbox, default=(54, 32, 970, 1514))
    parser.add_argument("--report")
    return parser.parse_args()


def main():
    args = parse_args()
    source_path = Path(args.input)
    out_path = Path(args.out)
    image = Image.open(source_path).convert("RGBA")
    if image.size != CANVAS_SIZE:
        image = image.resize(CANVAS_SIZE, Image.Resampling.LANCZOS)

    source_bbox = image.getchannel("A").getbbox()
    if source_bbox is None:
        raise SystemExit(f"No visible alpha in {source_path}")

    crop = image.crop(source_bbox)
    x0, y0, x1, y1 = args.target_bbox
    resized = crop.resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    canvas.alpha_composite(resized, (x0, y0))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)

    report = {
        "input": str(source_path),
        "out": str(out_path),
        "canvasSize": list(CANVAS_SIZE),
        "sourceAlphaBbox": list(source_bbox),
        "targetAlphaBbox": list(args.target_bbox),
        "outputAlphaBbox": list(canvas.getchannel("A").getbbox() or ()),
    }
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
