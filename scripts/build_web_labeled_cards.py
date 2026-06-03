from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "data" / "major-arcana-v5-deck.json"
OUT_ROOT = ROOT / "assets" / "generated" / "card-production-v5-full" / "web-labeled"
OUT_ALPHA = OUT_ROOT / "alpha"
REPORTS = OUT_ROOT / "reports"

CANVAS_SIZE = (1024, 1536)
TOP_LABEL = (292, 200, 732, 270)
BOTTOM_LABEL = (256, 1258, 768, 1368)
TITLE_TEXT_Y_OFFSET = -10
KEYWORD_TEXT_Y_OFFSET = 12
ROMAN_NUMERALS = {
    "00": "0",
    "01": "I",
    "02": "II",
    "03": "III",
    "04": "IV",
    "05": "V",
    "06": "VI",
    "07": "VII",
    "08": "VIII",
    "09": "IX",
    "10": "X",
    "11": "XI",
    "12": "XII",
    "13": "XIII",
    "14": "XIV",
    "15": "XV",
    "16": "XVI",
    "17": "XVII",
    "18": "XVIII",
    "19": "XIX",
    "20": "XX",
    "21": "XXI",
}

FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\meiryob.ttc"),
    Path(r"C:\Windows\Fonts\YuGothB.ttc"),
    Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf"),
    Path(r"C:\Windows\Fonts\meiryo.ttc"),
    Path(r"C:\Windows\Fonts\YuGothM.ttc"),
    Path(r"C:\Windows\Fonts\msgothic.ttc"),
]


def font_path() -> Path:
    for path in FONT_CANDIDATES:
        if path.exists():
            return path
    raise SystemExit("No Japanese-capable font found in C:\\Windows\\Fonts")


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    return round(draw.textlength(text, font=font))


def fitted_font(draw: ImageDraw.ImageDraw, text: str, font_file: Path, max_width: int, start: int, minimum: int) -> ImageFont.FreeTypeFont:
    for size in range(start, minimum - 1, -1):
        font = ImageFont.truetype(str(font_file), size)
        width, _ = text_size(draw, text, font)
        if width <= max_width:
            return font
    return ImageFont.truetype(str(font_file), minimum)


def visual_text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int, int, int]:
    return draw.textbbox((0, 0), text, font=font)


def draw_visual_center(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    center: tuple[float, float],
    fill: tuple[int, int, int, int],
) -> None:
    left, top, right, bottom = visual_text_size(draw, text, font)
    x = center[0] - (left + right) / 2
    y = center[1] - (top + bottom) / 2
    draw.text((x, y), text, font=font, fill=fill)


def centered_line_at(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    y: float,
    fill: tuple[int, int, int, int],
) -> None:
    cx = rect[0] + (rect[2] - rect[0]) / 2
    draw_visual_center(draw, text, font, (cx, y), fill)


def display_number(number: str) -> str:
    return ROMAN_NUMERALS.get(number, number)


def draw_title_label(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    number: str,
    name: str,
    font_file: Path,
    fill: tuple[int, int, int, int],
) -> tuple[int, int]:
    number_text = display_number(number)
    gap = 38
    max_width = rect[2] - rect[0] - 24
    for size in range(44, 29, -1):
        number_font = ImageFont.truetype(str(font_file), max(size - 1, 28))
        name_font = ImageFont.truetype(str(font_file), size)
        number_width = text_width(draw, number_text, number_font)
        name_width = text_width(draw, name, name_font)
        if number_width + gap + name_width <= max_width:
            break
    else:
        number_font = ImageFont.truetype(str(font_file), 28)
        name_font = ImageFont.truetype(str(font_file), 30)
        number_width = text_width(draw, number_text, number_font)
        name_width = text_width(draw, name, name_font)

    total_width = number_width + gap + name_width
    x = rect[0] + ((rect[2] - rect[0]) - total_width) // 2
    y = rect[1] + (rect[3] - rect[1]) / 2 + TITLE_TEXT_Y_OFFSET
    draw_visual_center(draw, number_text, number_font, (x + number_width / 2, y), fill)
    draw_visual_center(draw, name, name_font, (x + number_width + gap + name_width / 2, y), fill)
    return number_font.size, name_font.size


