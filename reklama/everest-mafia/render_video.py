#!/usr/bin/env python3
"""
Everest Mafia — Instagram Reels reklama videosini render qiladi.

Kadrlar (AI generatsiya qilingan) ustiga o'zbekcha matn qo'yadi va
9:16 (1080x1920) hamda 4:5 (1080x1350) formatlarda stills yaratadi.

Ishlatish:
    python render_video.py --format 9x16
    python render_video.py --format 4x5
"""
from __future__ import annotations

import argparse
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(HERE, "frames")
OUT = os.path.join(HERE, "build", "stills")

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

RED = (226, 32, 42)
WHITE = (255, 255, 255)
DIM = (214, 219, 226)

# Sahnar: (img, kicker, headline, sub, buton_matni, link_matni, brand)
SCENES = [
    dict(
        img="01_hook.jpg",
        kicker="TELEGRAMʼDA MAFA OʻYINI",
        headline="OʻYINCHI BOʻL!",
        sub="Oʻzbek tilidagi haqiqiy mafiya oʻyini",
        cta=None,
        link=None,
    ),
    dict(
        img="02_gameplay.jpg",
        kicker="SIZ SHAHARDASIZ",
        headline="DOʻSTLARINGIZ YONDAKI XONADA",
        sub="Ulardan biri — mafiya. Siz esa shahof.",
        cta=None,
        link=None,
    ),
    dict(
        img="03_roles.jpg",
        kicker="ROLLAR",
        headline="KIM MAFIYA,\nKIM SHAHOF?",
        sub="Mafiya · Shahof · Tibbiyotchi",
        cta=None,
        link=None,
    ),
    dict(
        img="04_phone.jpg",
        kicker="FEIL",
        headline="FAQAT FEILIN\nSOʻZLARI SIZNI\nOGOHLANTIRADI",
        sub="Har bir soʻz — dalil. Har bir dalil — gʻalaba.",
        cta=None,
        link=None,
    ),
    dict(
        img="03_roles.jpg",
        kicker="DALIL TOʻPLA",
        headline="MAFIYANI\nUSHLA",
        sub="Shahof boʻlsangiz — shaharda yutasaniz",
        cta=None,
        link=None,
    ),
    dict(
        img="05_win.jpg",
        kicker="TUNDA YOKI KUNDA",
        headline="GʻALABA SENING\nQOʻLINGDA",
        sub="Everest Mafia — har kuni yangi oʻyin",
        cta=None,
        link=None,
    ),
    dict(
        img="01_hook.jpg",
        kicker="",
        headline="EVEREST\nMAFIA",
        sub="Telegramʼdagi mafiya oʻyini",
        cta="HOZIR OʻYNASH",
        link="t.me/everest_mafia_uzbekiston",
        brand=False,
    ),
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def cover(img: Image.Image, w: int, h: int) -> Image.Image:
    """Rasmni kadrlab to'ldiradi (cover)."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 1), int(ih * scale + 1)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return img.crop((left, top, left + w, top + h))


def scrim(img: Image.Image, strength: float = 1.0) -> Image.Image:
    """Yuqoridan pastga qoraytiruvchi gradient — matn o'qilishi uchun."""
    w, h = img.size
    overlay = Image.new("L", (1, h))
    px = overlay.load()
    for y in range(h):
        t = y / max(1, h - 1)
        # yuqorida 0.28, pastda 0.86
        v = 0.28 + (0.86 - 0.28) * (t ** 1.25)
        px[0, y] = int(255 * min(1.0, v * strength))
    mask = overlay.resize((w, h))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(dark, img, mask)


def vignette(img: Image.Image, amount: float = 0.55) -> Image.Image:
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-w * 0.35, -h * 0.18, w * 1.35, h * 1.18), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=min(w, h) * 0.12))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.blend(img, Image.composite(img, dark, mask), amount)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines: list[str] = []
    for block in text.split("\n"):
        words = block.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = f"{cur} {word}"
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    # juda uzun so'zlarni belgilar bo'yicha bo'lish
    fixed: list[str] = []
    for line in lines:
        if draw.textlength(line, font=fnt) <= max_w or not line:
            fixed.append(line)
            continue
        chunk = ""
        for ch in line:
            if draw.textlength(chunk + ch, font=fnt) > max_w and chunk:
                fixed.append(chunk)
                chunk = ch
            else:
                chunk += ch
        if chunk:
            fixed.append(chunk)
    return fixed


def draw_tracked(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill, tracking: int = 4, center: bool = False, width: int = 0):
    """Harflar orasidagi boʻshliqni oshirib chizadi."""
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=fnt) + tracking
    total -= tracking
    x, y = xy
    if center:
        x -= total / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, stroke_width=3, stroke_fill=(0, 0, 0, 220))
        x += draw.textlength(ch, font=fnt) + tracking
    return total


