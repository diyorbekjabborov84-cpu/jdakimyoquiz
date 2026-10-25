"""Original teaching figures for 7.3 "H2SO4 — sulfat kislota (tuzilishi)".

Barcha sonli egri chiziqlar — jadval ma'lumotlaridan olingan taxminiy hisoblar
(o'lchov ma'lumoti emas). Chizmalar original sxematik ishlanmalar.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

from prep_07_03 import (ASSETS as A, M_H2SO4, M_H2O, M_S, M_SO2, M_SO3,
                        R_SO, R_SOH, R_OH, ANG_OSO_X, ANG_OSO_H, ANG_HOS,
                        TAU_HOSO, R_SO4, CRYSTAL_A, CRYSTAL_B, CRYSTAL_C,
                        CRYSTAL_BETA, CRYSTAL_Z, KA1, KA2, PKA2,
                        DFH_GAS, S_GAS, PA, GB, DG_DEPROT, HO_HO,
                        SPECTRA, HYDRATES, LIMITS, WORLD_PRODUCTION,
                        FERTILIZER_SHARE, METALLURGY_SHARE, BATTERY_SHARE,
                        CONV_99_7, T_M, T_B, RHO_LIQ, VISC_20, EPS,
                        second_step, dissolution_series, speciation_ph,
                        autoprotolysis, acid_capacity, hydrate_composition,
                        contact, oleum, equivalents, num)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'
INK = '#243746'; RED = '#C0392B'; PURPLE = '#6C3483'; GREEN = '#2E7D4F'
BROWN = '#8C5A2B'; SULFUR = '#D4A017'


def font(n):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', n)


def txt(d, x, y, s, n=28, c=N, maxw=None):
    maxw = (760 - x - 12) if maxw is None else maxw
    while n > 11 and d.textlength(s, font=font(n)) > maxw:
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


# --- Grafik 1: spektroskopiya -------------------------------------------------
im, d = canvas('Spektroskopiya: SO₄²⁻, HSO₄⁻ va H₂SO₄ tebranish bandlari (taxminiy chizma)', 1200)
X0, X1 = 210, 700
LO, HI = 400.0, 1300.0
rows = [('SO₄²⁻ (Tᵈ)', TEAL, 210, [('981', 100, 'ν₁', 'top'), ('451', 55, 'ν₂', 'top'),
                                    ('1104', 90, 'ν₃', 'top'), ('617', 48, 'ν₄', 'top')]),
        ('HSO₄⁻ (Cₛ)', B, 450, [('1055', 88, 'ν(SOH)', 'top'), ('1030', 62, 'yon', 'bottom'),
                                  ('900', 50, 'ν₃′', 'top'), ('617', 36, 'deform.', 'top')]),
        ('H₂SO₄ (g)', N, 690, [('1248', 78, 'S=O', 'top'), ('792', 56, 'S–OH', 'top'),
                               ('499', 36, 'SO₃', 'top')])]


def sx(v):
    return X0 + (v - LO) / (HI - LO) * (X1 - X0)


for lab, col, ybase, items in rows:
    d.line((X0, ybase, X1, ybase), fill='#C3CDD6', width=2)
    for (v, amp, name, pos) in items:
        x = sx(float(v))
        y = ybase - amp * 0.95
        d.line((x, ybase, x, y), fill=col, width=5)
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=col, outline='#FFFFFF', width=2)
        if pos == 'top':
            txt(d, x - 20, y - 52, name, 15, G)
            txt(d, x - 20, y - 30, v, 16, INK)
        else:
            txt(d, x - 20, y + 22, v, 16, INK)
            txt(d, x - 20, y + 44, name, 15, G)
    txt(d, 40, ybase - 112, lab, 21, col)
    txt(d, 40, ybase - 84, 'intensivlik', 16, G)
d.line((X0, 800, X1, 800), fill=G, width=3)
for v in range(400, 1301, 100):
    txt(d, sx(v) - 16, 806, str(v), 17, G)
txt(d, 380, 838, 'chastota, sm⁻¹', 21, G)
txt(d, 40, 878, 'Taxminiy hisob (chizma):  SO₄²⁻ — 4 ta chastota: ν₁ 981, ν₂ 451, ν₃ 1104, ν₄ 617 sm⁻¹;', 20, N)
txt(d, 40, 912, 'χ — «chekilish» 450 sm⁻¹.  HSO₄⁻ — 1055, 1030, 900 (Raman) sm⁻¹.', 20, INK)
txt(d, 40, 946, 'Taxminiy hisob: 3N − 6 = 6 = 1 (A₁) + 2 (E) + 3 (F₂) → 3 ta chastota IR’da faol.', 20, INK)
txt(d, 40, 980, 'H₂SO₄ (g): O–H 3603;  S=O 1248;  S–OH 792;  SO₃ «shlyapa» 499 sm⁻¹.', 20, G)
d.rectangle((40, 1018, 700, 1122), fill='#EAF2F8')
txt(d, 58, 1028, 'Tᵈ — faqat T₂ modasi IR’da faol (ν₃ va ν₄).', 19, N)
txt(d, 58, 1060, 'Cₛ — barcha 12 ta chastota ham IR, ham Raman’da faol.', 19, INK)
txt(d, 58, 1090, 'H₂SO₄ (C₂) — 15 oddiy tebranish;  inversiya markazi yo‘q.', 19, INK)
txt(d, 40, 1150, 'Intensivliklar shartli; ³³S NMR: sulfat ioni 328 ppm.  Original sxematik chizma.', 20, G)
save(im, 'spektr')

# --- Grafik 2: kislotalik va spetsiatsiya -------------------------------------
im, d = canvas('Kislotalik: HSO₄⁻ / SO₄²⁻ ulushlari pH bo‘yicha va 2-bosqich ulushi (taxminiy hisob)', 1240)
d.line((130, 175, 130, 520, 690, 520), fill=G, width=3)
for v, s in [(100, '100'), (75, '75'), (50, '50'), (25, '25'), (0, '0')]:
    txt(d, 76, 520 - v / 100.0 * 345 - 16, s, 20)
txt(d, 30, 112, 'ulush, %', 24)
for ph in range(0, 15, 2):
    x = 130 + ph / 14.0 * 560
    txt(d, x - 8, 526, str(ph), 16, G)
txt(d, 330, 548, 'pH', 22)
hso, so4 = [], []
for i in range(0, 57):
    ph = i * 0.25
    sp = speciation_ph(ph)
    x = 130 + i / 56.0 * 560
    hso.append((x, 520 - sp['hso4'] / 100.0 * 345))
    so4.append((x, 520 - sp['so4'] / 100.0 * 345))
d.line(hso, fill=TEAL, width=4)
d.line(so4, fill=B, width=4)
xp = 130 + PKA2 / 14.0 * 560
for yy in range(175, 521, 18):
    d.line((xp, yy, xp, yy + 9), fill=RED, width=2)
txt(d, xp - 84, 150, 'pKₐ₂ = 1,99', 20, RED)
d.ellipse((560, 300, 576, 316), fill=TEAL); txt(d, 584, 294, 'HSO₄⁻', 21, INK)
d.ellipse((560, 336, 576, 352), fill=B); txt(d, 584, 330, 'SO₄²⁻', 21, INK)
txt(d, 140, 578, 'Taxminiy hisob: pH 1 da HSO₄⁻ 89,29 %, SO₄²⁻ 10,71 %;  pH 2 da 45,45 % / 54,55 %', 19, INK)
txt(d, 140, 610, 'pH 3 da 7,69 % / 92,31 %;  pH 7 da 0,001 % / 99,999 % — pKₐ₂ = 1,99 da tenglik nuqtasi', 19, INK)

d.line((130, 690, 130, 960, 690, 960), fill=G, width=3)
for v, s in [(0, '0'), (25, '25'), (50, '50'), (75, '75'), (100, '100')]:
    txt(d, 76, 960 - v / 100.0 * 270 - 16, s, 20)
txt(d, 20, 644, '2-bosqich ulushi, %', 23)
for i, c in enumerate([0.001, 0.005, 0.010, 0.020, 0.050, 0.100, 0.200, 0.500, 1.000, 2.000, 4.000]):
    r = second_step(c)
    x = 140 + i * 52
    h = r['so4_pct'] / 100.0 * 270
    d.rectangle((x - 17, 960 - h, x + 17, 960), fill=N if i % 2 == 0 else TEAL)
    txt(d, x - 22, 960 - h - 26, n2(r['so4_pct'], 2), 14, INK)
    txt(d, x - 24, 968, num(c, 3), 14, G)
txt(d, 330, 980, 'c, mol/L', 20, G)
txt(d, 140, 1010, 'Taxminiy hisob: 0,001 M → 86,55 %;  0,010 M → 45,24 %;  0,100 M → 9,85 %;  1,000 M → 1,17 %', 19, N)
txt(d, 60, 1052, 'Kₐ₁ ≈ 10³ (to‘liq);  Kₐ₂ = 1,2×10⁻² (pKₐ₂ = 1,99).  Paulining qoidasi: 8,3×10⁴ ≈ 10⁵.', 20, INK)
txt(d, 60, 1096, 'Sulfat ioni ulushi konsentratsiya ortishi bilan monoton kamayadi.', 20, G)
txt(d, 60, 1158, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 22, G)
save(im, 'kislotalik')

# --- Grafik 3: dissotsiatsiya -------------------------------------------------
im, d = canvas('Suvdagi dissotsiatsiya: pH va sulfat ioni miqdori (taxminiy hisob)', 1240)
series = dissolution_series()
LOGC = [math.log10(r['c']) for r in series]


def gx(lc):
    return 140 + (lc + 3.0) / 7.4 * 540


d.line((140, 180, 140, 520, 690, 520), fill=G, width=3)
for v, s in [(0, '0'), (1, '1'), (2, '2'), (3, '3')]:
    txt(d, 100, 520 - v / 3.0 * 340 - 16, s, 20)
txt(d, 62, 118, 'pH', 25)
pts = []
for i, r in enumerate(series):
    x = gx(LOGC[i])
    y = 520 - (r['ph'] + 0.7) / 3.4 * 340
    pts.append((x, y))
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=B, outline='#FFFFFF', width=2)
d.line(pts, fill=B, width=4)
for lc, lab in [(-3, '0,001'), (-2, '0,010'), (-1, '0,100'), (0, '1,000')]:
    txt(d, gx(lc) - 22, 526, lab, 15, G)
txt(d, gx(0.6) - 18, 526, '4,000', 15, G)
txt(d, 330, 552, 'c, mol/L (logarifmik o‘q)', 21, G)
d.ellipse((486, 186, 502, 202), fill=B); txt(d, 510, 180, 'pH (taxminiy hisob)', 21, INK)
txt(d, 140, 592, 'Kvadrat yechim:  Kₐ₂ = h·x/(c − x)  →  x² + (c + Kₐ₂)x − Kₐ₂·c = 0;  Kₐ₂ = 1,2×10⁻²', 19, N)

d.line((140, 690, 140, 950, 690, 950), fill=G, width=3)
for v, s in [(0, '0'), (5, '5'), (10, '10'), (15, '15')]:
    txt(d, 94, 950 - v / 15.0 * 260 - 16, s, 20)
txt(d, 26, 644, '[SO₄²⁻], mol/L', 23)
pts = []
for i, r in enumerate(series):
    x = gx(LOGC[i])
    y = 950 - r['x'] / 0.015 * 260
    pts.append((x, y))
d.line(pts, fill=TEAL, width=4)
for (x, y) in pts:
    d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=TEAL, outline='#FFFFFF', width=2)
for lc, lab in [(-3, '0,001'), (-2, '0,010'), (-1, '0,100'), (0, '1,000')]:
    txt(d, gx(lc) - 22, 956, lab, 15, G)
txt(d, gx(0.6) - 18, 956, '4,000', 15, G)
txt(d, 330, 980, 'c, mol/L (logarifmik o‘q)', 21, G)
txt(d, 140, 1014, 'Taxminiy hisob: 0,001 M → 0,000865 mol/L;  0,100 M → 0,009848 mol/L;  4,000 M → 0,011929 mol/L', 19, N)
txt(d, 60, 1054, 'Sulfat ioni miqdori konsentratsiya bilan sekin o‘sadi va 0,012 mol/L ga yaqinashadi.', 20, INK)
txt(d, 60, 1096, 'Raman dalili: 1055 sm⁻¹ (HSO₄⁻), 980 sm⁻¹ (SO₄²⁻), 900 sm⁻¹ — nisbat konsentratsiyaga bog‘liq.', 20, INK)
txt(d, 60, 1138, 'Chegara: 5 M dan yuqorida faol koeffitsiyent va ion assotsiatsiyasi hisobga olinadi.', 20, G)
txt(d, 60, 1196, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 22, G)
save(im, 'dissotsiatsiya')

# --- Grafik 4: gidratlar -----------------------------------------------------
im, d = canvas('Gidratlar: H₂SO₄ massadagi ulushi va fazaviy tarkib (taxminiy hisob)', 1260)
rows = hydrate_composition()
d.line((140, 175, 140, 520, 690, 520), fill=G, width=3)
for v, s in [(0, '0'), (25, '25'), (50, '50'), (75, '75'), (100, '100')]:
    txt(d, 88, 520 - v / 100.0 * 345 - 16, s, 20)
txt(d, 36, 110, 'H₂SO₄, %', 24)
cols = [N, TEAL, B, BROWN, GREEN, PURPLE]
labels = ['SAM', 'SAD', 'SATri', 'SAT', 'SAH', 'SAO']
for i, r in enumerate(rows):
    x = 200 + i * 100
    h = r['wt_calc'] / 100.0 * 345
    d.rectangle((x - 36, 520 - h, x + 36, 520), fill=cols[i])
    txt(d, x - 38, 520 - h - 28, n2(r['wt_calc'], 2) + ' %', 16, INK)
    txt(d, x - 26, 528, labels[i], 16, G)
    txt(d, x - 32, 552, 'n = %s' % n2(r['n'], 1), 14, G)
txt(d, 140, 592, 'Taxminiy hisob:  w = 100·98,08/(98,08 + 18,015n) — hisob va jadval qiymatlari mos keladi.', 19, N)
txt(d, 140, 624, 'n = 1 → 84,48 %;  n = 2 → 73,13 %;  n = 3 → 64,47 %;  n = 4 → 57,65 %;  n = 8 → 40,49 %', 19, INK)

d.line((150, 700, 150, 950, 670, 950), fill=G, width=3)
for v, s in [(0, '0'), (2, '2'), (4, '4'), (6, '6'), (8, '8')]:
    txt(d, 106, 950 - v / 8.0 * 250 - 16, s, 20)
txt(d, 40, 656, 'suv molekulasi soni, n', 22)
pts = []
for i in range(0, 33):
    n = i * 0.25
    x = 150 + i / 32.0 * 520
    y = 950 - n / 8.0 * 250
    pts.append((x, y))
d.line(pts, fill=TEAL, width=4)
for (x, y) in pts[::4]:
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=TEAL, outline='#FFFFFF', width=2)
for n, lab in [(1, 'SAM'), (2, 'SAD'), (3, 'SATri'), (4, 'SAT'), (6.5, 'SAH'), (8, 'SAO')]:
    x = 150 + n / 8.0 * 520
    for yy in range(700, 951, 18):
        d.line((x, yy, x, yy + 9), fill=RED, width=2)
    txt(d, x - 20, 684, lab, 18, RED)
txt(d, 150, 982, 'Taxminiy hisob: 60 % eritmada n = (98,08/18,015)·(40/60) = 3,63 — uzluksiz nisbiy qiymat.', 19, N)
txt(d, 60, 1022, 'Tuzilmalar: SAM — H₃O⁺HSO₄⁻;  SAT — [H₅O₂⁺]₂SO₄²⁻;  SAO — H₃O⁺ + SO₄²⁻·7H₂O.', 20, INK)
txt(d, 60, 1064, 'Evteklar: muz–SAH 211 K (36 %);  muz–SAT 199 K (38 %);  80–90 % da viskozite maksimumi.', 20, INK)
txt(d, 60, 1106, 'Stratosferadagi aerozollar: H₂SO₄ kristallari quyoshni yansitadi (Pinatubo, 1991).', 20, G)
txt(d, 60, 1168, 'Taxminiy egri chiziq; o‘lchov ma’lumoti emas', 22, G)
save(im, 'gidratlar')

# --- Grafik 5: sanoat va ekvivalent -------------------------------------------
im, d = canvas('Sanoat: sarf ulushlari, moddiy balans va ekvivalent (taxminiy hisob)', 1240)
d.line((130, 175, 130, 520, 690, 520), fill=G, width=3)
for v, s in [(0, '0'), (20, '20'), (40, '40'), (60, '60'), (80, '80')]:
    txt(d, 76, 520 - v / 80.0 * 345 - 16, s, 20)
txt(d, 24, 110, 'jami sarfdan, %', 23)
shares = [('Fosfat o‘g‘itlari', 60.0, N), ('Metallurgiya', 22.0, TEAL),
          ('Akkumulatorlar', 7.0, B), ('Boshqa', 11.0, G)]
for i, (lab, val, col) in enumerate(shares):
    x = 220 + i * 130
    h = val / 80.0 * 345
    d.rectangle((x - 42, 520 - h, x + 42, 520), fill=col)
    txt(d, x - 34, 520 - h - 28, n2(val, 0) + ' %', 18, INK)
    txt(d, x - 50, 528, lab, 15, G)
txt(d, 140, 578, 'Dunyoda ishlab chiqarish 260–290 mln t/y;  kontakt usuli ≈ 90 %;  fosfat o‘g‘itlari 56–60 %.', 19, N)

cc = contact()
ol = oleum()
d.line((130, 645, 130, 900, 690, 900), fill=G, width=3)
for v, s in [(0, '0'), (200, '200'), (400, '400'), (600, '600'), (800, '800')]:
    txt(d, 76, 900 - v / 800.0 * 255 - 16, s, 20)
txt(d, 44, 598, 'kg', 22)
bars = [('S', cc['m_s'], BROWN), ('SO₂', cc['m_so2'], TEAL),
        ('O₂', cc['m_o2'], G), ('H₂O', cc['m_h2o'], PURPLE)]
for i, (lab, val, col) in enumerate(bars):
    x = 220 + i * 130
    h = val / 800.0 * 255
    d.rectangle((x - 40, 900 - h, x + 40, 900), fill=col)
    txt(d, x - 42, 900 - h - 28, n2(val, 1), 18, INK)
    txt(d, x - 32, 908, lab, 18, G)
txt(d, 140, 934, 'Taxminiy hisob: 1000 kg H₂SO₄ → S 326,9 kg;  SO₂ 653,2 kg;  O₂ 163,1 kg;  H₂O 183,7 kg.', 19, N)
d.rounded_rectangle((40, 972, 700, 1080), radius=10, outline='#D6DFE7', width=2, fill='#FFFFFF')
eq = equivalents()
txt(d, 60, 986, 'Oleum: 1000 kg kislot + 20 % erkin SO₃ → 1163,3 kg H₂S₂O₇;  erkin SO₃ 14,0 %.', 19, INK)
txt(d, 60, 1020, 'Ekvivalent massa:  98,08/2 = 49,04 g/eq;  1 mol H₂SO₄ = 2 mol H⁺ = 192 970 C.', 19, TEAL)
txt(d, 60, 1052, 'SO₃ konversiyasi (ikki pog‘onali sxema) 99,7 %;  100 % kislota proton zaxirasi 37,3 mol H⁺/L.', 19, INK)
txt(d, 60, 1116, 'Barcha sonlar taxminiy hisob; o‘lchov ma’lumoti emas.', 21, G)
txt(d, 60, 1160, 'Dozalar, apparat parametrlari va konsentratsiyalar bo‘yicha tavsiya 12-bo‘limda.', 20, G)
save(im, 'sanoat')


# --- Sxemalar ----------------------------------------------------------------
def scheme(name, title, boxes, h=None, w=3):
    h = h or (125 + 210 * len(boxes) + 70)
    im, d = canvas(title, h)
    for i, (s, a, b) in enumerate(boxes):
        y = 125 + 210 * i
        d.rounded_rectangle((32, y, 728, y + 160), radius=14, outline=N, width=3)
        txt(d, 52, y + 14, s, 30, B, 640)
        txt(d, 52, y + 65, a, 26, N, 640)
        txt(d, 52, y + 107, b, 25, G, 640)
        if i < len(boxes) - 1:
            txt(d, 360, y + 165, '↓', 33, B)
    save(im, name)


scheme('geometriax', 'Molekula geometriyasi: o‘lchovlar va simmetriya (sxematik)', [
    ('Nuqta guruhi', 'C₂ — o‘q oltingugurt atomidan o‘tadi', 'gauche-gauche konformatsiya; τ = 89,1°'),
    ('Bog‘ uzunliklari', 'r(S=O) 142,2 pm;  r(S–OH) 157,4 pm;  r(O–H) 97,0 pm', 'Ab initio: 140,99 / 157,51 pm;  τ = −86,66°'),
    ('Burchaklar', '∠O=S=O 123,3°;  ∠O=S–OH 101,3°;  ∠H–O–S 108,5°', 'Taxminiy hisob: yig‘indi 439,7°;  ideal 437,9°'),
    ('Sulfat ioni solishtiruvi', 'SO₄²⁻ — Tᵈ;  o‘rtacha r(S–O) 147,2 pm', 'To‘rtala bog‘ teng uzun'),
    ('Fazalar farqi', 'Erkin molekula: OH guruhlari erkin;  kristalda vodorod bog‘i zanjiri', 'Suyuq fazadagi geometriya boshqacha')])

scheme('rezonansx', 'Elektron tuzilma: rezonans va gaz fazidagi kislotalik (sxematik)', [
    ('S–O bog‘i', '142,2 pm — quyu, lekin qisqa (gipervalent bog‘)', 'Zamonaviy yondashuv: quyu taqsimot + rezonans'),
    ('Rezonans', 'Sulfat ionida 4!/(2!·2!) = 6 kanonik struktura', 'Taxminiy hisob: zaryad −0,5 e har bir O da'),
    ('Proton affinity', '699,4 kJ/mol;  gaz bazikligi 666,9 kJ/mol', 'NIST (Hunter & Lias, 1998)'),
    ('Gaz fazasidagi kislotalik', 'ΔrG°(deprotonatsiya) = 1265 ± 10 kJ/mol', 'Taxminiy hisob: 1265 − 691 = +574 kJ/mol — endotermik'),
    ('Suv fazasi', 'Proton gidratsiyasi ≈ −1091 kJ/mol — kamomad qoplanadi', '«Kuchli kislotalik» — muhitning natijasi')])

scheme('sufmax', 'Sufma kislota: avtoprotoliz, turlar va superkislotalik (sxematik)', [
    ('Avtoprotoliz', '2H₂SO₄ ⇌ H₃SO₄⁺ + HSO₄⁻', 'Protonli erituvchi;  elektr tokini yaxshi o‘tkazadi'),
    ('Turlar (mmol/kg)', 'HSO₄⁻ 15,0;  H₃SO₄⁺ 11,3;  H₃O⁺ 8,0;  HS₂O₇⁻ 4,4', 'H₂S₂O₇ 3,6;  H₂O 0,1'),
    ('Taxminiy hisob: Kₐₚ', '0,0113 × 0,0150 = 1,70×10⁻⁴ mol²/kg² (mole ulushida 1,63×10⁻⁶)', 'Adabiyotda ≈ 2,7×10⁻⁴ — bir xil tartib'),
    ('Superkislotalik', 'H₀ = −12;  proton solvatsiyasi ≈85 kJ/mol zaif', 'Proton kimyoviy faol;  anion kuchli solvatsiyalanadi'),
    ('Proton zaxirasi', 'Taxminiy hisob: 1,8302×1000/98,08 = 18,66 mol/L → 37,3 mol H⁺/L', '1 M suvli eritma — faqat 2 mol H⁺/L')])

scheme('ionlarx', 'Sulfat va gidrosulfat ionlari: tuzilma va rezonans (sxematik)', [
    ('Sulfat ioni SO₄²⁻', 'Tᵈ — tetraedrik;  r(S–O) 147,2 pm;  ∠O–S–O 109,47°', 'To‘rtala bog‘ teng — zaryad taqsimoti teng'),
    ('Gidrosulfat HSO₄⁻', 'Cₛ simmetriya;  Γ(vib) = 8a′ + 4a″ (12 chastota)', 'Protonatsiya bitta kislorodda'),
    ('Taxminiy hisob: rezonans', '6 kanonik struktura — zaryad 4 kislorodga teng taqsimlanadi', 'Sodda yondashuvda −0,5 e / O'),
    ('Bog‘ uzunliklari farqi', 'Terminal S=O 5,0 pm qisqa;  S–OH 10,2 pm uzun (sulfatga nisbatan)', 'Pauling yondashuvi: S=O π → S–OH σ*'),
    ('Pseudo-simmetriya', 'SAM kristalida HSO₄⁻ yadrosi pseudo-C₃ᵥ — 3 ta IR-faol modda', 'Nuqtadan istiqbolat tuzilma')])

scheme('gidratx', 'Gidratlar: tarkibi, tuzilmasi va fazaviy hodisalar (sxematik)', [
    ('SAM — monogidrat', 'H₂SO₄·H₂O;  84,5 %;  H₃O⁺HSO₄⁻', 'Proton suvga to‘liq o‘tgan'),
    ('SAT — tetragidrat', 'H₂SO₄·4H₂O;  57,6 %;  [H₅O₂⁺]₂SO₄²⁻', 'Sulfat ioni ikki protonlangan gidr Clustersiya bilan'),
    ('Taxminiy hisob', 'w = 100·98,08/(98,08 + 18,015n) — jadval bilan mos', 'n = 1 → 84,48 %;  n = 8 → 40,49 %'),
    ('Fazaviy hodisalar', 'Muz–SAH 211 K (36 %);  muz–SAT 199 K (38 %)', '80–90 % da viskozite maksimumi'),
    ('Atmosfera', 'Stratosferadagi H₂SO₄ aerozollari (Pinatubo, 1991)', 'Yupiter oylarida kristallik gidratlar')])

scheme('kristalx', 'Kristal tuzilma: hujra, vodorod bog‘i va fazalar (sxematik)', [
    ('Kristal tizimi', 'Monoklin;  fazoviy guruh C2/c;  Z = 4', 'a = 818,1;  b = 469,60;  c = 856,3 pm;  β = 111,39°'),
    ('Taxminiy hisob: hajm', 'V = a·b·c·sinβ = 306 313 pm³;  V/Z = 76 578 pm³', 'Kristal zichligi ≈ 2,13 g/cm³'),
    ('Vodorod bog‘i zanjiri', 'Har bir molekula ikkita qo‘shni molekulaga ulanadi', '(010) yo‘liq parallel qatlamlar'),
    ('Fizik xossalar', 'Erish nuqtasi 10,31 °C;  qaynash nuqtasi 337 °C (SO₃ ajraladi)', 'ρ = 1,8302 g/cm³;  viskozitet 26,7 cP'),
    ('Molekulyar qattiq', 'Dielektrik doimiy ≈ 100;  p(20 °C) = 0,001 mmHg', 'ΔvapH ≈ 69 kJ/mol')])

scheme('xavfsizlikx', 'Xavfsizlik chegaralari, ta’sir va favqulodda holat (sxematik)', [
    ('Kasb chegaralari', 'OSHA PEL 1 mg/m³;  NIOSH REL 1 mg/m³;  ACGIH TLV 0,2 mg/m³', 'ACGIH — torakal fraksiya, A2'),
    ('Hayot uchun xavfli daraja', 'NIOSH IDLH 15 mg/m³', 'Daraja oshganda zudlik bilan evakuatsiya'),
    ('Favqulodda holat chegaralari', 'AIHA ERPG-1 / 2 / 3 — 2 / 10 / 120 mg/m³', 'Reaktsion javoblar va avariya ssenariylari'),
    ('Ta’sir mexanizmi', 'Ko‘z va nafas yo‘llarini kuydiradi;  metall bilan reaksiyada vodorajon ajraladi', 'Organika moddalarni kug‘aklantiradi'),
    ('Kanserogenlik', 'IARC 1 — kuchli noorganik kislota tumanlari', 'Himoya vositalari va idish tanlash 12-bo‘limda')])


# --- Original illyustratsiyalar ------------------------------------------------
im, d = canvas('H₂SO₄ molekulasi: C₂ simmetriya va gauche-gauche konformatsiya (sxematik)', 880)
import math as _m
cx, cy = 200, 360
half_x = _m.radians(ANG_OSO_X / 2.0)
half_h = _m.radians(ANG_OSO_H / 2.0)
L1, L2, L3 = 112.0, 120.0, 88.0
ox_pts = []
for sgn in (-1, 1):
    ax = cx + sgn * L1 * _m.sin(half_x)
    ay = cy - L1 * _m.cos(half_x)
    ox_pts.append((ax, ay))
    d.line((cx, cy, ax, ay), fill=N, width=9)
for sgn in (-1, 1):
    ox = cx + sgn * L2 * _m.sin(half_h)
    oy = cy + L2 * _m.cos(half_h)
    d.line((cx, cy, ox, oy), fill=N, width=9)
    # H yo'nalishi: O -> S vektorini 108,5° ga burish
    vx, vy = cx - ox, cy - oy
    base = _m.atan2(vy, vx)
    rot = base + (1 if sgn > 0 else -1) * _m.radians(ANG_HOS)
    hx, hy = ox + L3 * _m.cos(rot), oy + L3 * _m.sin(rot)
    d.line((ox, oy, hx, hy), fill=N, width=7)
# C2 o'q
for yy in range(int(cy - 190), int(cy + 190), 16):
    d.line((cx, yy, cx, yy + 8), fill=GREEN, width=3)
# atomlar ustidan chiziladi
for (ax, ay) in ox_pts:
    d.ellipse((ax - 34, ay - 34, ax + 34, ay + 34), fill='#FFFFFF', outline=N, width=4)
    txt(d, ax - 13, ay - 19, 'O', 29, N)
for sgn in (-1, 1):
    ox = cx + sgn * L2 * _m.sin(half_h)
    oy = cy + L2 * _m.cos(half_h)
    vx, vy = cx - ox, cy - oy
    base = _m.atan2(vy, vx)
    rot = base + (1 if sgn > 0 else -1) * _m.radians(ANG_HOS)
    hx, hy = ox + L3 * _m.cos(rot), oy + L3 * _m.sin(rot)
    d.ellipse((ox - 33, oy - 33, ox + 33, oy + 33), fill='#FFFFFF', outline=N, width=4)
    txt(d, ox - 13, oy - 18, 'O', 29, N)
    d.ellipse((hx - 28, hy - 28, hx + 28, hy + 28), fill='#FFFFFF', outline=N, width=4)
    txt(d, hx - 11, hy - 16, 'H', 27, N)
d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), fill=SULFUR, outline=BROWN, width=4)
txt(d, cx - 17, cy - 24, 'S', 40, '#FFFFFF')
# burchak yoyi
a1 = _m.degrees(_m.atan2(ox_pts[0][1] - cy, ox_pts[0][0] - cx))
a2 = _m.degrees(_m.atan2(ox_pts[1][1] - cy, ox_pts[1][0] - cx))
d.arc((cx - 150, cy - 150, cx + 150, cy + 150), a1, a2, fill=RED, width=4)
txt(d, 40, 168, '∠O=S=O = 123,3°', 22, RED)
txt(d, 40, 128, 'C₂ nuqta guruhi — o‘q oltingugurt atomidan o‘tadi', 21, N)
txt(d, 40, 100, 'C₂ o‘qi', 20, GREEN)
txt(d, 442, 236, '∠O=S–OH = 101,3°', 21, RED)
txt(d, 442, 274, '∠H–O–S = 108,5°', 21, RED)
txt(d, 442, 312, 'τ(H–O–S–O) = 89,1°', 21, RED)
txt(d, 442, 358, 'r(S=O) = 142,2 pm', 21, INK)
txt(d, 442, 396, 'r(S–OH) = 157,4 pm', 21, INK)
txt(d, 442, 434, 'r(O–H) = 97,0 pm', 21, INK)
txt(d, 40, 560, 'Taxminiy hisob: burchaklar yig‘indisi 123,3 + 101,3 + 106,4 + 108,7 = 439,7°', 21, INK)
txt(d, 40, 596, 'tetraedrik ideal 4 × 109,47° = 437,9°;  farq +1,8°.', 21, INK)
txt(d, 40, 638, 'Sulfat ioni SO₄²⁻ — Tᵈ, r(S–O) 147,2 pm;  to‘rtala bog‘ teng uzun.', 21, INK)
d.rectangle((40, 676, 700, 742), fill='#EAF2F8')
txt(d, 58, 688, 'Erkin molekulada OH guruhlari «gauche»;  kristolda har bir molekula', 19, N)
txt(d, 58, 716, 'ikki qo‘shni molekulaga vodorod bog‘i orqali ulanadi (10-bo‘lim).', 19, N)
txt(d, 40, 786, 'Original sxematik chizma; o‘lchamlar shartli masshtabda.', 20, G)
txt(d, 40, 826, 'Atom radiuslari, rang va geometriya — o‘quv materiali; o‘lchov ma’lumoti emas.', 20, G)
save(im, 'molekulax')

im, d = canvas('Oltingugurt manbalari va sulfat kislota ishlab chiqarish (sxematik)', 820)
d.rectangle((40, 140, 700, 290), outline=N, width=4)
d.rectangle((70, 170, 150, 290), fill='#8C5A2B')
d.rectangle((112, 152, 192, 290), fill='#6E4A22')
txt(d, 210, 158, 'OLTINGUGURT MANBALARI', 22, INK)
txt(d, 210, 192, 'Neft qayta ishlash (qoldiq gaz) va gazni tozalash', 19, INK)
txt(d, 210, 222, 'Dunyoda ≈ 8 600 ming t/y oltingugurt', 19, G, 480)
txt(d, 210, 252, '≈ 90 % H₂SO₄ ga yo‘naltiriladi (USGS, 2024)', 19, G, 480)
d.rectangle((40, 310, 700, 460), outline=N, width=4)
txt(d, 64, 326, 'SANOAT ISHLAB CHIQARISH', 22, INK)
txt(d, 64, 360, '260–290 mln t/y;  kontakt usuli ≈ 90 %', 20, INK)
txt(d, 64, 392, 'Fosfat o‘g‘itlari 56–60 %;  metallurgiya ≈ 30 mln t', 19, G)
txt(d, 64, 422, 'Akkumulatorlar ≈ 14 mln t (USGS, S&P Global)', 19, G)
d.rectangle((40, 480, 700, 630), outline=N, width=4)
txt(d, 64, 496, 'TABIIY VA EKOLOGIK MANBALAR', 22, INK)
txt(d, 64, 530, 'Vulkan SO₂ → stratosferadagi H₂SO₄ aerozollari (Pinatubo, 1991)', 19, INK)
txt(d, 64, 562, 'Kengaytirilgan chang va ruda yig‘ish ta’siri', 19, INK)
txt(d, 64, 594, 'Konsentratsiyalar, texnik usullar berilmaydi', 19, G)
txt(d, 40, 676, 'Original sxematik chizma; bloklar shartli.', 20, G)
txt(d, 40, 716, 'Yillik baholash ko‘rsatkichlari;  mahalliy sharoitga qarab farq qiladi.', 20, G)
txt(d, 40, 764, 'Xavfsizlik amaliyoti 12-bo‘limda.', 20, G)
save(im, 'tabiiyx')

im, d = canvas('Kontakt usuli: oltingugurtdan sulfat kislotagacha (sxematik)', 880)
stages = [('1 — YONDIRISH', 'S + O₂ → SO₂   (yoki sulfid ruda kuydirish)', 'Ko‘mir va oltingugurt; 800–1000 °C', RED),
          ('2 — KONTAKT REAKTOR', '2SO₂ + O₂ ⇌ 2SO₃', 'V₂O₅ katalizatori;  400–450 °C', TEAL),
          ('3 — GIDRATLANISH', 'SO₃ + H₂O → H₂SO₄', 'Absorberda;  kislota 7.4-bo‘limda', BROWN)]
for i, (head, rxn, cond, col) in enumerate(stages):
    y = 140 + i * 180
    d.rounded_rectangle((40, y, 470, y + 145), radius=12, outline=col, width=4)
    txt(d, 62, y + 12, head, 23, col, 390)
    txt(d, 62, y + 50, rxn, 20, INK, 390)
    txt(d, 62, y + 88, cond, 18, G, 390)
    if i < 2:
        txt(d, 240, y + 148, '↓', 30, B)
d.rounded_rectangle((500, 140, 720, 310), radius=12, outline=N, width=4)
txt(d, 520, 156, 'MODDIY BALANS', 21, N, 185)
txt(d, 520, 194, '1000 kg H₂SO₄ uchun:', 18, INK, 190)
txt(d, 520, 226, 'S 326,9 kg', 17, TEAL, 190)
txt(d, 520, 256, 'SO₂ 653,2 kg', 17, TEAL, 190)
txt(d, 520, 282, 'O₂ 163,1 kg;  H₂O 183,7 kg', 16, TEAL, 185)
d.rounded_rectangle((500, 340, 720, 510), radius=12, outline=G, width=4)
txt(d, 520, 356, 'OLEUM', 22, G, 190)
txt(d, 520, 394, '1000 kg kislot + 20 % SO₃', 16, INK, 190)
txt(d, 520, 424, '→ 1163,3 kg H₂S₂O₇', 16, INK, 190)
txt(d, 520, 454, 'erkin SO₃ 14,0 %', 16, INK, 190)
txt(d, 520, 484, 'suyultirish → 1200,0 kg', 16, G, 190)
txt(d, 40, 700, 'Taxminiy hisob: 1000 kg kislot uchun reagentlar;  moddiy balans 0,00 kg.', 20, INK)
txt(d, 40, 738, 'Konversiya 99,7 % (ikki pog‘onali sxema).', 20, INK)
txt(d, 40, 786, 'Original sxematik chizma; oqim sxemasi shartli; apparat parametrlari berilmagan.', 19, G)
txt(d, 40, 826, 'Qurilma, idish tanlash va dozalar bo‘yicha tavsiya 12-bo‘limda.', 19, G)
save(im, 'zavodx')

im, d = canvas('Sulfat tuzlari: kristallar va eruvchanlik (sxematik)', 820)
salts = [('CaSO₄', 'Kalsiy sulfat', 'kips: CaSO₄·2H₂O', GREEN),
         ('BaSO₄', 'Bariy sulfat', 'radyografiya uchun', N),
         ('Ag₂SO₄', 'Kumush sulfat', 'eritilgan holda', TEAL),
         ('PbSO₄', 'Qo‘rg‘o‘l sulfat', 'akkumulator qatlami', BROWN)]
for i, (f, name, note, col) in enumerate(salts):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 160, x + 160, 350), radius=12, outline=col, width=4)
    d.rectangle((x + 28, 178, x + 132, 240), fill=col)
    txt(d, x + 40, 194, f, 24, '#FFFFFF')
    txt(d, x + 8, 258, name, 18, INK)
    txt(d, x + 4, 288, note, 16, G)
    for k in range(4):
        d.rectangle((x + 38 + 22 * k, 314, x + 52 + 22 * k, 330), fill=col)
txt(d, 40, 396, 'Kalsiy va qo‘rg‘o‘l sulfat deyarli erimaydi — bu ularning tabiiy ajratish usuli.', 19, N)
txt(d, 40, 436, 'Sulfat kislota neytralizatsiyasi:  H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O', 20, B)
txt(d, 40, 480, 'Ekvivalent massa:  98,08/2 = 49,04 g/eq (kislota);  SO₄²⁻ — tuz, proton soni 0.', 20, INK)
txt(d, 40, 524, 'Natriy sulfat elektrolit;  magniy sulfat tibbiyotda — 12-bo‘limga qarang.', 20, INK)
d.rectangle((40, 566, 700, 636), fill='#EAF2F8')
txt(d, 58, 580, 'Sulfat ioni tuzilishi:  Tᵈ simmetriya;  to‘rtta teng S–O bog‘i (147,2 pm);', 19, N)
txt(d, 58, 608, 'rezonans shakllari 4!/(2!·2!) = 6 — zaryad to‘rtta kislorodga teng.', 19, N)
txt(d, 40, 686, 'Original sxematik chizma; kristallar shartli chizilgan.', 20, G)
txt(d, 40, 726, 'Retsept, doza va konsentratsiya bo‘yicha tavsiya berilmaydi.', 20, G)
txt(d, 40, 774, 'Kislota va tuzlari bo‘yicha amaliyot 12-bo‘limda.', 20, G)
save(im, 'tuzlarilx')

im, d = canvas('Gidrat kristallari: tuzilma va fazaviy tuzilma (sxematik)', 900)


def sulfate_core(d, cx, cy, r=52):
    """Sxematik SO4 yadrosi: markazda S, atrofida to'rtta O."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SULFUR, outline=BROWN, width=3)
    pos = [(-46, -34), (46, -34), (-46, 34), (46, 34)]
    for (dx, dy) in pos:
        d.line((cx, cy, cx + dx, cy + dy), fill=N, width=5)
    for (dx, dy) in pos:
        d.ellipse((cx + dx - 15, cy + dy - 15, cx + dx + 15, cy + dy + 15),
                  fill='#FFFFFF', outline=N, width=3)
    txt(d, cx - 11, cy - 16, 'S', 26, '#FFFFFF')


