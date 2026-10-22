#!/usr/bin/env python3
"""5.3 moduli uchun QA: model hisoblarining matn va hujjat bilan mosligi."""
from pathlib import Path
import csv, math, re, json
from docx import Document
import prep_05_03 as M

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / 'chiqish' / 'Noorganik-kislotalar-5.3-Quritish-va-suvsizlantirish.docx'
ASSETS = ROOT / 'rasmlar' / 'quritish'
MS = ROOT / 'matn' / '05_03.md'
fails = []


def ck(cond, msg):
    if cond:
        print('  OK  ', msg)
    else:
        print('  FAIL', msg); fails.append(msg)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print('1) Model: namlik ko‘rsatkichlari va higroskopiklik')
w = M.water_fraction(0.35, 1.0)
ck(close(w['X_wet'], 0.2593, 5e-5) and close(w['w_dry'], 0.35, 1e-9),
   'namlik asoslari: X = 0,2593; w = 0,350')
ck(close(M.loss_on_drying(10.0, 9.95), 0.50, 1e-6), 'quruq qoldig‘: 0,50 % m/m')
h = M.hygroscopicity(5.0, 15.0, 15.35)
ck(close(h['increase'], 3.50, 1e-6) and h['class'] == 'higroskopik',
   'higroskopiklik: 3,50 % → higroskopik sinf')
for m1, m2, m3, cls in [(5.0, 15.0, 17.3, 'juda higroskopik'),
                        (5.0, 15.0, 15.2, 'biroz higroskopik'),
                        (5.0, 15.0, 15.01, 'higroskopik emas')]:
    r = M.hygroscopicity(m1, m2, m3)
    ck(r['class'] == cls, 'sinf chegarasi: %.2f %% → %s' % (r['increase'], cls))
kf = M.karl_fischer(2.000, 0.50, 22.2)
ck(close(kf['n'], 0.0111, 1e-9) and close(kf['m_water'], 0.19997, 1e-4)
   and close(kf['w_percent'], 9.998, 1e-2), 'Karl Fischer: 0,2000 g suv → 10,00 %')

print('2) Model: bug‘lanish termodinamikasi va vakuum')
ck(close(M.DVAP_H2O_25, 44.01, 1e-9), 'ΔvapH(25 °C) = 44,01 kJ/mol')
ck(close(M.vapour_pressure(298.15, M.DVAP_H2O_25), 2.8578, 5e-3),
   'p_sat(25 °C) = 2,858 kPa')
for P, T in [(101.325, 100.0), (10.0, 43.96), (2.5, 17.80), (1.5, 9.22), (0.1, -28.96)]:
    ck(close(M.boiling_temperature(P) - 273.15, T, 5e-3),
       'P = %g kPa → T = %.2f °C' % (P, T))
for rh, we in [(0.20, 0.03571), (0.50, 0.04545), (0.80, 0.04878), (0.95, 0.04974)]:
    ck(close(M.equilibrium_moisture(rh), we, 5e-6),
       'muvozanat namligi %d %% RH → %.5f kg/kg' % (int(rh * 100), we))

print('3) Model: quritish kinetikasi va quritgichlar')
ck(close(M.drying_curve(0), 0.35, 1e-9) and close(M.drying_curve(10), 0.20, 1e-9),
   'kinetika: X(0) = 0,35; X(10 min) = 0,20 (kritik nuqta)')
ck(M.drying_at_temperature(373.15, 30) < M.drying_at_temperature(333.15, 30),
   'yuqori haroratda tezroq quriladi (Arrhenius modeli)')
p25 = M.p2o5_capacity()
ck(close(p25['capacity'], 38.076, 5e-3), 'P₂O₅ sig‘imi: 38,08 % massa')
ck(close(M.salt_capacity(M.M_CACL2, 0, 6)['capacity'], 0.974, 5e-3),
   'CaCl₂ sig‘imi: 0,974 kg suv/kg')
ck(close(M.salt_capacity(M.M_MGSO4, 0, 7)['capacity'], 1.048, 5e-3),
   'MgSO₄ sig‘imi: 1,048 kg suv/kg')
