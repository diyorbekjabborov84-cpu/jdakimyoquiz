#!/usr/bin/env python3
"""5.2 moduli uchun QA: model hisoblarining matn va hujjat bilan mosligi."""
from pathlib import Path
import csv, math, re, json
from docx import Document
import prep_05_02 as M

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'chiqish' / 'Noorganik-kislotalar-5.2-Kislotalarni-tozalash.docx'
ASSETS = ROOT / 'rasmlar' / 'tozalash'
MS = ROOT / 'matn' / '05_02.md'
fails = []


def ck(cond, msg):
    if cond:
        print('  OK  ', msg)
    else:
        print('  FAIL', msg); fails.append(msg)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print('1) Model: Ksp, eruvchanlik va kompleks')
ck(close(M.metal_solubility(2.0, M.KSP['Fe(OH)3'], 3), 4.0e-2, 1e-6), 'Fe³⁺ pH 2 da 4,0×10⁻² M')
ck(close(M.metal_solubility(3.0, M.KSP['Fe(OH)3'], 3), 4.0e-5, 1e-9), 'Fe³⁺ pH 3 da 4,0×10⁻⁵ M')
ck(close(M.metal_solubility(5.0, M.KSP['Cu(OH)2'], 2), 2.2e-2, 1e-5), 'Cu²⁺ pH 5 da 2,2×10⁻² M')
ck(close(M.metal_solubility(7.0, M.KSP['Cu(OH)2'], 2), 2.2e-6, 1e-9), 'Cu²⁺ pH 7 da 2,2×10⁻⁶ M')
ck(close(M.metal_solubility(8.0, M.KSP['Cd(OH)2'], 2), 5.9e-3, 1e-5), 'Cd²⁺ pH 8 da 5,9×10⁻³ M')
ck(close(M.cu_with_ammonia(2.0), 1.294117647e-9, 1e-12), 'Cu²⁺ + 4NH₃ (1,0 M), pH 2 → 1,29×10⁻⁹ M')
ck(close(M.KSP['CuS'], 8.5e-45, 1e-47) and close(M.KSP['HgS'], 1.6e-54, 1e-56)
   and close(M.KSP['PbS'], 7e-29, 1e-31), 'sulfidlar Ksp: CuS 8,5×10⁻⁴⁵; HgS 1,6×10⁻⁵⁴; PbS 7×10⁻²⁹')

print('2) Model: kaskad, Fenske, R_min, McCabe-Thiele')
for phi, n in [(10.0, 6.0), (100.0, 3.0), (1000.0, 2.0), (10000.0, 1.5)]:
    ck(close(M.stages_for(phi, 1e-6), n, 1e-9), 'Φ = %g → %g bosqich (10⁻⁶ gacha)' % (phi, n))
for a, n in [(1.2, 32.30), (1.5, 14.52), (2.0, 8.50), (3.0, 5.36)]:
    ck(close(M.fenske(a), n, 5e-3), 'Fenske α = %.1f → %.2f pog‘ona' % (a, n))
ck(close(M.r_min(2.0), 1.70, 5e-3), 'R_min(α = 2,0) = 1,70')
ck(close(M.r_min(3.0), 0.80, 5e-3), 'R_min(α = 3,0) = 0,80')
ck(close(M.r_min(1.5), 3.50, 5e-3), 'R_min(α = 1,5) = 3,50')
m2 = M.mccabe_thiele(2.0)
ck(m2['feasible'] and m2['N'] == 16, 'McCabe-Thiele α = 2,0 → 16 pog‘ona')
m3 = M.mccabe_thiele(3.0)
ck(m3['feasible'] and m3['N'] == 7, 'McCabe-Thiele α = 3,0 → 7 pog‘ona')
m15 = M.mccabe_thiele(1.5)
ck((not m15['feasible']) and close(m15['r_min'], 3.50, 1e-6) and m15['N'] is None,
   'McCabe-Thiele α = 1,5: R_min = 3,50 > R = 2,0 — dizayn mumkin emas')

