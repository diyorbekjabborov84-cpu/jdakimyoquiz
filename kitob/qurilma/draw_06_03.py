"""Original teaching figures for 6.3 "HCl — xlorid kislota".
All curves are taxminiy hisob outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_06_03 import (ASSETS as A, PHYS, SOLUTIONS, speciation_series, mannheim,
                         synthesis, regeneration, pickling_balance, neutralisation,
                         metal_dissolution, titration_standardisation)

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


def rows(name):
    return [{k: float(v) for k, v in r.items()}
            for r in csv.DictReader((A / (name + '.csv')).open())]


def axes(d, xlo, xhi, ylo, yhi, xlabel, ylabel, xt, yt, x0=120, x1=680, y0=175, y1=700):
    def p(x, y):
        return (x0 + (x - xlo) / (xhi - xlo) * (x1 - x0), y1 - (y - ylo) / (yhi - ylo) * (y1 - y0))
    d.line((x0, y0, x0, y1, x1, y1), fill=G, width=3)
    for x, s in xt:
        txt(d, p(x, ylo)[0] - 15, y1 + 18, s, 24)
    for y, s in yt:
        txt(d, 20, p(xlo, y)[1] - 16, s, 24)
    if xlabel:
        txt(d, x0 + 25, y1 + 80, xlabel, 27)
    if ylabel:
        txt(d, 45, 108, ylabel, 28)
    return p


# --- Graph 1: suvli HCl — shartli hisob pH va jadval pH ----------------------------
im, d = canvas('Suvli HCl: shartli hisob pH va jadvalning apparent pH qiymati', 1180)
LO, HI = -1.0, math.log10(12.0)

def px(c):
    return 120 + (math.log10(c) - LO) / (HI - LO) * (680 - 120)


def py(ph):
    return 700 - (ph + 1.4) / 2.8 * (700 - 175)


d.line((120, 175, 120, 700, 680, 700), fill=G, width=3)
for c, s in [(0.1, '0,1'), (0.5, '0,5'), (1, '1,0'), (2, '2,0'), (4, '4,0'),
             (8, '8,0'), (12, '12')]:
    txt(d, px(c) - 15, 718, s, 24)
for v, s in [(1.0, '1,0'), (0.5, '0,5'), (0.0, '0'), (-0.5, '−0,5'), (-1.0, '−1,0')]:
    txt(d, 20, py(v) - 16, s, 24)
txt(d, 300, 780, 'konsentratsiya, M (log o‘q)', 27)
txt(d, 45, 108, 'pH', 28)
spec = speciation_series()
pts = []
for s in spec:
    x, y = px(s['c']), py(s['ph'])
    pts.append((x, y))
    d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=N, outline='#FFFFFF', width=2)
d.line(pts, fill=N, width=4)
for r in rows('eritma'):
    x, y = px(r['mol_L']), py(r['pH'])
    d.rectangle((x - 6, y - 6, x + 6, y + 6), fill=RED)
d.ellipse((300, 130, 316, 146), fill=N); txt(d, 324, 124, 'shartli hisob pH = −lg c', 21, N)
d.rectangle((520, 132, 546, 154), fill=RED); txt(d, 554, 128, 'jadval pH (apparent)', 21, RED)
txt(d, 45, 830, 'Taxminiy hisob: Ka = 7,9×10⁵; lgK(HCl + Cl⁻ ⇌ HCl₂⁻) = 0,7; ideal erituvchi sharoiti', 22, N)
txt(d, 45, 880, 'Taxminiy hisob pH: 1,000 (0,1 M) · 0,000 (1,0 M) · −1,079 (12,0 M);  HCl₂⁻ ulushi 0,09 %', 22, B)
txt(d, 45, 930, 'Jadval nuqtalari taxminiy egri chiziqga yaqin: apparent pH ≈ −lg c', 22, G)
txt(d, 45, 1000, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'spetsiatsiya')

# --- Graph 2: eritma fizik xossalari ---------------------------------------
im, d = canvas('Suvli HCl: qaynash harorati, bug‘ bosimi va zichlik', 1180)
tab = rows('eritma')
# yuqori panel: qaynash harorati
d.line((120, 175, 120, 460, 680, 460), fill=G, width=3)
for i, r in enumerate(tab):
    txt(d, 120 + i * 93 - 12, 478, '%d %%' % r['w_pct'], 24)
for v, s in [(60, '60'), (80, '80'), (100, '100')]:
    txt(d, 26, 460 - (v - 40) / 70 * 285 - 16, s, 24)
txt(d, 300, 508, 'mass ulushi, %', 24)
txt(d, 45, 108, 'qaynash, °C', 26)
pts = []
for i, r in enumerate(tab):
    x = 120 + i * 93
    y = 460 - (r['tb_C'] - 40) / 70 * 285
    pts.append((x, y))
    d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=N, outline='#FFFFFF', width=2)
    txt(d, x - 34, y - 34, '%d' % r['tb_C'], 19, N)
d.line(pts, fill=N, width=4)
d.line((120 + 1 * 93, 175, 120 + 1 * 93, 460), fill=RED, width=2)
txt(d, 240, 412, 'azeotrop 20,2 % → 108,6 °C', 20, RED)
# pastki panel: bug‘ bosimi va zichlik
d.line((120, 585, 120, 790, 680, 790), fill=G, width=3)
txt(d, 45, 546, 'bug‘ bosimi, kPa  (ustun)  ·  zichlik, g/cm³  (yozuv ostida)', 22, N)
for i, r in enumerate(tab):
    x = 120 + i * 93
    h = r['vp_kPa'] / 30.0 * 205
    d.rectangle((x - 24, 790 - h, x + 24, 790), fill=TEAL)
    txt(d, x - 26, 790 - h - 28, '%.1f' % r['vp_kPa'], 19, TEAL)
    txt(d, x - 44, 802, '%.3f' % r['rho'], 20, INK)
txt(d, 45, 830, 'Jadval: 10 % → ρ 1,048, Tb 103 °C, vp 1,95 kPa;  20 % → 1,098, 108 °C, 1,40 kPa', 22, N)
txt(d, 45, 880, '30 % → 1,149, 90 °C;  38 % → 1,189, 48 °C, 28,3 kPa (pH −1,1)', 22, B)
txt(d, 45, 930, 'Konsentratsiya oshsa, bug‘ bosimi tez o‘sadi, qaynash harorati tushadi', 22, G)
txt(d, 45, 1000, 'Jadval ma’lumotlari; o‘lchov ma’lumoti emas', 23, G)
save(im, 'eritma')

# --- Graph 3: ishlab chiqarish mass oqimi ----------------------------------
im, d = canvas('Ishlab chiqarish: 1000 kg HCl uchun mass oqimi', 1180)
mn = mannheim(1000.0, 0.98)
sy = synthesis(1000.0)
p = axes(d, -0.5, 2.5, 0, 2200, '', 'kg',
         [(0, 'NaCl'), (1, 'H₂SO₄'), (2, 'Na₂SO₄')],
         [(0, '0'), (550, '550'), (1100, '1100'), (1650, '1650'), (2200, '2200')])
items = [('NaCl (kirish)', mn['m_nacl'], N), ('H₂SO₄ (kirish)', mn['m_h2so4'], TEAL),
         ('Na₂SO₄ (chiqish)', mn['m_na2so4'], B)]
for i, (name, v, col) in enumerate(items):
    x = p(i, 0)[0]
    h = v / 2200.0 * 525
    d.rectangle((x - 44, 700 - h, x + 44, 700), fill=col)
    txt(d, x - 46, 700 - h - 30, '%.1f kg' % v, 21, col)
d.line((120, 760, 680, 760), fill=G, width=2)
txt(d, 45, 775, 'sintetik usul (H₂ + Cl₂ → 2HCl):  H₂ 27,6 kg;  Cl₂ 972,4 kg;  ΔrH −2531,7 MJ', 21, INK)
txt(d, 45, 820, 'Mannheim usuli (2NaCl + H₂SO₄ → Na₂SO₄ + 2HCl):  ΔrH +884,8 MJ (32,3 kJ/mol HCl)', 21, INK)
txt(d, 45, 880, 'Taxminiy hisob: 1000 kg HCl → NaCl 1602,8 kg;  H₂SO₄ 1345,0 kg;  Na₂SO₄ 1947,8 kg', 22, N)
txt(d, 45, 930, 'Kirish 2947,8 kg = chiqish 2947,8 kg;  Mannheim usulida Na₂SO₄ (salt cake) chiqadi', 22, G)
txt(d, 45, 1000, 'Taxminiy hisobi; o‘lchov ma’lumoti emas', 23, G)
save(im, 'ishlabchiqarish')

# --- Graph 4: metall yemirilishi -------------------------------------------
im, d = canvas('Metall yemirilishi: 1 g metallga to‘g‘ri kelgan HCl (shartli hisob)', 1180)
md = metal_dissolution(1.0)
p = axes(d, -0.5, 4.5, 0, 4.5, '1 g metall', 'HCl sarfi, g',
         [(0, 'Fe'), (1, 'Zn'), (2, 'Al'), (3, 'Mg'), (4, 'Cu')],
         [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (4.5, '4,5')])
for i, m in enumerate(md):
    x = p(i, 0)[0]
    h = m['m_hcl'] / 4.5 * 525
    col = RED if m['need_o2'] else N
    d.rectangle((x - 40, 700 - h, x + 40, 700), fill=col)
    txt(d, x - 42, 700 - h - 30, '%.3f g' % m['m_hcl'], 20, col)
d.rectangle((430, 128, 456, 150), fill=N); txt(d, 464, 128, 'H₂ ajraladi', 21, N)
d.rectangle((430, 164, 456, 186), fill=RED); txt(d, 464, 164, 'Cu: havo (O₂) kerak', 21, RED)
txt(d, 45, 830, 'Taxminiy hisob: 1 g Fe → 2,270 g FeCl₂ + 1,306 g HCl + 0,036 g H₂;  1 g Zn → 2,084 g ZnCl₂', 22, N)
txt(d, 45, 880, '1 g Al → 4,942 g AlCl₃ + 4,054 g HCl;  1 g Mg → 3,917 g MgCl₂ + 3,000 g HCl', 22, B)
txt(d, 45, 930, 'Mis: 1 g Cu → 1,148 g HCl va 0,252 g O₂; o‘z-o‘zidan HCl misni eritmaydi', 22, G)
txt(d, 45, 1000, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'metallar')

# --- Graph 5: chiqindi va tiklash ------------------------------------------
im, d = canvas('Chiqindi: neytralizatsiya va kislotani tiklash sikli', 1180)
n1 = neutralisation(1000.0, 10.0, 'Na2CO3')
rg = regeneration(1000.0)
p = axes(d, -0.5, 3.5, 0, 200, '', 'kg',
         [(0, 'Na₂CO₃'), (1, 'NaCl'), (2, 'CO₂'), (3, 'H₂O')],
         [(0, '0'), (50, '50'), (100, '100'), (150, '150'), (200, '200')], y1=520)
for i, (name, v, col) in enumerate([('Na₂CO₃', n1['m_agent'], TEAL), ('NaCl', n1['m_salt'], N),
                                    ('CO₂', n1['m_gas'], B), ('H₂O', n1['m_h2o'], GREEN)]):
    x = p(i, 0)[0]
    h = v / 200.0 * 345
    d.rectangle((x - 40, 520 - h, x + 40, 520), fill=col)
    txt(d, x - 42, 520 - h - 28, '%.1f kg' % v, 20, col)
txt(d, 45, 566, 'neytralizatsiya: 1000 kg 10 % li HCl + Na₂CO₃ → NaCl + CO₂ + H₂O', 21, INK)
d.line((120, 596, 680, 596), fill=G, width=2)
for i, (name, v, col) in enumerate([('FeCl₂ (kirish)', 1000.0, N), ('Fe₂O₃ (chiqish)', rg['m_fe2o3'], B),
                                    ('HCl (tikilgan)', rg['m_hcl'], TEAL)]):
    x = 170 + i * 190
    h = v / 1000.0 * 140
    d.rectangle((x - 34, 790 - h, x + 34, 790), fill=col)
    txt(d, x - 40, 790 - h - 26, '%.1f kg' % v, 19, col)
    txt(d, x - 62, 802, name, 18, G)
txt(d, 45, 830, 'Taxminiy hisob: 1000 kg FeCl₂ → Fe₂O₃ 629,9 kg;  HCl 575,3 kg;  H₂O 142,1 kg;  O₂ 63,1 kg', 22, N)
txt(d, 45, 880, 'Neytralizatsiya: kirish 245,3 kg = chiqish 245,3 kg;  tiklash: 1205,2 ≈ 1205,2 kg', 22, B)
txt(d, 45, 930, 'Tiklangan kislota ≈18 % li bo‘lib, pickling zanjiriga qaytariladi', 22, G)
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


scheme('fizikx', 'HCl: fizik xossalar (sxematik)', [
    ('Gaz holati', 'M = 36,461 g/mol; ρ 1,627 kg/m³ (0 °C)', 'Havoga nisbatan 1,27 barobar og‘ir'),
    ('Kritik nuqta', '51,4 °C; 83,1 bar; 450 kg/m³', 'Quyuq holda saqlash mumkin'),
    ('Eritma', '10 % → 1,048 g/cm³;  38 % → 1,189 g/cm³', 'Jadval: 20 °C, 1 atm'),
    ('Azeotrop', '20,2 % HCl; 108,6 °C', 'Doimiy qaynash nuqtasi'),
    ('Gidronium tuzlari', '[H₃O]Cl 68 %;  [H₅O₂]Cl 51 %', 'Eutektik kristallar')])

scheme('olishsx', 'HCl ishlab chiqarish va tozalash (sxematik)', [
    ('Mannheim usuli', '2NaCl + H₂SO₄ → Na₂SO₄ + 2HCl', 'Taxminiy hisob: NaCl 1602,8 kg / 1000 kg HCl'),
    ('Sintetik usul', 'H₂ + Cl₂ → 2HCl (HCl pechi)', 'Taxminiy hisob: H₂ 27,6 kg;  Cl₂ 972,4 kg'),
    ('Tozalash', 'Cl₂, H₂S va namni olib tashlash', 'Quruq holda — suvda tozalash mumkin emas'),
    ('Yig‘ish', 'Deionlangan suvga yig‘ish', '20,2 % azeotrop chegarasi'),
    ('Navlar', 'Texnik 30–35 %;  murik 20–32 %;  konsentratsiyalangan 38 %', 'Sanoat va eksport')])

scheme('kloridlarsx', 'Tuzlar va xloro-komplekslar (sxematik)', [
    ('Oddiy xloridlar', 'NaCl, KCl, CaCl₂, MgCl₂', 'CaCl₂ — qurituvchi'),
    ('Kislota muhitidagi tuz', 'AlCl₃ gidrolizi', '[Al(H₂O)₆]³⁺ ionlashuvi'),
    ('Xloro-komplekslar', '[CuCl₄]²⁻, [CoCl₄]²⁻, [FeCl₄]⁻', 'Cl⁻ kuchli ligand'),
    ('Tuz hosil qilish', 'M + 2HCl → MCl₂ + H₂', 'Eng oddiy usul'),
    ('Analitik ahamiyati', 'AgCl, argentometriya, ion xromatografiya', '11-bo‘lim')])

scheme('metalsx', 'Metallarga ta’sir: passivatsiya yo‘qligi (sxematik)', [
    ('Sirtda himoya qatlami yo‘q', 'Reaksiya to‘xtamaydi', 'HF dan asosiy farq'),
    ('Fe, Zn, Al, Mg', 'M + 2HCl → MCl₂ + H₂↑', 'Taxminiy hisob: 1 g Fe → 1,306 g HCl'),
    ('Mis istisnosi', 'HCl o‘z-o‘zidan eritmaydi', '2Cu + O₂ + 4HCl → 2CuCl₂ + 2H₂O'),
    ('Vodorod embrittlementi', 'H₂ po‘lat ichiga diffuziya bilan sing‘adi', 'Mustahkamlik pasayadi'),
    ('Teshik korroziya', 'Cl⁻ zanglamaydigan po‘latni teshadi', 'Yuqori haroratda tez')])

scheme('suvsizsx', 'Suvsiz muhit va xloroaluminatlar (sxematik)', [
    ('Suvsiz dissotsiatsiya', 'HCl + CH₃OH → [CH₃OH₂]⁺ + Cl⁻', 'Erituvchi protonlanadi'),
    ('Lewis kislota qo‘shish', 'AlCl₃ → xloroaluminat anion', 'Proton uchun kuchli qabul qiluvchi'),
    ('Ion suyuqligi', 'AlCl₃ + EMIC; HCl oqimi', 'Brønsted superkislota tizimi'),
    ('H₀ qiymatlari', '−11,3;  −12,7;  ≈ −18', 'JACS va adabiyot o‘lchovlari'),
    ('Taqqoslash', 'Suyuq HF: H₀ = −15,1', 'Bir xil darajada protonlaydi')])

scheme('qollanishsx', 'HCl qo‘llanish sohalari (sxematik)', [
    ('Po‘lat tozalash', '18 % li texnik kislota', 'Eng katta iste’mol sohasi'),
    ('Vinil xlorid', 'C₂H₂ + HCl → CH₂=CHCl', 'PVC zanjiri kirish nuqtasi'),
    ('Suv dezinfectsiyasi', 'Cl₂ + H₂O ⇌ HCl + HOCl', 'Ta’sir HOCl dan'),
    ('Ion almashinuv va pH', 'Kationit tiklash; neytralizatsiya', 'Keng miqyosda'),
    ('Oziq-ovqat va dori', 'Jelly, guruch, tuz hosil qilish', 'Farmatsevtika darajasi')])

scheme('tahlilsx', 'HCl tahlil usullari (sxematik)', [
    ('Standartlash', 'Na₂CO₃ yoki boraks bilan titrlash', 'Taxminiy hisob: 0,2500 g → 0,18984 mol/L'),
    ('Dead-stop titr', 'Pt elektrod; rang indikatori kerak emas', 'HCl uchun klassik usul'),
    ('Kjeldahl', 'NH₃ ni HCl ga tutib qayta titrlash', 'Azot tahlili'),
    ('Kloridni aniqlash', 'AgCl gravimetriya; Mohr; Fajans', 'Arzon va aniq'),
    ('Zamonaviy usullar', 'Ion xromatografiya; ISE; ICP-MS', 'Fe, Pb, As izotoplari')])


# --- Original illustrasiyalar ---------------------------------------------
im, d = canvas('HCl molekulasi va dipol–dipol ta’sir (sxematik)', 640)
for i in range(4):
    x = 110 + 160 * i
    d.ellipse((x - 30, 200, x + 30, 260), fill='#FFFFFF', outline=N, width=4)
    d.ellipse((x + 40, 200, x + 100, 260), fill='#FFFFFF', outline=TEAL, width=4)
    d.line((x + 30, 230, x + 40, 230), fill=B, width=6)
    txt(d, x - 20, 216, 'H', 30, N)
    txt(d, x + 56, 216, 'Cl', 28, TEAL)
    if i < 3:
        d.line((x + 100, 230, x + 130, 230), fill=G, width=3)
d.line((110, 300, 590, 300), fill=RED, width=4)
d.polygon([(590, 300), (566, 288), (566, 312)], fill=RED)
txt(d, 250, 312, 'dipol momenti 1,08 D', 24, RED)
d.rectangle((60, 370, 700, 424), fill='#EAF2F8')
txt(d, 80, 384, 'vodorod bog‘i yo‘q — molekulalar orasida dipol–dipol tortish', 24, N)
txt(d, 60, 460, 'Shuning uchun HCl qaynash harorati −85,1 °C da qoladi: HF (19,5 °C) dan ancha past.', 21, N)
txt(d, 60, 505, 'Taxminiy hisob: r(H–Cl) = 1,2746 Å;  D = 432 kJ/mol;  χ(Cl) = 3,16.', 21, B)
txt(d, 60, 570, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'molekulax')

im, d = canvas('Po‘latni tozalash: oksid qatlamining erishi (sxematik)', 660)
d.rectangle((70, 200, 690, 300), fill='#D9D4C8')
txt(d, 95, 235, 'po‘lat (Fe)', 26, INK)
d.rectangle((70, 150, 690, 200), fill='#8C5A2B')
txt(d, 95, 160, 'oksid qatlami (okkala): Fe₃O₄, FeO', 23, '#FFFFFF')
d.ellipse((250, 120, 286, 156), fill=B)
txt(d, 200, 78, 'HCl', 28, B)
for x in (255, 275, 295):
    d.line((x, 156, x - 6, 186), fill=B, width=4)
for x in (420, 470, 520):
    d.ellipse((x, 110, x + 26, 136), outline=G, width=3)
    txt(d, x - 2, 82, 'H₂', 20, G)
d.rectangle((70, 300, 690, 360), fill='#EAF2F8')
txt(d, 95, 315, 'toza metall sirt — keyingi shakllantirishga tayyor', 23, TEAL)
txt(d, 70, 410, 'Taxminiy hisob: 1 t po‘lat uchun HCl 7,6 kg;  Fe 5,8 kg;  Cl⁻ 7,4 kg.', 21, N)
txt(d, 70, 455, 'Oksid qatlami eriganda H₂ ajraladi; uning po‘latga sing‘ishi — embrittlement xavfi.', 21, B)
txt(d, 70, 530, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'korroziyax')

im, d = canvas('Teshik (pitting) korroziya: Cl⁻ ning ta’siri (sxematik)', 660)
d.rectangle((70, 220, 690, 430), fill='#DDE6F2')
txt(d, 95, 240, 'zanglamaydigan po‘lat sirti', 24, N)
d.rectangle((70, 180, 690, 220), fill='#DCEBF4')
txt(d, 95, 186, 'himoya qatlami (Cr₂O₃)', 22, TEAL)
for x in (170, 330, 520):
    d.ellipse((x - 26, 250, x + 26, 302), fill='#FFFFFF', outline=RED, width=3)
    d.ellipse((x - 12, 264, x + 12, 288), fill=RED)
    d.line((x, 180, x, 250), fill=RED, width=3)
    txt(d, x - 26, 316, 'teshik', 20, RED)
txt(d, 70, 470, 'Cl⁻ ionlari qatlamni nuqta nuqtadan buzadi: teshik ostida pH keskin pasayadi.', 21, N)
txt(d, 70, 515, 'Natija — tez teshik korroziya; ayniqsa yuqori haroratda. HCl HF dan farqli.', 21, B)
txt(d, 70, 580, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'teshikx')

im, d = canvas('HCl saqlash va transport (sxematik)', 660)
boxes = [('A', '30–35 % eritma', 'Rezina qoplama idish', N),
         ('B', 'Konsentratsiyalangan', 'Sovutish va bosim talab', TEAL),
         ('C', 'Transport', 'Maxsus idish, cheklangan', B),
         ('D', 'Tiklash sikli', 'SPL → Fe₂O₃ + HCl', PURPLE)]
for i, (a, b, c, col) in enumerate(boxes):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 170, x + 160, 320), radius=12, outline=col, width=4)
    d.ellipse((x + 52, 185, x + 108, 241), fill=col)
    txt(d, x + 72, 196, a, 28, '#FFFFFF')
    txt(d, x + 12, 255, b, 21, INK)
    txt(d, x + 8, 282, c, 19, G)
    if i < 3:
        d.line((x + 160, 245, x + 178, 245), fill=G, width=4)
txt(d, 40, 370, 'Tanlov mezonlari: reaktivlik (shisha mos emas), nam, temperatura, ifloslanish.', 21, N)
txt(d, 40, 415, 'Konsentratsiyalangan HCl bug‘lanadi — idish yopiq, ventilyatsiya nazoratli bo‘lishi shart.', 21, B)
txt(d, 40, 460, 'Taxminiy hisob: saqlash shartlari konsentratsiya, miqdor va mahalliy qoidalarga bog‘liq.', 21, G)
txt(d, 40, 535, 'Original sxematik chizma; idish turlari shartli.', 21, G)
save(im, 'idishx')

im, d = canvas('Ishlangan hisob: to‘rt shartli hisob (sxematik)', 740)
mn = mannheim(1000.0, 0.98)
n1 = neutralisation(1000.0, 10.0, 'Na2CO3')
rg = regeneration(1000.0)
t = titration_standardisation(0.2500, 24.85)
blocks = [('A — Ishlab chiqarish', '2NaCl + H₂SO₄ → Na₂SO₄ + 2HCl', 'NaCl 1602,8 kg / 1000 kg HCl', N),
          ('B — Neytralizatsiya', '2HCl + Na₂CO₃ → 2NaCl + CO₂ + H₂O', 'Na₂CO₃ 145,3 kg;  kirish = chiqish', TEAL),
          ('C — Metall yemirilishi', 'Fe + 2HCl → FeCl₂ + H₂', '1 g Fe → 2,270 g FeCl₂', B),
          ('D — Kislotani tiklash', '4FeCl₂ + 4H₂O + O₂ → 2Fe₂O₃ + 8HCl', '1000 kg FeCl₂ → HCl 575,3 kg', PURPLE)]
for i, (a, b, cc, col) in enumerate(blocks):
    y = 130 + 125 * i
    d.rounded_rectangle((40, y, 450, y + 100), radius=12, outline=col, width=4)
    txt(d, 60, y + 10, a, 25, col)
    txt(d, 60, y + 44, b, 20, INK)
    txt(d, 60, y + 70, cc, 20, G)
d.rounded_rectangle((470, 130, 712, 530), radius=12, outline=GREEN, width=4)
txt(d, 490, 148, 'Taxminiy hisob natijalari', 24, GREEN)
txt(d, 490, 200, 'ΔrH +884,8 MJ', 20, INK)
txt(d, 490, 235, '(Mannheim usuli)', 19, G)
txt(d, 490, 285, 'NaCl 1602,8 kg', 20, INK)
txt(d, 490, 320, 'Na₂SO₄ 1947,8 kg', 20, INK)
txt(d, 490, 370, 'Fe₂O₃ 629,9 kg', 20, INK)
txt(d, 490, 405, 'HCl tikilgan 575,3 kg', 20, INK)
txt(d, 490, 450, 'C(HCl) 0,18984 mol/L', 19, INK)
txt(d, 490, 485, '(standartlash bo‘yicha shartli hisob)', 19, G)
txt(d, 40, 660, 'Barcha sonlar ochiq shartli hisoblar; o‘lchov ma’lumoti emas.', 21, G)
save(im, 'hisob')
print('5 grafik + CSV; 7 sxema; 5 original illustration.')
