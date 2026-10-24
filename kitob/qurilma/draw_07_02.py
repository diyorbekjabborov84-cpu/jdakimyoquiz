"""Original teaching figures for 7.2 "H2SO3 — sulfit kislota".

Barcha sonli egri chiziqlar — jadval ma'lumotlaridan olingan taxminiy hisoblar
(o'lchov ma'lumoti emas). Chizmalar original sxematik ishlanmalar.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

from prep_07_02 import (ASSETS as A, SALTS, LIMITS, MG_PER_PPM, M_SO2, M_H2SO3,
                        M_SO3, M_H2SO4, M_NAOH, M_CAOH2, M_CASO3, M_N2S2O5,
                        M_I2, M_THIO, M_O2, M_H2O, M_AIR,
                        BOND_R, BOND_ANGLE, BOND_R_SULFITE, ANGLE_SULFITE,
                        DIPOLE, IE, EA, DFH, DFG, S_STD, CP,
                        T_B, T_F, T_T, T_C, P_C, DH_VAP, RHO_LIQ, RHO_GAS_25,
                        KA1, KA2, KW, SOL_25, KH, H_HENRY,
                        ADI_SULFITE, FGD_WET, FGD_DRY, VOLCANIC_SO2,
                        US_CUT, US_2023, NAAQS_1H, NAAQS_SEC_ANNUAL,
                        ph_of, ph_series, speciation, saturated_solution,
                        sulfite_ion, vapor_pressure, vapor_pressure_table_25,
                        gas_density, henry_constant, iodometric,
                        neutralisation, equivalents, contact, air_load, num)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'
INK = '#243746'; RED = '#C0392B'; PURPLE = '#6C3483'; GREEN = '#2E7D4F'
BROWN = '#8C5A2B'; SULFUR = '#D4A017'


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


def n2(x, n=2):
    return ('%.*f' % (n, x)).replace('.', ',')


# --- Grafik 1: kislotalik va spetsiatsiya ------------------------------------
im, d = canvas('Kislotalik: SO₂(aq) / HSO₃⁻ / SO₃²⁻ ulushlari va [SO₃²⁻] (taxminiy hisob)', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(100, '100'), (75, '75'), (50, '50'), (25, '25'), (0, '0')]:
    txt(d, 8, 520 - v / 100.0 * 345 - 16, s, 22)
txt(d, 34, 108, 'ulush, %', 25)
for ph in range(0, 15, 2):
    x = 120 + ph / 14.0 * 560
    txt(d, x - 9, 526, str(ph), 16, G)
txt(d, 300, 548, 'pH', 23)
so2_pts, hso3_pts, so3_pts = [], [], []
for i in range(0, 57):
    ph = i * 0.25
    sp = speciation(ph)
    x = 120 + i / 56.0 * 560
    so2_pts.append((x, 520 - sp['so2'] / 100.0 * 345))
    hso3_pts.append((x, 520 - sp['hso3'] / 100.0 * 345))
    so3_pts.append((x, 520 - sp['so3'] / 100.0 * 345))
d.line(so2_pts, fill=N, width=4)
d.line(hso3_pts, fill=TEAL, width=4)
d.line(so3_pts, fill=B, width=4)
for ph, col, lab in [(1.81, RED, 'pK_a1 = 1,81'), (7.2, PURPLE, 'pK_a2 = 7,2')]:
    x = 120 + ph / 14.0 * 560
    for yy in range(175, 521, 18):
        d.line((x, yy, x, yy + 9), fill=col, width=2)
x1 = 120 + 1.81 / 14.0 * 560
x2 = 120 + 7.2 / 14.0 * 560
txt(d, x1 - 66, 150, 'pK_a1 = 1,81', 20, RED)
txt(d, x2 - 70, 122, 'pK_a2 = 7,2', 20, PURPLE)
d.ellipse((566, 316, 582, 332), fill=N); txt(d, 590, 310, 'SO₂(aq)', 21, INK)
d.ellipse((566, 352, 582, 368), fill=TEAL); txt(d, 590, 346, 'HSO₃⁻', 21, INK)
d.ellipse((566, 388, 582, 404), fill=B); txt(d, 590, 382, 'SO₃²⁻', 21, INK)
txt(d, 120, 578, 'Taxminiy hisob: pH 2 da SO₂ 39,4 %, HSO₃⁻ 60,6 %;  pH 7 da HSO₃⁻ 61,3 %, SO₃²⁻ 38,7 %', 20, INK)

d.line((120, 650, 120, 950, 680, 950), fill=G, width=3)
for lv, s in [('0', '0'), ('−2', '−2'), ('−4', '−4'), ('−6', '−6'), ('−8', '−8'), ('−10', '−10')]:
    lv = float(s.replace('−', '-'))
    txt(d, 2, 650 + (0 - lv) / 10.0 * 300 - 16, s, 21)
txt(d, 26, 612, 'lg[SO₃²⁻], mol/L', 22)
for ph in (1.0, 2.0, 4.0, 6.0, 8.0, 10.0):
    x = 120 + (ph - 1.0) / 9.0 * 560
    txt(d, x - 9, 956, num(ph, 0), 16, G)
txt(d, 336, 952, 'pH', 20, G)
pts = []
for i in range(0, 37):
    ph = 1.0 + i * 0.25
    lg = math.log10(sulfite_ion(1.000, ph))
    x = 120 + i / 36.0 * 560
    y = 650 + (0 - lg) / 10.0 * 300
    pts.append((x, y))
d.line(pts, fill=B, width=4)
for (x, y) in pts[::4]:
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=B, outline='#FFFFFF', width=2)
txt(d, 120, 988, '[SO₂(aq)] = 1,000 M;  [SO₃²⁻] = K_a2·[HSO₃⁻]/[H⁺] asosida', 21, N)
txt(d, 60, 1032, 'Sulfit ioni miqdori pH ga juda kuchli bog‘liq: pH 7 da ulushi 38,7 %, pH 10 da 99,8 %.', 20, INK)
txt(d, 60, 1082, 'K_a1 = 1,54×10⁻² (pK_a1 = 1,81);  K_a2 = 6,3×10⁻⁸ (pK_a2 = 7,2)', 21, G)
txt(d, 60, 1140, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
save(im, 'kislotalik')

# --- Grafik 2: fizik xossalar -------------------------------------------------
im, d = canvas('Fizik xossalar: bug‘ bosimi, gaz zichligi va fazalar (taxminiy hisob)', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]:
    txt(d, 8, 520 - v / 6.0 * 345 - 16, s, 22)
txt(d, 26, 110, 'p_sat, bar', 25)
for t in (190.0, 210.0, 230.0, 250.0, 270.0, 290.0, 310.0):
    x = 120 + (t - 185.0) / 130.0 * 560
    txt(d, x - 12, 526, num(t, 0), 16, G)
txt(d, 300, 548, 'T, K', 23)
pts = []
for i in range(0, 14):
    t = 185.0 + i * 10.0
    x = 120 + i / 13.0 * 560
    y = 520 - vapor_pressure(t) / 6.0 * 345
    pts.append((x, y))
d.line(pts, fill=N, width=4)
xb = 120 + (T_B - 185.0) / 130.0 * 560
yb = 520 - vapor_pressure(T_B) / 6.0 * 345
d.ellipse((xb - 8, yb - 8, xb + 8, yb + 8), fill=RED, outline='#FFFFFF', width=2)
txt(d, xb - 92, yb - 44, 'Tb = 263,15 K', 19, RED)
for t, p in [(283.15, 230.0), (293.15, 330.0), (303.15, 462.0)]:
    x = 120 + (t - 185.0) / 130.0 * 560
    y = 520 - (p / 101.325) / 6.0 * 345
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=TEAL, outline='#FFFFFF', width=2)
d.ellipse((486, 186, 502, 202), fill=N); txt(d, 510, 180, 'C–C egri chizig‘i', 21, INK)
d.ellipse((486, 216, 502, 232), fill=TEAL); txt(d, 510, 210, 'Jadval nuqtalari', 21, INK)
txt(d, 120, 578, 'Taxminiy hisob: p(25 °C) = 3,85 bar;  jadval interpolatsiyasi 390 kPa ≈ 3,85 bar (farq 0,01 %)', 20, INK)

d.line((120, 645, 120, 950, 680, 950), fill=G, width=3)
for v, s in [(2.4, '2,4'), (2.6, '2,6'), (2, '3,0'), (3.2, '3,2'), (3.4, '3,4'), (3.6, '3,6')]:
    val = float(s.replace(',', '.'))
    txt(d, 2, 950 - (val - 2.4) / 1.2 * 305 - 16, s, 21)
txt(d, 20, 600, 'ρ_gaz, g/L', 23)
pts = []
for i in range(7, 14):
    t = 185.0 + i * 10.0
    x = 120 + i / 13.0 * 560
    y = 950 - (gas_density(t) - 2.4) / 1.2 * 305
    pts.append((x, y))
d.line(pts, fill=BROWN, width=4)
for t, rho, lab, dy in [(273.15, gas_density(273.15), '2,858 g/L (0 °C)', -36), (298.15, gas_density(298.15), '2,618 g/L (25 °C)', 16)]:
    x = 120 + (t - 185.0) / 130.0 * 560
    y = 950 - (rho - 2.4) / 1.2 * 305
    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=BROWN, outline='#FFFFFF', width=2)
    txt(d, x - 100, y + dy, lab, 19, INK)
for t in (260.0, 280.0, 300.0):
    x = 120 + (t - 185.0) / 130.0 * 560
    txt(d, x - 12, 956, num(t, 0), 16, G)
txt(d, 336, 952, 'T, K', 20, G)
txt(d, 120, 976, 'M = 64,06 g/mol;  havo nisbati 64,06/28,965 ≈ 2,21 — havo ustida yig‘iladi', 21, N)
txt(d, 60, 1026, 'Suyuq SO₂ zichligi 1,434 g/mL;  Tf 200,75 K;  Tt 197,70 K;  Pc 78,79 bar;  Tc 430,80 K.', 20, INK)
txt(d, 60, 1080, 'ΔvapH = 24,90 kJ/mol;  SO₂ kislorodda yong‘inmaydi — +IV daraja.', 21, G)
txt(d, 60, 1140, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
save(im, 'fizik')

# --- Grafik 3: eritma --------------------------------------------------------
im, d = canvas('Suvli eritma: pH, dissotsiatsiya darajasi va to‘yingan holda (taxminiy hisob)', 1200)
cs = [0.001, 0.005, 0.010, 0.020, 0.050, 0.100, 0.200, 0.500, 1.000, 1.200, 1.4674]
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(2, '2'), (1, '1'), (0, '0')]:
    txt(d, 16, 520 - v / 2.0 * 345 - 16, s, 23)
txt(d, 40, 108, 'pH', 26)
txt(d, 250, 548, 'c, mol/L (chiziq teng intervalda)', 23)
pts = []
for i, c in enumerate(cs):
    p = ph_of(c)
    x = 120 + i * 50
    y = 520 - p['ph'] / 2.0 * 345
    pts.append((x, y))
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=B, outline='#FFFFFF', width=2)
d.line(pts, fill=B, width=4)
ss = saturated_solution()
xs = 120 + 10 * 50
ys = 520 - ss['ph'] / 2.0 * 345
d.ellipse((xs - 11, ys - 11, xs + 11, ys + 11), outline=RED, width=4)
txt(d, xs - 232, ys + 24, 'to‘yingan: c = 1,4674 M;  pH = 0,845', 19, RED)
txt(d, 120, 574, 'Kvadrat yechim:  h = (−K_a1 + √(K_a1² + 4K_a1·c))/2;  K_a1 = 1,54×10⁻²', 20, N)

d.line((120, 660, 120, 920, 680, 920), fill=G, width=3)
for v, s in [(0, '0'), (20, '20'), (40, '40'), (60, '60'), (80, '80')]:
    txt(d, 4, 920 - v / 80.0 * 260 - 16, s, 22)
txt(d, 24, 622, 'dissotsiatsiya, %', 23)
txt(d, 250, 940, 'c, mol/L (chiziq teng intervalda)', 22)
pts = []
for i, c in enumerate(cs):
    p = ph_of(c)
    x = 120 + i * 50
    y = 920 - p['pct'] / 80.0 * 260
    pts.append((x, y))
d.line(pts, fill=TEAL, width=4)
for (x, y) in pts:
    d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=TEAL, outline='#FFFFFF', width=2)
txt(d, 120, 972, 'Taxminiy hisob: 0,001 M → 69,0 %;  0,100 M → 32,3 %;  1,000 M → 11,7 % dissotsiatsiya', 20, N)
txt(d, 60, 1016, 'K_a1 katta bo‘lgani uchun sulfit kislota kuchsiz emas — to‘yingan eritma pH ≈ 0,85.', 20, INK)
txt(d, 60, 1066, 'S(25 °C) = 94 g/L;  k_H = 1,242 mol/(L·atm);  H = 0,805 atm·L/mol — manba qiymatlari', 20, G)
txt(d, 60, 1120, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
save(im, 'eritma')

# --- Grafik 4: tuzlar --------------------------------------------------------
im, d = canvas('Sulfit, bisulfit va metabisulfit: SO₂ mazmuni va molar massasi (taxminiy hisob)', 1200)
sel = [s for s in SALTS if s[0] in ('Natriy sulfit', 'Natriy bisulfit', 'Natriy metabisulfit',
                                    'Kalsiy sulfit', 'Kaliy sulfit')]
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(0, '0'), (20, '20'), (40, '40'), (60, '60'), (80, '80')]:
    txt(d, 4, 520 - v / 80.0 * 345 - 16, s, 22)
txt(d, 20, 110, 'SO₂ mazmuni, %', 24)
cols = [N, TEAL, B, BROWN, GREEN, PURPLE]
for i, (name, formula, m, ns, note, character) in enumerate(sel):
    so2 = M_SO2 * ns / m * 100.0
    x = 180 + i * 112
    h = so2 / 80.0 * 345
    d.rectangle((x - 40, 520 - h, x + 40, 520), fill=cols[i])
    txt(d, x - 40, 520 - h - 28, '%s %%' % n2(so2, 1), 19, INK)
    txt(d, x - 40, 534, formula, 17, G)
txt(d, 120, 578, 'Na₂SO₃ 50,8 %;  NaHSO₃ 61,6 %;  Na₂S₂O₅ 67,4 %;  CaSO₃ 53,3 %;  K₂SO₃ 40,5 %', 19, N)

d.line((120, 645, 120, 950, 680, 950), fill=G, width=3)
for v, s in [(0, '0'), (50, '50'), (100, '100'), (150, '150'), (200, '200')]:
    txt(d, 2, 950 - v / 200.0 * 305 - 16, s, 22)
txt(d, 26, 604, 'M, g/mol', 24)
for i, (name, formula, m, ns, note, character) in enumerate(sel):
    x = 180 + i * 112
    h = m / 200.0 * 305
    d.rectangle((x - 40, 950 - h, x + 40, 950), fill=cols[i])
    txt(d, x - 40, 950 - h - 28, n2(m, 2), 19, INK)
    txt(d, x - 40, 960, formula, 17, G)
txt(d, 120, 988, 'Sulfit ioni amfoter: K_b(SO₃²⁻) = 1,59×10⁻⁷ → Na₂SO₃ eritmasi alkalik, NaHSO₃ eritmasi kislik', 19, N)
txt(d, 60, 1012, '(NH₄)₂SO₃: SO₂ mazmuni 55,2 %, M = 116,14 g/mol;  ZnSO₃ — 44,0 %, M = 145,45 g/mol.', 19, INK)
txt(d, 60, 1060, 'Metabisulfit suvga tushganda:  Na₂S₂O₅ + H₂O → 2Na⁺ + 2HSO₃⁻ — u “quruq bisulfit” hisoblanadi.', 19, INK)
txt(d, 60, 1104, 'Oziq-ovqatda E220–E228;  EFSA 2016 bo‘yicha ADI 0,7 mg/kg tana vazni (SO₂ hisobida).', 19, G)
txt(d, 60, 1152, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 22, G)
save(im, 'tuzlar')

# --- Grafik 5: ekvivalent va neytralizatsiya ----------------------------------
im, d = canvas('Ekvivalent massa, tuzlarga aylantirish va kontakt usuli (taxminiy hisob)', 1240)
nn = neutralisation()
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(0, '0'), (40, '40'), (80, '80'), (120, '120'), (160, '160')]:
    txt(d, 2, 520 - v / 160.0 * 345 - 16, s, 22)
txt(d, 26, 108, 'kg', 25)
items = [('NaOH → NaHSO₃', nn['naoh_nahs3'], TEAL),
         ('NaOH → Na₂SO₃', nn['naoh_na2so3'], N),
         ('Ca(OH)₂', nn['caoh2'], BROWN),
         ('Na₂S₂O₅', nn['na2s2o5'], PURPLE),
         ('CaSO₃', nn['casao3'], GREEN)]
for i, (lab, val, col) in enumerate(items):
    x = 160 + i * 122
    h = val / 160.0 * 345
    d.rectangle((x - 44, 520 - h, x + 44, 520), fill=col)
    txt(d, x - 46, 520 - h - 28, '%s kg' % n2(val, 1), 18, INK)
    txt(d, x - 46, 538, lab, 15, G)
txt(d, 120, 578, '1000 kg 10 % li eritma (100,0 kg SO₂):  NaOH 62,4 / 124,9 kg;  Ca(OH)₂ 115,7 kg;  Na₂S₂O₅ 148,4 kg', 19, N)

cc = contact()
d.line((120, 635, 120, 900, 680, 900), fill=G, width=3)
for v, s in [(0, '0'), (400, '400'), (800, '800'), (1200, '1200'), (1600, '1600')]:
    txt(d, 2, 900 - v / 1600.0 * 265 - 16, s, 21)
txt(d, 30, 596, 'kg', 23)
bars = [('SO₃', cc['m_so3'], BROWN), ('O₂', cc['m_o2'], TEAL), ('H₂SO₄', cc['m_h2so4'], N)]
for i, (lab, val, col) in enumerate(bars):
    x = 230 + i * 210
    h = val / 1600.0 * 265
    d.rectangle((x - 55, 900 - h, x + 55, 900), fill=col)
    txt(d, x - 62, 900 - h - 28, '%s kg' % n2(val, 1), 19, INK)
    txt(d, x - 55, 918, lab, 20, G)
io = iodometric()
d.rounded_rectangle((40, 950, 700, 1060), radius=10, outline='#D6DFE7', width=2, fill='#FFFFFF')
txt(d, 60, 966, 'Yodometriya (Ripper):  25,00 mL 0,1000 M Na₂SO₃ → n = 0,002500 mol', 19, INK)
txt(d, 60, 1000, 'I₂ 0,6345 g;  Na₂S₂O₃ 1,2409 g', 19, TEAL)
txt(d, 60, 1030, 'Ekvivalent massa:  82,08/2 = 41,04 g/eq (kislota);  64,06/2 = 32,03 g/eq (redoks)', 19, INK)
txt(d, 60, 1100, 'Kontakt usuli:  2SO₂ + O₂ → 2SO₃;  SO₃ + H₂O → H₂SO₄;  moddiy balans −0,09 kg.', 20, INK)
txt(d, 60, 1150, 'Taxminiy hisob; o‘lchov ma’lumoti emas. Dozalar bo‘yicha tavsiya 12-bo‘limda.', 20, G)
save(im, 'ekvivalent')


# --- Sxemalar ----------------------------------------------------------------
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


scheme('fizikx', 'Fizik xossalar va agregat holatlari (sxematik)', [
    ('Qaynash va suyuqlash', 'Tb 263,15 K (−10,0 °C);  Tf 200,75 K (−72,4 °C)', 'Burchakli molekula; quyuq ammozaga yaqin'),
    ('Kritik nuqta', 'Tc 430,80 K;  Pc 78,79 bar;  ρsuyuq = 1,434 g/mL', 'Bu nuqtadan yuqorida suyuqlash mumkin emas'),
    ('Bug‘ bosimi', 'Taxminiy hisob: p(25 °C) = 3,85 bar (ΔvapH = 24,90 kJ/mol)', 'Jadval interpolatsiyasi 390 kPa — farq 0,01 %'),
    ('Termik barqarorlik', '1000 °C gacha deyarli parchalanmaydi', 'Kislorodli muhitda ayniqsa barqaror'),
    ('Suyuq SO₂ — erituvchi', 'Oltingugurt va organik moddalarni eritadi', 'Ekstraksiya va muzlatish vositasi')])

scheme('eritmax', 'Suvli eritma: Henry muvozanati, klathrat va korroziya (sxematik)', [
    ('Eruvchanlik', 'S(25 °C) = 94 g/L → c = 1,4674 mol/L', 'Vazn bo‘yicha 8,5 % (25 °C)'),
    ('Henry qonuni', 'k_H = 1,242 mol/(L·atm);  H = p/c = 0,805 atm·L/mol', 'Taxminiy hisob: 1 atm da 79,6 g/L'),
    ('Kislotalik', 'Taxminiy hisob: h = 0,1428 M;  pH = 0,845;  α = 9,7 %', 'K_a1 = 1,54×10⁻² — “apparent” qiymat'),
    ('Klathrat kristalli', '4SO₂·23H₂O;  7 °C dan yuqorida buziladi', 'Suvdagi SO₂ ni barqarorlashtiradi'),
    ('Korroziya', 'Kislik xossasi tufayli metall bilan reaksiyaga kiradi', 'Idish materiali tanlash amaliyot chegarasida')])

scheme('gidratx', 'Gidratatsiya, klathrat va dissotsiatsiya zanjiri (sxematik)', [
    ('Gaz fazi', 'SO₂ molekulasi: burchak 119,47°;  r(S=O) = 143,10 pm', 'ΔfH°(g) = −296,81 kJ/mol'),
    ('Gidratatsiya', 'SO₂(g) + H₂O ⇌ H₂SO₃(aq)   (κ ≪ 10⁻⁹)', 'ΔfH = −285,8 kJ/mol;  entropiya yo‘qotishi katta'),
    ('Dissotsiatsiya', 'SO₂(aq) + H₂O ⇌ H⁺ + HSO₃⁻', 'K_a1 = 1,54×10⁻²;  pK_a1 = 1,81'),
    ('Ikkinchi bosqich', 'HSO₃⁻ ⇌ H⁺ + SO₃²⁻', 'K_a2 = 6,3×10⁻⁸;  pK_a2 = 7,2'),
    ('Klathrat', '4SO₂·23H₂O kristalli (7 °C dan yuqorida buziladi)', '2024-yilda H₂SO₃ atmosferada aniqlangan')])

scheme('redoksx', 'Redoks xossalari: Latimer, Frost va adduktlar (sxematik)', [
    ('Latimer (kislik muhit)', 'SO₄²⁻ (+0,17 V) → SO₂ (+0,45 V) → S (+0,14 V) → H₂S', 'Sulfit kislota kuchli qaytaruvchi'),
    ('Latimer (asosiy muhit)', 'SO₄²⁻/SO₃²⁻ ≈ −0,93 V', 'Asosiy muhitda kuchli zaiflashadi'),
    ('Frost diagrammasi', 'nE° ning oksidlanish darajasi bo‘yicha grafigi', 'Barqarorlikni bir qarashda ko‘rsatadi'),
    ('Yod bilan oksidlanish', 'H₂SO₃ + I₂ + H₂O → H₂SO₄ + 2HI', 'Yodometrik tahlilning asosi'),
    ('Bisulfit addukti', 'Bisulfit + aldehyd ⇌ α-gidroksisulfonat', 'K = 10²–10⁶ M⁻¹;  vino “bog‘langan” SO₂')])

scheme('tuzlarx', 'Sulfit oilasi: tuzlar ierarxiyasi va qo‘llanilishi (sxematik)', [
    ('Sulfit kislota', 'Suvda SO₂(aq) / HSO₃⁻ / SO₃²⁻', 'Beqaror — saqlanmaydi'),
    ('Oddiy sulfitlar', 'Na₂SO₃, K₂SO₃, (NH₄)₂SO₃, CaSO₃', 'Alkalin eritma; kengaytirish va oqilash'),
    ('Bisulfitlar', 'NaHSO₃;  kalsiy bisulfit faqat eritmada', 'Kislik eritma; addukt hosil qiladi'),
    ('Metabisulfitlar', 'Na₂S₂O₅ — “quruq bisulfit”', 'Suvda 2HSO₃⁻ beradi; quruq saqlanadi'),
    ('Oziq-ovqat va tibbiyot', 'E220–E228;  ADI 0,7 mg/kg (EFSA, 2016)', 'Sezgirlik: astma kuchayishi kuzatiladi')])

scheme('tahlilx', 'Tahlil usullari: yodometriya, distillatsiya va spektrofotometriya (sxematik)', [
    ('Ripper (yodometrik)', '1892: SO₃²⁻ + I₂ + H₂O → SO₄²⁻ + 2I⁻ + 2H⁺', 'Ish diapazoni 3–100 mg/L; sezgirlik ~10 mg/L'),
    ('Monier–Williams', '1927: distillatsiya + H₂O₂ oksidlanishi + NaOH titrlash', 'Sekin, lekin spetsifik'),
    ('West–Gaeke', '1956: Na₂HgCl₄ tortish + pararosanilin-formaldehid; 560 nm', 'Atmosfera SO₂ si uchun 0,005–5 ppm'),
    ('Zamonaviy usullar', 'Oqim usullari, ion xromatografiyasi, elektrokimyoviy sensorlar', 'Tez va avtomatlashtirilgan'),
    ('Gravimetrik usul', 'Sulfitni sulfatgacha oksidlab BaSO₄ cho‘qmasini o‘lchash', 'Eng ishonchli, eng sekin')])

scheme('xavfsizlikx', 'Xavfsizlik chegaralari, monitoring va ekologiya (sxematik)', [
    ('Kasb chegaralari', 'OSHA PEL 5 ppm;  NIOSH REL 2/5 ppm;  ACGIH STEL 0,25 ppm', '1 ppm ≈ 2,62 mg/m³'),
    ('Hayot uchun xavfli daraja', 'IDLH 100 ppm', 'Daraja oshganda zudlik bilan evakuatsiya'),
    ('Favqulodda holat chegaralari', 'ERPG 0,3 / 3 / 25 ppm;  AEGL 0,2 / 0,75 / 30 ppm', 'Reaksion javoblar va avariya ssenariylari'),
    ('Ta’sir mexanizmi', 'Bronxospazm (astma);  shilliq qatlamda kislota hosil bo‘lishi', 'Suyuq SO₂ — teri muzlatishi'),
    ('Ekologik ta’sir', 'Kislik yomg‘iri;  stratosferada alyuminiy sulfat aerozoli', 'FGD: nam skrubber 92–99 %;  gips chiqindisi')])


# --- Original illyustratsiyalar ------------------------------------------------
im, d = canvas('SO₂ molekulasi, HSO₃⁻ va SO₃²⁻ tuzilmasi (sxematik)', 800)
cx, cy = 250, 290
half = math.radians(BOND_ANGLE / 2.0)
for sgn in (-1, 1):
    ax = cx + sgn * 74 * math.sin(half)
    ay = cy + 74 * math.cos(half)
    d.line((cx, cy, ax, ay), fill=N, width=8)
    d.ellipse((ax - 32, ay - 32, ax + 32, ay + 32), fill='#FFFFFF', outline=N, width=4)
    txt(d, ax - 11, ay - 17, 'O', 28, N)
d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), fill=SULFUR, outline=BROWN, width=4)
txt(d, cx - 16, cy - 22, 'S', 38, '#FFFFFF')
for k in range(2):
    px = cx - 16 + 12 * k
    py = cy - 58 + 10 * k
    d.ellipse((px - 8, py - 8, px + 8, py + 8), fill=G)
d.arc((cx - 100, cy - 100, cx + 100, cy + 100), 40, 140, fill=RED, width=4)
txt(d, 128, 392, '∠OSO = 119,47°', 21, RED)
txt(d, 500, 150, 'HSO₃⁻', 24, TEAL)
txt(d, 500, 196, 'H–SO₃⁻ (C_s)', 19, INK)
txt(d, 500, 228, 'proton oltingugurtda', 18, G)
txt(d, 500, 262, 'SO₃²⁻', 24, B)
txt(d, 500, 308, 'piramida, C₃ᵥ', 19, INK)
txt(d, 500, 340, '∠O–S–O ≈ 106°', 18, G)
txt(d, 500, 372, 'r(S–O) ≈ 151 pm', 18, G)
txt(d, 60, 130, 'r(S=O) = 143,10 pm', 23, INK)
txt(d, 60, 168, 'μ = 1,63 D;  IE = 12,30 eV', 23, INK)
txt(d, 60, 200, 'S atomida 1 erkin elektron jufti', 21, G)
txt(d, 60, 440, 'ΔfH°(g) = −296,81 kJ/mol;  ΔfG° = −300,09 kJ/mol', 22, INK)
txt(d, 60, 478, 'S° = 248,223 J/(mol·K);  C_p = 39,84 J/(mol·K)', 22, INK)
d.rectangle((60, 530, 700, 596), fill='#EAF2F8')
txt(d, 78, 542, '¹⁷O NMR:  [H–OSO₂]⁻ ⇌ [H–SO₃]⁻ — eritmada ikki izomer.', 20, N)
txt(d, 78, 570, 'H₂SO₃ molekulasi gaz fazida 1988-yilda, atmosferada 2024-yilda aniqlangan.', 19, N)
txt(d, 60, 640, 'Original sxematik chizma; o‘lchamlar shartli.', 21, G)
txt(d, 60, 684, 'Atom radiusi va bog‘ uzunligi shartli masshtabda berilgan.', 21, G)
txt(d, 60, 736, 'Ramka, rang va geometriya — o‘quv materiali; o‘lchov ma’lumoti emas.', 20, G)
save(im, 'molekulax')

im, d = canvas('Sulfit kislota olish yo‘llari va tuzlarga o‘tish (sxematik)', 800)
cols = [('LABORATORIYA', TEAL, ['S + O₂ → SO₂',
                                 'Na₂SO₃ + 2HCl → SO₂↑',
                                 '4FeS₂ + 11O₂ → 8SO₂']),
        ('TABIIY JARAYON', GREEN, ['Vulkan gazlari, fumarol',
                                   'Ko‘mir va neft yonish',
                                   'Sulfidli chang va eritmalar']),
        ('SANOAT', BROWN, ['Kontakt usuli bilan SO₂',
                           'SO₂ + NaOH → NaHSO₃',
                           'Na₂S₂O₅ — “quruq bisulfit”'])]
for i, (head, col, rows) in enumerate(cols):
    x = 34 + i * 232
    d.rounded_rectangle((x, 150, x + 214, 570), radius=12, outline=col, width=4)
    d.rectangle((x, 150, x + 214, 206), fill=col)
    txt(d, x + 22, 164, head, 22, '#FFFFFF')
    for j, r in enumerate(rows):
        y = 228 + j * 108
        d.rounded_rectangle((x + 12, y, x + 202, y + 88), radius=10,
                            outline='#D6DFE7', width=2, fill='#FFFFFF')
        txt(d, x + 22, y + 14, r, 18, INK)
        d.ellipse((x + 22, y + 58, x + 36, y + 72), fill=col)
        if j < len(rows) - 1:
            txt(d, x + 96, y + 86, '↓', 22, G)
txt(d, 40, 600, 'Kislota beqaror bo‘lgani uchun amalda uning tuzlari ishlatiladi.', 20, N)
txt(d, 40, 640, 'H₂S + SO₂ + suv → polissulfidlar: “Vakenroder eritmasi”.', 20, INK)
txt(d, 40, 690, 'Original sxematik chizma; bloklar shartli, parametrlar berilmagan.', 20, G)
txt(d, 40, 732, 'Qurilma, idish tanlash va dozalar bo‘yicha tavsiya 12-bo‘limda.', 20, G)
save(im, 'hosilax')

im, d = canvas('Tabiiy va sanoat manbalari: atmosferaga SO₂ chiqishi (sxematik)', 800)
d.rectangle((40, 150, 700, 290), outline=N, width=4)
d.polygon([(110, 290), (190, 180), (270, 290)], fill='#D8E8DC')
d.ellipse((170, 200, 210, 240), fill=RED)
txt(d, 92, 158, 'VULKAN', 22, INK)
txt(d, 300, 168, 'Fumarol, krater va magma degazashi', 20, INK)
txt(d, 300, 198, '20–25 mln t/y SO₂ (NASA ma’lumotlari)', 19, G)
txt(d, 300, 230, 'Tabiiy eng katta manba', 19, G)
d.rectangle((40, 310, 700, 450), outline=N, width=4)
d.rectangle((70, 340, 150, 450), fill='#8C5A2B')
d.rectangle((112, 322, 192, 450), fill='#6E4A22')
txt(d, 210, 328, 'KO‘MIR VA NEFT YONISH', 22, INK)
txt(d, 210, 360, 'Antropogen chiqarishning 45–50 %', 20, INK)
txt(d, 210, 390, 'Elektr stansiyalari, metallurgiya', 19, G)
txt(d, 210, 420, 'AQShda 1995–2023 yillarda −95 %', 19, G)
d.rectangle((40, 470, 700, 610), outline=N, width=4)
txt(d, 64, 486, 'SANOAT VA TABIIY CHIQINDILAR', 22, INK)
txt(d, 64, 520, 'Sulfidli chang va eritmalar;  neft konlari', 20, INK)
txt(d, 64, 552, 'Kontsentratsiyalar va texnik usullar berilmaydi', 19, G)
txt(d, 64, 582, 'Kislik yomg‘iri manbalari: 70 Tg(S)/y yoqilma, 7–8 Tg(S)/y vulqon', 19, G)
txt(d, 40, 660, 'Original sxematik chizma; miqdorlar yillik baholash.', 20, G)
txt(d, 40, 702, 'Manbalar: NASA (vulkan SO₂), EPA (chiqarishlar va FGD), IPCC ma’lumotlari.', 19, G)
txt(d, 40, 752, 'Mahalliy sharoitlarning ta’siri kuchli — ko‘rsatkichlar o‘rtacha baholash.', 19, G)
save(im, 'tabiiyx')

im, d = canvas('Sulfit tuzlari: kristall tuzilmasi va “quruq bisulfit” (sxematik)', 800)
boxes = [('Na₂SO₃', 'Natriy sulfit', 'SO₂ 50,8 %;  M = 126,04', TEAL),
         ('NaHSO₃', 'Natriy bisulfit', 'SO₂ 61,6 %;  M = 104,06', N),
         ('Na₂S₂O₅', 'Natriy metabisulfit', 'SO₂ 67,4 %;  M = 190,10', B),
         ('CaSO₃', 'Kalsiy sulfit', 'SO₂ 53,3 %;  M = 120,14', BROWN)]
for i, (f, name, note, col) in enumerate(boxes):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 170, x + 160, 350), radius=12, outline=col, width=4)
    d.rectangle((x + 30, 188, x + 130, 248), fill=col)
    txt(d, x + 42, 202, f, 24, '#FFFFFF')
    txt(d, x + 8, 268, name, 18, INK)
    txt(d, x + 4, 298, note, 17, G)
    for k in range(4):
        d.rectangle((x + 40 + 22 * k, 320, x + 54 + 22 * k, 336), fill=col)
txt(d, 40, 396, 'Tuz kristallari shartli chizilgan; haqiqiy tuzilma anionning koordinatsiyasiga bog‘liq.', 19, N)
txt(d, 40, 440, 'Metabisulfit suvda oddiy tuzdek emas:  Na₂S₂O₅ + H₂O → 2Na⁺ + 2HSO₃⁻.', 20, B)
txt(d, 40, 486, 'Sulfit ioni amfoter: natriy sulfit eritmasi alkalik, bisulfit eritmasi kislik.', 20, INK)
txt(d, 40, 530, 'Tuzlar sulfit kislotaning barqaror “zaxirasi”: quritilgan holda saqlanadi.', 20, INK)
d.rectangle((40, 570, 700, 636), fill='#EAF2F8')
txt(d, 58, 582, 'Oziq-ovqatda E220–E228;  EFSA 2016 bo‘yicha ADI 0,7 mg/kg tana vazni.', 19, N)
txt(d, 58, 610, 'Sezgirlik: astma kuchayishi kuzatiladi;  yorlikda nomlash majburiy.', 19, INK)
txt(d, 40, 686, 'Original sxematik chizma; kristall o‘lchamlari shartli.', 20, G)
txt(d, 40, 730, 'Retsept, doza va konsentratsiya bo‘yicha tavsiya berilmaydi.', 20, G)
save(im, 'tuzlarilx')

im, d = canvas('Kontakt usuli va nam skrubber: SO₂ dan sulfat kislotagacha (sxematik)', 860)
stages = [('1 — YONDIRISH', 'S + O₂ → SO₂   (yoki ruda kuydirish)', 'Ko‘mir va oltingugurt; 800–1000 °C', RED),
          ('2 — KONTAKT REAKTOR', '2SO₂ + O₂ ⇌ 2SO₃', 'V₂O₅ / Pt katalizatori;  400–450 °C', TEAL),
          ('3 — GIDRATLANISH', 'SO₃ + H₂O → H₂SO₄', 'Absorberda;  sulfat kislota 7.3–7.4-bo‘lim', BROWN)]
for i, (head, rxn, cond, col) in enumerate(stages):
    y = 140 + i * 175
    d.rounded_rectangle((40, y, 470, y + 140), radius=12, outline=col, width=4)
    txt(d, 62, y + 12, head, 23, col)
    txt(d, 62, y + 48, rxn, 20, INK)
    txt(d, 62, y + 84, cond, 18, G)
    if i < 2:
        txt(d, 240, y + 144, '↓', 30, B)
d.rounded_rectangle((500, 140, 720, 300), radius=12, outline=N, width=4)
txt(d, 520, 156, 'SO₃', 23, N)
txt(d, 520, 196, 'SO₃ 1249,8 kg', 19, INK)
txt(d, 520, 226, '(1000 kg SO₂ dan)', 18, G)
txt(d, 520, 258, 'O₂ 249,8 kg', 19, INK)
d.rounded_rectangle((500, 330, 720, 490), radius=12, outline=G, width=4)
txt(d, 520, 346, 'NAM SKRUBBER', 22, G)
txt(d, 520, 386, 'Olindi: 92–99 %', 19, INK)
txt(d, 520, 416, 'Xomashyo: CaCO₃', 18, G)
txt(d, 520, 444, 'Chiqindi: gips', 18, G)
d.line((470, 430, 500, 430), fill=G, width=3)
txt(d, 40, 664, 'FGD: dunyo quvvatining ~79 % i nam skrubber;  quruq usullar 50–95 % beradi.', 20, INK)
txt(d, 40, 700, 'AQShda elektr stansiyalarining SO₂ chiqarilishi 1995–2023 yillarda 95 % ga kamaygan.', 19, INK)
txt(d, 40, 748, 'Original sxematik chizma; oqim sxemasi shartli; apparat parametrlari berilmagan.', 19, G)
save(im, 'zavodx')

print('17 PNG yozildi:', A)
for f in sorted(A.glob('*.png')):
    print('  ', f.name)
