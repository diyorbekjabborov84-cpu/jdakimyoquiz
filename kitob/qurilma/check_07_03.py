#!/usr/bin/env python3
"""7.3 moduli uchun QA: taxminiy hisoblarning matn va hujjat bilan mosligi."""
from pathlib import Path
import csv, math, re, json
from docx import Document
import prep_07_03 as M

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'chiqish' / 'Noorganik-kislotalar-7.3-Sulfat-kislota-tuzilishi.docx'
ASSETS = ROOT / 'rasmlar' / 'sulfat'
MS = ROOT / 'matn' / '07_03.md'
fails = []


def ck(cond, msg):
    if cond:
        print('  OK  ', msg)
    else:
        print('  FAIL', msg); fails.append(msg)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print('1) Taxminiy hisob: dissotsiatsiya va spetsiatsiya')
ser = M.dissolution_series()
ck(close(ser[0]['x'], 0.00086547, 1e-6) and close(ser[0]['ph'], 2.7292, 1e-3)
   and close(ser[0]['so4_pct'], 86.546, 0.01),
   '0,001 M: x = 0,000865 mol/L;  pH = 2,729;  SO₄²⁻ 86,55 %')
ck(close(ser[3]['h'], 0.014524, 1e-5) and close(ser[3]['so4_pct'], 45.242, 0.01),
   '0,010 M: h = 0,014524 mol/L;  SO₄²⁻ 45,24 %')
ck(close(ser[6]['h'], 0.109848, 1e-5) and close(ser[6]['so4_pct'], 9.848, 0.01),
   '0,100 M: h = 0,109848 mol/L;  SO₄²⁻ 9,85 %')
ck(close(ser[9]['h'], 1.011722, 1e-5) and close(ser[9]['ph'], -0.0051, 1e-3),
   '1,000 M: h = 1,011722 mol/L;  pH = −0,01')
ck(close(ser[11]['so4_pct'], 0.2982, 0.01) and close(ser[11]['ph'], -0.6034, 1e-3),
   '4,000 M: pH = −0,60;  SO₄²⁻ 0,30 %')
sp = M.speciation_ph(1.0)
ck(close(sp['hso4'], 89.286, 0.01) and close(sp['so4'], 10.714, 0.01),
   'pH 1: HSO₄⁻ 89,29 %;  SO₄²⁻ 10,71 %')
sp = M.speciation_ph(3.0)
ck(close(sp['hso4'], 7.692, 0.01) and close(sp['so4'], 92.308, 0.01),
   'pH 3: HSO₄⁻ 7,69 %;  SO₄²⁻ 92,31 %')
sp = M.speciation_ph(7.0)
ck(close(sp['so4'], 99.9992, 1e-3), 'pH 7: SO₄²⁻ 99,999 %')
ck(close(M.KA1 / M.KA2, 8.3333e4, 1.0), 'Paulining nisbiy oraliq: 8,3×10⁴ ≈ 10⁵')

print('2) Taxminiy hisob: sufma kislota, gidratlar, kontakt, ekvivalent')
ap = M.autoprotolysis()
ck(close(ap['k_molal'], 1.695e-4, 1e-9) and close(ap['k_mole_fraction'], 1.6305e-6, 1e-9),
   'K_ap: 1,70×10⁻⁴ mol²/kg²;  mole ulushida 1,63×10⁻⁶')
ck(close(ap['c_total'], 10.196, 0.001), '100 % kislota: jami 10,196 mol/kg')
ac = M.acid_capacity()
ck(close(ac['c_pure'], 18.661, 0.01) and close(ac['h_per_l_pure'], 37.32, 0.02),
   '100 % kislota: 18,66 mol/L;  proton zaxirasi 37,32 mol H⁺/L')
hy = M.hydrate_composition()
for r, wt in zip(hy, [84.48, 73.13, 64.47, 57.65, 45.58, 40.49]):
    ck(close(r['wt_calc'], wt, 0.01), 'gidrat %s: hisob %.2f %% ≈ jadval' % (r['name'], wt))
cc = M.contact()
ck(close(cc['m_s'], 326.883, 0.01) and close(cc['m_so2'], 653.154, 0.01)
   and close(cc['m_o2'], 163.135, 0.01) and close(cc['m_h2o'], 183.680, 0.01),
   'kontakt moddiy balansi: S 326,9;  SO₂ 653,2;  O₂ 163,1;  H₂O 183,7 kg')
