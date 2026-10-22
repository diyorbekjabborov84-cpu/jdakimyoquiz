#!/usr/bin/env python3
"""A4: 3/4 asosiy matn + 1/4 vizual yon ustun. 5.3 "QuRITish va suvsizlantirish" moduli."""
import book_equations
from book_equations import add_equation
book_equations.EQ_SIZE = 19   # 5.3 formulalari biroz kichikroq
book_equations.EQ_GAP = 4
book_equations.EQ_LEAD = 1.0
from pathlib import Path
import re, json
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'chiqish' / 'Noorganik-kislotalar-5.3-Quritish-va-suvsizlantirish.docx'
ASSETS = ROOT / 'rasmlar' / 'quritish'
NAVY = '0B2C4A'; BRONZE = 'C28E3B'; PALE = 'EDF3F7'; INK = '243746'

panels = [
 (0, 'namliksxema.png', 'sxema', 'Suvning holatlari va o‘lchov usullari.',
  '5.3.1-sxema. Erkin, kristallizatsiya, sorbsiyalangan va reagent suvi; o‘lchov usullari.'),
 (1, 'higroskopik.png', 'rasm', 'Higroskopiklik: namlik darajasi va massa o‘sishi.',
  '5.3.2-rasm. Ph. Eur. 5.11 sinflari: deliquescent, ≥ 15 %, 2–15 %, 0,2–2 % (sxematik).'),
 (2, 'usullarsxema.png', 'sxema', 'QuRITish usullarining beshta oilasi.',
  '5.3.3-sxema. Mexanik, fizik, kimyoviy, fizik-kimyoviy va maxsus usullar.'),
 (3, 'vakuum.png', 'grafik', 'Vakuum: suvning qaynash harorati.',
  '5.3.4-grafik. Klausius–Klapeiron modeli: P va T bog‘liqligi (model egri chizig‘i).'),
 (4, 'azeotrop.png', 'grafik', 'Azeotrop: entrainer va suv sig‘imi.',
  '5.3.5-grafik. Entrainerlarning azeotrop harorati va bug fazasidagi suv ulushi.'),
 (5, 'sitalsxema.png', 'sxema', 'Molekulyar sital kolonkasi va regeneratsiya.',
  '5.3.6-sxema. Adsorbsiya, regeneratsiya va chiqindi sikli.'),
 (6, 'gidratsxema.png', 'sxema', 'Gidrat quritish: fazaviy o‘tish.',
  '5.3.7-sxema. CuSO₄·5H₂O → ·3H₂O → ·H₂O → anhiddrid.'),
 (7, 'ajratish.png', 'rasm', 'Azeotrop distillatining fazalarga ajralishi.',
  '5.3.8-rasm. Entrainer va suv fazasining ajralishi (sxematik).'),
 (8, 'nazoratsxema.png', 'sxema', 'Suv miqdori nazorati va hujjatlashtirish.',
  '5.3.9-sxema. Namuna olishdan hujjatgacha bo‘lgan nazorat zanjiri.'),
 (9, 'energiya.png', 'grafik', 'QuRITish usullarining energetik sarfi.',
  '5.3.10-grafik. 1 kg suvni olib tashlash uchun model energiyasi (kWh/kg).'),
 (10, 'hisob.png', 'rasm', 'Ishlangan hisob: ikki modelning modda oqimi.',
  '5.3.11-rasm. Model A — gidrat quritish; Model B — azeotropik suv chiqarish.')]

extra = {
 0: [('kinetika.png', '5.3.1-grafik. Quritish kinetikasi: namlik va vaqt (model egri chizig‘i).')],
 1: [('quritishegri.png', '5.3.2-rasm. Quritish egri chizig‘ining bosqichlari (sxematik).')],
 2: [('shkaf.png', '5.3.3-rasm. Quritish uskonasining kesimi (sxematik).')],
 3: [('shkafsxema.png', '5.3.4-sxema. Shkaf, vakuum desikatori va chuqur vakuum variantlari.')],
 4: [('azeotropsxema.png', '5.3.5-sxema. Azeotropik quritishning umumiy oqimi.')],
 5: [('adsorbsiya.png', '5.3.6-grafik. Muvozanat namligi va nisbiy namlik (model egri chizig‘i).')]}