ck(close(M.sieve_demand(100.0, 20.5), 487.8, 0.1), '4A sital: 100 kg suv uchun 487,8 kg')

print('4) Model: gidrat va azeotrop')
h = M.hydrate_mass('CuSO4', 1000.0, '5H2O', 'H2O')
ck(close(h['kmol'], 4.0051, 1e-3), 'CuSO₄·5H₂O: n = 4,0051 kmol')
ck(close(h['m_water'], 288.60, 1e-2), 'gidrat quritish: suv 288,60 kg')
ck(close(h['m_product'], 711.40, 1e-2), 'gidrat quritish: mahsulot 711,40 kg')
ck(close(h['w_start'], 36.08, 5e-3) and close(h['w_end'], 10.14, 5e-3),
   'suv ulushi: 36,08 % → 10,14 %')
h0 = M.hydrate_mass('CuSO4', 1000.0, '5H2O', '0')
ck(close(h0['m_water'], 360.75, 1e-2) and close(h0['m_product'], 639.25, 1e-2),
   'anhiddirgacha: suv 360,75 kg; mahsulot 639,25 kg')
a = M.azeotropic_drying(1000.0, 0.32, 0.005, 'toluen')
ck(close(a['m_acid'], 680.0, 1e-6), 'azeotrop: kislota 680,0 kg')
ck(close(a['m_water_out'], 316.58, 5e-3), 'azeotrop: chiqarilgan suv 316,58 kg')
ck(close(a['m_distillate'], 1598.90, 5e-2), 'azeotrop: distillat 1598,90 kg')
ck(close(a['m_entrainer'], 1282.32, 5e-2), 'azeotrop: toluen 1282,32 kg')
ck(close(a['m_entrainer_loss'], 0.158, 1e-3), 'azeotrop: toluen yo‘qotish 0,158 kg')

print('5) Model: energetika')
e = M.evaporation_energy(316.58)
ck(close(e['Q_MJ'], 714.5, 1e-1), '316,58 kg suv → 714,5 MJ')
ck(close(M.energy_kwh(1.0), 0.6269, 1e-4), '1 kg suv → 0,6269 kWh')
ck(close(M.evaporation_energy(288.60)['Q_MJ'], 651.3, 1e-1), '288,60 kg suv → 651,3 MJ')

print('6) Model: CSV fayllar')
for name, n in [('vakuum', 55), ('kinetika', 121), ('adsorbsiya', 50), ('azeotrop', 3), ('energiya', 4)]:
    rows = list(csv.DictReader((ASSETS / (name + '.csv')).open()))
    ck(len(rows) == n, '%s.csv: %d qator' % (name, len(rows)))

print('7) Matn: model raqamlari matnda bor')
ms = MS.read_text()
tables_txt = json.dumps(json.loads((ROOT / 'matn' / '05_03_jadvallar.json').read_text()), ensure_ascii=False)
notes_txt = json.dumps(json.loads((ROOT / 'matn' / '05_03_yonlavhalar.json').read_text()), ensure_ascii=False)
ms_all = ms + tables_txt + notes_txt
need = ['0,2593', '0,350', '0,50 %', '3,50 %', '15 %', '2 %', '0,2 %', '80 ± 2 %', '24 soat',
        '44,01', '40,657', '2,858', '43,96', '17,80', '9,22', '−28,96',
        '0,0357', '0,0455', '0,0488', '0,0497',
        '84,1 °C', '19,8 %', '69,5 °C', '8,4 %', '70,9 °C', '12,5 %',
        '0,2469', '0,0917', '0,1429', '316,58 kg', '1598,90 kg', '1282,32 kg', '0,158 kg',
        '38,08 %', '0,974', '1,048', '487,8 kg', '19,5 %', '20,5 %', '21,0 %', '23,5 %',
        '4,0051 kmol', '288,60 kg', '711,40 kg', '36,08 %', '10,14 %', '360,75 kg', '639,25 kg',
        '0,0111 mol', '0,2000 g', '10,00 %', '2,2568 MJ', '0,6269 kWh',
        '651,3 MJ', '180,9 kWh', '1244,2 MJ', '0,50 mg/g', '1,5–2,5 kPa', '0,1 kPa',
        '2.2.32', '2.5.12', '5.11', 'D01582', 'E01909', 'D01618', 'Ph. Eur.', 'USP']
