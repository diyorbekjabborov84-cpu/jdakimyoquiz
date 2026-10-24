"""Original teaching figures for 5.1 "Olishning umumiy usullari".
All curves are taxminiy hisob outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_05_01 import (ASSETS as A, eq_conversion, cascade, fenske, pyrite_chain,
                         efactor, dH, dS, dG, lgK, RX_SO2, RX_DIMER, save_data)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'; INK = '#243746'


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

# --- Graph 0: standart Gibbs energiyasi haroratga bog'liqligi --------------
im, d = canvas('Standart Gibbs energiyasi: haroratga bog‘liqlik', 1180)
p = axes(d, 250, 500, -200, 50, 'T, K', 'ΔG°, kJ/mol',
         [(250, '250'), (300, '300'), (350, '350'), (400, '400'), (450, '450'), (500, '500')],
         [(-200, '−200'), (-150, '−150'), (-100, '−100'), (-50, '−50'), (0, '0'), (50, '50')])
rr = rows('dG')
d.line((120, p(250, 0)[1], 680, p(250, 0)[1]), fill=G, width=3)
curve(d, p, rr, 'T_K', 'dG_SO2_kJ', N)
curve(d, p, rr, 'T_K', 'dG_HCl_kJ', B)
curve(d, p, rr, 'T_K', 'dG_N2O4_kJ', TEAL)
txt(d, 45, 865, 'Ko‘k: SO₂ + ½O₂ → SO₃;  bronza: H₂ + Cl₂ → 2HCl', 25, N)
txt(d, 45, 925, 'Teal: N₂O₄ ⇌ 2NO₂;  chiziq ΔG° = 0 — T ≈ 315 K', 25, G)
txt(d, 45, 985, '4NH₃ + 5O₂ → 4NO + 6H₂O: ΔG° ≈ −1011 kJ/mol', 25, G)
txt(d, 45, 1045, 'Shartli hisob egri chizig‘i; tajriba ma’lumoti emas', 25, G)
save(im, 'dG')

# --- Graph 1: N2O4 ⇌ 2 NO2 muvozanat konversiyasi -------------------------
im, d = canvas('Muvozanat konversiyasi: harorat va bosim', 1180)
p = axes(d, 250, 400, 0, 1.0, 'T, K', 'X (konversiya)',
         [(250, '250'), (275, '275'), (300, '300'), (325, '325'), (350, '350'),
          (375, '375'), (400, '400')],
         [(0, '0'), (0.25, '0,25'), (0.5, '0,5'), (0.75, '0,75'), (1, '1')])
rr = rows('mivozanat')
curve(d, p, rr, 'T_K', 'X_1bar', N)
curve(d, p, rr, 'T_K', 'X_10bar', B)
curve(d, p, rr, 'T_K', 'X_100bar', TEAL)
txt(d, 45, 865, 'N₂O₄ ⇌ 2 NO₂ dissotsiatsiyasi; taxminiy egri chiziq', 26, N)
txt(d, 45, 925, '1 bar — ko‘k;  10 bar — bronza;  100 bar — teal', 26, B)
txt(d, 45, 985, '298,15 K: X = 0,269 / 0,088 / 0,028 (1 / 10 / 100 bar)', 25, G)
txt(d, 45, 1045, 'Ideal gaz; ΔH°, ΔS° doimiy; tajriba ma’lumoti emas', 25, G)
save(im, 'mivozanat')

# --- Graph 2: kaskad — umumiy konversiya ---------------------------------
im, d = canvas('Kaskad: bosqichlar soni va umumiy konversiya', 1180)
p = axes(d, 1, 40, 0, 1.0, 'N (bosqichlar soni)', 'X umumiy',
         [(1, '1'), (5, '5'), (10, '10'), (20, '20'), (30, '30'), (40, '40')],
         [(0, '0'), (0.25, '0,25'), (0.5, '0,5'), (0.75, '0,75'), (1, '1')])
rr = rows('kaskad')
curve(d, p, rr, 'N', 'X_umumiy_x0.4', TEAL)
curve(d, p, rr, 'N', 'X_umumiy_x0.6', N)
curve(d, p, rr, 'N', 'X_umumiy_x0.8', B)
txt(d, 45, 865, 'X umumiy = 1 − (1 − x₁)^N', 27, N)
txt(d, 45, 925, 'x₁ = 0,4 — teal;  0,6 — ko‘k;  0,8 — bronza', 26, B)
txt(d, 45, 985, 'x₁ = 0,60: N = 1 → 0,60;  N = 2 → 0,84;  N = 5 → 0,990', 25, G)
txt(d, 45, 1045, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 25, G)
save(im, 'kaskad')

# --- Graph 3: ajratish — minimal pog‘onalar soni ---------------------------
im, d = canvas('Ajratish qiyinligi: nisbiy uchuvchanlik', 1180)
p = axes(d, 1.05, 10.0, 0, 130, 'α (nisbiy uchuvchanlik)', 'N min (pog‘ona)',
         [(2, '2'), (4, '4'), (6, '6'), (8, '8'), (10, '10')],
         [(0, '0'), (20, '20'), (40, '40'), (60, '60'), (80, '80'), (100, '100'), (130, '130')])
rr = rows('buglanish')
curve(d, p, rr, 'alpha', 'N_min', N, ylo=0, yhi=130)
curve(d, p, rr, 'alpha', 'N_min_xD99', B, ylo=0, yhi=130)
txt(d, 45, 865, 'Fenske: N min = lg[(xD/(1−xD))·((1−xB)/xB)] / lg α', 26, N)
txt(d, 45, 925, 'xD = 0,95 (ko‘k);  xD = 0,99 (bronza)', 25, B)
txt(d, 45, 985, 'α = 1,1 → 61,8 pog‘ona;  α = 2,0 → 8,5;  α = 5,0 → 3,7', 25, G)
txt(d, 45, 1045, 'Shartli hisob egri chizig‘i; tajriba ma’lumoti emas', 25, G)
save(im, 'buglanish')

# --- Graph 4: resurs samaradorligi — chiqindi omili ------------------------
im, d = canvas('Resurs samaradorligi: chiqindi omili', 1180)
p = axes(d, 0.50, 1.0, 0.40, 1.60, 'X (SO₂ → SO₃ konversiyasi)', 'E (kg/kg)',
         [(0.5, '0,5'), (0.6, '0,6'), (0.7, '0,7'), (0.8, '0,8'), (0.9, '0,9'), (1.0, '1,0')],
         [(0.4, '0,4'), (0.6, '0,6'), (0.8, '0,8'), (1.0, '1,0'),
          (1.2, '1,2'), (1.4, '1,4'), (1.6, '1,6')])
rr = rows('chiqindi')
curve(d, p, rr, 'X_SO3', 'E_factor', N, ylo=0.40, yhi=1.60)
x, y = p(0.96, efactor(0.96))
d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=B)
txt(d, x - 210, y - 52, 'X = 0,96 → 0,46 kg/kg', 25, B)
txt(d, 45, 865, 'E = m(chiqindi) / m(mahsulot);  1000 t pyrit bo‘yicha shartli hisob', 26, N)
txt(d, 45, 925, 'Chiqqindi: Fe₂O₃ qoldig‘i va qolgan SO₂', 26, G)
txt(d, 45, 985, 'X = 0,90 → 0,54;  0,96 → 0,46;  0,99 → 0,43 kg/kg', 25, G)
txt(d, 45, 1045, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 25, G)
save(im, 'resurs')


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


scheme('usullar', 'Kislota olishning asosiy usullari', [
    ('To‘g‘ridan-to‘g‘ri birikish', 'H₂ + Cl₂ → 2HCl', 'Yon mahsulot yo‘q'),
    ('Oksidlash zanjiri', 'S → SO₂ → SO₃', 'Ko‘p bosqich ketma-ket'),
    ('Tuzdan siqish', 'Tuz + kuchliroq kislota', 'Kislotaning tuzini sarflaydi'),
    ('Gidroliz', 'Galogenid + H₂O → kislota', 'Suv bilan birga chiqadi'),
    ('Elektrokimyaviy usul', 'm = MQ/(zF)', 'Tok manbai kerak')])

scheme('mezon', 'Usulni tanlash mezonlari', [
    ('1. Termodinamik', 'ΔG° < 0 bo‘lishi kerak', 'K qanchalik katta?'),
    ('2. Kinetik', 'Aktivatsiya to‘sig‘i', 'Katalizator mumkinmi?'),
    ('3. Texnologik', 'Ajratish va konsentratsiya', 'Chiqindi qancha?'),
    ('4. Xavfsizlik va ekologiya', 'Chiqariladigan gazlar', 'Yutish imkoni bormi?'),
    ('5. Yekuniy qaror', 'Barcha mezonlar birga', 'Usul va sxema tanlanadi')])

scheme('qalqon', 'Kinetik to‘siqlar va ularning yechimi', [
    ('Reagent donadorligi', 'Reaksiya faqat yuzada', 'Reagent usuli'),
    ('Qalqon usuli', 'Reaksiya qalqon bilan boshqariladi', 'Qalqon asta ochiladi'),
    ('Fazalararo mass transfer', 'Interfeysda reagent tanqisligi', 'Aralashuv va doljinka'),
    ('Harorat profili', 'Issiq nuqta hosil bo‘ladi', 'Profilni boshqarish')])

scheme('sxema', 'Sanoat sxemasining asosiy bloklari', [
    ('Xom ashyo', 'Kerakli modda kiritish', 'Tarkib va namdorlik nazorati'),
    ('Reagent tayyorlash', 'Eritma yoki gaz', 'Konsentratsiya va tozalik'),
    ('Reaksiya', 'Kimyoviy o‘zgarish', 'Konversiya va selektivlik'),
    ('Fazalarni ajratish', 'Cho‘kma va suyuq', 'Qoldiq miqdori'),
    ('Absorbsiya', 'Gazni suyuq fazaga o‘tkazish', 'Yutilish unumi'),
    ('Tozalash va konsentratsiya', 'Suv va ifloslikni olib tashlash', 'Mass ulushi va zichlik')])

scheme('sifat', 'Tayyor kislota sifati: tekshiruv nuqtalari', [
    ('Kislota miqdori', 'Titrlash', 'c = n(titrant)/V'),
    ('Zichlik', 'Areometr', 'Solishtirish uchun'),
    ('Rang', 'Ko‘z va spektroskopiya', 'NO₂ kabi nishonlar'),
    ('Metallar', 'ICP spektrometriyasi', 'Katalizator qoldig‘i'),
    ('Suv miqdori', 'Karl Fischer usuli', 'Kondensatsiya darajasi'),
    ('Hujjatlashtirish', 'Partiya, metod, natija, sana', 'Mas’ul shaxs')])


scheme('chiqindi', 'Chiqindini ushlash va tiklash sikli', [
    ('Chiqindi manbasi', 'Reaksiya va ajratish', 'Gaz yoki suyuq chiqindi'),
    ('Yig‘ish', 'Chiqindi yaxlitlanadi', 'Kontsentratsiya oshadi'),
    ('Yutish', 'Suyuq fazaga o‘tkaziladi', 'Mahsulotga aylantiriladi'),
    ('Tiklash', 'Reagentga qaytarish', 'Resurs qaytadi'),
    ('Yo‘qotish', 'To‘liq chiqindiga berish', 'Resurs yo‘qoladi; ekologik mezon')])

# --- Original schematic illustrations ---------------------------------------
def base(t, h=590):
    return canvas(t, h)


im, d = base('Material oqimi: kirish, mahsulot va chiqindi')
d.rounded_rectangle((60, 180, 250, 300), radius=12, outline=N, width=4)
txt(d, 85, 220, 'Xom ashyo', 27, N)
d.rounded_rectangle((300, 180, 470, 300), radius=12, outline=N, width=4)
txt(d, 335, 220, 'Reaksiya', 27, N)
d.rounded_rectangle((530, 140, 700, 240), radius=12, outline=TEAL, width=4)
txt(d, 560, 175, 'Mahsulot', 26, TEAL)
d.rounded_rectangle((530, 260, 700, 360), radius=12, outline=B, width=4)
txt(d, 560, 295, 'Chiqindi', 26, B)
d.line((250, 240, 300, 240), fill=G, width=5)
d.polygon([(300, 240), (280, 228), (280, 252)], fill=G)
d.line((470, 220, 530, 190), fill=TEAL, width=4)
d.polygon([(530, 190), (510, 182), (516, 204)], fill=TEAL)
d.line((470, 260, 530, 310), fill=B, width=4)
d.polygon([(530, 310), (510, 302), (516, 324)], fill=B)
txt(d, 35, 430, 'Har bir oqim miqdori bilan hisoblanadi: kirish = mahsulot + chiqindi', 23, G)
txt(d, 35, 480, 'Sxematik; mass oqimi taxminiy hisobi', 23, G)
save(im, 'oqim')

im, d = base('Reagent donador qatlami va diffuziya qatlami')
d.rectangle((60, 330, 700, 470), fill='#E4D2B0')
for i in range(9):
    x = 90 + i * 70
    d.ellipse((x, 350, x + 44, 440), outline=N, width=4)
txt(d, 95, 480, 'Reagent donalari — reaksion yuzasi', 24, N)
d.rectangle((60, 270, 700, 330), fill='#DCEBF4')
txt(d, 95, 285, 'Diffuziya qatlami', 24, TEAL)
d.rectangle((60, 150, 700, 270), fill='#EAF1E4')
txt(d, 95, 165, 'Reagent oqimi (yuqoridan pastga)', 24, G)
d.line((380, 200, 380, 290), fill=B, width=4)
d.polygon([(380, 290), (366, 266), (394, 266)], fill=B)
txt(d, 35, 525, 'Tezlik diffuziya bilan cheklanishi mumkin; sxematik kesim', 22, G)
save(im, 'qatlam')

im, d = base('Rektifikatsiya kolonkasi (sxematik kesim)')
d.rectangle((300, 90, 460, 470), outline=N, width=4)
for i in range(6):
    y = 130 + i * 55
    d.line((300, y, 460, y), fill=G, width=3)
txt(d, 320, 100, 'Kolonka', 26, N)
d.line((150, 250, 300, 250), fill=B, width=4)
d.polygon([(300, 250), (278, 238), (278, 262)], fill=B)
txt(d, 60, 210, 'Kirish aralashmasi', 24, B)
d.line((380, 90, 380, 40), fill=TEAL, width=4)
d.polygon([(380, 40), (366, 64), (394, 64)], fill=TEAL)
txt(d, 395, 35, 'Distillyat', 24, TEAL)
d.line((380, 470, 380, 520), fill=G, width=4)
d.polygon([(380, 520), (366, 496), (394, 496)], fill=G)
txt(d, 395, 495, 'Qoldiq', 24, G)
txt(d, 35, 545, 'Sxematik kesim; real kolonka 5.2-bo‘limda', 22, G)
save(im, 'kolonka')

im, d = base('Reaktorda harorat profili va issiq nuqta')
pts = [(90, 430), (170, 400), (260, 350), (350, 250), (430, 200), (520, 260), (640, 330)]
d.line(pts, fill=N, width=5)
for x, y in pts:
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=B)
d.ellipse((415, 185, 445, 215), outline=B, width=4)
txt(d, 330, 130, 'Issiq nuqta', 25, B)
d.line((90, 470, 640, 470), fill=G, width=3)
txt(d, 95, 480, 'Reaktor uzunligi', 24, G)
txt(d, 70, 520, 'Sxematik profil; qiymatlar o‘lchovdan olingan emas', 23, G)
save(im, 'profil')

im, d = base('Xavfsizlik zaxirasi: asosiy va ikkilamchi to‘siq')
d.rounded_rectangle((250, 150, 470, 430), radius=18, outline=N, width=4)
txt(d, 300, 250, 'Idish', 30, N)
d.rounded_rectangle((200, 120, 520, 460), radius=18, outline=TEAL, width=4)
txt(d, 225, 95, 'Asosiy to‘siq', 25, TEAL)
d.rounded_rectangle((150, 90, 570, 490), radius=18, outline=B, width=4)
txt(d, 165, 60, 'Ikkilamchi to‘siq', 25, B)
txt(d, 35, 525, 'Sxematik; idish materiali va hajm hisoblanmaydi', 23, G)
save(im, 'zaxira')

# --- Shartli hisob zanjiri: pyritdan sulfat kislotagacha --------------------------
im, d = base('Shartli hisob zanjiri: pyritdan sulfat kislotagacha', 620)
steps = [('FeS₂', '1000 t', N), ('SO₂', '16 669 kmol', N),
         ('SO₃', '16 003 kmol', N), ('H₂SO₄', '1538,15 t', TEAL)]
x0 = 40
for i, (name, val, col) in enumerate(steps):
    x = x0 + i * 180
    d.rounded_rectangle((x, 180, x + 150, 300), radius=12, outline=col, width=4)
    txt(d, x + 42, 200, name, 30, col)
    txt(d, x + 26, 254, val, 19, INK)
    if i < 3:
        d.line((x + 150, 240, x + 176, 240), fill=G, width=4)
        d.polygon([(x + 176, 240), (x + 158, 230), (x + 158, 250)], fill=G)
d.rounded_rectangle((40, 340, 340, 450), radius=12, outline=B, width=4)
txt(d, 95, 360, 'Fe₂O₃ qoldig‘i', 26, B)
txt(d, 80, 405, '665,49 t — chiqindi', 22, INK)
d.line((115, 300, 115, 340), fill=B, width=4)
d.polygon([(115, 340), (104, 318), (126, 318)], fill=B)
txt(d, 360, 360, 'Unum 94,08 %', 26, N)
txt(d, 360, 405, 'Chiqindi omili 0,46 kg/kg', 22, INK)
txt(d, 40, 490, 'Taxminiy hisob zanjir; ΔH° va ΔS° doimiy, tajriba ma’lumoti emas', 23, G)
txt(d, 40, 545, 'Harorat, bosim va reaktorni yig‘ish ko‘rsatmalari berilmaydi', 23, G)
save(im, 'hisob')

print('5 grafik + CSV; 6 sxema; 6 original illustration.')
