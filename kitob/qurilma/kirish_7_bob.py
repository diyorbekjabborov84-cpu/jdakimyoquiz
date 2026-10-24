#!/usr/bin/env python3
"""7-bob kirish (sarlavhali) rasmi: AI konsept-fon + tipografik qoplama.

6-bob kirish rasmi uslubiy referens: krem/navy/bronza kompozitsiya,
uparida kichik harfli sarlavha, ikki chiziq + olmos bezak, bob nomi,
mavzular ro'yxati va ingichka chiziqlar.

7-bob foni: oltingugurt kislotalari oilasi — bronza armaturali gaz
generatori, krem va amber rangli shisha idishlar, platina katalizatorli
kontakt quvuri, oltingugurt kristallari; chap yuqori qism bo'sh krem
(matn maydoni), pastki o'ngda jihozlar.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
RAS = ROOT / 'rasmlar'
FON = RAS / '7-bob-fon.png'
OUT = RAS / '7-bob-kirish-sarlavhali.png'
SH = RAS / 'shriftlar'

W, H = 1664, 2496
NAVY = (11, 44, 74)
BRONZE = (163, 116, 44)
RULE = (150, 138, 120)
F_TITLE = SH / 'playfair-display-latin-500-normal.ttf'
F_SMALL = SH / 'libre-baskerville-latin-400-normal.ttf'
F_NUM = SH / 'libre-baskerville-latin-400-normal.ttf'

PART = 'III QISM · ALOHIDA KISLOTALAR'
CHAP = '7-BOB'
TITLE = ['Oltingugurt', 'kislotalari']
SUB = 'BOB MAVZULARI'
TOPICS = [('7.1.', 'H₂S — vodorod sulfid'),
          ('7.2.', 'H₂SO₃ — sulfit kislota'),
          ('7.3.', 'H₂SO₄ — sulfat kislota (tuzilishi)'),
          ('7.4.', 'H₂SO₄ — xossalari'),
          ('7.5.', 'Kontakt usuli'),
          ('7.6.', 'Oleum va pirosulfat'),
          ('7.7.', 'Tiosulfat va peroksokislotalar')]

LIST_X0, LIST_X1 = 452, 1152
LIST_Y0, LIST_STEP = 946, 98


def spaced(d, xy, text, font, fill, track, anchor='mm'):
    """Harflar orasidagi kengaytirilgan matnni chizadi."""
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill, anchor='l' + anchor[1])
        x += w + track
    return total


def fit(d, text, path, size, max_w):
    while size > 20:
        f = ImageFont.truetype(str(path), size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(str(path), size)


SUBS = {'\u2082': '2', '\u2083': '3', '\u2084': '4'}


def measure_chem(d, text, font, size):
    """Kimyiy yorliq kengligi (pastki indekslar kichikroq hisobga olinadi)."""
    small = ImageFont.truetype(str(F_SMALL), max(10, int(size * 0.62)))
    total = 0.0
    for ch in text:
        if ch in SUBS:
            total += d.textlength(SUBS[ch], font=small)
        else:
            total += d.textlength(ch, font=font)
    return total


def fit_chem(d, text, path, size, max_w):
    while size > 18:
        f = ImageFont.truetype(str(path), size)
        if measure_chem(d, text, f, size) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(str(path), size)


def draw_chem(d, x, y, text, font, fill, size):
    """Kimyoiy shaklni kichik pastki indekslar bilan chizadi (bazal chiziqqa qarab)."""
    small = ImageFont.truetype(str(F_SMALL), max(10, int(size * 0.62)))
    base = y + int(size * 0.34)
    for ch in text:
        if ch in SUBS:
            d.text((x, base + int(size * 0.23)), SUBS[ch], font=small, fill=fill, anchor='ls')
            x += d.textlength(SUBS[ch], font=small)
        else:
            d.text((x, base), ch, font=font, fill=fill, anchor='ls')
            x += d.textlength(ch, font=font)
    return x


def diamond(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


def build_background(src):
    """Fonni kompozitsiyaga tayyorlaydi: 1024x1365 -> 1664x2496 (proportsiya saqlanadi)."""
    return src.resize((W, H), Image.LANCZOS)


def soft_patch(im, box, color=(255, 250, 240), alpha=118, blur=115):
    """Matn zonasi uchun yumshoq krem dog' (chiziqli, chegarasiz)."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle(box, fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')


def main():
    src = Image.open(FON).convert('RGB')
    im = build_background(src)

    # mavzular ro'yxati zonasi uchun yumshoq krem dog'
    im = soft_patch(im, (60, 890, 1240, 1600))
    d = ImageDraw.Draw(im)

    # yuqori qismda matn uchun yumshoq krem parda (6-bob uslubidagi yorug'lik)
    veil = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    for i in range(1300):
        if i <= 620:
            a = 104
        else:
            a = int(104 * (1 - (i - 620) / 680) ** 1.4)
        vd.rectangle((0, i, W, i + 1), fill=(255, 250, 240, a))
    im = Image.alpha_composite(im.convert('RGBA'), veil).convert('RGB')
    d = ImageDraw.Draw(im)

    # 1) qism sarlavhasi
    f_small = ImageFont.truetype(str(F_SMALL), 34)
    spaced(d, (W // 2, 131), PART, f_small, BRONZE, 7.5)
    # yuqori chiziq + olmos
    d.line((250, 184, 800, 184), fill=RULE, width=2)
    d.line((864, 184, 1414, 184), fill=RULE, width=2)
    diamond(d, 832, 184, 13, BRONZE)

    # 2) bob raqami
    f_chap = ImageFont.truetype(str(F_SMALL), 52)
    spaced(d, (W // 2, 322), CHAP, f_chap, BRONZE, 6.0)

    # 3) sarlavha (ikki qator)
    f_title = fit(d, TITLE[0], F_TITLE, 162, 1160)
    for i, line in enumerate(TITLE):
        y = 486 + i * 192
        d.text((W // 2 + 3, y + 3), line, font=f_title, fill=(255, 252, 246), anchor='mm')
        d.text((W // 2, y), line, font=f_title, fill=NAVY, anchor='mm')

    # 4) sarlavha ostidagi chiziq + olmos
    d.line((560, 782, 790, 782), fill=RULE, width=2)
    d.line((874, 782, 1104, 782), fill=RULE, width=2)
    diamond(d, 832, 782, 12, BRONZE)

    # 5) 'BOB MAVZULARI'
    f_sub = ImageFont.truetype(str(F_SMALL), 33)
    spaced(d, (W // 2, 856), SUB, f_sub, BRONZE, 7.0)

    # 6) mavzular ro'yxati — eng uzun yorliqqa sig'ishi uchun shrift moslashtiriladi
    longest = max(name for _, name in TOPICS)
    f_item = fit_chem(d, longest, F_SMALL, 42, LIST_X1 - (LIST_X0 + 104))
    size_item = f_item.size
    f_num = ImageFont.truetype(str(F_NUM), 40)
    y = LIST_Y0
    for num, name in TOPICS:
        d.text((LIST_X0, y), num, font=f_num, fill=BRONZE, anchor='lm')
        draw_chem(d, LIST_X0 + 104, y, name, f_item, NAVY, size_item)
        d.line((LIST_X0, y + 50, LIST_X1, y + 50), fill=(196, 186, 170), width=1)
        y += LIST_STEP

    im.save(OUT)
    print(OUT, im.size, '| mavzular:', len(TOPICS))


if __name__ == '__main__':
    main()