LABEL = {'grafik': 'HISOBIY GRAFIK', 'sxema': 'TUSHUNTIRUVCHI SXEMA', 'rasm': 'CHIZMA VA IZOH'}

doc = Document(); sec = doc.sections[0]
sec.page_width = Cm(21); sec.page_height = Cm(29.7)
sec.left_margin = Cm(1.5); sec.right_margin = Cm(1.5)
sec.top_margin = Cm(1.5); sec.bottom_margin = Cm(1.4)
sec.header_distance = Cm(.65); sec.footer_distance = Cm(.65)
normal = doc.styles['Normal']; normal.font.name = 'Times New Roman'; normal.font.size = Pt(10)
normal.paragraph_format.line_spacing = 1.03
normal.paragraph_format.space_after = Pt(2)
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


comparisons = json.loads((ROOT / 'matn' / '05_03_jadvallar.json').read_text())
comparison_count = 0


def add_comparison_table(cell, spec):
    global comparison_count
    comparison_count += 1
    p = cell.add_paragraph(); p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4); p.paragraph_format.keep_with_next = True
    runs(p, spec['caption'], 8.5, True, NAVY)
    t = cell.add_table(rows=1, cols=len(spec['headers'])); t.autofit = False
    for col, w in zip(t.columns, spec['widths']): col.width = Cm(w)
    for i, label in enumerate(spec['headers']):
        c = t.rows[0].cells[i]; c.width = Cm(spec['widths'][i]); shade(c, NAVY)
        cell_margin(c, top=28, bottom=28, left=80, right=80)
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
        runs(p, label, 8, True, 'FFFFFF')
    rp = t.rows[0]._tr.get_or_add_trPr(); repeat = OxmlElement('w:tblHeader'); rp.append(repeat)
    for ri, row in enumerate(spec['rows']):
        r = t.add_row(); trp = r._tr.get_or_add_trPr(); trp.append(OxmlElement('w:cantSplit'))
        for ci, value in enumerate(row):
            c = r.cells[ci]; c.width = Cm(spec['widths'][ci])
            cell_margin(c, top=28, bottom=28, left=80, right=80)
            if ri % 2 == 0: shade(c, PALE)
            border(c, 'bottom', 'D6DFE7', 3)
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
            runs(p, value, 8, ci == 0, INK)
    p = cell.add_paragraph(); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(3)


refs = [
 '[1] OpenStax, Chemistry 2e, App. G — Standard Thermodynamic Properties. openstax.org/books/chemistry-2e/pages/g-standard-thermodynamic-properties-for-selected-substances . ΔfH° (25 °C).',
 '[2] Ph. Eur. 6.0, 2.2.32 — Loss on drying (5 usul: desikator, vakuum, vakuum+harorat, shkaf, chuqur vakuum ≤ 0,1 kPa; ±2 °C).',
 '[3] Ph. Eur. 6.0, 2.5.12 — Water (semi-micro Karl Fischer); 2.5.32 — micro usul.',
 '[4] Ph. Eur. 6.0, 5.11 — Characters section in monographs: higroskopiklik sinovi (25 °C, 80 ± 2 % RH, 24 h) va sinflar.',
 '[5] USP <731> — Loss on Drying: doimiy mass = ketma-ket tarozilar farqi ≤ 0,50 mg/g.',
 '[6] IUPAC Gold Book: deliquescence (D01582), efflorescence (E01909), desiccant (D01618).',
 '[7] U.S. EPA Method 9000 — Karl Fischer titratsiyasi (1:1 stixiometriya).',
 '[8] CRC Handbook of Chemistry and Physics, 97th ed. — ΔvapH, sublimatsiya entalpiyasi, molar massalar.']

source = (ROOT / 'matn' / '05_03.md').read_text()
sections = []
for raw in source.split('## ')[1:]:
    title, body = raw.split('\n', 1); sections.append((title, body.strip().split('\n\n')))