print('3) Model: suv olib tashlash, ion almashinuv, tozalash zanjiri')
for w0, m in [(0.50, 48.98), (0.68, 30.61), (0.75, 23.47)]:
    ck(close(M.water_removal(w0, 0.98)['m_water_out'], m, 5e-3),
       '100 kg da %s → 0,98: %.2f kg suv' % (w0, m))
for c0, bv, q in [(50.0, 4.965, 48.08), (100.0, 1.2801, 49.02), (200.0, 0.3385, 49.51)]:
    ck(close(M.breakthrough_bv(c0), bv, 5e-3), 'fronti kiring BV (C₀ = %g mg/L) = %.3f' % (c0, bv))
    r = M.thomas(c0); ck(close(r['q_eq'], q, 5e-2), 'C₀ = %g mg/L: q_eq = %.2f mg/g' % (c0, r['q_eq']))
r50 = M.thomas(50.0)
ck(close(r50['area'], 48.0769, 5e-3), 'massa balansi: yig‘ilgan miqdor 48,08 mg/g')
a = M.no2_to_hno3(1000.0, 0.68, 4.0)
for k, v, tol in [('n_no2', 86.9376, 1e-3), ('m_h2o_used', 0.7831, 1e-4), ('m_o2', 0.6955, 1e-4),
                  ('m_hno3_new', 5.4779, 1e-4), ('m_final', 999.9124, 1e-3), ('w_final', 0.68554, 1e-5)]:
    ck(close(a[k], v, tol), 'NO₂ modeli: %s = %.4f' % (k, a[k]))
b = M.fe_precipitation(1000.0, 0.0003)
for k, v, tol in [('n_fe', 5.3715, 1e-3), ('m_feoh3', 0.5741, 1e-4), ('m_caso4', 1.0969, 1e-4),
                  ('m_cao', 0.4519, 1e-4), ('m_caco3', 0.8065, 1e-4), ('m_h2so4_lost', 0.7903, 1e-4),
                  ('m_final', 998.926, 1e-2), ('E_factor', 0.00167, 1e-5)]:
    ck(close(b[k], v, tol), 'Fe modeli: %s = %.4f' % (k, b[k]))

print('4) Model: CSV fayllar')
for name in ['kaskad', 'choqish', 'rektifikatsiya', 'buglash', 'ionalmashinuv', 'mcbabgele']:
    rows = list(csv.DictReader((ASSETS / (name + '.csv')).open()))
    ck(len(rows) > 20, '%s.csv: %d qator' % (name, len(rows)))

print('5) Matn: model raqamlari matnda bor')
ms = MS.read_text()
tables_txt = json.dumps(json.loads((ROOT / 'matn' / '05_02_jadvallar.json').read_text()), ensure_ascii=False)
notes_txt = json.dumps(json.loads((ROOT / 'matn' / '05_02_yonlavhalar.json').read_text()), ensure_ascii=False)
ms_all = ms + tables_txt + notes_txt
need = ['4,0×10⁻²', '2,2×10⁻⁶', '5,9×10⁻³', '1,29×10⁻⁹', '1,7×10¹³', '8,5×10⁻⁴⁵',
        '1,6×10⁻⁵⁴', '7×10⁻²⁹', '1,0×10⁻²⁸', '4×10⁻³⁸', '2,2×10⁻²⁰', '5,9×10⁻¹⁵',
        '68,8 %', '120,5 °C', '20,2 %', '108,6 °C', '98,3 %', '337 °C',
        '32,3', '14,52', '8,5', '5,4', '16 pog‘ona', '7 pog‘ona', 'R_min = 3,50',
        '48,98 kg', '30,61 kg', '23,47 kg', '4,96 bed hajmida', '1,28', '0,34', '48,08 mg/g',
        '86,938', '0,7831', '0,6955', '5,4779', '68,55 %', '5,3715', '0,5741', '1,0969',
        '0,4519', '0,7903', '0,00167', '0,8065', '0,079 %',
        '68,0–70,0 %', '0,5 ppm', '10 ppm', '2 ppm', '0,01 %', 'Y6', 'ASTM D1209',
        'Karl Fischer', 'Ph. Eur.', '15315', 'I03171', 'S05566']
