"""Original teaching figures for 6.1 "Guruhning umumiy tavsifi".
All curves are model outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_06_01 import (ASSETS as A, ACIDS, hf_ionisation_series, gas_to_ion,
                        net_bond, thermal_decomposition, glass_model,
                        neutralisation_model, azeotrope_model)

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
    out = []
    for r in csv.DictReader((A / (name + '.csv')).open()):
        out.append({k: float(v) for k, v in r.items()})
    return out


def axes(d, xlo, xhi, ylo, yhi, xlabel, ylabel, xt, yt, x0=120, x1=680, y0=175, y1=700):
    def p(x, y):
        return (x0 + (x - xlo) / (xhi - xlo) * (x1 - x0), y1 - (y - ylo) / (yhi - ylo) * (y1 - y0))
    d.line((x0, y0, x0, y1, x1, y1), fill=G, width=3)
    for x, s in xt:
        txt(d, p(x, ylo)[0] - 15, y1 + 18, s, 24)
    for y, s in yt:
        txt(d, 20, p(xlo, y)[1] - 16, s, 24)
    txt(d, 45, 108, ylabel, 28)
    txt(d, x0 + 25, y1 + 80, xlabel, 27)
    return p


# --- Graph 1: kislotalik (suv va DMSO) ------------------------------------
im, d = canvas('Kislotalik: suvda tekislanish va DMSOdagi farq', 1180)
p = axes(d, 0, 4, -12, 16, '', 'pK_a',
         [(0, 'HF'), (1, 'HCl'), (2, 'HBr'), (3, 'HI')],
         [(-10, '−10'), (-5, '−5'), (0, '0'), (5, '5'), (10, '10'), (15, '15')])
zero = p(0, 0)[1]
d.line((120, zero, 680, zero), fill=RED, width=3)
for i, a in enumerate(ACIDS):
    gx = 120 + 140 * i + 20
    for j, (val, col) in enumerate([(a['pka'], N), (a['pka_dmso'], TEAL)]):
        bx = gx + j * 52
        yv = p(0, val)[1]
        d.rectangle((bx, min(yv, zero), bx + 44, max(yv, zero)), fill=col)
        ly = yv - 30 if val >= 0 else yv + 10
        txt(d, bx - 4, ly, ('%.1f' % val).replace('-', '−'), 21, col)
d.rectangle((430, 128, 456, 150), fill=N); txt(d, 464, 128, 'suvda', 21, N)
d.rectangle((560, 128, 586, 150), fill=TEAL); txt(d, 594, 128, 'DMSOda', 21, TEAL)
txt(d, 45, 790, 'Suvda HCl = HBr = HI: kislotalar H₃O⁺ darajasiga tekislanadi (leveling effect)', 22, N)
txt(d, 45, 840, 'DMSOda pK_a: HF 15 · HCl −2,0 · HBr −6,8 · HI −10,9 — tartib ochiladi', 22, B)
txt(d, 45, 890, 'Model qiymatlar; suvdagi pK_a baholari ±0,4–1,0 aniqlikda', 22, G)
txt(d, 45, 975, 'Model egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'kislotalik')

# --- Graph 2: energiya balansi --------------------------------------------
im, d = canvas('Energetik balans: bog‘ energiyasi va gidratatsiya', 1180)
p = axes(d, 0, 4, -560, 620, '', 'kJ/mol',
         [(0, 'HF'), (1, 'HCl'), (2, 'HBr'), (3, 'HI')],
         [(-500, '−500'), (-250, '−250'), (0, '0'), (250, '250'), (500, '500')])
zero = p(0, 0)[1]
d.line((120, zero, 680, zero), fill=RED, width=3)
for i, a in enumerate(ACIDS):
    gx = 120 + 140 * i + 14
    series = [(a['d'], N), (a['hyd'], TEAL), (net_bond(a['key']), B)]
    for j, (val, col) in enumerate(series):
        bx = gx + j * 38
        yv = p(0, val)[1]
        d.rectangle((bx, min(yv, zero), bx + 34, max(yv, zero)), fill=col)
        ly = yv - 28 if val >= 0 else yv + 8
        txt(d, bx - 2, ly, '%d' % val, 19, col)
d.rectangle((430, 128, 456, 150), fill=N); txt(d, 464, 128, 'D(H–X)', 21, N)
d.rectangle((575, 128, 601, 150), fill=TEAL); txt(d, 609, 128, 'ΔH_hyd(X⁻)', 21, TEAL)
d.rectangle((430, 164, 456, 186), fill=B); txt(d, 464, 164, 'D + ΔH_hyd', 21, B)
txt(d, 45, 790, 'HF: 569 − 506 = 63 kJ/mol — kuchli bog‘ kuchli gidratatsiya bilan kompensatsiya qilinadi', 22, N)
txt(d, 45, 840, 'HCl: 432 − 364 = 68 · HBr: 370 − 335 = 35 · HI: 295 − 293 = 2 kJ/mol', 22, B)
txt(d, 45, 890, 'Net qiymat kamaygan sayin kislotalik kuchayadi', 22, G)
txt(d, 45, 975, 'Model egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'energiya')

# --- Graph 3: molekulyar o'lchamlar ----------------------------------------
im, d = canvas('Bog‘ uzunligi va dipol moment (model)', 1180)
# yuqori panel: bog' uzunligi
p = axes(d, 0, 4, 0, 1.9, '', 'r(H–X), Å',
         [], [(0, '0'), (0.5, '0,5'), (1.0, '1,0'), (1.5, '1,5'), (1.9, '1,9')],
         y1=400)
for i, a in enumerate(ACIDS):
    gx = 120 + 140 * i + 20
    for j, (val, col) in enumerate([(a['rexp'], N), (a['rcov'] + a['rcov_h'], TEAL)]):
        bx = gx + j * 52
        yv = p(0, val)[1]
        d.rectangle((bx, yv, bx + 44, 400), fill=col)
        txt(d, bx - 6, yv - 28, '%.2f' % val, 20, col)
d.rectangle((430, 128, 456, 150), fill=N); txt(d, 464, 128, 'tajribiy', 21, N)
d.rectangle((575, 128, 601, 150), fill=TEAL); txt(d, 609, 128, 'r(H)+r(X)', 21, TEAL)
# pastki panel: dipol moment
d.line((120, 470, 120, 700, 680, 700), fill=G, width=3)
txt(d, 45, 440, 'μ, D', 26, G)
for i, a in enumerate(ACIDS):
    x = 150 + 140 * i
    yv = 700 - a['mu'] / 2.0 * 230
    d.rectangle((x, yv, x + 60, 700), fill=PURPLE)
    txt(d, x + 6, yv - 30, '%.2f' % a['mu'], 21, PURPLE)
    txt(d, x + 8, 715, a['key'], 24, INK)
txt(d, 45, 790, 'Dipol moment: HF 1,82 → HI 0,44 D — elektronegativlik farqining kamayishi', 22, N)
txt(d, 45, 840, 'Bog‘ uzunligi: 0,917 → 1,609 Å; radiuslar yig‘indisi har doim katta', 22, B)
txt(d, 45, 890, 'Suyuqlash harorati: −83,6 / −114,2 / −86,9 / −50,8 °C', 22, G)
txt(d, 45, 975, 'Model chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'fizik')

# --- Graph 4: termik barqarorlik ------------------------------------------
im, d = canvas('Termik barqarorlik: 2HX ⇌ H₂ + X₂ dekompozitsiyasi', 1180)
p = axes(d, 0, 4, 0, 600, '', 'ΔG°, kJ/mol',
         [(0, 'HF'), (1, 'HCl'), (2, 'HBr'), (3, 'HI')],
         [(0, '0'), (150, '150'), (300, '300'), (450, '450'), (600, '600')])
for i, a in enumerate(ACIDS):
    t = thermal_decomposition(a['key'])
    x, y = p(i, t['dg'])
    d.rectangle((x - 44, y, x + 44, 700), fill=N if i < 3 else RED)
    txt(d, x - 40, y - 32, '%.1f' % t['dg'], 21, N if i < 3 else RED)
    txt(d, x - 46, 755, 'lgK = %.2f' % t['log10k'], 20, G)
d.rectangle((430, 128, 456, 150), fill=N); txt(d, 464, 128, 'barchasi', 21, N)
d.rectangle((575, 128, 601, 150), fill=RED); txt(d, 609, 128, 'HI: eng zaif', 21, RED)
txt(d, 45, 830, 'Model: ΔG° 550,8 / 190,6 / 110,0 / 15,9 kJ/mol;  lgK −96,50 / −33,39 / −19,27 / −2,79', 22, N)
txt(d, 45, 880, 'Termodinamik imkoniyat — kinetika emas: HI xona haroratida barqaror qoladi', 22, B)
txt(d, 45, 930, 'Tezlash uchun 300–500 °C (H₂ + I₂ → 2HI, Pt katalizatori)', 22, G)
txt(d, 45, 1000, 'Model chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'termik')

# --- Graph 5: HF dissotsiatsiyasi -----------------------------------------
im, d = canvas('HF dissotsiatsiyasi: konsentratsiya va ionizatsiya', 1180)
p = axes(d, 0, 5, 0, 26, 'kislota konsentratsiyasi, M', 'ionizatsiya, %',
         [(0, '0,010'), (1, '0,050'), (2, '0,100'), (3, '0,500'), (4, '1,000')], [])
pts = []
for i, r in enumerate(hf_ionisation_series()):
    x, y = p(i, r['pct'])
    pts.append((x, y))
    d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=B, outline='#FFFFFF', width=2)
    dx = 22 if i == 0 else -30
    dy = -46 if i == 0 else -46
    txt(d, x + dx, y + dy, '%.2f %%' % r['pct'], 21, B)
    txt(d, x + (30 if i == 0 else -26), y + 22, 'pH %.2f' % r['ph'], 21, G)
d.line(pts, fill=N, width=5)
txt(d, 45, 830, 'Ka = 6,8×10⁻⁴: 0,010 M → 22,90 % (pH 2,640);  1,000 M → 2,57 % (pH 1,589)', 22, N)
txt(d, 45, 880, 'Konsentratsiya 100 barobar oshsa, ionizatsiya 9 barobar kamayadi', 22, B)
txt(d, 45, 930, 'pH baribir 1 birlikka yaqin tushadi — kislota kuchi konsentratsiyada emas', 22, G)
txt(d, 45, 1000, 'Model egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'dissotsiatsiya')


# --- Sxemalar -------------------------------------------------------------
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


scheme('sxematurlari', 'Guruh trendlari: bitta sxema, beshta ko‘rsatkich', [
    ('Elektronegativlik ↓', 'F 3,98 → I 2,66', 'Bog‘ quyuqligi oshadi'),
    ('Bog‘ energiyasi ↓', '569 → 432 → 370 → 295 kJ/mol', 'Dissotsiatsiya osonlashadi'),
    ('Kislotalik ↑', 'pKa 3,17 → −5,9 → −8,8 → −9,5', 'Suvda uchta kuchli kislota tekislanadi'),
    ('Termik barqarorlik ↓', 'ΔG° 550,8 → 190,6 → 110,0 → 15,9 kJ/mol', '2HX ⇌ H₂ + X₂'),
    ('Qaytaruvchilik ↑', 'HF < HCl < HBr < HI', 'I⁻ kuchsiz oksidlovchilarni ham qaytaradi')])

scheme('gibridlanishx', 'H–X bog‘i va dipol moment (sxematik)', [
    ('Elektron bulutining siljishi', 'Hδ+ — Xδ− ; elektronegativlik farqi', 'Dipol moment 1,82 → 0,44 D'),
    ('σ bog‘ quyuqligi', 'H 1s va X np orbitalalari qo‘shiladi', 'Uzunlik 0,917 → 1,609 Å'),
    ('Nishon quyuqligi', 'F da eng kuchli, I da eng kuchsiz', 'HF da qisman ion xarakter'),
    ('Hydrogen bog‘i', 'HF molekulalari orasida zanjir hosil qiladi', 'HF qaynash harorati 19,5 °C'),
    ('Xulosa', 'Kislotalik va barqarorlik — bir xil tuzilmaning ikki yuzasi', 'Model sxemasi')])

scheme('olishsx', 'Olish usullari: bitta mantiq, to‘rt reagent', [
    ('HF: CaF₂ + H₂SO₄', 'Fluorit + kislota → 2HF + CaSO₄', 'Model: 1000 kg fluorit → 447,4 kg HF'),
    ('HCl: Cl₂ + H₂', 'Xlor-alkali yoki NaCl + H₂SO₄', 'Gaz suvga yotqiziladi → 32–37 %'),
    ('HBr: Br₂ + SO₂ + 2H₂O', 'Brom sulfit bilan qaytariladi', '2HBr + H₂SO₄'),
    ('HI: I₂ + H₂S', 'Yod sulfid bilan qaytariladi', 'Cho‘kma filtrlanadi, distillatsiya qilinadi'),
    ('Chegara', 'Parametrlar, qurilma va kartalar berilmaydi', 'Sxematik tavsif')])

scheme('xossalarsx', 'Kislota xossalari: metallar, oksidlar, tuzlar (sxematik)', [
    ('Metall bilan', '2HX + M → MX₂ + H₂↑', 'Kislota kuchi yetarli bo‘lishi kerak'),
    ('Metall oksidi bilan', 'MO + 2HX → MX₂ + H₂O', 'Kislota + asos'),
    ('Karbonat bilan', 'CaCO₃ + 2HX → CaX₂ + CO₂↑ + H₂O', 'CO₂ ajralishi tug‘diradi'),
    ('Model: neytralizatsiya', '1000 kg 10 % HCl → CaCO₃ 137,3 kg; CaCl₂ 152,2 kg; CO₂ 60,4 kg', 'Kirish 237,3 = chiqish 237,2 kg'),
    ('Xulosa', 'Uch shart: proton berish + konjugat asos + termodinamik imkon', 'Model mantiqi')])

scheme('redokssx', 'Redoks xossalari: qaytaruvchilik (sxematik)', [
    ('HBr + H₂SO₄ → Br₂', 'Brom ajraladi: 1 kg HBr → 987,5 g Br₂', 'Sulfit kislotasi qaytaradi'),
    ('HI + H₂SO₄ → I₂', 'Yod ajraladi: 1 kg HI → 992,1 g I₂', 'Eng kuchli qaytaruvchi'),
    ('4HI + O₂ → 2I₂ + 2H₂O', 'Havo bilan reaksiya: 62,54 g O₂ / kg HI', 'Eritma qorayadi — saqlash chegarasi'),
    ('Halogenning o‘zi', 'F₂ eng kuchli oksidlovchi: balans −754,6 kJ/mol', 'I₂ eng kuchsiz: −481,2 kJ/mol'),
    ('Xulosa', 'Qaytaruvchilik va oksidlovchilik teskari', 'Model balansi')])

scheme('materiallarx', 'Materiallar bilan munosabat (sxematik)', [
    ('HF + SiO₂ → H₂SiF₆ + 2H₂O', 'Shishani yemiradi', '1 kg SiO₂ uchun 1997,9 g HF'),
    ('HF idishi', 'PTFE yoki PP; shisha mos emas', 'Xavf xususiyati'),
    ('HCl, HBr, HI va shisha', 'SiO₂ ni amalda tegmaydi', 'Metallarga nisbatan agressiv'),
    ('316L va Ni legirlari', 'HCl ga chidamliroq; HBr/HI da tezlashadi', 'Kattaroq X⁻ kuchsiz kompleks'),
    ('Tanlov mezoni', 'Reaktivlik + nam va T + ifloslanish', 'Amaliyot tavsiyalari berilmaydi')])

scheme('xavfsizliksx', 'Xavfsizlik va ekologiya (sxematik)', [
    ('HF: tizimli toksiklik', 'F⁻ kalsiy va magniyni ushlab qoladi', 'Gipokalsemiya; kalsiy glyukonat'),
    ('Chegara', 'OSHA TWA 3 ppm; NIOSH IDLH 30 ppm', 'Manba chegaralari'),
    ('HCl, HBr, HI', 'Mahallay kuyish; gaz holatida nafas olishi', 'Ventilyatsiya va shaxsiy himoya'),
    ('Neytralizatsiya', 'CaCO₃ bilan: 1000 kg 10 % HCl → 60,4 kg CO₂', 'Ekosistema yukini kamaytiradi'),
    ('Logistika', 'HCl quvurda; HF maxsus idishda; HI qorong‘i', 'Amaliyot tavsiyalari berilmaydi')])


# --- Original illustrasiyalar ---------------------------------------------
im, d = canvas('Guruhning to‘rt molekulasi (sxematik)', 620)
cols = [N, TEAL, B, PURPLE]
for i, a in enumerate(ACIDS):
    cx = 110 + 180 * i
    d.ellipse((cx - 34, 200, cx + 34, 268), fill='#FFFFFF', outline=cols[i], width=4)
    d.ellipse((cx + 42, 200, cx + 110, 268), fill='#FFFFFF', outline=cols[i], width=4)
    d.line((cx + 34, 234, cx + 42, 234), fill=cols[i], width=6)
    txt(d, cx - 26, 218, 'H', 30, cols[i])
    txt(d, cx + 56, 218, a['name'], 30, cols[i])
    txt(d, cx - 40, 290, a['key'], 32, cols[i])
    txt(d, cx - 52, 335, 'r = %.2f Å' % a['rexp'], 21, G)
    txt(d, cx - 52, 370, 'μ = %.2f D' % a['mu'], 21, G)
    txt(d, cx - 62, 405, 'D = %d kJ/mol' % a['d'], 21, G)
txt(d, 45, 490, 'Chiziqli, ikkiatomli molekulalar; bitta σ bog‘. Rang va o‘lcham shartli.', 22, N)
txt(d, 45, 535, 'Original sxematik chizma; mikrofoto yoki atom tuzilmasi tasviri emas.', 21, G)
save(im, 'guruhx')

im, d = canvas('HF eritmasida spetsiatsiya (sxematik)', 640)
d.ellipse((60, 180, 200, 320), fill='#EAF2F8', outline=N, width=4)
txt(d, 92, 225, 'HF', 34, N)
txt(d, 84, 280, 'molekula', 20, G)
d.ellipse((250, 170, 420, 340), fill='#EAF2F8', outline=N, width=4)
txt(d, 286, 210, 'HF₂⁻', 34, N)
txt(d, 272, 270, 'bifluorid', 20, G)
d.ellipse((470, 180, 610, 320), fill='#EAF2F8', outline=N, width=4)
txt(d, 498, 225, 'H₂F⁺', 34, N)
txt(d, 488, 280, 'protonlangan', 20, G)
for x in (200, 420):
    d.line((x, 250, x + 50, 250), fill=B, width=5)
txt(d, 40, 380, 'Suvda: HF + H₂O ⇌ H₃O⁺ + F⁻;  konsentratsiya oshganda HF₂⁻ va H₂F⁺ paydo bo‘ladi', 21, N)
txt(d, 40, 425, 'Konsentratsiyalangan HF — kuchsiz kislota emas, kuchli to‘xtatuvchi.', 21, B)
txt(d, 40, 470, 'Model: 0,010 M → 22,90 %;  1,000 M → 2,57 % ionizatsiya (Ka = 6,8×10⁻⁴).', 21, G)
txt(d, 40, 535, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'speciatsiyax')

im, d = canvas('Shishani HF yemirishi: sxematik kesim', 640)
d.rectangle((60, 180, 700, 250), fill='#DCEBF4')
txt(d, 80, 195, 'shisha (SiO₂ qatlami)', 24, TEAL)
d.rectangle((60, 330, 700, 400), fill='#DCEBF4')
txt(d, 80, 345, 'shisha (SiO₂ qatlami)', 24, TEAL)
d.polygon([(60, 250), (700, 250), (700, 330), (60, 330)], fill='#F3F0E6')
txt(d, 90, 270, 'eritilgan zona: H₂SiF₆ + H₂O', 24, B)
d.rectangle((250, 250, 420, 330), fill='#F6E2C0', outline=B, width=3)
txt(d, 300, 275, 'HF', 30, B)
for x in (290, 330, 370):
    d.ellipse((x, 120, x + 12, 132), fill=B)
txt(d, 250, 90, 'HF eritmasi', 24, N)
d.line((300, 140, 300, 245), fill=B, width=4)
txt(d, 60, 440, 'SiO₂ + 6HF → H₂SiF₆ + 2H₂O', 26, N)
txt(d, 60, 485, 'Model: 1 kg SiO₂ uchun 1997,9 g HF (48 % li eritmada 4162,4 g)', 21, B)
txt(d, 60, 530, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'sishax')

im, d = canvas('Saqlash va transport: idish tanlash (sxematik)', 660)
boxes = [('HF', 'PTFE / PP idish', 'Shisha mos emas', N),
         ('HCl', 'Rezina qoplangan po‘lat', 'Quvur tashimasi', TEAL),
         ('HBr', 'Shisha idish', 'Och maydon', B),
         ('HI', 'Qorong‘i idish', 'Havo va yorug‘likdan himoya', PURPLE)]
for i, (a, b, c, col) in enumerate(boxes):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 180, x + 160, 300), radius=12, outline=col, width=4)
    txt(d, x + 50, 200, a, 32, col)
    txt(d, x + 10, 250, b, 20, INK)
    txt(d, x + 14, 276, c, 19, G)
    if i < 3:
        d.line((x + 160, 240, x + 178, 240), fill=G, width=4)
txt(d, 40, 350, 'Tanlov uch uchta mezon: reaktivlik, nam va temperatura, ifloslanish.', 21, N)
txt(d, 40, 395, 'HF — ayniqsa xavfli: fluorid ioni Ca²⁺ va Mg²⁺ ni ushlab qoladi.', 21, B)
txt(d, 40, 440, 'Model: saqlash shartlari konsentratsiya, miqdor va mahalliy qoidalarga bog‘liq.', 21, G)
txt(d, 40, 500, 'Original sxematik chizma; idish turlari shartli.', 21, G)
save(im, 'logistikax')

im, d = canvas('Ishlangan hisob: uch model (sxematik)', 660)
g = glass_model(1.0, 48.0)
n = neutralisation_model(1000.0, 10.0)
blocks = [('A — HF muvozanati', 'Ka = 6,8×10⁻⁴', '0,010 M → 22,90 %; 1,000 M → 2,57 %', N),
          ('B — Azeotrop chegarasi', 'HCl 20,2 % / 108,6 °C', '1000 kg 10 % → 495,0 kg qoldiq', TEAL),
          ('C — Energetik balans', 'D + ΔH_hyd', '63 / 68 / 35 / 2 kJ/mol', B)]
for i, (a, b, c, col) in enumerate(blocks):
    y = 150 + 140 * i
    d.rounded_rectangle((50, y, 440, y + 110), radius=12, outline=col, width=4)
    txt(d, 70, y + 14, a, 26, col)
    txt(d, 70, y + 52, b, 22, INK)
    txt(d, 70, y + 82, c, 21, G)
d.rounded_rectangle((470, 150, 710, 470), radius=12, outline=PURPLE, width=4)
txt(d, 490, 170, 'Model natijalari', 26, PURPLE)
txt(d, 490, 220, 'g‘ = 1997,9 g HF', 21, INK)
txt(d, 490, 255, '(1 kg SiO₂)', 20, G)
txt(d, 490, 300, 'CaCO₃ 137,3 kg', 21, INK)
txt(d, 490, 335, 'CO₂ 60,4 kg', 21, INK)
txt(d, 490, 380, 'H₂SiF₆ 2398,3 g', 21, INK)
txt(d, 490, 425, 'kirish = chiqish', 21, N)
txt(d, 50, 540, 'Barcha sonlar ochiq shartli model; o‘lchov ma’lumoti emas.', 21, G)
txt(d, 50, 585, 'Original sxematik chizma.', 21, G)
save(im, 'hisob')
print('5 grafik + CSV; 7 sxema; 5 original illustration.')
