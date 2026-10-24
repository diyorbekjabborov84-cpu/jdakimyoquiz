#!/usr/bin/env python3
"""6.5 moduli uchun QA: model hisoblarining matn va hujjat bilan mosligi."""
from pathlib import Path
import csv, math, re, json
from docx import Document
import prep_06_05 as M

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'chiqish' / 'Noorganik-kislotalar-6.5-HI-yodid-kislota.docx'
ASSETS = ROOT / 'rasmlar' / 'hi'
MS = ROOT / 'matn' / '06_05.md'
fails = []


def ck(cond, msg):
    if cond:
        print('  OK  ', msg)
    else:
        print('  FAIL', msg); fails.append(msg)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print('1) Model: spetsiatsiya va triiodid')
s = M.speciation_series()
ck(close(s[0]['ph'], 1.000, 1e-3) and close(s[0]['w_i'], 100.0, 0.001),
   '0,100 M: I⁻ 100,000 %; pH 1,000')
ck(close(s[6]['ph'], -0.879, 1e-3) and close(s[6]['w_i'], 100.0, 0.001),
   '7,560 M: I⁻ 100,000 %; pH −0,879')
ck(close(s[9]['ph'], -1.079, 1e-3) and close(s[9]['w_hi2'], 0.00002, 1e-5),
   '12,000 M: pH −1,079; HI₂⁻ 0,00002 %')
ck(close(M.KA_HI / 1e9, 3.1623, 1e-3) and close(M.K_HI2, 10 ** 0.7, 1e-6),
   'Ka = 3,2×10⁹; lgK(HI₂⁻) = 0,7')
tb = M.triiodide_series()
ck(close(tb[0]['w_i3'], 98.54, 0.05), '0,10 M I⁻: I₃⁻ ulushi 98,54 %')
ck(close(tb[6]['w_i3'], 99.98, 0.01), '7,56 M I⁻: I₃⁻ ulushi 99,98 %')
ck(close(tb[8]['w_i3'], 99.99, 0.01), '12,0 M I⁻: I₃⁻ ulushi 99,99 %')

print('2) Model: ishlab chiqarish, redoks, metallar, chiqindi')
ds = M.direct_synthesis(1000.0)
ck(close(ds['m_h2'], 7.88, 0.01) and close(ds['m_i2'], 992.1, 0.5)
   and close(ds['dh_kj'], -9.44, 0.01) and close(ds['k_eq'], 0.254, 1e-3),
   'sintetik: H₂ 7,88 kg; I₂ 992,1 kg; ΔrH −9,44 kJ; K(298 K) = 0,254')
hz = M.hydrazine_method(1000.0)
ck(close(hz['m_i2'], 992.1, 0.5) and close(hz['m_n2h4'], 62.6, 0.1),
   'gidrazin: I₂ 992,1 kg; N₂H₄ 62,6 kg')
ph = M.phosphorus_method(1000.0)
ck(close(ph['m_p'], 80.7, 0.1) and close(ph['m_h2o'], 140.8, 0.1)
   and close(ph['m_h3po3'], 213.7, 0.1),
   'fosfor: P 80,7 kg; H₂O 140,8 kg; H₃PO₃ 213,7 kg')
hs = M.h2s_method(1000.0)
ck(close(hs['m_h2s'], 133.2, 0.1) and close(hs['m_s'], 125.3, 0.1),
   'H₂S usuli: H₂S 133,2 kg; S 125,3 kg')
ii = M.iodine_from_iodide(1000.0)
ck(close(ii['m_cl2'], 236.5, 0.1) and close(ii['m_i2'], 846.6, 0.1)
   and close(ii['m_nacl'], 389.9, 0.1), 'yod sikli: Cl₂ 236,5; I₂ 846,6; NaCl 389,9 kg')
ck(close(ii['m_input'], ii['m_output'], 0.2), 'yod sikli mass balansi: 1236,5 = 1236,5 kg')
o2 = M.oxidation_by_oxygen(1000.0)
ck(close(o2['m_o2'], 62.5, 0.1) and close(o2['m_i2'], 992.1, 0.5),
   'O₂ bilan: O₂ 62,5 kg; I₂ 992,1 kg')
