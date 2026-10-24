"""Original teaching figures for 5.4 "Sanoat prinsiplari".
All curves are taxminiy hisob outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_05_04 import (ASSETS as A, chain_balance, economics, unit_cost,
                        STEAM, OPEX_MIX, OEE_A, OEE_P, OEE_Q, pinch_profile,
                        oxidation_heat, drying_heat)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'; INK = '#243746'
RED = '#C0392B'; PURPLE = '#6C3483'; GREEN = '#2E7D4F'


def font(n):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', n)


def txt(d, x, y, s, n=28, c=N):
    maxw = 760 - x - 12
    while n > 12 and d.textlength(s, font=font(n)) > maxw:
        n -= 1
    d.text((x, y), s, font=font(n), fill=c)


def canvas(s, h=1120):
    im = Image.new('RGB', (760, h), BG)
    d = ImageDraw.Draw(im)
    n = 32
    while d.textlength(s, font=font(n)) > 700:
        n -= 1
    txt(d, 30, 22, s, n)
    return im, d


def save(im, n):
    im.save(A / (n + '.png'))


def rows(name, numeric=True):
    out = []
    for r in csv.DictReader((A / (name + '.csv')).open()):
        if numeric:
            out.append({k: float(v) for k, v in r.items()})
        else:
            out.append({k: (float(v) if _num(v) else v) for k, v in r.items()})
    return out


def _num(v):
    try:
        float(v); return True
    except ValueError:
        return False


def axes(d, xlo, xhi, ylo, yhi, xlabel, ylabel, xt, yt, x0=120, x1=680, y0=175, y1=700):
    def p(x, y):
        return (x0 + (x - xlo) / (xhi - xlo) * (x1 - x0), y1 - (y - ylo) / (yhi - ylo) * (y1 - y0))
    d.line((x0, y0, x0, y1, x1, y1), fill=G, width=3)
    for x, s in xt:
        txt(d, p(x, ylo)[0] - 15, y1 + 18, s, 24)
    for y, s in yt:
        txt(d, 20, p(xlo, y)[1] - 16, s, 24)
    txt(d, 45, 108, ylabel, 28)
    txt(d, x0 + 25, y1 + 80, xlabel, 27)
    return p


# --- Graph 1: materiallar oqimi -----------------------------------------
im, d = canvas('Zanjir bo‘yicha materiallar oqimi', 880)
c = chain_balance()
items = [('N₂ (ortiqcha)', c['m_n2'], G), ('Toluen (aylanadi)', c['m_toluene'], B),
         ('O₂', c['m_o2'], TEAL), ('HNO₃ (68 %)', c['m_hno3'], N),
         ('Mahsulot (98 %)', c['m_final'], GREEN),
         ('Suv chiqarilgan', c['m_water_removed'], RED),
         ('NH₃', c['m_nh3'], PURPLE)]
mx = max(v for _, v, _ in items)
y = 175
for name, v, col in items:
    d.rectangle((250, y, 250 + v / mx * 400, y + 42), fill=col)
    txt(d, 30, y + 6, name, 23, INK)
    txt(d, 258 + v / mx * 400, y + 8, '%.2f kg' % v, 22, col)
    y += 62
txt(d, 45, 655, 'Taxminiy hisob: 1000 kg 68 % li HNO₃ eritmasi asosida', 24, N)
txt(d, 45, 700, 'HNO₃ 680,00 kg; NH₃ 183,80; O₂ 690,68; suv chiqarilgan 306,12 kg', 22, B)
txt(d, 45, 745, 'Konsentratsiya: distillat 1546,07 kg, toluen 1239,95 kg (aylanadi)', 22, G)
txt(d, 45, 790, 'Massa oqimi taxminiy hisobi; o‘lchov ma’lumoti emas', 23, G)
save(im, 'oqim')

# --- Graph 2: bug' darajalari --------------------------------------------
im, d = canvas('Bug‘ darajalari: bosim va harorat', 1180)
p = axes(d, 0, 8.5, 90, 305, 'qatnoq bug‘ bosimi, MPa', 'T, °C',
         [(0, '0'), (2, '2'), (4, '4'), (6, '6'), (8, '8')],
         [(100, '100'), (150, '150'), (200, '200'), (250, '250'), (300, '300')])
pts = [(pp, tt) for pp, tt, hh in STEAM]
d.line([p(x, y) for x, y in pts], fill=N, width=5)
for pp, tt, hh in STEAM:
    x, y = p(pp, tt)
    d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=B)
    txt(d, x + 14, y - 16, '%.2f MPa, %.1f °C' % (pp, tt), 21, B)
    txt(d, x + 14, y + 8, 'h_fg = %.0f kJ/kg' % hh, 20, G)
txt(d, 45, 865, 'Issiqlik integratsiyasi: yuqori daraja qizdiradi, past daraja bug‘latadi', 22, N)
txt(d, 45, 910, 'Bug‘latish entalpiyasi daraja oshganda kamayadi: 2257,5 → 1441,0 kJ/kg', 22, B)
txt(d, 45, 955, 'Bug‘ jadvali qiymatlari; taxminiy hisob sxemasida ishlatiladi', 22, G)
txt(d, 45, 1010, 'Bug‘ jadvali, CRC; o‘lchov ma’lumoti emas', 23, G)
save(im, 'bug')

# --- Graph 3: OPEX tarkibi ------------------------------------------------
im, d = canvas('Ekspluatatsiya xarajatlarining tarkibi', 1180)
p = axes(d, 0, 45, 0, 5, 'ulush, %', 'element', [(0, ''), (10, ''), (20, ''), (30, ''), (40, '')],
         [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
cols = [N, B, TEAL, G, PURPLE, GREEN, RED]
y = 0
for i, (name, pct) in enumerate(OPEX_MIX):
    x0 = p(0, y)[0] + 20
    x1 = p(pct, y)[0]
    d.rectangle((x0, y + 12, x1, y + 52), fill=cols[i % len(cols)])
    txt(d, x0 + 6, y + 20, name, 22, '#FFFFFF' if pct > 10 else INK)
    txt(d, x1 + 8, y + 22, '%d %%' % pct, 22, cols[i % len(cols)])
    y += 58
txt(d, 45, 640, 'Taxminiy hisob: umumiy ekspluatatsiya xarajati 420 USD/t (100 000 t/y zavod)', 22, N)
txt(d, 45, 690, 'Xom ashyo 42 %; energiya 26 %; ish kuchi 8 %; ta’minot 9 %', 22, B)
txt(d, 45, 735, 'Qurilma va IT 5 %; ekologik xarajatlar 6 %; boshqa 4 %', 22, G)
txt(d, 45, 790, 'Ular ulushi taxminiy hisobdan; real zavod ko‘rsatkichlari emas', 23, G)
save(im, 'opex')

# --- Graph 4: issiqlik integratsiyasi ------------------------------------
im, d = canvas('Issiqlik integratsiyasi: oqim va bug‘ darajalari', 1180)
# chap panel: bug' darajalari
ylab = [(0.10, 99.63), (1.00, 179.89), (4.00, 250.40), (8.00, 295.06)]


def ty(t):
    return 620 - t / 900.0 * 445


d.line((70, 175, 70, 620, 330, 620), fill=G, width=3)
txt(d, 20, 150, 'T, °C', 24, G)
for i, (p_mpa, t) in enumerate(ylab):
    y = ty(t)
    d.line((70, y, 300, y), fill='#9FB2C2', width=4)
    off = -32 if i % 2 == 0 else 10
    txt(d, 78, y + off, '%.2f MPa → %.1f °C' % (p_mpa, t), 20, TEAL)
txt(d, 40, 660, 'Qatnoq bug‘ darajalari', 23, N)
# o'ng panel: oqim profili
d.line((390, 175, 390, 620, 700, 620), fill=G, width=3)
txt(d, 340, 150, 'T, °C', 24, G)
stream, _ = pinch_profile()
pts = [(390 + i * 38, ty(t)) for i, (name, t) in enumerate(stream)]
d.line(pts, fill=N, width=5)
for i, ((name, t), (x, y)) in enumerate(zip(stream, pts), 1):
    d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=B, outline='#FFFFFF', width=2)
    txt(d, x - 8, y - 40, str(i), 19, B)
txt(d, 400, 660, 'Jarayon oqimi harorat profili', 23, N)
# legenda
short = {'NH₃ kirish': 'NH₃ kirish', 'Oksidlash reaktori': 'Oksidlash',
         'Issiq gaz': 'Issiq gaz', 'SO2/N2 tozalash': 'SO₂/N₂ tozalash',
         'Absorbsiya': 'Absorbsiya', 'Konsentratsiya': 'Konsentratsiya',
         'Azeotrop reabiler': 'Azeotrop reabiler', 'Kondenser': 'Kondenser',
         'Mahsulot': 'Mahsulot'}
for i, (name, t) in enumerate(stream):
    col = i % 2
    row = i // 2
    x = 40 + col * 370
    y = 700 + row * 32
    d.ellipse((x, y + 4, x + 18, y + 22), fill=B)
    txt(d, x + 6, y + 5, str(i + 1), 15, '#FFFFFF')
    txt(d, x + 26, y + 2, '%s — %d °C' % (short.get(name, name), t), 20)
txt(d, 40, 940, 'Taxminiy hisob: oqim harorat profili va bug‘ darajalari; pinch nuqtasi sxema bo‘yicha', 21, B)
txt(d, 40, 985, 'Issiqlik integratsiyasi: yuqori daraja qizdiradi, past daraja bug‘latadi', 21, N)
txt(d, 40, 1030, 'O‘lchov ma’lumoti emas', 22, G)
save(im, 'issiqlik')

# --- Graph 5: birlik FOA --------------------------------------------------
im, d = canvas('Birlik FOA va hajm bog‘liqligi', 1180)
p = axes(d, 0, 250000, 300, 560, 'quvvat, t/y', 'birlik narx, USD/t',
         [(0, '0'), (50000, '50k'), (100000, '100k'), (150000, '150k'), (200000, '200k'), (250000, '250k')],
         [(320, '320'), (400, '400'), (480, '480'), (560, '560')])
rr = rows('birlik_qiymat')
line = [(r['V_tpy'], r['c_total']) for r in rr]
d.line([p(x, y) for x, y in line], fill=N, width=5)
for x, y in line:
    px, py = p(x, y)
    d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=B)
yp = p(0, 560)[1]
d.line((120, yp, 680, yp), fill=RED, width=3)
txt(d, 470, yp - 34, 'bozor narxi 560 USD/t (shartli hisob)', 21, RED)
e = economics()
txt(d, 45, 830, 'c(V) = c_o‘z + FOA/V;  c_o‘z = 324 USD/t;  FOA = 9,60 mln USD/y', 23, N)
txt(d, 45, 875, '50 000 t/y → 516 USD/t;  100 000 → 420;  200 000 → 372 USD/t', 22, B)
txt(d, 45, 920, 'OEE = 0,92 × 0,95 × 0,99 = 0,8653 → savdo 86 526 t/y (shartli hisob)', 22, G)
txt(d, 45, 970, 'Shartli hisob egri chizig‘i; real narxlar emas', 23, G)
save(im, 'birlikqiymat')


# --- Sxemalar -------------------------------------------------------------
def scheme(name, title, boxes, h=None):
    h = h or (125 + 210 * len(boxes) + 70)
    im, d = canvas(title, h)
    for i, (s, a, b) in enumerate(boxes):
        y = 125 + 210 * i
        d.rounded_rectangle((32, y, 728, y + 160), radius=14, outline=N, width=3)
        txt(d, 52, y + 14, s, 30, B)
        txt(d, 52, y + 65, a, 26)
        txt(d, 52, y + 107, b, 25, G)
        if i < len(boxes) - 1:
            txt(d, 360, y + 165, '↓', 33, B)
    save(im, name)


scheme('sxematurlari', 'Texnologik sxemaning uch turi', [
    ('To‘g‘ridan-to‘g‘ri', 'Xom ashyo bir marta mahsulotga aylanadi', 'Orthiqcha modda chiqindi'),
    ('Oraliq mahsulotli', 'Avval oraliq modda ajratiladi', '5.2 tozalash bosqichi'),
    ('Yopiq (qaytma oqimli)', 'Modda mahsulotga yaqin qaytariladi', 'Reagent sarfi kamayadi'),
    ('Darajalar', 'Birinchi → ikkinchi → oxirgi', 'Boshqaruv hisoboti uchun'),
    ('Sxema — hujjat', 'Har bir oqim: nomi, miqdori, holati', 'Taxminiy hisob asosi')])

scheme('oqsxemasi', 'Oqim sxemasi: apparat va oqimlar (sxematik)', [
    ('Oksidlash reaktori', 'NH₃ + O₂ → NO + H₂O', 'Reaksion issig‘i qaytariladi'),
    ('Absorber', 'NO₂ + H₂O → HNO₃', '68 % li eritma'),
    ('Tozalash (5.2)', 'Cho‘ktirish, ion almashinuv', 'Metal iflosligi chiqariladi'),
    ('Konsentratsiya (5.3)', 'Azeotrop yoki bug‘latish', '98 % li mahsulot'),
    ('Qadoqlash', 'Sifat nazorati, partiya', 'Yuklash uchun tayyor')])

scheme('logistikax', 'Xom ashyo va mahsulot logistikasi', [
    ('Xom ashyo bazasi', 'Ammiak, katalizator, tozalovchi', 'Shartnoma va zaxira'),
    ('Transport', 'Tanker, konteyner, vagon', 'Masofa = xarajat va xavf'),
    ('Qabul va saqlash', 'Tank park, zaxira hajmi', 'Xotira = xavf zaxirasi'),
    ('Ishlab chiqarish', 'Zanjir: olish → tozalash → quritish', '5.1–5.3'),
    ('Yetkazib berish', 'Qadoqlash, transport, izchillik', 'Mijoz talabi')])

scheme('bugtizimi', 'Bug‘ va energiya tizimi (sxematik)', [
    ('Kotlovana', 'Bug‘ ishlab chiqarish', 'Turli daraja: 0,10–8,00 MPa'),
    ('Turbogenerator', 'Bug‘ → elektr', 'Elektr tarmog‘i'),
    ('WHR (qayta foydalanish)', 'Reaksion va gaz issig‘i', 'Bug‘ga aylantiriladi'),
    ('Reabiler / kondensor', 'Issiqlik integratsiyasi', 'Pinch nuqtasi'),
    ('Sarflash o‘lchagich', 'Bug‘ va elektr hisobi', 'Energiya balansi')])

scheme('inertlashsx', 'Inertlash va yonishdan himoya tizimi', [
    ('Oldini olish', 'Inertlash (N₂), qoldiq modda chiqarish', 'To‘g‘ri material tanlash'),
    ('Aniqlash', 'Gaz tarkibi, T va p chegaralari', 'On-line analizator'),
    ('Hamkorlikda', 'Avtomatik uzish, ventilyatsiya', 'Fail-safe tizim'),
    ('Quyilishdan himoya', 'Tag‘in (bund), to‘shama zaxirasi', 'Jarayon uzilishi'),
    ('Tekshiruv', 'Hodisa tahlili, audit', 'Xavf baholashni yangilash')])

scheme('chiqindisx', 'Chiqindilarni boshqarish sxemasi', [
    ('Gazlar', 'NOₓ, SO₂, HCl, VOC', 'Skrubber, katalitik redoks'),
    ('Suyuqlar', 'Kislotali quyimlar, og‘ir metallar', 'Neytralizatsiya, qayta ishlatish'),
    ('Qattiq', 'Katalizator, sital adsorbat', 'Regeneratsiya, qoldiq'),
    ('Miqdor kamaytirish', 'Qayta ishlatish → uzatish → yo‘qotish', 'Omil: 0,012 (shartli hisob)'),
    ('Hisobot', 'CO₂e, chiqindi omili, suv sarfi', 'ISO 14001')])

scheme('raqamlisx', 'Raqamli boshqaruv zanjiri', [
    ('Maydon', 'Sensorlar, on-line analizator', 'O‘lchov va signal'),
    ('Boshqaruv', 'PLC va DCS', 'Qaror, uzish, regulyatsiya'),
    ('Yuqori pog‘ona', 'MES va ERP', 'Reja, ta’minot, hisobot'),
    ('Ma’lumot tahlili', 'Soft sensor, raqamli egizin', 'Bashorat va trening'),
    ('Sifat', 'OEE, partiya, izchillik', 'ISO 22400-2, izchillik zanjiri')])


# --- Original illustrasiyalar ---------------------------------------------
def base(t, h=590):
    return canvas(t, h)


im, d = base('Materiallar: qoplama va korroziya qatlami (sxematik)')
d.rectangle((90, 160, 670, 210), fill='#DCEBF4')
txt(d, 120, 172, 'muhit (kislota)', 23, TEAL)
d.rectangle((90, 210, 670, 250), fill='#E4D2B0')
txt(d, 130, 220, 'himoya qatlami: PTFE, grafit, keramika', 22, INK)
d.rectangle((90, 250, 670, 300), fill='#C9D4DD')
txt(d, 120, 262, 'qotishma: 316L / 904L / Hastelloy', 22, INK)
d.rectangle((90, 300, 670, 360), fill=N)
txt(d, 130, 315, 'konstruktsiya po‘lati (karkas)', 22, '#FFFFFF')
d.rectangle((90, 360, 670, 400), fill='#EDE3D2')
txt(d, 140, 368, 'izolyatsiya', 22, INK)
txt(d, 35, 470, 'Sxematik kesim; material tanlash sharoitga bog‘liq', 22, G)
txt(d, 35, 520, 'Taxminiy hisob: korroziya tezligi 0,0012 g/(m²·soat) — o‘lchilgan qiymat', 21, G)
save(im, 'materiallar')

im, d = base('Xotira: tank park va uzluksizlik (sxematik)')
for i in range(3):
    x = 70 + i * 200
    d.rounded_rectangle((x, 200, x + 160, 380), radius=12, outline=N, width=4)
    txt(d, x + 30, 280, 'T-%d' % (i + 1), 26, N)
d.line((150, 380, 250, 440, 450, 440, 550, 380), fill=B, width=5)
txt(d, 300, 455, 'o‘lchov va boshqaruv', 22, B)
d.line((390, 120, 390, 195), fill=G, width=5)
d.polygon([(390, 195), (376, 170), (404, 170)], fill=G)
txt(d, 405, 120, 'xom ashyo', 22, G)
txt(d, 35, 510, 'Sxematik: xotira — uzluksiz ishlash va xavf zaxirasi', 22, G)
txt(d, 35, 555, 'Taxminiy hisob: quvvat 100 000 t/y; OEE 0,8653 → savdo 86 526 t/y', 21, G)
save(im, 'xotira')

im, d = base('Xavf boshqaruv zanjiri (sxematik)')
for i, (s, col) in enumerate([('Oldini olish', N), ('Aniqlash', B), ('Hamkorlikda', TEAL)]):
    x = 40 + i * 240
    d.rounded_rectangle((x, 220, x + 200, 330), radius=12, outline=col, width=4)
    txt(d, x + 28, 265, s, 25, col)
    if i < 2:
        txt(d, x + 205, 258, '→', 30, G)
txt(d, 40, 165, 'Xavf boshqaruv: uch qatlam', 26, N)
txt(d, 40, 390, 'Har bir qatlam alohida tekshiriladi; tizim butun sifatida baholanadi', 22, INK)
txt(d, 40, 440, 'Taxminiy hisob: oqibat × ehtimollik ro‘yxati; har o‘zgarishda qayta ko‘riladi', 21, G)
txt(d, 40, 495, 'Texnologik parametrlar berilmaydi', 22, RED)
save(im, 'xavf')

im, d = base('Izchillik (traceability) zanjiri (sxematik)')
labels = [('Xom ashyo\npartiyasi', N), ('Reaktiv\npartiyasi', B), ('Apparat', TEAL),
          ('Operator\nva sana', G), ('Tekshiruv\nnatijasi', PURPLE), ('Tayyor\nmahsulot', GREEN)]
x = 30
for i, (s, col) in enumerate(labels):
    d.rounded_rectangle((x, 230, x + 110, 340), radius=10, outline=col, width=4)
    parts = s.split('\n')
    txt(d, x + 12, 255, parts[0], 19, col)
    if len(parts) > 1:
        txt(d, x + 12, 285, parts[1], 19, col)
    if i < len(labels) - 1:
        txt(d, x + 110, 268, '→', 26, G)
    x += 122
txt(d, 40, 175, 'Elektron izchillik: xom ashyodan tayyor mahsulotgacha', 25, N)
txt(d, 40, 395, 'Muvaffaqiyatsizlik aniqlansa, butun partiya emas — tegishli partiya qaytariladi', 22, INK)
txt(d, 40, 450, 'Farmatsevtik xom ashyo uchun majburiy; reagent va elektron darajasida iqtisodiy ustuvorlik', 21, G)
txt(d, 40, 505, 'Taxminiy hisob sxema; tizimning aniq arxitekturasi korxonaga bog‘liq', 22, G)
save(im, 'izchillik')

im, d = base('Ishlangan hisob: zanjir va iqtisodiyot', 640)
c = chain_balance(); e = economics()
d.rounded_rectangle((30, 140, 350, 320), radius=12, outline=N, width=4)
txt(d, 55, 160, 'Taxmin A: zanjir balansi', 25, N)
txt(d, 55, 200, 'NH₃ 183,80 kg → HNO₃ 680,00 kg', 21, INK)
txt(d, 55, 232, 'Suv chiqarilgan 306,12 kg', 21, INK)
txt(d, 55, 264, 'Mahsulot 693,88 kg (98 %)', 21, INK)
txt(d, 55, 294, 'Reaksiya −4468,2 MJ; quritish 1203,1 MJ', 20, G)
d.rounded_rectangle((410, 140, 730, 320), radius=12, outline=B, width=4)
txt(d, 435, 160, 'Taxmin B: iqtisodiyot', 25, B)
txt(d, 435, 200, 'CAPEX 120,0 mln USD; FOA 96 USD/t', 21, INK)
txt(d, 435, 232, 'c_o‘z = 324 USD/t; c = 420 USD/t', 21, INK)
txt(d, 435, 264, 'OEE 0,8653 → 86 526 t/y', 21, INK)
txt(d, 435, 294, 'Marja 140 USD/t; qaytish 9,9 yil', 20, G)
d.rounded_rectangle((30, 360, 350, 490), radius=12, outline=TEAL, width=4)
txt(d, 60, 380, 'FOA/V: 50k→516; 100k→420; 200k→372', 21, TEAL)
txt(d, 60, 420, 'Birlik narx hajmga bog‘liq', 21, INK)
d.rounded_rectangle((410, 360, 730, 490), radius=12, outline=TEAL, width=4)
txt(d, 440, 380, 'Chiqindi omili, samaradorlik', 21, TEAL)
txt(d, 440, 420, 'To‘rt o‘lchak birga baholanadi', 21, INK)
txt(d, 40, 525, 'Shartli hisob zanjiri; o‘lchov ma’lumoti emas', 23, G)
txt(d, 40, 570, 'Texnologik parametrlar va texnologik retseptlar berilmaydi', 23, G)
save(im, 'hisob')

print('5 grafik + CSV; 7 sxema; 5 original illustration.')