d.rounded_rectangle((40, 130, 700, 336), radius=12, outline=N, width=4)
txt(d, 62, 146, 'SAM — H₂SO₄·H₂O (84,5 %):  H₃O⁺HSO₄⁻', 21, N)
d.ellipse((80, 200, 180, 300), fill=TEAL, outline=N, width=3)
txt(d, 96, 236, 'H₃O⁺', 24, '#FFFFFF')
sulfate_core(d, 300, 250, 46)
txt(d, 384, 196, 'C₃ᵥ mahalliy simmetriya', 18, INK)
txt(d, 384, 232, '3 ta IR-faol modda (2A₁ + E)', 18, G)
txt(d, 384, 268, 'Proton suvga to‘liq o‘tgan', 18, G)

d.rounded_rectangle((40, 356, 700, 562), radius=12, outline=N, width=4)
txt(d, 62, 372, 'SAT — H₂SO₄·4H₂O (57,6 %):  [H₅O₂⁺]₂SO₄²⁻', 21, N)
d.ellipse((80, 426, 180, 526), fill=TEAL, outline=N, width=3)
txt(d, 96, 462, 'H₅O₂⁺', 24, '#FFFFFF')
sulfate_core(d, 300, 476, 46)
txt(d, 384, 422, 'Protonlangan gidr Clustersiya', 18, INK)
txt(d, 384, 458, 'sulfat ioni bilan juftlashgan', 18, G)
txt(d, 384, 494, 'Sulfat yadrosi deyarli tetraedrik', 18, G)

txt(d, 40, 602, 'Taxminiy hisob:  w = 100·98,08/(98,08 + 18,015n) — jadval bilan mos (84,48 → 40,49 %).', 20, INK)
txt(d, 40, 642, 'Fazaviy hodisalar: muz–SAH 211 K (36 %);  muz–SAT 199 K (38 %);  80–90 % da viskozite maksimumi.', 20, INK)
txt(d, 40, 682, 'Stratosfera aerozollari (Pinatubo, 1991);  Yupiter oylarida kristallik gidratlar.', 20, G)
txt(d, 40, 734, 'Original sxematik chizma; atom joylashuvi shartli, tuzilma soddalashtirilgan.', 20, G)
txt(d, 40, 774, 'Tuzilma jadvali va fazaviy diagramma ma’lumotlariga asoslangan.', 20, G)
txt(d, 40, 822, 'Apparat parametrlari va konsentratsiyalar bo‘yicha tavsiya 12-bo‘limda.', 20, G)
save(im, 'gidratilx')

print('17 PNG yozildi:', A)
for f in sorted(A.glob('*.png')):
    print('  ', f.name)
