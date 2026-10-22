#!/usr/bin/env python3
"""5-bob kirish (sarlavhali) rasmi: AI konsept-fon + tipografik qoplama.

4-bob kirish rasmi uslubiy referens: krem/navy/bronza kompozitsiya,
uparida kichik harfli sarlavha, ikki chiziq + olmos bezak, bob nomi,
mavzular ro'yxati va ingichka chiziqlar.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RAS = ROOT / 'rasmlar'
FON = RAS / '5-bob-fon.png'
OUT = RAS / '5-bob-kirish-sarlavhali.png'
SH = RAS / 'shriftlar'

W, H = 1664, 2496
NAVY = (11, 44, 74)
BRONZE = (163, 116, 44)
RULE = (150, 138, 120)
F_TITLE = SH / 'playfair-display-latin-500-normal.ttf'
F_SMALL = SH / 'libre-baskerville-latin-400-normal.ttf'
F_NUM = SH / 'libre-baskerville-latin-400-normal.ttf'

PART = 'II QISM · UMUMIY KIMYO'
CHAP = '5-BOB'
TITLE = ['Olish, tozalash,', 'konsentrlash']
SUB = 'BOB MAVZULARI'
TOPICS = [('5.1.', 'Olishning umumiy usullari'),
          ('5.2.', 'Tozalash'),
          ('5.3.', 'Quritish va suvsizlantirish'),
          ('5.4.', 'Sanoat prinsiplari')]


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


def diamond(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


def main():
    # fon: chap tomonni qisqartirib zoom — jihozlar o'ng pastki burchakka suriladi
    src = Image.open(FON).convert('RGB')
    bg = src.crop((0, 100, 844, 1366)).resize((W, H), Image.LANCZOS)
    im = bg.copy()
    d = ImageDraw.Draw(im)

    # yuqori qismda matn uchun yumshoq krem parda (4-bob uslubidagi yorug'lik)
    veil = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    for i in range(1050):
        a = int(115 * (1 - i / 1050) ** 1.6)
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
    f_title = fit(d, TITLE[0], F_TITLE, 160, 1180)
    for i, line in enumerate(TITLE):
        y = 478 + i * 190
        d.text((W // 2 + 3, y + 3), line, font=f_title, fill=(255, 252, 246), anchor='mm')
        d.text((W // 2, y), line, font=f_title, fill=NAVY, anchor='mm')

    # 4) sarlavha ostidagi chiziq + olmos
    d.line((560, 792, 790, 792), fill=RULE, width=2)
    d.line((874, 792, 1104, 792), fill=RULE, width=2)
    diamond(d, 832, 792, 12, BRONZE)

    # 5) 'BOB MAVZULARI'
    f_sub = ImageFont.truetype(str(F_SMALL), 33)
    spaced(d, (W // 2, 866), SUB, f_sub, BRONZE, 7.0)

    # 6) mavzular ro'yxati
    f_item = ImageFont.truetype(str(F_ITEM := F_SMALL), 42)
    f_num = ImageFont.truetype(str(F_NUM), 42)
    x0, x1 = 470, 1178
    y = 966
    for num, name in TOPICS:
        d.text((x0, y), num, font=f_num, fill=BRONZE, anchor='lm')
        d.text((x0 + 96, y), name, font=f_item, fill=NAVY, anchor='lm')
        d.line((x0, y + 50, x1, y + 50), fill=(196, 186, 170), width=1)
        y += 104

    im.save(OUT)
    print(OUT, im.size)


if __name__ == '__main__':
    main()
