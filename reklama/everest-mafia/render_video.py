#!/usr/bin/env python3
"""
Everest Mafia — Instagram reklama videosi uchun kadrlar va matn qatlamlari.

Har bir sahna uchun:
  * fon rasmi (qorongʻilash, gradient, vinyetka bilan)
  * alohida matn qatlamlari (RGBA PNG) — ffmpeg ularni vaqt boʻyicha ochadi
  * manifest.json — qatlamlarning joyi, kechikishi va kadrlar (qismlar) roʻyxati

Shrift: Tinos (Times New Roman bilan metrik-mos, OFL litsenziya).

Ishlatish:
    python render_video.py --format 9x16 --durations durations.json
"""
from __future__ import annotations

import argparse
import json
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(HERE, "frames")
FONTS = os.path.join(HERE, "fonts")

SERIF = os.path.join(FONTS, "Tinos-Regular.ttf")
SERIF_B = os.path.join(FONTS, "Tinos-Bold.ttf")
SERIF_I = os.path.join(FONTS, "Tinos-Italic.ttf")
SERIF_BI = os.path.join(FONTS, "Tinos-BoldItalic.ttf")

RED = (226, 32, 42)
RED_HOT = (255, 58, 62)
WHITE = (255, 255, 255)
DIM = (219, 223, 228)

# Sahnar: qismlar = kadrlar (kadr ichida kesilish), matn qatlamlari
SCENES = [
    dict(
        key="s1",
        parts=["01_hook.jpg"],
        kicker="TELEGRAMʼDA MAFA OʻYINI",
        headline=["OʻYINCHI BOʻL!"],
        sub=["Telegram guruhida, bot orqali oʻynang"],
    ),
    dict(
        key="s2",
        parts=["02_gameplay.jpg", "04_phone.jpg"],
        kicker="SIZ SHAHARDASIZ",
        headline=["DOʻSTLARINGIZ", "YONDAKI XONADA"],
        sub=["Ulardan biri — mafiya. Siz esa komissar."],
    ),
    dict(
        key="s3",
        parts=["03_roles.jpg"],
        kicker="OʻYIN ROLLARI",
        headline=["ASOSIY ROLLAR —", "KIM SIZ?"],
        sub=["Mafiya · Komissar · Tinch aholi · Doktor"],
    ),
    dict(
        key="s4",
        parts=["04_phone.jpg", "01_hook.jpg"],
        kicker="FEIL",
        headline=["FAQAT FEILIN SOʻZLARI", "SIZNI OGOHLANTIRADI"],
        sub=["Har bir soʻz — dalil. Har bir dalil — gʻalaba."],
    ),
    dict(
        key="s5",
        parts=["03_roles.jpg"],
        kicker="DALIL TOʻPLA",
        headline=["MAFIYANI USHLA"],
        sub=["Dalil toʻplab, mafiyani ushlang."],
    ),
    dict(
        key="s6",
        parts=["05_win.jpg", "02_gameplay.jpg"],
        kicker="TUNDA YOKI KUNDA",
        headline=["GʻALABA SENING", "QOʻLINGDA"],
        sub=["Everest Mafia — har kuni yangi oʻyin"],
    ),
    dict(
        key="s7",
        parts=["01_hook.jpg"],
        style="cta",
        headline=["EVEREST", "MAFIA"],
        sub=["Telegram guruhidagi mafiya oʻyini"],
        button="HOZIR OʻYNASH",
        link="t.me/everest_mafia_uzbekiston",
        note="Bot orqali oʻynang — bepul, oʻzbek tilida",
    ),
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


_DRAW = ImageDraw.Draw(Image.new("RGBA", (10, 10)))  # oʻlchov uchun


def cover(img: Image.Image, w: int, h: int) -> Image.Image:
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 1), int(ih * scale + 1)
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    return img.crop((left, top, left + w, top + h))


