#!/usr/bin/env python3
"""7.1 moduli uchun QA: taxminiy hisoblarning matn va hujjat bilan mosligi."""
from pathlib import Path
import csv, math, re, json
from docx import Document
import prep_07_01 as M

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'chiqish' / 'Noorganik-kislotalar-7.1-Vodorod-sulfid.docx'
ASSETS = ROOT / 'rasmlar' / 'h2s'
MS = ROOT / 'matn' / '07_01.md'
fails = []


def ck(cond, msg):
    if cond:
        print('  OK  ', msg)
    else:
        print('  FAIL', msg); fails.append(msg)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print('1) Taxminiy hisob: kislotalik, spetsiatsiya va sulfid ioni')
ss = M.saturated_solution()
ck(close(ss['c'], 0.1168, 1e-4) and close(ss['ph'], 3.99, 0.01),
   'to‘yingan eritma: c = 0,1168 mol/L;  pH = 3,99')
ck(close(ss['h'], 1.03e-4, 1e-6), 'to‘yingan eritma: h = 1,03×10⁻⁴ mol/L')
sp = M.speciation(7.4)
ck(close(sp['h2s'], 30.43, 0.01) and close(sp['hs'], 69.56, 0.01)
   and close(sp['s2'], 0.0021, 1e-4),
   'pH 7,4: H₂S 30,43 %;  HS⁻ 69,56 %;  S²⁻ 0,0021 %')
sp = M.speciation(10.0)
ck(close(sp['hs'], 98.71, 0.01) and close(sp['s2'], 1.18, 0.01),
   'pH 10: HS⁻ 98,71 %;  S²⁻ 1,18 %')
ck(close(M.sulfide_ion(0.100, 1.0), 1.09e-18, 1e-20),
   '[S²⁻] pH 1 da = 1,09×10⁻¹⁸ mol/L')
ck(close(M.sulfide_ion(0.100, 7.0), 1.09e-6, 1e-8),
   '[S²⁻] pH 7 da = 1,09×10⁻⁶ mol/L')
ck(close(M.KA1, 9.1e-8) and close(M.KA2, 1.2e-12),
   'K_a1 = 9,1×10⁻⁸;  K_a2 = 1,2×10⁻¹²')
ck(close(M.Kw / M.KA2 if hasattr(M, 'Kw') else 1e-14 / M.KA2, 8.3e-3, 1e-4),
   'K_b(S²⁻) = K_w/K_a2 ≈ 8,3×10⁻³')
p = M.ph_of(0.010)
ck(close(p['h'], 3.012e-5, 1e-7) and close(p['pct'], 0.301, 0.01)
   and close(p['ph'], 4.521, 1e-2), '0,010 M: h = 3,01×10⁻⁵ M;  α = 0,30 %;  pH = 4,52')
p = M.ph_of(0.100)
ck(close(p['pct'], 0.0953, 1e-3) and close(p['ph'], 4.021, 1e-2),
   '0,100 M: α = 0,095 %;  pH = 4,02')

print('2) Taxminiy hisob: fizik, cho‘qma, neytralizatsiya, yodometriya, Claus')
ck(close(M.vapor_pressure(298.15), 23.68, 0.01), 'p(25 °C) = 23,68 bar (Clausius–Clapeyron)')
ck(close(M.P_25 / 760.0 * 1.01325, 20.80, 0.01), 'jadvaldagi p(25 °C) = 20,80 bar')
ck(close(100.0 * (M.vapor_pressure(298.15) - M.P_25 / 760.0 * 1.01325)
          / (M.P_25 / 760.0 * 1.01325), 13.8, 0.2), 'C–C farqi: +13,8 %')
h, pb, c = M.henry_constant()
ck(close(h * 100.0, 17800, 60) and close(c, 0.1168, 1e-4),
   'Henry: H = p/c ≈ 17 800 kPa·L/mol;  c = 0,1168 mol/L')
ck(close(M.gas_density(273.15), 1.5205, 1e-3) and close(M.gas_density(298.15), 1.3930, 1e-3),
   'ρ_gaz: 273,15 K da 1,520 g/L;  298,15 K da 1,393 g/L')