assert len(sections) == 11
side_notes = json.loads((ROOT / 'matn' / '05_03_yonlavhalar.json').read_text())
assert len(side_notes) == len(sections)
counter = 0
for idx, ((title, paras), (pidx, pic, kind, panel, note)) in enumerate(zip(sections, panels)):
    assert pidx == idx
    if idx:
        pb = doc.add_page_break(); pb.paragraph_format.space_after = Pt(0)
        pb.paragraph_format.space_before = Pt(0); pb.paragraph_format.line_spacing = Pt(1)
        for r in pb.runs: r.font.size = Pt(1)
    if idx == 0:
        band('5-BOB  /  OLISH, TOZALASH, KONSENTRLASH', NAVY, 'FFFFFF', 11)
        band('5.3. Quritish va suvsizlantirish', PALE, NAVY, 18, True)
    else:
        band('5.3  /  QURITISH VA SUVSIZLANTIRISH', PALE, NAVY, 11, True)
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(9); p.paragraph_format.keep_with_next = True
    runs(p, title, 14, True, NAVY)
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
            add_comparison_table(left, comparisons[key])
            continue
        p = left.paragraphs[0] if first else left.add_paragraph()
        j = 0 if first else 1
        first = False
        if text.startswith('[[EQ:') and text.endswith(']]'):
            text = text[5:-2]
            counter += 1; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(6)
            add_equation(p, left, '5.3', counter, runs)
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(.45 if j else 0)
            runs(p, text)
    p = right.paragraphs[0]; p.paragraph_format.space_after = Pt(9)
    runs(p, panel, 10, True, NAVY)
    p = right.add_paragraph(); p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(ASSETS / pic), width=Cm(3.92))
    p = right.add_paragraph(); p.paragraph_format.space_after = Pt(10)
    runs(p, LABEL[kind], 9, True, NAVY)
    p = right.add_paragraph(); runs(p, note, 9)
    for image, caption in extra.get(idx, []):
        p = right.add_paragraph(); p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(ASSETS / image), width=Cm(3.30))
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
        runs(p, 'Barcha grafik, sxema va rasmlar original o‘quv ishlanmalari; sonli egri chiziqlar model hisoblari (o‘lchov ma’lumotlari emas). Rasmlar mikrofoto yoki atom tuzilmasi tasviri emas. Konsentratsiya, harorat, bosim va vaqt oralig‘i eksperiment uchun ko‘rsatma emas; xavfli kislotalarning tayyorlanishi, quritish rejasi va saqlanishi bo‘yicha amaliyot tavsiyalari berilmaydi.', 8)
        p = right.add_paragraph(); p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3); p.paragraph_format.keep_with_next = True
        pp = p._p.get_or_add_pPr(); bd = OxmlElement('w:pBdr')
        rule = OxmlElement('w:top'); rule.set(qn('w:val'), 'single')
        rule.set(qn('w:sz'), '4'); rule.set(qn('w:color'), BRONZE)
        rule.set(qn('w:space'), '5'); bd.append(rule); pp.append(bd)
        runs(p, 'Manbalar va adabiyotlar', 9, True, NAVY)
        for ref in refs:
            p = right.add_paragraph(); p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(3); runs(p, ref, 7.5)

p = sec.header.paragraphs[0]; runs(p, 'NOORGANIK KISLOTALAR', 8, False, NAVY)
p = sec.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
runs(p, '5-BOB   ·   ', 8, False, NAVY)
f = OxmlElement('w:fldSimple'); f.set(qn('w:instr'), 'PAGE'); p._p.append(f)
doc.core_properties.title = 'Noorganik kislotalar · 5.3 · Quritish va suvsizlantirish'
doc.core_properties.author = ''
OUT.parent.mkdir(parents=True, exist_ok=True); doc.save(OUT)
assert len(doc.inline_shapes) == 17
assert counter == 11
assert comparison_count == 11
assert sum(len(notes) for notes in side_notes) == 22
print(OUT)
print('11 bo‘lim; 11 jadval; 5 hisoblangan grafik; 7 sxema; 5 original illyustratsiya; 11 formula; 22 yon lavha.')