def scrim(img: Image.Image, strength: float = 1.0) -> Image.Image:
    """Yuqoridan pastga qoraytiruvchi gradient — matn oʻqilishi uchun."""
    w, h = img.size
    overlay = Image.new("L", (1, h))
    px = overlay.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = int(255 * min(1.0, (0.30 + (0.88 - 0.30) * (t ** 1.2)) * strength))
    return Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), img, overlay.resize((w, h)))


def vignette(img: Image.Image, amount: float = 0.55) -> Image.Image:
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((-w * 0.35, -h * 0.18, w * 1.35, h * 1.18), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=min(w, h) * 0.12))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.blend(img, Image.composite(img, dark, mask), amount)


def make_bg(name: str, w: int, h: int, out_path: str, mood: str = "normal") -> None:
    """Fon rasmni tayyorlab saqlaydi (qorongʻi kinematik koʻrinish)."""
    img = Image.open(os.path.join(FRAMES, name)).convert("RGB")
    img = cover(img, w, h)
    if mood == "cta":
        img = ImageEnhance.Brightness(img).enhance(0.55)
        img = ImageEnhance.Contrast(img).enhance(1.12)
        img = scrim(img, 1.15)
        img = vignette(img, 0.8)
    else:
        img = ImageEnhance.Brightness(img).enhance(0.70)
        img = ImageEnhance.Contrast(img).enhance(1.10)
        img = scrim(img, 1.0)
        img = vignette(img, 0.5)
    img.save(out_path, quality=94)


def tracked_width(draw: ImageDraw.ImageDraw, text: str, fnt, tracking: int) -> float:
    if not text:
        return 0
    return sum(draw.textlength(ch, font=fnt) for ch in text) + tracking * (len(text) - 1)


