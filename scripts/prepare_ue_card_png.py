import argparse
from collections import deque
import json
import warnings
from pathlib import Path

from PIL import Image, ImageDraw, ImageStat


warnings.filterwarnings("ignore", category=DeprecationWarning)

CANVAS_SIZE = (1024, 1536)
TARGET_RECT = (54, 32, 970, 1514)
CORNER_RADIUS = 52


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare a generated ONOKO ARCANA card image for Unreal.")
    parser.add_argument("--input", required=True, help="Source chroma-key PNG.")
    parser.add_argument("--out", required=True, help="Final alpha PNG path.")
    parser.add_argument("--staging-out", help="Optional copy path for Unreal import staging.")
    parser.add_argument("--report", help="Optional JSON report path.")
    parser.add_argument("--key-threshold", type=float, default=90.0)
    return parser.parse_args()


def border_key_color(image):
    pixels = []
    width, height = image.size
    for x in range(width):
        pixels.append(image.getpixel((x, 0))[:3])
        pixels.append(image.getpixel((x, height - 1))[:3])
    for y in range(height):
        pixels.append(image.getpixel((0, y))[:3])
        pixels.append(image.getpixel((width - 1, y))[:3])
    sample = Image.new("RGB", (len(pixels), 1))
    sample.putdata(pixels)
    return tuple(int(v) for v in ImageStat.Stat(sample).median)


def chroma_alpha(image, key, threshold):
    alpha = Image.new("L", image.size, 0)
    src = image.convert("RGBA")
    out = []
    kr, kg, kb = key
    for r, g, b, _ in src.getdata():
        distance = ((r - kr) ** 2 + (g - kg) ** 2 + (b - kb) ** 2) ** 0.5
        out.append(0 if distance <= threshold else 255)
    alpha.putdata(out)
    return alpha


def keylike_mask(image, key, threshold):
    kr, kg, kb = key
    data = []
    for r, g, b, _ in image.convert("RGBA").getdata():
        distance = ((r - kr) ** 2 + (g - kg) ** 2 + (b - kb) ** 2) ** 0.5
        data.append(distance <= threshold)
    return data


def connected_background_mask(image, key, threshold, passable_mask=None):
    width, height = image.size
    keylike = keylike_mask(image, key, threshold)
    if passable_mask is not None:
        passable = [k or p for k, p in zip(keylike, passable_mask)]
    else:
        passable = keylike
    seen = [False] * (width * height)
    queue = deque()

    def push(x, y):
        idx = y * width + x
        if not seen[idx] and passable[idx]:
            seen[idx] = True
            queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)
    for y in range(height):
        push(0, y)
        push(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                push(nx, ny)
    return seen


def inverse_bbox(background_mask, size):
    width, height = size
    xs = []
    ys = []
    for y in range(height):
        row = y * width
        for x in range(width):
            if not background_mask[row + x]:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def rounded_mask(size):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    x0, y0, x1, y1 = TARGET_RECT
    draw.rounded_rectangle((x0, y0, x1 - 1, y1 - 1), radius=CORNER_RADIUS, fill=255)
    return mask


def main():
    args = parse_args()
    source_path = Path(args.input)
    out_path = Path(args.out)
    staging_path = Path(args.staging_out) if args.staging_out else None
    report_path = Path(args.report) if args.report else None

    source = Image.open(source_path).convert("RGBA")
    if source.size != CANVAS_SIZE:
        source = source.resize(CANVAS_SIZE, Image.Resampling.LANCZOS)

    key = border_key_color(source)
    background = connected_background_mask(source, key, args.key_threshold)
    bbox = inverse_bbox(background, source.size)
    if bbox is None:
        raise RuntimeError(f"No visible card body detected in {source_path}")

    crop = source.crop(bbox)
    target_width = TARGET_RECT[2] - TARGET_RECT[0]
    target_height = TARGET_RECT[3] - TARGET_RECT[1]
    fitted = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    canvas.alpha_composite(fitted, TARGET_RECT[:2])
    mask = rounded_mask(CANVAS_SIZE)
    r, g, b, _ = canvas.split()
    rgba_data = []
    for rv, gv, bv, mv in zip(r.getdata(), g.getdata(), b.getdata(), mask.getdata()):
        is_visible_key_spill = rv > 120 and bv > 120 and gv < 80
        final_a = 255 if mv >= 128 else 0
        if final_a == 0:
            rgba_data.append((0, 0, 0, 0))
        elif is_visible_key_spill:
            rgba_data.append((0, 0, 0, final_a))
        else:
            rgba_data.append((rv, gv, bv, final_a))
    final = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    final.putdata(rgba_data)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(out_path)
    if staging_path:
        staging_path.parent.mkdir(parents=True, exist_ok=True)
        final.save(staging_path)

    if report_path:
        alpha_bbox = final.getchannel("A").getbbox()
        report = {
            "input": str(source_path),
            "output": str(out_path),
            "stagingOutput": str(staging_path) if staging_path else None,
            "canvasSize": list(CANVAS_SIZE),
            "keyColor": list(key),
            "sourceVisibleBbox": list(bbox),
            "finalAlphaBbox": list(alpha_bbox) if alpha_bbox else None,
            "targetRect": list(TARGET_RECT),
            "cornerRadius": CORNER_RADIUS,
        }
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
