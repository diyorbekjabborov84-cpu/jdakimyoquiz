#!/usr/bin/env python3
"""A4: 3/4 asosiy matn + 1/4 vizual yon ustun. 6.1 "Guruhning umumiy tavsifi" moduli."""
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
OUT = ROOT / 'chiqish' / 'Noorganik-kislotalar-6.1-Guruhning-umumiy-tavsifi.docx'
ASSETS = ROOT / 'rasmlar' / 'galogenid'
NAVY = '0B2C4A'; BRONZE = 'C28E3B'; PALE = 'EDF3F7'; INK = '243746'

panels = [
 (0, 'sxematurlari.png', 'sxema', 'Guruh trendlari: bitta sxema, beshta ko‘rsatkich.',
  '6.1.1-sxema. Elektronegativlik, bog‘ energiyasi, kislotalik, termik barqarorlik va qaytaruvchilik trendlari.'),
 (1, 'gibridlanishx.png', 'sxema', 'H–X bog‘i va dipol moment.',
  '6.1.2-sxema. Elektron bulutining siljishi, σ bog‘ quyuqligi va vodorod bog‘i (sxematik).'),
 (2, 'kislotalik.png', 'grafik', 'Suvda tekislash va DMSOdagi farq.',
  '6.1.3-grafik. pK_a qiymatlari suvda va DMSO da (taxminiy egri chiziq).'),
 (3, 'energiya.png', 'grafik', 'Energetik balans: bog‘ va gidratatsiya.',
  '6.1.4-grafik. D(H–X), ΔH_hyd(X⁻) va ular yig‘indisi (taxminiy egri chiziq).'),
 (4, 'termik.png', 'grafik', 'Termik barqarorlik: dekompozitsiya.',
  '6.1.5-grafik. 2HX ⇌ H₂ + X₂ reaksiyasi uchun ΔG° va lgK (taxminiy egri chiziq).'),
 (5, 'olishsx.png', 'sxema', 'Olish usullari: bitta mantiq, to‘rt reagent.',
  '6.1.6-sxema. HF, HCl, HBr va HI olishining sxematik yo‘llari.'),
 (6, 'xossalarsx.png', 'sxema', 'Kislota xossalari: metallar, oksidlar, tuzlar.',
  '6.1.7-sxema. Namoyonlar va neytralizatsiya mass balansi (shartli hisob).'),
 (7, 'redokssx.png', 'sxema', 'Redoks xossalari: qaytaruvchi xarakter.',
  '6.1.8-sxema. HBr va HI ning oksidlanishi hamda halogenning o‘zining oksidlovchi xarakteri.'),
 (8, 'materiallarx.png', 'sxema', 'Materiallar bilan munosabat.',
  '6.1.9-sxema. HF va shisha, metallarga ta’sir, idish tanlash mezonlari (sxematik).'),
 (9, 'xavfsizliksx.png', 'sxema', 'Xavfsizlik, ekologiya va logistika.',
  '6.1.10-sxema. HF ning tizimli toksikligi, neytralizatsiya va saqlash tashimoti.'),
 (10, 'hisob.png', 'rasm', 'Ishlangan hisob: uch shartli hisob.',
  '6.1.11-rasm. Taxmin A — HF muvozanati; Taxmin B — azeotrop; Taxmin C — energiya balansi.')]

extra = {
 0: [('guruhx.png', '6.1.1-rasm. To‘rt molekula va ularning o‘lchamlari (sxematik).')],
 1: [('fizik.png', '6.1.2-grafik. Bog‘ uzunligi va dipol moment (taxminiy egri chiziq).')],
 2: [('dissotsiatsiya.png', '6.1.3-grafik. HF dissotsiatsiyasi: konsentratsiya va ionizatsiya (shartli hisob).')],
 3: [('speciatsiyax.png', '6.1.4-rasm. HF eritmasida spetsiatsiya: HF, HF₂⁻ va H₂F⁺ (sxematik).')],
 8: [('sishax.png', '6.1.9-rasm. Shishani HF yemirishi: sxematik kesim.')],
 9: [('logistikax.png', '6.1.10-rasm. Saqlash va transport: idish tanlash (sxematik).')]}

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


