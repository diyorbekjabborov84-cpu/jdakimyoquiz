"""QA: model identities, native mathematics, layout and figure inventory for 4.5."""
from pathlib import Path
from collections import Counter
from zipfile import ZipFile
from lxml import etree
from docx import Document
from docx.shared import Cm
import math, csv, re, json
from decomp_04_05 import (DATA, T0, dH, dS, dG, lgK, lnK, t_star, arrhenius_k,
                          half_life, sulfite_fractions, RX_HNO3, RX_H2SO4, RX_H2O2,
                          A_MODEL, EA_MODEL, KA1, KA2)

D = Path(__file__).resolve().parents[1]
A = D / 'rasmlar' / 'parchalanish'


def near(a, b, tol=1e-9):
    assert math.isclose(a, b, rel_tol=tol, abs_tol=1e-12), (a, b)


def rows(name):
    return [{k: float(v) for k, v in r.items()}
            for r in csv.DictReader((A / (name + '.csv')).open())]


points = 0
for name in ('dG', 'K', 'kinetics', 'sulfite'):
    rr = rows(name)
    assert len(rr) == 401, (name, len(rr))
    points += len(rr)
    for r in rr:
        if name == 'dG':
            near(r['dG_HNO3_kJ'], dG(dH(*RX_HNO3), dS(*RX_HNO3), r['T_K']))
            near(r['dG_H2SO4_kJ'], dG(dH(*RX_H2SO4), dS(*RX_H2SO4), r['T_K']))
        elif name == 'K':
            near(r['lgK_H2SO4'], lgK(dH(*RX_H2SO4), dS(*RX_H2SO4), r['T_K']))
            near(r['K_H2SO4'], 10.0 ** r['lgK_H2SO4'])
        elif name == 'kinetics':
            near(r['k_s-1'], arrhenius_k(r['T_K']))
            near(r['log10_k'], math.log10(arrhenius_k(r['T_K'])))
            near(r['t_half_s'], half_life(r['T_K']))
        else:
            a2, ah, a3 = sulfite_fractions(r['pH'])
            near(r['alpha_SO2aq'], a2); near(r['alpha_HSO3'], ah); near(r['alpha_SO3'], a3)
            near(a2 + ah + a3, 1.0)

# --- Termodinamik identifikatsiyalar ---------------------------------------
dh, ds = dH(*RX_HNO3), dS(*RX_HNO3)
near(dh, -78.53, 1e-4); near(ds, 257.10, 1e-4)
near(dG(dh, ds), -155.1785, 1e-4); near(lgK(dh, ds), 27.1891, 1e-4)
near(t_star(dh, ds), -305.4454, 1e-4)
dh, ds = dH(*RX_H2SO4), dS(*RX_H2SO4)
near(dh, 132.439, 1e-4); near(ds, 169.86, 1e-4)
near(dG(dh, ds), 81.7977, 1e-4); near(lgK(dh, ds), -14.3312, 1e-4)
near(t_star(dh, ds), 779.6583, 1e-4)
dh, ds = dH(*RX_H2O2), dS(*RX_H2O2)
near(dh, -98.05, 1e-4); near(ds, 63.00, 1e-4)
near(dG(dh, ds), -116.8255, 1e-4); near(lgK(dh, ds), 20.4687, 1e-4)

# van 't Hoff nuqtalari (matn va jadvallardagi qiymatlar)
for T, val in ((600, 2.2e-3), (700, 9.8e-2), (900, 15.0), (1000, 90.0), (1200, 1.3e3)):
    k = math.exp(lnK(dH(*RX_H2SO4), dS(*RX_H2SO4), T))
    assert math.isclose(k, val, rel_tol=0.12), (T, k, val)
near(math.exp(lnK(dH(*RX_H2SO4), dS(*RX_H2SO4), 780.0)), 1.0, 1e-2)

# Kinetik model nuqtalari
near(arrhenius_k(298.15), 3.0200e-05, 1e-3); near(half_life(298.15), 2.2956e04, 1e-3)
near(arrhenius_k(320.0), 4.7413e-04, 1e-3); near(half_life(320.0), 1461.4, 1e-3)
near(arrhenius_k(350.0), 1.1886e-02, 1e-3); near(half_life(350.0), 58.30, 1e-3)
near(arrhenius_k(400.0), 8.7301e-01, 1e-3); near(half_life(400.0), 0.7939, 1e-3)
near(A_MODEL, 1.0e13); near(EA_MODEL, 1.0e5)

