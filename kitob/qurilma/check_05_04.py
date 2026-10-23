#!/usr/bin/env python3
"""5.4 moduli uchun QA: model hisoblarining matn va hujjat bilan mosligi."""
from pathlib import Path
import csv, math, re, json
from docx import Document
import prep_05_04 as M

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'chiqish' / 'Noorganik-kislotalar-5.4-Sanoat-prinsiplari.docx'
ASSETS = ROOT / 'rasmlar' / 'sanoat'
MS = ROOT / 'matn' / '05_04.md'
fails = []


def ck(cond, msg):
    if cond:
        print('  OK  ', msg)
    else:
        print('  FAIL', msg); fails.append(msg)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print('1) Model: zanjir mass balansi')
c = M.chain_balance()
ck(close(c['m_hno3'], 680.0, 1e-9), 'HNO₃: 680,00 kg')
ck(close(c['n_hno3'], 10.7919, 5e-4), 'n(HNO₃) = 10,7919 kmol')
ck(close(c['m_nh3'], 183.80, 5e-3), 'NH₃: 183,80 kg')
ck(close(c['m_o2'], 690.68, 5e-3), 'O₂: 690,68 kg')
ck(close(c['m_n2'], 2596.97, 5e-2), 'N₂: 2596,97 kg')
ck(close(c['m_water_formed'], 194.42, 5e-3), 'hosil bo‘lgan suv: 194,42 kg')
ck(close(c['m_water_bound'], 97.21, 5e-3), 'bog‘langan suv: 97,21 kg')
ck(close(c['m_water_external'], 222.79, 5e-3), 'tashqaridan suv: 222,79 kg')
ck(close(c['m_water_in'], 417.21, 5e-3), 'kiruvchi suv: 417,21 kg')
ck(close(c['m_final'], 693.88, 5e-3), 'mahsulot: 693,88 kg')
ck(close(c['m_water_final'], 13.88, 5e-3), 'qolgan suv: 13,88 kg')
ck(close(c['m_water_removed'], 306.12, 5e-3), 'chiqarilgan suv: 306,12 kg')
ck(close(c['m_toluene'], 1239.95, 5e-2), 'toluen: 1239,95 kg')
ck(close(c['m_distillate'], 1546.07, 5e-2), 'distillat: 1546,07 kg')
ck(close(c['m_no'], 323.87, 5e-2), 'NO: 323,87 kg')
ck(close(c['m_no2'], 496.54, 5e-2), 'NO₂: 496,54 kg')
ck(close(c['m_hno3'] + c['m_w0'], 1000.0, 1e-6), 'kirish: HNO₃ + suv = 1000,00 kg')
ck(close(c['m_final'] + c['m_water_removed'], 1000.0, 1e-6), 'chiqish: mahsulot + chiqarilgan suv = 1000,00 kg')

print('2) Model: energiya')
ck(close(M.DH_OVERALL, -414.03, 1e-9), 'ΔH = −414,03 kJ/mol')
ck(close(M.oxidation_heat(c['n_hno3']), -4.4682, 1e-3), 'reaksion issig‘i: −4,47 GJ (= −4468,2 MJ)')
d = M.drying_heat(c['m_water_removed'], c['m_toluene'])
ck(close(d['Q_water'], 690.9, 0.1), 'suv bug‘latish: 690,9 MJ')
ck(close(d['Q_toluene'], 512.2, 0.1), 'toluen bug‘latish: 512,2 MJ')
ck(close(d['Q_total'], 1203.1, 0.1), 'jami: 1203,1 MJ')
ck(len(M.STEAM) == 7 and close(M.STEAM[2][1], 179.89, 1e-9) and close(M.STEAM[6][1], 295.06, 1e-9),
   'bug‘ jadvali: 1,00 MPa → 179,89 °C; 8,00 MPa → 295,06 °C')