rows = {r['ph']: r for r in M.precipitation(0.100, (1.0, 7.0))}
ck(close(rows[1.0]['PbS'], 2.93e-10, 1e-12), 'PbS: pH 1 da [Pb²⁺] = 2,93×10⁻¹⁰ mol/L')
ck(close(rows[7.0]['PbS'], 2.93e-22, 1e-24), 'PbS: pH 7 da [Pb²⁺] = 2,93×10⁻²² mol/L')
ksp = {s[1]: s[2] for s in M.SULFIDES}
ck(close(ksp['CaS'], 8.0e-6) and close(ksp['ZnS'], 2.0e-25)
   and close(ksp['PbS'], 3.2e-28) and close(ksp['CuS'], 7.9e-37)
   and close(ksp['HgS'], 2.0e-53), 'K_sp: CaS 8×10⁻⁶; ZnS 2,0×10⁻²⁵; PbS 3,2×10⁻²⁸; CuS 7,9×10⁻³⁷; HgS 2×10⁻⁵³')
io = M.iodometric()
ck(close(io['n_h2s'], 0.005, 1e-9) and close(io['m_i2'], 1.2690, 1e-4)
   and close(io['m_thio'], 2.4818, 1e-4),
   'yodometriya: n = 0,00500 mol;  I₂ 1,2690 g;  tiosulfat 2,4818 g')
nn = M.neutralisation()
ck(close(nn['m_h2s'], 100.0) and close(nn['naoh_nash'], 117.4, 0.05)
   and close(nn['naoh_na2s'], 234.7, 0.05) and close(nn['caoh2'], 217.4, 0.05),
   'neytralizatsiya: NaOH 117,4 / 234,7 kg;  Ca(OH)₂ 217,4 kg')
ck(close(nn['eq_mass'], 17.041, 1e-3), 'ekvivalent massa: 17,041 g/eq')
cl = M.claus()
ck(close(cl['m_s'], 940.7, 0.05) and close(cl['m_h2o'], 528.6, 0.05)
   and close(cl['m_o2'], 469.4, 0.05), 'Claus: S 940,7 kg;  H₂O 528,6 kg;  O₂ 469,4 kg')
ck(close(cl['balance'], 0.15, 0.01), 'Claus mass balansi: kirish − chiqish 0,15 kg')
ck(close(M.air_load(20.0)['mg'], 28.0, 0.1) and close(M.air_load(100.0)['mg'], 140.0, 0.1),
   'havo yuklamasi: 20 ppm → 28 mg/m³;  100 ppm → 140 mg/m³')

print('3) CSV fayllar va rasmlar')
for name, n in [('kislotalik', 57), ('fizik', 21), ('eritma', 12), ('metall', 11),
                ('sulfidlar', 4), ('yodometriya', 5), ('neytralizatsiya', 5),
                ('ekvivalent', 4), ('xavfsizlik', 8), ('sanoat', 6)]:
    rows = list(csv.DictReader((ASSETS / (name + '.csv')).open()))
    ck(len(rows) == n, '%s.csv: %d qator' % (name, len(rows)))
pngs = sorted(p.stem for p in ASSETS.glob('*.png'))
ck(len(pngs) == 17, 'rasmlar soni: %d' % len(pngs))
for n in ['kislotalik', 'fizik', 'eritma', 'metall', 'ekvivalent',
          'fizikx', 'eritmax', 'metallx', 'redoksx', 'tuzlarx', 'tahlilx', 'xavfsizlikx',
          'molekulax', 'hosilax', 'idishx', 'tabiiy', 'clausx']:
    ck(n in pngs, 'rasm %s.png bor' % n)

