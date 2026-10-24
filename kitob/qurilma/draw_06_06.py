"""Original teaching figures for 6.6 "Taqqoslash" (vodorod galogenid kislotalari).

All curves are taxminiy hisob outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

from prep_06_06 import (ASSETS as A, KEYS, BY_KEY, ph_series, ph_at, metal_demand,
                        halogen_from_acid, oxygen_oxidation, neutralisation_demand,
                        acid_equivalents, salt_rows, complex_stability, thermal_rows,
                        E_REDUX, M_X2)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'; INK = '#243746'
RED = '#C0392B'; PURPLE = '#6C3483'; GREEN = '#2E7D4F'; BROWN = '#8C5A2B'

HAL_SYMBOL = {'HF': 'F', 'HCl': 'Cl', 'HBr': 'Br', 'HI': 'I'}
GAS_DH = {'HF': 1555.0, 'HCl': 1395.0, 'HBr': 1349.0, 'HI': 1313.0}
GAS_DG = {'HF': 1530.0, 'HCl': 1377.0, 'HBr': 1328.0, 'HI': 1297.0}
ATOM_COLOR = {'HF': '#EAF2F8', 'HCl': '#DCEBF4', 'HBr': '#D8E8DC', 'HI': '#F3E3D3'}
HAL_COLOR = {'HF': TEAL, 'HCl': GREEN, 'HBr': BROWN, 'HI': PURPLE}


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


def num(s):
    return str(s).replace('.', ',')


# --- Graph 1: kislotalik (suv, DMSO, gaz fazi) -------------------------------
im, d = canvas('Kislotalik: suv, DMSO va gaz fazidagi o‘lchovlar', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(15, '15'), (5, '5'), (0, '0'), (-5, '−5'), (-10, '−10')]:
    txt(d, 16, 175 + (15 - v) / 30.0 * 345 - 16, s, 23)
txt(d, 30, 110, 'pK_a', 26)
pts1, pts2 = [], []
for i, k in enumerate(KEYS):
    a = BY_KEY[k]
    x = 130 + i * 155
    y1 = 175 + (15 - a['pka']) / 30.0 * 345
    y2 = 175 + (15 - a['pka_dmso']) / 30.0 * 345
    pts1.append((x, y1)); pts2.append((x, y2))
    d.ellipse((x - 7, y1 - 7, x + 7, y1 + 7), fill=RED, outline='#FFFFFF', width=2)
    d.ellipse((x - 7, y2 - 7, x + 7, y2 + 7), fill=TEAL, outline='#FFFFFF', width=2)
    txt(d, x - 14, 538, k, 24, INK)
d.line(pts1, fill=RED, width=4)
d.line(pts2, fill=TEAL, width=4)
d.ellipse((470, 190, 486, 206), fill=RED); txt(d, 494, 184, 'pK_a (suv)', 21, RED)
d.ellipse((470, 228, 486, 244), fill=TEAL); txt(d, 494, 222, 'pK_a (DMSO)', 21, TEAL)
txt(d, 120, 578, 'Gaz fazi: HX(g) → H⁺(g) + X⁻(g) deprotonatsiya entalpisi', 23, INK)
txt(d, 30, 632, 'ΔH_acid, kJ/mol', 23)
d.line((120, 665, 120, 950, 680, 950), fill=G, width=3)
for v, s in [(1600, '1600'), (1450, '1450'), (1300, '1300')]:
    txt(d, 10, 665 + (1600 - v) / 350.0 * 285 - 16, s, 22)
for i, k in enumerate(KEYS):
    x = 130 + i * 155
    h = (GAS_DH[k] - 1250) / 350.0 * 285
    d.rectangle((x - 36, 950 - h, x + 36, 950), fill=HAL_COLOR[k])
    txt(d, x - 40, 950 - h - 28, '%d' % GAS_DH[k], 19, INK)
    txt(d, x - 14, 968, k, 22, G)
txt(d, 60, 1020, 'Gaz fazida ham tartib o‘zgarilmaydi: HF 1555 > HCl 1395 > HBr 1349 > HI 1313 kJ/mol', 21, N)
txt(d, 60, 1070, 'Kichik ΔH_acid — kuchli kislota; bu yerda faqat H–X bog‘i o‘lchovchi.', 21, B)
txt(d, 60, 1140, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
save(im, 'kislotalik')

# --- Graph 2: fizik xossalar --------------------------------------------------
im, d = canvas('Fizik xossalar: qaynash, suyuqlash va molekula o‘lchami', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(40, '40'), (0, '0'), (-40, '−40'), (-80, '−80'), (-120, '−120')]:
    txt(d, 8, 175 + (40 - v) / 170.0 * 345 - 16, s, 22)
txt(d, 30, 110, 'harorat, °C', 24)
for i, k in enumerate(KEYS):
    a = BY_KEY[k]
    x = 130 + i * 155
    for j, (v, col) in enumerate([(a['tb'], HAL_COLOR[k]), (a['tm'], N)]):
        y = 175 + (40 - v) / 170.0 * 345
        d.ellipse((x - 22 + j * 46, y - 12, x + 22 + j * 46, y + 12), fill=col)
    txt(d, x - 14, 538, k, 24, INK)
d.ellipse((470, 190, 486, 206), fill=N); txt(d, 494, 184, 'qaynash (Tb)', 21, INK)
d.ellipse((470, 228, 486, 244), fill=HAL_COLOR['HF']); txt(d, 494, 222, 'suyuqlash (Tm)', 21, INK)
d.line((120, 600, 680, 600), fill=G, width=2)
txt(d, 120, 620, 'Bog‘ uzunligi va dipol moment', 23, INK)
d.line((120, 690, 120, 950, 680, 950), fill=G, width=3)
for v, s in [(0, '0'), (0, '0'), (0, '0'), (0, '0')]:
    pass
for v, s in [(0, '0'), (0.5, '0,5'), (1.0, '1,0'), (1.5, '1,5'), (2.0, '2,0')]:
    txt(d, 10, 690 + (2.0 - v) / 2.0 * 260 - 16, s, 22)
txt(d, 26, 650, 'μ, D', 23)
pts = []
for i, k in enumerate(KEYS):
    a = BY_KEY[k]
    x = 130 + i * 155
    y = 690 + (2.0 - a['mu']) / 2.0 * 260
    pts.append((x, y))
    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=B, outline='#FFFFFF', width=2)
    d.rectangle((x - 30, 950, x + 30, 950 + (a['rexp'] - 0.9) / 0.75 * 60),
                fill=ATOM_COLOR[k], outline=N, width=2)
    txt(d, x - 34, 950 + (a['rexp'] - 0.9) / 0.75 * 60 + 8,
        '%s Å' % num('%.3f' % a['rexp']), 17, INK)
d.line(pts, fill=B, width=4)
txt(d, 60, 1045, 'r(H–X): 0,917; 1,2746; 1,414; 1,609 Å  —  molekula kattalashadi', 21, N)
txt(d, 60, 1090, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
save(im, 'fizik')

# --- Graph 3: pH ga bog‘liqlik -----------------------------------------------
im, d = canvas('Suvli eritma: pH ning konsentratsiyaga bog‘liqligi', 1200)
d.line((120, 175, 120, 560, 680, 560), fill=G, width=3)
for v, s in [(0, '0'), (1, '1'), (2, '2'), (3, '3')]:
    txt(d, 16, 560 - v / 4.0 * 385 - 16, s, 23)
txt(d, 40, 108, 'pH', 26)
pts_hf = []
for i, c in enumerate([0.0005, 0.001, 0.002, 0.005, 0.010, 0.020, 0.050, 0.100, 0.200,
                        0.500, 1.000, 2.000]):
    p = ph_at('HF', c)
    x = 120 + i * 50
    y = 560 - p['ph'] / 4.0 * 385
    pts_hf.append((x, y))
d.line(pts_hf, fill=B, width=5)
for (x, y), c in zip(pts_hf, [0.0005, 0.001, 0.002, 0.005, 0.010, 0.020, 0.050, 0.100,
                              0.200, 0.500, 1.000, 2.000]):
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=B, outline='#FFFFFF', width=2)
txt(d, 300, 590, 'c, mol/L (log o‘lchak; chiziq teng intervalda)', 23)
for k, col in [('HCl', GREEN), ('HBr', BROWN), ('HI', PURPLE)]:
    pts = []
    for i, c in enumerate([0.001, 0.002, 0.005, 0.010, 0.020, 0.050, 0.100, 0.200,
                           0.500, 1.000, 2.000]):
        p = ph_at(k, c)
        x = 120 + i * 50
        y = 560 - p['ph'] / 4.0 * 385
        pts.append((x, y))
    d.line(pts, fill=col, width=3)
    txt(d, 640, 190 + 30 * ['HCl', 'HBr', 'HI'].index(k), '%s (pH = −lg c)' % k, 21, col)
d.ellipse((470, 660, 486, 676), fill=B); txt(d, 494, 654, 'HF — kvadrat yechim', 21, B)
d.line((120, 700, 680, 700), fill=G, width=2)
txt(d, 120, 720, 'HF dissotsiatsiya darajasi (taxminiy hisob)', 23, INK)
d.line((120, 780, 120, 1000, 680, 1000), fill=G, width=3)
for v, s in [(0, '0'), (10, '10'), (20, '20'), (30, '30')]:
    txt(d, 8, 1000 - v / 30.0 * 220 - 16, s, 22)
txt(d, 40, 745, 'α, %', 23)
pts = []
for i, c in enumerate([0.001, 0.002, 0.005, 0.010, 0.020, 0.050, 0.100, 0.200, 0.500,
                        1.000, 2.000]):
    p = ph_at('HF', c)
    x = 120 + i * 50
    y = 1000 - p['pct'] / 30.0 * 220
    pts.append((x, y))
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=TEAL, outline='#FFFFFF', width=2)
d.line(pts, fill=TEAL, width=4)
txt(d, 60, 1040, '0,010 M → 22,90 %;  0,100 M → 7,91 %;  1,000 M → 2,57 %  (taxminiy hisob)', 21, N)
txt(d, 60, 1090, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
save(im, 'eritma')

# --- Graph 4: metall va halogen ----------------------------------------------
im, d = canvas('Metall talabi va halogen ajratish (shartli hisob)', 1240)
md = {x['key']: x for x in metal_demand(1.0)}
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]:
    txt(d, 16, 520 - v / 5.0 * 345 - 16, s, 23)
txt(d, 30, 108, 'kislota sarfi, g (1 g Fe uchun)', 25)
for i, k in enumerate(KEYS):
    x = 150 + i * 155
    h = md[k]['m_acid'] / 5.0 * 345
    d.rectangle((x - 40, 520 - h, x + 40, 520), fill=HAL_COLOR[k])
    txt(d, x - 44, 520 - h - 28, '%s g' % num('%.3f' % md[k]['m_acid']), 19, INK)
    txt(d, x - 22, 538, k, 24, G)
    txt(d, x - 46, 568, '%s g' % num('%.3f' % md[k]['m_salt']), 17, G)
txt(d, 120, 610, 'taxminiy hisob: 1 g Fe → tuz FeF₂ 1,680 g;  FeCl₂ 2,270 g;  FeBr₂ 3,861 g;  FeI₂ 5,545 g', 21, N)
d.line((120, 655, 680, 655), fill=G, width=2)
txt(d, 120, 675, '1000 kg kislotadan ajratiladigan X₂ (taxminiy hisob)', 23, INK)
d.line((120, 735, 120, 1010, 680, 1010), fill=G, width=3)
for v, s in [(0, '0'), (400, '400'), (800, '800'), (1000, '1000')]:
    txt(d, 4, 1010 - v / 1000.0 * 275 - 16, s, 22)
txt(d, 40, 700, 'kg', 23)
hg = {h['key']: h for h in halogen_from_acid(1000.0)}
for i, k in enumerate(KEYS):
    x = 150 + i * 155
    h = hg[k]['m_x2'] / 1000.0 * 275
    if h > 0:
        d.rectangle((x - 40, 1010 - h, x + 40, 1010), fill=HAL_COLOR[k])
        txt(d, x - 44, 1010 - h - 28, '%s kg' % num('%.1f' % hg[k]['m_x2']), 19, INK)
    else:
        d.rectangle((x - 40, 1010 - 6, x + 40, 1010), fill=RED)
        txt(d, x - 44, 970, '0 — F⁻ oksidlanmaydi', 18, RED)
    txt(d, x - 22, 1028, k, 24, G)
txt(d, 60, 1075, 'Taxminiy hisob chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'metall')

# --- Graph 5: ekvivalent va neytralizatsiya ----------------------------------
im, d = canvas('Ekvivalent va neytralizatsiya xarajati (shartli hisob)', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(0, '0'), (10, '10'), (20, '20'), (30, '30'), (40, '40'), (50, '50')]:
    txt(d, 10, 520 - v / 50.0 * 345 - 16, s, 23)
txt(d, 30, 108, 'H⁺ ekvivalenti, mol/kg', 25)
eq = {e['key']: e for e in acid_equivalents(1000.0)}
for i, k in enumerate(KEYS):
    x = 150 + i * 155
    h = eq[k]['eq_per_kg'] / 50.0 * 345
    d.rectangle((x - 40, 520 - h, x + 40, 520), fill=HAL_COLOR[k])
    txt(d, x - 44, 520 - h - 28, num('%.3f' % eq[k]['eq_per_kg']), 19, INK)
    txt(d, x - 22, 538, k, 24, G)
txt(d, 60, 580, 'Ekvivalent massa: HF 20,01;  HCl 36,46;  HBr 80,91;  HI 127,91 g/eq (taxminiy hisob)', 21, N)
d.line((120, 615, 680, 615), fill=G, width=2)
txt(d, 120, 635, '1000 kg 10 % li eritmaga neytrallash uchun Na₂CO₃ talabi (kg)', 23, INK)
d.line((120, 695, 120, 1010, 680, 1010), fill=G, width=3)
for v, s in [(0, '0'), (100, '100'), (200, '200'), (300, '300')]:
    txt(d, 4, 1010 - v / 300.0 * 315 - 16, s, 22)
txt(d, 40, 660, 'kg', 23)
nn = {n['key']: n for n in neutralisation_demand(1000.0, 10.0)}
for i, k in enumerate(KEYS):
    x = 150 + i * 155
    h = nn[k]['m_naco3'] / 300.0 * 315
    d.rectangle((x - 40, 1010 - h, x + 40, 1010), fill=HAL_COLOR[k])
    txt(d, x - 44, 1010 - h - 28, num('%.1f' % nn[k]['m_naco3']), 19, INK)
    txt(d, x - 22, 1028, k, 24, G)
txt(d, 60, 1075, 'Taxminiy hisob chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'ekvivalent')


# --- Sxemalar ---------------------------------------------------------------
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


scheme('organiksx', 'Organik kimyoga ta’sir (sxematik)', [
    ('Spirtdan galogenid', 'R–OH + HX → R–X + H₂O', 'Tartib: HI > HBr > HCl >> HF'),
    ('Alkil bromidi va iodidi', 'Keng qo‘llanadi; reagent sifatida qimmat', 'Laboratoriya va sanoat'),
    ('Alkil xloridi', 'Katalizator talab qiladi (ZnCl₂)', 'Zararli gaz ajralishi nazorat talab qiladi'),
    ('Eter kesish', 'R–O–R′ + HI → R–I + R′–OH', 'Faqat HI va HBr uchun'),
    ('Qaytarish va Cativa', 'ArNO₂ → ArNH₂;  CH₃OH + CO → CH₃COOH', 'HI — metanoldan siryaga katalizator')])

scheme('fizikx', 'Fizik xossalar va agregat holatlari (sxematik)', [
    ('Qaynash harorati', 'HF 19,5 °C;  HCl −85,1 °C;  HBr −66,8 °C;  HI −35,4 °C', 'Faqat HF xona haroratida suyuq'),
    ('Vodorod bog‘i zanjiri', 'Kichik F atomida kuchli zanjir', 'Kattaroq halogen — faqat dispersiya'),
    ('Azeotrop', 'HF 37,0 %;  HCl 20,2 %;  HBr 47,6 %;  HI 56,9 %', 'Oddiy distillatsiya bilan oshirib bo‘lmaydi'),
    ('Taxminiy hisob', 'c = w·ρ/M → 21,27; 6,11; 8,77; 7,56 mol/L', '1 L azeotrop: 426,0; 222,8; 710,0; 965,2 g'),
    ('Sanoat navi', 'HF 48 %;  HCl 37 %;  HBr 47,6 %;  HI 48–57 %', 'Konsentratsiya chegarasi')])

scheme('eritmax', 'Suvli eritma: dissotsiatsiya va pH (sxematik)', [
    ('Kuchli kislota', 'HCl, HBr, HI: [H₃O⁺] ≈ c', 'pH = −lg c; 0,100 M da pH 1,000'),
    ('Kuchsiz kislota', 'HF: h²/(c − h) = K_a (K_a = 6,8×10⁻⁴)', '0,100 M da α = 7,91 %, pH 2,102'),
    ('Konsentratsiyalangan HF', 'HF₂⁻ va H₂F⁺ hosil bo‘ladi', 'Oddiy kvadrat yechim yetarli bo‘lmaydi'),
    ('Apparent pH', 'Faolik koeffitsiyentlar 1 dan kichik', 'Termodinamik pH dan farqlanadi'),
    ('Titrlash va indikator', 'HF da keng pH sakrashi; kuchli kislotalarda tor', 'Metil zaytun — HF uchun')])

scheme('metallx', 'Metallarga ta’sir va passivatsiya (sxematik)', [
    ('Umumiy reaksiya', 'M + 2HX → MX₂ + H₂↑', 'Taxminiy hisob: 1 g Fe → H₂ 0,036 g'),
    ('Kislota talabi', 'HF 0,716 g;  HCl 1,306 g;  HBr 2,898 g;  HI 4,581 g', 'Kichik molekula — kamroq massa'),
    ('Passivatsiya', 'Faqat HF da: FeF₃ va CaF₂ qatlami', 'Qolgan kislotalarda himoya qatlami yo‘q'),
    ('Shisha bilan ishlash', 'HF: SiO₂ → H₂SiF₆ (shisha eriydi)', 'HCl, HBr, HI shishaga ta’sir qilmaydi'),
    ('Mis va vodorod', 'Mis uchun O₂ kerak; H₂ po‘latga sing‘adi', 'Embittlement — 12-bo‘lim')])

scheme('redoksx', 'Qaytaruvchilik va oksidlanish yo‘llari (sxematik)', [
    ('E°(X₂/2X⁻)', 'F 2,87;  Cl 1,36;  Br 1,07;  I 0,54 V', 'Qaytaruvchilik: F⁻ < Cl⁻ < Br⁻ < I⁻'),
    ('HF istisnosi', 'F⁻ oksidlanmaydi — F₂ olish mumkin emas', 'Guruhning eng barqaror anioni'),
    ('Havodan oksidlanish', 'Faqat HI: 4HI + O₂ → 2I₂ + 2H₂O', 'Taxminiy hisob: O₂ 62,5 kg / 1000 kg HI'),
    ('Kuchli oksidlovchi', 'HCl va HBr uchun MnO₂, KClO₃ kerak', 'Tuzlar: 2NaX + Cl₂ → 2NaCl + X₂'),
    ('Termik dekompozitsiya', '2HX ⇌ H₂ + X₂: ΔG° +550,8 → +15,9 kJ/mol', 'Termodinamik imkoniyat — kinetika emas')])

scheme('tuzlarx', 'Tuzlar, eruvchanlik va komplekslar (sxematik)', [
    ('Kumush halogenidlari', 'AgF eriydi (≈1,8 kg/L);  AgCl 1,8×10⁻¹⁰', 'AgBr 5,4×10⁻¹³;  AgI 8,3×10⁻¹⁷'),
    ('Cho‘qish kamayishi', 'AgF → AgCl → AgBr → AgI', 'Anion o‘lchami oshgani bilan izohlanadi'),
    ('Fluoridlar', 'CaF₂ 3,9×10⁻¹¹;  BaF₂ 1,7×10⁻⁶;  PbF₂ 3,7×10⁻⁸', 'CaF₂ deyarli erimaydi'),
    ('CaF₂ hosil bo‘lishi', 'CaCO₃ + 2HF → CaF₂↓ + CO₂ + H₂O', 'HF neytralizatsiyasining asosi'),
    ('Komplekslar', '[AgX₂]⁻;  [CuCl₄]²⁻;  [PtCl₆]²⁻;  [HgI₄]²⁻', 'Ligandlik: F⁻ < Cl⁻ < Br⁻ < I⁻')])

scheme('tahlilx', 'Tahlil usullari va xavfsizlik (sxematik)', [
    ('Standartlash', 'Na₂CO₃ yoki boraks bilan titrlash', 'Kuchli kislotalar uchun to‘g‘ri usul'),
    ('Gravimetriya', 'AgX cho‘kmasi quritilib o‘lchanadi', 'Barcha to‘rt kislota uchun umumiy'),
    ('Yodometriya', 'IO₃⁻ + 5I⁻ + 6H⁺ → 3I₂ + 3H₂O', 'Taxminiy hisob: 1,000 g KIO₃ → I₂ 0,712 g'),
    ('Zamonaviy usullar', 'Ion xromatografiya; ion-elektrod; ICP-OES/MS', 'F, Cl, Br, I aniqlanadi'),
    ('Xavfsizlik', 'HF IDLH 30 ppm;  HCl 50 ppm;  HBr va HI 35 ppm', 'HI: ICSC 1326 DANGER')])


# --- Original illustrasiyalar ------------------------------------------------
im, d = canvas('To‘rt kislota molekulalari (sxematik)', 700)
for i, k in enumerate(KEYS):
    a = BY_KEY[k]
    x = 95 + 175 * i
    r_x = 24 + 10 * i
    r_h = 20
    d.ellipse((x - r_x - r_h - 6, 200, x - r_x + r_h - 6, 200 + 2 * r_h),
              fill='#FFFFFF', outline=N, width=4)
    d.ellipse((x + r_x - r_h + 6, 200, x + r_x + r_h + 6, 200 + 2 * r_h),
              fill=ATOM_COLOR[k], outline=HAL_COLOR[k], width=4)
    d.line((x - r_x + r_h - 4, 200 + r_h, x + r_x - r_h + 4, 200 + r_h),
           fill=B, width=6)
    txt(d, x - r_x - r_h + 6, 206, 'H', 26, N)
    txt(d, x + r_x - r_h + 14, 206, HAL_SYMBOL[k], 24, HAL_COLOR[k])
    txt(d, x - 40, 268, k, 30, INK)
    txt(d, x - 46, 306, 'r = %s Å' % num('%.3f' % a['rexp']), 20, G)
    txt(d, x - 46, 336, 'D = %d kJ/mol' % a['d'], 20, G)
    txt(d, x - 46, 366, 'μ = %s D' % num('%.2f' % a['mu']), 20, G)
d.rectangle((60, 420, 700, 486), fill='#EAF2F8')
txt(d, 78, 432, 'Halogening o‘lchami oshgani sayin H–X bog‘i uzayadi va zaiflashadi.', 21, N)
txt(d, 60, 510, 'HF — guruhning eng qisqa va eng kuchli bog‘i; HI — eng uzun va eng zaif bog‘i.', 21, B)
txt(d, 60, 560, 'Kislotalik, qaytaruvchilik va termik barqarorlik shu bitta o‘zgarishdan kelib chiqadi.', 21, INK)
txt(d, 60, 630, 'Original sxematik chizma; atom o‘lchamlari shartli.', 21, G)
save(im, 'molekulax')

im, d = canvas('Kislotalik o‘lchovi: suv, DMSO va gaz fazi (sxematik)', 700)
d.rounded_rectangle((50, 150, 350, 470), radius=12, outline=N, width=4)
txt(d, 76, 166, 'SUV', 30, N)
for i, (lab, val, col) in enumerate([('HF', '3,17', TEAL), ('HCl', '−5,9', GREEN),
                                     ('HBr', '−8,8', BROWN), ('HI', '−9,5', PURPLE)]):
    y = 220 + i * 58
    d.ellipse((80, y, 108, y + 28), fill=col)
    txt(d, 124, y - 2, lab, 26, INK)
    txt(d, 210, y - 2, 'pK_a = ' + val, 24, INK)
d.rounded_rectangle((410, 150, 710, 470), radius=12, outline=N, width=4)
txt(d, 436, 166, 'GAZ FAZI', 30, N)
for i, (lab, val, col) in enumerate([('HF', '1555', TEAL), ('HCl', '1395', GREEN),
                                     ('HBr', '1349', BROWN), ('HI', '1313', PURPLE)]):
    y = 220 + i * 58
    d.ellipse((440, y, 468, y + 28), fill=col)
    txt(d, 484, y - 2, lab, 26, INK)
    txt(d, 570, y - 2, val, 24, INK)
txt(d, 76, 500, 'kJ/mol', 22, G)
txt(d, 436, 500, 'kJ/mol (ΔH_acid)', 22, G)
d.rectangle((50, 545, 710, 610), fill='#EAF2F8')
txt(d, 70, 558, 'Tartib ikkala o‘lchovda ham bir xil: HI eng kuchli, HF eng kuchsiz.', 21, N)
txt(d, 50, 635, 'Original sxematik chizma; qiymatlar manba jadvalidan.', 20, G)
save(im, 'teskarilanishx')

im, d = canvas('Idish materiallari va korroziya (sxematik)', 700)
boxes = [('HF', 'Shisha va plastik', 'CaF₂ qatlami', TEAL),
         ('HCl', 'Gummi va plastika', 'Anod korroziyasi', GREEN),
         ('HBr', 'Gummi, ko‘p qatlamli', 'Tez korroziya', BROWN),
         ('HI', 'Maxsus materiallar', 'Eng tez korroziya', PURPLE)]
for i, (a, b, c, col) in enumerate(boxes):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 170, x + 160, 330), radius=12, outline=col, width=4)
    d.ellipse((x + 52, 185, x + 108, 241), fill=col)
    txt(d, x + 66, 198, a, 30, '#FFFFFF')
    txt(d, x + 8, 262, b, 20, INK)
    txt(d, x + 6, 292, c, 18, G)
    if i < 3:
        d.line((x + 160, 250, x + 178, 250), fill=G, width=4)
txt(d, 40, 380, 'Tanlov mezonlari: reaktivlik, namlik, ifloslanish, idishning zichlikka chidami.', 21, N)
txt(d, 40, 425, 'HI bug‘lari havoga to‘planadi va teri uchun ayniqsa xavfli — idish yopiq bo‘lishi shart.', 20, B)
txt(d, 40, 480, 'Tanlov parametrlari konsentratsiya, miqdor va mahalliy qoidalarga bog‘liq.', 20, G)
txt(d, 40, 545, 'HF uchun CaF₂ qatlami metallni himoya qiladi; boshqalarda himoya qatlami yo‘q.', 20, INK)
txt(d, 40, 630, 'Original sxematik chizma; materiallar shartli.', 20, G)
save(im, 'idishx')

im, d = canvas('Xavfsizlik: bug‘ va namlanish (sxematik)', 700)
d.rectangle((60, 160, 700, 300), fill='#DCEBF4')
txt(d, 86, 176, 'xona havolari', 26, N)
d.rounded_rectangle((110, 200, 260, 285), radius=10, outline=N, width=4)
txt(d, 140, 225, 'HF', 32, TEAL)
d.rounded_rectangle((310, 200, 460, 285), radius=10, outline=N, width=4)
txt(d, 336, 225, 'HCl', 32, GREEN)
d.rounded_rectangle((510, 200, 660, 285), radius=10, outline=N, width=4)
txt(d, 530, 225, 'HI', 32, PURPLE)
for x in (185, 385, 585):
    d.line((x, 160, x, 118), fill=RED, width=4)
    txt(d, x - 60, 78, 'bug‘', 22, RED)
d.rectangle((60, 360, 700, 430), fill='#EAF2F8')
txt(d, 80, 375, 'Bug‘ havoga to‘planadi (HI eng og‘ir); nam namunalar qorayadi.', 21, N)
txt(d, 60, 460, 'Xavfsizlik chegaralari: HF IDLH 30 ppm;  HCl 50 ppm (tarixiy);  HBr va HI 35 ppm.', 20, B)
txt(d, 60, 510, 'HI uchun ICSC 1326 — DANGER; teri va ko‘zda kuchli kuyish, nafas tirikligi xavfi.', 20, INK)
txt(d, 60, 560, 'Shisha bilan ishlash HF uchun xalq bo‘lsa, HI bug‘i uchun — tortish tizimi talab qiladi.', 20, G)
txt(d, 60, 630, 'Original sxematik chizma; shakllar shartli.', 20, G)
save(im, 'xavfsizlikx')

im, d = canvas('Ishlangan hisob: besh shartli hisob (sxematik)', 850)
blocks = [('A — Metall talabi', '1 g Fe → kislota masasi', 'HF 0,716 g;  HCl 1,306 g;  HBr 2,898 g;  HI 4,581 g', N),
          ('B — Neytralizatsiya', '1000 kg 10 % li eritma + Na₂CO₃', '264,9; 145,3; 65,5; 41,4 kg (kirish = chiqish)', TEAL),
          ('C — Ekvivalent', 'H⁺ ekvivalenti, 1 kg kislotada', '49,985; 27,427; 12,359; 7,818 mol', B),
          ('D — Halogen ajratish', '1000 kg kislotadan X₂', 'Cl₂ 972,4;  Br₂ 987,5;  I₂ 992,1 kg;  HF uchun 0', PURPLE),
          ('E — Eritma pH', '0,100 M eritma', 'pH: HF 2,102;  HCl/HBr/HI 1,000', GREEN)]
for i, (a, b, cc, col) in enumerate(blocks):
    y = 130 + 118 * i
    d.rounded_rectangle((40, y, 468, y + 96), radius=12, outline=col, width=4)
    txt(d, 60, y + 8, a, 25, col)
    txt(d, 60, y + 40, b, 20, INK)
    txt(d, 60, y + 66, cc, 18, G)
d.rounded_rectangle((488, 130, 716, 560), radius=12, outline=G, width=4)
txt(d, 506, 148, 'Taxminiy hisob natijalari', 24, GREEN)
txt(d, 506, 200, 'pK_a 3,17 → −9,5', 20, INK)
txt(d, 506, 232, '(suvda, kuchli tomon)', 19, G)
txt(d, 506, 285, 'E° 2,87 → 0,54 V', 20, INK)
txt(d, 506, 317, '(qaytaruvchilik, teskari)', 19, G)
txt(d, 506, 370, 'AgI 8,3×10⁻¹⁷', 20, INK)
txt(d, 506, 402, '(eng oz eriydigan)', 19, G)
txt(d, 506, 455, 'ΔH_acid 1555 → 1313', 20, INK)
txt(d, 506, 487, '(kJ/mol, gaz fazi)', 19, G)
txt(d, 506, 530, 'K 0,254 — to‘liq konversiya emas', 17, G)
txt(d, 40, 740, 'Barcha sonlar ochiq shartli hisoblar; o‘lchov ma’lumoti emas.', 21, G)
txt(d, 40, 785, 'Shartli hisob chegarasi: faolik koeffitsiyentlar va havo namligi hisobga olinmagan.', 21, G)
save(im, 'hisob')
print('5 grafik; 7 sxema; 5 original illustration.')
