#!/usr/bin/env python3
"""A4: 3/4 asosiy matn + 1/4 vizual yon ustun. 7.3 "Sulfat kislota (tuzilishi)" moduli."""
import book_equations
from book_equations import add_equation
book_equations.EQ_SIZE = 18
book_equations.EQ_GAP = 3
book_equations.EQ_LEAD = 0.95
from pathlib import Path
import re, json
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'chiqish' / 'Noorganik-kislotalar-7.3-Sulfat-kislota-tuzilishi.docx'
ASSETS = ROOT / 'rasmlar' / 'sulfat'
NAVY = '0B2C4A'; BRONZE = 'C28E3B'; PALE = 'EDF3F7'; INK = '243746'

panels = [
 (0, 'tabiiyx.png', 'rasm', 'Manbalar va ishlab chiqarish.',
  '7.3.1-rasm. Oltingugurt manbalari va sulfat kislota ishlab chiqarish (sxematik, original).'),
 (1, 'molekulax.png', 'rasm', 'Molekula geometriyasi.',
  '7.3.2-rasm. H₂SO₄ molekulasi: C₂ simmetriya va gauche-gauche konformatsiya (sxematik, original).'),
 (2, 'rezonansx.png', 'sxema', 'Elektron tuzilma.',
  '7.3.3-sxema. S–O bog‘lar, rezonans va gaz fazidagi kislotalik (sxematik).'),
 (3, 'spektr.png', 'grafik', 'Spektroskopiya.',
  '7.3.4-grafik. SO₄²⁻, HSO₄⁻ va H₂SO₄ tebranish bandlari (taxminiy chizma).'),
 (4, 'kislotalik.png', 'grafik', 'Kislotalik va spetsiatsiya.',
  '7.3.5-grafik. HSO₄⁻ / SO₄²⁻ ulushlari pH bo‘yicha va 2-bosqich ulushi (taxminiy egri chiziq).'),
 (5, 'dissotsiatsiya.png', 'grafik', 'Suvdagi dissotsiatsiya.',
  '7.3.6-grafik. pH va sulfat ioni miqdori konsentratsiya bo‘yicha (taxminiy egri chiziq).'),
 (6, 'sufmax.png', 'sxema', 'Sufma kislota va superkislotalik.',
  '7.3.7-sxema. Avtoprotoliz, turlar va proton zaxirasi (sxematik).'),
 (7, 'tuzlarilx.png', 'rasm', 'Sulfat tuzlari.',
  '7.3.8-rasm. Sulfat tuzlari: kristallar va eruvchanlik (sxematik, original).'),
 (8, 'gidratlar.png', 'grafik', 'Gidratlar va fazaviy tarkib.',
  '7.3.9-grafik. Gidratlardagi H₂SO₄ ulushi va suv molekulasi soni (taxminiy egri chiziq).', 3.40),
 (9, 'kristalx.png', 'sxema', 'Kristal tuzilma.',
  '7.3.10-sxema. Monoklin hujra, vodorod bog‘i zanjiri va fazalar (sxematik).', 2.95),
 (10, 'sanoat.png', 'grafik', 'Sanoat va ekvivalent.',
  '7.3.11-grafik. Sarf ulushlari, moddiy balans va ekvivalent (taxminiy hisob).', 3.15)]
# Asosiy panel kengligi (sm) va qo'shimcha rasm kengligi — bo'limlararo vizual
# muvozanat uchun individually sozlanadi (7.9 va 7.11 da qo'shimcha rasm ko'p).
extra = {
 1: [('geometriax.png', '7.3.2-sxema. Geometrik o‘lchovlar va simmetriya (sxematik).')],
 7: [('ionlarx.png', '7.3.8-sxema. Sulfat va gidrosulfat ionlari: tuzilma va rezonans (sxematik).')],
 8: [('gidratx.png', '7.3.9-sxema. Gidrat tarkibi va fazaviy hodisalar.', 2.55)],
 9: [('gidratilx.png', '7.3.10-rasm. Gidrat kristallari: tuzilma va fazaviy tuzilma (sxematik).', 2.20)],
 10: [('xavfsizlikx.png', '7.3.11-sxema. Xavfsizlik chegaralari va favqulodda holat (sxematik).', 2.10),
      ('zavodx.png', '7.3.11-rasm. Kontakt usuli: oltingugurtdan kislotagacha (sxematik).', 2.10)]}

LABEL = {'grafik': 'HISOBIY GRAFIK', 'sxema': 'TUSHUNTIRUVCHI SXEMA', 'rasm': 'CHIZMA VA IZOH'}

