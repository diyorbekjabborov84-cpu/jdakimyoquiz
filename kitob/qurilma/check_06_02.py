#!/usr/bin/env python3
"""6.2 moduli uchun QA: model hisoblarining matn va hujjat bilan mosligi."""
from pathlib import Path
import csv, math, re, json
from docx import Document
import prep_06_02 as M

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'chiqish' / 'Noorganik-kislotalar-6.2-HF-florid-kislota.docx'
ASSETS = ROOT / 'rasmlar' / 'hf'
MS = ROOT / 'matn' / '06_02.md'
fails = []


def ck(cond, msg):
    if cond:
        print('  OK  ', msg)
    else:
        print('  FAIL', msg); fails.append(msg)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print('1) Model: spetsiatsiya')
s = M.speciation_series()
ck(close(s[0]['ph'], 2.635, 1e-3) and close(s[0]['w_hf'], 76.0, 0.1)
   and close(s[0]['w_f'], 22.3, 0.1) and close(s[0]['w_hf2'], 0.8, 0.1),
   '0,010 M: HF 76,0 %; F⁻ 22,3 %; HF₂⁻ 0,8 %; pH 2,635')
ck(close(s[2]['w_hf'], 87.9, 0.1) and close(s[2]['w_f'], 6.4, 0.1) and close(s[2]['w_hf2'], 2.8, 0.1),
   '0,100 M: HF 87,9 %; F⁻ 6,4 %; HF₂⁻ 2,8 %')
ck(close(s[4]['w_hf'], 89.5, 0.1) and close(s[4]['w_f'], 1.1, 0.1) and close(s[4]['w_hf2'], 4.7, 0.1)
   and close(s[4]['ph'], 1.238, 1e-3), '1,000 M: HF 89,5 %; F⁻ 1,1 %; HF₂⁻ 4,7 %; pH 1,238')
ck(close(s[7]['w_hf2'], 5.2, 0.1) and close(s[7]['ph'], 0.277, 1e-3), '10,000 M: HF₂⁻ 5,2 %; pH 0,277')
ck(close(M.KA_HF, 6.8e-4) and close(M.KF, 10 ** 0.7, 1e-6), 'Ka = 6,8×10⁻⁴; lgK(HF₂⁻) = 0,7')

print('2) Model: yemirish, passivatsiya, chiqindi, kaltsiy, olish')
e = M.etch_rate(1.0); ck(close(e['r'], 687.8, 0.5), '1,000 M da tezlik: 687,8 Å/min')
e4 = M.etch_rate(4.0); ck(close(e4['r'], 2778.7, 1.0), '4,000 M da tezlik: 2778,7 Å/min')
e8 = M.etch_rate(8.0); ck(close(e8['r'], 5567.7, 1.0), '8,000 M da tezlik: 5567,7 Å/min')
ck(close(e['r_hf2'] / e['r'] * 100, 20.0, 1.0), 'HF₂⁻ ulushi 1,000 M da ~20 %')
p = {x['metal']: x for x in M.passivation(1.0)}
ck(close(p['Al']['ratio'], 3.113, 1e-3) and close(p['Al']['m_hf'], 1.483, 1e-3), '1 g Al → 3,113 g AlF₃; HF 1,483 g')
ck(close(p['Fe']['ratio'], 2.326, 1e-3), '1 g Fe → 2,326 g FeF₃')
ck(close(p['Ni']['ratio'], 1.647, 1e-3), '1 g Ni → 1,647 g NiF₂')
ck(close(p['Cu']['ratio'], 1.598, 1e-3), '1 g Cu → 1,598 g CuF₂')
w = M.waste_model(1000.0, 10.0)
ck(close(w['m_caoh2'], 185.2, 0.2) and close(w['m_caf2'], 195.1, 0.2) and close(w['m_h2o'], 90.0, 0.2),
   'chiqindi: Ca(OH)₂ 185,2 kg; CaF₂ 195,1 kg; H₂O 90,0 kg')
