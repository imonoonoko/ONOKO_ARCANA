import argparse
import json
from pathlib import Path
import warnings

from PIL import Image, ImageDraw, ImageOps


warnings.filterwarnings("ignore", category=DeprecationWarning)

CANVAS_SIZE = (1024, 1536)
CARD_ALPHA_RECT = (54, 32, 970, 1514)
CORNER_RADIUS = 52
# Keep the illustration inside the frame's open window. The earlier V4 pass used
# the wider legacy crop and let city/background pixels show under the side rails.
CENTRAL_ART_RECT = (222, 346, 802, 1098)
FRAME_CUTOUT_RECT = (210, 320, 814, 1136)
CENTRAL_ART_MASK_RADIUS = 24


def parse_args():
    parser = argparse.ArgumentParser(description="Compose ONOKO ARCANA V4 card layers.")
    parser.add_argument("--template", required=True, help="Front frame template PNG.")
    parser.add_argument("--central-art", help="Central art source PNG/JPG for a front card.")
    parser.add_argument("--back-source", help="Full card back source PNG.")
    parser.add_argument("--card-mask-source", help="Optional PNG whose alpha defines the final card silhouette.")
    parser.add_argument("--out-composed", required=True, help="Output composed PNG.")
    parser.add_argument("--out-alpha", required=True, help="Output UE alpha PNG.")
    parser.add_argument("--staging-out", help="Optional copy for Unreal import staging.")
    parser.add_argument("--frame-out", help="Optional transparent front frame template output.")
    parser.add_argument("--alpha-mask-out", help="Optional alpha mask output.")
    parser.add_argument("--report", help="Optional JSON report output.")
    return parser.parse_args()


def ensure_canvas(image):
    image = image.convert("RGBA")
    if image.size != CANVAS_SIZE:
        image = ImageOps.fit(image, CANVAS_SIZE, method=Image.Resampling.LANCZOS)
    return image


