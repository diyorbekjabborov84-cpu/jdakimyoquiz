#!/usr/bin/env python3
"""6.6 moduli uchun QA: taxminiy hisoblarning matn va hujjat bilan mosligi."""
from pathlib import Path
import csv, math, re, json
from docx import Document
import prep_06_06 as M

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'chiqish' / 'Noorganik-kislotalar-6.6-Taqqoslash.docx'
ASSETS = ROOT / 'rasmlar' / 'taqqoslash'
MS = ROOT / 'matn' / '06_06.md'
fails = []


def ck(cond, msg):
    if cond:
        print('  OK  ', msg)
    else:
        print('  FAIL', msg); fails.append(msg)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print('1) Taxminiy hisob: kislotalik va pH')
for key, pka, ka in [('HF', 3.17, 6.8e-4), ('HCl', -5.9, 1.3e6),
                     ('HBr', -8.8, 6.3e8), ('HI', -9.5, 3.2e9)]:
    a = M.BY_KEY[key]
    ck(close(a['pka'], pka) and close(a['ka'], ka),
       '%s: pK_a %s; K_a %s' % (key, pka, ka))
for key, dmso in [('HF', 15.0), ('HCl', -2.0), ('HBr', -6.8), ('HI', -10.9)]:
    ck(close(M.BY_KEY[key]['pka_dmso'], dmso), '%s: pK_a (DMSO) %s' % (key, dmso))
p = M.ph_at('HF', 0.010)
ck(close(p['h'], 0.002290, 1e-5) and close(p['pct'], 22.90, 0.01)
   and close(p['ph'], 2.640, 1e-3), 'HF 0,010 M: h 0,002290 M; α 22,90 %; pH 2,640')
p = M.ph_at('HF', 0.100)
ck(close(p['h'], 0.007913, 1e-5) and close(p['pct'], 7.91, 0.01)
   and close(p['ph'], 2.102, 1e-3), 'HF 0,100 M: h 0,007913 M; α 7,91 %; pH 2,102')
p = M.ph_at('HF', 1.000)
ck(close(p['h'], 0.025739, 1e-5) and close(p['pct'], 2.57, 0.01)
   and close(p['ph'], 1.589, 1e-3), 'HF 1,000 M: h 0,025739 M; α 2,57 %; pH 1,589')
for key in ['HCl', 'HBr', 'HI']:
    p = M.ph_at(key, 0.100)
    ck(close(p['ph'], 1.000, 1e-6) and close(p['pct'], 100.0),
       '%s 0,100 M: pH 1,000; α 100 %%' % key)

print('2) Taxminiy hisob: metall, halogen, neytralizatsiya, ekvivalent')
md = {x['key']: x for x in M.metal_demand(1.0)}
ck(close(md['HF']['m_acid'], 0.716, 1e-3) and close(md['HCl']['m_acid'], 1.306, 1e-3)
   and close(md['HBr']['m_acid'], 2.898, 1e-3) and close(md['HI']['m_acid'], 4.581, 1e-3),
   '1 g Fe uchun kislota: HF 0,716; HCl 1,306; HBr 2,898; HI 4,581 g')
ck(close(md['HF']['m_salt'], 1.680, 1e-3) and close(md['HCl']['m_salt'], 2.270, 1e-3)
   and close(md['HBr']['m_salt'], 3.861, 1e-3) and close(md['HI']['m_salt'], 5.545, 1e-3),
   '1 g Fe uchun tuz: FeF₂ 1,680; FeCl₂ 2,270; FeBr₂ 3,861; FeI₂ 5,545 g')
ck(all(close(x['m_h2'], 0.036, 1e-3) for x in md.values()),
   '1 g Fe dan H₂ 0,036 g — barcha kislotalarda bir xil')
hg = {x['key']: x for x in M.halogen_from_acid(1000.0)}
ck(close(hg['HF']['m_x2'], 0.0) and not hg['HF']['possible'],
   'HF dan F₂ olish mumkin emas')
ck(close(hg['HCl']['m_x2'], 972.4, 0.5) and close(hg['HBr']['m_x2'], 987.5, 0.5)
   and close(hg['HI']['m_x2'], 992.1, 0.5),
   '1000 kg kislotadan Cl₂ 972,4; Br₂ 987,5; I₂ 992,1 kg')