ck(close(w['m_input'], w['m_output'], 0.3), 'neytralizatsiya mass balansi: kirish = chiqish 285,2 kg')
r1 = M.residual_fluoride(0.001); r2 = M.residual_fluoride(0.010); r3 = M.residual_fluoride(0.100)
ck(close(r1['f_mg'], 3.752, 1e-3) and close(r2['f_mg'], 1.186, 1e-3) and close(r3['f_mg'], 0.375, 1e-3),
   'qoldiq F⁻: 3,752 / 1,186 / 0,375 mg/L')
c = M.calcium_requirement(20.0)
ck(close(c['n_ca'], 0.500, 1e-3) and close(c['m_ca'], 20.03, 1e-2) and close(c['m_caglu'], 224.1, 0.2),
   '20 g HF → 0,500 mol Ca²⁺ → 20,03 g Ca → 224,1 g kalsiy glyukonat')
c2 = M.calcium_requirement(100.0)
ck(close(c2['n_ca'], 2.499, 1e-3) and close(c2['m_caglu'], 1120.6, 0.5), '100 g HF → 2,499 mol Ca²⁺ → 1120,6 g')
pr = M.production_model(1000.0, 0.97, 0.92)
ck(close(pr['m_hf'], 457.3, 0.5) and close(pr['m_h2so4'], 1218.5, 0.5) and close(pr['m_caso4'], 1691.4, 0.5),
   '1000 kg fluorit: HF 457,3 kg; H₂SO₄ 1218,5 kg; CaSO₄ 1691,4 kg')
g = M.glass_model(1.0, 48.0)
ck(close(g['m_hf'], 1997.8, 0.5) and close(g['m_solution'], 4162.1, 0.5) and close(g['m_h2siof6'], 2398.2, 0.5),
   '1 kg SiO₂: HF 1997,8 g (48 % da 4162,1 g); H₂SiF₆ 2398,2 g')
ck(close(M.AHF['k_self_273'], 2.0e-12) and close(M.AHF['eps_273'], 84.0) and close(M.AHF['h0'], -15.1),
   'anhidr HF: K_self 2×10⁻¹²; ε = 84; H₀ = −15,1')

print('3) CSV fayllar va rasmlar')
for name, n in [('spetsiatsiya', 8), ('yemirish', 8), ('passivatsiya', 4),
                ('chiqindi', 11), ('kalsiy', 6), ('fizik_hf', 13)]:
    rows = list(csv.DictReader((ASSETS / (name + '.csv')).open()))
    ck(len(rows) == n, '%s.csv: %d qator' % (name, len(rows)))
pngs = sorted(p.stem for p in ASSETS.glob('*.png'))
ck(len(pngs) == 17, 'rasmlar soni: %d' % len(pngs))

print('4) Matn: model raqamlari va atamalar')
ms = MS.read_text()
tables_txt = json.dumps(json.loads((ROOT / 'matn' / '06_02_jadvallar.json').read_text()), ensure_ascii=False)
notes_txt = json.dumps(json.loads((ROOT / 'matn' / '06_02_yonlavhalar.json').read_text()), ensure_ascii=False)
ms_all = ms + tables_txt + notes_txt
need = ['0,917', '569', '3,98', '19,5', '−83,6', '190–292,5', '84', '175', '2×10⁻¹²',
        'H₂F⁺', 'HF₂⁻', '−15,1', '−21', '−28', 'SbF₅', '6,8×10⁻⁴', '0,7',
        '76,0', '22,3', '0,8', '87,9', '6,4', '2,8', '89,5', '1,1', '4,7', '5,2',
        '2,635', '2,033', '1,238', '0,277', '457,3', '1218,5', '1691,4',
        '1997,8', '4162,1', '2398,2', '599,6', '510', '610', '2890', '65,1', '340,3',
        '687,8', '2778,7', '5567,7', '3,113', '2,326', '1,647', '1,598',
        '1,483', '0,716', '0,682', '0,630', '185,2', '195,1', '90,0', '285,2',
        '3,752', '1,186', '0,375', '1,5 mg/L', '4,0 mg/L', '2,0 mg/L',
        '224,1', '1120,6', '0,500', '2,499', '20,03', '100,16',
        '3 ppm', '0,5 ppm', '2 ppm', '30 ppm', 'kalsiy glyukonat', 'gipokalsemiya',
        'WHO', 'AQSh', 'Na₃AlF₆', 'H₂SiF₆', 'kriyolit']
