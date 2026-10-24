"""Original teaching figures for 5.2 "Kislotalarni tozalash".
All curves are taxminiy hisob outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_05_02 import (ASSETS as A, metal_solubility, cu_with_ammonia, KSP,
                         cascade_purity, y_eq, mccabe_thiele, water_removal,
                         thomas, breakthrough_bv, no2_to_hno3,
                         fe_precipitation, save_data)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'; INK = '#243746'
PURPLE = '#6C3483'; RED = '#C0392B'


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


def curve(d, p, rr, x, y, col, ylo=None, yhi=None, width=5):
    line = []
    for r in rr:
        if (ylo is None or ylo <= r[y]) and (yhi is None or r[y] <= yhi):
            line.append(p(r[x], r[y]))
        else:
            if len(line) > 1:
                d.line(line, fill=col, width=width)
            line = []
    if len(line) > 1:
        d.line(line, fill=col, width=width)


save_data()

# --- Graph 0: tozalash kaskadi — ifloslik pasayishi -----------------------
im, d = canvas('Tozalash kaskadi: ifloslik pasayishi', 1180)
p = axes(d, 1, 40, -13, 0, 'N (ajratish bosqichi)', 'lg(c/c₀)',
         [(1, '1'), (10, '10'), (20, '20'), (30, '30'), (40, '40')],
         [(-12, '−12'), (-10, '−10'), (-8, '−8'), (-6, '−6'), (-4, '−4'),
          (-2, '−2'), (0, '0')])
rr = rows('kaskad')
curve(d, p, rr, 'N', 'log10_c_phi10', N, ylo=-13, yhi=0)
curve(d, p, rr, 'N', 'log10_c_phi100', B, ylo=-13, yhi=0)
curve(d, p, rr, 'N', 'log10_c_phi1000', TEAL, ylo=-13, yhi=0)
curve(d, p, rr, 'N', 'log10_c_phi10000', G, ylo=-13, yhi=0)
d.line((120, p(1, -6)[1], 680, p(1, -6)[1]), fill='#C9D4DD', width=3)
txt(d, 300, p(1, -6)[1] - 34, 'reagent darajasi: 10⁻⁶', 24, G)
txt(d, 45, 865, 'c/c₀ = (1/Φ)ᴺ — ajratish faktori Φ ga bog‘liq pasayish', 25, N)
txt(d, 45, 920, 'ko‘k: Φ = 10;  bronza: 100;  teal: 1000;  kul: 10000', 25, B)
txt(d, 45, 975, '10⁻⁶ gacha: Φ = 10 → 6 bosqich;  100 → 3;  1000 → 2', 24, G)
txt(d, 45, 1030, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 24, G)
save(im, 'kaskad')

# --- Graph 1: cho'ktirish — metall qoldig'i pH ga bog'liqligi -------------
im, d = canvas('Cho‘ktirish: metall qoldig‘i va pH', 1180)
p = axes(d, 0, 14, -20, 0, 'pH', 'lg[M], M',
         [(0, '0'), (2, '2'), (4, '4'), (6, '6'), (8, '8'), (10, '10'),
          (12, '12'), (14, '14')],
         [(-20, '−20'), (-16, '−16'), (-12, '−12'), (-8, '−8'), (-4, '−4'), (0, '0')])
rr = rows('choqish')


def logcurve(col, key):
    line = []
    for r in rr:
        v = math.log10(max(r[key], 1e-20))
        if v > 0:
            if len(line) > 1:
                d.line(line, fill=col, width=5)
            line = []
            continue
        line.append(p(r['pH'], v))
    if len(line) > 1:
        d.line(line, fill=col, width=5)


logcurve(N, 'Fe3')
logcurve(B, 'Cu2')
logcurve(TEAL, 'Ni2')
logcurve(G, 'Cd2')
logcurve(PURPLE, 'Pb2')
pts = []
for r in rr:
    v = math.log10(max(r['Cu2_NH3'], 1e-20))
    if v <= 0:
        pts.append(p(r['pH'], v))
for i in range(0, len(pts) - 1, 6):
    d.line((pts[i], pts[i + 1]), fill=RED, width=4)
xm, ym = p(2, math.log10(1.29e-9))
d.ellipse((xm - 7, ym - 7, xm + 7, ym + 7), fill=RED)
txt(d, 45, 865, '[Mⁿ⁺] = Ksp / [OH⁻]ⁿ;  lg[M] = lg Ksp − n·lg[OH⁻]', 25, N)
txt(d, 45, 920, 'ko‘k: Fe(OH)₃;  bronza: Cu(OH)₂;  teal: Ni(OH)₂;  kul: Cd(OH)₂', 23, B)
txt(d, 45, 975, 'binafsha: Pb(OH)₂;  qizil punktli: Cu²⁺ + 4NH₃ (1,0 M)', 23, PURPLE)
txt(d, 45, 1030, 'pH 2: Fe³⁺ 4,0×10⁻² M;  pH 7: Cu²⁺ 2,2×10⁻⁶ M;  pH 8: Cd²⁺ 5,9×10⁻³ M', 22, G)
txt(d, 45, 1080, 'Ksp: OpenStax App. J;  taxminiy egri chiziq — o‘lchov ma’lumoti emas', 22, G)
save(im, 'choqish')

# --- Graph 2: rektifikatsiya — x-y diagrammasi ----------------------------
im, d = canvas('Rektifikatsiya: McCabe-Thiele diagrammasi', 1180)
p = axes(d, 0, 1, 0, 1, 'x (uchuvchan komponent)', 'y',
         [(0, '0'), (0.2, '0,2'), (0.4, '0,4'), (0.6, '0,6'), (0.8, '0,8'), (1, '1')],
         [(0, '0'), (0.2, '0,2'), (0.4, '0,4'), (0.6, '0,6'), (0.8, '0,8'), (1, '1')])
rr = rows('rektifikatsiya')
curve(d, p, rr, 'x', 'y_a1.5', G, width=4)
curve(d, p, rr, 'x', 'y_a2', B)
curve(d, p, rr, 'x', 'y_a3', TEAL)
d.line((p(0, 0), p(1, 1)), fill='#9FB0BD', width=3)
mct = mccabe_thiele(2.0)
ar, br = mct['rect']
ast, bst = mct['strip']
xq = mct['xq']
y_int = ar * xq + br
d.line((p(xq, y_int), p(0.95, 0.95)), fill=PURPLE, width=4)
d.line((p(0.05, 0.05), p(xq, y_int)), fill=PURPLE, width=4)
pts = [(r['x'], r['y']) for r in rows('mcbabgele')]
for i in range(len(pts) - 1):
    d.line((p(pts[i][0], pts[i][1]), p(pts[i + 1][0], pts[i + 1][1])),
           fill=INK, width=3)
d.ellipse((p(0.95, 0.95)[0] - 6, p(0.95, 0.95)[1] - 6,
           p(0.95, 0.95)[0] + 6, p(0.95, 0.95)[1] + 6), fill=N)
txt(d, 45, 865, 'Muvozanat: y = αx/(1 + (α−1)x);  diagonal: y = x', 25, N)
txt(d, 45, 920, 'kul: α = 1,5;  bronza: 2,0;  teal: 3,0  (taxminiy hisoblar, doimiy α)', 24, B)
txt(d, 45, 975, 'α = 2,0: N = 16 pog‘ona (q = 1, R = 2,0, xF = 0,50)', 24, INK)
txt(d, 45, 1030, 'R_min = 1,70;  α = 1,5: R_min = 3,50 > R (mumkin emas)', 23, G)
txt(d, 45, 1080, 'Taxminiy hisob: real kislota–suv tizimi ideal emas', 23, G)
save(im, 'rektifikatsiya')

# --- Graph 3: suvni olib tashlash ----------------------------------------
im, d = canvas('Konsentratsiyalash: olib tashlanadigan suv', 1180)
p = axes(d, 0.1, 1.0, 0, 100, 'boshlang‘ich mass ulushi w₀', 'suv, kg / 100 kg',
         [(0.1, '0,1'), (0.3, '0,3'), (0.5, '0,5'), (0.7, '0,7'), (0.9, '0,9'), (1.0, '1,0')],
         [(0, '0'), (20, '20'), (40, '40'), (60, '60'), (80, '80'), (100, '100')])
rr = rows('buglash')
curve(d, p, rr, 'w0', 'out_to_0.99', N, ylo=0, yhi=100)
curve(d, p, rr, 'w0', 'out_to_0.98', B, ylo=0, yhi=100)
curve(d, p, rr, 'w0', 'out_to_0.90', TEAL, ylo=0, yhi=100)
curve(d, p, rr, 'w0', 'out_to_0.68', G, ylo=0, yhi=100)
for w, lbl in ((0.202, 'HCl 20,2 %'), (0.688, 'HNO₃ 68,8 %'), (0.983, 'H₂SO₄ 98,3 %')):
    d.line((p(w, 0)[0], 175, p(w, 0)[0], 700), fill='#C9D4DD', width=3)
    txt(d, p(w, 0)[0] - 45, 140, lbl, 21, G)
txt(d, 45, 865, 'Mass balansi: m(suv) = 100 − 100·w₀/w₁ (kislota yo‘qotilmaydi)', 24, N)
txt(d, 45, 920, 'ko‘k: w₁ = 0,99;  bronza: 0,98;  teal: 0,90;  kul: 0,68', 24, B)
txt(d, 45, 975, '0,50 → 0,98: 48,98 kg suv;  0,68 → 0,98: 30,61 kg;  0,75: 23,47 kg', 23, G)
txt(d, 45, 1030, 'Azeotrop chegarasidan o‘tib bo‘lmaydi (oddiy bug‘lash)', 23, G)
txt(d, 45, 1080, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'buglash')

# --- Graph 4: ion almashinuv — fronti kiring ------------------------------
im, d = canvas('Ion almashinuv: fronti kiring egri chizig‘i', 1180)
p = axes(d, 0, 6, 0, 1, 'bed hajmlari (BV)', 'C/C₀',
         [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')],
         [(0, '0'), (0.25, '0,25'), (0.5, '0,5'), (0.75, '0,75'), (1, '1')])
rr = rows('ionalmashinuv')
curve(d, p, rr, 'BV', 'c50', N, ylo=0, yhi=1)
curve(d, p, rr, 'BV', 'c100', B, ylo=0, yhi=1)
curve(d, p, rr, 'BV', 'c200', TEAL, ylo=0, yhi=1)
d.line((120, p(0, 0.5)[1], 680, p(0, 0.5)[1]), fill='#C9D4DD', width=3)
for c0, col in ((50, N), (100, B), (200, TEAL)):
    bv = breakthrough_bv(float(c0))
    x, y = p(bv, 0.5)
    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=col)
txt(d, 45, 865, 'Plug-flow taxminiy hisoblar, Langmuir izotermasi; q_max = 50 mg/g', 24, N)
txt(d, 45, 915, 'ko‘k: 50 mg/L;  bronza: 100 mg/L;  teal: 200 mg/L', 24, B)
txt(d, 45, 965, 'fronti kiring BV:  4,96  /  1,28  /  0,34', 24, INK)
txt(d, 45, 1015, 'Massa balansi: yig‘ilgan miqdor 48,08 mg/g ≈ q_max', 23, G)
txt(d, 45, 1065, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'front')


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


scheme('usullar', 'Tozalash usullarining beshta oilasi', [
    ('1. Mexanik', 'Filtratsiya, sentrifugalash', 'Fazalarni ajratadi'),
    ('2. Fizik-kimyoviy', 'Cho‘ktirish, ekstraksiya, adsorbsiya', 'Ifloslikni ko‘chiradi'),
    ('3. Kimyoviy', 'Redoks, kompleks, kislota-asos', 'Ifloslikni o‘zgartiradi'),
    ('4. Membranaviy', 'Nano-, ultrafiltratsiya', 'Oqim tezligi, selektivlik'),
    ('5. Kombinatsiya', 'Zanjir: filtr → cho‘k → konsentratsiya', 'Ketma-ketlik mantiqiyligi')])

scheme('zanjir', 'Tozalash zanjiri: umumiy oqim', [
    ('Daqiqotlash va filtratsiya', 'Suspenziya va qattiq zarracha', 'Barcha bosqichlardan oldin'),
    ('Kimyoviy tozalash', 'NO₂ → HNO₃; Fe³⁺ → Fe²⁺', 'Reagent sarfi nazoratda'),
    ('Cho‘kmani ajratish', 'Filtratsiya', 'Cho‘kma reagentini to‘liq chiqarish'),
    ('Konsentratsiya', 'Bug‘lash yoki ekstraksiya', 'Azeotrop chegarasi hisobga olinadi'),
    ('Ion almashinuv / membrana', 'Qoldiq metall va anion', 'Regeneratsiya rejalashtiriladi'),
    ('Qadoqlash', 'Partiya raqami va hujjat', 'Ishlatish muddati')])

scheme('choqirish', 'Cho‘ktirish: reagent tanlash va chiqindi', [
    ('Ksp asosida tanlov', '[M] = Ksp/[OH⁻]ⁿ', 'pH — asosiy dastak'),
    ('Ortiqcha reagent qo‘shish', 'CaO, CuO, Ba(OH)₂', 'Kislota saqlanadi'),
    ('Cho‘kma ajratish', 'Filtratsiya', 'Reagent to‘liq chiqariladi'),
    ('Chiqqindini baholash', 'E = m(chiqindi)/m(mahsulot)', 'Taxminiy hisob: 0,00167 kg/kg'),
    ('Resursni tiklash', 'Cu, Ag, Ni qaytariladi', 'Fe — yo‘qotish ma’qul')])

scheme('ionsxema', 'Ion almashinuv kolonkasi va regeneratsiya', [
    ('Kirish eritmasi', 'C₀ — ifloslik konsentratsiyasi', 'Taxminiy hisob: 50–200 mg/L'),
    ('Smola qatlami', 'Kationit (H⁺ shakli)', 'Metall kationlari ushlanadi'),
    ('Fronti kiring', 'C/C₀ = 0,5 nuqtasi', 'Kolonka to‘lganini bildiradi'),
    ('Regeneratsiya', 'Reagent yuboriladi', 'Smola tiklanadi'),
    ('Sikl chegarasi', 'Yig‘ilgan begona moddalar', 'Sifat pasayadi')])

scheme('sifat', 'Sifat nazorati: tekshiruv nuqtalari', [
    ('Kislota miqdori', 'Titrlash', 'Ph. Eur.: 68,0–70,0 %'),
    ('Rang', 'Y6 / Pt-Co (ASTM D1209)', 'Y6 dan kuchsiz'),
    ('Xloridlar', 'AgNO₃ solishtirish (2.4.4)', '≤ 0,5 ppm'),
    ('Metallar', 'ICP spektrometriyasi', 'Fe ≤ 10; Pb ≤ 2 ppm'),
    ('Suv', 'Karl Fischer usuli', 'Ishlatish muddati'),
    ('Hujjatlashtirish', 'Partiya, metod, natija, sana', 'Izchillik')])

scheme('chiqindi', 'Chiqindini ushlash va resursni tiklash', [
    ('Chiqindi manbai', 'Cho‘kma, eritma, gaz', 'Tozalash zanjiridan'),
    ('Yig‘ish', 'Alohida oqim', 'Konsentratsiya oshadi'),
    ('Baholash', 'Toksiklik va narx', 'Eslatma: Hg, Pb, Cd, As'),
    ('Tiklash', 'Qaytarish yoki qayta ishlatish', 'Resurs qaytadi'),
    ('Yo‘qotish', 'To‘liq chiqindiga berish', 'Resurs yo‘qoladi')])

scheme('xarita', 'Kislota oilalari bo‘yicha tozalash xaritasi', [
    ('HCl', 'Fe, Cu; gaz holatida ajratish', 'Distillatsiya'),
    ('HNO₃', 'NO₂ (rang), HNO₂, Cu, Fe', 'Pervaza + cho‘ktirish'),
    ('H₂SO₄', 'Fe, Cu, As, Pb, Cd; NOx', 'Denitrifikatsiya'),
    ('H₃PO₄ (nam usul)', 'F⁻, As, Cd, Pb', 'Defluorinatsiya + cho‘ktirish'),
    ('HF', 'Si; H₂SiF₆', 'Kremniy alohida chiqariladi')])


# --- Original illustrasiyalar ------------------------------------------------
def base(t, h=590):
    return canvas(t, h)


im, d = base('Ifloslik manbalari: kislotaga ta’siri')
srcs = [('Xom ashyo', 70, 120), ('Reagent', 70, 250), ('Suv', 70, 380),
        ('Idish', 470, 120), ('Qayta ishlatish', 470, 250), ('Parchalanish', 470, 380)]
d.rounded_rectangle((255, 195, 400, 300), radius=12, outline=N, width=4)
txt(d, 285, 235, 'Kislota', 28, N)
for label, x, y in srcs:
    d.rounded_rectangle((x, y, x + 160, y + 75), radius=10, outline=G, width=3)
    txt(d, x + 12, y + 26, label, 22, INK)
    sx = x + 160 if x < 200 else x
    d.line((sx, y + 37, 255 if x < 200 else 400, 247), fill=G, width=3)
    d.polygon([(255, 247), (238, 239), (240, 257)] if x < 200
              else [(400, 247), (382, 239), (384, 257)], fill=G)
txt(d, 35, 500, 'Har bir manba alohida usul talab qiladi; sxematik', 23, G)
save(im, 'manbalar')

im, d = base('Cho‘kma ajratish va filtratsiya (sxematik)')
d.rectangle((90, 300, 620, 430), fill='#E4D2B0')
for i in range(7):
    x = 120 + i * 70
    d.ellipse((x, 320, x + 46, 410), outline=N, width=4)
txt(d, 110, 445, 'Cho‘kma qatlami (qattiq zarracha)', 24, N)
d.rectangle((90, 250, 620, 295), fill='#DCEBF4')
txt(d, 110, 258, 'Kislota eritmasi (faza chegarasi)', 24, TEAL)
d.rectangle((90, 150, 620, 245), fill='#EAF1E4')
txt(d, 110, 165, 'Filtrat — mahsulot oqimi', 24, G)
d.line((355, 245, 355, 200), fill=B, width=5)
d.polygon([(355, 200), (340, 224), (370, 224)], fill=B)
d.line((355, 430, 355, 480), fill=G, width=4)
d.polygon([(355, 480), (340, 456), (370, 456)], fill=G)
txt(d, 375, 455, 'Cho‘kma chiqindisi', 24, G)
txt(d, 35, 530, 'Sxematik kesim; hajm va tezlik hisoblanmaydi', 22, G)
save(im, 'kolkada')

im, d = base('Azeotrop: t–x diagrammasi (sxematik)')
d.line((120, 430, 660, 430), fill=G, width=3)
d.line((120, 430, 120, 150), fill=G, width=3)
pts = [(120, 430), (200, 330), (280, 250), (360, 205), (440, 195), (520, 215), (600, 250)]
d.line(pts, fill=N, width=5)
d.ellipse((pts[4][0] - 9, pts[4][1] - 9, pts[4][0] + 9, pts[4][1] + 9), fill=B)
d.line((pts[4][0], 150, pts[4][0], 430), fill='#C9D4DD', width=3)
txt(d, pts[4][0] - 60, 120, 'azeotrop', 24, B)
txt(d, 560, 445, 'x (kislota)', 24, G)
txt(d, 40, 160, 'T', 26, G)
txt(d, 150, 320, 'bug‘lash egri chizig‘i', 24, INK)
txt(d, 35, 500, 'Sxematik: minimum yoki maksimum qaynash nuqtasi', 23, G)
txt(d, 35, 545, 'qayerda x = y, oddiy bug‘lash tarkibni o‘zgartirmaydi', 23, G)
save(im, 'azeotrop')

im, d = base('Membrana ajratish: sxematik kesim')
d.rectangle((120, 150, 160, 440), fill=N)
txt(d, 60, 460, 'membrana', 23, N)
d.rectangle((160, 150, 640, 440), outline=G, width=3)
for i in range(6):
    x = 200 + i * 70
    d.ellipse((x, 250, x + 34, 284), outline=TEAL, width=3)
txt(d, 200, 190, 'eritma (kislota + ifloslik)', 24, INK)
d.line((240, 320, 520, 320), fill=TEAL, width=5)
d.polygon([(520, 320), (498, 308), (498, 332)], fill=TEAL)
txt(d, 330, 285, 'permeat', 24, TEAL)
d.ellipse((190, 350, 224, 384), outline=B, width=3)
d.ellipse((560, 200, 594, 234), outline=B, width=3)
txt(d, 180, 395, 'retentat', 24, B)
txt(d, 35, 500, 'Sxematik; materiallar va parametrlar berilmaydi', 22, G)
save(im, 'membrana')

im, d = base('Shartli hisob zanjiri: rangli HNO₃ va sulfat kislotadagi Fe', 620)
h = no2_to_hno3(1000.0, 0.68, 4.0)
f = fe_precipitation(1000.0, 0.0003)
steps = [('NO₂ 4,0 t', 'rang beruvchi', N), ('O₂ 0,6955 t', 'kislotaga aylanadi', N),
         ('HNO₃ +5,4779 t', 'w = 68,55 %', TEAL)]
for i, (name, val, col) in enumerate(steps):
    x = 40 + i * 180
    d.rounded_rectangle((x, 160, x + 150, 280), radius=12, outline=col, width=4)
    txt(d, x + 30, 180, name, 24, col)
    txt(d, x + 20, 230, val, 19, INK)
    if i < 2:
        d.line((x + 150, 220, x + 176, 220), fill=G, width=4)
        d.polygon([(x + 176, 220), (x + 158, 210), (x + 158, 230)], fill=G)
d.rounded_rectangle((40, 330, 340, 440), radius=12, outline=B, width=4)
txt(d, 95, 350, 'Fe(OH)₃ 0,5741 t', 25, B)
txt(d, 80, 395, 'CaSO₄ 1,0969 t — chiqindi', 21, INK)
d.rounded_rectangle((380, 330, 700, 440), radius=12, outline=TEAL, width=4)
txt(d, 415, 350, 'E = 0,00167 kg/kg', 25, TEAL)
txt(d, 405, 395, 'CaCO₃ yo‘lida: 0,7903 t yo‘qotish', 21, INK)
txt(d, 40, 490, 'Shartli hisob zanjiri; o‘lchov ma’lumoti emas', 23, G)
txt(d, 40, 545, 'Texnologik parametrlar va retseptlar berilmaydi', 23, G)
save(im, 'hisob')

print('5 grafik + CSV; 7 sxema; 5 original illustration.')
