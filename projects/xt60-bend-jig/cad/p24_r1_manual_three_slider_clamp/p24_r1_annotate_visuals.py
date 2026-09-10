"""Create the P24 R1 repair-cycle-2 visual evidence from frozen raster renders.

This recipe performs image-only cropping, scaling, labels, arrows, and explanatory
insets. It does not import, regenerate, or modify CAD geometry.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CAD_DIR = Path(__file__).resolve().parent
RELEASED = CAD_DIR / "p24_r1_released_open_repair1_final_20260830T040058Z.png"
CUTAWAY = CAD_DIR / "p24_r1_clamped_contact_cutaway.png"
OPERATION_OUT = CAD_DIR / "p24_r1_operation_annotated.png"
CONTACT_OUT = CAD_DIR / "p24_r1_clamped_contact_annotated.png"

EXPECTED = {
    RELEASED: "db875b1a25d5242ffd4de14c74d436d62cb18cb1dc8be87440ca2cdbd0e9bf95",
    CUTAWAY: "a826095c49459ee962812f1b395b26630362235dec6b347582284ec3f7fb94f5",
}

CJK = "/System/Library/Fonts/STHeiti Light.ttc"
LATIN_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
LATIN = "/System/Library/Fonts/Supplemental/Arial.ttf"

WHITE = "#ffffff"
INK = "#102033"
NAVY = "#0b1725"
TEAL = "#07979a"
FRAME = "#27384a"
BLUE = "#147ed1"
ORANGE = "#ed8b16"
GREEN = "#21ad64"
RED = "#ef4444"
YELLOW = "#ffd34d"


def font(size: int, *, bold: bool = False, cjk: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(CJK if cjk else (LATIN_BOLD if bold else LATIN), size)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_inputs() -> None:
    for path, expected in EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"Refusing changed input: {path.name}: {actual} != {expected}")


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str, width: int = 14) -> None:
    draw.line((start, end), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = width * 2.2
    wing = width * 1.25
    p1 = (
        end[0] - length * math.cos(angle) + wing * math.sin(angle),
        end[1] - length * math.sin(angle) - wing * math.cos(angle),
    )
    p2 = (
        end[0] - length * math.cos(angle) - wing * math.sin(angle),
        end[1] - length * math.sin(angle) + wing * math.cos(angle),
    )
    draw.polygon((end, p1, p2), fill=color)


def ring(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, color: str) -> None:
    draw.ellipse(
        (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
        outline=WHITE,
        width=12,
    )
    draw.ellipse(
        (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
        outline=color,
        width=7,
    )


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str = "#ffffff") -> None:
    draw.rounded_rectangle(box, radius=28, fill=fill, outline=outline, width=3)


def operation_image() -> None:
    base = Image.open(RELEASED).convert("RGB")
    canvas = Image.new("RGB", (2400, 1200), NAVY)
    canvas.paste(base, (0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.rounded_rectangle((28, 24, 1740, 150), radius=24, fill=(7, 20, 33, 226))
    draw.text((62, 40), "RELEASED_OPEN — 先手動定位 / POSITION BY HAND FIRST", font=font(50, cjk=True), fill=WHITE)
    draw.text((64, 105), "三個滑鞋到位後，最後才轉中央白色螺絲。", font=font(31, cjk=True), fill="#dce9f4")

    ring(draw, (1370, 590), 63, ORANGE)
    arrow(draw, (1370, 650), (1370, 790), ORANGE, 18)
    draw.rounded_rectangle((1185, 720, 1580, 820), radius=18, fill=(12, 20, 30, 220), outline=ORANGE, width=4)
    draw.text((1210, 738), "橘色 Orange：往下推 ↓", font=font(34, cjk=True), fill=WHITE)

    ring(draw, (1168, 627), 58, BLUE)
    arrow(draw, (1040, 590), (1255, 685), BLUE, 17)
    ring(draw, (1428, 806), 58, GREEN)
    arrow(draw, (1305, 756), (1510, 850), GREEN, 17)

    ring(draw, (1220, 915), 93, YELLOW)
    draw.line(((1290, 955), (1780, 1080)), fill=YELLOW, width=8)

    draw.rectangle((1800, 0, 2399, 1199), fill=NAVY)
    draw.text((1840, 52), "操作順序", font=font(48, cjk=True), fill=WHITE)
    draw.text((1842, 110), "OPERATION ORDER", font=font(26, bold=True), fill="#91a9bd")

    panel(draw, (1835, 175, 2365, 395), "#3b250c", ORANGE)
    draw.text((1870, 198), "1  橘色 Orange", font=font(38, cjk=True), fill=ORANGE)
    draw.text((1870, 257), "大拇指往下推", font=font(44, cjk=True), fill=WHITE)
    draw.text((1870, 326), "THUMB: PUSH DOWN", font=font(27, bold=True), fill="#ffe1b5")

    panel(draw, (1835, 425, 2365, 700), "#0b2944", BLUE)
    draw.text((1870, 448), "2  藍色 Blue + 綠色 Green", font=font(34, cjk=True), fill=WHITE)
    draw.text((1870, 510), "食指／中指", font=font(39, cjk=True), fill=WHITE)
    draw.text((1870, 568), "從後往前推  →", font=font(42, cjk=True), fill=WHITE)
    draw.text((1870, 640), "INDEX / MIDDLE: BACK → FRONT", font=font(23, bold=True), fill="#b9e6ff")

    panel(draw, (1835, 730, 2365, 1050), "#332b08", YELLOW)
    draw.text((1870, 753), "3  中央白色螺絲", font=font(38, cjk=True), fill=WHITE)
    draw.text((1870, 818), "只在三桿到位後", font=font(41, cjk=True), fill=WHITE)
    draw.text((1870, 878), "才夾緊", font=font(48, cjk=True), fill=YELLOW)
    draw.text((1870, 952), "CLAMP ONLY AFTER ALL 3", font=font(25, bold=True), fill="#fff1a8")
    draw.text((1870, 988), "RODS ARE POSITIONED", font=font(25, bold=True), fill="#fff1a8")

    draw.text((1840, 1092), "Exact RELEASED STEP snapshot + labels", font=font(23), fill="#9fb2c3")
    draw.text((1840, 1127), "Pressure plate open: +0.60 mm", font=font(23, bold=True), fill="#dce9f4")
    OPERATION_OUT.unlink(missing_ok=True)
    canvas.save(OPERATION_OUT, "PNG", optimize=True)


def contact_image() -> None:
    raw = Image.open(CUTAWAY).convert("RGB")
    crop = raw.crop((425, 165, 875, 840)).resize((840, 1260), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (2400, 1400), "#edf3f8")
    canvas.paste(crop, (35, 105))
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.rounded_rectangle((25, 20, 875, 102), radius=20, fill=(7, 20, 33, 235))
    draw.text((52, 36), "精確 CLAMPED STEP 切面 / EXACT CUTAWAY", font=font(37, cjk=True), fill=WHITE)
    draw.text((55, 1325), "Cropped/enlarged only — CAD geometry unchanged", font=font(23, bold=True), fill=INK)

    # Leaders on the exact clipped CAD image.
    ring(draw, (530, 835), 94, WHITE)
    draw.line(((605, 785), (755, 700)), fill=WHITE, width=8)
    draw.text((760, 665), "白色螺絲頭", font=font(27, cjk=True), fill=INK)
    draw.text((760, 705), "WHITE SCREW HEAD", font=font(20, bold=True), fill=INK)

    draw.line(((395, 555), (755, 480)), fill=TEAL, width=8)
    draw.text((760, 438), "青綠色壓板", font=font(27, cjk=True), fill=INK)
    draw.text((760, 478), "TEAL PRESSURE PLATE", font=font(20, bold=True), fill=INK)

    draw.line(((245, 570), (755, 290)), fill=FRAME, width=8)
    draw.text((760, 245), "深色框架／反力", font=font(27, cjk=True), fill=INK)
    draw.text((760, 285), "DARK FRAME REACTION", font=font(20, bold=True), fill=INK)

    draw.line(((650, 570), (755, 570)), fill=ORANGE, width=8)
    draw.text((760, 535), "三個彩色滑鞋接觸", font=font(25, cjk=True), fill=INK)
    draw.text((760, 575), "3 COLORED SHOE CONTACTS", font=font(19, bold=True), fill=INK)

    # Central screw axial contact inset.
    panel(draw, (1175, 35, 2365, 665), "#f8fbfd", FRAME)
    draw.text((1210, 63), "A  中央螺絲反力迴路 / SCREW REACTION LOOP", font=font(33, cjk=True), fill=INK)
    draw.text((1210, 112), "INBOARD  ←────────────────────────→  OUTBOARD", font=font(22, bold=True), fill="#526779")

    y = 345
    # Frame and conceptual threaded reaction.
    draw.rounded_rectangle((1240, 175, 1340, 525), radius=10, fill=FRAME)
    for yy in range(245, 450, 28):
        draw.line(((1245, yy + 16), (1335, yy - 16)), fill="#9db0c0", width=5)
    draw.line(((1260, y), (2050, y)), fill=BLUE, width=28)
    draw.text((1210, 535), "框架螺紋反力：概念表示", font=font(27, cjk=True), fill=FRAME)
    draw.text((1210, 575), "CONCEPTUAL THREAD — NO HELIX MODELED", font=font(21, bold=True), fill=RED)

    # Retainer, pressure plate and head.
    draw.rounded_rectangle((1570, 275, 1635, 415), radius=12, fill="#687789", outline=INK, width=3)
    draw.rounded_rectangle((1690, 205, 1780, 485), radius=12, fill=TEAL, outline=INK, width=3)
    draw.rounded_rectangle((1780, 245, 1985, 445), radius=70, fill="#f2f2ef", outline=INK, width=4)
    draw.line(((1638, 255), (1687, 255)), fill=ORANGE, width=6)
    arrow(draw, (1640, 255), (1685, 255), ORANGE, 7)
    draw.text((1515, 185), "0.30 mm", font=font(23, bold=True), fill=ORANGE)
    draw.text((1465, 445), "CAPTIVE PULL-BACK RETAINER", font=font(19, bold=True), fill=INK)
    draw.text((1500, 476), "inactive gap in CLAMPED", font=font(18), fill=ORANGE)
    draw.line(((1780, 230), (1780, 465)), fill=RED, width=9)
    draw.text((1810, 192), "ACTIVE: HEAD → PLATE", font=font(21, bold=True), fill=RED)
    draw.text((1810, 220), "zero-clearance contact", font=font(19), fill=RED)

    # Three-shoe sandwich inset.
    panel(draw, (1175, 700, 2365, 1365), "#f8fbfd", FRAME)
    draw.text((1210, 728), "B  三滑鞋夾層 / THREE-SHOE SANDWICH", font=font(34, cjk=True), fill=INK)
    draw.text((1210, 776), "CLAMPED_END: frame | flange | pressure plate", font=font(22, bold=True), fill="#526779")

    draw.rounded_rectangle((1370, 830, 1450, 1275), radius=10, fill=FRAME)
    draw.rounded_rectangle((1805, 830, 1885, 1275), radius=10, fill=TEAL)
    roles = ((BLUE, "藍 Blue"), (ORANGE, "橘 Orange"), (GREEN, "綠 Green"))
    for index, (color, label) in enumerate(roles):
        yy = 900 + index * 145
        draw.rounded_rectangle((1450, yy - 38, 1805, yy + 38), radius=32, fill=color, outline=INK, width=3)
        draw.ellipse((1418, yy - 57, 1532, yy + 57), fill=color, outline=INK, width=3)
        draw.text((1230, yy - 24), label, font=font(26, cjk=True), fill=INK)
        draw.line(((1448, yy - 56), (1448, yy + 56)), fill=RED, width=6)
        draw.line(((1807, yy - 56), (1807, yy + 56)), fill=RED, width=6)

    draw.text((1390, 1288), "FRAME CONTACT", font=font(20, bold=True), fill=FRAME, anchor="mm")
    draw.text((1845, 1288), "PLATE CONTACT", font=font(20, bold=True), fill=TEAL, anchor="mm")
    draw.text((1630, 1323), "All 3 active together • zero penetration", font=font(22, bold=True), fill=RED, anchor="mm")
    draw.text((1210, 1338), "Derived explanatory overlay — not to scale; exact CAD remains visible at left.", font=font(17), fill="#526779")

    CONTACT_OUT.unlink(missing_ok=True)
    canvas.save(CONTACT_OUT, "PNG", optimize=True)


if __name__ == "__main__":
    verify_inputs()
    operation_image()
    contact_image()
    print(OPERATION_OUT)
    print(CONTACT_OUT)
