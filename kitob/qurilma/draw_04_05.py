"""Original teaching figures for 4.5 "Parchalanish".
All curves are model outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from decomp_04_05 import (ASSETS as A, dH, dS, dG, lgK, lnK, t_star, arrhenius_k,
                          half_life, sulfite_fractions, RX_HNO3, RX_H2SO4,
                          RX_H2O2, T0, save_data)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'


def font(n):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', n)


def txt(d, x, y, s, n=28, c=N):
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


def rows(n):
    return [{k: float(v) for k, v in r.items()}
            for r in csv.DictReader((A / (n + '.csv')).open())]


def axes(d, xlo, xhi, ylo, yhi, xlabel, ylabel, xt, yt):
    def p(x, y):
        return (120 + (x - xlo) / (xhi - xlo) * 560, 700 - (y - ylo) / (yhi - ylo) * 525)
    d.line((120, 175, 120, 700, 680, 700), fill=G, width=3)
    for x, s in xt:
        txt(d, p(x, ylo)[0] - 15, 718, s, 24)
    for y, s in yt:
        txt(d, 20, p(xlo, y)[1] - 16, s, 24)
    txt(d, 45, 108, ylabel, 28)
    txt(d, 145, 780, xlabel, 27)
    return p


def curve(d, p, rr, x, y, col, ylo=None, yhi=None):
    line = []
    for r in rr:
        if (ylo is None or ylo <= r[y]) and (yhi is None or r[y] <= yhi):
            line.append(p(r[x], r[y]))
        else:
            if len(line) > 1:
                d.line(line, fill=col, width=5)
            line = []
    if len(line) > 1:
        d.line(line, fill=col, width=5)


save_data()

# --- Graph 1: ΔG° as a function of temperature -------------------------------
dh1, ds1 = dH(*RX_HNO3), dS(*RX_HNO3)
dh2, ds2 = dH(*RX_H2SO4), dS(*RX_H2SO4)
im, d = canvas('Gibbs energiyasi va parchalanish chegarasi', 1180)
p = axes(d, 250, 1000, -350, 100, 'T, K', 'ΔG°, kJ/mol',
         [(250, '250'), (400, '400'), (600, '600'), (780, '780'), (1000, '1000')],
         [(-350, '−350'), (-200, '−200'), (-50, '−50'), (0, '0'), (50, '50'), (100, '100')])
rr = rows('dG')
curve(d, p, rr, 'T_K', 'dG_HNO3_kJ', N, ylo=-350, yhi=100)
curve(d, p, rr, 'T_K', 'dG_H2SO4_kJ', B, ylo=-350, yhi=100)
x, y = p(779.7, 0.0)
d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=TEAL)
d.line((x, 700, x, y), fill=TEAL, width=3)
d.line((320, 318, 500, 300), fill=TEAL, width=2)
txt(d, 140, 290, 'T* ≈ 780 K', 25, TEAL)
txt(d, 140, 330, 'bu nuqtada K = 1', 24, TEAL)
txt(d, 45, 865, 'HNO₃ → NO₂ + H₂O + ½O₂ — ko‘k egri chiziq', 26, N)
txt(d, 45, 925, 'H₂SO₄ → SO₃ + H₂O — bronza egri chiziq', 26, B)
txt(d, 45, 985, 'ΔH°, ΔS° doimiy; standart holat modeli', 25, G)
txt(d, 45, 1045, 'Model egri chizig‘i; tajriba ma’lumoti emas', 25, G)
save(im, 'dG')

# --- Graph 2: equilibrium constant versus temperature ------------------------
im, d = canvas('Muvozanat konstantasining haroratga bog‘liqligi', 1180)
p = axes(d, 550, 1200, -4, 4, 'T, K', 'lg K',
         [(600, '600'), (780, '780'), (900, '900'), (1000, '1000'), (1200, '1200')],
         [(-4, '−4'), (-2, '−2'), (0, '0'), (2, '2'), (4, '4')])
rr = rows('K')
curve(d, p, rr, 'T_K', 'lgK_H2SO4', N, ylo=-4, yhi=4)
x, y = p(779.7, 0.0)
d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=B)
txt(d, x - 130, 640, 'K = 1', 25, B)
txt(d, 45, 865, 'H₂SO₄(l) → SO₃(g) + H₂O(l)', 28, N)
txt(d, 45, 925, 'ln K = −ΔH°/RT + ΔS°/R (van ’t Hoff)', 26, G)
txt(d, 45, 985, 'K(298 K) ≈ 4,8×10⁻¹⁵;  K(1000 K) ≈ 90', 25, G)
txt(d, 45, 1045, 'Model egri chizig‘i; tajriba ma’lumoti emas', 25, G)
save(im, 'K')

# --- Graph 3: Arrhenius model ------------------------------------------------
im, d = canvas('Kinetika: harorat parchalanishni tezlashtiradi', 1180)
p = axes(d, 250, 450, -6, 2, 'T, K', 'lg k, s⁻¹',
         [(250, '250'), (300, '300'), (350, '350'), (400, '400'), (450, '450')],
         [(-6, '−6'), (-4, '−4'), (-2, '−2'), (0, '0'), (2, '2')])
rr = rows('kinetics')
curve(d, p, rr, 'T_K', 'log10_k', N, ylo=-6, yhi=2)
for T in (298.15, 320, 350, 400):
    x, y = p(T, math.log10(arrhenius_k(T)))
    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=B)
txt(d, 45, 865, 'k = A·exp(−Ea/RT)', 28, N)
txt(d, 45, 925, 'Model: A = 1,0×10¹³ s⁻¹, Ea = 100 kJ/mol', 26, G)
txt(d, 45, 985, 't½: 298 K ≈ 6,4 soat;  350 K ≈ 58 s', 25, G)
txt(d, 45, 1045, 'Model egri chizig‘i; aniq kislotga tegishli emas', 25, G)
save(im, 'kinetics')

# --- Graph 4: sulfite speciation versus pH ----------------------------------
im, d = canvas('pH ning S(IV) tarkibiga ta’siri', 1180)
p = axes(d, 1, 12, 0, 1, 'pH', 'Ulush',
         [(1, '1'), (3, '3'), (5, '5'), (7, '7'), (9, '9'), (12, '12')],
         [(0, '0'), (.25, '0,25'), (.5, '0,5'), (.75, '0,75'), (1, '1')])
rr = rows('sulfite')
curve(d, p, rr, 'pH', 'alpha_SO2aq', N, ylo=0, yhi=1)
curve(d, p, rr, 'pH', 'alpha_HSO3', B, ylo=0, yhi=1)
curve(d, p, rr, 'pH', 'alpha_SO3', TEAL, ylo=0, yhi=1)
txt(d, 45, 855, 'Erkin SO₂·H₂O — ko‘k egri chiziq', 26, N)
txt(d, 45, 905, 'HSO₃⁻ — bronza;  SO₃²⁻ — teal egri chiziq', 26, B)
txt(d, 45, 955, 'Ka1 = 1,6×10⁻²;  Ka2 = 6,4×10⁻⁸ (25 °C)', 26, G)
txt(d, 45, 1005, 'pH 1 da α(SO₂·H₂O) = 0,862;  pH 7 da = 3,8×10⁻⁶', 25, G)
txt(d, 45, 1055, 'Hisob egri chizig‘i; tajriba ma’lumoti emas', 25, G)
save(im, 'sulfite')


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


scheme('turlar', 'Parchalanishning asosiy yo‘nalishlari', [
    ('Termik', 'H₂SO₄ → SO₃ + H₂O', 'Energiya haroratdan olinadi'),
    ('Fotokimyoviy', 'HNO₃ → NO₂ + H₂O + ½O₂', 'Energiya yorug‘likdan olinadi'),
    ('Katalitik', 'H₂O₂ → H₂O + ½O₂', 'To‘siq katalizator bilan pasayadi'),
    ('Dismutatsion', '3HNO₂ → HNO₃ + 2NO + H₂O', 'Bitta element ikki yo‘naladi'),
    ('Kondensatsion', '2H₃PO₄ → H₄P₂O₇ + H₂O', 'Suv ajratib oligomer hosil bo‘ladi')])

scheme('fotokimyo', 'Fotokimyoviy zanjirning to‘rt bosqichi', [
    ('Boshlanish', 'Fotonly energiya beradi', 'Radikal yoki qo‘shimcha tuzilma'),
    ('Davom', 'Radikal yangi radikal hosil qiladi', 'Zanjir uzluksiz davom etadi'),
    ('Tarmoqlanish', 'Bitta o‘lchovdan ko‘p zanjir', 'Jarayon tezlashadi'),
    ('Tugatish', 'Radikallar bir-birini yo‘q qiladi', 'Zanjir uziladi')])

scheme('dismutatsiya', 'Dismutatsiya: bitta elementning ikki yo‘li', [
    ('Kirish holati', 'Nitrit kislota: N (+3)', 'Nitrat kislota ta’minlanadi'),
    ('Oksidlanish', 'N (+3) → N (+5)', 'HNO₃ hosil bo‘ladi'),
    ('Qaytarilish', 'N (+3) → N (+2)', 'NO hosil bo‘ladi'),
    ('Natija', 'Kislota tarkibi butunlay o‘zgardi', 'Titrlash butun kislotani o‘lchaydi')])

scheme('kondensatsiya', 'Kondensatsiya: monomerdan zanjirgacha', [
    ('Orto shakl', 'H₃PO₄', 'Suv ajratib pyrofosfat'),
    ('Piro shakl', 'H₄P₂O₇', 'Yana suv ajratib metafosfat'),
    ('Meta shakl', 'HPO₃', 'Polifosfat kislotalar'),
    ('Boshqa yo‘l', 'H₂SO₄ + SO₃ → H₂S₂O₇', 'Oleum; teskari yo‘nalish ekzotermik')])

scheme('saqlash', 'Saqlashning to‘rt asosiy omili', [
    ('Harorat', 'Sovuq sharoitda saqlash', 'Kinetik blok kuchayadi'),
    ('Yorug‘lik', 'Qorong‘i idish', 'Fotokimyaviy parchalanish bo‘lmaydi'),
    ('Ifloslik', 'Toza ushbu va idish', 'Katalizator bo‘lib chiqmaydi'),
    ('Hujjat', 'Ochilish va sarflanish sanasi', 'Muddat nazorati')])

scheme('tahlil', 'Parchalanish mahsulotlarini aniqlash', [
    ('Qolgan kislota', 'Titratsiya, pH o‘lchash', 'Nimani o‘lchayotganini yozish kerak'),
    ('Rangli mahsulot', 'UV–Vis spektroskopiyasi', 'NO₂, ClO₂ kabi turlar'),
    ('Uchuvchi mahsulot', 'Boshlash gazi xromatografiyasi', 'Sarf bo‘lishini ko‘rsatadi'),
    ('Tarkib', 'Ion va element tahlili', 'Anionlar, metall qoldig‘i')])

scheme('hisob', 'Hisob natijasi: termodinamik va kinetik', [
    ('ΔH°', '+132,44 kJ/mol', 'Endotermik: SO₃ va suv ajraladi'),
    ('ΔS°', '169,86 J/(mol·K)', 'Entropiya ortadi'),
    ('ΔG°(298,15)', '+81,80 kJ/mol', '298 K da qulay emas'),
    ('T*', '779,7 K ≈ 507 °C', 'K = 1 bo‘lgan nuqta'),
    ('Kinetik model', '298 K → 6,4 soat; 350 K → 58 s', 'Saqlash cheklovi kinetik')])

# --- Original schematic illustrations ---------------------------------------
def base(t, h=590):
    return canvas(t, h)

im, d = base('Energiya profili: termodinamik qulay, lekin kinetik blok')
pts = [(90, 430), (210, 400), (300, 190), (390, 400), (520, 360), (640, 330)]
d.line(pts, fill=N, width=5)
for x, y in pts:
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=B)
d.line((90, 470, 640, 470), fill=G, width=3)
txt(d, 95, 480, 'Reaktsiya yo‘li', 24, G)
txt(d, 258, 130, 'Aktivatsiya to‘sig‘i', 25, B)
txt(d, 70, 520, 'Mahsulotlar energetik jihatdan pastda — ΔG < 0', 24, N)
txt(d, 35, 555, 'Sxematik; energiya profili tajribadan o‘lchanmagan', 22, G)
save(im, 'profil')

im, d = base('Radikal zanjiri: ko‘payish va tugatish')
d.ellipse((120, 200, 240, 320), outline=N, width=4)
txt(d, 150, 235, 'R•', 34, N)
d.ellipse((420, 200, 540, 320), outline=N, width=4)
txt(d, 450, 235, 'R•', 34, N)
d.line((250, 260, 410, 260), fill=B, width=5)
d.polygon([(420, 260), (398, 246), (398, 274)], fill=B)
txt(d, 265, 215, '+ M → RM•', 26, B)
d.rounded_rectangle((300, 360, 460, 460), radius=12, outline=TEAL, width=4)
txt(d, 325, 390, 'Yangi zanjir', 26, TEAL)
d.line((180, 330, 330, 360), fill=G, width=3)
d.line((480, 330, 400, 360), fill=G, width=3)
txt(d, 35, 505, 'Radikal juftlanishi; mexanizm sxemasi', 23, G)
save(im, 'zanjir')

im, d = base('Sargayish: mahsulot to‘shishi belgisi')
d.rounded_rectangle((150, 130, 610, 460), radius=18, outline=N, width=4)
d.rectangle((170, 150, 590, 440), fill='#E4D2B0')
d.rectangle((250, 100, 510, 140), fill=N)
txt(d, 285, 92, '', 20)
txt(d, 215, 250, 'Kislota', 34, N)
txt(d, 205, 310, 'NO₂ to‘shishi', 26, B)
txt(d, 205, 360, 'rang — miqdor emas', 24, G)
txt(d, 35, 505, 'Sxematik idish; rang o‘lchovi konsentratsiya emas', 23, G)
save(im, 'sargayish')

im, d = base('Kondensatsiya: monomerdan oligomerga')
for i in range(4):
    x = 90 + i * 150
    d.rounded_rectangle((x, 210, x + 110, 320), radius=10, outline=N, width=4)
    txt(d, x + 30, 240, 'M', 34, N)
    if i < 3:
        d.line((x + 110, 265, x + 150, 265), fill=B, width=5)
d.line((90, 350, 640, 350), fill=G, width=3)
txt(d, 95, 360, 'monomer → oligomer → zanjir (sxematik)', 25, G)
txt(d, 35, 505, 'Zanjir uzunligi shartli; molekula masshtabi emas', 23, G)
save(im, 'kondzanjir')

im, d = base('pH bilan S(IV) ning uch shakli')
d.rectangle((60, 150, 330, 400), fill='#DCEBF4')
txt(d, 95, 185, 'Kislotali muhit', 29, N)
txt(d, 110, 265, 'SO₂·H₂O', 32)
txt(d, 95, 330, 'Gaz holatiga chiqadi', 25, G)
d.rectangle((440, 150, 710, 400), fill='#EAF1E4')
txt(d, 475, 185, 'Ishqoriy muhit', 29, N)
txt(d, 500, 265, 'HSO₃⁻, SO₃²⁻', 30)
txt(d, 460, 330, 'Gaz ajralishi to‘siqlanadi', 25, G)
d.line((330, 275, 440, 275), fill=B, width=5)
d.polygon([(440, 275), (418, 262), (418, 288)], fill=B)
txt(d, 35, 505, 'Sxematik; muvozanat grafigi alohida ko‘rsatilgan', 23, G)
save(im, 'phshakli')

print('4 grafik + CSV; 7 sxema; 5 original illustration.')