ol = M.oleum()
ck(close(ol['m_oleum'], 1163.258, 0.01) and close(ol['w_so3'], 14.035, 0.01)
   and close(ol['m_h2so4_final'], 1199.994, 0.01),
   'oleum: 1163,3 kg;  erkin SO₃ 14,0 %;  suyultirishda 1200,0 kg')
eq = M.equivalents()
ck(close(eq['h2so4'], 49.039, 1e-6), 'ekvivalent massa: 49,04 g/eq')
ck(close(M.CRYSTAL_A * M.CRYSTAL_B * M.CRYSTAL_C * math.sin(math.radians(M.CRYSTAL_BETA)) / 1000.0,
         306313.3, 1.0), 'kristal hujra hajmi: 306 313 pm³')
ck(close(123.3 + 101.3 + 106.4 + 108.7, 439.7, 1e-6), 'burchaklar yig‘indisi 439,7°')
ck(close(4 * 109.47, 437.88, 1e-6), 'tetraedrik ideal 437,9°')

print('3) CSV fayllar va rasmlar')
for name, n in [('dissotsiatsiya', 12), ('kislotalik', 9), ('geometriya', 13),
                ('spektra', 14), ('gidratlar', 6), ('sufma', 8), ('kristal', 11),
                ('xavfsizlik', 8), ('sanoat', 9), ('ekvivalent', 5)]:
    rows = list(csv.DictReader((ASSETS / (name + '.csv')).open()))
    ck(len(rows) == n, '%s.csv: %d qator' % (name, len(rows)))
pngs = sorted(p.stem for p in ASSETS.glob('*.png'))
ck(len(pngs) == 17, 'rasmlar soni: %d' % len(pngs))
for n in ['spektr', 'kislotalik', 'dissotsiatsiya', 'gidratlar', 'sanoat',
          'geometriax', 'rezonansx', 'sufmax', 'ionlarx', 'gidratx', 'kristalx', 'xavfsizlikx',
          'molekulax', 'tabiiyx', 'tuzlarilx', 'gidratilx', 'zavodx']:
    ck(n in pngs, 'rasm %s.png bor' % n)

print('4) Matn: taxminiy hisob raqamlari va atamalar')
ms = MS.read_text()
tables_txt = json.dumps(json.loads((ROOT / 'matn' / '07_03_jadvallar.json').read_text()), ensure_ascii=False)
notes_txt = json.dumps(json.loads((ROOT / 'matn' / '07_03_yonlavhalar.json').read_text()), ensure_ascii=False)
ms_all = ms + tables_txt + notes_txt
need = ['98,08', '97,9674', '142,2', '157,4', '97,0', '123,3', '101,3', '108,5', '89,1',
        '140,99', '157,51', '86,66', '699,4', '666,9', '1265', '574', '−1091',
        '981', '451', '1104', '617', '1055', '1030', '900', '3603', '1248', '792', '499',
        'K_a1 ≈ 10³', '1,2×10⁻²', '1,99', '8,3×10⁴', '10⁵',
        '2,73', '86,55', '1,84', '45,24', '0,96', '9,85', '1,011722', '−0,01', '1,17',
        '0,000865', '0,001865', '−0,60', '0,30', '0,014524', '0,109848',
        '1,70×10⁻⁴', '1,63×10⁻⁶', '10,196', '37,3', 'H₀ = −12',
        '147,2', '109,47', '6 kanonik', '−0,5 e', '5,0 pm', '10,2 pm',
        '84,5', '73,1', '64,5', '57,6', '45,6', '40,5', '84,48', '40,49', '3,63',
        '818,1', '469,60', '856,3', '111,39', '306 313', '76 578', '2,13',
        '260–290', '56–60', '30 mln', '14 mln', '99,7', '326,9', '653,2', '163,1', '183,7',
        '1163,3', '14,0', '49,04', '192 970',
        '1 mg/m³', '0,2 mg/m³', '15 mg/m³', '2 / 10 / 120', 'IARC 1']
for x in need:
    ck(x in ms_all, 'matnda «%s» bor' % x)
ck(ms.count('[[EQ:') == 11 and ms.count('[[TABLE:') == 11, 'matnda 11 formula va 11 jadval belgisi')
ck(len(re.findall(r'^## ', ms, flags=re.M)) == 11, 'matnda 11 bo‘lim')
ck('amaliyot tavsiyalari berilmaydi' in ms, 'xavfsizlik chegarasi matnda bayon qilindi')
ck('o‘lchov ma’lumoti emas' in ms, 'taxminiy hisob cheklovi matnda ko‘rsatilgan')
ck('taxminiy hisob' in ms.lower(), 'terminologiya: «taxminiy hisob» ishlatilgan')
ck('model' not in ms_all.lower(), 'terminologiya: «model» yo‘q')
ck('sulfat kislota' in ms and 'sulfat ioni' in ms and 'gauche' in ms.lower()
   and 'C₂' in ms, 'mavzu kalit tushunchalari matnda')
