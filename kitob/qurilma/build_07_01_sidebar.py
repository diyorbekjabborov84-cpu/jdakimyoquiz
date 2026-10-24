#!/usr/bin/env python3
"""A4: 3/4 asosiy matn + 1/4 vizual yon ustun. 7.1 "Vodorod sulfid" moduli."""
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
OUT = ROOT / 'chiqish' / 'Noorganik-kislotalar-7.1-Vodorod-sulfid.docx'
ASSETS = ROOT / 'rasmlar' / 'h2s'
NAVY = '0B2C4A'; BRONZE = 'C28E3B'; PALE = 'EDF3F7'; INK = '243746'

panels = [
 (0, 'tabiiy.png', 'rasm', 'Tabiiy manbalar va biologik rol.',
  '7.1.1-rasm. Vulkan, neft konlari va anaerob sulfat-reduksiya (sxematik, original).'),
 (1, 'molekulax.png', 'rasm', 'Molekula tuzilishi va energetika.',
  '7.1.2-rasm. H₂S molekulasi: burchak, bog‘ uzunligi, erkin elektron juftlari (sxematik, original).'),
 (2, 'fizik.png', 'grafik', 'Bug‘ bosimi va gaz zichligi.',
  '7.1.3-grafik. Clausius–Clapeyron egri chizig‘i va ideal gaz zichligi (taxminiy egri chiziq).'),
 (3, 'eritma.png', 'grafik', 'Eritma pH va dissotsiatsiya.',
  '7.1.4-grafik. Kuchsiz kislota uchun pH va dissotsiatsiya darajasi (taxminiy egri chiziq).'),
 (4, 'kislotalik.png', 'grafik', 'Spetsiatsiya va [S²⁻].',
  '7.1.5-grafik. H₂S/HS⁻/S²⁻ ulushlari va sulfid ioni konsentratsiyasi (taxminiy egri chiziq).'),
 (5, 'hosilax.png', 'rasm', 'Hosilalish usullari.',
  '7.1.6-rasm. Laboratoriya, tabiiy jarayon va sanoat yo‘llari (sxematik, original).'),
 (6, 'redoksx.png', 'sxema', 'Redoks xossalari.',
  '7.1.7-sxema. Yondirish, yod bilan reaksiya va standart potensiallar (sxematik).'),
 (7, 'metall.png', 'grafik', 'Sulfidlar va cho‘qma chegarasi.',
  '7.1.8-grafik. K_sp va pH bo‘yicha [M²⁺] chegarasi (taxminiy egri chiziq).'),
 (8, 'xavfsizlikx.png', 'sxema', 'Xavfsizlik chegaralari.',
  '7.1.9-sxema. Kasb chegaralari, IDLH, reaksion javoblar va monitor (sxematik).'),
 (9, 'clausx.png', 'rasm', 'Claus usuli.',
  '7.1.10-rasm. Termik va katalitik bosqichlar, separator va qoldiq gaz (sxematik, original).'),
 (10, 'ekvivalent.png', 'grafik', 'Ekvivalent va yodometriya.',
  '7.1.11-grafik. Ekvivalent massa, neytralizatsiya va yodometrik aniqlash (taxminiy egri chiziq).')]
extra = {
 0: [('idishx.png', '7.1.1-rasm. Idish materiallari, korroziya va saqlash shartlari (sxematik, original).', 2.80)],
 2: [('fizikx.png', '7.1.3-sxema. Agregat holatlari, kritik nuqta va yong‘inuvchanlik (sxematik).')],
 3: [('eritmax.png', '7.1.4-sxema. Dissotsiatsiya, pH va Henry muvozanati (sxematik).')],
 6: [('metallx.png', '7.1.7-sxema. Metallarga ta’sir, sulfid cho‘qmalari va minerallik (sxematik).')],
 7: [('tuzlarx.png', '7.1.8-sxema. K_sp, eruvchanlik va cho‘qma ranglari (sxematik).')],
 8: [('tahlilx.png', '7.1.9-sxema. Yodometriya, gravimetriya, spektroskopiya va monitor (sxematik).')]}

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
TOKEN = re.compile(r'([A-Za-zΑ-Ωα-ωβγδΔ′][A-Za-zΑ-Ωα-ωβγδΔ′₀-₉]*)_([A-Za-z0-9,′]+)')


def runs(p, text, size=10, bold=False, color=INK):
    def put(t, lower=False, upper=False):
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