doc = Document(); sec = doc.sections[0]
sec.page_width = Cm(21); sec.page_height = Cm(29.7)
sec.left_margin = Cm(1.5); sec.right_margin = Cm(1.5)
sec.top_margin = Cm(1.5); sec.bottom_margin = Cm(1.4)
sec.header_distance = Cm(.65); sec.footer_distance = Cm(.65)
normal = doc.styles['Normal']; normal.font.name = 'Times New Roman'; normal.font.size = Pt(10)
normal.paragraph_format.line_spacing = 1.0
normal.paragraph_format.space_after = Pt(1.5)
normal.paragraph_format.widow_control = True
for sty in doc.styles:
    if sty.type == 1:
        sty.font.name = 'Times New Roman'
        rp = sty.element.get_or_add_rPr(); rf = OxmlElement('w:rFonts')
        for a in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
            rf.set(qn('w:' + a), 'Times New Roman')
        rp.append(rf)
sub = dict(zip('₀₁₂₃₄₅₆₇₈₉ₐᵦₘⱼ', '0123456789abmj'))
sup = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵐⁿ‡', '0123456789+−mn‡'))
TOKEN = re.compile(r'([A-Za-zΑ-Ωα-ωβγδΔ′][A-Za-zΑ-Ωα-ωβγδΔ′₀-₉]*)_([A-Za-z0-9′]+)')


def runs(p, text, size=10, bold=False, color=INK):
    """Matnni yozadi: **...** qalin shrift, X_a / X_a2 kabi pastki indekslar va ^ belgilari."""
    segments = text.split('**')
    for i, seg in enumerate(segments):
        if seg:
            _segment(p, seg, size, bold or (i % 2 == 1), color)


def _segment(p, text, size, bold, color):
    def put(t, lower=False, upper=False):
        if not t: return
        r = p.add_run(t); r.font.name = 'Times New Roman'; r.font.size = Pt(size)
        r.bold = bold; r.font.color.rgb = RGBColor.from_string(color)
        if lower: r.font.subscript = True
        if upper: r.font.superscript = True
    def emit(chunk):
        if not chunk: return
        buf = ''
        for ch in chunk:
            if ch in sub:
                put(buf); buf = ''; put(sub[ch], lower=True)
            elif ch in sup:
                put(buf); buf = ''; put(sup[ch], upper=True)
            else:
                buf += ch
        put(buf)
    pos = 0
    for m in TOKEN.finditer(text):
        emit(text[pos:m.start()])
        put(m.group(1)); put(m.group(2), lower=True)
        pos = m.end()
    emit(text[pos:])


def shade(cell, fill):
    x = OxmlElement('w:shd'); x.set(qn('w:fill'), fill); cell._tc.get_or_add_tcPr().append(x)


def cell_margin(cell, **kwargs):
    x = OxmlElement('w:tcMar')
    for k, v in kwargs.items():
        y = OxmlElement('w:' + k); y.set(qn('w:w'), str(v)); y.set(qn('w:type'), 'dxa'); x.append(y)
    cell._tc.get_or_add_tcPr().append(x)


def border(cell, edge, color, size):
    bs = OxmlElement('w:tcBorders'); b = OxmlElement('w:' + edge)
    b.set(qn('w:val'), 'single'); b.set(qn('w:color'), color); b.set(qn('w:sz'), str(size))
    bs.append(b); cell._tc.get_or_add_tcPr().append(bs)


def band(label, fill, color, size, accent=False):
    t = doc.add_table(rows=1, cols=1); t.autofit = False; t.columns[0].width = Cm(18)
    c = t.cell(0, 0); shade(c, fill); cell_margin(c, top=140, bottom=140, left=200, right=160)
    if accent: border(c, 'left', BRONZE, 24)
    p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.keep_with_next = True
    runs(p, label, size, True, color)
    for p in c.paragraphs: p.paragraph_format.keep_with_next = True
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.line_spacing = Pt(3)
    p.paragraph_format.keep_with_next = True


tables = json.loads((ROOT / 'matn' / '07_03_jadvallar.json').read_text())
table_count = 0


def add_table(cell, spec):
    global table_count
    table_count += 1
    p = cell.add_paragraph(); p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4); p.paragraph_format.keep_with_next = True
    runs(p, spec['caption'], 8.5, True, NAVY)
    t = cell.add_table(rows=1, cols=len(spec['headers'])); t.autofit = False
    for col, w in zip(t.columns, spec['widths']): col.width = Cm(w)
    for i, label in enumerate(spec['headers']):
        c = t.rows[0].cells[i]; c.width = Cm(spec['widths'][i]); shade(c, NAVY)
        cell_margin(c, top=10, bottom=10, left=70, right=70)
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
        runs(p, label, 7.5, True, 'FFFFFF')
    rp = t.rows[0]._tr.get_or_add_trPr(); repeat = OxmlElement('w:tblHeader'); rp.append(repeat)
    for ri, row in enumerate(spec['rows']):
        r = t.add_row(); trp = r._tr.get_or_add_trPr(); trp.append(OxmlElement('w:cantSplit'))
        for ci, value in enumerate(row):
            c = r.cells[ci]; c.width = Cm(spec['widths'][ci])
            cell_margin(c, top=10, bottom=10, left=70, right=70)
            if ri % 2 == 0: shade(c, PALE)
            border(c, 'bottom', 'D6DFE7', 3)
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
            runs(p, value, 7.5, ci == 0, INK)
    p = cell.add_paragraph(); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(3)