hn = M.oxidation_by_nitric(1000.0)
ck(close(hn['m_hno3'], 164.2, 0.1) and close(hn['m_i2'], 992.1, 0.5),
   'HNO₃ bilan: HNO₃ 164,2 kg; I₂ 992,1 kg')
md = {x['metal']: x for x in M.metal_dissolution(1.0)}
ck(close(md['Fe']['m_salt'], 5.545, 1e-3) and close(md['Fe']['m_hi'], 4.581, 1e-3)
   and close(md['Fe']['m_h2'], 0.036, 1e-3), '1 g Fe → 5,545 g FeI₂; HI 4,581 g; H₂ 0,036 g')
ck(close(md['Al']['m_salt'], 15.110, 1e-3) and close(md['Al']['m_hi'], 14.222, 1e-3),
   '1 g Al → 15,110 g AlI₃; HI 14,222 g')
ck(close(md['Zn']['m_hi'], 3.913, 1e-3) and close(md['Mg']['m_hi'], 10.526, 1e-3),
   '1 g Zn → HI 3,913 g; 1 g Mg → HI 10,526 g')
ck(close(md['Cu']['m_hi'], 4.026, 1e-3) and close(md['Cu']['m_o2'], 0.252, 1e-3),
   '1 g Cu → HI 4,026 g + O₂ 0,252 g')
n1 = M.neutralisation(1000.0, 10.0, 'Na2CO3')
ck(close(n1['m_agent'], 41.4, 0.1) and close(n1['m_salt'], 117.2, 0.1)
   and close(n1['m_gas'], 17.2, 0.1) and close(n1['m_h2o'], 7.0, 0.1),
   'neytralizatsiya: Na₂CO₃ 41,4; NaI 117,2; CO₂ 17,2; H₂O 7,0 kg')
ck(close(n1['m_input'], n1['m_output'], 0.1), 'neytralizatsiya mass balansi: 141,4 = 141,4 kg')
n2 = M.neutralisation(1000.0, 10.0, 'Ca(OH)2')
ck(close(n2['m_agent'], 29.0, 0.1) and close(n2['m_salt'], 114.9, 0.1)
   and close(n2['m_h2o'], 14.1, 0.1) and close(n2['m_input'], n2['m_output'], 0.1),
   'Ca(OH)₂ bilan: 29,0 / 114,9 / 14,1 kg; kirish = chiqish 129,0 kg')
t = M.titration_standardisation(0.2000, 30.00)
ck(close(t['c_hi'], 0.12580, 1e-5), 'standartlash: 0,2000 g Na₂CO₃; 30,00 mL → 0,12580 mol/L')
io = M.iodometry_sample(1.0)
ck(close(io['m_i2'], 0.712, 1e-3) and close(io['m_thio'], 0.887, 1e-3),
   'yodometriya: 1,000 g KIO₃ → I₂ 0,712 g; tiosulfat 0,887 g')
iz = M.iodized_salt(1000.0, 30.0)
ck(close(iz['m_ki'], 39.2, 0.1) and close(iz['m_kio3'], 50.6, 0.1),
   'yodlangan tuz: 1 t + 30 g I → KI 39,2 g; KIO₃ 50,6 g')
ck(close(M.PHYS['tb'], -35.36) and close(M.PHYS['tm'], -50.80) and close(M.PHYS['tc'], 151.0)
   and close(M.PHYS['pc'], 8.31) and close(M.PHYS['aze_pct'], 56.7)
   and close(M.PHYS['aze_tb'], 126.7) and close(M.PHYS['aze_c'], 7.56)
   and close(M.PHYS['sol20'], 42.0) and close(M.PHYS['sol10'], 234.0)
   and close(M.PHYS['rho_liq'], 2.85) and close(M.PHYS['rho_g25'], 5.229)
   and close(M.PHYS['vp_atm'], 7.81) and close(M.PHYS['d_air'], 4.4),
   'fizik konstantalar: −35,36 / −50,80 °C; 151 °C; 8,31 MPa; azeotrop 56,7 % / 126,7 °C')