print('4) Matn: taxminiy hisob raqamlari va atamalar')
ms = MS.read_text()
tables_txt = json.dumps(json.loads((ROOT / 'matn' / '07_01_jadvallar.json').read_text()), ensure_ascii=False)
notes_txt = json.dumps(json.loads((ROOT / 'matn' / '07_01_yonlavhalar.json').read_text()), ensure_ascii=False)
ms_all = ms + tables_txt + notes_txt
need = ['34,081', '212,87', '190,85', '187,66', '89,63', '373,3', '10,2',
        '−20,6', '205,81', '−37,28', '34,25', '92,11', '1,3356', '0,97', '347',
        '10,46', '705', '19,5', '232', '4–44',
        '3,98', '5,3', '1,22', '0,1168', '3,99', '17 800', '23,68', '20,80', '13,8',
        '7,04', '11,96', '9,1×10⁻⁸', '30,4', '69,6', '0,0021', '98,7', '8,3×10⁻³',
        '1,09×10⁻¹⁸', '1,09×10⁻⁶', '2,93×10⁻¹⁰', '2,93×10⁻²²',
        '0,00500', '1,2690', '2,4818', '117,4', '234,7', '217,4', '17,041', '58,680',
        '940,7', '528,6', '469,4', '0,15', '−518', '−1165,6', '95–97', '97–98', '0,8–1,5',
        '0,14 V', '−0,407 V', '8×10⁻⁶', '2,0×10⁻²⁵', '3,2×10⁻²⁸', '7,9×10⁻³⁷', '2×10⁻⁵³',
        '82,1', '26,7', '90–100', '85,8', 'IDLH 100', '20 ppm', '10 ppm', '1,40 mg/m³',
        '0,51', '1,539', '1,39', '1 ppm']
for x in need:
    ck(x in ms_all, 'matnda «%s» bor' % x)
ck(ms.count('[[EQ:') == 11 and ms.count('[[TABLE:') == 11, 'matnda 11 formula va 11 jadval belgisi')
ck(len(re.findall(r'^## ', ms, flags=re.M)) == 11, 'matnda 11 bo‘lim')
ck('amaliyot tavsiyalari berilmaydi' in ms, 'xavfsizlik chegarasi matnda bayon qilindi')
ck('o‘lchov ma’lumoti emas' in ms, 'taxminiy hisob cheklovi matnda ko‘rsatilgan')
ck('taxminiy hisob' in ms.lower(), 'terminologiya: «taxminiy hisob» ishlatilgan')
ck('model' not in ms_all.lower(), 'terminologiya: «model» yo‘q')
ck('vodorod bog‘i' in ms and 'sulfid ioni' in ms and 'Claus' in ms,
   'mavzu kalit tushunchalari matnda')
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
ck(xml.count('<m:oMath') >= 56, 'OMML satrlari (11 guruh): %d' % xml.count('<m:oMath'))
ck(xml.count('<m:f>') >= 1, 'kasrlar: %d' % xml.count('<m:f>'))
ck(xml.count('<m:sSub>') >= 25, 'pastki indekslar: %d' % xml.count('<m:sSub>'))
ck(xml.count('sSup') >= 1, 'yuqori indekslar: %d' % xml.count('sSup'))
ck(text_all.count('-jadval.') == 11, 'jadval sarlavhalari: %d' % text_all.count('-jadval.'))
ck(text_all.count('-sxema.') == 7, 'sxema sarlavhalari: %d' % text_all.count('-sxema.'))
ck(text_all.count('-grafik.') == 5, 'grafik sarlavhalari: %d' % text_all.count('-grafik.'))
ck(text_all.count('-rasm.') == 5, 'rasm sarlavhalari: %d' % text_all.count('-rasm.'))
for i in range(1, 12):
    ck(text_all.count('(7.1.%d)' % i) == 1, 'formula raqami (7.1.%d)' % i)
ck('_' not in text_all, 'matnda "_" qolmadi (pastki indeksga o‘girilgan)')
ck('Times New Roman' in xml, 'Times New Roman shrifti qo‘llangan')
ck('Cambria Math' in xml, 'formulalar Cambria Math shriftida')
ck(text_all.count('HISOBIY GRAFIK') == 5, 'grafik yorliqlari: %d' % text_all.count('HISOBIY GRAFIK'))
ck(text_all.count('TUSHUNTIRUVCHI SXEMA') == 2, 'sxema yorliqlari: %d' % text_all.count('TUSHUNTIRUVCHI SXEMA'))
ck(text_all.count('CHIZMA VA IZOH') == 4, 'chizma yorliqlari: %d' % text_all.count('CHIZMA VA IZOH'))
ck('NOORGANIK KISLOTALAR' in doc.sections[0].header.paragraphs[0].text, 'sarlavha matni')
ck('7-BOB' in doc.sections[0].footer.paragraphs[0].text, 'kolontitul matni')
for x in ['34,081', '92,11', '17 800', '0,00500', '940,7', 'IDLH', '17,041']:
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
print('BARCHA TEKSHIRUVLAR O‘TDI (7.1).')