def cover_fit(image, size):
    return ImageOps.fit(image.convert("RGBA"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def contain_fit(image, size):
    image = image.convert("RGBA")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    out = Image.new("RGBA", size, (4, 7, 12, 255))
    out.alpha_composite(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return out


def alpha_mask():
    mask = Image.new("L", CANVAS_SIZE, 0)
    draw = ImageDraw.Draw(mask)
    x0, y0, x1, y1 = CARD_ALPHA_RECT
    draw.rounded_rectangle((x0, y0, x1 - 1, y1 - 1), radius=CORNER_RADIUS, fill=255)
    return mask


def alpha_mask_from_source(path):
    source = ensure_canvas(Image.open(path))
    alpha = source.getchannel("A")
    mask = Image.new("L", CANVAS_SIZE, 0)
    mask.putdata([255 if a > 0 else 0 for a in alpha.getdata()])
    return mask


def final_card_mask(mask_source=None):
    if mask_source:
        return alpha_mask_from_source(mask_source)
    return alpha_mask()


def make_front_frame(template):
    frame = ensure_canvas(template)
    alpha = frame.getchannel("A")
    clear = Image.new("L", CANVAS_SIZE, 0)
    draw = ImageDraw.Draw(clear)
    x0, y0, x1, y1 = FRAME_CUTOUT_RECT
    draw.rounded_rectangle((x0, y0, x1 - 1, y1 - 1), radius=30, fill=255)
    alpha_data = []
    for a, c in zip(alpha.getdata(), clear.getdata()):
        alpha_data.append(0 if c else a)
    new_alpha = Image.new("L", CANVAS_SIZE, 0)
    new_alpha.putdata(alpha_data)
    frame.putalpha(new_alpha)
    return frame


def clip_alpha_to_card_mask(image, mask_source=None):
    image = ensure_canvas(image)
    mask = final_card_mask(mask_source)
    original = image.getchannel("A")
    clipped = Image.new("L", CANVAS_SIZE, 0)
    clipped.putdata([255 if a and m else 0 for a, m in zip(original.getdata(), mask.getdata())])
    image.putalpha(clipped)
    return image


def apply_final_alpha(image, mask_source=None):
    image = ensure_canvas(image)
    mask = final_card_mask(mask_source)
    mask_values = list(mask.getdata())
    width, height = CANVAS_SIZE
    edge_values = [False] * (width * height)
    edge_radius = 3
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            if not mask_values[idx]:
                continue
            for dy in range(-edge_radius, edge_radius + 1):
                if edge_values[idx]:
                    break
                for dx in range(-edge_radius, edge_radius + 1):
                    if abs(dx) + abs(dy) > edge_radius:
                        continue
                    nx = x + dx
                    ny = y + dy
                    if nx < 0 or nx >= width or ny < 0 or ny >= height or not mask_values[ny * width + nx]:
                        edge_values[idx] = True
                        break
    out = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    pixels = []
    for r, g, b, a in image.getdata():
        pixels.append((r, g, b, 255 if a else 0))
    solid = Image.new("RGBA", CANVAS_SIZE)
    solid.putdata(pixels)
    out.alpha_composite(solid)
    out.putalpha(mask)
    data = []
    for idx, (r, g, b, a) in enumerate(out.getdata()):
        if a == 0:
            data.append((0, 0, 0, 0))
        elif edge_values[idx]:
            data.append((0, 0, 0, 255))
        elif r > 120 and b > 120 and g < 80:
            data.append((0, 0, 0, 255))
        else:
            data.append((r, g, b, 255))
    out.putdata(data)
    return out


def compose_front(template_path, central_art_path):
    template = ensure_canvas(Image.open(template_path))
    frame = make_front_frame(template)
    art_size = (CENTRAL_ART_RECT[2] - CENTRAL_ART_RECT[0], CENTRAL_ART_RECT[3] - CENTRAL_ART_RECT[1])
    art = cover_fit(Image.open(central_art_path), art_size)
    art_mask = Image.new("L", art_size, 0)
    draw = ImageDraw.Draw(art_mask)
    draw.rounded_rectangle((0, 0, art_size[0] - 1, art_size[1] - 1), radius=CENTRAL_ART_MASK_RADIUS, fill=255)
    art.putalpha(art_mask)
    base = Image.new("RGBA", CANVAS_SIZE, (4, 7, 12, 255))
    base.alpha_composite(art, CENTRAL_ART_RECT[:2])
    base.alpha_composite(frame)
    return base, frame


def compose_back(back_source_path, mask_source_path=None):
    source = ensure_canvas(Image.open(back_source_path))
    if not mask_source_path:
        return source

    source_bbox = source.getchannel("A").getbbox() or (0, 0, CANVAS_SIZE[0], CANVAS_SIZE[1])
    target_mask = final_card_mask(mask_source_path)
    target_bbox = target_mask.getbbox() or CARD_ALPHA_RECT
    crop = source.crop(source_bbox)
    fitted = crop.resize((target_bbox[2] - target_bbox[0], target_bbox[3] - target_bbox[1]), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    canvas.alpha_composite(fitted, target_bbox[:2])
    return canvas


def main():
    args = parse_args()
    out_composed = Path(args.out_composed)
    out_alpha = Path(args.out_alpha)
    staging_out = Path(args.staging_out) if args.staging_out else None

    if args.back_source:
        composed = compose_back(args.back_source, args.card_mask_source)
        frame = None
        mode = "back"
    else:
        if not args.central_art:
            raise SystemExit("--central-art is required when --back-source is not used")
        composed, frame = compose_front(args.template, args.central_art)
        mode = "front"

    final_alpha = apply_final_alpha(composed, args.card_mask_source)

    out_composed.parent.mkdir(parents=True, exist_ok=True)
    out_alpha.parent.mkdir(parents=True, exist_ok=True)
    composed.save(out_composed)
    final_alpha.save(out_alpha)

    if staging_out:
        staging_out.parent.mkdir(parents=True, exist_ok=True)
        final_alpha.save(staging_out)

    if args.frame_out and frame:
        frame_out = Path(args.frame_out)
        frame_out.parent.mkdir(parents=True, exist_ok=True)
        clip_alpha_to_card_mask(frame, args.card_mask_source).save(frame_out)

    if args.alpha_mask_out:
        mask_out = Path(args.alpha_mask_out)
        mask_out.parent.mkdir(parents=True, exist_ok=True)
        final_card_mask(args.card_mask_source).save(mask_out)

    if args.report:
        final_bbox = final_alpha.getchannel("A").getbbox()
        report = {
            "mode": mode,
            "canvasSize": list(CANVAS_SIZE),
            "cardAlphaRect": list(CARD_ALPHA_RECT),
            "cornerRadius": CORNER_RADIUS,
            "centralArtRect": list(CENTRAL_ART_RECT),
            "frameCutoutRect": list(FRAME_CUTOUT_RECT),
            "template": args.template,
            "centralArt": args.central_art,
            "backSource": args.back_source,
            "cardMaskSource": args.card_mask_source,
            "finalAlphaBbox": list(final_bbox) if final_bbox else None,
            "outComposed": str(out_composed),
            "outAlpha": str(out_alpha),
            "stagingOut": str(staging_out) if staging_out else None,
        }
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