# Sulfit ulushlari (matn va jadvallardagi qiymatlar)
a2, ah, a3 = sulfite_fractions(1.0)
near(a2, 0.862069, 1e-5); near(ah, 0.137931, 1e-5)
a2, ah, a3 = sulfite_fractions(7.0)
near(a2, 3.810961086276347e-06, 1e-9); near(ah, 0.609754, 1e-5); near(a3, 0.390242, 1e-5)
a2, ah, a3 = sulfite_fractions(12.0)
near(a3, 0.999984, 1e-5)
near(KA1, 1.6e-2); near(KA2, 6.4e-8)

# Kondensatsiya entalpiyalari
near(dH({'H3PO4(s)': 2}, {'H4P2O7(s)': 1, 'H2O(l)': 1}), 31.17, 1e-4)
near(dH({'H4P2O7(s)': 1}, {'HPO3(s)': 2, 'H2O(l)': 1}), 58.17, 1e-4)
near(dH({'H2SO4(l)': 1, 'SO3(g)': 1}, {'H2S2O7(s)': 1}), -63.891, 1e-4)
near(dH({'H2SiO3(s)': 1}, {'SiO2(s)': 1, 'H2O(l)': 1}), -7.86, 1e-4)
near(dH({'H3BO3(s)': 1}, {'HBO2(s)': 1, 'H2O(l)': 1}), 14.25, 1e-4)
near(dH({'H3BO3(s)': 2}, {'B2O3(s)': 1, 'H2O(l)': 3}), 57.67, 1e-4)

# --- Atom va zaryad balanslari ----------------------------------------------
spec = {
    'HNO3': ({'H': 1, 'N': 1, 'O': 3}, 0), 'NO2': ({'N': 1, 'O': 2}, 0),
    'H2O': ({'H': 2, 'O': 1}, 0), 'O2': ({'O': 2}, 0),
    'H2SO4': ({'H': 2, 'S': 1, 'O': 4}, 0), 'SO3': ({'S': 1, 'O': 3}, 0),
    'H2O2': ({'H': 2, 'O': 2}, 0), 'HNO2': ({'H': 1, 'N': 1, 'O': 2}, 0),
    'NO': ({'N': 1, 'O': 1}, 0), 'HClO3': ({'H': 1, 'Cl': 1, 'O': 3}, 0),
    'HClO4': ({'H': 1, 'Cl': 1, 'O': 4}, 0), 'ClO2': ({'Cl': 1, 'O': 2}, 0),
    'HCl': ({'H': 1, 'Cl': 1}, 0), 'H3PO4': ({'H': 3, 'P': 1, 'O': 4}, 0),
    'H4P2O7': ({'H': 4, 'P': 2, 'O': 7}, 0), 'HPO3': ({'H': 1, 'P': 1, 'O': 3}, 0),
    'H2S2O7': ({'H': 2, 'S': 2, 'O': 7}, 0), 'H2SiO3': ({'H': 2, 'Si': 1, 'O': 3}, 0),
    'SiO2': ({'Si': 1, 'O': 2}, 0), 'H3BO3': ({'H': 3, 'B': 1, 'O': 3}, 0),
    'HBO2': ({'H': 1, 'B': 1, 'O': 2}, 0), 'B2O3': ({'B': 2, 'O': 3}, 0),
    'H2S': ({'H': 2, 'S': 1}, 0), 'S': ({'S': 1}, 0),
    'H2SO3': ({'H': 2, 'S': 1, 'O': 3}, 0),
}
rx = [
    ({'HNO3': 4}, {'NO2': 4, 'H2O': 2, 'O2': 1}),
    ({'H2SO4': 1}, {'SO3': 1, 'H2O': 1}),
    ({'H2O2': 2}, {'H2O': 2, 'O2': 1}),
    ({'HNO2': 3}, {'HNO3': 1, 'NO': 2, 'H2O': 1}),
    ({'HClO3': 3}, {'HClO4': 1, 'ClO2': 2, 'H2O': 1}),
    ({'HClO3': 4}, {'HClO4': 3, 'HCl': 1}),
    ({'H2O2': 2}, {'H2O': 2, 'O2': 1}),
    ({'H3PO4': 2}, {'H4P2O7': 1, 'H2O': 1}),
    ({'H4P2O7': 1}, {'HPO3': 2, 'H2O': 1}),
    ({'H2SO4': 1, 'SO3': 1}, {'H2S2O7': 1}),
    ({'H2SiO3': 1}, {'SiO2': 1, 'H2O': 1}),
    ({'H3BO3': 1}, {'HBO2': 1, 'H2O': 1}),
    ({'H3BO3': 2}, {'B2O3': 1, 'H2O': 3}),
    ({'H2S': 2, 'H2SO3': 1}, {'S': 3, 'H2O': 3}),
]


