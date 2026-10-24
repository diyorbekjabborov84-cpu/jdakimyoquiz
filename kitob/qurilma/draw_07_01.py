"""Original teaching figures for 7.1 "H2S — vodorod sulfid".

Barcha sonli egri chiziqlar — jadval ma'lumotlaridan olingan taxminiy hisoblar
(o'lchov ma'lumotlari emas). Chizmalar original sxematik ishlanmalar.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

from prep_07_01 import (ASSETS as A, SULFIDES, LIMITS, MG_PER_PPM, M_H2S, M_AIR,
                        BOND_R, BOND_ANGLE, BOND_D, DIPOLE, IE, PA, DFH, DFG,
                        S_STD, CP, T_B, T_F, T_T, T_C, P_C, RHO_C, DH_VAP, P_25,
                        AUTOIGN, FLAM_LO, FLAM_HI, RHO_G_0, RHO_G_25,
                        KA1, KA2, SOL_20, SOL_10, SOL_25,
                        ph_of, ph_series, speciation, saturated_solution,
                        sulfide_ion, vapor_pressure, gas_density, henry_constant,
                        iodometric, iodometric_series, precipitation,
                        neutralisation, claus, full_oxidation, air_load, num)

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
im, d = canvas('Kislotalik: H₂S / HS⁻ / S²⁻ ulushlari va [S²⁻] (taxminiy hisob)', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(100, '100'), (75, '75'), (50, '50'), (25, '25'), (0, '0')]:
    txt(d, 8, 520 - v / 100.0 * 345 - 16, s, 22)
txt(d, 34, 108, 'ulush, %', 25)
for ph in range(0, 15, 2):
    x = 120 + ph / 14.0 * 560
    txt(d, x - 9, 526, str(ph), 16, G)
txt(d, 300, 548, 'pH', 23)
h2s_pts, hs_pts = [], []
for i in range(0, 57):
    ph = i * 0.25
    sp = speciation(ph)
    x = 120 + i / 56.0 * 560
    h2s_pts.append((x, 520 - sp['h2s'] / 100.0 * 345))
    hs_pts.append((x, 520 - sp['hs'] / 100.0 * 345))
d.line(h2s_pts, fill=N, width=4)
d.line(hs_pts, fill=TEAL, width=4)
for ph, col in [(7.04, RED), (11.96, PURPLE)]:
    x = 120 + ph / 14.0 * 560
    for yy in range(175, 521, 18):
        d.line((x, yy, x, yy + 9), fill=col, width=2)
x1 = 120 + 7.04 / 14.0 * 560
x2 = 120 + 11.96 / 14.0 * 560
txt(d, x1 - 66, 150, 'pK_a1 = 7,04', 20, RED)
txt(d, x2 - 78, 122, 'pK_a2 = 11,96', 20, PURPLE)
d.ellipse((146, 262, 162, 278), fill=N); txt(d, 170, 256, 'H₂S', 21, INK)
d.ellipse((146, 294, 162, 310), fill=TEAL); txt(d, 170, 288, 'HS⁻', 21, INK)
txt(d, 120, 578, 'Taxminiy hisob: pH 7,4 da H₂S 30,4 %;  HS⁻ 69,6 %;  S²⁻ 0,0021 %', 21, INK)

d.line((120, 650, 120, 950, 680, 950), fill=G, width=3)
for lv, s in [(-4, '−4'), (-8, '−8'), (-12, '−12'), (-16, '−16'), (-18, '−18')]:
    txt(d, 2, 650 + (-4 - lv) / 14.0 * 300 - 16, s, 21)
txt(d, 22, 612, 'lg[S²⁻], mol/L', 22)
for ph in (1.0, 2.0, 4.0, 6.0, 8.0):
    x = 120 + (ph - 1.0) / 7.0 * 560
    txt(d, x - 9, 956, num(ph, 0), 16, G)
txt(d, 290, 956, 'pH', 20, G)
pts = []
for i in range(0, 29):
    ph = 1.0 + i * 0.25
    lg = math.log10(sulfide_ion(0.100, ph))
    x = 120 + i / 28.0 * 560
    y = 650 + (-4 - lg) / 14.0 * 300
    pts.append((x, y))
d.line(pts, fill=B, width=4)
for (x, y) in pts[::4]:
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=B, outline='#FFFFFF', width=2)
txt(d, 120, 988, '[H₂S] = 0,100 M;  pH 1 → 1,09×10⁻¹⁸;  pH 7 → 1,09×10⁻⁶ mol/L', 21, N)
txt(d, 60, 1032, 'Sulfid ioni konsentratsiyasi pH ga kuchli bog‘liq; hisob K_a1·K_a2·[H₂S]/[H⁺]² asosida.', 21, INK)
txt(d, 60, 1082, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
txt(d, 60, 1140, 'K_a1 = 9,1×10⁻⁸ (pK_a1 = 7,04);  K_a2 ≈ 1,2×10⁻¹² (pK_a2 = 11,96)', 21, G)
save(im, 'kislotalik')

# --- Grafik 2: fizik xossalar -------------------------------------------------
im, d = canvas('Fizik xossalar: bug‘ bosimi, gaz zichligi va fazalar (taxminiy hisob)', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(0, '0'), (5, '5'), (10, '10'), (15, '15'), (20, '20'), (25, '25')]:
    txt(d, 8, 520 - v / 25.0 * 345 - 16, s, 22)
txt(d, 26, 110, 'p_sat, bar', 25)
for t in (190.0, 210.0, 230.0, 250.0, 270.0, 290.0):
    x = 120 + (t - 185.0) / 110.0 * 560
    txt(d, x - 12, 526, num(t, 0), 16, G)
txt(d, 300, 548, 'T, K', 23)
pts = []
for i in range(0, 12):
    t = 185.0 + i * 10.0
    x = 120 + i / 11.0 * 560
    y = 520 - vapor_pressure(t) / 25.0 * 345
    pts.append((x, y))
d.line(pts, fill=N, width=4)
xb = 120 + (T_B - 185.0) / 110.0 * 560
yb = 520 - vapor_pressure(T_B) / 25.0 * 345
d.ellipse((xb - 8, yb - 8, xb + 8, yb + 8), fill=RED, outline='#FFFFFF', width=2)
txt(d, xb - 96, yb - 44, 'Tb = 212,87 K', 20, RED)
d.ellipse((486, 186, 502, 202), fill=N); txt(d, 510, 180, 'C–C egri chizig‘i', 21, INK)
txt(d, 120, 578, 'Taxminiy hisob: p(25 °C) = 23,68 bar;  jadvaldagi 20,80 bar dan 13,8 % yuqori', 22, INK)

d.line((120, 645, 120, 950, 680, 950), fill=G, width=3)
for v, s in [(0.6, '0,6'), (1.0, '1,0'), (1.4, '1,4'), (1.8, '1,8'), (2.2, '2,2')]:
    txt(d, 8, 950 - (v - 0.6) / 1.8 * 305 - 16, s, 22)
txt(d, 26, 600, 'ρ_gaz, g/L', 23)
pts = []
for i in range(0, 12):
    t = 185.0 + i * 10.0
    x = 120 + i / 11.0 * 560
    y = 950 - (gas_density(t) - 0.6) / 1.8 * 305
    pts.append((x, y))
d.line(pts, fill=TEAL, width=4)
for t, rho, lab, dy in [(273.15, RHO_G_0, '1,539 g/L (0 °C)', -36), (298.15, RHO_G_25, '1,39 g/L (25 °C)', 18)]:
    x = 120 + (t - 185.0) / 110.0 * 560
    y = 950 - (rho - 0.6) / 1.8 * 305
    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=BROWN, outline='#FFFFFF', width=2)
    txt(d, x - 96, y + dy, lab, 19, INK)
txt(d, 120, 976, 'M = 34,081 g/mol;  havo nisbati 34,081/28,965 ≈ 1,18 — havo ustida yig‘iladi', 21, N)
txt(d, 60, 1026, 'Yong‘inuvchanlik 4–44 % (hajm);  o‘z-o‘zidan yong‘in harorati 232 °C.', 21, INK)
txt(d, 60, 1080, 'Tf = 190,85 K;  Tt = 187,66 K;  Pc = 89,63 bar;  ρc = 10,2 mol/L', 21, G)
txt(d, 60, 1140, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
save(im, 'fizik')

# --- Grafik 3: eritma --------------------------------------------------------
im, d = canvas('Suvli eritma: pH, dissotsiatsiya darajasi va to‘yingan holda (taxminiy hisob)', 1200)
cs = [0.0005, 0.001, 0.002, 0.005, 0.010, 0.020, 0.050, 0.100, 0.200, 0.500, 1.000, 2.000]
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(6, '6'), (4, '4'), (2, '2'), (0, '0')]:
    txt(d, 16, 520 - v / 6.0 * 345 - 16, s, 23)
txt(d, 40, 108, 'pH', 26)
txt(d, 250, 548, 'c, mol/L (chiziq teng intervalda)', 23)
pts = []
for i, c in enumerate(cs):
    p = ph_of(c)
    x = 120 + i * 50
    y = 520 - p['ph'] / 6.0 * 345
    pts.append((x, y))
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=B, outline='#FFFFFF', width=2)
d.line(pts, fill=B, width=4)
ss = saturated_solution()
xs = 120 + (7 + 0.2248) * 50
ys = 520 - ss['ph'] / 6.0 * 345
d.ellipse((xs - 11, ys - 11, xs + 11, ys + 11), outline=RED, width=4)
txt(d, xs - 200, ys + 26, 'to‘yingan: c = 0,1168 M;  pH = 3,99', 19, RED)
txt(d, 120, 574, 'Kuchsiz kislota uchun kvadrat yechim:  h = (−K_a1 + √(K_a1² + 4K_a1·c))/2', 20, N)

d.line((120, 660, 120, 920, 680, 920), fill=G, width=3)
for v, s in [(0, '0'), (0.5, '0,5'), (1.0, '1,0'), (1.5, '1,5')]:
    txt(d, 4, 920 - v / 1.5 * 260 - 16, s, 22)
txt(d, 24, 622, 'dissotsiatsiya, %', 23)
txt(d, 250, 940, 'c, mol/L (chiziq teng intervalda)', 22)
pts = []
for i, c in enumerate(cs):
    p = ph_of(c)
    x = 120 + i * 50
    y = 920 - p['pct'] / 1.5 * 260
    pts.append((x, y))
d.line(pts, fill=TEAL, width=4)
for (x, y) in pts:
    d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=TEAL, outline='#FFFFFF', width=2)
txt(d, 120, 972, 'Taxminiy hisob: 0,0005 M → 1,35 %;  0,010 M → 0,30 %;  1,000 M → 0,030 % dissotsiatsiya', 20, N)
txt(d, 60, 1016, 'Eritma juda kuchsiz kislota: pH asosan eritilgan H₂S konsentratsiyasidan kelib chiqadi.', 21, INK)
txt(d, 60, 1066, 'S(20 °C) = 3,98 g/L;  S(10 °C) = 5,3 g/L;  S(25 °C) = 1,22 g/L — manba qiymatlari', 21, G)
txt(d, 60, 1120, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 23, G)
save(im, 'eritma')

# --- Grafik 4: metall sulfidlar ----------------------------------------------
im, d = canvas('Metall sulfidlar: K_sp va pH bo‘yicha [M²⁺] chegarasi (taxminiy hisob)', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for lv, s in [('−5', '−5'), ('−15', '−15'), ('−25', '−25'), ('−35', '−35'), ('−45', '−45'), ('−55', '−55')]:
    lv = float(lv.replace('−', '-'))
    txt(d, 2, 175 + (-5 - lv) / 50.0 * 345 - 16, s, 21)
txt(d, 26, 110, 'lg K_sp', 25)
for i, (name, formula, ksp, col) in enumerate(SULFIDES):
    x = 132 + i * 49
    lg = math.log10(ksp)
    y = 175 + (-5 - lg) / 50.0 * 345
    d.rectangle((x - 18, y, x + 18, 520), fill=TEAL if lg > -20 else (BROWN if lg > -35 else PURPLE))
    txt(d, x - 20, 534, formula, 15, INK)
txt(d, 120, 578, 'K_sp:  CaS 8×10⁻⁶;  ZnS 2,0×10⁻²⁵;  PbS 3,2×10⁻²⁸;  CuS 7,9×10⁻³⁷;  HgS 2×10⁻⁵³', 20, N)

d.line((120, 660, 120, 950, 680, 950), fill=G, width=3)
for lv, s in [('−6', '−6'), ('−10', '−10'), ('−14', '−14'), ('−18', '−18'), ('−22', '−22'), ('−24', '−24')]:
    lv = float(lv.replace('−', '-'))
    txt(d, 2, 660 + (-6 - lv) / 18.0 * 290 - 16, s, 21)
txt(d, 20, 618, 'lg[M²⁺], mol/L', 22)
for ph in (1.0, 2.0, 4.0, 6.0, 8.0):
    x = 120 + (ph - 1.0) / 7.0 * 560
    txt(d, x - 9, 956, num(ph, 0), 16, G)
txt(d, 290, 956, 'pH', 20, G)
ksp_sel = {'ZnS': 2.0e-25, 'PbS': 3.2e-28, 'CdS': 1.0e-28}
colmap = {'ZnS': TEAL, 'PbS': RED, 'CdS': PURPLE}
for key, ksp in ksp_sel.items():
    pts = []
    for i in range(0, 29):
        ph = 1.0 + i * 0.25
        lg = math.log10(ksp / sulfide_ion(0.100, ph))
        x = 120 + i / 28.0 * 560
        y = 660 + (-6 - lg) / 18.0 * 290
        pts.append((x, y))
    d.line(pts, fill=colmap[key], width=3)
    d.ellipse((pts[0][0] - 7, pts[0][1] - 7, pts[0][0] + 7, pts[0][1] + 7),
              fill=colmap[key], outline='#FFFFFF', width=2)
for j, key in enumerate(['ZnS', 'PbS', 'CdS']):
    d.ellipse((452, 672 + j * 30, 466, 686 + j * 30), fill=colmap[key])
    txt(d, 474, 666 + j * 30, key, 20, INK)
txt(d, 120, 990, 'Taxminiy hisob: PbS uchun pH 1 → [Pb²⁺] = 2,93×10⁻¹⁰;  pH 7 → 2,93×10⁻²² mol/L', 20, N)
txt(d, 60, 1036, 'Chiqarilgan [M²⁺] chegarasi pH ga bog‘liq: S²⁻ konsentratsiyasi kichiklashishi bilan chegara kichiklashadi.', 19, INK)
txt(d, 60, 1086, '[H₂S] = 0,100 M;  taxminiy egri chiziq; o‘lchov ma’lumoti emas', 22, G)
save(im, 'metall')

# --- Grafik 5: ekvivalent va neytralizatsiya ----------------------------------
im, d = canvas('Ekvivalent massa, neytralizatsiya va yodometrik aniqlash (taxminiy hisob)', 1240)
d.line((120, 175, 120, 520, 680, 520), fill=G, width=3)
for v, s in [(0, '0'), (50, '50'), (100, '100'), (150, '150'), (200, '200'), (250, '250')]:
    txt(d, 2, 520 - v / 250.0 * 345 - 16, s, 22)
txt(d, 26, 108, 'kg', 25)
nn = neutralisation()
items = [('NaOH → NaHS', nn['naoh_nash'], TEAL),
         ('NaOH → Na₂S', nn['naoh_na2s'], N),
         ('Ca(OH)₂', nn['caoh2'], BROWN),
         ('CaS', nn['cas'], PURPLE)]
for i, (lab, val, col) in enumerate(items):
    x = 165 + i * 145
    h = val / 250.0 * 345
    d.rectangle((x - 48, 520 - h, x + 48, 520), fill=col)
    txt(d, x - 52, 520 - h - 28, '%s kg' % n2(val, 1), 19, INK)
    txt(d, x - 48, 538, lab, 17, G)
txt(d, 120, 578, '1000 kg 10 % li eritma: H₂S 100,0 kg  →  NaOH 117,4 / 234,7 kg;  Ca(OH)₂ 217,4 kg', 20, N)

d.line((120, 635, 120, 900, 680, 900), fill=G, width=3)
for v, s in [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]:
    txt(d, 10, 900 - v / 6.0 * 265 - 16, s, 22)
txt(d, 30, 596, 'g', 23)
io = iodometric()
bars = [('m(I₂)', io['m_i2'], RED), ('m(tiosulfat)', io['m_thio'], TEAL)]
for i, (lab, val, col) in enumerate(bars):
    x = 250 + i * 250
    h = val / 6.0 * 265
    d.rectangle((x - 55, 900 - h, x + 55, 900), fill=col)
    txt(d, x - 60, 900 - h - 28, '%s g' % n2(val, 4), 19, INK)
    txt(d, x - 55, 918, lab, 20, G)
txt(d, 120, 950, 'Yodometriya: 100,0 mL 0,0500 M eritma → n(H₂S) = 0,00500 mol;  I₂ 1,2690 g', 21, N)
txt(d, 60, 1000, 'Ekvivalent massa: 34,081/2 = 17,041 g/eq;  1 kg H₂S da 58,680 mol H⁺ ekvivalenti.', 21, INK)
txt(d, 60, 1055, 'I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻;  taxminiy hisob, o‘lchov ma’lumoti emas', 21, G)
txt(d, 60, 1110, 'Ekvivalent va zaxira hisoblar — nazariy; amaliy dozalar 12-bo‘limda', 22, G)
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
    ('Qaynash va suyuqlash', 'Tb 212,87 K (−60,28 °C);  Tf 190,85 K (−82,3 °C)', 'Burchakli molekula; qo‘pol, izotrop'),
    ('Kritik nuqta', 'Tc 373,3 K;  Pc 89,63 bar;  ρc 10,2 mol/L', 'Bu nuqtadan yuqorida suyuqlash mumkin emas'),
    ('Bug‘ bosimi', 'Taxminiy hisob: p(25 °C) = 23,68 bar', 'Jadvaldagi 20,80 bar dan 13,8 % yuqori'),
    ('Yong‘inuvchanlik', '4–44 % hajm;  o‘z-o‘zidan yong‘in 232 °C', 'Havo ustida ~1,18 marta og‘ir'),
    ('Molekulalar orasidagi kuch', 'ΔvapH ≈ 19,5 kJ/mol (200 K)', 'Vodorod bog‘i yo‘q — London dispersiyasi')])

scheme('eritmax', 'Suvli eritma: dissotsiatsiya, pH va muvozanat (sxematik)', [
    ('To‘yingan eritma', 'S(20 °C) = 3,98 g/L → c = 0,1168 mol/L', 'Taxminiy hisob: pH = 3,99 (haqiqiy taxmin ~4,5)'),
    ('Kuchsiz kislota', 'K_a1 = 9,1×10⁻⁸  (pK_a1 = 7,04)', 'h = √(K_a1·c) — taxminiy hisob'),
    ('Ikkinchi dissotsiatsiya', 'K_a2 ≈ 1,2×10⁻¹²  (pK_a2 = 11,96)', 'S²⁻ ulushi juda kichik'),
    ('Sulfid ioni', '[S²⁻] = K_a1·K_a2·[H₂S]/[H⁺]²', 'pH 1 → 1,09×10⁻¹⁸;  pH 7 → 1,09×10⁻⁶ mol/L'),
    ('Henry qonuni', 'H = p/c ≈ 17 800 kPa·L/mol (taxminiy hisob)', 'Suvda va ko‘pchilik erituvchilarda yaxshi eriydi')])

scheme('metallx', 'Metallarga ta’sir va sulfidlar (sxematik)', [
    ('Sulfidni kislota bilan yechish', 'FeS + 2HCl → FeCl₂ + H₂S↑', 'Tog‘-ruda va kavaklarda tabiiy manba'),
    ('To‘g‘ridan-to‘g‘ri reaksiya', 'M + 2H⁺ → M²⁺ + H₂↑', 'H₂S o‘zi kuchli kislota kabi ta’sir qiladi'),
    ('Cho‘qma hosil bo‘lishi', 'M²⁺ + H₂S → MS↓ + 2H⁺', 'K_sp bo‘yicha tartib: CaS > ZnS > PbS > CuS'),
    ('Mineral va ranglar', 'CaS oq;  ZnS oq;  CdS sariq;  CuS, PbS, HgS qora', 'Geologiya va minerallik uchun muhim belgi'),
    ('Nitratlar bilan', 'Sulfidlar HNO₃ da oksidlanadi', 'Sulfid ioni emas, S(0) hosil bo‘ladi')])

scheme('redoksx', 'Redoks xossalari va energetikasi (sxematik)', [
    ('To‘liq yondirish', '2H₂S + 3O₂ → 2SO₂ + 2H₂O  (ΔH ≈ −518 kJ/mol)', 'Sanoatda SO₂ olinadi'),
    ('Chala yondirish', '2H₂S + O₂ → 2S + 2H₂O', 'Aralash mahsulot — sariq rangli polimer'),
    ('Yod bilan reaksiya', 'H₂S + I₂ → S↓ + 2HI', 'Yodometrik aniqlashning asosi'),
    ('Standart potensiallar', 'E°(S + 2H⁺ + 2e⁻ ⇌ H₂S) = +0,14 V', 'E°(S + 2e⁻ ⇌ S²⁻) = −0,407 V'),
    ('Claus reaksiyasi', '2H₂S + SO₂ ⇌ 3S + 2H₂O  (ΔH ≈ −1165,6 kJ/mol)', 'Zanjirning eng eksotermik bosqichi')])

scheme('tuzlarx', 'Sulfidlar: K_sp, eruvchanlik va cho‘qma (sxematik)', [
    ('K_sp ta’rifi', 'K_sp = [M²⁺][S²⁻]', 'Jadvalda 11 ta metall sulfidi'),
    ('Erish tartibi', 'CaS 8×10⁻⁶ → ZnS 2,0×10⁻²⁵ → HgS 2×10⁻⁵³', 'K_sp kichik — cho‘qma barqaror'),
    ('Kislotada erish', 'MS + 2HCl → MCl₂ + H₂S↑', 'Kislotaga qarab teskari qaytadi'),
    ('PbS chegarasi', 'pH 1 → [Pb²⁺] = 2,93×10⁻¹⁰;  pH 7 → 2,93×10⁻²² mol/L', 'Taxminiy hisob, [H₂S] = 0,100 M'),
    ('Cho‘qma rangi', 'CdS sariq;  CuS, Ag₂S, HgS qora', 'Sifat va tahlil uchun qo‘llanadi')])

scheme('tahlilx', 'Tahlil usullari va gaz monitori (sxematik)', [
    ('Yodometriya', 'H₂S + I₂ → S + 2HI;  I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻', 'Taxminiy hisob: 100,0 mL 0,0500 M → I₂ 1,2690 g'),
    ('Gravimetriya', 'CuS yoki PbS cho‘kmasi quritilib o‘lchanadi', 'Aniq, lekin sekin usul'),
    ('Spektroskopiya', 'UV: 254 nm;  IR: ν 2615–2626 cm⁻¹', 'Gaz fazi va suvli eritma uchun'),
    ('Elektrokimiy usul', 'H₂S + 2e⁻ → S + 2H⁺ (elektroda)', 'Uzluksiz monitoring uchun'),
    ('Zamonaviy usullar', 'GC, ICP-OES/MS, elektrod signali', 'Laboratoriya va sanoat monitori')])

scheme('xavfsizlikx', 'Xavfsizlik chegaralari, monitor va muhofaza (sxematik)', [
    ('Kasb chegaralari', 'OSHA PEL 20 ppm (50 ppm — 10 daqiqa);  NIOSH REL 10 ppm', 'ACGIH: TWA 1 ppm;  STEL 5 ppm'),
    ('Hayot uchun xavfli daraja', 'IDLH 100 ppm', 'Daraja oshganda zudlik bilan evakuatsiya'),
    ('Reaksion javoblar', 'ERPG 0,1 / 30 / 100 ppm;  PAC 0,51 / 27 / 50 ppm', 'Qoldiq gaz va avariya ssenariylari'),
    ('Og‘irligi va monitor', '1 ppm = 1,40 mg/m³;  1 m³ da 20 ppm → 28 mg', 'Fixatsiyalangan elektrod yoki kolorimetr'),
    ('Hid va sezish', 'Hid charchashi 2–15 daqiqa', 'Hid — ishonchli signal emas; monitor shart')])


# --- Original illyustratsiyalar ------------------------------------------------
im, d = canvas('H₂S molekulasi: tuzilma, geometriya va energiya (sxematik)', 780)
cx, cy = 300, 300
half = math.radians(BOND_ANGLE / 2.0)
for sgn in (-1, 1):
    ax = cx + sgn * 78 * math.sin(half)
    ay = cy + 78 * math.cos(half)
    d.line((cx, cy, ax, ay), fill=N, width=8)
    d.ellipse((ax - 34, ay - 34, ax + 34, ay + 34), fill='#FFFFFF', outline=N, width=4)
    txt(d, ax - 12, ay - 18, 'H', 30, N)
d.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), fill=SULFUR, outline=BROWN, width=4)
txt(d, cx - 18, cy - 24, 'S', 40, '#FFFFFF')
for sgn in (-1, 1):
    for k in range(2):
        px = cx + sgn * (72 + 14 * k)
        py = cy - 62 + 9 * k
        d.ellipse((px - 8, py - 8, px + 8, py + 8), fill=G)
d.arc((cx - 104, cy - 104, cx + 104, cy + 104), 44, 136, fill=RED, width=4)
txt(d, cx + 116, cy + 6, '∠HSH = 92,11°', 22, RED)
txt(d, 60, 158, 'r(H–S) = 1,3356 Å', 23, INK)
txt(d, 60, 188, 'C₂v simmetriya', 23, INK)
txt(d, 60, 218, 'S atomida 2 erkin elektron jufti', 21, G)
txt(d, 60, 448, 'D(H–S) ≈ 347 kJ/mol;  μ = 0,97 D', 23, INK)
txt(d, 60, 482, 'IE = 10,46 eV;  PA = 705 kJ/mol', 23, INK)
txt(d, 60, 516, 'ΔfH°(g) = −20,6 kJ/mol;  S° = 205,81 J/(mol·K)', 22, INK)
d.rectangle((60, 566, 700, 630), fill='#EAF2F8')
txt(d, 78, 578, 'VSEPR bo‘yicha AX₂E₂ turi: burchakli molekula, C₂v simmetriya.', 21, N)
txt(d, 60, 672, 'Original sxematik chizma; o‘lchamlar shartli.', 21, G)
txt(d, 60, 716, 'Atom radiusi va bog‘ uzunligi shartli masshtabda berilgan.', 21, G)
save(im, 'molekulax')

im, d = canvas('H₂S olish usullari: laboratoriya, tabiiy jarayon va sanoat (sxematik)', 780)
cols = [('LABORATORIYA', TEAL, ['FeS + 2HCl → FeCl₂ + H₂S↑',
                                 'Al₂S₃ + 6H₂O → 2Al(OH)₃ + 3H₂S↑',
                                 'H₂ + S → H₂S']),
        ('TABIIY JARAYON', GREEN, ['Vulkan gazlari, fumarol',
                                   'Neft va gaz konlari',
                                   'Anaerob sulfat-reduksiya']),
        ('SANOAT', BROWN, ['Kavaklardan gaz yig‘ish',
                           'Absorber — stripper — “acid gas”',
                           'Claus usuli bilan oltingugurt'])]
for i, (head, col, rows) in enumerate(cols):
    x = 34 + i * 232
    d.rounded_rectangle((x, 150, x + 214, 560), radius=12, outline=col, width=4)
    d.rectangle((x, 150, x + 214, 206), fill=col)
    txt(d, x + 22, 164, head, 22, '#FFFFFF')
    for j, r in enumerate(rows):
        y = 228 + j * 108
        d.rounded_rectangle((x + 12, y, x + 202, y + 88), radius=10,
                            outline='#D6DFE7', width=2, fill='#FFFFFF')
        txt(d, x + 22, y + 12, r, 18, INK)
        d.ellipse((x + 22, y + 60, x + 36, y + 74), fill=col)
        if j < len(rows) - 1:
            txt(d, x + 96, y + 86, '↓', 22, G)
txt(d, 40, 596, 'Har bir usul tabiiy yoki sun’iy manbadan kelib chiqadi; mexanik qismi — gazni ajratib olish.', 19, N)
txt(d, 40, 640, 'Original sxematik chizma; bloklar shartli, parametrlar berilmagan.', 20, G)
txt(d, 40, 690, 'Qurilma, idish tanlash va dozalar bo‘yicha tavsiya 12-bo‘limda.', 20, G)
save(im, 'hosilax')

im, d = canvas('Idish materiallari, korroziya va saqlash (sxematik)', 780)
boxes = [('Novec', 'Molekulyar erituvchi', 'Kam qalinlikdagi qatlam', TEAL),
         ('Ss', 'Zarrarli po‘lat', 'H₂S bilan reaksiya — xavfli', GREEN),
         ('K', 'Shisha va keramika', 'Inert, lekin og‘ir', BROWN),
         ('Pt', 'Platina', 'Eng barqaror, qimmat', PURPLE)]
for i, (a, b, c, col) in enumerate(boxes):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 170, x + 160, 330), radius=12, outline=col, width=4)
    d.ellipse((x + 52, 185, x + 108, 241), fill=col)
    txt(d, x + 62, 196, a, 26, '#FFFFFF')
    txt(d, x + 8, 262, b, 19, INK)
    txt(d, x + 6, 292, c, 17, G)
    if i < 3:
        d.line((x + 160, 250, x + 178, 250), fill=G, width=4)
txt(d, 40, 380, 'Tanlov mezonlari: reaktivlik, namlik, ifloslanish, idishning zichlikka chidami.', 20, N)
txt(d, 40, 424, 'Bug‘ havoga to‘planadi va idish ichida quyi bosim hosil qiladi — yopiq idish talab qilinadi.', 19, B)
txt(d, 40, 478, 'Sulfid eritmasi saqlansa, metall idishda korroziya tez sodir bo‘ladi.', 20, INK)
txt(d, 40, 532, 'Saqlash shartlari: salqin, qorong‘i, yopiq, tekshiriladigan idish; markazlashgan talab.', 19, G)
txt(d, 40, 620, 'Original sxematik chizma; materiallar shartli.', 20, G)
txt(d, 40, 672, 'Materiallar ro‘yxati va xizmat muddati — amaliyot tavsiyasi emas.', 20, G)
save(im, 'idishx')

im, d = canvas('Tabiiy manbalar va biologik rol (sxematik)', 780)
d.rectangle((40, 150, 700, 300), outline=N, width=4)
d.polygon([(120, 300), (200, 190), (280, 300)], fill='#D8E8DC')
d.ellipse((180, 210, 220, 250), fill=RED)
txt(d, 100, 158, 'VULKAN', 22, INK)
txt(d, 300, 170, 'Fumarol va krater', 20, INK)
txt(d, 300, 200, 'SO₂ va H₂S aralashmasi', 19, G)
txt(d, 300, 232, 'H₂S — vulkan gazi tarkibida', 19, G)
d.rectangle((40, 320, 700, 470), outline=N, width=4)
d.rectangle((70, 350, 150, 470), fill='#8C5A2B')
d.rectangle((110, 330, 190, 470), fill='#6E4A22')
txt(d, 210, 340, 'NEFT VA GAZ KONLARI', 22, INK)
txt(d, 210, 372, 'Sulfid tarkibli neft va gaz', 20, INK)
txt(d, 210, 402, 'H₂S 90–100 Mt/y miqdarda', 19, G)
txt(d, 210, 430, 'Ajratib olish: absorber — stripper', 19, G)
d.rectangle((40, 490, 700, 640), outline=N, width=4)
txt(d, 64, 506, 'BIOLOGIK JARAYON', 22, INK)
txt(d, 64, 540, 'Anaerob sulfat-reduksiya:  SO₄²⁻ → S²⁻ → H₂S', 20, INK)
txt(d, 64, 572, 'Metanogenlar bilan birga:  CO₂ + H₂ → CH₄ + H₂O', 19, G)
txt(d, 64, 604, 'Tog‘-ruda suvlari, neft konlari, cho‘kindi', 19, G)
txt(d, 40, 690, 'Original sxematik chizma; miqdorlar yillik baholash.', 20, G)
txt(d, 40, 732, 'Manbalar: USGS (oltingugurt 85,8 Mt, 2023), IPCC va sanoat sharhlari.', 19, G)
save(im, 'tabiiy')

im, d = canvas('Claus usuli: oltingugurtni qaytarish zanjiri (sxematik)', 850)
stages = [('1 — TERMIK REAKTOR', '2H₂S + 3O₂ → 2SO₂ + 2H₂O', '315–330 °C;  1/3 H₂S yondiriladi', RED),
          ('2 — KATALITIK REAKTOR', '2H₂S + SO₂ ⇌ 3S + 2H₂O', 'Al₂O₃ / TiO₂;  ~240 °C va ~200 °C', TEAL),
          ('3 — SEPARATOR', 'S (suyuq) + H₂O + qoldiq gaz', 'Bug‘ va oltingugurt ajratiladi', BROWN)]
for i, (head, rxn, cond, col) in enumerate(stages):
    y = 140 + i * 175
    d.rounded_rectangle((40, y, 470, y + 140), radius=12, outline=col, width=4)
    txt(d, 62, y + 12, head, 23, col)
    txt(d, 62, y + 48, rxn, 20, INK)
    txt(d, 62, y + 84, cond, 18, G)
    if i < 2:
        txt(d, 240, y + 144, '↓', 30, B)
d.rounded_rectangle((500, 140, 720, 300), radius=12, outline=N, width=4)
txt(d, 520, 156, 'OLTINGUGURT', 23, N)
txt(d, 520, 196, 'S = 940,7 kg', 20, INK)
txt(d, 520, 226, '(1000 kg H₂S dan)', 18, G)
txt(d, 520, 258, 'Qaytarish 95–97 %', 18, INK)
d.rounded_rectangle((500, 330, 720, 480), radius=12, outline=G, width=4)
txt(d, 520, 346, 'QOLDIQ GAZ', 22, G)
txt(d, 520, 386, 'H₂S 0,8–1,5 %', 19, INK)
txt(d, 520, 416, 'yoqishgacha', 18, G)
txt(d, 520, 444, 'yoki SO₂ ga', 18, G)
d.line((470, 430, 500, 430), fill=G, width=3)
txt(d, 40, 654, 'Claus reaksiyasi ΔH ≈ −1165,6 kJ/mol;  termik bosqich ΔH ≈ −518 kJ/mol.', 20, INK)
txt(d, 40, 690, 'Original sxematik chizma; oqim sxemasi shartli.', 20, G)
d.rectangle((40, 716, 700, 790), fill='#EAF2F8')
txt(d, 58, 728, 'Taxminiy hisob: 1000 kg H₂S → S 940,7 kg;  H₂O 528,6 kg;  O₂ 469,4 kg;  kirish − chiqish 0,15 kg.', 18, N)
txt(d, 58, 758, 'Qaytarish chegarasi 97–98 %;  katalizator Al₂O₃ ≥ 300 m²/g.', 18, B)
save(im, 'clausx')

print('17 PNG yozildi:', A)
for f in sorted(A.glob('*.png')):
    print('  ', f.name)