for s in need:
    ck(s in ms_all, 'matnda «%s» bor' % s)
ck(ms.count('[[EQ:') == 11 and ms.count('[[TABLE:') == 11, 'matnda 11 formula va 11 jadval belgisi')
ck('tavsiyalari berilmaydi' in ms, 'xavfsizlik chegarasi matnda bayon qilindi')
ck('tajriba ma’lumoti emas' in ms, 'model cheklovi matnda ko‘rsatilgan')

print('8) DOCX tuzilmasi')
doc = Document(DOCX)
xml = doc.element.xml
text_all = '\n'.join(p.text for p in doc.paragraphs)
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                text_all += '\n' + p.text
ck(len(doc.inline_shapes) == 17, 'rasmlar soni: %d' % len(doc.inline_shapes))
ck(xml.count('<m:oMath') == 43, 'OMML satrlari (11 guruh, 43 qator): %d' % xml.count('<m:oMath'))
ck(xml.count('<m:f>') >= 8, 'kasrlar: %d' % xml.count('<m:f>'))
ck(xml.count('<m:sSub>') >= 12, 'pastki indekslar: %d' % xml.count('<m:sSub>'))
ck(xml.count('<m:sSup>') >= 2, 'yuqori indekslar: %d' % xml.count('<m:sSup>'))
ck(text_all.count('-jadval.') == 11, 'jadval sarlavhalari: %d' % text_all.count('-jadval.'))
ck(text_all.count('-sxema.') == 7, 'sxema sarlavhalari: %d' % text_all.count('-sxema.'))
ck(text_all.count('-grafik.') == 5, 'grafik sarlavhalari: %d' % text_all.count('-grafik.'))
ck(text_all.count('-rasm.') == 5, 'rasm sarlavhalari: %d' % text_all.count('-rasm.'))
for i in range(1, 12):
    ck(text_all.count('(5.3.%d)' % i) == 1, 'formula raqami (5.3.%d)' % i)
ck('_' not in text_all, 'matnda "_" qolmadi (pastki indeksga o‘girilgan)')
ck('Times New Roman' in xml, 'Times New Roman shrifti qo‘llangan')
ck('Cambria Math' in xml, 'formulalar Cambria Math shriftida')
ck(text_all.count('HISOBIY GRAFIK') == 3, 'grafik yorliqlari: %d' % text_all.count('HISOBIY GRAFIK'))
ck(text_all.count('TUSHUNTIRUVCHI SXEMA') == 5, 'sxema yorliqlari: %d' % text_all.count('TUSHUNTIRUVCHI SXEMA'))
ck(text_all.count('CHIZMA VA IZOH') == 3, 'chizma yorliqlari: %d' % text_all.count('CHIZMA VA IZOH'))
hdr = doc.sections[0].header.paragraphs[0].text
ftr = doc.sections[0].footer.paragraphs[0].text
ck('NOORGANIK KISLOTALAR' in hdr, 'sarlavha matni')
ck('5-BOB' in ftr and '5.3' in text_all, 'kolontitul matni')
for s in ['0,2593', '44,01', '316,58', '288,60', '711,40', '2,2568', '38,08']:
    ck(s in text_all, 'DOCX matnida «%s» bor' % s)
ck('OpenStax' in text_all and 'Ph. Eur.' in text_all and 'Gold Book' in text_all,
   'adabiyotlar ro‘yxati joylashdi')
ck('amaliyot tavsiyalari berilmaydi' in text_all, 'xavfsizlik chegarasi bayon qilindi')
size = DOCX.stat().st_size
ck(size > 400000, 'DOCX hajmi: %d bayt' % size)

print()
if fails:
    print('XATO: %d tekshiruv bajarilmadi' % len(fails))
    for f in fails: print('  -', f)
    raise SystemExit(1)
print('BARCHA TEKSHIRUVLAR O‘TDI (5.3).')