ck('$' not in ms, 'matnda dollar belgisi yo‘q')
ck(not re.search(r'[Ѐ-ӿ]', ms_all), 'matnda kirill harflari yo‘q')
ck(not re.search(r'[　-鿿]', ms_all), 'matnda CJK belgilar yo‘q')

print('5) DOCX tuzilmasi')
doc = Document(DOCX)
xml = doc.element.xml


def collect(container):
    out = []
    for t in container.tables:
        for row in t.rows:
            for c in row.cells:
                out.append(c.text)
                out.extend(collect(c))
    return out


text_all = '\n'.join(p.text for p in doc.paragraphs)
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                text_all += '\n' + p.text
            text_all += '\n' + '\n'.join(collect(c))
ck(len(doc.inline_shapes) == 17, 'rasmlar soni: %d' % len(doc.inline_shapes))
import equations_07_03 as EQ
n_eq = sum(len(g) for g in EQ.sulfate_equations())
ck(xml.count('<m:oMath') == n_eq, 'OMML satrlari: %d (kutilgan %d)' % (xml.count('<m:oMath'), n_eq))
ck(xml.count('<m:f>') >= 1, 'kasrlar: %d' % xml.count('<m:f>'))
ck(xml.count('<m:sSub>') >= 40, 'pastki indekslar: %d' % xml.count('<m:sSub>'))
ck(xml.count('sSup') >= 1, 'yuqori indekslar: %d' % xml.count('sSup'))
ck(text_all.count('-jadval.') == 11, 'jadval sarlavhalari: %d' % text_all.count('-jadval.'))
ck(text_all.count('-sxema.') == 7, 'sxema sarlavhalari: %d' % text_all.count('-sxema.'))
ck(text_all.count('-grafik.') == 5, 'grafik sarlavhalari: %d' % text_all.count('-grafik.'))
ck(text_all.count('-rasm.') == 5, 'rasm sarlavhalari: %d' % text_all.count('-rasm.'))
for i in range(1, 12):
    ck(text_all.count('(7.3.%d)' % i) == 1, 'formula raqami (7.3.%d)' % i)
ck('_' not in text_all, 'matnda "_" qolmadi (pastki indeksga o‘girilgan)')
ck('**' not in text_all, 'matnda "**" markerlari qolmadi')
omml_txt = ''.join(re.findall(r'<m:t[^>]*>([^<]*)</m:t>', xml))
ck('_' not in omml_txt, 'OMML matnida "_" qolmadi (pastki indeks native)')
ck('Times New Roman' in xml, 'Times New Roman shrifti qo‘llangan')
ck('Cambria Math' in xml, 'formulalar Cambria Math shriftida')
ck(text_all.count('HISOBIY GRAFIK') == 5, 'grafik yorliqlari: %d' % text_all.count('HISOBIY GRAFIK'))
ck(text_all.count('TUSHUNTIRUVCHI SXEMA') == 3, 'sxema yorliqlari: %d' % text_all.count('TUSHUNTIRUVCHI SXEMA'))
ck(text_all.count('CHIZMA VA IZOH') == 3, 'chizma yorliqlari: %d' % text_all.count('CHIZMA VA IZOH'))
ck('NOORGANIK KISLOTALAR' in doc.sections[0].header.paragraphs[0].text, 'sarlavha matni')
ck('7-BOB' in doc.sections[0].footer.paragraphs[0].text, 'kolontitul matni')
for x in ['98,08', '142,2', '1,70×10', '1163,3', 'IDLH', '49,04']:
    ck(x in text_all, 'DOCX matnida «%s» bor' % x)
ck('OSHA' in text_all and 'NIOSH' in text_all and 'NIST' in text_all,
   'adabiyotlar ro‘yxati joylashdi')
ck('amaliyot tavsiyalari berilmaydi' in text_all, 'xavfsizlik chegarasi bayon qilindi')
size = DOCX.stat().st_size
ck(size > 400000, 'DOCX hajmi: %d bayt' % size)

print()
if fails:
    print('XATO: %d tekshiruv bajarilmadi' % len(fails))
    for f in fails: print('  -', f)
    raise SystemExit(1)
print('BARCHA TEKSHIRUVLAR O‘TDI (7.3).')