comparisons = json.loads((ROOT / 'matn' / '06_01_jadvallar.json').read_text())
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
 '[1] OpenStax, Chemistry 2e, §7.5 va §8.1: D(H–F) 569, H–Cl 432, H–Br 370, H–I 295 kJ/mol; r(H–X) 127,5 / 141,4 / 160,9 pm.',
 '[2] OpenStax, Chemistry 2e, App. G: ΔfH°(g) HF −273,3, HCl −92,307, HBr −36,3, HI +26,48 kJ/mol; ΔfG°(X⁻,aq) −278,8 / −131,2 / −102,82 / −51,57.',
 '[3] ChemGuide — Halogens as oxidising agents: ΔH_hyd(X⁻) −506 / −364 / −335 / −293 kJ/mol.',
 '[4] Acid strength (baholangan pK_a): suvda HCl −5,9, HBr −8,8, HI −9,5; DMSOda HF 15, HCl −2,0, HBr −6,8, HI −10,9.',
 '[5] Azeotroplar: HCl 20,2 % / 108,6 °C; HBr 47,6 % / 124,3 °C; HI 56,9 % / 127 °C; HF 37 % / 120 °C.',
 '[6] CDC/NIOSH (MMG 1142), Calpoison, StatPearls: HF — OSHA TWA 3 ppm, IDLH 30 ppm, kalsiy glyukonat; ACA — Anhydrous HF ko‘rsatmalari.',
 '[7] Ph. Eur. 6.0 — 2.2.32, 2.5.12 va 5.11 umumiy bo‘limlari (5.1–5.3-bo‘limlarda ko‘rib chiqilgan).']

source = (ROOT / 'matn' / '06_01.md').read_text()
sections = []
for raw in source.split('## ')[1:]:
    title, body = raw.split('\n', 1); sections.append((title, body.strip().split('\n\n')))
assert len(sections) == 11
side_notes = json.loads((ROOT / 'matn' / '06_01_yonlavhalar.json').read_text())
assert len(side_notes) == len(sections)
counter = 0
for idx, ((title, paras), (pidx, pic, kind, panel, note)) in enumerate(zip(sections, panels)):
    assert pidx == idx
    if idx:
        pb = doc.add_page_break(); pb.paragraph_format.space_after = Pt(0)
        pb.paragraph_format.space_before = Pt(0); pb.paragraph_format.line_spacing = Pt(1)
        for r in pb.runs: r.font.size = Pt(1)
    if idx == 0:
        band('6-BOB  /  VODOROD GALOGENIDLARI', NAVY, 'FFFFFF', 11)
        band('6.1. Guruhning umumiy tavsifi', PALE, NAVY, 18, True)
    else:
        band('6.1  /  GURUHNING UMUMIY TAVSIFI', PALE, NAVY, 11, True)
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
            add_equation(p, left, '6.1', counter, runs)
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
        runs(p, 'Barcha grafik, sxema va rasmlar original o‘quv ishlanmalari; sonli egri chiziqlar taxminiy hisoblar (o‘lchov ma’lumotlari emas). Qurilma, texnologik parametrlar, konsentratsiya va idish materiali tanlash bo‘yicha amaliyot tavsiyalari berilmaydi; xavfli kislotalar bilan ishlash tartibi 12-bo‘limda.', 8)
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
runs(p, '6-BOB   ·   ', 8, False, NAVY)
f = OxmlElement('w:fldSimple'); f.set(qn('w:instr'), 'PAGE'); p._p.append(f)
doc.core_properties.title = 'Noorganik kislotalar · 6.1 · Guruhning umumiy tavsifi'
doc.core_properties.author = ''
OUT.parent.mkdir(parents=True, exist_ok=True); doc.save(OUT)
assert len(doc.inline_shapes) == 17
assert counter == 11
assert comparison_count == 11
assert sum(len(notes) for notes in side_notes) == 22
print(OUT)
print('11 bo‘lim; 11 jadval; 5 hisoblangan grafik; 7 sxema; 5 original illyustratsiya; 11 formula; 22 yon lavha.')