for s in need:
    ck(s in ms_all, 'matnda «%s» bor' % s)
ck(ms.count('[[EQ:') == 11 and ms.count('[[TABLE:') == 11, 'matnda 11 formula va 11 jadval belgisi')
ck('amaliyot tavsiyalari berilmaydi' in ms, 'xavfsizlik chegarasi matnda bayon qilindi')
ck('o‘lchov ma’lumotlari emas' in ms, 'model cheklovi matnda ko‘rsatilgan')
ck('CaF₂ + H₂SO₄' in ms and 'SiO₂ + 6HF' in ms, 'asosiy tengliklar matnda')
ck('hydrogen bog‘i' in ms and 'passivatsiya' in ms, 'mavzu kalit tushunchalari matnda')

print('5) DOCX tuzilmasi')
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
ck(xml.count('<m:f>') >= 1, 'kasrlar: %d' % xml.count('<m:f>'))
ck(xml.count('<m:sSub>') >= 30, 'pastki indekslar: %d' % xml.count('<m:sSub>'))
ck(xml.count('sSup') >= 1, 'yuqori indekslar: %d' % xml.count('sSup'))
ck(text_all.count('-jadval.') == 11, 'jadval sarlavhalari: %d' % text_all.count('-jadval.'))
ck(text_all.count('-sxema.') == 7, 'sxema sarlavhalari: %d' % text_all.count('-sxema.'))
ck(text_all.count('-grafik.') == 5, 'grafik sarlavhalari: %d' % text_all.count('-grafik.'))
ck(text_all.count('-rasm.') == 5, 'rasm sarlavhalari: %d' % text_all.count('-rasm.'))
for i in range(1, 12):
    ck(text_all.count('(6.2.%d)' % i) == 1, 'formula raqami (6.2.%d)' % i)
ck('_' not in text_all, 'matnda "_" qolmadi (pastki indeksga o‘girilgan)')
ck('Times New Roman' in xml, 'Times New Roman shrifti qo‘llangan')
ck('Cambria Math' in xml, 'formulalar Cambria Math shriftida')
ck(text_all.count('HISOBIY GRAFIK') == 1, 'grafik yorliqlari: %d' % text_all.count('HISOBIY GRAFIK'))
ck(text_all.count('TUSHUNTIRUVCHI SXEMA') == 7, 'sxema yorliqlari: %d' % text_all.count('TUSHUNTIRUVCHI SXEMA'))
ck(text_all.count('CHIZMA VA IZOH') == 3, 'chizma yorliqlari: %d' % text_all.count('CHIZMA VA IZOH'))
ck('NOORGANIK KISLOTALAR' in doc.sections[0].header.paragraphs[0].text, 'sarlavha matni')
ck('6-BOB' in doc.sections[0].footer.paragraphs[0].text, 'kolontitul matni')
for s in ['0,002290' if False else '1997,8 g', '185,2 kg', '224,1 g', '687,8 Å/min',
          '3,113 g', '−15,1', '2×10', '457,3 kg']:
    ck(s in text_all, 'DOCX matnida «%s» bor' % s)
ck('Housecroft' in text_all and 'WHO' in text_all and 'Ph. Eur.' in text_all,
   'adabiyotlar ro‘yxati joylashdi')
ck('amaliyot tavsiyalari berilmaydi' in text_all, 'xavfsizlik chegarasi bayon qilindi')
size = DOCX.stat().st_size
ck(size > 400000, 'DOCX hajmi: %d bayt' % size)

print()
if fails:
    print('XATO: %d tekshiruv bajarilmadi' % len(fails))
    for f in fails: print('  -', f)
    raise SystemExit(1)
print('BARCHA TEKSHIRUVLAR O‘TDI (6.2).')