ck(close(M.STEAM[0][2], 2257.5, 1e-9) and close(M.STEAM[6][2], 1441.0, 1e-9),
   'bug‘latish entalpiyasi: 2257,5 → 1441,0 kJ/kg')

print('3) Model: iqtisodiyot va OEE')
e = M.economics()
ck(close(e['capex'], 120000000.0, 1e-6), 'CAPEX: 120,0 mln USD')
ck(close(e['foa'], 9600000.0, 1e-6), 'FOA: 9,60 mln USD/y')
ck(close(e['foa_per_t'], 96.0, 1e-9), 'birlik FOA: 96 USD/t')
ck(close(e['c_var'], 324.0, 1e-9) and close(e['c_total'], 420.0, 1e-9), 'birlik narx: 324 + 96 = 420 USD/t')
ck(close(e['oee'], 0.8653, 5e-5), 'OEE = 0,8653')
ck(close(e['eff_output'], 86526.0, 1.0), 'savdo hajmi: 86 526 t/y')
ck(close(e['margin'], 140.0, 1e-9), 'marja: 140 USD/t')
ck(close(e['ebitda'], 12113640.0, 1.0), 'yillik foyda: 12,11 mln USD')
ck(close(e['payback'], 9.9062, 1e-3), 'qaytish muddati: 9,9 yil')
ck(close(M.unit_cost(50000), 516.0, 1e-6) and close(M.unit_cost(100000), 420.0, 1e-6)
   and close(M.unit_cost(200000), 372.0, 1e-6), 'birlik FOA: 50k→516; 100k→420; 200k→372')
ck(close(M.oee(0.92, 0.95, 0.99), 0.8653, 5e-5), 'OEE formulasi (ISO 22400-2)')

print('4) Model: CSV fayllar')
for name, n in [('oqim', 10), ('bug', 7), ('opex', 7), ('birlik_qiymat', 8), ('issiqlik', 16)]:
    rows = list(csv.DictReader((ASSETS / (name + '.csv')).open()))
    ck(len(rows) == n, '%s.csv: %d qator' % (name, len(rows)))
opex_sum = sum(float(r['ulush_%']) for r in csv.DictReader((ASSETS / 'opex.csv').open()))
ck(close(opex_sum, 100.0, 1e-9), 'OPEX ulushlari yig‘indisi: 100 %')

print('5) Matn: model raqamlari matnda bor')
ms = MS.read_text()
tables_txt = json.dumps(json.loads((ROOT / 'matn' / '05_04_jadvallar.json').read_text()), ensure_ascii=False)
notes_txt = json.dumps(json.loads((ROOT / 'matn' / '05_04_yonlavhalar.json').read_text()), ensure_ascii=False)
ms_all = ms + tables_txt + notes_txt
need = ['680,00 kg', '10,7919 kmol', '183,80 kg', '690,68 kg', '2596,97 kg',
        '194,42 kg', '97,21 kg', '222,79 kg', '417,21 kg', '320,00 kg',
        '306,12 kg', '693,88 kg', '13,88 kg', '1546,07 kg', '1239,95 kg',
        '323,87 kg', '496,54 kg', '−414,03 kJ/mol', '4468,2 MJ', '690,9 MJ', '512,2 MJ', '1203,1 MJ',
        '99,63', '151,83', '179,89', '212,42', '250,40', '295,06', '2257,5', '1441,0',
        '0,92', '0,95', '0,99', '0,8653', '86 526', '120,0 mln', '9,60 mln', '96 USD/t',
        '324 USD/t', '420 USD/t', '516', '372', '140 USD/t', '9,9 yil', '0,012', '1,39',
        'ISO 22400', 'ISO 9001', 'ISO 14001', 'ISO 45001', 'Ph. Eur.', 'Ramshaw', 'exergy',
        'eksergiya', 'Ostwald', 'SCR', '2.2.32', '5.11']