g = {x[0]: x for x in M.GROUP}
ck(close(g['HI'][1], 295.0) and close(g['HI'][2], -9.5) and close(g['HI'][3], -10.9)
   and close(g['HI'][4], 56.7) and close(g['HF'][1], 569.0),
   'guruh: D 569/432/366/295; pK_a (suv) va DMSO to‘g‘ri')

print('3) CSV fayllar va rasmlar')
for name, n in [('fizik_hi', 24), ('eritma', 4), ('spetsiatsiya', 10), ('guruh', 4),
                ('ishlabchiqarish', 20), ('metallar', 5), ('chiqindi', 20), ('triiodid', 9)]:
    rows = list(csv.DictReader((ASSETS / (name + '.csv')).open()))
    ck(len(rows) == n, '%s.csv: %d qator' % (name, len(rows)))
pngs = sorted(p.stem for p in ASSETS.glob('*.png'))
ck(len(pngs) == 17, 'rasmlar soni: %d' % len(pngs))
for n in ['molekulax', 'fizikx', 'guruh', 'olishsx', 'triiodidsx', 'metalsx',
          'redoks', 'organiksx', 'qollanishsx', 'tahlilsx', 'hisob',
          'ishlabchiqarish', 'metallar', 'teshikx', 'yodradio', 'idishx', 'chiqindi']:
    ck(n in pngs, 'rasm %s.png bor' % n)

print('4) Matn: model raqamlari va atamalar')
ms = MS.read_text()
tables_txt = json.dumps(json.loads((ROOT / 'matn' / '06_05_jadvallar.json').read_text()), ensure_ascii=False)
notes_txt = json.dumps(json.loads((ROOT / 'matn' / '06_05_yonlavhalar.json').read_text()), ensure_ascii=False)
ms_all = ms + tables_txt + notes_txt
need = ['1,609', '295 kJ/mol', '0,45', '2,66', '10,39', '−35,36', '−50,80',
        '151', '8,31', '5,23 g/L', '4,4', '7,81', '2,85', '42 g/100 mL', '234',
        '56,7', '126,7', '7,56', '48–57', '+26,5', '+1,7', '206,6', '29,2',
        '−9,5', '−10,9', '3,2×10⁹', '1,000', '−0,879', '−1,079', '0,00002',
        '98,54', '99,98', '7,88', '992,1', '−9,44', '0,254', '62,6', '80,7', '140,8',
        '213,7', '133,2', '125,3', '236,5', '846,6', '389,9', '1236,5', '62,5', '164,2',
        '5,545', '4,581', '0,036', '15,110', '14,222', '0,112', '4,882', '3,913',
        '11,443', '10,526', '4,026', '0,252', '41,4', '117,2', '17,2', '141,4',
        '29,0', '114,9', '14,1', '129,0', '0,2000', '30,00', '0,12580', '0,712', '0,887',
        '39,2', '50,6', '569', '432', '3,17', 'Ksp ≈ 8×10⁻¹⁷',
        '30 000 t/y', '23 000', '9 000', '54 %', '43 %',
        'ICSC 1326', 'IDLH 35 ppm', '183 mg/m³', '740 ppm', '150 ppm', '0,01 ppm',
        '0,1 ppm', '2 ppm', '30 ppm', 'DEA', 'Cativa', 'I-131', 'I-129',
        'AgI', '[HgI₄]²⁻', 'Al₂I₆', 'I₃⁻']
for x in need:
    ck(x in ms_all, 'matnda «%s» bor' % x)
