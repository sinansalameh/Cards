"""Draw the app icons (four card suits on the app's green) into icons/.

Usage:  python tools/make_icons.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "icons"
GREEN = (17, 105, 74)
CREAM = (246, 235, 207)
CORAL = (255, 150, 136)
FONT = r"C:\Windows\Fonts\seguisym.ttf"  # has the suit glyphs
S = 1024  # draw large, scale down


def draw(full_bleed: bool, content: float) -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if full_bleed:
        d.rectangle([0, 0, S, S], fill=GREEN)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=GREEN)
    # 2x2 suits centred inside `content` of the canvas
    box = S * content
    cell = box / 2
    font = ImageFont.truetype(FONT, int(cell * 1.2))
    origin = (S - box) / 2
    suits = [("\u2660", CREAM), ("\u2665", CORAL), ("\u2666", CORAL), ("\u2663", CREAM)]
    for i, (ch, col) in enumerate(suits):
        cx = origin + cell * (i % 2) + cell / 2
        cy = origin + cell * (i // 2) + cell / 2
        d.text((cx, cy), ch, font=font, fill=col, anchor="mm")
    return img


def main():
    OUT.mkdir(exist_ok=True)
    regular = draw(full_bleed=False, content=0.70)
    maskable = draw(full_bleed=True, content=0.56)  # stays inside Android's safe circle
    for size in (192, 512):
        regular.resize((size, size), Image.LANCZOS).save(OUT / f"icon-{size}.png")
    maskable.resize((512, 512), Image.LANCZOS).save(OUT / "icon-maskable-512.png")
    maskable.convert("RGB").resize((180, 180), Image.LANCZOS).save(OUT / "apple-touch-icon.png")
    print("icons written to", OUT)


if __name__ == "__main__":
    main()
