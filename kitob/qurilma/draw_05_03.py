"""Original teaching figures for 5.3 "QuRITish va suvsizlantirish".
All curves are taxminiy hisob outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_05_03 import (ASSETS as A, boiling_temperature, vapour_pressure,
                        equilibrium_moisture, drying_at_temperature,
                        drying_curve, AZEOTROPE, SIEVES, hydrate_mass,
                        azeotropic_drying, evaporation_energy, DVAP_H2O_100)

N = '#0B2C4A'; B = '#B37C2D'; G = '#657583'; TEAL = '#318E95'; BG = '#F5F8FA'; INK = '#243746'
RED = '#C0392B'; PURPLE = '#6C3483'


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


def rows(n, numeric=True):
    out = []
    for r in csv.DictReader((A / (n + '.csv')).open()):
        if numeric:
            out.append({k: float(v) for k, v in r.items()})
        else:
            out.append({k: (float(v) if k not in ('usul', 'entrainer') else v)
                        for k, v in r.items()})
    return out


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


# --- Graph 1: vakuumning ta'siri ---------------------------------------
im, d = canvas('Vakuum: suvning qaynash harorati', 1180)
p = axes(d, -1.0, 2.1, -40, 110, 'lg(P), kPa', 'T, °C',
         [(-1, '0,1'), (0, '1'), (1, '10'), (2, '100')],
         [(-40, '−40'), (-20, '−20'), (0, '0'), (20, '20'), (40, '40'),
          (60, '60'), (80, '80'), (100, '100')])
rr = rows('vakuum')
curve(d, p, rr, 'lgP', 'T_C', N, ylo=-40, yhi=110)
for P, col, lbl in ((101.325, N, '101,325 kPa → 100,0 °C'),
                    (10.0, B, '10,0 kPa → 43,96 °C'),
                    (2.5, TEAL, '2,5 kPa → 17,80 °C'),
                    (1.5, PURPLE, '1,5 kPa → 9,22 °C'),
                    (0.1, RED, '0,1 kPa → −28,96 °C')):
    x, y = p(math.log10(P), boiling_temperature(P) - 273.15)
    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=col)
    txt(d, x + 14, y - 30, lbl, 22, col)
txt(d, 45, 865, 'Klausius–Klapeiron (taxminiy hisoblar, ΔvapH = 40,657 kJ/mol)', 25, N)
txt(d, 45, 920, 'Ph. Eur. 2.2.32: vakuumda quritish 1,5–2,5 kPa; chuqur vakuum ≤ 0,1 kPa', 22, B)
txt(d, 45, 975, 'p_sat(25 °C) = 2,858 kPa (shartli hisob); ΔvapH(25 °C) = 44,01 kJ/mol', 22, G)
txt(d, 45, 1030, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'vakuum')

# --- Graph 2: azeotrop entrainerlari -------------------------------------
im, d = canvas('Azeotrop: entrainer va suv sig‘imi', 1180)
p = axes(d, 60, 90, 0, 22, 'azeotrop harorati, °C', 'bug fazasida suv, %',
         [(60, '60'), (65, '65'), (70, '70'), (75, '75'), (80, '80'), (85, '85'), (90, '90')],
         [(0, '0'), (5, '5'), (10, '10'), (15, '15'), (20, '20')])
for name, col in (('toluen', N), ('sikloheksan', B), ('n-geptan', TEAL)):
    a = AZEOTROPE[name]
    x, y = p(a['T'], a['w_water'] * 100)
    d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=col)
    txt(d, x + 16, y - 16, '%s  %.1f °C, %.1f %%' % (name, a['T'], a['w_water'] * 100), 22, col)
txt(d, 45, 865, '1 kg entrainer necha kg suv olib ketadi (shartli hisob):', 25, N)
txt(d, 45, 915, 'toluen 0,2469 kg;  sikloheksan 0,0917 kg;  n-geptan 0,1429 kg', 23, B)
txt(d, 45, 970, 'Heteroazeotrop: distillat ikki fazaga ajraladi va entrainer qaytadi', 22, G)
txt(d, 45, 1025, 'Taxminiy hisob ma’lumoti; o‘lchov ma’lumoti emas', 23, G)
save(im, 'azeotrop')

# --- Graph 3: quritish kinetikasi ---------------------------------------
im, d = canvas('QuRITish kinetikasi: namlik va vaqt', 1180)
p = axes(d, 0, 60, 0, 0.36, 'vaqt, min', 'X (nam asosdagi ulush)',
         [(0, '0'), (10, '10'), (20, '20'), (30, '30'), (40, '40'), (50, '50'), (60, '60')],
         [(0, '0'), (0.1, '0,10'), (0.2, '0,20'), (0.3, '0,30')])
rr = rows('kinetika')
curve(d, p, rr, 't_min', 'X_333', RED, ylo=0, yhi=0.36)
curve(d, p, rr, 't_min', 'X_353', B, ylo=0, yhi=0.36)
curve(d, p, rr, 't_min', 'X_373', N, ylo=0, yhi=0.36)
xe = rr[0]['X_eq']
d.line((120, p(0, xe)[1], 680, p(0, xe)[1]), fill='#C9D4DD', width=3)
txt(d, 300, p(0, xe)[1] - 32, 'muvozanat namligi (80 % RH)', 22, G)
txt(d, 45, 865, 'Ikki bosqichli shartli hisob: doimiy tezlik + birinchi pasayish bosqichi', 24, N)
txt(d, 45, 915, 'ko‘k: 373 K (100 °C);  bronza: 353 K;  qizil: 333 K (60 °C)', 23, B)
txt(d, 45, 970, 'Arrhenius koeffitsienti: Eₐ = 30 kJ/mol (shartli hisob)', 22, G)
txt(d, 45, 1025, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'kinetika')

# --- Graph 4: adsorbsiya va muvozanat namligi ----------------------------
im, d = canvas('Adsorbsiya: muvozanat namligi va nisbiy namlik', 1180)
p = axes(d, 0, 100, 0, 0.09, 'nisbiy namlik, %', 'w_eq, kg/kg',
         [(0, '0'), (20, '20'), (40, '40'), (60, '60'), (80, '80'), (100, '100')],
         [(0, '0'), (0.03, '0,03'), (0.06, '0,06'), (0.09, '0,09')])
rr = rows('adsorbsiya')
curve(d, p, rr, 'RH', 'w_0.03', G, ylo=0, yhi=0.09)
curve(d, p, rr, 'RH', 'w_0.05', N, ylo=0, yhi=0.09)
curve(d, p, rr, 'RH', 'w_0.08', B, ylo=0, yhi=0.09)
txt(d, 45, 865, 'w_eq = w_m·C·x/(1 + (C − 1)x),  x = p/p₀,  C = 10', 25, N)
txt(d, 45, 915, 'ko‘k: w_m = 0,05 kg/kg;  bronza: 0,08;  kul: 0,03', 23, B)
txt(d, 45, 970, '20 % RH → 0,0357;  50 % → 0,0455;  80 % → 0,0488 kg/kg (w_m = 0,05)', 22, G)
txt(d, 45, 1025, 'Shartli hisob egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'adsorbsiya')

# --- Graph 5: energetika -------------------------------------------------
im, d = canvas('QuRITish usullarining energetik sarfi', 1180)
p = axes(d, 0, 4, 0, 1.8, 'usul', 'kWh / 1 kg suv',
         [(0, ''), (1, ''), (2, ''), (3, ''), (4, '')],
         [(0, '0'), (0.5, '0,5'), (1.0, '1,0'), (1.5, '1,5')])
rr = rows('energiya', numeric=False)
cols = [G, TEAL, N, B]
for i, r in enumerate(rr):
    x0, x1 = p(i + 0.15, 0)[0], p(i + 0.85, 0)[0]
    y = p(0, r['kWh_per_kg'])[1]
    d.rectangle((x0, y, x1, 700), fill=cols[i % len(cols)])
    txt(d, x0 - 4, y - 34, '%.2f' % r['kWh_per_kg'], 24, INK)
    txt(d, x0 - 24, 722, r['usul'][:9], 21, INK)
txt(d, 45, 865, 'Taxminiy hisob: 1 kg suvni olib tashlash uchun taxminiy elektr energiyasi', 24, N)
txt(d, 45, 915, 'molekulyar sital 0,18;  vakuum 0,85;  shkaf 1,05;  azeotrop 1,55 kWh/kg', 23, B)
txt(d, 45, 970, 'Sital regeneratsiyasi energiyani yashiradi; azeotrop entrainer aylanishini talab qiladi', 22, G)
txt(d, 45, 1025, 'Taxminiy qiymatlar — reyting emas, usullarning tartibini ko‘rsatadi', 22, G)
save(im, 'energiya')


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


scheme('namliksxema', 'Suvning holatlari va o‘lchov usullari', [
    ('1. Erkin suv', 'Eritmada eringan', 'Bug‘lash, ekstraksiya'),
    ('2. Kristallizatsiya suvi', 'Gidrat tuzda stixiometrik', 'Fazaviy o‘zgarish'),
    ('3. Sorbsiyalangan suv', 'Sirt va mikroporalar', 'Quritgich, vakuum'),
    ('4. Reagent suvi', 'Reaksiyada qatnashgan', 'Massa balansi'),
    ('O‘lchov', 'KF · quruq qoldig‘ · TGA · higroskopiklik', 'Usul monografiyada ko‘rsatiladi')])

scheme('usullarsxema', 'QuRITish usullarining beshta oilasi', [
    ('1. Mexanik', 'Quruq filtratsiya, sentrifugalash', 'Faqat erkin suv'),
    ('2. Fizik', 'Shkaf, vakuum, gaz oqimi', 'Bug‘lanish tezligini oshirish'),
    ('3. Kimyoviy', 'P₂O₅, CaCl₂, molekulyar sital', 'Suvni bog‘lash'),
    ('4. Fizik-kimyoviy', 'Azeotrop, ekstraksiya', 'Yordamchi komponent'),
    ('5. Maxsus', 'Suhlatish, spray, membrana', 'Zarracha va tuzilma o‘zgaradi')])

scheme('shkafsxema', 'QuRITish shkafi va vakuum desikatori (sxematik)', [
    ('Shkaf (105 °C)', 'Konveksiya va radiatsiya', 'Ph. Eur. 2.2.32 (d)'),
    ('Vakuum desikatori', 'P₂O₅ ustida, 1,5–2,5 kPa', 'Ph. Eur. 2.2.32 (b)'),
    ('Chuqur vakuum', '≤ 0,1 kPa', 'Ph. Eur. 2.2.32 (e)'),
    ('Doimiy massa', 'Ketma-ket tarozilar farqi ≤ 0,50 mg/g', 'USP <731>'),
    ('Chegara', 'Harorat monografiyada ±2 °C', 'Parametr tavsiyasi emas')])

scheme('azeotropsxema', 'Azeotropik quritish sxemasi', [
    ('Reabiler', 'Kislota + toluen + suv', '84,1 °C azeotrop'),
    ('Kondenser', 'Distillat sovutiladi', 'Ikki faza hosil bo‘ladi'),
    ('Ajratish', 'Suv fazasi va organik faza', '~99,95 % / ~99,95 %'),
    ('Entrainer qaytishi', 'Organik faza qaytadi', 'Yo‘qotish 0,158 kg (shartli hisob)'),
    ('Mahsulot', 'Kislota + minimal suv', 'Azeotrop chegarasi yoriladi')])

scheme('sitalsxema', 'Molekulyar sital kolonkasi va regeneratsiya', [
    ('Kirish oqimi', 'Nam gaz yoki eritma', 'Taxminiy hisob: C₀ = 50–200 mg/L'),
    ('Sital qatlami', '3A / 4A / 5A / 13X', 'Sig‘im 19,5–23,5 %'),
    ('Adsorbsiya', 'Suv yuzaga tortiladi', 'Suv kamayadi'),
    ('Regeneratsiya', '200–300 °C da', 'Energiya sarfi'),
    ('Chiqindi', 'Adsorbat va CO₂', 'Alohida yig‘iladi')])

scheme('gidratsxema', 'Gidrat quritish: fazaviy o‘tish', [
    ('CuSO₄·5H₂O', 'M = 249,68 g/mol; suv 36,08 %', 'Boshlang‘ich faza'),
    ('CuSO₄·3H₂O', 'M = 213,65 g/mol', 'Oraliq faza'),
    ('CuSO₄·H₂O', 'M = 177,62 g/mol; suv 10,14 %', 'Shartli hisob maqsadi'),
    ('CuSO₄ (anh.)', 'M = 159,61 g/mol', 'To‘liq quruq'),
    ('Taxminiy hisob', '1000 kg pentahidrat → 288,60 kg suv', '711,40 kg monohidrat')])

scheme('nazoratsxema', 'Suv miqdori nazorati va hujjatlashtirish', [
    ('Namuna olish', 'Toza, qopqoqli idish', 'O‘z vaqtida'),
    ('Karl Fischer', 'Faqat suv; 1:1 stixiometriya', 'Tez, aniq natija'),
    ('Quruq qoldig‘', 'Barcha uchuvchi moddalar', 'Gravimetrik'),
    ('TGA', 'Haroratga bog‘liq yo‘qotish', 'Tarkibni ajratadi'),
    ('Hujjat', 'Partiya, sana, usul, sharoit, natija', 'Izchillik')])


# --- Original illustrasiyalar ------------------------------------------------
def base(t, h=590):
    return canvas(t, h)


im, d = base('Higroskopiklik: namlik darajasi va massa o‘sishi (sxematik)')
d.line((120, 430, 660, 430), fill=G, width=3)
d.line((120, 430, 120, 150), fill=G, width=3)
for frac, col, lbl in ((0.92, N, 'deliquescent'), (0.70, B, 'juda higroskopik (≥ 15 %)'),
                       (0.45, TEAL, 'higroskopik (2–15 %)'), (0.22, G, 'biroz higroskopik (0,2–2 %)')):
    x = 150 + frac * 480
    d.ellipse((x - 11, 419, x + 11, 441), fill=col)
    txt(d, x - 40, 452, lbl, 20, col)
d.line((120, 300, 660, 300), fill='#C9D4DD', width=3)
txt(d, 480, 272, '15 % chegarasi', 21, G)
txt(d, 40, 165, 'Δm, %', 25, G)
txt(d, 520, 448, '24 soat, 25 °C, 80 % RH', 21, G)
txt(d, 35, 520, 'Sxematik: Ph. Eur. 5.11 sinflari', 22, G)
save(im, 'higroskopik')

im, d = base('QuRITish egri chizig‘i: bosqichlar (sxematik)')
d.line((120, 430, 660, 430), fill=G, width=3)
d.line((120, 430, 120, 140), fill=G, width=3)
pts = [(120, 180), (250, 200), (330, 230), (420, 300), (520, 355), (660, 380)]
d.line(pts, fill=N, width=5)
d.line((120, 380, 660, 380), fill='#C9D4DD', width=3)
txt(d, 470, 392, 'muvozanat namligi', 21, G)
d.line((250, 165, 250, 200), fill=B, width=3)
txt(d, 195, 132, 'doimiy tezlik', 21, B)
txt(d, 330, 255, '1-pasayish', 21, B)
txt(d, 470, 320, '2-pasayish', 21, B)
txt(d, 40, 150, 'X', 25, G)
txt(d, 590, 445, 'vaqt', 22, G)
txt(d, 35, 510, 'Sxematik: umumiy ko‘rinish', 22, G)
txt(d, 35, 555, 'Taxminiy hisob: doimiy tezlik + 1-pasayish + muvozanat', 22, G)
save(im, 'quritishegri')

im, d = base('Quritish uskonasining kesimi (sxematik)')
d.rectangle((120, 150, 640, 200), fill='#E4D2B0')
txt(d, 190, 162, 'quritiladigan modda', 23, INK)
d.rectangle((120, 200, 640, 250), fill='#DCEBF4')
txt(d, 150, 210, 'bug‘ oqimi (yuqoriga)', 22, TEAL)
d.rectangle((120, 380, 640, 440), fill='#E4D2B0')
txt(d, 175, 392, 'quritgich (P₂O₅ yoki sital)', 23, INK)
d.rectangle((90, 250, 120, 440), fill=N)
txt(d, 30, 300, 'devor', 21, N)
d.line((380, 150, 380, 95), fill=B, width=5)
d.polygon([(380, 95), (368, 118), (392, 118)], fill=B)
txt(d, 400, 70, 'vakuum / havo chiqishi', 22, B)
txt(d, 35, 505, 'Sxematik kesim; parametrlar berilmaydi', 22, G)
save(im, 'shkaf')

im, d = base('Azeotrop distillatining ikki fazaga ajralishi (sxematik)')
d.polygon([(300, 140), (460, 140), (420, 470), (340, 470)], outline=N, width=4)
d.rectangle((322, 300, 438, 462), fill='#DCEBF4')
txt(d, 340, 330, 'suv fazasi', 23, TEAL)
d.rectangle((322, 150, 438, 250), fill='#E4D2B0')
txt(d, 336, 180, 'entrainer fazasi', 23, B)
d.line((300, 250, 460, 250), fill=RED, width=4)
txt(d, 470, 235, 'faza chegarasi', 22, RED)
d.line((380, 470, 380, 520), fill=G, width=4)
d.polygon([(380, 520), (366, 496), (394, 496)], fill=G)
txt(d, 400, 500, 'suv fazasi chiqishi', 22, G)
txt(d, 35, 550, 'Sxematik; faza tarkibi taxminiy hisobda ~99,95 %', 22, G)
save(im, 'ajratish')

im, d = base('Ishlangan hisob: ikki taxminiy hisobning modda oqimi', 620)
d.rounded_rectangle((30, 140, 350, 300), radius=12, outline=N, width=4)
txt(d, 55, 160, 'Taxmin A: gidrat quritish', 25, N)
txt(d, 55, 205, '1000 kg CuSO₄·5H₂O', 22, INK)
txt(d, 55, 240, '→ 288,60 kg suv ajraladi', 22, INK)
txt(d, 55, 272, '→ 711,40 kg CuSO₄·H₂O', 22, INK)
d.rounded_rectangle((410, 140, 730, 300), radius=12, outline=B, width=4)
txt(d, 435, 160, 'Taxmin B: azeotrop', 25, B)
txt(d, 435, 205, '1000 kg 68 % li HNO₃', 22, INK)
txt(d, 435, 240, '→ 316,58 kg suv + 1282,32 kg toluen', 22, INK)
txt(d, 435, 272, '→ 683,42 kg mahsulot', 22, INK)
d.rounded_rectangle((30, 340, 350, 470), radius=12, outline=TEAL, width=4)
txt(d, 70, 360, 'Q = 651,3 MJ = 180,9 kWh', 24, TEAL)
txt(d, 60, 405, 'Taxmin A — bug‘latish energiyasi', 21, INK)
d.rounded_rectangle((410, 340, 730, 470), radius=12, outline=TEAL, width=4)
txt(d, 440, 360, 'Q = 1244,2 MJ = 345,6 kWh', 24, TEAL)
txt(d, 430, 405, 'Taxmin B — suv + toluen', 21, INK)
txt(d, 40, 505, 'Shartli hisob zanjiri; o‘lchov ma’lumoti emas', 23, G)
txt(d, 40, 555, 'Texnologik parametrlar va retseptlar berilmaydi', 23, G)
save(im, 'hisob')

print('5 grafik + CSV; 7 sxema; 5 original illustration.')
