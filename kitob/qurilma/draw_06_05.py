"""Original teaching figures for 6.5 "HI — yodid kislota".
All curves are taxminiy hisob outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_06_05 import (ASSETS as A, PHYS, SOLUTIONS, GROUP, speciation_series,
                        triiodide_series, direct_synthesis, hydrazine_method,
                        phosphorus_method, h2s_method, iodine_from_iodide,
                        oxidation_by_oxygen, oxidation_by_nitric, neutralisation,
                        metal_dissolution, titration_standardisation, iodometry_sample,
                        iodized_salt)

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


def num(s):
    return str(s).replace('.', ',')


# --- Graph 1: guruh bo‘yicha kislotalik -------------------------------------
im, d = canvas('Guruh bo‘yicha kislotalik: bog‘ energiyasi va pK_a', 1180)
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
im, d = canvas('Ishlab chiqarish va yod sikli (shartli hisob)', 1180)
ds = direct_synthesis(1000.0); hz = hydrazine_method(1000.0)
ph = phosphorus_method(1000.0); ii = iodine_from_iodide(1000.0)
d.line((120, 175, 120, 500, 680, 500), fill=G, width=3)
for v, s in [(0, '0'), (250, '250'), (500, '500'), (750, '750'), (1000, '1000')]:
    txt(d, 14, 500 - v / 1000.0 * 325 - 16, s, 23)
txt(d, 45, 108, 'kg', 26)
txt(d, 125, 112, 'to‘g‘ridan-to‘g‘ri: H₂ + I₂ ⇌ 2HI', 22, INK)
for i, (name, v, col) in enumerate([('H₂', ds['m_h2'], TEAL), ('I₂', ds['m_i2'], N)]):
    x = 200 + i * 110
    h = v / 1000.0 * 325
    d.rectangle((x - 34, 500 - h, x + 34, 500), fill=col)
    txt(d, x - 38, 500 - h - 28, '%s kg' % num('%.2f' % v), 19, col)
    txt(d, x - 26, 512, name, 21, G)
txt(d, 400, 112, 'gidrazin: 2I₂ + N₂H₄ → 4HI + N₂', 22, INK)
for i, (name, v, col) in enumerate([('I₂', hz['m_i2'], N), ('N₂H₄', hz['m_n2h4'], TEAL),
                                    ('H₃PO₃', ph['m_h3po3'], B)]):
    x = 450 + i * 78
    h = v / 1000.0 * 325
    d.rectangle((x - 26, 500 - h, x + 26, 500), fill=col)
    txt(d, x - 32, 500 - h - 26, '%s' % num('%.0f' % v), 17, col)
    txt(d, x - 30, 512, name, 19, G)
d.line((120, 545, 680, 545), fill=G, width=2)
txt(d, 120, 565, 'yod sikli: 2NaI + Cl₂ → 2NaCl + I₂', 23, INK)
for i, (name, v, col) in enumerate([('NaI (kirish)', ii['m_nai'], N), ('Cl₂ (kirish)', ii['m_cl2'], TEAL),
                                    ('I₂ (chiqish)', ii['m_i2'], B), ('NaCl (chiqish)', ii['m_nacl'], GREEN)]):
    x = 200 + i * 125
    h = v / 1000.0 * 150
    d.rectangle((x - 30, 800 - h, x + 30, 800), fill=col)
    txt(d, x - 38, 800 - h - 26, num('%.1f' % v), 18, col)
    txt(d, x - 52, 812, name, 17, G)
txt(d, 45, 880, 'Taxminiy hisob: 1000 kg HI → H₂ 7,88 kg, I₂ 992,1 kg (ΔrH −9,44 kJ; K(298 K) = 0,254)', 22, N)
txt(d, 45, 930, 'Taxminiy hisob: 1000 kg NaI + Cl₂ 236,5 kg → I₂ 846,6 kg + NaCl 389,9 kg (kirish 1236,5 = chiqish)', 22, B)
txt(d, 45, 1000, 'Taxminiy hisob chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'ishlabchiqarish')

# --- Graph 3: redoks ---------------------------------------------------------
im, d = canvas('Redoks: yod olishi va triiodid ion (shartli hisob)', 1180)
d.line((120, 175, 120, 470, 680, 470), fill=G, width=3)
for v, s in [(0, '0'), (25, '25'), (50, '50'), (75, '75'), (100, '100')]:
    txt(d, 12, 470 - v / 100.0 * 295 - 16, s, 23)
txt(d, 45, 108, 'I₃⁻ ulushi, %', 26)
pts = []
for i, tb in enumerate(triiodide_series()):
    x = 120 + i * 70
    y = 470 - tb['w_i3'] / 100.0 * 295
    pts.append((x, y))
    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=N, outline='#FFFFFF', width=2)
d.line(pts, fill=N, width=4)
for i, tb in enumerate(triiodide_series()):
    x = 120 + i * 70
    lbl = num('%.1f' % tb['c_i']) if tb['c_i'] != 7.56 else '7,56'
    txt(d, x - 22, 488, lbl, 18, G)
txt(d, 300, 525, '[I⁻], M', 25)
txt(d, 120, 560, '1 g I₂ ning triiodidga aylanishi: I₂ + I⁻ ⇌ I₃⁻ (K ≈ 700)', 22, INK)
d.line((120, 615, 120, 880, 680, 880), fill=G, width=3)
for v, s in [(0, '0'), (250, '250'), (500, '500'), (750, '750'), (1000, '1000')]:
    txt(d, 14, 880 - v / 1000.0 * 265 - 16, s, 23)
txt(d, 45, 592, 'kg (1000 kg HI dan)', 23)
o2 = oxidation_by_oxygen(1000.0); hn = oxidation_by_nitric(1000.0)
for i, (name, v, col) in enumerate([('O₂ (O₂ bilan)', o2['m_o2'], TEAL), ('HNO₃ (HNO₃ bilan)', hn['m_hno3'], B),
                                    ('I₂ (natija)', o2['m_i2'], N)]):
    x = 210 + i * 180
    h = v / 1000.0 * 265
    d.rectangle((x - 40, 880 - h, x + 40, 880), fill=col)
    txt(d, x - 46, 880 - h - 28, '%s kg' % num('%.1f' % v), 20, col)
    txt(d, x - 56, 892, name, 18, G)
txt(d, 45, 950, 'Taxminiy hisob: 4HI + O₂ → 2I₂ + 2H₂O (62,5 kg O₂);  6HI + 2HNO₃ → 3I₂ + 2NO + 4H₂O (164,2 kg)', 22, N)
txt(d, 45, 1000, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'redoks')

# --- Graph 4: metallar ------------------------------------------------------
im, d = canvas('Metall yemirilishi: 1 g metallga to‘g‘ri kelgan HI (shartli hisob)', 1180)
md = metal_dissolution(1.0)
d.line((120, 175, 120, 700, 680, 700), fill=G, width=3)
for v, s in [(0, '0'), (4, '4'), (8, '8'), (12, '12'), (16, '16')]:
    txt(d, 20, 700 - v / 16.0 * 525 - 16, s, 23)
txt(d, 45, 108, 'HI sarfi, g', 26)
for i, m in enumerate(md):
    x = 120 + i * 140
    h = m['m_hi'] / 16.0 * 525
    col = RED if m['need_o2'] else N
    d.rectangle((x - 40, 700 - h, x + 40, 700), fill=col)
    txt(d, x - 44, 700 - h - 30, '%s g' % num('%.3f' % m['m_hi']), 20, col)
    txt(d, x - 30, 718, m['metal'], 24, G)
    txt(d, x - 50, 748, '%s g tuz' % num('%.3f' % m['m_salt']), 18, G)
txt(d, 45, 830, 'Taxminiy hisob: 1 g Fe → 5,545 g FeI₂ + 4,581 g HI;  1 g Zn → 4,882 g ZnI₂ + 3,913 g HI', 22, N)
txt(d, 45, 880, '1 g Al → 15,110 g AlI₃ + 14,222 g HI;  1 g Mg → 11,443 g MgI₂ + 10,526 g HI', 22, B)
txt(d, 45, 930, 'Mis: 1 g Cu → 4,026 g HI va 0,252 g O₂ — o‘z-o‘zidan eritilmaydi', 22, G)
txt(d, 45, 1000, 'Taxminiy hisob chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'metallar')

# --- Graph 5: chiqindi ------------------------------------------------------
im, d = canvas('Chiqindi: neytralizatsiya va yod ajratish (shartli hisob)', 1180)
n1 = neutralisation(1000.0, 10.0, 'Na2CO3'); n2 = neutralisation(1000.0, 10.0, 'Ca(OH)2')
d.line((120, 175, 120, 560, 680, 560), fill=G, width=3)
for v, s in [(0, '0'), (40, '40'), (80, '80'), (120, '120'), (160, '160')]:
    txt(d, 20, 560 - v / 160.0 * 385 - 16, s, 23)
txt(d, 45, 108, 'kg', 26)
for i, (name, v, col) in enumerate([('HI', n1['m_hi'], N), ('Na₂CO₃', n1['m_agent'], TEAL),
                                    ('NaI', n1['m_salt'], B), ('CO₂', n1['m_gas'], GREEN),
                                    ('H₂O', n1['m_h2o'], PURPLE)]):
    x = 150 + i * 115
    h = v / 160.0 * 385
    d.rectangle((x - 34, 560 - h, x + 34, 560), fill=col)
    txt(d, x - 38, 560 - h - 28, num('%.1f' % v), 19, col)
    txt(d, x - 32, 572, name, 19, G)
txt(d, 45, 620, 'neytralizatsiya: 1000 kg 10 % li HI + Na₂CO₃ (kirish 141,4 = chiqish 141,4 kg)', 22, INK)
d.line((120, 655, 680, 655), fill=G, width=2)
for i, (name, v, col) in enumerate([('Ca(OH)₂', n2['m_agent'], TEAL), ('CaI₂', n2['m_salt'], B),
                                    ('H₂O', n2['m_h2o'], GREEN)]):
    x = 250 + i * 130
    h = v / 160.0 * 120
    d.rectangle((x - 34, 820 - h, x + 34, 820), fill=col)
    txt(d, x - 38, 820 - h - 26, num('%.1f' % v), 19, col)
    txt(d, x - 30, 832, name, 19, G)
txt(d, 45, 880, 'Taxminiy hisob: 1000 kg 10 % HI → Na₂CO₃ 41,4 kg, NaI 117,2 kg, CO₂ 17,2 kg, H₂O 7,0 kg', 22, N)
txt(d, 45, 930, 'Ca(OH)₂ bilan: 29,0 kg Ca(OH)₂, 114,9 kg CaI₂, 14,1 kg H₂O (kirish 129,0 = chiqish 129,0 kg)', 22, B)
txt(d, 45, 1000, 'Taxminiy hisob chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'chiqindi')


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


scheme('fizikx', 'HI: fizik xossalar (sxematik)', [
    ('Gaz holati', 'M = 127,9125 g/mol; ρ 5,23 g/L (25 °C)', 'Havoga nisbatan 4,4 barobar og‘ir'),
    ('Kritik nuqta', '151 °C; 8,31 MPa; ρ 2,85 g/cm³ (−47 °C)', 'Boshqa galogenidlardan yuqori'),
    ('Erutma', '48 % → 1,60 g/cm³;  57 % → 1,70 g/cm³', 'Sanoat navi (Ullmann)'),
    ('Azeotrop', '56,7 % HI; 126,7 °C; 7,56 mol/L', 'Doimiy qaynash nuqtasi'),
    ('Eruvchanlik', '42 g/100 mL (20 °C); 234 g/100 mL (10 °C)', 'Sovuqda ancha yaxshi eriydi')])

scheme('olishsx', 'HI ishlab chiqarish (sxematik)', [
    ('To‘g‘ridan-to‘g‘ri usul', 'H₂ + I₂ ⇌ 2HI (Pt katalizator)', 'Taxminiy hisob: H₂ 7,88 kg / I₂ 992,1 kg; K = 0,254'),
    ('Gidrazin usuli', '2I₂ + N₂H₄ → 4HI + N₂', 'Taxminiy hisob: N₂H₄ 62,6 kg / 1000 kg HI'),
    ('Fosfor usuli', '3I₂ + 2P + 6H₂O → 6HI + 2H₃PO₃', 'Taxminiy hisob: P 80,7 kg; H₂O 140,8 kg'),
    ('H₂S usuli', 'H₂S + I₂ → 2HI + S', 'Tarixiy usul; I₂ 992,1 kg, H₂S 133,2 kg'),
    ('Yod olish sikli', '2NaI + Cl₂ → 2NaCl + I₂', 'Jahon yodi ≈30 000 t/y; brindan olinadi')])

scheme('triiodidsx', 'Yodidlar va yod komplekslari (sxematik)', [
    ('Oddiy yodidlar', 'NaI, KI, CaI₂, MgI₂', 'KI — tibbiy va ovqat yodlash'),
    ('Dimer', 'AlI₃ ⇌ ½Al₂I₆', 'Kuchli kovalent o‘zaro ta’sir'),
    ('Yod komplekslari', '[HgI₄]²⁻, [PbI₄]²⁻, [BiI₄]⁻, [AgI₂]⁻', 'I⁻ kuchli ligand'),
    ('Kumush yodidi', 'Ag⁺ + I⁻ → AgI↓ (sariq)', 'Ksp ≈ 8×10⁻¹⁷ — eng oz eriydi'),
    ('Triiodid ion', 'I₂ + I⁻ ⇌ I₃⁻ (K ≈ 700)', 'Taxminiy hisob: 7,56 M da 99,98 %')])

scheme('metalsx', 'Metallarga ta’sir: passivatsiya yo‘qligi (sxematik)', [
    ('Sirtda himoya qatlami yo‘q', 'Reaksiya to‘xtamaydi', 'HF dan asosiy farq'),
    ('Fe, Zn, Al, Mg', 'M + 2HI → MI₂ + H₂↑', 'Taxminiy hisob: 1 g Al → 14,222 g HI'),
    ('Mis istisnosi', 'HI o‘z-o‘zidan eritmaydi', '2Cu + O₂ + 4HI → 2CuI₂ + 2H₂O'),
    ('Kumush', 'Ag⁺ + I⁻ → AgI↓ (sariq cho‘kma)', 'Gravimetrik tahlil usuli'),
    ('Vodorod embrittlementi', 'H₂ po‘lat ichiga sing‘adi', 'Mustahkamlik pasayadi')])

scheme('organiksx', 'Organik kimyoga ta’sir (sxematik)', [
    ('Alkil iodidlari', 'R–OH + HI → R–I + H₂O', 'Guruhning eng reaktiv halogenidi'),
    ('Markerovnikov', 'R–CH=CH₂ + HI → R–CHI–CH₃', 'Klassik qoidasi'),
    ('Eter kesish', 'R–O–R′ + HI → R–I + R′–OH', 'Reagent sifatida qimmat'),
    ('Nitroaromatik qaytarish', 'ArNO₂ → ArNH₂ (HI + qizil fosfor)', '2001-yilda takomillashtirilgan usul'),
    ('Muhim mahsulotlar', 'CH₃I; metil va etil iodidlari', 'Cativa sikli: CH₃I + H₂O → CH₃OH + HI')])

scheme('qollanishsx', 'HI qo‘llanish sohalari (sxematik)', [
    ('Siriya ishlab chiqarish', 'Cativa jarayoni: HI kofizayqin', 'Asosiy sanoat iste’moli'),
    ('Yodlangan tuz', 'KI yoki KIO₃ — 20–40 mg I/kg', 'Ommaviy sog‘liq: endemik bo‘q profilaktikasi'),
    ('Tibbiyot', 'KI — tireotrop modda; radioaktiv zaxira', 'Endokrinologiya va radiatsiya himoyasi'),
    ('Kontrast va ekranlar', 'Rentgen kontrast agentlari; LCM moddalari', 'Diagnostika va elektronika'),
    ('Dezinfectant', 'Yod moddalari va iodoforlar', 'Tibbiyot va sanitariya')])

scheme('tahlilsx', 'HI tahlil usullari (sxematik)', [
    ('Standartlash', 'Na₂CO₃ yoki boraks bilan titrlash', 'Taxminiy hisob: 0,2000 g → 0,12580 mol/L'),
    ('Dead-stop titr', 'Pt elektrod; rang indikatori kerak emas', 'HI uchun klassik usul'),
    ('Yodometriya', 'IO₃⁻ + 5I⁻ + 6H⁺ → 3I₂ + 3H₂O', 'Taxminiy hisob: 1,000 g KIO₃ → 0,712 g I₂'),
    ('Gravimetriya', 'AgI cho‘kmasi quritilib o‘lchanadi', 'I⁻ aniqlash'),
    ('Zamonaviy usullar', 'Ion xromatografiya; ISE; ICP-MS', 'I, Hg, Pb izotoplari')])


# --- Original illustrasiyalar ------------------------------------------------
im, d = canvas('HI molekulasi va guruh trendi (sxematik)', 660)
for i in range(4):
    x = 110 + 160 * i
    d.ellipse((x - 30, 195, x + 30, 255), fill='#FFFFFF', outline=N, width=4)
    d.ellipse((x + 40, 195, x + 100, 255), fill='#FFFFFF', outline=BROWN, width=4)
    d.line((x + 30, 225, x + 40, 225), fill=B, width=6)
    txt(d, x - 20, 211, 'H', 30, N)
    txt(d, x + 52, 211, 'I', 28, BROWN)
    if i < 3:
        d.line((x + 100, 225, x + 130, 225), fill=G, width=3)
d.line((110, 295, 590, 295), fill=RED, width=4)
d.polygon([(590, 295), (566, 283), (566, 307)], fill=RED)
txt(d, 260, 305, 'dipol momenti 0,45 D', 24, RED)
d.rectangle((60, 360, 700, 414), fill='#EAF2F8')
txt(d, 80, 374, 'vodorod bog‘i yo‘q — yodning katta elektron buluti faqat dispersiya kuchini kuchaytiradi', 21, N)
txt(d, 60, 455, 'Shuning uchun HI qaynash harorati −35,4 °C: HF (19,5 °C) dan ancha tez bug‘laydi.', 21, N)
txt(d, 60, 500, 'Taxminiy hisob: r(H–I) = 1,609 Å;  D = 295 kJ/mol;  χ(I) = 2,66.', 21, B)
txt(d, 60, 570, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'molekulax')

im, d = canvas('Radioyod: tabiiy va sun’iy manbalar (sxematik)', 660)
d.rectangle((60, 150, 700, 230), fill='#DCEBF4')
txt(d, 90, 170, 'tabiiy fond: urin va gormonlar orqali', 23, N)
d.ellipse((330, 270, 430, 370), outline=G, width=4)
txt(d, 352, 300, 'I', 40, G)
d.ellipse((150, 300, 210, 360), fill=BROWN)
txt(d, 168, 315, 'I', 26, '#FFFFFF')
d.ellipse((480, 300, 540, 360), fill=BROWN)
txt(d, 498, 315, 'I', 26, '#FFFFFF')
d.line((210, 330, 330, 330), fill=RED, width=4)
d.polygon([(330, 330), (310, 320), (310, 340)], fill=RED)
d.line((430, 330, 480, 330), fill=RED, width=4)
d.polygon([(480, 330), (460, 320), (460, 340)], fill=RED)
txt(d, 230, 385, 'qalqon radiyodini yig‘adi', 21, RED)
d.rectangle((60, 455, 700, 505), fill='#EAF2F8')
txt(d, 80, 468, 'I-131 (yarim umr 8 kuni) — fuqarolar zaxirasini qalqon uchun ishlatishda', 20, N)
txt(d, 60, 545, 'I-129 — yirik yarim umr; atrof-muhit va suv manbalari uchun maxsus nazorat ostida.', 20, B)
txt(d, 60, 600, 'Original sxematik chizma; shakllar va masshtab shartli.', 20, G)
save(im, 'yodradio')

im, d = canvas('HI bilan korroziya: yuzada ulanish (sxematik)', 660)
d.rectangle((70, 220, 690, 430), fill='#DDE6F2')
txt(d, 95, 240, 'po‘lat sirti', 24, N)
d.rectangle((70, 180, 690, 220), fill='#DCEBF4')
txt(d, 95, 186, 'himoya qatlami (korroziya mahsulotlari yo‘q)', 22, TEAL)
for x in (170, 330, 520):
    d.ellipse((x - 26, 250, x + 26, 302), fill='#FFFFFF', outline=RED, width=3)
    d.ellipse((x - 12, 264, x + 12, 288), fill=RED)
    d.line((x, 180, x, 250), fill=RED, width=3)
    txt(d, x - 26, 316, 'ulkanish', 20, RED)
txt(d, 70, 470, 'I⁻ — guruhning eng kuchli qaytaruvchisi: u temirni qaytarib, oksidlanishni davom ettiradi.', 21, N)
txt(d, 70, 515, 'Natija — HCl va HBr ga qaraganda tezroq korroziya; vodorod embrittlementi ham kuchliroq.', 20, B)
txt(d, 70, 580, 'Original sxematik chizma; rang va o‘lcham shartli.', 20, G)
save(im, 'teshikx')

im, d = canvas('HI saqlash va transport (sxematik)', 660)
boxes = [('A', 'Sanoat navi', '48–57 %; sovuq holda', N),
         ('B', 'Azeotrop nav', '56,7 %; doimiy qaynash', TEAL),
         ('C', 'Transport', 'Maxsus idish, pufakchalar', B),
         ('D', 'I₂ bilan ishlash', 'Triiodid; yodometriya', PURPLE)]
for i, (a, b, c, col) in enumerate(boxes):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 170, x + 160, 320), radius=12, outline=col, width=4)
    d.ellipse((x + 52, 185, x + 108, 241), fill=col)
    txt(d, x + 72, 196, a, 28, '#FFFFFF')
    txt(d, x + 8, 255, b, 20, INK)
    txt(d, x + 6, 282, c, 18, G)
    if i < 3:
        d.line((x + 160, 245, x + 178, 245), fill=G, width=4)
txt(d, 40, 370, 'Tanlov mezonlari: reaktivlik, namlik, ifloslanish, idishning zichlikka chidami.', 21, N)
txt(d, 40, 415, 'HI bug‘lari havoga to‘planadi va teri uchun ayniqsa xavfli — idish yopiq bo‘lishi shart.', 20, B)
txt(d, 40, 460, 'Taxminiy hisob: saqlash shartlari konsentratsiya, miqdor va mahalliy qoidalarga bog‘liq.', 20, G)
txt(d, 40, 535, 'Original sxematik chizma; idish turlari shartli.', 20, G)
save(im, 'idishx')

im, d = canvas('Ishlangan hisob: besh shartli hisob (sxematik)', 830)
ds = direct_synthesis(1000.0); ii = iodine_from_iodide(1000.0)
n1 = neutralisation(1000.0, 10.0, 'Na2CO3'); io = iodometry_sample(1.0)
blocks = [('A — Ishlab chiqarish', 'H₂ + I₂ ⇌ 2HI', 'H₂ 7,88 kg; I₂ 992,1 kg; K = 0,254', N),
          ('B — Yod sikli', '2NaI + Cl₂ → 2NaCl + I₂', 'I₂ 846,6 kg / 1000 kg NaI', TEAL),
          ('C — Metall yemirilishi', 'Fe + 2HI → FeI₂ + H₂', '1 g Fe → 5,545 g FeI₂; 4,581 g HI', B),
          ('D — Neytralizatsiya', '2HI + Na₂CO₃ → 2NaI + CO₂ + H₂O', 'Na₂CO₃ 41,4 kg; kirish = chiqish', PURPLE),
          ('E — Yodometriya', 'IO₃⁻ + 5I⁻ + 6H⁺ → 3I₂ + 3H₂O', '1,000 g KIO₃ → I₂ 0,712 g; 0,887 g tiosulfat', GREEN)]
for i, (a, b, cc, col) in enumerate(blocks):
    y = 130 + 118 * i
    d.rounded_rectangle((40, y, 468, y + 96), radius=12, outline=col, width=4)
    txt(d, 60, y + 8, a, 25, col)
    txt(d, 60, y + 40, b, 20, INK)
    txt(d, 60, y + 66, cc, 18, G)
d.rounded_rectangle((488, 130, 716, 560), radius=12, outline=G, width=4)
txt(d, 506, 148, 'Taxminiy hisob natijalari', 24, GREEN)
txt(d, 506, 200, 'I₂ 992,1 kg', 20, INK)
txt(d, 506, 235, '(1000 kg HI dan)', 19, G)
txt(d, 506, 285, 'I₂ 846,6 kg', 20, INK)
txt(d, 506, 320, '(yod sikli)', 19, G)
txt(d, 506, 370, 'NaI 117,2 kg', 20, INK)
txt(d, 506, 405, '(neytralizatsiya)', 19, G)
txt(d, 506, 455, 'I₃⁻ 99,98 %', 20, INK)
txt(d, 506, 490, '(7,56 M da, taxminiy hisob)', 19, G)
txt(d, 506, 530, 'pH −0,879', 20, INK)
txt(d, 40, 740, 'Barcha sonlar ochiq shartli hisoblar; o‘lchov ma’lumoti emas.', 21, G)
txt(d, 40, 785, 'Shartli hisob chegarasi: faolik koeffitsiyentlar hisobga olinmagan.', 21, G)
save(im, 'hisob')
print('5 grafik; 7 sxema; 5 original illustration.')