for s in need:
    ck(s in ms_all, 'matnda «%s» bor' % s)
ck(ms.count('[[EQ:') == 11 and ms.count('[[TABLE:') == 11, 'matnda 11 formula va 11 jadval belgisi')
ck('tavsiyalari berilmaydi' in ms, 'xavfsizlik chegarasi matnda bayon qilindi')
ck('o‘lchov ma’lumoti emas' in ms, 'model cheklovi matnda ko‘rsatilgan')

print('6) DOCX tuzilmasi')
doc = Document(DOCX)
xml = doc.element.xml
text_all = '\n'.join(p.text for p in doc.paragraphs)
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                text_all += '\n' + p.text
ck(len(doc.inline_shapes) == 17, 'rasmlar soni: %d' % len(doc.inline_shapes))
ck(xml.count('<m:oMath') == 46, 'OMML satrlari (11 guruh, 46 qator): %d' % xml.count('<m:oMath'))
ck(xml.count('<m:f>') >= 8, 'kasrlar: %d' % xml.count('<m:f>'))
ck(xml.count('<m:sSub>') >= 20, 'pastki indekslar: %d' % xml.count('<m:sSub>'))
ck(xml.count('sSup') >= 2, 'yuqori indekslar: %d' % xml.count('<m:sSup>'))
ck(text_all.count('-jadval.') == 11, 'jadval sarlavhalari: %d' % text_all.count('-jadval.'))
ck(text_all.count('-sxema.') == 7, 'sxema sarlavhalari: %d' % text_all.count('-sxema.'))
ck(text_all.count('-grafik.') == 5, 'grafik sarlavhalari: %d' % text_all.count('-grafik.'))
ck(text_all.count('-rasm.') == 5, 'rasm sarlavhalari: %d' % text_all.count('-rasm.'))
for i in range(1, 12):
    ck(text_all.count('(5.4.%d)' % i) == 1, 'formula raqami (5.4.%d)' % i)
ck('_' not in text_all, 'matnda "_" qolmadi (pastki indeksga o‘girilgan)')
ck('Times New Roman' in xml, 'Times New Roman shrifti qo‘llangan')
ck('Cambria Math' in xml, 'formulalar Cambria Math shriftida')
ck(text_all.count('HISOBIY GRAFIK') == 3, 'grafik yorliqlari: %d' % text_all.count('HISOBIY GRAFIK'))
ck(text_all.count('TUSHUNTIRUVCHI SXEMA') == 5, 'sxema yorliqlari: %d' % text_all.count('TUSHUNTIRUVCHI SXEMA'))
ck(text_all.count('CHIZMA VA IZOH') == 3, 'chizma yorliqlari: %d' % text_all.count('CHIZMA VA IZOH'))
hdr = doc.sections[0].header.paragraphs[0].text
ftr = doc.sections[0].footer.paragraphs[0].text
ck('NOORGANIK KISLOTALAR' in hdr, 'sarlavha matni')
ck('5-BOB' in ftr and '5.4' in text_all, 'kolontitul matni')
for s in ['10,7919', '183,80', '316', '306,12', '693,88', '414,03', '4468,2', '0,8653', '120,0', '96 USD/t']:
    ck(s in text_all, 'DOCX matnida «%s» bor' % s)
ck('OpenStax' in text_all and 'ISO 22400' in text_all and 'Gold Book' in text_all,
   'adabiyotlar ro‘yxati joylashdi')
ck('amaliyot tavsiyalari berilmaydi' in text_all, 'xavfsizlik chegarasi bayon qilindi')
size = DOCX.stat().st_size
ck(size > 400000, 'DOCX hajmi: %d bayt' % size)

print()
if fails:
    print('XATO: %d tekshiruv bajarilmadi' % len(fails))
    for f in fails: print('  -', f)
    raise SystemExit(1)
print('BARCHA TEKSHIRUVLAR O‘TDI (5.4).')
