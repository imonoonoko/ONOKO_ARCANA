import argparse
from pathlib import Path

from PIL import Image


# Source crop intentionally excludes the legacy side rails and label panels from
# the full-card concepts. Those rails are supplied by the V4 frame template.
SOURCE_ART_RECT = (222, 330, 802, 1118)


def parse_args():
    parser = argparse.ArgumentParser(description="Extract ONOKO ARCANA central art crops from existing full cards.")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("cards", nargs="+")
    return parser.parse_args()


def main():
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for card in args.cards:
        path = Path(card)
        image = Image.open(path).convert("RGBA")
        if image.size != (1024, 1536):
            image = image.resize((1024, 1536), Image.Resampling.LANCZOS)
        crop = image.crop(SOURCE_ART_RECT)
        out = out_dir / f"{path.stem}-central-v4-approved.png"
        crop.save(out)
        print(out)


if __name__ == "__main__":
    main()