def fit_headline(draw, text, max_w, max_lines, start_size, min_size):
    """Sarlavhani oʻlcham moslashtiradi (hech qanday satr chegaradan chiqmasligi uchun)."""
    size = start_size
    while size > min_size:
        fnt = font(BOLD, size)
        lines = wrap(draw, text, fnt, max_w)
        line_h = int(size * 1.12)
        fits = (
            len(lines) <= max_lines
            and all(draw.textlength(l, font=fnt) <= max_w for l in lines)
            and len(lines) * line_h <= int(max_w * 1.15)
        )
        if fits:
            return fnt, lines, line_h
        size -= 4
    fnt = font(BOLD, min_size)
    return fnt, wrap(draw, text, fnt, max_w), int(min_size * 1.12)


def render_scene(scene: dict, w: int, h: int, index: int) -> Image.Image:
    bg = Image.open(os.path.join(FRAMES, scene["img"])).convert("RGB")
    bg = cover(bg, w, h)
    bg = ImageEnhance.Brightness(bg).enhance(0.72)
    bg = ImageEnhance.Contrast(bg).enhance(1.08)
    bg = scrim(bg, 1.0 if scene.get("cta") is None else 1.12)
    bg = vignette(bg, 0.5 if scene.get("cta") is None else 0.75)

    layer = bg.convert("RGBA")
    draw = ImageDraw.Draw(layer)

    # Yuqorida brand
    if scene.get("brand", True):
        brand_f = font(BOLD, int(h * 0.019))
        draw_tracked(draw, (w // 2, int(h * 0.045)), "EVEREST MAFIA", brand_f, (255, 255, 255, 205), tracking=6, center=True)

    side = int(w * 0.09)
    max_w = w - side * 2
    bottom_limit = int(h * 0.86)  # Reels UI ostidan chiqmasligi uchun

    if scene.get("cta"):
        # CTA sahna — markazda joylashgan
        kicker_f = font(BOLD, int(h * 0.019))
        head_f = font(BOLD, int(h * 0.072))
        sub_f = font(REGULAR, int(h * 0.024))

        head_lines = scene["headline"].split("\n")
        head_h = len(head_lines) * int(head_f.size * 1.1)
        sub_y = int(h * 0.47) + head_h
        sub = scene.get("sub") or ""
        if sub:
            draw.text((w // 2, sub_y), sub, font=sub_f, fill=DIM + (235,), anchor="ma")

        y = int(h * 0.40) - head_h // 2
        for line in head_lines:
            draw.text((w // 2, y), line, font=head_f, fill=WHITE + (255,), anchor="ma")
            y += int(head_f.size * 1.1)

        # Tugma
        btn_f = font(BOLD, int(h * 0.026))
        btn_text = scene["cta"]
        bw = int(draw.textlength(btn_text, font=btn_f)) + int(w * 0.16)
        bh = int(h * 0.052)
        bx = (w - bw) // 2
        by = sub_y + int(h * 0.035)
        draw.rounded_rectangle((bx, by, bx + bw, by + bh), radius=bh // 2, fill=RED + (255,))
        draw.text((w // 2, by + bh // 2), btn_text, font=btn_f, fill=WHITE + (255,), anchor="mm")

        # Havola
        link_f = font(BOLD, int(h * 0.023))
        draw.text((w // 2, by + bh + int(h * 0.028)), scene["link"], font=link_f, fill=WHITE + (255,), anchor="ma")
        note_f = font(REGULAR, int(h * 0.0185))
        draw.text((w // 2, by + bh + int(h * 0.062)), "Telegramʼda — bepul va oʻzbek tilida",
                  font=note_f, fill=DIM + (225,), anchor="ma")
    else:
        kicker_f = font(BOLD, int(h * 0.0205))
        head_f, head_lines, line_h = fit_headline(
            draw, scene["headline"], max_w, 3, int(h * 0.062), int(h * 0.030)
        )
        sub_f = font(REGULAR, int(h * 0.0235))

        sub_text = scene.get("sub") or ""
        sub_lines = wrap(draw, sub_text, sub_f, max_w) if sub_text else []
        sub_block = len(sub_lines) * int(sub_f.size * 1.35)

        block_h = int(kicker_f.size * 2.1) + len(head_lines) * line_h + int(h * 0.018) + sub_block
        y = bottom_limit - block_h

        # kicker
        kicker_y = y
        draw_tracked(draw, (side, kicker_y), scene["kicker"], kicker_f, RED + (255,), tracking=5)
        y += int(kicker_f.size * 2.1)

        # headline
        for line in head_lines:
            draw.text((side, y), line, font=head_f, fill=WHITE + (255,), stroke_width=2, stroke_fill=(0, 0, 0, 210))
            y += line_h

        y += int(h * 0.016)
        # sub
        for line in sub_lines:
            draw.text((side, y), line, font=sub_f, fill=DIM + (238,), stroke_width=2, stroke_fill=(0, 0, 0, 200))
            y += int(sub_f.size * 1.35)

    return layer.convert("RGB")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=["9x16", "4x5"], default="9x16")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    w, h = (1080, 1920) if args.format == "9x16" else (1080, 1350)
    out_dir = args.out or os.path.join(OUT, args.format)
    os.makedirs(out_dir, exist_ok=True)

    for i, scene in enumerate(SCENES, start=1):
        img = render_scene(scene, w, h, i)
        path = os.path.join(out_dir, f"scene{i:02d}.png")
        img.save(path, quality=95)
        print("✓", path)


if __name__ == "__main__":
    main()
