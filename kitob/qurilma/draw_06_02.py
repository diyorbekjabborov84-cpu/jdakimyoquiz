"""Original teaching figures for 6.2 "HF — ftorid kislota".
All curves are model outputs computed from tabulated standard data, not measurements.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, math
from prep_06_02 import (ASSETS as A, AHF, ETCH_K, speciation_series, etch_rate,
                         passivation, waste_model, residual_fluoride,
                         calcium_requirement, production_model, glass_model)

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


# --- Graph 1: suvli HF spetsiatsiyasi -------------------------------------
im, d = canvas('Suvli HF: zarrachalarning ulushi konsentratsiyaga bog‘liq', 1180)
p = axes(d, -0.5, 7.5, 0, 100, '', 'ulush, %',
         [(0, '0,01'), (1, '0,05'), (2, '0,1'), (3, '0,5'), (4, '1,0'), (5, '2,0'), (6, '5,0'), (7, '10')],
         [(0, '0'), (25, '25'), (50, '50'), (75, '75'), (100, '100')])
spec = speciation_series()
for i, s in enumerate(spec):
    x = p(i, 0)[0]
    vals = [(s['w_hf'], N, 'HF'), (s['w_f'], TEAL, 'F⁻'), (s['w_hf2'], B, 'HF₂⁻')]
    y = 700
    for v, col, lab in vals:
        h = v / 100.0 * 525
        d.rectangle((x - 34, y - h, x + 34, y), fill=col)
        y -= h
    txt(d, x - 30, 690, '%.1f' % s['w_hf'], 19, '#FFFFFF')
d.rectangle((430, 128, 456, 150), fill=N); txt(d, 464, 128, 'HF', 21, N)
d.rectangle((520, 128, 546, 150), fill=TEAL); txt(d, 554, 128, 'F⁻', 21, TEAL)
d.rectangle((610, 128, 636, 150), fill=B); txt(d, 644, 128, 'HF₂⁻', 21, B)
txt(d, 45, 830, 'Model: Ka = 6,8×10⁻⁴; lgK(HF + F⁻ ⇌ HF₂⁻) = 0,7; ideal erituvchi modeli', 22, N)
txt(d, 45, 880, 'pH: 2,635 (0,01 M) → 1,238 (1,0 M) → 0,277 (10 M)', 22, B)
txt(d, 45, 930, 'Model faolik koeffitsiyentlarni hisobga olmaydi; real eritmada HF₂⁻ ulushi kattaroq', 22, G)
txt(d, 45, 1000, 'Model egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'spetsiatsiya')

# --- Graph 2: yemirish tezligi --------------------------------------------
im, d = canvas('SiO₂ yemirish tezligi: HF konsentratsiyasi va zarracha hissi', 1180)
p = axes(d, -0.5, 7.5, 0, 6000, 'jami HF konsentratsiyasi, M', 'tezlik, Å/min',
         [(0, '0,05'), (1, '0,1'), (2, '0,25'), (3, '0,5'), (4, '1,0'), (5, '2,0'), (6, '4,0'), (7, '8,0')],
         [(0, '0'), (1500, '1500'), (3000, '3000'), (4500, '4500'), (6000, '6000')])
er = [etch_rate(c) for c in (0.05, 0.10, 0.25, 0.50, 1.0, 2.0, 4.0, 8.0)]
for i, e in enumerate(er):
    x = p(i, 0)[0]
    y = 700
    for v, col in [(e['r_f'], TEAL), (e['r_hf'], N), (e['r_hf2'], B)]:
        h = v / 6000.0 * 525
        d.rectangle((x - 32, y - h, x + 32, y), fill=col)
        y -= h
    txt(d, x - 36, y - 30, '%d' % round(e['r']), 18, B)
d.rectangle((430, 128, 456, 150), fill=TEAL); txt(d, 464, 128, 'F⁻ ulushi', 21, TEAL)
d.rectangle((570, 128, 596, 150), fill=N); txt(d, 604, 128, 'HF', 21, N)
d.rectangle((430, 164, 456, 186), fill=B); txt(d, 464, 164, 'HF₂⁻', 21, B)
txt(d, 45, 830, 'Model: r = 510[F⁻] + 610[HF] + 2890[HF₂⁻] (Å/min) — empirik kinetik qonun', 22, N)
txt(d, 45, 880, '0,10 M → 65,1 Å/min;  1,00 M → 687,8;  4,00 M → 2778,7;  8,00 M → 5567,7 Å/min', 22, B)
txt(d, 45, 930, 'HF₂⁻ ulushi 13 % dan 21 % gacha; qolgani HF va F⁻ hissiga', 22, G)
txt(d, 45, 1000, 'Model egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'yemirish')

# --- Graph 3: passivatsiya -------------------------------------------------
im, d = canvas('Metallning fluoridga aylanishi (1 g metall)', 1180)
p = axes(d, 0, 4, 0, 3.6, '', 'g fluorid / g metall',
         [(0, 'Al'), (1, 'Fe'), (2, 'Ni'), (3, 'Cu')],
         [(0, '0'), (0, '0'), (1, '1'), (2, '2'), (3, '3'), (3.6, '3,6')])
for i, mt in enumerate(passivation(1.0)):
    x = p(i, 0)[0]
    h = mt['ratio'] / 3.6 * 525
    d.rectangle((x - 42, 700 - h, x + 42, 700), fill=N if i < 2 else TEAL)
    txt(d, x - 36, 700 - h - 30, '%.3f g' % mt['ratio'], 21, INK)
    txt(d, x - 44, 755, mt['salt'], 20, G)
d.rectangle((430, 128, 456, 150), fill=N); txt(d, 464, 128, 'Al va Fe: mustahkam qatlam', 21, N)
d.rectangle((430, 164, 456, 186), fill=TEAL); txt(d, 464, 164, 'Ni va Cu: zaifroq', 21, TEAL)
txt(d, 45, 830, 'Model: 1 g Al → 3,113 g AlF₃ (HF 1,483 g, H₂ 0,112 g);  1 g Fe → 2,326 g FeF₃', 22, N)
txt(d, 45, 880, '1 g Ni → 1,647 g NiF₂ (HF 0,682 g);  1 g Cu → 1,598 g CuF₂ (HF 0,630 g)', 22, B)
txt(d, 45, 930, 'Qatlam reaksiyani to‘xtatadi — bu passivatsiya, emas, oddiy yemirish emas', 22, G)
txt(d, 45, 1000, 'Model chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'passivatsiya')

# --- Graph 4: chiqindi boshqaruv -------------------------------------------
im, d = canvas('Chiqindi: neytralizatsiya mass balansi va qoldiq fluorid', 1180)
w = waste_model(1000.0, 10.0)
p = axes(d, -0.5, 3.5, 0, 420, '', 'kg',
         [(0, 'HF'), (1, 'Ca(OH)₂'), (2, 'CaF₂'), (3, 'H₂O')],
         [(0, '0'), (100, '100'), (200, '200'), (300, '300'), (400, '400')], y1=420)
items = [('HF (kirish)', w['m_hf'], N), ('Ca(OH)₂ (kirish)', w['m_caoh2'], TEAL),
         ('CaF₂ (cho‘kma)', w['m_caf2'], B), ('H₂O (hosil)', w['m_h2o'], GREEN)]
for i, (name, v, col) in enumerate(items):
    x = p(i, 0)[0]
    h = v / 420.0 * 245
    d.rectangle((x - 40, 420 - h, x + 40, 420), fill=col)
    txt(d, x - 40, 420 - h - 30, '%.1f kg' % v, 21, col)
# pastki panel: qoldiq F-
d.line((120, 480, 120, 700, 680, 700), fill=G, width=3)
txt(d, 470, 448, 'qoldiq F⁻, mg/L  (Ca²⁺, M)', 24, G)
cas = [0.001, 0.005, 0.010, 0.050, 0.100]
for k, ca in enumerate(cas):
    r = residual_fluoride(ca)
    x = 170 + k * 120
    y = 700 - min(r['f_mg'], 4.2) / 4.2 * 220
    d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=RED if ca == 0.001 else B,
              outline='#FFFFFF', width=2)
    txt(d, x - 26, y - 32, '%.2f' % r['f_mg'], 20, INK)
    txt(d, x - 18, 712, '%g' % ca, 20, INK)
yl = 700 - 1.5 / 4.2 * 220
d.line((130, yl, 680, yl), fill=RED, width=3)
txt(d, 480, yl - 30, 'chegara 1,5 mg/L', 19, RED)
txt(d, 45, 830, 'Model: 2HF + Ca(OH)₂ → CaF₂ + 2H₂O; 1000 kg 10 % li HF uchun Ca(OH)₂ 185,2 kg kerak', 22, N)
txt(d, 45, 880, 'CaF₂ 195,1 kg va H₂O 90,0 kg hosil bo‘ladi; kirish 285,2 kg = chiqish 285,2 kg', 22, B)
txt(d, 45, 930, 'Qoldiq F⁻: K_sp(CaF₂) = 3,9×10⁻¹¹ bo‘yicha model — ohak ortiqchasi kerak', 22, G)
txt(d, 45, 1000, 'Model chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'chiqindi')

# --- Graph 5: kaltsiy talabi ------------------------------------------------
im, d = canvas('Fluoridni bog‘lash uchun kaltsiy stoxiometriyasi', 1180)
p = axes(d, -0.5, 5.5, 0, 1300, 'HF massi, g', 'kalsiy glyukonat, g',
         [(0, '1'), (1, '5'), (2, '10'), (3, '20'), (4, '50'), (5, '100')],
         [(0, '0'), (300, '300'), (600, '600'), (900, '900'), (1200, '1200')])
xs = [1.0, 5.0, 10.0, 20.0, 50.0, 100.0]
pts = []
for i, m in enumerate(xs):
    c = calcium_requirement(m)
    x, y = p(i, c['m_caglu'])
    pts.append((x, y))
    d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=B, outline='#FFFFFF', width=2)
    txt(d, x - 44, y - 36, '%.0f' % c['m_caglu'], 19, B)
d.line(pts, fill=N, width=5)
txt(d, 45, 830, 'Model: 20 g HF → 0,500 mol Ca²⁺ → 224,1 g kalsiy glyukonat (yoki 55,5 g CaCl₂)', 22, N)
txt(d, 45, 880, '100 g HF → 2,499 mol Ca²⁺ → 1120,6 g kalsiy glyukonat', 22, B)
txt(d, 45, 930, 'Stoksiometrik hisob — tibbiy doza bo‘yicha tavsiya emas', 22, G)
txt(d, 45, 1000, 'Model egri chizig‘i; o‘lchov ma’lumoti emas', 23, G)
save(im, 'kalsiy')


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


scheme('olishsx', 'Ishlab chiqarish, tozalash va qayta foydalanish (sxematik)', [
    ('Xom ashyo', 'Fluorit CaF₂ (97 % model)', 'Yagona tabiiy manba'),
    ('Reaksiya', 'CaF₂ + H₂SO₄ → 2HF + CaSO₄', 'Model: HF 457,3 kg / 1000 kg fluorit'),
    ('Ajratish va tozalash', 'Quruq holda distillatsiya', 'Suv bilan tozalash mumkin emas'),
    ('Mahsulot', '48–50 % li eritma; yupqa HF 99,99 %+', 'Yarim o‘tkazgich darajasi'),
    ('Qayta tiklash', 'Skrubber → CaF₂ cho‘kma → kalsinatsiya → HF', 'CaF₂ — kriyolit kabi xom ashyo')])

scheme('anidrsx', 'Anhidr HF erituvchi tizimi (sxematik)', [
    ('O‘z-o‘zini ionlashuv', '3HF ⇌ H₂F⁺ + HF₂⁻', 'K_self = 2×10⁻¹² (273 K)'),
    ('Proton holati', 'H₂F⁺ va solvatsiyalangan agregatlar', 'Mustaqil H⁺ yo‘q'),
    ('Kationlar', 'Yomon solvatatsiya qilinadi', 'Ko‘p tuzlar yomon eriydi'),
    ('Kislota qabul qiluvchi', 'BF₃, PF₅, AlF₃, SbF₅', 'F⁻ ni tortadi — kislotalik kuchayadi'),
    ('Superkislota', 'SbF₅ + 2HF ⇌ H₂F⁺ + SbF₆⁻', 'H₀ ≈ −21; 1:1 aralashma < −28')])

scheme('shishasx', 'Shishani yemirish mexanizmi (sxematik)', [
    ('Sirtda', 'Si–O–Si bog‘i HF bilan zaiflanadi', 'Suv katalitik ishtirok qiladi'),
    ('Asosiy tenglik', 'SiO₂ + 6HF → H₂SiF₆ + 2H₂O', 'Model: 1 kg SiO₂ → 1997,8 g HF'),
    ('Gaz fazasida', 'SiO₂ + 4HF → SiF₄↑ + 2H₂O', 'SiF₄ + 2HF → H₂SiF₆'),
    ('Tezlik qonuni', 'r = 510[F⁻] + 610[HF] + 2890[HF₂⁻] Å/min', 'Chiziqli bog‘liqlik'),
    ('Kamchilik', 'H₂SiF₆ to‘planishi yemirishni sekinlashtiradi', 'Nazorat talab qiladi')])

scheme('passivatsiyasx', 'Metallarning fluoridli passivatsiyasi (sxematik)', [
    ('Boshlang‘ich sirt', 'Metall + oksid qatlami', 'HF oksidni eritadi'),
    ('Reaksiya', '2Al + 6HF → 2AlF₃ + 3H₂↑', 'Model: 1 g Al → 3,113 g AlF₃'),
    ('Qatlam', 'Zich, uzluksiz, yopuvchi', 'Reaksiyani to‘xtatadi'),
    ('Barqarorlik farqi', 'Al va Fe — mustahkam; Ni va Cu — zaif', 'Cu qatlami teshikli bo‘lishi mumkin'),
    ('Sanoat maqsadi', 'Aniq profil va toza sirt', 'Yakuniy himoya — boshqa usul')])

scheme('komplekssx', 'Fluoridlar va komplekslar (sxematik)', [
    ('Oddiy fluoridlar', 'NaF, KF, AlF₃, CaF₂', 'CaF₂ — HF ning xom ashyosi'),
    ('Kriyolit', 'Na₃AlF₆', 'Alyumin elektrolizining elektroliti'),
    ('Kompleks anionlar', 'AlF₆³⁻, BF₄⁻, PF₆⁻, SbF₆⁻', 'Barqaror, lekin kuchsiz nukleofil'),
    ('Fluorosilitsiy kislota', 'H₂SiF₆', 'Suv tozalash va katalizator'),
    ('Suv chegaralari', 'WHO 1,5 mg/L · AQSh MCL 4,0 mg/L', 'Ikkilamchi standart 2,0 mg/L')])

scheme('xavfsizliksx', 'Xavfsizlik zanjiri: oldini olish → aniqlash → javob (sxematik)', [
    ('Oldini olish', 'Material mosligi (PTFE/PP), ventilyatsiya, shaxsiy himoya', 'Shisha idish mos emas'),
    ('Aniqlash', 'Gaz monitori, T va nam nazorati', 'Kuzatuv nuqtalari'),
    ('Tezlik javobi', 'Ko‘p suv bilan yuvish, tibbiy yordam', 'Kalsiy glyukonat — asosiy vosita'),
    ('Tizimli xavf', 'F⁻ Ca²⁺ va Mg²⁺ ni bog‘laydi', 'Gipokalsemiya, aritmiya'),
    ('Chegaralar', 'OSHA 3 ppm · ACGIH 0,5 ppm (F) · IDLH 30 ppm', 'Kechikuvchi og‘riq')])

scheme('fizikx', 'Anhidr HF: fizik xossalar va erituvchi sifatida (sxematik)', [
    ('Suyuqlanish diapazoni', '190–292,5 K', 'Keng diapazon — qulay erituvchi'),
    ('Nisbiy o‘tkazuvchanlik', 'ε = 84 (273 K); 175 (200 K)', 'Kationlarni yomon solvatatsiya qiladi'),
    ('Hydrogen bog‘i', 'Molekulalar zanjiri hosil qiladi', 'Suyuq fazada polimerlanish'),
    ('O‘z-o‘zini ionlashuv', '3HF ⇌ H₂F⁺ + HF₂⁻', 'K_self = 2×10⁻¹² (273 K)'),
    ('Proton holati', 'H₂F⁺ va solvatsiyalangan agregatlar', 'Mustaqil H⁺ yo‘q — erituvchi mantiqi')])


# --- Original illustrasiyalar ---------------------------------------------
im, d = canvas('HF molekulasi va hydrogen bog‘i zanjiri (sxematik)', 620)
for i in range(5):
    x = 95 + 150 * i
    d.ellipse((x - 30, 210, x + 30, 270), fill='#FFFFFF', outline=N, width=4)
    d.ellipse((x + 40, 210, x + 100, 270), fill='#FFFFFF', outline=TEAL, width=4)
    d.line((x + 30, 240, x + 40, 240), fill=B, width=6)
    txt(d, x - 20, 226, 'H', 30, N)
    txt(d, x + 56, 226, 'F', 30, TEAL)
    if i < 4:
        for k in range(3):
            d.ellipse((x + 102 + k * 13, 233, x + 110 + k * 13, 241), fill=B)
d.rectangle((60, 320, 700, 372), fill='#EAF2F8')
txt(d, 80, 333, 'zanjir:  F–H···F–H···F–H   (H-bond orqali)', 25, N)
txt(d, 60, 410, 'Suyuq HF da molekulalar zanjirlar hosil qiladi — shuning uchun qaynash harorati 19,5 °C.', 21, N)
txt(d, 60, 455, 'Guruhdagi boshqa a’zolar: HCl −85,1 °C, HBr −66,8 °C, HI −35,4 °C.', 21, B)
txt(d, 60, 500, 'Model: r(H–F) = 0,917 Å; D = 569 kJ/mol; χ(F) = 3,98; μ = 1,8–1,9 D.', 21, G)
txt(d, 60, 565, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'molekulax')

im, d = canvas('Fluorid qatlami: metall sirtidagi himoya plyonkasi (sxematik)', 640)
d.rectangle((60, 190, 700, 250), fill='#DCEBF4')
txt(d, 85, 205, 'muhit (kislota)', 24, TEAL)
d.rectangle((60, 330, 700, 470), fill='#D9D4C8')
txt(d, 85, 385, 'metal (Al, Fe, Ni, Cu)', 24, INK)
d.rectangle((60, 250, 700, 330), fill='#F6E2C0', outline=B, width=3)
txt(d, 95, 268, 'zich fluorid qatlami:  AlF₃ / FeF₃ / NiF₂ / CuF₂', 24, B)
d.rectangle((250, 288, 420, 308), fill=B)
txt(d, 296, 290, 'AlF₃', 22, '#FFFFFF')
d.rectangle((430, 288, 560, 308), fill=TEAL)
txt(d, 470, 290, 'FeF₃', 22, '#FFFFFF')
d.ellipse((150, 282, 166, 298), fill=RED)
d.ellipse((600, 282, 616, 298), fill=RED)
txt(d, 60, 505, 'Model: 1 g Al → 3,113 g AlF₃; 1 g Fe → 2,326 g FeF₃ (qatlam zichligi shartli).', 21, N)
txt(d, 60, 545, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'qatlamx')

im, d = canvas('Yarim o‘tkazgich tozalash: qatlam va membrana (sxematik)', 640)
d.rectangle((90, 220, 670, 420), fill='#DDE6F2')
txt(d, 120, 240, 'Si plokasi', 26, N)
d.rectangle((90, 160, 670, 220), fill='#EAF2F8')
txt(d, 110, 175, 'SiO₂ qatlami (nazorat qilinadi)', 23, TEAL)
for i, x in enumerate((120, 260, 400, 540)):
    d.rectangle((x, 150, x + 90, 160), fill=TEAL)
    d.ellipse((x + 20, 130, x + 70, 150), fill='#FFFFFF', outline=TEAL, width=3)
d.ellipse((330, 90, 420, 130), fill=B)
txt(d, 300, 55, 'HF', 28, B)
for x in (350, 370, 390):
    d.line((x, 130, x, 160), fill=B, width=4)
txt(d, 90, 460, 'Sxematik: yuqorida SiO₂ qatlami, pastda Si substrati; HF faqat qatlamni eritadi.', 21, N)
txt(d, 90, 500, 'Selektivlik SiO₂ : Si₃N₄ : Si ≈ 1 : >100 : 0,1 — aynan shu nisbat texnologiyani imkon qiladi.', 21, B)
txt(d, 90, 555, 'Original sxematik chizma; rang va o‘lcham shartli.', 21, G)
save(im, 'plyotax')

im, d = canvas('HF saqlash va transport (sxematik)', 660)
boxes = [('A', 'Yupqa HF', 'PTFE / PP idish', N),
         ('B', '48–50 % eritma', 'Rezina qoplama idish', TEAL),
         ('C', 'Transport', 'Maxsus idish, cheklangan', B),
         ('D', 'Qayta tiklash', 'CaF₂ → kalsinatsiya', PURPLE)]
for i, (a, b, c, col) in enumerate(boxes):
    x = 40 + 180 * i
    d.rounded_rectangle((x, 180, x + 160, 320), radius=12, outline=col, width=4)
    d.ellipse((x + 52, 195, x + 108, 251), fill=col)
    txt(d, x + 72, 206, a, 28, '#FFFFFF')
    txt(d, x + 12, 265, b, 21, INK)
    txt(d, x + 8, 292, c, 19, G)
    if i < 3:
        d.line((x + 160, 250, x + 178, 250), fill=G, width=4)
txt(d, 40, 370, 'Tanlov mezonlari: reaktivlik (shisha mos emas), nam, temperatura, ifloslanish.', 21, N)
txt(d, 40, 410, 'HF gaz holatida ham ajratiladi — ventilyatsiya va gaz monitori talab qiladi.', 21, B)
txt(d, 40, 450, 'Model: saqlash shartlari konsentratsiya, miqdor va mahalliy qoidalarga bog‘liq.', 21, G)
txt(d, 40, 520, 'Original sxematik chizma; idish turlari shartli.', 21, G)
save(im, 'idishx')

im, d = canvas('Ishlangan hisob: to‘rt model (sxematik)', 660)
g = glass_model(1.0, 48.0)
w = waste_model(1000.0, 10.0)
c = calcium_requirement(20.0)
blocks = [('A — Spetsiatsiya', 'Ka = 6,8×10⁻⁴', '1,000 M: HF 89,5 %, F⁻ 1,1 %', N),
          ('B — Yemirish', 'SiO₂ + 6HF', '1 kg SiO₂ → HF 1997,8 g', TEAL),
          ('C — Chiqindi', 'Ca(OH)₂ bilan', 'CaF₂ 195,1 kg / 1000 kg', B),
          ('D — Kaltsiy', '2HF + Ca²⁺', '20 g HF → 224,1 g glyukonat', PURPLE)]
for i, (a, b, cc, col) in enumerate(blocks):
    y = 140 + 125 * i
    d.rounded_rectangle((40, y, 440, y + 100), radius=12, outline=col, width=4)
    txt(d, 60, y + 10, a, 25, col)
    txt(d, 60, y + 44, b, 21, INK)
    txt(d, 60, y + 70, cc, 20, G)
d.rounded_rectangle((460, 140, 710, 540), radius=12, outline=GREEN, width=4)
txt(d, 480, 158, 'Model natijalari', 24, GREEN)
txt(d, 480, 205, 'pH 1,238 (1,0 M)', 20, INK)
txt(d, 480, 240, 'r = 687,8 Å/min', 20, INK)
txt(d, 480, 275, '(1,00 M HF)', 19, G)
txt(d, 480, 320, 'CaF₂ 195,1 kg', 20, INK)
txt(d, 480, 355, 'F⁻ 1,186 mg/L', 20, INK)
txt(d, 480, 390, '(Ca²⁺ 0,010 M)', 19, G)
txt(d, 480, 435, 'Ca²⁺ 0,500 mol', 20, INK)
txt(d, 480, 470, 'kalsiy glyukonat', 19, G)
txt(d, 40, 585, 'Barcha sonlar ochiq shartli model; o‘lchov ma’lumoti emas.', 21, G)
save(im, 'hisob')
print('5 grafik + CSV; 7 sxema; 5 original illustration.')