ck(ms.count('[[EQ:') == 11 and ms.count('[[TABLE:') == 11, 'matnda 11 formula va 11 jadval belgisi')
ck('amaliyot tavsiyalari berilmaydi' in ms, 'xavfsizlik chegarasi matnda bayon qilindi')
ck('o‘lchov ma’lumoti emas' in ms, 'model cheklovi matnda ko‘rsatilgan')
ck('H₂ + I₂' in ms and 'N₂H₄' in ms and '2NaI + Cl₂' in ms, 'asosiy tengliklar matnda')
ck('4HI + O₂' in ms and 'HNO₃' in ms and 'IO₃⁻' in ms, 'redoks tengliklari matnda')
ck('vodorod bog‘i' in ms and 'passivatsiya' in ms and 'embrittlement' in ms,
   'mavzu kalit tushunchalari matnda')
ck('hydrogen bog‘i' not in ms.lower(), 'terminologiya: vodorod bog‘i')
ck('$' not in ms, 'matnda dollar belgisi yo‘q')
ck(not re.search(r'[Ѐ-ӿ]', ms), 'matnda kirill harflari yo‘q')

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
ck(xml.count('<m:oMath') == 66, 'OMML satrlari (11 guruh, 66 qator): %d' % xml.count('<m:oMath'))
ck(xml.count('<m:f>') >= 1, 'kasrlar: %d' % xml.count('<m:f>'))
ck(xml.count('<m:sSub>') >= 30, 'pastki indekslar: %d' % xml.count('<m:sSub>'))
ck(xml.count('sSup') >= 1, 'yuqori indekslar: %d' % xml.count('sSup'))
ck(text_all.count('-jadval.') == 11, 'jadval sarlavhalari: %d' % text_all.count('-jadval.'))
ck(text_all.count('-sxema.') == 7, 'sxema sarlavhalari: %d' % text_all.count('-sxema.'))
ck(text_all.count('-grafik.') == 5, 'grafik sarlavhalari: %d' % text_all.count('-grafik.'))
ck(text_all.count('-rasm.') == 5, 'rasm sarlavhalari: %d' % text_all.count('-rasm.'))
for i in range(1, 12):
    ck(text_all.count('(6.5.%d)' % i) == 1, 'formula raqami (6.5.%d)' % i)
ck('_' not in text_all, 'matnda "_" qolmadi (pastki indeksga o‘girilgan)')
ck('Times New Roman' in xml, 'Times New Roman shrifti qo‘llangan')
ck('Cambria Math' in xml, 'formulalar Cambria Math shriftida')
ck(text_all.count('HISOBIY GRAFIK') == 2, 'grafik yorliqlari: %d' % text_all.count('HISOBIY GRAFIK'))
ck(text_all.count('TUSHUNTIRUVCHI SXEMA') == 7, 'sxema yorliqlari: %d' % text_all.count('TUSHUNTIRUVCHI SXEMA'))
ck(text_all.count('CHIZMA VA IZOH') == 2, 'chizma yorliqlari: %d' % text_all.count('CHIZMA VA IZOH'))
ck('NOORGANIK KISLOTALAR' in doc.sections[0].header.paragraphs[0].text, 'sarlavha matni')
ck('6-BOB' in doc.sections[0].footer.paragraphs[0].text, 'kolontitul matni')
for x in ['992,1 kg', '4,581 g', '0,12580 mol/L', '846,6 kg', '99,98',
          '3,2×10', '141,4 kg', 'IDLH']:
    ck(x in text_all, 'DOCX matnida «%s» bor' % x)
ck('OSHA' in text_all and 'NIOSH' in text_all and 'EPA' in text_all,
   'adabiyotlar ro‘yxati joylashdi')
ck('amaliyot tavsiyalari berilmaydi' in text_all, 'xavfsizlik chegarasi bayon qilindi')
size = DOCX.stat().st_size
ck(size > 400000, 'DOCX hajmi: %d bayt' % size)

print()
if fails:
    print('XATO: %d tekshiruv bajarilmadi' % len(fails))
    for f in fails: print('  -', f)
    raise SystemExit(1)
print('BARCHA TEKSHIRUVLAR O‘TDI (6.5).')
