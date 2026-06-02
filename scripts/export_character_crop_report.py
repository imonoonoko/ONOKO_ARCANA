import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


CENTRAL_ART_RECT = (154, 324, 870, 1132)
FACE_RECT = (322, 360, 704, 742)
HANDS_OR_SYMBOL_RECT = (210, 610, 814, 1040)
CELL = (248, 248)
PAD = 14
LABEL_HEIGHT = 28


def parse_args():
    parser = argparse.ArgumentParser(description="Export visual crop report for ONOKO ARCANA character quality.")
    parser.add_argument("--out", required=True)
    parser.add_argument("images", nargs="+")
    return parser.parse_args()


def fit_crop(image, rect):
    crop = image.crop(rect).convert("RGBA")
    return ImageOps.fit(crop, CELL, method=Image.Resampling.LANCZOS)


def main():
    args = parse_args()
    paths = [Path(p) for p in args.images]
    cols = 4
    rows = len(paths)
    width = PAD + cols * (CELL[0] + PAD)
    height = PAD + rows * (CELL[1] + LABEL_HEIGHT + PAD)
    sheet = Image.new("RGBA", (width, height), (18, 20, 24, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    headers = ["full", "central", "face", "hands/symbol"]
    for c, header in enumerate(headers):
        draw.text((PAD + c * (CELL[0] + PAD), 2), header, fill=(170, 190, 230, 255), font=font)

    for row, path in enumerate(paths):
        image = Image.open(path).convert("RGBA")
        full = ImageOps.fit(image, CELL, method=Image.Resampling.LANCZOS)
        crops = [
            full,
            fit_crop(image, CENTRAL_ART_RECT),
            fit_crop(image, FACE_RECT),
            fit_crop(image, HANDS_OR_SYMBOL_RECT),
        ]
        y = PAD + row * (CELL[1] + LABEL_HEIGHT + PAD)
        for col, crop in enumerate(crops):
            x = PAD + col * (CELL[0] + PAD)
            sheet.alpha_composite(crop, (x, y))
        draw.text((PAD, y + CELL[1] + 6), path.stem[:80], fill=(235, 238, 244, 255), font=font)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out)


if __name__ == "__main__":
    main()