refs = [
 '[1] NIST Chemistry WebBook (CAS 7664-93-9) va NIST-JANAF (Chase, 1998): ΔfH°(g) −735,13 kJ/mol;  S° 298,78 J/(mol·K);  proton affinity 699,4 kJ/mol;  gaz bazikligi 666,9 kJ/mol;  ΔrG°(deprotonatsiya) 1265 ± 10 kJ/mol (Hunter & Lias, 1998).',
 '[2] NIST CCCBDB (C7664939):  C₂ simmetriya;  r(S=O) 142,2 pm;  r(S–OH) 157,4 pm;  r(O–H) 97,0 pm;  ∠O=S=O 123,3°;  ∠H–O–S 108,5°;  τ 89,1°;  kristal C2/c: a 818,1, b 469,60, c 856,3 pm, β 111,39°, Z 4.',
 '[3] Ab initio muvozanat tuzilmasi (2007): r(S=O) 140,99 pm;  τ −86,66°.  Raman/IR: SO₄²⁻ ν₁ 981, ν₂ 451, ν₃ 1104, ν₄ 617 sm⁻¹;  HSO₄⁻ 1055/1030/900 sm⁻¹ (Myhre va b., 2003; Attaia va b., 2020).',
 '[4] Kislotalik: K_a2 = 1,2×10⁻² (pK_a2 1,99);  K_a1 ≈ 10³;  H₀ = −12;  proton solvatatsiyasi ≈ −995 kJ/mol;  100 % kislota tarkibi (mmol/kg): HSO₄⁻ 15,0, H₃SO₄⁺ 11,3, H₃O⁺ 8,0, HS₂O₇⁻ 4,4, H₂S₂O₇ 3,6, H₂O 0,1.',
 '[5] Gidratlar va fazaviy diagramma (IUCr, 2012): SAM 84,5 %, SAD 73,1 %, SATri 64,5 %, SAT 57,6 %, SAH 45,6 %, SAO 40,5 %;  muz–SAH 211 K, muz–SAT 199 K.  Sanoat: USGS (2024), S&P Global — 260–290 mln t/y, fosfat o‘g‘itlari 56–60 %.',
 '[6] OSHA (29 CFR 1910.1000), NIOSH NPG/IDLH, ACGIH TLV, AIHA ERPG: PEL 1 mg/m³;  REL 1 mg/m³;  TLV-TWA 0,2 mg/m³ (torakal, A2);  IDLH 15 mg/m³;  ERPG 2/10/120 mg/m³;  IARC 1 — kuchli noorganik kislota tumanlari.']

source = (ROOT / 'matn' / '07_03.md').read_text()
sections = []
for raw in source.split('## ')[1:]:
    title, body = raw.split('\n', 1); sections.append((title, body.strip().split('\n\n')))
