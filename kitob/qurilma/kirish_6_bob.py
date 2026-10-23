#!/usr/bin/env python3
"""6-bob kirish (sarlavhali) rasmi: AI konsept-fon + tipografik qoplama.

5-bob kirish rasmi uslubiy referens: krem/navy/bronza kompozitsiya,
uparida kichik harfli sarlavha, ikki chiziq + olmos bezak, bob nomi,
mavzular ro'yxati va ingichka chiziqlar.

6-bob foni: vodorod galogenidlarining oilasi — bronza armaturali to'rtta
shisha idishda F, Cl, Br, I ga xos ranglar (yashil, sariq-yashil, amber,
binafsha) va kristallar; chap yuqori qism bo'sh krem (matn maydoni).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
RAS = ROOT / 'rasmlar'
FON = RAS / '6-bob-fon.png'
OUT = RAS / '6-bob-kirish-sarlavhali.png'
SH = RAS / 'shriftlar'

W, H = 1664, 2496
NAVY = (11, 44, 74)
BRONZE = (163, 116, 44)
RULE = (150, 138, 120)
F_TITLE = SH / 'playfair-display-latin-500-normal.ttf'
F_SMALL = SH / 'libre-baskerville-latin-400-normal.ttf'
F_NUM = SH / 'libre-baskerville-latin-400-normal.ttf'

PART = 'III QISM · ALOHIDA KISLOTALAR'
CHAP = '6-BOB'
TITLE = ['Vodorod', 'galogenidlari']
SUB = 'BOB MAVZULARI'
TOPICS = [('6.1.', 'Guruhning umumiy tavsifi'),
          ('6.2.', 'HF — ftorid kislota'),
          ('6.3.', 'HCl — xlorid kislota'),
          ('6.4.', 'HBr — bromid kislota'),
          ('6.5.', 'HI — yodid kislota'),
          ('6.6.', 'Taqqoslash')]


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


def build_background(src):
    """Fonni kompozitsiyaga tayyorlaydi: chapdan kengaytirilgan krem maydon,
    pastki o'ngda galogen idishlari (4 ta: F, Cl, Br, I ranglari)."""
    # manba fonning yuqori qismi bo'sh krem; pastki o'ngda idishlar.
    # chapdan 114 px kesib, 910x1365 -> 1664x2496 (proportsiya saqlanadi).
    bg = src.crop((114, 0, src.width, src.height)).resize((W, H), Image.LANCZOS)
    return bg


def soft_patch(im, box, color=(255, 250, 240), alpha=132, blur=105):
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
    im = soft_patch(im, (40, 880, 1160, 1580))
    d = ImageDraw.Draw(im)

    # yuqori qismda matn uchun yumshoq krem parda (5-bob uslubidagi yorug'lik)
    veil = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    for i in range(1150):
        if i <= 640:
            a = 122
        else:
            a = int(122 * (1 - (i - 640) / 510) ** 1.4)
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
    f_title = fit(d, TITLE[0], F_TITLE, 168, 1180)
    for i, line in enumerate(TITLE):
        y = 492 + i * 196
        d.text((W // 2 + 3, y + 3), line, font=f_title, fill=(255, 252, 246), anchor='mm')
        d.text((W // 2, y), line, font=f_title, fill=NAVY, anchor='mm')

    # 4) sarlavha ostidagi chiziq + olmos
    d.line((560, 796, 790, 796), fill=RULE, width=2)
    d.line((874, 796, 1104, 796), fill=RULE, width=2)
    diamond(d, 832, 796, 12, BRONZE)

    # 5) 'BOB MAVZULARI'
    f_sub = ImageFont.truetype(str(F_SMALL), 33)
    spaced(d, (W // 2, 872), SUB, f_sub, BRONZE, 7.0)

    # 6) mavzular ro'yxati
    f_item = ImageFont.truetype(str(F_SMALL), 42)
    f_num = ImageFont.truetype(str(F_NUM), 42)
    x0, x1 = 450, 1078
    y = 968
    for num, name in TOPICS:
        d.text((x0, y), num, font=f_num, fill=BRONZE, anchor='lm')
        d.text((x0 + 96, y), name, font=f_item, fill=NAVY, anchor='lm')
        d.line((x0, y + 52, x1, y + 52), fill=(196, 186, 170), width=1)
        y += 104

    im.save(OUT)
    print(OUT, im.size)


if __name__ == '__main__':
    main()
