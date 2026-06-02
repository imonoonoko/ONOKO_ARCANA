import argparse
import json
from pathlib import Path

from PIL import Image


def parse_bbox(value):
    parts = [int(part.strip()) for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox must be x1,y1,x2,y2")
    x1, y1, x2, y2 = parts
    if x2 <= x1 or y2 <= y1:
        raise argparse.ArgumentTypeError("bbox must have positive width and height")
    return x1, y1, x2, y2


def parse_args():
    parser = argparse.ArgumentParser(description="Fit an RGBA card's visible alpha bbox to a target bbox.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--target-bbox", required=True, type=parse_bbox)
    parser.add_argument("--report", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    src_path = Path(args.input)
    out_path = Path(args.out)
    report_path = Path(args.report)
    image = Image.open(src_path).convert("RGBA")
    alpha = image.getchannel("A")
    source_bbox = alpha.getbbox()
    if not source_bbox:
        raise RuntimeError(f"No visible alpha bbox found: {src_path}")

    target_bbox = args.target_bbox
    source_crop = image.crop(source_bbox)
    target_size = (target_bbox[2] - target_bbox[0], target_bbox[3] - target_bbox[1])
    fitted = source_crop.resize(target_size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", image.size, (0, 0, 0, 0))
    canvas.alpha_composite(fitted, (target_bbox[0], target_bbox[1]))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)

    final_bbox = canvas.getchannel("A").getbbox()
    report = {
        "input": str(src_path),
        "out": str(out_path),
        "sourceSize": list(image.size),
        "sourceBbox": list(source_bbox),
        "sourceBboxSize": [source_bbox[2] - source_bbox[0], source_bbox[3] - source_bbox[1]],
        "targetBbox": list(target_bbox),
        "targetBboxSize": list(target_size),
        "finalBbox": list(final_bbox) if final_bbox else None,
        "reason": "Fit the visible alpha silhouette to the requested target bbox so card sizes match in Unreal QA.",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
