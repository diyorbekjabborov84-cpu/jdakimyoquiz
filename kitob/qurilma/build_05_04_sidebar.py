#!/usr/bin/env python3
"""A4: 3/4 asosiy matn + 1/4 vizual yon ustun. 5.4 "Sanoat prinsiplari" moduli."""
import book_equations
from book_equations import add_equation
book_equations.EQ_SIZE = 19
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
OUT = ROOT / 'chiqish' / 'Noorganik-kislotalar-5.4-Sanoat-prinsiplari.docx'
ASSETS = ROOT / 'rasmlar' / 'sanoat'
NAVY = '0B2C4A'; BRONZE = 'C28E3B'; PALE = 'EDF3F7'; INK = '243746'

panels = [
 (0, 'sxematurlari.png', 'sxema', 'Texnologik sxemaning uch turi.',
  '5.4.1-sxema. To‘g‘ridan-to‘g‘ri, oraliq mahsulotli va yopiq sxemalar.'),
 (1, 'bugtizimi.png', 'sxema', 'Bug‘ va energiya tizimi.',
  '5.4.2-sxema. Kotlovana, turbogenerator, issiqlikni qayta foydalanish va sarflash o‘lchagichi.'),
 (2, 'oqim.png', 'grafik', 'Zanjir bo‘yicha materiallar oqimi.',
  '5.4.3-grafik. Kiruvchi va chiquvchi oqimlar, 1000 kg 68 % li HNO₃ asosida (shartli hisob).'),
 (3, 'bug.png', 'grafik', 'Bug‘ darajalari: bosim va harorat.',
  '5.4.4-grafik. Qatnoq bug‘ jadvali qiymatlari va ularning izchilligi.'),
 (4, 'materiallar.png', 'rasm', 'Materiallar: qoplama va korroziya qatlami.',
  '5.4.5-rasm. Muhit, himoya qatlami, qotishma va konstruktsiya (sxematik kesim).'),
 (5, 'inertlashsx.png', 'sxema', 'Inertlash va yonishdan himoya tizimi.',
  '5.4.6-sxema. Oldini olish, aniqlash va hamkorlikdagi chora-tadbirlar.'),
 (6, 'chiqindisx.png', 'sxema', 'Chiqindilarni boshqarish sxemasi.',
  '5.4.7-sxema. Gaz, suyuq va qattiq chiqindilar hamda ularni kamaytirish yo‘llari.'),
 (7, 'izchillik.png', 'rasm', 'Izchillik (traceability) zanjiri.',
  '5.4.8-rasm. Xom ashyo partiyasidan tayyor mahsulotgacha (sxematik).'),
 (8, 'raqamlisx.png', 'sxema', 'Raqamli boshqaruv zanjiri.',
  '5.4.9-sxema. Maydon → boshqaruv → yuqori pog‘ona va ma’lumot tahlili.'),
 (9, 'opex.png', 'grafik', 'Ekspluatatsiya xarajatlarining tarkibi.',
  '5.4.10-grafik. OPEX tarkibi (shartli hisob ulushlar).'),
 (10, 'hisob.png', 'rasm', 'Ishlangan hisob: zanjir va iqtisodiyot.',
  '5.4.11-rasm. Taxmin A — zanjir mass balansi; Taxmin B — iqtisodiyot.')]

extra = {
 0: [('oqsxemasi.png', '5.4.1-sxema. Apparat va oqimlar ketma-ketligi (sxematik).')],
 1: [('logistikax.png', '5.4.2-sxema. Xom ashyodan tayyor mahsulotgacha logistika zanjiri.')],
 2: [('xotira.png', '5.4.3-rasm. Tank park va uzluksizlik: xotira — xavf zaxirasi (sxematik).')],
 3: [('issiqlik.png', '5.4.4-grafik. Jarayon oqimi harorat profili va bug‘ darajalari (shartli hisob).')],
 5: [('xavf.png', '5.4.6-rasm. Xavf boshqaruvning uch qatlami (sxematik).')],
 9: [('birlikqiymat.png', '5.4.10-grafik. Birlik FOA va quvvat bog‘liqligi (taxminiy egri chiziq).')]}

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


comparisons = json.loads((ROOT / 'matn' / '05_04_jadvallar.json').read_text())
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
 '[1] OpenStax, Chemistry 2e, App. G — Standard Thermodynamic Properties. ΔfH° (25 °C): NH₃ −45,90; HNO₃(l) −174,10; H₂O(l) −285,83; NO 90,25; NO₂ 33,20 kJ/mol.',
 '[2] ISO 22400-2:2014 — Automation systems and integration. Key performance indicators for manufacturing operations management. Part 2: Definitions and descriptions. OEE = Availability × Performance × Quality.',
 '[3] OPC UA — OPC-40501-1, Part 1: Machine Monitoring and Job Management, C.2.4 Calculation of OEE (APT/PBT; PRI×PQ/APT; GQ/PQ).',
 '[4] IUPAC Gold Book: exergy; process intensification (Ramshaw, 1995; Stankiewicz & Moulijn, 2000); waste; hazard.',
 '[5] CRC Handbook of Chemistry and Physics, 97th ed. — qatnoq bug‘ jadvali (harorat, entalpiya) va molar massalar.',
 '[6] ISO 9001 (sifat), ISO 14001 (muhit), ISO 45001 (kasbiy xavfsizlik); WHO GMP; FDA 21 CFR Part 211 (cGMP).',
 '[7] Ph. Eur. 6.0 — monografiyalar va umumiy bo‘limlar (2.2.32, 2.5.12, 5.11).',
 '[8] Luis, P. (2013) Exergy as a tool for measuring process intensification in chemical engineering. J. Chem. Technol. Biotechnol. 88(11), 1711–1718.']

source = (ROOT / 'matn' / '05_04.md').read_text()
sections = []
for raw in source.split('## ')[1:]:
    title, body = raw.split('\n', 1); sections.append((title, body.strip().split('\n\n')))
assert len(sections) == 11
side_notes = json.loads((ROOT / 'matn' / '05_04_yonlavhalar.json').read_text())
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
        band('5.4. Sanoat prinsiplari', PALE, NAVY, 18, True)
    else:
        band('5.4  /  SANOAT PRINSIPLARI', PALE, NAVY, 11, True)
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
            add_equation(p, left, '5.4', counter, runs)
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
        runs(p, 'Barcha grafik, sxema va rasmlar original o‘quv ishlanmalari; sonli egri chiziqlar taxminiy hisoblar (o‘lchov ma’lumotlari emas). Rasmlar mikrofoto yoki atom tuzilmasi tasviri emas. Qurilma, apparat va texnologik parametrlar, xom ashyo nisbatlari, mahsulot narxi va ishlab chiqarish retsepti bo‘yicha amaliyot tavsiyalari berilmaydi; xavfli kislotalarning tayyorlanishi va saqlanishi bo‘yicha ko‘rsatmalar 7, 8 va 12-bo‘limlarda.', 8)
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
doc.core_properties.title = 'Noorganik kislotalar · 5.4 · Sanoat prinsiplari'
doc.core_properties.author = ''
OUT.parent.mkdir(parents=True, exist_ok=True); doc.save(OUT)
assert len(doc.inline_shapes) == 17
assert counter == 11
assert comparison_count == 11
assert sum(len(notes) for notes in side_notes) == 22
print(OUT)
print('11 bo‘lim; 11 jadval; 5 hisoblangan grafik; 7 sxema; 5 original illyustratsiya; 11 formula; 22 yon lavha.')