def total(side):
    c = Counter(); charge = 0
    for k, n in side.items():
        a, z = spec[k]; charge += n * z
        for atom, v in a.items():
            c[atom] += n * v
    return c, charge


for left, right in rx:
    assert total(left) == total(right), (left, right)

# --- DOCX tuzilmasi ----------------------------------------------------------
p = D / 'chiqish/Noorganik-kislotalar-4.5-Parchalanish.docx'
doc = Document(p)


def paras(o):
    yield from o.paragraphs
    for t in o.tables:
        for row in t.rows:
            for c in row.cells:
                yield from paras(c)


ps = list(paras(doc)); txt = '\n'.join(x.text for x in ps)
assert len(doc.inline_shapes) == 16
for label, n in [('jadval.', 11), ('grafik.', 4), ('sxema.', 7), ('rasm.', 5)]:
    assert sum(label in x.text for x in ps) == n, (label,)
assert all(txt.count(f'(4.5.{i})') == 1 for i in range(1, 12))
assert '[[EQ:' not in txt and '[[TABLE:' not in txt and '4.4.' not in txt
assert all(r.font.name == 'Times New Roman' for x in ps for r in x.runs if r.text)
outer = [t for t in doc.tables if len(t.columns) == 2]
assert len(outer) == 11
for t in outer:
    assert abs(t.columns[0].width - Cm(13.5)) < 1000 and abs(t.columns[1].width - Cm(4.5)) < 1000
ns = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(p) as z:
    assert z.testzip() is None
    tree = etree.fromstring(z.read('word/document.xml'))
omml = len(tree.xpath('//m:oMath', namespaces=ns))
fracs = len(tree.xpath('//m:f', namespaces=ns))
subs = len(tree.xpath('//m:sSub', namespaces=ns))
sups = len(tree.xpath('//m:sSup', namespaces=ns))
assert len(tree.xpath('//w:tblHeader', namespaces=ns)) == 11
alltext = ' '.join(tree.xpath('//w:t/text()|//m:t/text()', namespaces=ns))
without_urls = re.sub(r'https?://\S+', '', alltext)
assert '_' not in without_urls, [m for m in re.findall(r'\S*_\S*', without_urls)][:8]
assert subs >= 25 and sups >= 8, (subs, sups)
tight = alltext.replace(' ', '')
for key in ['ΔG', 'ΔH', 'ΔS', 'Ka1', 'Ka2', 'Ea', 'Φ']:
    assert key in tight, key
notes = json.loads((D / 'matn/04_05_yonlavhalar.json').read_text())
assert sum(map(len, notes)) == 22 and len(notes) == 11
tables = json.loads((D / 'matn/04_05_jadvallar.json').read_text())
assert len(tables) == 11
print(f'PASS: {points} model nuqtasi; termodinamik, kinetik va sulfit identifikatsiyalari; '
      f'{len(rx)} atom/zarjad balansi; {omml} OMML qator / {fracs} kasr / {subs} pastki / {sups} yuqori; '
      f'11 jadval, 16 rasm, 22 yon lavha, 3:1 tuzilma.')
print('Words with math:', len(alltext.split()), 'Bytes:', p.stat().st_size)
rt = D.parent / 'google_drive/Noorganik kislotalar — 4.5. Parchalanish — tekshirilgan.roundtrip.docx'
if rt.exists():
    with ZipFile(rt) as z:
        gt = etree.fromstring(z.read('word/document.xml'))
    assert len(gt.xpath('//m:oMath', namespaces=ns)) == omml
    assert len(gt.xpath('//m:f', namespaces=ns)) == fracs
    gs = ' '.join(gt.xpath('//w:t/text()|//m:t/text()', namespaces=ns))
    assert gs.count('jadval.') == 11 and all(f'(4.5.{i})' in gs for i in range(1, 12))
    print('Google Docs→DOCX roundtrip PASS: native math lines and fractions retained.')