tables = json.loads((ROOT / 'matn' / '07_01_jadvallar.json').read_text())
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
 '[1] NIST Chemistry WebBook, CAS 7783-06-4: ΔfH°(g) −20,6 kJ/mol;  S° 205,81 J/(mol·K);  ΔfG° −37,28 kJ/mol;  C_p 34,25 J/(mol·K);  Tb 212,87 K;  Tm 190,85 K;  Pc 89,63 bar;  ρ_c 10,2 mol/L.',
 '[2] NIST CCCBDB (Coo, DeL 1975): r(S–H) 1,3356 Å;  ∠H–S–H 92,11°;  C₂v simmetriya.',
 '[3] EPA/IRIS (0061tr) va ATSDR (Tox. Prof. 114): eruvchanlik 3,98 g/L (20 °C), 5,3 g/L (10 °C), 1,22 g/L (25 °C);  pK_a1 7,04;  pK_a2 11,96;  1 ppm = 1,39 mg/m³.',
 '[4] OSHA, NIOSH (npgd0337), ACGIH, ICSC 1326: PEL 20 ppm (50 ppm — 10 daqiqa);  REL 10 ppm;  TLV 1/5 ppm;  IDLH 100 ppm;  ERPG 0,1/30/100 ppm;  PAC 0,51/27/50 ppm.',
 '[5] K_sp jadvallari (UMass, URI, OpenStax) va US EPA AP-42 8.13 (Claus usuli);  USGS: jahon oltingugurt ishlab chiqarishi 85,8 Mt (2023).']

source = (ROOT / 'matn' / '07_01.md').read_text()
sections = []
for raw in source.split('## ')[1:]:
    title, body = raw.split('\n', 1); sections.append((title, body.strip().split('\n\n')))
assert len(sections) == 11
side_notes = json.loads((ROOT / 'matn' / '07_01_yonlavhalar.json').read_text())
assert len(side_notes) == len(sections)
counter = 0
for idx, ((title, paras), pan) in enumerate(zip(sections, panels)):
    pidx, pic, kind, panel, note = pan[:5]
    main_w = pan[5] if len(pan) > 5 else 3.92
    assert pidx == idx
    if idx:
        pb = doc.add_page_break(); pb.paragraph_format.space_after = Pt(0)
        pb.paragraph_format.space_before = Pt(0); pb.paragraph_format.line_spacing = Pt(1)
        for r in pb.runs: r.font.size = Pt(1)
    if idx == 0:
        band('7-BOB  /  OLTINGUGURT KISLOTALARI', NAVY, 'FFFFFF', 11)
        band('7.1. Vodorod sulfid', PALE, NAVY, 18, True)
    else:
        band('7.1  /  VODOROD SULFID', PALE, NAVY, 11, True)
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
            add_equation(p, left, '7.1', counter, runs)
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
        width = item[2] if len(item) > 2 else 3.30
        p = right.add_paragraph(); p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(ASSETS / image), width=Cm(width))
        p = right.add_paragraph(); runs(p, caption + ' Rang, o‘lcham va geometriya shartli.', 9)
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
        runs(p, 'Barcha grafik, sxema va rasmlar original o‘quv ishlanmalari; sonli egri chiziqlar taxminiy hisoblar (o‘lchov ma’lumotlari emas). Rasmlar mikrofoto yoki atom tuzilmasi tasviri emas. Qurilma, texnologik parametrlar, konsentratsiya tanlash, idish materiallari, dozalar va tibbiy tavsiyalar bo‘yicha amaliyot tavsiyalari berilmaydi; xavfli gazlar bilan ishlash tartibi 12-bo‘limda.', 8)
        p = right.add_paragraph(); p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = True
        pp = p._p.get_or_add_pPr(); bd = OxmlElement('w:pBdr')
        rule = OxmlElement('w:top'); rule.set(qn('w:val'), 'single')
        rule.set(qn('w:sz'), '4'); rule.set(qn('w:color'), BRONZE)
        rule.set(qn('w:space'), '5'); bd.append(rule); pp.append(bd)
        runs(p, 'Manbalar va adabiyotlar', 9, True, NAVY)
        for ref in refs:
            p = right.add_paragraph(); p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2); runs(p, ref, 7)

p = sec.header.paragraphs[0]; runs(p, 'NOORGANIK KISLOTALAR', 8, False, NAVY)
p = sec.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
runs(p, '7-BOB   ·   ', 8, False, NAVY)
f = OxmlElement('w:fldSimple'); f.set(qn('w:instr'), 'PAGE'); p._p.append(f)
doc.core_properties.title = 'Noorganik kislotalar · 7.1 · Vodorod sulfid'
doc.core_properties.author = ''
OUT.parent.mkdir(parents=True, exist_ok=True); doc.save(OUT)
assert len(doc.inline_shapes) == 17
assert counter == 11
assert table_count == 11
assert sum(len(notes) for notes in side_notes) == 22
print(OUT)
print('11 bo‘lim; 11 jadval; 5 hisoblangan grafik; 7 sxema; 5 original illyustratsiya; 11 formula; 22 yon lavha.')
