import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


THUMB_SIZE = (256, 384)
LABEL_HEIGHT = 28
PAD = 16


def parse_args():
    parser = argparse.ArgumentParser(description="Build a contact sheet for ONOKO ARCANA cards.")
    parser.add_argument("--out", required=True)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("images", nargs="+")
    return parser.parse_args()


def checkerboard(size, cell=16):
    image = Image.new("RGBA", size, (230, 230, 230, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(190, 190, 190, 255))
    return image


def make_thumb(path):
    source = Image.open(path).convert("RGBA")
    thumb = Image.new("RGBA", THUMB_SIZE, (0, 0, 0, 0))
    copy = source.copy()
    copy.thumbnail(THUMB_SIZE, Image.Resampling.LANCZOS)
    x = (THUMB_SIZE[0] - copy.width) // 2
    y = (THUMB_SIZE[1] - copy.height) // 2
    bg = checkerboard(THUMB_SIZE)
    bg.alpha_composite(copy, (x, y))
    return bg


def main():
    args = parse_args()
    paths = [Path(p) for p in args.images]
    cols = max(1, args.columns)
    rows = (len(paths) + cols - 1) // cols
    width = PAD + cols * (THUMB_SIZE[0] + PAD)
    height = PAD + rows * (THUMB_SIZE[1] + LABEL_HEIGHT + PAD)
    sheet = Image.new("RGBA", (width, height), (18, 20, 24, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, path in enumerate(paths):
        col = index % cols
        row = index // cols
        x = PAD + col * (THUMB_SIZE[0] + PAD)
        y = PAD + row * (THUMB_SIZE[1] + LABEL_HEIGHT + PAD)
        sheet.alpha_composite(make_thumb(path), (x, y))
        label = path.stem[:34]
        draw.text((x, y + THUMB_SIZE[1] + 6), label, fill=(235, 238, 244, 255), font=font)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out)


if __name__ == "__main__":
    main()

