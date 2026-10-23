#!/usr/bin/env python3
"""A4: 3/4 asosiy matn + 1/4 vizual yon ustun. 6.3 "HCl — xlorid kislota" moduli."""
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
OUT = ROOT / 'chiqish' / 'Noorganik-kislotalar-6.3-HCl-xlorid-kislota.docx'
ASSETS = ROOT / 'rasmlar' / 'hcl'
NAVY = '0B2C4A'; BRONZE = 'C28E3B'; PALE = 'EDF3F7'; INK = '243746'

panels = [
 (0, 'molekulax.png', 'rasm', 'HCl molekulasi va dipol–dipol ta’sir.',
  '6.3.1-rasm. HCl molekulasi: r = 1,2746 Å, D = 432 kJ/mol, μ = 1,08 D (sxematik, original).'),
 (1, 'fizikx.png', 'sxema', 'HCl: fizik xossalar.',
  '6.3.2-sxema. Gaz holati, kritik nuqta, eritma, azeotrop va gidronium tuzlari (sxematik).'),
 (2, 'spetsiatsiya.png', 'grafik', 'Suvli HCl: model pH va jadval pH.',
  '6.3.3-grafik. Ideal model (−lg c) va jadvalning apparent pH qiymatlari (model egri chizig‘i).'),
 (3, 'olishsx.png', 'sxema', 'Ishlab chiqarish va tozalash.',
  '6.3.4-sxema. Mannheim va sintetik usullar, quruq tozalash, yig‘ish va navlar (sxematik).'),
 (4, 'kloridlarsx.png', 'sxema', 'Tuzlar va xloro-komplekslar.',
  '6.3.5-sxema. Xloridlar, kislota muhitidagi tuzlar va xloro-kompleks anionlar (sxematik).'),
 (5, 'metalsx.png', 'sxema', 'Metallarga ta’sir.',
  '6.3.6-sxema. Passivatsiya yo‘qligi, mis istisnosi, vodorod embrittlementi va teshik korroziya (sxematik).'),
 (6, 'korroziyax.png', 'rasm', 'Po‘latni tozalash.',
  '6.3.7-rasm. Oksid qatlamining HCl bilan erishi va H₂ ajralishi (sxematik, original).'),
 (7, 'suvsizsx.png', 'sxema', 'Suvsiz muhit va superkislotalar.',
  '6.3.8-sxema. Suvsiz dissotsiatsiya, xloroaluminat ion suyuqliklari va H₀ qiymatlari (sxematik).'),
 (8, 'qollanishsx.png', 'sxema', 'Qo‘llanish sohalari.',
  '6.3.9-sxema. Pickling, PVC, dezinfectsiya, ion almashinuv, oziq-ovqat va dori (sxematik).'),
 (9, 'tahlilsx.png', 'sxema', 'Tahlil usullari.',
  '6.3.10-sxema. Standartlash, dead-stop titr, Kjeldahl, argentometriya va zamonaviy usullar (sxematik).'),
 (10, 'hisob.png', 'rasm', 'Ishlangan hisob: to‘rt model.',
  '6.3.11-rasm. Model A — ishlab chiqarish; B — neytralizatsiya; C — metall; D — tiklash.')]

extra = {
 1: [('eritma.png', '6.3.2-grafik. Eritmaning qaynash harorati, bug‘ bosimi va zichligi (jadval ma’lumotlari).')],
 3: [('ishlabchiqarish.png', '6.3.4-grafik. 1000 kg HCl uchun mass oqimi: Mannheim va sintetik usul (model).')],
 4: [('metallar.png', '6.3.5-grafik. Metall yemirilishida HCl sarfi (model egri chizig‘i).')],
 5: [('teshikx.png', '6.3.6-rasm. Teshik (pitting) korroziya: Cl⁻ ionlarining ta’siri (sxematik, original).')],
 6: [('idishx.png', '6.3.7-rasm. Saqlash va transport: idish tanlash mezonlari (sxematik, original).')],
 9: [('chiqindi.png', '6.3.10-grafik. Neytralizatsiya mass balansi va kislotani tiklash sikli (model egri chizig‘i).')]}

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