def text_layer(
    text: str,
    font_path: str,
    size: int,
    fill,
    tracking: int = 0,
    stroke: int = 0,
    stroke_fill=(0, 0, 0, 225),
    pad: int = 10,
    shadow: int = 0,
) -> Image.Image:
    """Alohida matn qatlami (shaffof PNG)."""
    fnt = font(font_path, size)
    tmp = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(tmp)
    width = int(tracked_width(d, text, fnt, tracking)) + pad * 2 + stroke * 2
    height = int(size * 1.42) + pad * 2 + stroke * 2
    layer = Image.new("RGBA", (max(1, width), max(1, height)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    x = pad + stroke
    y = pad + stroke + int(size * 0.12)
    for ch in text:
        if shadow:
            ld.text((x + shadow, y + shadow), ch, font=fnt, fill=(0, 0, 0, 160))
        ld.text(
            (x, y), ch, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill
        )
        x += ld.textlength(ch, font=fnt) + tracking
    return layer


def button_layer(label: str, size: int, w: int, h: int) -> Image.Image:
    """Qizil tugma (yumaloq burchakli) — RGBA."""
    fnt = font(SERIF_B, size)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=RED + (255,))
    d.rounded_rectangle((0, 0, w - 1, int(h * 0.5)), radius=h // 2, fill=RED_HOT + (70,))
    d.text((w // 2, h // 2), label, font=fnt, fill=WHITE + (255,), anchor="mm",
           stroke_width=1, stroke_fill=(90, 0, 0, 200))
    return layer


def glow_layer(w: int, h: int) -> Image.Image:
    """Tugma ortidagi qizil nur (pulsatsiyalanadi)."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = layer.load()
    cx, cy = w / 2, h / 2
    for y in range(h):
        for x in range(0, w, 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / (w / 2)
            a = max(0.0, 1.0 - d) ** 2
            v = int(150 * a)
            px[x, y] = (255, 40, 45, v)
            if x + 1 < w:
                px[x + 1, y] = (255, 40, 45, v)
    return layer.filter(ImageFilter.GaussianBlur(radius=w * 0.06))


def build_scene_layers(scene: dict, w: int, h: int, out_dir: str, duration: float) -> dict:
    """Sahnaning matn qatlamlarini yaratadi va manifest qismini qaytaradi."""
    key = scene["key"]
    os.makedirs(out_dir, exist_ok=True)
    layers: list[dict] = []
    side = int(w * 0.085)
    max_w = w - side * 2

    if scene.get("style") == "cta":
        head_f = font(SERIF_B, int(h * 0.070))
        sub_f = font(SERIF_I, int(h * 0.026))
        btn_f_size = int(h * 0.026)
        link_f = font(SERIF_B, int(h * 0.024))
        note_f = font(SERIF_I, int(h * 0.020))

        head_lines = scene["headline"]
        head_h = len(head_lines) * int(head_f.size * 1.16)
        block_top = int(h * 0.30)
        y = block_top

        # Yorqinlik (glow) — sarlavha ORTASIDA (matn rangini buzmasligi uchun avval)
        gw, gh = int(w * 0.95), int(h * 0.30)
        glow = glow_layer(gw, gh)
        glow.save(os.path.join(out_dir, f"{key}_glow.png"))
        layers.append(dict(file=f"{key}_glow.png", x=(w - gw) // 2, y=block_top - int(h * 0.10),
                           delay=0.0, kind="glow"))

        # Sarlavha qatlamlari
        for i, line in enumerate(head_lines):
            layer = text_layer(line, SERIF_B, int(h * 0.070), WHITE + (255,), stroke=3,
                               stroke_fill=(0, 0, 0, 220), pad=14, shadow=2)
            lx = (w - layer.width) // 2
            layers.append(dict(file=f"{key}_head{i}.png", x=lx, y=y, delay=None, kind="text"))
            layer.save(os.path.join(out_dir, f"{key}_head{i}.png"))
            y += int(h * 0.070) * 1.16

        # Tagʻ-alt (subtitle)
        sub = scene.get("sub", "")
        if sub:
            layer = text_layer(sub, SERIF_I, int(h * 0.026), DIM + (240,), stroke=2,
                               stroke_fill=(0, 0, 0, 210), pad=10)
            layers.append(dict(file=f"{key}_sub.png", x=(w - layer.width) // 2,
                               y=y + int(h * 0.02), delay=None, kind="text"))
            layer.save(os.path.join(out_dir, f"{key}_sub.png"))

        # Tugma
        btn_f = font(SERIF_B, btn_f_size)
        bw = int(_DRAW.textlength(scene["button"], font=btn_f)) + int(w * 0.16)
        bh = int(h * 0.055)
        bx = (w - bw) // 2
        by = y + int(h * 0.035) + int(h * 0.02)
        btn = button_layer(scene["button"], btn_f_size, bw, bh)
        btn.save(os.path.join(out_dir, f"{key}_btn.png"))
        layers.append(dict(file=f"{key}_btn.png", x=bx, y=by, delay=None, kind="text"))

        # Havola
        link = text_layer(scene["link"], SERIF_B, int(h * 0.024), WHITE + (255,), stroke=2,
                          stroke_fill=(0, 0, 0, 220), pad=10)
        link.save(os.path.join(out_dir, f"{key}_link.png"))
        layers.append(dict(file=f"{key}_link.png", x=(w - link.width) // 2,
                           y=by + bh + int(h * 0.022), delay=None, kind="text"))

        # Izoh
        note = text_layer(scene["note"], SERIF_I, int(h * 0.020), DIM + (225,), stroke=1,
                          stroke_fill=(0, 0, 0, 200), pad=8)
        note.save(os.path.join(out_dir, f"{key}_note.png"))
        layers.append(dict(file=f"{key}_note.png", x=(w - note.width) // 2,
                           y=by + bh + int(h * 0.062), delay=None, kind="text"))
    else:
        kick_f = font(SERIF_B, int(h * 0.0215))
        head_size = int(h * 0.058)
        sub_f = font(SERIF_I, int(h * 0.0255))

        # sarlavha shriftini sigʻadigan qilib moslashtiramiz
        head_lines = scene["headline"]
        while head_size > int(h * 0.030):
            f = font(SERIF_B, head_size)
            ok = all(_DRAW.textlength(l, font=f) <= max_w for l in head_lines)
            if ok:
                break
            head_size -= 3
        head_f = font(SERIF_B, head_size)
        line_h = int(head_size * 1.18)

        sub_blocks: list[dict] = []
        for s in scene.get("sub", []):
            if " · " in s:
                # roʻyxat — har bir element alohida ochiladi
                sub_blocks.append(dict(kind="row", items=[t.strip() for t in s.split(" · ")]))
            else:
                sub_blocks.append(dict(kind="lines", lines=_wrap(_DRAW, s, sub_f, max_w)))

        sub_line_h = int(sub_f.size * 1.32)
        # balandlik hisobi: roʻyxat satrlarini oldindan hisoblaymiz
        sub_row_count = 0
        for b in sub_blocks:
            if b["kind"] == "row":
                widths = [
                    text_layer(t, SERIF_I, int(h * 0.0255), DIM + (242,), stroke=2,
                               stroke_fill=(0, 0, 0, 205), pad=8).width
                    for t in b["items"]
                ]
                b["widths"] = widths
                b["rows"] = _chunk_row(widths, int(w * 0.035), max_w)
                sub_row_count += len(b["rows"])
            else:
                sub_row_count += len(b["lines"])

        block_h = (
            int(kick_f.size * 2.2)
            + len(head_lines) * line_h
            + int(h * 0.020)
            + sub_row_count * sub_line_h
        )
        bottom = int(h * 0.845)
        y = bottom - block_h

        # Kicker + qizil chiziq
        kick = text_layer(scene["kicker"], SERIF_B, int(h * 0.0215), RED_HOT + (255,), tracking=5,
                          stroke=2, stroke_fill=(0, 0, 0, 230), pad=8)
        kick.save(os.path.join(out_dir, f"{key}_kick.png"))
        layers.append(dict(file=f"{key}_kick.png", x=side, y=y, delay=None, kind="text"))
        bar_y = y + int(kick.height * 0.92)
        layers.append(dict(file=None, x=side, y=bar_y, w=int(kick.width * 0.55), h=4,
                           delay=None, kind="bar"))
        y += int(kick_f.size * 2.2)

        # Sarlavha
        for i, line in enumerate(head_lines):
            layer = text_layer(line, SERIF_B, head_size, WHITE + (255,), stroke=3,
                               stroke_fill=(0, 0, 0, 225), pad=12, shadow=2)
            layer.save(os.path.join(out_dir, f"{key}_head{i}.png"))
            layers.append(dict(file=f"{key}_head{i}.png", x=side, y=y, delay=None, kind="text"))
            y += line_h

        y += int(h * 0.018)
        # Tagʻ-alt
        gi = 0
        for block in sub_blocks:
            if block["kind"] == "lines":
                for line in block["lines"]:
                    layer = text_layer(line, SERIF_I, int(h * 0.0255), DIM + (242,), stroke=2,
                                       stroke_fill=(0, 0, 0, 205), pad=8)
                    layer.save(os.path.join(out_dir, f"{key}_sub{gi}.png"))
                    layers.append(dict(file=f"{key}_sub{gi}.png", x=side, y=y, delay=None, kind="text"))
                    gi += 1
                    y += sub_line_h
            else:
                # roʻyxat — qatorlab (kerak boʻlsa bir necha satrga), har biri alohida ochiladi
                gap = int(w * 0.035)
                widths = block["widths"]
                for row in block["rows"]:
                    x = side
                    for j in row:
                        layer = text_layer(block["items"][j], SERIF_I, int(h * 0.0255), DIM + (242,),
                                           stroke=2, stroke_fill=(0, 0, 0, 205), pad=8)
                        layer.save(os.path.join(out_dir, f"{key}_sub{gi}.png"))
                        layers.append(dict(file=f"{key}_sub{gi}.png", x=x, y=y, delay=None, kind="text"))
                        gi += 1
                        x += widths[j] + gap
                    y += sub_line_h

    # Qatlamlarning ochilish vaqti (sahna davomiyligiga moslashtiriladi)
    text_layers = [l for l in layers if l["kind"] == "text"]
    span = min(duration * 0.68, 2.8)   # uzun sahnalarda matn kechiktirilmaydi
    step = span / max(1, len(text_layers))
    for i, l in enumerate(text_layers):
        l["delay"] = round(0.06 + i * step, 3)
    for l in layers:
        if l["kind"] in ("bar", "glow"):
            l["delay"] = 0.10

    return dict(key=key, duration=round(duration, 3), layers=layers, style=scene.get("style", "stack"))


def _chunk_row(widths: list[int], gap: int, max_w: int) -> list[list[int]]:
    """Elementlarni sigʻadigan qatorlarga boʻlish (rol chiplari uchun)."""
    rows: list[list[int]] = []
    cur: list[int] = []
    cur_w = 0
    for i, w in enumerate(widths):
        add = w + (gap if cur else 0)
        if cur and cur_w + add > max_w:
            rows.append(cur)
            cur = [i]
            cur_w = w
        else:
            cur.append(i)
            cur_w += add
    if cur:
        rows.append(cur)
    return rows


def _wrap(draw, text: str, fnt, max_w: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines, cur = [], words[0]
    for word in words[1:]:
        trial = f"{cur} {word}"
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=["9x16", "4x5"], default="9x16")
    ap.add_argument("--durations", default=None, help="Sahna davomiyaliklari (JSON)")
    args = ap.parse_args()

    w, h = (1080, 1920) if args.format == "9x16" else (1080, 1350)
    out_dir = os.path.join(HERE, "build", "stills", args.format)
    os.makedirs(out_dir, exist_ok=True)

    durations = {}
    if args.durations and os.path.exists(args.durations):
        with open(args.durations) as f:
            durations = json.load(f)

    manifest = dict(width=w, height=h, fps=30, scenes=[])

    # Fon rasmlari
    bg_files: dict[str, str] = {}
    for scene in SCENES:
        for part in scene["parts"]:
            if part in bg_files:
                continue
            name = part.replace(".jpg", "")
            out = os.path.join(out_dir, f"bg_{name}.png")
            mood = "cta" if scene.get("style") == "cta" else "normal"
            make_bg(part, w, h, out, mood)
            bg_files[part] = f"bg_{name}.png"

    # Sahnalar
    for idx, scene in enumerate(SCENES):
        dur = float(durations.get(scene["key"], durations.get(str(idx), 3.0)))
        built = build_scene_layers(scene, w, h, out_dir, dur)

        # Kadrlar (qismlar) — davomiylik sahna boʻyicha teng taqsimlanadi
        parts = []
        if len(scene["parts"]) == 1:
            parts.append(dict(bg=bg_files[scene["parts"][0]], duration=round(dur, 3)))
        else:
            share = dur / len(scene["parts"])
            for i, p in enumerate(scene["parts"]):
                d = share if i < len(scene["parts"]) - 1 else dur - share * (len(scene["parts"]) - 1)
                parts.append(dict(bg=bg_files[p], duration=round(d, 3)))
        built["parts"] = parts
        manifest["scenes"].append(built)

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Cover — CTA sahnasining to'liq ko'rinishi
    cta = next(s for s in SCENES if s.get("style") == "cta")
    base = Image.open(os.path.join(out_dir, f"bg_{cta['parts'][0].replace('.jpg', '')}.png")).convert("RGBA")
    for entry in manifest["scenes"][-1]["layers"]:
        if entry["kind"] == "text" and entry.get("file"):
            layer = Image.open(os.path.join(out_dir, entry["file"])).convert("RGBA")
            base.alpha_composite(layer, (int(entry["x"]), int(entry["y"])))
    base.convert("RGB").save(os.path.join(out_dir, "cover.jpg"), quality=92)
    print(f"✓ {out_dir} — {len(manifest['scenes'])} sahna, manifest.json yozildi")


if __name__ == "__main__":
    main()