for s in need:
    ck(s in ms_all, 'matnda «%s» bor' % s)
ck(ms.count('[[EQ:') == 11 and ms.count('[[TABLE:') == 11, 'matnda 11 formula va 11 jadval belgisi')
ck('tavsiyalari berilmaydi' in ms, 'xavfsizlik chegarasi matnda bayon qilindi')
ck('tajriba ma’lumoti emas' in ms, 'model cheklovi matnda ko‘rsatilgan')

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
ck(xml.count('<m:oMath') == 40, 'OMML satrlari (11 guruh, 40 qator): %d' % xml.count('<m:oMath'))
ck(xml.count('<m:f>') >= 22, 'kasrlar: %d' % xml.count('<m:f>'))
ck(xml.count('<m:sSub>') >= 12, 'pastki indekslar: %d' % xml.count('<m:sSub>'))
ck(xml.count('<m:sSup>') >= 12, 'yuqori indekslar: %d' % xml.count('<m:sSup>'))
ck(text_all.count('-jadval.') == 11, 'jadval sarlavhalari: %d' % text_all.count('-jadval.'))
ck(text_all.count('-sxema.') == 7, 'sxema sarlavhalari: %d' % text_all.count('-sxema.'))
ck(text_all.count('-grafik.') == 5, 'grafik sarlavhalari: %d' % text_all.count('-grafik.'))
ck(text_all.count('-rasm.') == 5, 'rasm sarlavhalari: %d' % text_all.count('-rasm.'))
for i in range(1, 12):
    ck(text_all.count('(5.2.%d)' % i) == 1, 'formula raqami (5.2.%d)' % i)
ck('_' not in text_all, 'matnda "_" qolmadi (pastki indeksga o‘girilgan)')
ck('Times New Roman' in xml, 'Times New Roman shrifti qo‘llangan')
ck('Cambria Math' in xml, 'formulalar Cambria Math shriftida')
ck(text_all.count('HISOBIY GRAFIK') == 4, 'grafik yorliqlari: %d' % text_all.count('HISOBIY GRAFIK'))
ck(text_all.count('TUSHUNTIRUVCHI SXEMA') == 4, 'sxema yorliqlari: %d' % text_all.count('TUSHUNTIRUVCHI SXEMA'))
ck(text_all.count('CHIZMA VA IZOH') == 3, 'chizma yorliqlari: %d' % text_all.count('CHIZMA VA IZOH'))
hdr = doc.sections[0].header.paragraphs[0].text
ftr = doc.sections[0].footer.paragraphs[0].text
ck('NOORGANIK KISLOTALAR' in hdr, 'sarlavha matni')
ck('5-BOB' in ftr and '5.2' in text_all, 'kolontitul matni')
for s in ['4,0×10−2', '1,29×10−9', '68,8 %', '5,4779', '0,00167', '0,7903', '68,55 %']:
    ck(s in text_all, 'DOCX matnida «%s» bor' % s)
ck('OpenStax' in text_all and 'Gold Book' in text_all and 'European Pharmacopoeia' in text_all,
   'adabiyotlar ro‘yxati joylashdi')
ck('amaliyot tavsiyalari berilmaydi' in text_all, 'xavfsizlik chegarasi bayon qilindi')
ck('0,5 ppm' in text_all, 'Ph. Eur. chegaralari hujjatda')
ck('48,08 mg/g' in text_all, 'ion almashinuv massa balansi hujjatda')
size = DOCX.stat().st_size
ck(size > 400000, 'DOCX hajmi: %d bayt' % size)

print()
if fails:
    print('XATO: %d tekshiruv bajarilmadi' % len(fails))
    for f in fails: print('  -', f)
    raise SystemExit(1)
print('BARCHA TEKSHIRUVLAR O‘TDI (5.2).')