comparisons = json.loads((ROOT / 'matn' / '06_03_jadvallar.json').read_text())
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
 '[1] Wikipedia — Hydrochloric acid: fizik jadval (10–38 %: ρ, pH, μ, c_p, v_b, T_b, T_m); azeotrop 20,2 % / 108,6 °C; gidronium tuzlari [H₃O]Cl 68 %, [H₅O₂]Cl 51 %, [H₇O₃]Cl 41 %, [H₃O]Cl·5H₂O 25 %.',
 '[2] Air Liquide (Gas Encyclopedia), Messer va Cheméo: M = 36,461 g/mol; T_k = 51,4 °C; p_k = 83,1 bar; ρ_k = 450,14 kg/m³; triya nuqtasi 158,96 K / 0,138 bar; gaz zichligi 1,627 kg/m³.',
 '[3] Wikipedia — Hydrochloric acid: ishlab chiqarish (Mannheim: 2NaCl + H₂SO₄ → Na₂SO₄ + 2HCl; H₂ + Cl₂ → 2HCl), Jahon hajmi ≈20 Mt/y (3 Mt/y to‘g‘ridan-to‘g‘ri sintez), pickling (18 % kislota), ion almashinuv, pH nazorati.',
 '[4] OSHA (chemicaldata/620), NIOSH Pocket Guide va IDLH profili (2025-110): OSHA PEL 5 ppm (7 mg/m³) ceiling; NIOSH REL 5 ppm; ACGIH TLV 2,98 ppm; IDLH 50 ppm (2025-yilda 45 ppm).',
 '[5] JACS 1996 (Acidity of HCl in buffered chloroaluminate melts): H₀ = −11,3 (NaCl tizimi) va −12,7 (LiCl tizimi); Adabiyot ma’lumotlari: 1 atm HCl bilan to‘yingan eritmada H₀ ≈ −18; suyuq HF: H₀ = −15,1.',
 '[6] Journal of Cleaner Production (2021), US Patent US20030026746 va Unipa (2022): spray roasting 4FeCl₂ + 4H₂O + O₂ → 2Fe₂O₃ + 8HCl; SPL tarkibi 11–13 % Fe, 2–4 % erkin HCl; tiklangan kislota ≈18 %; 1 t po‘lat: HCl 7,6 kg, Fe 5,8 kg, Cl⁻ 7,4 kg.']

source = (ROOT / 'matn' / '06_03.md').read_text()
sections = []
for raw in source.split('## ')[1:]:
    title, body = raw.split('\n', 1); sections.append((title, body.strip().split('\n\n')))
assert len(sections) == 11
side_notes = json.loads((ROOT / 'matn' / '06_03_yonlavhalar.json').read_text())
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
        band('6.3. HCl — xlorid kislota', PALE, NAVY, 18, True)
    else:
        band('6.3  /  HCl — XLORID KISLOTA', PALE, NAVY, 11, True)
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
            add_equation(p, left, '6.3', counter, runs)
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
        runs(p, 'Barcha grafik, sxema va rasmlar original o‘quv ishlanmalari; sonli egri chiziqlar model hisoblari (o‘lchov ma’lumotlari emas). Rasmlar mikrofoto yoki atom tuzilmasi tasviri emas. Qurilma, texnologik parametrlar, konsentratsiya tanlash, idish materiallari va tibbiy dozalar bo‘yicha amaliyot tavsiyalari berilmaydi; xavfli kislotalar bilan ishlash tartibi 12-bo‘limda.', 8)
        p = right.add_paragraph(); p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3); p.paragraph_format.keep_with_next = True
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
runs(p, '6-BOB   ·   ', 8, False, NAVY)
f = OxmlElement('w:fldSimple'); f.set(qn('w:instr'), 'PAGE'); p._p.append(f)
doc.core_properties.title = 'Noorganik kislotalar · 6.3 · HCl — xlorid kislota'
doc.core_properties.author = ''
OUT.parent.mkdir(parents=True, exist_ok=True); doc.save(OUT)
assert len(doc.inline_shapes) == 17
assert counter == 11
assert comparison_count == 11
assert sum(len(notes) for notes in side_notes) == 22
print(OUT)
print('11 bo‘lim; 11 jadval; 5 hisoblangan grafik; 7 sxema; 5 original illyustratsiya; 11 formula; 22 yon lavha.')