def draw_card_labels(card: dict, source: Path, dest: Path, font_file: Path) -> dict:
    image = Image.open(source).convert("RGBA")
    if image.size != CANVAS_SIZE:
        raise ValueError(f"{source} is {image.size}, expected {CANVAS_SIZE}")

    draw = ImageDraw.Draw(image)
    dark = (20, 16, 10, 255)

    upright = "正位置 " + " / ".join(card["uprightKeywords"])
    reversed_line = "逆位置 " + " / ".join(card["reversedKeywords"])

    bottom_width = BOTTOM_LABEL[2] - BOTTOM_LABEL[0] - 58

    number_font_size, title_font_size = draw_title_label(draw, TOP_LABEL, card["number"], card["japaneseName"], font_file, dark)
    keyword_font = fitted_font(draw, upright, font_file, bottom_width, 32, 22)
    reversed_font = fitted_font(draw, reversed_line, font_file, bottom_width, 29, 20)

    center_y = BOTTOM_LABEL[1] + (BOTTOM_LABEL[3] - BOTTOM_LABEL[1]) / 2 + KEYWORD_TEXT_Y_OFFSET
    centered_line_at(draw, BOTTOM_LABEL, upright, keyword_font, center_y - 22, dark)
    centered_line_at(draw, BOTTOM_LABEL, reversed_line, reversed_font, center_y + 22, dark)

    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)

    alpha_bbox = image.getchannel("A").getbbox()
    return {
        "id": card["id"],
        "number": card["number"],
        "displayNumber": display_number(card["number"]),
        "japaneseName": card["japaneseName"],
        "englishName": card["englishName"],
        "source": str(source.relative_to(ROOT)),
        "output": str(dest.relative_to(ROOT)),
        "size": list(image.size),
        "alphaBbox": list(alpha_bbox) if alpha_bbox else None,
        "numberFont": number_font_size,
        "titleFont": title_font_size,
        "keywordFont": keyword_font.size,
    }


def deck_path(value: str) -> Path:
    return (DECK.parent / value).resolve()


def build_contact_sheet(paths: list[Path], out_path: Path) -> None:
    thumb_size = (150, 225)
    columns = 6
    rows = (len(paths) + columns - 1) // columns
    gap = 16
    label_h = 22
    sheet = Image.new("RGB", (columns * thumb_size[0] + (columns + 1) * gap, rows * (thumb_size[1] + label_h) + (rows + 1) * gap), (4, 7, 12))
    draw = ImageDraw.Draw(sheet)
    font_file = font_path()
    label_font = ImageFont.truetype(str(font_file), 14)

    for index, path in enumerate(paths):
        row = index // columns
        col = index % columns
        x = gap + col * (thumb_size[0] + gap)
        y = gap + row * (thumb_size[1] + label_h + gap)
        card = Image.open(path).convert("RGBA")
        card.thumbnail(thumb_size, Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", thumb_size, (0, 0, 0, 0))
        frame.alpha_composite(card, ((thumb_size[0] - card.width) // 2, (thumb_size[1] - card.height) // 2))
        sheet.paste(frame.convert("RGB"), (x, y))
        draw.text((x, y + thumb_size[1] + 4), path.stem.replace("-onoko-v5-alpha", ""), font=label_font, fill=(216, 180, 107))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def main() -> None:
    deck = json.loads(DECK.read_text(encoding="utf-8"))
    font_file = font_path()
    OUT_ALPHA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    generated = []

    back_source = deck_path(deck["back"]["alphaImage"])
    back_dest = OUT_ALPHA / Path(deck["back"]["alphaImage"]).name
    shutil.copyfile(back_source, back_dest)

    for card in deck["cards"]:
        source = deck_path(card["alphaImage"])
        dest = OUT_ALPHA / Path(card["alphaImage"]).name
        generated.append(draw_card_labels(card, source, dest, font_file))

    contact_sheet = REPORTS / "web-labeled-major-arcana-contact-sheet.png"
    build_contact_sheet([OUT_ALPHA / Path(card["alphaImage"]).name for card in deck["cards"]], contact_sheet)

    report = {
        "ok": True,
        "deck": str(DECK.relative_to(ROOT)),
        "font": str(font_file),
        "outputRoot": str(OUT_ALPHA.relative_to(ROOT)),
        "cardBack": str(back_dest.relative_to(ROOT)),
        "cards": generated,
        "contactSheet": str(contact_sheet.relative_to(ROOT)),
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
    }
    report_path = REPORTS / "web-labeled-major-arcana-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "cards": len(generated), "report": str(report_path.relative_to(ROOT)), "contactSheet": str(contact_sheet.relative_to(ROOT))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