assert len(sections) == 11
side_notes = json.loads((ROOT / 'matn' / '07_03_yonlavhalar.json').read_text())
assert len(side_notes) == len(sections)
counter = 0
for idx, ((title, paras), pan) in enumerate(zip(sections, panels)):
    pidx, pic, kind, panel, note = pan[:5]
    main_w = pan[5] if len(pan) > 5 else 3.95
    assert pidx == idx
    if idx:
        pb = doc.add_paragraph()
        pb.paragraph_format.space_after = Pt(0); pb.paragraph_format.space_before = Pt(0)
        pb.paragraph_format.line_spacing = Pt(1)
        r = pb.add_run(); r.font.size = Pt(1)
        br = OxmlElement('w:br'); br.set(qn('w:type'), 'page'); r._r.append(br)
    if idx == 0:
        band('7-BOB  /  OLTINGUGURT KISLOTALARI', NAVY, 'FFFFFF', 11)
        band('7.3. Sulfat kislota — tuzilishi', PALE, NAVY, 18, True)
    else:
        band('7.3  /  SULFAT KISLOTA — TUZILISHI', PALE, NAVY, 11, True)
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4); p.paragraph_format.keep_with_next = True
    runs(p, title, 13, True, NAVY)
    table = doc.add_table(rows=1, cols=2); table.alignment = WD_TABLE_ALIGNMENT.CENTER; table.autofit = False
    table.columns[0].width = Cm(13.5); table.columns[1].width = Cm(4.5)
    left, right = table.rows[0].cells
    left.width = Cm(13.5); right.width = Cm(4.5)
    for c in [left, right]: c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    cell_margin(left, top=0, bottom=0, left=0, right=220)
    cell_margin(right, top=140, bottom=130, left=160, right=100)
    shade(right, 'F5F8FA'); border(right, 'left', 'D2DCE5', 6)
    first = True
    for text in paras:
        if text.startswith('[[TABLE:'):
            key = text[len('[[TABLE:'):-2]
            add_table(left, tables[key])
            continue
        p = left.paragraphs[0] if first else left.add_paragraph()
        j = 0 if first else 1
        first = False
        if text.startswith('[[EQ:') and text.endswith(']]'):
            text = text[5:-2]
            counter += 1; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(4)
            add_equation(p, left, '7.3', counter, runs)
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(.45 if j else 0)
            runs(p, text)
    p = right.paragraphs[0]; p.paragraph_format.space_after = Pt(9)
    runs(p, panel, 10, True, NAVY)
    p = right.add_paragraph(); p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(ASSETS / pic), width=Cm(main_w))
    p = right.add_paragraph(); p.paragraph_format.space_after = Pt(10)
    runs(p, LABEL[kind], 9, True, NAVY)
    p = right.add_paragraph(); runs(p, note, 9)
    for item in extra.get(idx, []):
        image, caption = item[0], item[1]
        width = item[2] if len(item) > 2 else 2.90
        p = right.add_paragraph(); p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(ASSETS / image), width=Cm(width))
        p = right.add_paragraph(); runs(p, caption + ' Rang shartli.', 9)
    for label, body in side_notes[idx]:
        p = right.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        pp = p._p.get_or_add_pPr(); bd = OxmlElement('w:pBdr')
        rule = OxmlElement('w:top'); rule.set(qn('w:val'), 'single')
        rule.set(qn('w:sz'), '4'); rule.set(qn('w:color'), BRONZE)
        rule.set(qn('w:space'), '5'); bd.append(rule); pp.append(bd)
        runs(p, label, 9, True, NAVY)
        p = right.add_paragraph()
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_together = True
        runs(p, body, 9)
    if idx == 10:
        p = left.add_paragraph(); p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.line_spacing = 1.0; p.paragraph_format.space_after = Pt(0)
        runs(p, 'Barcha grafik, sxema va rasmlar original o‘quv ishlanmalari; sonli egri chiziqlar taxminiy hisoblar (o‘lchov ma’lumotlari emas). Rasmlar mikrofoto yoki atom tuzilmasi tasviri emas. Qurilma, texnologik parametrlar, konsentratsiya tanlash, idish materiallari, dozalar va tibbiy tavsiyalar bo‘yicha amaliyot tavsiyalari berilmaydi; xavfli kislotalar bilan ishlash tartibi 12-bo‘limda.', 8)
        p = left.add_paragraph(); p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1); p.paragraph_format.keep_with_next = True
        pp = p._p.get_or_add_pPr(); bd = OxmlElement('w:pBdr')
        rule = OxmlElement('w:top'); rule.set(qn('w:val'), 'single')
        rule.set(qn('w:sz'), '4'); rule.set(qn('w:color'), BRONZE)
        rule.set(qn('w:space'), '4'); bd.append(rule); pp.append(bd)
        runs(p, 'Manbalar va adabiyotlar', 9, True, NAVY)
        for ref in refs:
            p = left.add_paragraph(); p.paragraph_format.line_spacing = 0.95
            p.paragraph_format.space_after = Pt(0); runs(p, ref, 7)

p = sec.header.paragraphs[0]; runs(p, 'NOORGANIK KISLOTALAR', 8, False, NAVY)
p = sec.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
runs(p, '7-BOB   ·   ', 8, False, NAVY)
f = OxmlElement('w:fldSimple'); f.set(qn('w:instr'), 'PAGE'); p._p.append(f)
doc.core_properties.title = 'Noorganik kislotalar · 7.3 · Sulfat kislota — tuzilishi'
doc.core_properties.author = ''
OUT.parent.mkdir(parents=True, exist_ok=True); doc.save(OUT)
assert len(doc.inline_shapes) == 17
assert counter == 11
assert table_count == 11
assert sum(len(notes) for notes in side_notes) == 45
print(OUT)
print('11 bo‘lim; 11 jadval; 5 hisoblangan grafik; 7 sxema; 5 original illyustratsiya; 11 formula; 45 yon lavha.')