nn = {x['key']: x for x in M.neutralisation_demand(1000.0, 10.0)}
ck(close(nn['HF']['m_naco3'], 264.9, 0.1) and close(nn['HCl']['m_naco3'], 145.3, 0.1)
   and close(nn['HBr']['m_naco3'], 65.5, 0.1) and close(nn['HI']['m_naco3'], 41.4, 0.1),
   'neytralizatsiya: Na₂CO₃ 264,9; 145,3; 65,5; 41,4 kg')
ck(all(close(x['m_input'], x['m_output'], 0.2) for x in nn.values()),
   'neytralizatsiya mass balansi: kirish = chiqish')
ck(close(nn['HF']['m_ca_salt'], 195.1, 0.1) and nn['HF']['precipitate'],
   'HF da CaF₂ cho‘kma: 195,1 kg')
eq = {x['key']: x for x in M.acid_equivalents(1000.0)}
ck(close(eq['HF']['eq_per_kg'], 49.985, 1e-3) and close(eq['HCl']['eq_per_kg'], 27.427, 1e-3)
   and close(eq['HBr']['eq_per_kg'], 12.359, 1e-3) and close(eq['HI']['eq_per_kg'], 7.818, 1e-3),
   '1 kg kislotada H⁺ ekvivalenti: 49,985; 27,427; 12,359; 7,818 mol')
sp = {x['name']: x for x in M.salt_rows()}
ck(close(sp['AgCl']['ksp'], 1.8e-10) and close(sp['AgBr']['ksp'], 5.4e-13)
   and close(sp['AgI']['ksp'], 8.3e-17), 'AgCl/AgBr/AgI Ksp: 1,8×10⁻¹⁰; 5,4×10⁻¹³; 8,3×10⁻¹⁷')
ck(close(sp['CaF₂']['ksp'], 3.9e-11) and close(sp['BaF₂']['ksp'], 1.7e-6)
   and close(sp['PbF₂']['ksp'], 3.7e-8), 'CaF₂ 3,9×10⁻¹¹; BaF₂ 1,7×10⁻⁶; PbF₂ 3,7×10⁻⁸')
ck(sp['AgF']['ksp'] is None, 'AgF uchun Ksp keltirilmagan (faqat eruvchanlik)')
tr = {x['key']: x for x in M.thermal_rows()}
ck(close(tr['HF']['dg_dec'], 550.8, 0.1) and close(tr['HCl']['dg_dec'], 190.6, 0.1)
   and close(tr['HBr']['dg_dec'], 110.0, 0.1) and close(tr['HI']['dg_dec'], 15.9, 0.1),
   'termik dekompozitsiya ΔG°: +550,8; +190,6; +110,0; +15,9 kJ/mol')
ck(close(tr['HF']['e'], 2.87) and close(tr['HI']['e'], 0.54),
   'E°(X₂/2X⁻): F 2,87 V; HI 0,54 V')

print('3) CSV fayllar va rasmlar')
for name, n in [('kislotalik', 4), ('fizik', 4), ('eruvchanlik', 10), ('ph', 28),
                ('metal', 4), ('galogen', 4), ('neytralizatsiya', 4), ('ekvivalent', 4),
                ('termik', 4)]:
    rows = list(csv.DictReader((ASSETS / (name + '.csv')).open()))
    ck(len(rows) == n, '%s.csv: %d qator' % (name, len(rows)))
pngs = sorted(p.stem for p in ASSETS.glob('*.png'))
ck(len(pngs) == 17, 'rasmlar soni: %d' % len(pngs))
for n in ['molekulax', 'kislotalik', 'fizik', 'eritma', 'metall', 'redoksx', 'tuzlarx',
          'organiksx', 'tahlilx', 'xavfsizlikx', 'hisob', 'teskarilanishx', 'fizikx',
          'eritmax', 'metallx', 'idishx', 'ekvivalent']:
    ck(n in pngs, 'rasm %s.png bor' % n)

