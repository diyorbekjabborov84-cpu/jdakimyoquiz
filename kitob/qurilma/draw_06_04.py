"""Original teaching figures for 6.4 "HBr — bromid kislota".
All curves are taxminiy hisob outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_06_04 import (ASSETS as A, PHYS, SOLUTIONS, GROUP, speciation_series,
                        tribromide_series, synthesis, lab_method, bromide_oxidation,
                        h2o2_bromination, oxidation_by_oxygen, neutralisation,
                        metal_dissolution, titration_standardisation)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'; INK = '#243746'
RED = '#C0392B'; PURPLE = '#6C3483'; GREEN = '#2E7D4F'; BROWN = '#8C5A2B'


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


def rows(name):
    return [{k: float(v) for k, v in r.items()}
            for r in csv.DictReader((A / (name + '.csv')).open())]


# --- Graph 1: guruh bo‘yicha kislotalik -------------------------------------
im, d = canvas('Guruh bo‘yicha kislotalik: bog‘ energiyasi va pK_a', 1180)
# yuqori panel: D(H–X)
d.line((120, 175, 120, 470, 680, 470), fill=G, width=3)
for i, g in enumerate(GROUP):
    x = 120 + i * 150
    h = g[1] / 600.0 * 295
    d.rectangle((x - 38, 470 - h, x + 38, 470), fill=N)
    txt(d, x - 34, 470 - h - 30, '%d' % g[1], 21, N)
    txt(d, x - 16, 488, g[0], 26, INK)
txt(d, 300, 525, 'vodorod galogenidi', 25)
txt(d, 45, 108, 'D(H–X), kJ/mol', 26)
txt(d, 45, 560, 'pK_a (suv) va pK_a (DMSO)', 26)
# pastki panel: pKa chiziqlari
d.line((120, 615, 120, 880, 680, 880), fill=G, width=3)
for v, s in [(15, '15'), (0, '0'), (-5, '−5'), (-10, '−10')]:
    txt(d, 20, 615 + (15 - v) / 30.0 * 265 - 16, s, 23)
pts1, pts2 = [], []
for i, g in enumerate(GROUP):
    x = 120 + i * 150
    y1 = 615 + (15 - g[2]) / 30.0 * 265
    y2 = 615 + (15 - g[3]) / 30.0 * 265
    pts1.append((x, y1)); pts2.append((x, y2))
    d.ellipse((x - 7, y1 - 7, x + 7, y1 + 7), fill=RED, outline='#FFFFFF', width=2)
    d.ellipse((x - 7, y2 - 7, x + 7, y2 + 7), fill=TEAL, outline='#FFFFFF', width=2)
    txt(d, x - 16, 898, g[0], 26, INK)
d.line(pts1, fill=RED, width=4)
d.line(pts2, fill=TEAL, width=4)
d.ellipse((430, 634, 446, 650), fill=RED); txt(d, 454, 628, 'pK_a (suv)', 21, RED)
d.ellipse((430, 672, 446, 688), fill=TEAL); txt(d, 454, 666, 'pK_a (DMSO)', 21, TEAL)
txt(d, 45, 950, 'Guruh: D(H–X) 569 / 432 / 366 / 295 kJ/mol;  pK_a (suv) 3,17 / −5,9 / −8,8 / −9,5', 22, N)
txt(d, 45, 1000, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'guruh')

# --- Graph 2: ishlab chiqarish ----------------------------------------------
im, d = canvas('Ishlab chiqarish va bromin sikli (shartli hisob)', 1180)
sy = synthesis(1000.0); lb = lab_method(1000.0); bo = bromide_oxidation(1000.0)
d.line((120, 175, 120, 500, 680, 500), fill=G, width=3)
for v, s in [(0, '0'), (250, '250'), (500, '500'), (750, '750'), (1000, '1000')]:
    txt(d, 14, 500 - v / 1000.0 * 325 - 16, s, 23)
txt(d, 45, 108, 'kg', 26)
txt(d, 125, 112, 'sintetik: H₂ + Br₂ → 2HBr', 22, INK)
for i, (name, v, col) in enumerate([('H₂', sy['m_h2'], TEAL), ('Br₂', sy['m_br2'], N)]):
    x = 200 + i * 110
    h = v / 1000.0 * 325
    d.rectangle((x - 34, 500 - h, x + 34, 500), fill=col)
    txt(d, x - 38, 500 - h - 28, '%.2f kg' % v, 19, col)
    txt(d, x - 26, 512, name, 21, G)
txt(d, 400, 112, 'laboratoriya: Br₂ + SO₂ + 2H₂O', 22, INK)
for i, (name, v, col) in enumerate([('Br₂', lb['m_br2'], N), ('SO₂', lb['m_so2'], TEAL), ('H₂SO₄', lb['m_h2so4'], B)]):
    x = 450 + i * 78
    h = v / 1000.0 * 325
    d.rectangle((x - 26, 500 - h, x + 26, 500), fill=col)
    txt(d, x - 34, 500 - h - 26, '%.0f' % v, 17, col)
    txt(d, x - 30, 512, name, 19, G)
d.line((120, 545, 680, 545), fill=G, width=2)
txt(d, 120, 565, 'bromin sikli: 2NaBr + Cl₂ → 2NaCl + Br₂', 23, INK)
for i, (name, v, col) in enumerate([('NaBr (kirish)', bo['m_nabr'], N), ('Cl₂ (kirish)', bo['m_cl2'], TEAL),
                                    ('Br₂ (chiqish)', bo['m_br2'], B), ('NaCl (chiqish)', bo['m_nacl'], GREEN)]):
    x = 200 + i * 125
    h = v / 1000.0 * 150
    d.rectangle((x - 30, 800 - h, x + 30, 800), fill=col)
    txt(d, x - 38, 800 - h - 26, '%.1f' % v, 18, col)
    txt(d, x - 52, 812, name, 17, G)
txt(d, 45, 880, 'Taxminiy hisob: 1000 kg HBr → H₂ 12,46 kg, Br₂ 987,5 kg (ΔrH −639,5 MJ);  laboratoriya: SO₂ 395,9 kg', 22, N)
txt(d, 45, 930, 'Taxminiy hisob: 1000 kg NaBr + Cl₂ 344,6 kg → Br₂ 776,6 kg + NaCl 568,0 kg (kirish 1344,6 ≈ chiqish)', 22, B)
txt(d, 45, 1000, 'Taxminiy hisob chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'ishlabchiqarish')

# --- Graph 3: redoks ---------------------------------------------------------
im, d = canvas('Redoks: bromin olishi va tribromid ion (shartli hisob)', 1180)
# yuqori panel: Br3- ulushi
d.line((120, 175, 120, 470, 680, 470), fill=G, width=3)
for v, s in [(0, '0'), (25, '25'), (50, '50'), (75, '75'), (100, '100')]:
    txt(d, 12, 470 - v / 100.0 * 295 - 16, s, 23)
txt(d, 45, 108, 'Br₃⁻ ulushi, %', 26)
pts = []
for i, tb in enumerate(tribromide_series()):
    x = 120 + i * 70
    y = 470 - tb['w_br3'] / 100.0 * 295
    pts.append((x, y))
    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=N, outline='#FFFFFF', width=2)
d.line(pts, fill=N, width=4)
for i, tb in enumerate(tribromide_series()):
    x = 120 + i * 70
    txt(d, x - 22, 488, '%.1f' % tb['c_br'] if tb['c_br'] != 8.77 else '8,8', 18, G)
txt(d, 300, 525, '[Br⁻], M', 25)
txt(d, 120, 560, '1 g Br₂ ning tribromidga aylanishi: Br₂ + Br⁻ ⇌ Br₃⁻ (lgK = 1,2)', 22, INK)
# pastki panel: HBr -> Br2
d.line((120, 615, 120, 880, 680, 880), fill=G, width=3)
for v, s in [(0, '0'), (250, '250'), (500, '500'), (750, '750'), (1000, '1000')]:
    txt(d, 14, 880 - v / 1000.0 * 265 - 16, s, 23)
txt(d, 45, 592, 'kg (1000 kg HBr dan)', 23)
h2 = h2o2_bromination(1000.0); o2 = oxidation_by_oxygen(1000.0)
for i, (name, v, col) in enumerate([('H₂O₂ (H₂O₂ bilan)', h2['m_h2o2'], TEAL), ('O₂ (O₂ bilan)', o2['m_o2'], B),
                                    ('Br₂ (natija)', h2['m_br2'], N)]):
    x = 210 + i * 180
    h = v / 1000.0 * 265
    d.rectangle((x - 40, 880 - h, x + 40, 880), fill=col)
    txt(d, x - 46, 880 - h - 28, '%.1f kg' % v, 20, col)
    txt(d, x - 56, 892, name, 18, G)
txt(d, 45, 950, 'Taxminiy hisob: 2HBr + H₂O₂ → Br₂ + 2H₂O (210,2 kg H₂O₂);  4HBr + O₂ → 2Br₂ + 2H₂O (98,9 kg O₂)', 22, N)
txt(d, 45, 1000, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'redoks')

# --- Graph 4: metallar ------------------------------------------------------
im, d = canvas('Metall yemirilishi: 1 g metallga to‘g‘ri kelgan HBr (shartli hisob)', 1180)
md = metal_dissolution(1.0)
d.line((120, 175, 120, 700, 680, 700), fill=G, width=3)
for v, s in [(0, '0'), (2, '2'), (4, '4'), (6, '6'), (8, '8'), (10, '10')]:
    txt(d, 26, 700 - v / 10.0 * 525 - 16, s, 23)
txt(d, 45, 108, 'HBr sarfi, g', 26)
for i, m in enumerate(md):
    x = 120 + i * 140
    h = m['m_hbr'] / 10.0 * 525
    col = RED if m['need_o2'] else N
    d.rectangle((x - 40, 700 - h, x + 40, 700), fill=col)
    txt(d, x - 44, 700 - h - 30, '%.3f g' % m['m_hbr'], 20, col)
    txt(d, x - 30, 718, m['metal'], 24, G)
    txt(d, x - 50, 748, '%.3f g tuz' % m['m_salt'], 18, G)
txt(d, 45, 830, 'Taxminiy hisob: 1 g Fe → 3,862 g FeBr₂ + 2,898 g HBr;  1 g Zn → 3,444 g ZnBr₂ + 2,475 g HBr', 22, N)
txt(d, 45, 880, '1 g Al → 9,884 g AlBr₃ + 8,996 g HBr;  1 g Mg → 7,575 g MgBr₂ + 6,658 g HBr', 22, B)
txt(d, 45, 930, 'Mis: 1 g Cu → 2,547 g HBr va 0,252 g O₂ — o‘z-o‘zidan eritilmaydi', 22, G)
txt(d, 45, 1000, 'Taxminiy hisob chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'metallar')

# --- Graph 5: chiqindi ------------------------------------------------------
im, d = canvas('Chiqindi: neytralizatsiya va bromin ajratish (shartli hisob)', 1180)
n1 = neutralisation(1000.0, 10.0, 'Na2CO3'); n2 = neutralisation(1000.0, 10.0, 'Ca(OH)2')
d.line((120, 175, 120, 560, 680, 560), fill=G, width=3)
for v, s in [(0, '0'), (40, '40'), (80, '80'), (120, '120'), (160, '160')]:
    txt(d, 20, 560 - v / 160.0 * 385 - 16, s, 23)
txt(d, 45, 108, 'kg', 26)
for i, (name, v, col) in enumerate([('HBr', n1['m_hbr'], N), ('Na₂CO₃', n1['m_agent'], TEAL),
                                    ('NaBr', n1['m_salt'], B), ('CO₂', n1['m_gas'], GREEN),
                                    ('H₂O', n1['m_h2o'], PURPLE)]):
    x = 150 + i * 115
    h = v / 160.0 * 385
    d.rectangle((x - 34, 560 - h, x + 34, 560), fill=col)
    txt(d, x - 38, 560 - h - 28, '%.1f' % v, 19, col)
    txt(d, x - 32, 572, name, 19, G)
txt(d, 45, 620, 'neytralizatsiya: 1000 kg 10 % li HBr + Na₂CO₃ (kirish 165,5 = chiqish 165,5 kg)', 22, INK)
d.line((120, 655, 680, 655), fill=G, width=2)
for i, (name, v, col) in enumerate([('Ca(OH)₂', n2['m_agent'], TEAL), ('CaBr₂', n2['m_salt'], B),
                                    ('H₂O', n2['m_h2o'], GREEN)]):
    x = 250 + i * 130
    h = v / 160.0 * 120
    d.rectangle((x - 34, 820 - h, x + 34, 820), fill=col)
    txt(d, x - 38, 820 - h - 26, '%.1f kg' % v, 19, col)
    txt(d, x - 30, 832, name, 19, G)
txt(d, 45, 880, 'Taxminiy hisob: 1000 kg 10 % HBr → Na₂CO₃ 65,5 kg, NaBr 127,2 kg, CO₂ 27,2 kg, H₂O 11,1 kg', 22, N)
txt(d, 45, 930, 'Ca(OH)₂ bilan: 45,8 kg Ca(OH)₂, 123,5 kg CaBr₂, 22,3 kg H₂O (kirish 145,8 = chiqish 145,8 kg)', 22, B)
txt(d, 45, 1000, 'Taxminiy hisob chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'chiqindi')


# --- Sxemalar --------------------------------------------------------------
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


scheme('fizikx', 'HBr: fizik xossalar (sxematik)', [
    ('Gaz holati', 'M = 80,912 g/mol; ρ 3,307 g/L (25 °C)', 'Havoga nisbatan 2,71 barobar og‘ir'),
    ('Kritik nuqta', '89,8 °C; 85,0 bar; 807 kg/m³', 'Suyuq holda saqlash mumkin'),
    ('Eritma', '40 % → 1,38 g/cm³;  48 % → 1,49 g/cm³', 'Katalog va nashr ma’lumotlari'),
    ('Azeotrop', '47,6 % HBr; 124,3 °C; 8,77 mol/L', 'Doimiy qaynash nuqtasi'),
    ('Gidratlar', 'HBr·nH₂O, n = 1, 2, 3, 4, 6', 'Gidronium bromidlar')])

scheme('olishsx', 'HBr ishlab chiqarish (sxematik)', [
    ('Sintetik usul', 'H₂ + Br₂ → 2HBr (200–400 °C, Pt)', 'Taxminiy hisob: H₂ 12,46 kg / Br₂ 987,5 kg'),
    ('Laboratoriya usuli', 'Br₂ + SO₂ + 2H₂O → H₂SO₄ + 2HBr', 'Bromin reagent sifatida sarflanadi'),
    ('Bromid + kislota', 'H₂SO₄ + KBr → KHSO₄ + HBr', 'Unum ≈85 %; >75 °C da oksidlanadi'),
    ('Bromin sikli', '2NaBr + Cl₂ → 2NaCl + Br₂', 'Jahon bromini ≈440 000 t/y'),
    ('Brom manbalari', 'Dengiz suvi ≈65 ppm Br; O‘rta dengiz ≈1 mlrd t', 'Brinlardan bug‘latish')])

scheme('bromokomplekssx', 'Bromidlar va bromokomplekslar (sxematik)', [
    ('Oddiy bromidlar', 'NaBr, KBr, CaBr₂, MgBr₂', 'KBr — tinchlantiruvchi vosita'),
    ('Dimer', 'AlBr₃ ⇌ ½Al₂Br₆', 'Kuchli kovalent o‘zaro ta’sir'),
    ('Bromokomplekslar', '[CuBr₄]²⁻, [CoBr₄]²⁻, [FeBr₄]⁻, [SnBr₆]²⁻', 'Br⁻ kuchli ligand'),
    ('Noble metall', '[PdBr₄]²⁻ — HBr muhitida Pd eriydi', 'Pt dan ajratish usuli'),
    ('Tribromid ion', 'Br₂ + Br⁻ ⇌ Br₃⁻', 'Taxminiy hisob: 8,77 M da 99,29 %')])

scheme('metalsx', 'Metallarga ta’sir: passivatsiya yo‘qligi (sxematik)', [
    ('Sirtda himoya qatlami yo‘q', 'Reaksiya to‘xtamaydi', 'HF dan asosiy farq'),
    ('Fe, Zn, Al, Mg', 'M + 2HBr → MBr₂ + H₂↑', 'Taxminiy hisob: 1 g Al → 8,996 g HBr'),
    ('Mis istisnosi', 'HBr o‘z-o‘zidan eritmaydi', '2Cu + O₂ + 4HBr → 2CuBr₂ + 2H₂O'),
    ('Kumush', 'Ag⁺ + Br⁻ → AgBr↓ (och sariq)', 'Tahlil usuli'),
    ('Vodorod embrittlementi', 'H₂ po‘lat ichiga sing‘adi', 'Mustahkamlik pasayadi')])

scheme('organiksx', 'Organik kimyoga ta’sir (sxematik)', [
    ('Alkil bromidlari', 'R–OH + HBr → R–Br + H₂O', 'Birlamchi spirtlardan'),
    ('Markerovnikov', 'R–CH=CH₂ + HBr → R–CHBr–CH₃', 'Klassik qoidasi'),
    ('Anti-Markerovnikov', 'Peroksidlar ishtirokida 1-bromalkanlar', 'Radikal mexanizm'),
    ('Bromlanish', '2ArH + 2HBr + H₂O₂ → 2ArBr + 2H₂O', 'Br₂ ni “joyida” hosil qilish'),
    ('Muhim mahsulotlar', 'Allil bromid; tetrabromobisfenol A; CH₃Br', 'Yong‘in qarshilash va fumigant')])

scheme('qollanishsx', 'HBr qo‘llanish sohalari (sxematik)', [
    ('Bromidlar', 'Fe, Ni, Zn bromidlari (gidrati)', 'Asosiy iste’mol sohasi'),
    ('Organik bromin moddalari', 'Alkil bromidlari, yong‘in qarshilash', 'Sanoat'),
    ('Foto va dori', 'AgBr — yorug‘likka sezgir; KBr — sedativ', 'An’anaviy sohalar'),
    ('Neft quyilish', 'Formiat bromli quyuq suyuqliklar', 'Past muzlash harorati'),
    ('Metallurgiya', 'Bromin ajratish; Pd ni HBr da eritish', 'Noble metall')])

scheme('tahlilsx', 'HBr tahlil usullari (sxematik)', [
    ('Standartlash', 'Na₂CO₃ yoki boraks bilan titrlash', 'Taxminiy hisob: 0,2000 g → 0,12580 mol/L'),
    ('Dead-stop titr', 'Pt elektrod; rang indikatori kerak emas', 'HBr uchun klassik usul'),
    ('Argentometriya', 'AgBr gravimetriya; Mohr; Fajans', 'Br⁻ aniqlash'),
    ('Zamonaviy usullar', 'Ion xromatografiya; ISE; ICP-MS', 'Br, Hg, Pb izotoplari'),
    ('Spesifikatsiya', 'Erkin HBr va umumiy bromid farqi', 'Kontsentratsiya nazorati')])


# --- Original illustrasiyalar ---------------------------------------------
im, d = canvas('HBr molekulasi va guruh trendi (sxematik)', 660)
for i in range(4):
    x = 110 + 160 * i
    d.ellipse((x - 30, 195, x + 30, 255), fill='#FFFFFF', outline=N, width=4)
    d.ellipse((x + 40, 195, x + 100, 255), fill='#FFFFFF', outline=BROWN, width=4)
    d.line((x + 30, 225, x + 40, 225), fill=B, width=6)
    txt(d, x - 20, 211, 'H', 30, N)
    txt(d, x + 50, 211, 'Br', 28, BROWN)
    if i < 3:
        d.line((x + 100, 225, x + 130, 225), fill=G, width=3)
d.line((110, 295, 590, 295), fill=RED, width=4)
d.polygon([(590, 295), (566, 283), (566, 307)], fill=RED)
txt(d, 260, 305, 'dipol momenti 0,8272 D', 24, RED)
d.rectangle((60, 360, 700, 414), fill='#EAF2F8')
txt(d, 80, 374, 'vodorod bog‘i yo‘q — bromining katta elektron buluti faqat dispersiya kuchini kuchaytiradi', 22, N)
txt(d, 60, 455, 'Shuning uchun HBr qaynash harorati −66,8 °C: HF (19,5 °C) dan tez, HI (−35,4 °C) dan sekin.', 21, N)
txt(d, 60, 500, 'Taxminiy hisob: r(H–Br) = 1,4144 Å;  D = 366 kJ/mol;  χ(Br) = 2,96.', 21, B)
txt(d, 60, 570, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'molekulax')

im, d = canvas('Bromin va stratosfera ozoni (sxematik)', 660)
d.rectangle((60, 150, 700, 230), fill='#DCEBF4')
txt(d, 90, 170, 'stratosfera (18–50 km)', 24, N)
d.rectangle((60, 230, 700, 430), fill='#F3E4C8')
txt(d, 90, 250, 'troposfera', 24, N)
d.ellipse((320, 255, 440, 375), outline=G, width=4)
txt(d, 350, 300, 'O₃', 34, G)
d.ellipse((170, 300, 230, 360), fill=BROWN)
txt(d, 178, 315, 'Br', 26, '#FFFFFF')
d.ellipse((500, 300, 560, 360), fill=BROWN)
txt(d, 512, 315, 'Br', 26, '#FFFFFF')
d.line((230, 330, 320, 330), fill=RED, width=4)
d.polygon([(320, 330), (300, 320), (300, 340)], fill=RED)
d.line((440, 330, 500, 330), fill=RED, width=4)
d.polygon([(500, 330), (480, 320), (480, 340)], fill=RED)
txt(d, 240, 380, 'BrO katalizatori', 22, RED)
d.rectangle((60, 455, 700, 505), fill='#EAF2F8')
txt(d, 80, 468, '≈20 pptv brom stratosferadagi 1000 pptv xlor bilan taqqoslanadi (ODP 0,6)', 21, N)
txt(d, 60, 545, 'Metilbromid (CH₃Br) — fumigant; 2005-yildan Montreyal protokoliga ko‘ra cheklangan.', 21, B)
txt(d, 60, 600, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'bromsx')

im, d = canvas('HBr bilan korroziya: yuzada ulanish (sxematik)', 660)
d.rectangle((70, 220, 690, 430), fill='#DDE6F2')
txt(d, 95, 240, 'po‘lat sirti', 24, N)
d.rectangle((70, 180, 690, 220), fill='#DCEBF4')
txt(d, 95, 186, 'himoya qatlami (korroziya mahsulotlari yo‘q)', 22, TEAL)
for x in (170, 330, 520):
    d.ellipse((x - 26, 250, x + 26, 302), fill='#FFFFFF', outline=RED, width=3)
    d.ellipse((x - 12, 264, x + 12, 288), fill=RED)
    d.line((x, 180, x, 250), fill=RED, width=3)
    txt(d, x - 26, 316, 'ulkanish', 20, RED)
txt(d, 70, 470, 'Br⁻ kuchsiz qaytaruvchi: u temirni qaytarib, oksidlanishni davom ettiradi.', 21, N)
txt(d, 70, 515, 'Natija — HCl ga qaraganda tezroq korroziya; vodorod embrittlementi ham kuchliroq.', 21, B)
txt(d, 70, 580, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'teshikx')

im, d = canvas('HBr saqlash va transport (sxematik)', 660)
boxes = [('A', 'To‘yingan eritma', '≤68,85 %; sovutish', N),
         ('B', 'Azeotrop nav', '47,6 %; doimiy qaynash', TEAL),
         ('C', 'Transport', 'Maxsus idish, pufakchalar', B),
         ('D', 'Br₂ bilan ishlash', 'Tribromid; H₂O₂ usuli', PURPLE)]
for i, (a, b, c, col) in enumerate(boxes):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 170, x + 160, 320), radius=12, outline=col, width=4)
    d.ellipse((x + 52, 185, x + 108, 241), fill=col)
    txt(d, x + 72, 196, a, 28, '#FFFFFF')
    txt(d, x + 8, 255, b, 20, INK)
    txt(d, x + 6, 282, c, 18, G)
    if i < 3:
        d.line((x + 160, 245, x + 178, 245), fill=G, width=4)
txt(d, 40, 370, 'Tanlov mezonlari: reaktivlik, yorug‘lik (rangli idish), temperatura, ifloslanish.', 21, N)
txt(d, 40, 415, 'HBr bug‘lari havoga to‘planadi va teri uchun ayniqsa xavfli — idish yopiq bo‘lishi shart.', 21, B)
txt(d, 40, 460, 'Taxminiy hisob: saqlash shartlari konsentratsiya, miqdor va mahalliy qoidalarga bog‘liq.', 21, G)
txt(d, 40, 535, 'Original sxematik chizma; idish turlari shartli.', 21, G)
save(im, 'idishx')

im, d = canvas('Ishlangan hisob: besh shartli hisob (sxematik)', 830)
mn = synthesis(1000.0)
bo = bromide_oxidation(1000.0)
n1 = neutralisation(1000.0, 10.0, 'Na2CO3')
h2 = h2o2_bromination(1000.0)
blocks = [('A — Ishlab chiqarish', 'H₂ + Br₂ → 2HBr', 'H₂ 12,46 kg; Br₂ 987,5 kg', N),
          ('B — Bromin sikli', '2NaBr + Cl₂ → 2NaCl + Br₂', 'Br₂ 776,6 kg / 1000 kg NaBr', TEAL),
          ('C — Metall yemirilishi', 'Fe + 2HBr → FeBr₂ + H₂', '1 g Fe → 3,862 g FeBr₂; 2,898 g HBr', B),
          ('D — Neytralizatsiya', '2HBr + Na₂CO₃ → 2NaBr + CO₂ + H₂O', 'Na₂CO₃ 65,5 kg; kirish = chiqish', PURPLE),
          ('E — Bromlanish', '2HBr + H₂O₂ → Br₂ + 2H₂O', 'H₂O₂ 210,2 kg → Br₂ 987,5 kg', GREEN)]
for i, (a, b, cc, col) in enumerate(blocks):
    y = 130 + 118 * i
    d.rounded_rectangle((40, y, 468, y + 96), radius=12, outline=col, width=4)
    txt(d, 60, y + 8, a, 25, col)
    txt(d, 60, y + 40, b, 20, INK)
    txt(d, 60, y + 66, cc, 19, G)
d.rounded_rectangle((488, 130, 716, 560), radius=12, outline=G, width=4)
txt(d, 506, 148, 'Taxminiy hisob natijalari', 24, GREEN)
txt(d, 506, 200, 'Br₂ 987,5 kg', 20, INK)
txt(d, 506, 528, 'ΔrH −639,5 MJ', 20, INK)
txt(d, 506, 235, '(1000 kg HBr dan)', 19, G)
txt(d, 506, 285, 'Br₂ 776,6 kg', 20, INK)
txt(d, 506, 320, '(bromin sikli)', 19, G)
txt(d, 506, 370, 'NaBr 127,2 kg', 20, INK)
txt(d, 506, 405, '(neytralizatsiya)', 19, G)
txt(d, 506, 455, 'Br₃⁻ 99,29 %', 20, INK)
txt(d, 506, 490, '(8,77 M da, taxminiy hisob)', 19, G)
txt(d, 506, 530, 'pH −0,943', 20, INK)
txt(d, 40, 740, 'Barcha sonlar ochiq shartli hisoblar; o‘lchov ma’lumoti emas.', 21, G)
txt(d, 40, 785, 'Shartli hisob chegarasi: faolik koeffitsiyentlar hisobga olinmagan.', 21, G)
save(im, 'hisob')
print('5 grafik; 7 sxema; 5 original illustration.')