print('4) Matn: taxminiy hisob raqamlari va atamalar')
ms = MS.read_text()
tables_txt = json.dumps(json.loads((ROOT / 'matn' / '06_06_jadvallar.json').read_text()), ensure_ascii=False)
notes_txt = json.dumps(json.loads((ROOT / 'matn' / '06_06_yonlavhalar.json').read_text()), ensure_ascii=False)
ms_all = ms + tables_txt + notes_txt
need = ['0,917', '1,2746', '1,414', '1,609', '569', '432', '370', '295',
        '3,98', '3,16', '2,96', '2,66', '20,006', '36,461', '80,912', '127,912',
        '1555', '1395', '1349', '1313', '1530', '1377', '1328', '1297',
        '19,5', '−85,1', '−66,8', '−35,4', '−83,6', '−114,2', '−86,9', '−50,8',
        '37,0', '20,2', '47,6', '56,9', '21,27', '6,11', '8,77', '7,56',
        '2,640', '2,102', '1,589', '22,90', '7,91', '2,57',
        '0,716', '1,306', '2,898', '4,581', '1,680', '2,270', '3,861', '5,545', '0,036',
        '972,4', '987,5', '992,1', '62,5', '2,87', '1,36', '1,07', '0,54',
        '264,9', '145,3', '65,5', '41,4', '195,1',
        '49,985', '27,427', '12,359', '7,818',
        '1,8×10⁻¹⁰', '5,4×10⁻¹³', '8,3×10⁻¹⁷', '3,9×10⁻¹¹', '1,7×10⁻⁶', '3,7×10⁻⁸',
        '1,8 kg/L', 'IDLH 30 ppm', '50 ppm', '35 ppm', '116 mg/m³', '183 mg/m³',
        '1 / 150 / 740 ppm', '1,5 mg/L', '4,0 mg/L', 'ICSC 1326',
        'CaF₂', 'H₂SiF₆', 'Cativa', 'Markerovnikov', 'Na₂CO₃', 'AgI']
for x in need:
    ck(x in ms_all, 'matnda «%s» bor' % x)
ck(ms.count('[[EQ:') == 11 and ms.count('[[TABLE:') == 11, 'matnda 11 formula va 11 jadval belgisi')
ck('amaliyot tavsiyalari berilmaydi' in ms, 'xavfsizlik chegarasi matnda bayon qilindi')
ck('o‘lchov ma’lumoti emas' in ms, 'taxminiy hisob cheklovi matnda ko‘rsatilgan')
ck('CaF₂↓' in ms and 'H₂SiF₆' in ms and 'AgX↓' in ms, 'asosiy tengliklar matnda')
ck('model' not in ms.lower(), 'terminologiya: «model» yo‘q')
ck('vodorod bog‘i' in ms and 'passivatsiya' in ms and 'embrittlement' in ms,
   'mavzu kalit tushunchalari matnda')
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
ck(xml.count('<m:oMath') >= 55, 'OMML satrlari (11 guruh): %d' % xml.count('<m:oMath'))
ck(xml.count('<m:f>') >= 1, 'kasrlar: %d' % xml.count('<m:f>'))
ck(xml.count('<m:sSub>') >= 25, 'pastki indekslar: %d' % xml.count('<m:sSub>'))
ck(xml.count('sSup') >= 1, 'yuqori indekslar: %d' % xml.count('sSup'))
ck(text_all.count('-jadval.') == 11, 'jadval sarlavhalari: %d' % text_all.count('-jadval.'))
ck(text_all.count('-sxema.') == 7, 'sxema sarlavhalari: %d' % text_all.count('-sxema.'))
ck(text_all.count('-grafik.') == 5, 'grafik sarlavhalari: %d' % text_all.count('-grafik.'))
ck(text_all.count('-rasm.') == 5, 'rasm sarlavhalari: %d' % text_all.count('-rasm.'))
for i in range(1, 12):
    ck(text_all.count('(6.6.%d)' % i) == 1, 'formula raqami (6.6.%d)' % i)
ck('_' not in text_all, 'matnda "_" qolmadi (pastki indeksga o‘girilgan)')
ck('Times New Roman' in xml, 'Times New Roman shrifti qo‘llangan')
ck('Cambria Math' in xml, 'formulalar Cambria Math shriftida')
ck(text_all.count('HISOBIY GRAFIK') == 4, 'grafik yorliqlari: %d' % text_all.count('HISOBIY GRAFIK'))
ck(text_all.count('TUSHUNTIRUVCHI SXEMA') == 4, 'sxema yorliqlari: %d' % text_all.count('TUSHUNTIRUVCHI SXEMA'))
ck(text_all.count('CHIZMA VA IZOH') == 3, 'chizma yorliqlari: %d' % text_all.count('CHIZMA VA IZOH'))
ck('NOORGANIK KISLOTALAR' in doc.sections[0].header.paragraphs[0].text, 'sarlavha matni')
ck('6-BOB' in doc.sections[0].footer.paragraphs[0].text, 'kolontitul matni')
for x in ['1555', '4,581 g', '49,985', '264,9 kg', '992,1 kg', '2,102', 'IDLH']:
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
print('BARCHA TEKSHIRUVLAR O‘TDI (6.6).')
