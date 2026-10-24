#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mundarija uchun maxsus DOCX qurilchi — kitob dizayni bilan.
Chiqish: kitob/chiqish/Noorganik Kislotalar - Mundarija (Loyiha).docx
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chiqish" / "Noorganik Kislotalar - Mundarija (Loyiha).docx"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Ranglar
NAVY = RGBColor(0x0B, 0x2C, 0x4A)
BRONZE = RGBColor(0xC2, 0x8E, 0x3B)
LIGHT_BG = "E8F0F6"
DARK_BG = "0B2C4A"
BRONZE_HEX = "C28E3B"
LIGHT_HEX = "E8F0F6"
WHITE = RGBColor(0xFF,0xFF,0xFF)
GRAPHITE = RGBColor(0x1A,0x1A,0x1A)
GRAY = RGBColor(0x5A,0x5A,0x5A)
LIGHT_GRAY = RGBColor(0x8A,0x8A,0x8A)

def set_page_margins(section, top=2, bottom=2, left=2, right=2, gutter=0.5):
    section.top_margin = Cm(top)
    section.bottom_margin = Cm(bottom)
    section.left_margin = Cm(left)
    section.right_margin = Cm(right)
    section.gutter = Cm(gutter)
    section.header_distance = Cm(1)
    section.footer_distance = Cm(1)

def set_cell_shading(cell, color_hex):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), color_hex)
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_borders(cell, color="0B2C4A", size="6"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), size)
        el.set(qn('w:color'), color)
        el.set(qn('w:space'), '0')
        tcBorders.append(el)
    tcPr.append(tcBorders)

def add_horizontal_line(doc, color_hex=BRONZE_HEX, width_pt=1):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(width_pt*4))
    bottom.set(qn('w:color'), color_hex)
    bottom.set(qn('w:space'), '6')
    pBdr.append(bottom)
    pPr.append(pBdr)
    # ensure paragraph has tiny height
    pPr2 = p._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:after'), '120')
    spacing.set(qn('w:before'), '60')
    pPr2.append(spacing)
    return p

def add_paragraph(doc, text, size=10, bold=False, italic=False, color=GRAPHITE, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, space_before=0, font_name="Calibri", line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    pPr = p._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:after'), str(int(space_after*20)))
    spacing.set(qn('w:before'), str(int(space_before*20)))
    spacing.set(qn('w:line'), str(int(line_spacing*240)))
    spacing.set(qn('w:lineRule'), 'auto')
    pPr.append(spacing)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    run.font.name = font_name
    if font_name == "Calibri":
        rPr = run._r.get_or_add_rPr()
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), 'Calibri')
        rFonts.set(qn('w:hAnsi'), 'Calibri')
        rFonts.set(qn('w:eastAsia'), 'Calibri')
        rPr.append(rFonts)
    return p

def add_mixed_paragraph(doc, segments, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, space_before=0):
    """segments: list of (text, dict{size,bold,italic,color,font_name})"""
    p = doc.add_paragraph()
    p.alignment = align
    pPr = p._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:after'), str(int(space_after*20)))
    spacing.set(qn('w:before'), str(int(space_before*20)))
    pPr.append(spacing)
    for text, style in segments:
        run = p.add_run(text)
        run.font.size = Pt(style.get('size',10))
        run.bold = style.get('bold',False)
        run.italic = style.get('italic',False)
        run.font.color.rgb = style.get('color', GRAPHITE)
        run.font.name = style.get('font','Calibri')
        rPr = run._r.get_or_add_rPr()
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), style.get('font','Calibri'))
        rFonts.set(qn('w:hAnsi'), style.get('font','Calibri'))
        rPr.append(rFonts)
    return p

def add_styled_table(doc, headers, rows, col_widths=None, header_bg=DARK_BG, header_color=WHITE, zebra=True):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    # header
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = header_color
        run.font.name = "Calibri"
        set_cell_shading(hdr_cells[i], header_bg)
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        # padding
        tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m in ['top','bottom','left','right']:
            el = OxmlElement(f'w:{m}')
            el.set(qn('w:w'), '80')
            el.set(qn('w:type'), 'dxa')
            tcMar.append(el)
        tcPr.append(tcMar)
    # body
    for r_idx, row in enumerate(rows):
        cells = table.rows[r_idx+1].cells
        bg = LIGHT_HEX if (zebra and r_idx % 2 == 0) else "FFFFFF"
        for c_idx, val in enumerate(row):
            cells[c_idx].text = ""
            p = cells[c_idx].paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(8.5)
            run.font.name = "Calibri"
            run.font.color.rgb = GRAPHITE if c_idx==0 else RGBColor(0x33,0x33,0x33)
            if c_idx==0:
                run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx>0 else WD_ALIGN_PARAGRAPH.CENTER
            set_cell_shading(cells[c_idx], bg)
            cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            tcPr = cells[c_idx]._tc.get_or_add_tcPr()
            tcMar = OxmlElement('w:tcMar')
            for m in ['top','bottom','left','right']:
                el = OxmlElement(f'w:{m}')
                el.set(qn('w:w'), '60')
                el.set(qn('w:type'), 'dxa')
                tcMar.append(el)
            tcPr.append(tcMar)
    # table borders
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:color'), '0B2C4A')
        el.set(qn('w:space'), '0')
        tblBorders.append(el)
    tblPr.append(tblBorders)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '0')
    tblW.set(qn('w:type'), 'auto')
    tblPr.append(tblW)
    if col_widths:
        tblPr2 = tbl.tblPr
        tblW2 = tblPr2.find(qn('w:tblW'))
        if tblW2 is not None:
            tblW2.set(qn('w:w'), '5000')
            tblW2.set(qn('w:type'), 'pct')
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return table

def add_info_box(doc, title, content, bg_hex=LIGHT_HEX, border_hex=DARK_BG, icon=""):
    # use single-cell table as box
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, bg_hex)
    # left border simulation via shading + inner
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '18')
    left.set(qn('w:color'), border_hex)
    left.set(qn('w:space'), '8')
    tcBorders.append(left)
    for edge in ['top','right','bottom']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:color'), border_hex)
        el.set(qn('w:space'), '4')
        tcBorders.append(el)
    tcPr.append(tcBorders)
    # title
    p1 = cell.paragraphs[0]
    run = p1.add_run(f"{icon}  {title}" if icon else title)
    run.bold = True
    run.font.size = Pt(9.5)
    run.font.color.rgb = NAVY
    run.font.name = "Calibri"
    # content paragraphs
    for line in content:
        p = cell.add_paragraph()
        run = p.add_run(line)
        run.font.size = Pt(9)
        run.font.color.rgb = GRAPHITE
        run.font.name = "Calibri"
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(1)
    # spacing after
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table

def add_chapter_block(doc, number, title, subtitle, sections, visuals, key_concepts=None, practical=None):
    # Chapter header
    p_num = add_paragraph(doc, f"{number:02d}", size=14, bold=True, color=BRONZE, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=1, font_name="Calibri")
    p_num.paragraph_format.space_before = Pt(12)
    p_title = add_paragraph(doc, title, size=13, bold=True, color=NAVY, space_after=2, font_name="Cambria")
    if subtitle:
        add_paragraph(doc, subtitle, size=9, italic=True, color=GRAY, space_after=6, font_name="Calibri")
    add_horizontal_line(doc, BRONZE_HEX, 1)
    # sections list
    for sec in sections:
        add_mixed_paragraph(doc, [
            (sec[0], {'size':9, 'bold':True, 'color':NAVY, 'font':'Calibri'}),
            (f"  —  {sec[1]}", {'size':9, 'bold':False, 'color':GRAPHITE, 'font':'Calibri'})
        ], space_after=3)
    # visuals
    if visuals:
        p = add_paragraph(doc, "Chizmalar va grafiklar:", size=8.5, bold=True, color=BRONZE, space_before=4, space_after=3, font_name="Calibri")
        vis_text = "  •  ".join(visuals)
        add_paragraph(doc, f"▸ {vis_text}", size=8, color=GRAY, space_after=4, font_name="Calibri")
    if key_concepts:
        add_paragraph(doc, f"Kalit tushunchalar: {key_concepts}", size=8, italic=True, color=GRAY, space_after=2, font_name="Calibri")
    if practical:
        add_paragraph(doc, f"Amaliyot: {practical}", size=8, color=RGBColor(0x2E,0x6B,0x3A), space_after=6, font_name="Calibri")
    # small spacer
    add_paragraph(doc, "", size=4, space_after=4)

# ============ BUILD DOCUMENT ============
doc = Document()

# Page setup
section = doc.sections[0]
set_page_margins(section, top=2, bottom=2, left=2.2, right=2, gutter=0.4)
section.page_height = Cm(29.7)
section.page_width = Cm(21)

# Styles
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10)
style.font.color.rgb = GRAPHITE
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.15

for i in [1,2,3]:
    hs = doc.styles[f'Heading {i}']
    hs.font.name = 'Cambria'
    hs.font.color.rgb = NAVY
    hs.font.bold = True

# ============ COVER PAGE ============
# Top bronze line
add_horizontal_line(doc, BRONZE_HEX, 3)

add_paragraph(doc, "JDA KITOBLAR  •  YUQORI KIMYO SERIYASI", size=8, bold=True, color=BRONZE, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16, font_name="Calibri")

add_paragraph(doc, "NOORGANIK", size=28, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, font_name="Cambria")
add_paragraph(doc, "KISLOTALAR", size=28, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6, font_name="Cambria")

add_horizontal_line(doc, BRONZE_HEX, 2)

add_paragraph(doc, "Chuqur ilmiy darslik  •  Nazariya  •  Tuzilish  •  Texnologiya  •  Hayot", size=10, italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, font_name="Calibri")

# Central decorative box
add_info_box(doc,
    "KITOB HAQIDA QISQA",
    [
        "Noorganik kislotalar — umumiy kimyo, analitik kimyo, fizik kimyo, kimyoviy texnologiya va biokimyoning kesishmasidagi markaziy mavzu. Ushbu kitob kislotalarni alohida moddalar to'plami sifatida emas, balki yagona tizim — proton, elektron juftligi, termodinamika va sanoat zanjiri orqali tushuntiradi.",
        "Har bir bob: nazariya → hisob → chizma → tajriba → sanoat → xavfsizlik → masala. Barcha chizmalar kitob uchun maxsus, yagona dizaynda chiziladi."
    ],
    bg_hex="F7F9FC", border_hex=BRONZE_HEX, icon="◆"
)

add_paragraph(doc, "25 bob  •  5 qism  •  7 ilova  •  ~260 sahifa  •  120+ chizma/grafik  •  45 jadval", size=9, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18, font_name="Calibri")

# Author block
add_horizontal_line(doc, "D9D9D9", 1)
add_mixed_paragraph(doc, [
    ("Muallif:  ", {'size':9, 'bold':True, 'color':GRAY, 'font':'Calibri'}),
    ("Diyorbek Jabborov  •  JDA Kimyo Quiz muallifi", {'size':9.5, 'bold':True, 'color':NAVY, 'font':'Cambria'}),
], align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_paragraph(doc, "Toshkent  •  JDA nashriyoti  •  2026", size=8, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, font_name="Calibri")
add_paragraph(doc, "Loyiha bosqichi: MUNDARIJA VA DIZAYN TASDIQI  •  v1.2  •  2026-05-13", size=7, color=LIGHT_GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, font_name="Calibri")

# Footer line
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "www.jdakimyo.uz  •  @jdakimyo_quiz", size=7, color=LIGHT_GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, font_name="Calibri")

# Page break
doc.add_page_break()

# ============ KITOB PASPORTI ============
add_paragraph(doc, "KITOB PASPORTI", size=16, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Ushbu sahifa — kitobning texnik pasporti. Nashriyot, kutubxona va taqrizchi uchun.", size=8, italic=True, color=GRAY, space_after=8, font_name="Calibri")

add_styled_table(doc,
    ["Ko'rsatkich", "Qiymat"],
    [
        ["To'liq nomi", "Noorganik kislotalar — chuqur ilmiy darslik"],
        ["Qisqa nomi", "Noorganik kislotalar"],
        ["Seriya", "JDA Yuqori Kimyo (2-kitob)"],
        ["Tur", "Nazariy darslik + ilmiy manba + amaliy qo'llanma"],
        ["Til", "O'zbekcha (lotin) — atamalar uch tilda: UZ / RU / EN"],
        ["Auditoriya", "Universitet 1–2-kurs, abituriyent-olimpiada, kimyo o'qituvchisi"],
        ["Hajm", "25 bob (5 qism) + 7 ilova  •  ~240–280 sahifa (A4)"],
        ["Vizual", "120+ chizma/grafik/sxema  •  45 jadval  •  25 ta 3D tasvir"],
        ["Har bob", "4–8 sahifa  •  2–4 chizma  •  5 toifada mashqlar  •  xulosa va adabiyot"],
        ["Ilmiy daraja", "Bakalavr + olimpiada chuqurligi, magistraturaga ko'prik"],
        ["Uslub", "Sodda o'zbekcha, aniq ilmiy til — «mumkin» emas, «bo'ladi»"],
        ["Xavfsizlik", "Har amaliy bobda xavfsizlik bloki, piktogrammalar bilan"],
        ["Raqamli", "Har bob QR-kodi — qo'shimcha video/tajriba havolasi"],
        ["Format", "A4, yumshoq/qattiq muqova, rangli ichki blok (ko'k+bronza)"],
    ],
    col_widths=[35,65]
)

add_info_box(doc,
    "NIMA UCHUN AYNAN NOORGANIK KISLOTALAR?",
    [
        "1) Umumiy kimyoning 40% masalasi kislota-asos muvozanatlariga tayanadi.",
        "2) Sanoatning 3 ta tayanch kislotasi (H₂SO₄, HNO₃, H₃PO₄)siz o'g'it, dori, metallurgiya yo'q.",
        "3) Olimpiada va DTM savollarining eng ko'p xato qilinadigan qismi — aynan shu mavzu (pKa, titrlash, oksidlovchilik).",
        "4) O'zbekcha chuqur manba deyarli yo'q — mavjud darsliklar 15-20 sahifada o'tib ketadi. Ushbu kitob bo'shliqni to'ldiradi."
    ],
    bg_hex=LIGHT_HEX, border_hex=DARK_BG, icon="★"
)

add_info_box(doc,
    "QANDAY O'RGANILADI — O'QUVCHIGA YO'RIQNOMA",
    [
        "•  Har bob boshida «Ushbu bobda o'rganasiz» — 4–6 maqsad. Avval shuni o'qing.",
        "•  Formula raqami (masalan (4.2)) — matnda qayta murojaat uchun. Muhim formulalar hoshiyada takrorlanadi.",
        "•  Moviy bloklar — nazariya; sariq — muhim; yashil — maslahat; qizil — diqqat/xavfsizlik.",
        "•  Har bob oxirida 5 toifa mashq: nazariy → hisob → mantiqiy zanjir → laboratoriya → test. Javoblar Ilova C2 da.",
        "•  QR-kodlar orqali tajriba videosi va 3D taxminiy hisobni ko'ring."
    ],
    bg_hex="FFF8E1", border_hex=BRONZE_HEX, icon="☑"
)

# ============ TO'LIQ MUNDARIJA JADVALI ============
add_paragraph(doc, "TO'LIQ MUNDARIJA", size=16, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Barcha 25 bobning qisqa mundarijasi — bir qarashda kitob xaritasi. Batafsil mazmun keyingi sahifalarda qismma-qism ochiladi.", size=8, italic=True, color=GRAY, space_after=6, font_name="Calibri")

add_styled_table(doc,
    ["№", "Bob nomi", "Sahifa*", "Chizma"],
    [
        ["—", "Muqaddima: Kitob haqida, qanday o'rganiladi, xavfsizlikning 5 qoidasi", "7", "—"],
        ["QISM I", "NAZARIY POYDEVOR — KISLOTA NIMA?", "", ""],
        ["1", "Kislota tushunchasining evolyutsiyasi", "9", "3"],
        ["2", "Nomenklatura va tasnif", "17", "3"],
        ["3", "Tuzilish va kimyoviy bog'lanish", "25", "4"],
        ["4", "Termodinamika: kislotalik kuchi nimadan keladi", "35", "4"],
        ["5", "Kinetika va mexanizmlar", "45", "3"],
        ["QISM II", "KISLOTALARNING UMUMIY KIMYOSI", "", ""],
        ["6", "Suvda o'zini tutish: dissotsiatsiya, pH, titrlash", "53", "4"],
        ["7", "Kislota–asos muvozanatlari va tuzlar", "65", "3"],
        ["8", "Oksidlovchi va qaytaruvchi xossalar", "73", "3"],
        ["9", "Qanday olinadi — laboratoriya va sanoat", "83", "3"],
        ["QISM III", "MUHIM KISLOTALARNING YAKKA KIMYOSI (monografiyalar)", "", ""],
        ["10", "Vodorod galogenidlari: HF, HCl, HBr, HI", "95", "4"],
        ["11", "Oltingugurt kislotalari: H₂S, H₂SO₃, H₂SO₄, oleum", "107", "4"],
        ["12", "Azot kislotalari: HNO₃, HNO₂", "123", "4"],
        ["13", "Fosfor kislotalari: H₃PO₄, polifosfatlar", "135", "4"],
        ["14", "Uglerod va kremniy kislotalari: H₂CO₃, HCN, H₄SiO₄", "147", "3"],
        ["15", "Bor va alyuminiy kislotalari: H₃BO₃, HBF₄", "155", "2"],
        ["16", "Galogenlarning kislorodli kislotalari", "161", "2"],
        ["17", "O'tish metallari kislotalari: H₂CrO₄, HMnO₄", "169", "2"],
        ["QISM IV", "SUVSIZ MUHIT VA MAXSUS HOLATLAR", "", ""],
        ["18", "Suvsiz va noan'anaviy muhitda kislotalar", "177", "3"],
        ["19", "Analitik kimyo: aniqlash va o'lchash", "187", "3"],
        ["20", "Biologik va tibbiy ahamiyati", "197", "3"],
        ["QISM V", "AMALIYOT, XAVFSIZLIK VA KELAJAK", "", ""],
        ["21", "Metallar korroziyasi va himoya", "207", "2"],
        ["22", "Ekologiya: kislotali yomg'ir, tuproq, suv", "215", "2"],
        ["23", "Sanoat zavodlari ichidan: 3 ta zavod", "223", "6"],
        ["24", "Xavfsizlik, saqlash, birinchi yordam", "235", "3"],
        ["25", "Kelajak: yangi energetika va materiallar", "245", "3"],
        ["A–C", "Ilovalar: jadvallar, tajribalar, javoblar, glossariy, indeks", "253", "—"],
    ]
)
add_paragraph(doc, "* Sahifalar taxminiy, yakuniy sahifalash dizayn tasdig'idan keyin aniqlanadi. Har bob yangi sahifadan boshlanadi.", size=7, italic=True, color=GRAY, space_after=6, font_name="Calibri")

# ============ QISM I ============
add_paragraph(doc, "QISM I", size=10, bold=True, color=BRONZE, space_after=1, font_name="Calibri")
add_paragraph(doc, "NAZARIY POYDEVOR — KISLOTA NIMA?", size=16, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Maqsad: o'quvchi «kislota» so'zini eshitganda bitta ta'rif emas, 5 ta nazariya xaritasi, ularning chegarasi va qo'llanish joyini ko'z oldiga keltira olsin. Qism oxirida har qanday kislotani tasniflab, nomlab, kuchini oldindan bashorat qila oladi.", size=9, italic=True, color=GRAPHITE, space_after=8, font_name="Calibri")

add_chapter_block(doc, 1, "Kislota tushunchasining evolyutsiyasi", "Acidus dan superkislotagacha — 300 yillik yo'l",
    [
        ("1.1", "Antiq davr va alkimyo: sirka, vitriol moyi, «acidus» etimologiyasi"),
        ("1.2", "Lavuazye xatosi va Devi to'g'rilashi — kislorod emas, vodorod"),
        ("1.3", "Arrenius (1884): suvda H⁺ — kuchi va chegarasi"),
        ("1.4", "Brønsted–Lowry (1923): proton donor/akseptor, konjugat juftliklar"),
        ("1.5", "Lyuis (1923): elektron juftligi, elektrofil/nukleofil tili"),
        ("1.6", "Zamonaviy kengaytmalar: Usanovich, Pearson HSAB, superkislotalar H₀ shkalasi"),
        ("1.7", "Taqqoslash: qaysi nazariya qachon ishlaydi — tanlash algoritmi"),
    ],
    ["Tarixiy timeline (miloddan 2024 superkislotagacha)", "Arrenius–Brønsted–Lyuis Venn diagrammasi", "HSAB jadvali (qattiq/yumshoq kislota-asos)", "H₀ shkalasida superkislotalar zinapoyasi"],
    key_concepts="Arrenius, Brønsted, Lyuis, HSAB, H₀, superkislota, konjugat juftlik",
    practical="Har bir nazariya uchun 1 ta hayotiy misol: oshqozon HCl (Arrenius), NH₄⁺/NH₃ (Brønsted), BF₃ (Lyuis)"
)

add_chapter_block(doc, 2, "Nomenklatura va tasnif", "IUPAC bo'yicha nomlash va 4 o'lchovda tasniflash",
    [
        ("2.1", "IUPAC nomenklaturasi: vodorodli, oksokislotalar, polikislotalar, tio- va perokso-"),
        ("2.2", "Tuzilish bo'yicha: bir/ikki/uch asosli, mono/poli, kislorodsiz/kislorodli"),
        ("2.3", "Kuch bo'yicha: kuchli–o'rta–kuchsiz–juda kuchsiz (pKa chegaralari)"),
        ("2.4", "Barqarorlik: barqaror, beqaror (H₂CO₃), faqat eritmadagi (H₂SO₃)"),
        ("2.5", "Oksidlanish darajasi ↔ kislotalik bog'liqligi (Cl: +1 → +7)"),
        ("2.6", "Amaliy mashq: 20 ta kislotani 4 o'lchovda tasniflash"),
    ],
    ["4 o'lchovli tasnif matritsasi", "Cl oksidlanish qatori grafigi (HClO → HClO₄)", "Nomlash algoritmi blok-sxemasi (qaror daraxti)"],
    key_concepts="IUPAC, asoslilik, oksokislota, polikislota, perokso-, tio-",
    practical="Dorixona yorlig'idan kislota nomini IUPAC ga o'tkazish"
)

add_chapter_block(doc, 3, "Tuzilish va kimyoviy bog'lanish", "Nega H₂SO₄ kuchli, H₂SO₃ kuchsiz?",
    [
        ("3.1", "O–H bog'i: qutblanish, energiya (463 kJ/mol), uzunlik, qisman zaryad"),
        ("3.2", "Markaziy atom: elektronegativlik, radius, oksidlanish darajasi, zaryad zichligi"),
        ("3.3", "Geometriya: VSEPR, gibridlanish — tetraedr SO₄²⁻, piramida SO₃²⁻, trigonal HNO₃"),
        ("3.4", "Rezonans va delokalizatsiya — kuchning 70% sababi"),
        ("3.5", "Vodorod bog'i va assotsiatsiya: HF zanjiri, H₃PO₄ tarmog'i"),
        ("3.6", "Rentgen va neytron difraksiya — real tuzilmalar"),
    ],
    ["O–H energiyasi vs pKa sochilma grafigi", "3D tasvirlar: H₂SO₄, HNO₃, H₃PO₄, HClO₄", "Rezonans tuzilmalari (H₂SO₄ 3 ta, HNO₃ 2 ta)", "HF vodorod zanjiri sxemasi + kristall qatlami"],
    key_concepts="VSEPR, rezonans, delokalizatsiya, vodorod bog'i, gibridlanish",
    practical="Tuzilishdan kuchni bashorat qilish — 5 ta noma'lum kislota"
)

add_chapter_block(doc, 4, "Termodinamika: kislotalik kuchi nimadan keladi", "Ka, pKa va kislotalikning 6 omili",
    [
        ("4.1", "Ka, pKa, α — ta'rif, bog'liqlik, o'lchov shartlari (25 °C, I→0)"),
        ("4.2", "Nega aynan suvda o'lchanadi — gidratatsiya va Le Chatelier"),
        ("4.3", "6 omil: elektronegativlik, o'lcham, zaryad, rezonans, gibridlanish, erituvchi"),
        ("4.4", "Induktiv/mezomer/maydon effektlari — sirka → trixlorsirka misolida"),
        ("4.5", "Hammett tenglamasi (lg K = ρσ) va superkislotalar H₀ shkalasi"),
        ("4.6", "Harorat va ion kuchi ta'siri — Van't Hoff"),
    ],
    ["To'liq pKa shkalasi (HI dan HSbF₆ gacha, rangli)", "HA → H⁺+A⁻ energiya diagrammasi (ΔG, ΔH, TΔS)", "Hammett grafigi (ρ aniqlash)", "pKa vs harorat oilasi egri chiziqlari"],
    key_concepts="Ka, pKa, Hammett σ/ρ, H₀, induktiv effekt, gidratatsiya",
    practical="HF nega kuchsiz, HCl nega kuchli — termodinamik hisob (Born sikli)"
)

add_chapter_block(doc, 5, "Kinetika va mexanizmlar", "Proton — eng chaqqon zarracha",
    [
        ("5.1", "Proton ko'chishi: 10⁻⁹ s, Grotthuss mexanizmi, tunnel effekti"),
        ("5.2", "Kislota katalizi: spetsifik (H⁺) vs umumiy (HA) — Brønsted qonuni"),
        ("5.3", "Neytrallanish: H⁺+OH⁻ → H₂O, ΔH = –55.8 kJ/mol, nega doim emas?"),
        ("5.4", "Oksidlovchi kislota mexanizmi: HNO₃ + Cu (kons. vs suyultirilgan)"),
        ("5.5", "Kislotali gidroliz va almashinish — ester, amid misolida"),
    ],
    ["Grotthuss proton sakrashi animatsion sxema", "Energiya profili (katalizsiz vs kataliz bilan)", "Cu + HNO₃ tajriba sxemasi (2 stakan, farqi)"],
    key_concepts="Grotthuss, kislota katalizi, spetsifik/umumiy, Brønsted qonuni",
    practical="Nima uchun kuchli kislotalar tez, kuchsizlar sekin neytrallaydi?"
)

# ============ QISM II ============
add_paragraph(doc, "QISM II", size=10, bold=True, color=BRONZE, space_after=1, font_name="Calibri")
add_paragraph(doc, "KISLOTALARNING UMUMIY KIMYOSI", size=16, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Maqsad: kislotalarni alohida yodlash emas, umumiy qonuniyatlarni tushunish — dissotsiatsiya, titrlash, oksidlovchilik, olish. Shu 4 bobdan keyin har qanday yangi kislota uchun xossani oldindan aytish mumkin.", size=9, italic=True, color=GRAPHITE, space_after=8, font_name="Calibri")

add_chapter_block(doc, 6, "Suvda o'zini tutish: dissotsiatsiya, pH, titrlash", "pH 0 dan 14 gacha — barcha hisoblar",
    [
        ("6.1", "Bir va ko'p bosqichli dissotsiatsiya: H₂SO₄, H₃PO₄, H₂CO₃, Ka₁/Ka₂/Ka₃"),
        ("6.2", "Kuchli vs kuchsiz: [H⁺] hisoblashning 4 sharti (aniq → taqribiy)"),
        ("6.3", "pH, pOH, ion kuchi, faollik (Debye–Hückel chegarasi)"),
        ("6.4", "Titrlash: 3 tur egri chiziq — kuchli/kuchli, kuchli/kuchsiz, poliprotik"),
        ("6.5", "Indikatorlar: rang o'tish oraliqi, tanlash qoidasi (pKa ±1)"),
        ("6.6", "Buferlar: Henderson–Hasselbalch, sig'im, qon (7.35–7.45) va okean misolida"),
    ],
    ["α vs pH spetsiatsiya diagrammasi (H₃PO₄ 4 egri)", "3 tur titrlash egri chizig'i (bir sahifada taqqos)", "Indikatorlar kamalagi (metiloranj → fenolftalein)", "Bufer sig'imi grafigi + qon buferi sxemasi"],
    key_concepts="Ka₁ Ka₂ Ka₃, pH, ion kuchi, titrlash, indikator, bufer",
    practical="Oshqozon pH 1.5 ni hisoblash — HCl konsentratsiyasi qancha?"
)

add_chapter_block(doc, 7, "Kislota–asos muvozanatlari va tuzlar", "Konjugat juftliklar va gidroliz",
    [
        ("7.1", "Konjugat juftlik: kuchli kislota ↔ kuchsiz asos — teskari proporsionallik"),
        ("7.2", "Gidroliz: kation (NH₄⁺, Fe³⁺) va anion (CO₃²⁻, PO₄³⁻) gidrolizi, Kh = Kw/Ka"),
        ("7.3", "Nordon (NaHSO₄), asosli (Cu₂(OH)₂CO₃) va o'rta tuzlar"),
        ("7.4", "Kompleks hosil qilish: kislota ligand sifatida (masalan, [FeF₆]³⁻)"),
    ],
    ["Konjugat sikli (kislota ↔ asos aylanasi)", "Gidroliz oqim sxemasi", "pH vs tuz turi jadvali (kislotali/neytral/asosli)"],
    key_concepts="Konjugat juftlik, gidroliz konstantasi, nordon tuz, kompleks",
    practical="Nima uchun Na₂CO₃ eritmasi sovun kabi sirpanchiq?"
)

add_chapter_block(doc, 8, "Oksidlovchi va qaytaruvchi xossalar", "Kislota va oksidlovchi — ikki rol bir vaqtda",
    [
        ("8.1", "Oksidlovchilik qatori: HClO₄ > HNO₃ (kons.) > H₂SO₄ (kons.) > H₃PO₄"),
        ("8.2", "Metallar faollik qatori vs kislotalar — kim H₂ chiqaradi, kim NO₂?"),
        ("8.3", "Passivlanish: Fe, Al, Cr da zich oksid parda (nega kons. HNO₃ da erimaydi)"),
        ("8.4", "HF ning alohida xossasi — SiO₂ ni eritishi (shisha «yeyishi»)"),
    ],
    ["Oksidlovchilik kuchi zinapoyasi", "Metall + kislota matritsasi (H₂ / NO₂ / SO₂ / passiv)", "Passiv qatlam kesimi (SEM uslubida)"],
    key_concepts="Oksidlovchi kislota, passivlanish, faollik qatori",
    practical="Temir mix nega suyultirilgan HNO₃ da eriydi, konsentrlanganida yo'q?"
)

add_chapter_block(doc, 9, "Qanday olinadi — laboratoriya va sanoat", "4 usul, 3 tozalash, 1 zavod",
    [
        ("9.1", "4 umumiy usul: tuz+kislota, oksid+suv, to'g'ridan sintez, elektroliz"),
        ("9.2", "Tozalash: oddiy haydash, rektifikatsiya, kristallash, quritish (CaCl₂, H₂SO₄)"),
        ("9.3", "Azeotrop muammosi: HNO₃–H₂O (68%), HCl–H₂O (20%) — qanday sindiriladi"),
        ("9.4", "Sanoat prinsiplari: xomashyo → katalizator → issiqlik → ekologiya"),
    ],
    ["4 usul sxemalari (bir qarashda)", "Azeotrop diagrammalari (qaynash nuqtasi vs tarkib)", "Sanoat blok-sxemasi umumiy andozasi"],
    key_concepts="Azeotrop, rektifikatsiya, kontakt usuli, Ostvald",
    practical="Laboratoriyada HCl olish — NaCl + H₂SO₄ (kons.) tajriba yo'riqnomasi"
)

# ============ QISM III ============
add_paragraph(doc, "QISM III", size=10, bold=True, color=BRONZE, space_after=1, font_name="Calibri")
add_paragraph(doc, "MUHIM NOORGANIK KISLOTALARNING YAKKA KIMYOSI", size=15, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_paragraph(doc, "— Monografiyalar qismi —", size=9, italic=True, color=BRONZE, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=2, font_name="Calibri")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_info_box(doc,
    "BU QISM QANDAY TUZILGAN — HAR BOB BITTA ANDOZA",
    [
        "Har bir bob 7 qadam: 1) Tarixi va nomi → 2) Tuzilishi (Lewis/3D) → 3) Fizik xossalar (jadval) → 4) Olinishi (lab+sanoat) → 5) Kimyoviy xossalar (reaksiyalar) → 6) Qo'llanilishi → 7) Xavfsizligi. Oxirida — taqqoslash jadvali va 5 masala.",
        "Shuning uchun 10-bobni o'qigan o'quvchi 11-bobni mustaqil o'qiy oladi — andoza bir xil."
    ],
    bg_hex="F7F9FC", border_hex=DARK_BG
)

add_chapter_block(doc, 10, "Vodorod galogenidlari: HF, HCl, HBr, HI", "Eng oddiy — eng ayyor",
    [
        ("10.1", "H–X bog'i: energiya HF 565 → HI 295 kJ/mol, lekin kislotalik teskari — nega?"),
        ("10.2", "Fizik anomaliyalar: HF qaynash nuqtasi 19.5 °C (vodorod bog'i zanjiri)"),
        ("10.3", "Olinishi: CaF₂+H₂SO₄ → HF, H₂+Cl₂ → HCl (sanoat sexi)"),
        ("10.4", "Kimyoviy taqqos: kislotalik, qaytaruvchilik (HI eng kuchli qaytaruvchi), kompleks ([AgCl₂]⁻)"),
        ("10.5", "Qo'llanilishi va xavfsizligi: HCl — oshqozon va metall tozalash, HF — shisha o'yish (o'ta zaharli)"),
    ],
    ["H–X bog' energiyasi vs pKa teskari grafigi", "Qaynash nuqtalari anomaliyasi (HF sakrashi)", "HCl sanoat sexi blok-sxemasi", "HF ning SiO₂ ni eritishi — molekulyar sxema"],
    key_concepts="Vodorod bog'i, galogenid, qaytaruvchilik qatori",
    practical="HF nega shisha idishda saqlanmaydi — PTFE da saqlash"
)

add_chapter_block(doc, 11, "Oltingugurt kislotalari oilasi: H₂S, H₂SO₃, H₂SO₄, oleum", "«Kimyo qoni» va uning oilasi",
    [
        ("11.1", "H₂S — kuchsiz, uchuvchan, zaharli kislota (K₁=10⁻⁷) va uning tuzlari"),
        ("11.2", "H₂SO₄ — 3 ta rezonans, 2 ta proton, 5 ta rol: kislota, oksidlovchi, suvsizlantiruvchi, sulfonlovchi, katalizator"),
        ("11.3", "Kontakt usuli: pirit/S → SO₂ → SO₃ (V₂O₅ katalizator) → H₂SO₄ → oleum (to'liq zavod sxemasi)"),
        ("11.4", "Konsentratsiyaga bog'liq xossalar: 10% vs 98% vs oleum — matritsa"),
        ("11.5", "Perokso: H₂S₂O₈ (Karo kislotasi), H₂SO₅ — oksidlovchi bombalar"),
    ],
    ["Kontakt zavodi panoramik sxemasi (3 qavat: kuydirish → kontakt → absorber)", "H₂SO₄ rezonans/delokalizatsiya (3 tuzilma)", "Konsentratsiya–xossa matritsasi (rangli)", "Oleum tarkibi diagrammasi (H₂S₂O₇)"],
    key_concepts="Kontakt usuli, oleum, pirosulfat, perokso-kislota",
    practical="Shakar + kons. H₂SO₄ — suvsizlantirish tajribasi (video QR)"
)

add_chapter_block(doc, 12, "Azot kislotalari: HNO₃, HNO₂", "Oksidlovchi malika",
    [
        ("12.1", "HNO₃ tuzilishi: tekis, ichki H-bog', 2 rezonans, N +5"),
        ("12.2", "Ostvald usuli: NH₃ → NO (Pt-Rh) → NO₂ → HNO₃ (3 bosqich, issiqlik balansi)"),
        ("12.3", "Konsentratsiyaga bog'liq oksidlovchilik: Cu + 4HNO₃(kons.) → NO₂ vs 3Cu + 8HNO₃(suyult.) → NO"),
        ("12.4", "NO⁺ va NO₂⁺ — nitrolashning haqiqiy agenti (H₂SO₄ + HNO₃ → NO₂⁺)"),
        ("12.5", "HNO₂ — beqaror, disproporsiyalanish 3HNO₂ → HNO₃ + 2NO + H₂O, diazotlash"),
    ],
    ["Ostvald zavodi sxemasi (3 reaktor kesimi)", "Cu+HNO₃ tajriba foto-sxemasi (2 kolba, jigarrang NO₂ vs rangsiz NO)", "Nitrolash mexanizmi (NO₂⁺ hujumi)", "N oksidlanish darajasi vs kislota kuchi grafigi"],
    key_concepts="Ostvald, nitrosoniy, nitroniy, nitrolash, disproporsiya",
    practical="Nima uchun HNO₃ da oltin erimaydi, lekin «shoh suvi» (HCl+HNO₃) da eriydi?"
)

add_chapter_block(doc, 13, "Fosfor kislotalari: H₃PO₄, H₄P₂O₇, polifosfatlar", "Kondensatsiya zanjiri — tiriklik asosi",
    [
        ("13.1", "Orto → piro → meta → poli: –H₂O ajralishi zanjiri, P–O–P ko'prik"),
        ("13.2", "Tuzilish: P=O va 3×P–OH, vodorod bog' tarmog'i (qovushqoqlik sababi)"),
        ("13.3", "Olinishi: ekstraksion (apatit+H₂SO₄) vs termik (P₄+O₂+H₂O) — taqqos"),
        ("13.4", "Uch bosqichli dissotsiatsiya (Ka₁≫Ka₂≫Ka₃) va buferligi"),
        ("13.5", "Biologiya: ATF (3 fosfat), DNK fosfodiester, suyak gidroksiapatit Ca₅(PO₄)₃OH"),
    ],
    ["Kondensatsiya zanjiri (4 molekula animatsion)", "Fosfatlar oilasi daraxti (6 a'zo)", "pH vs spetsiatsiya (H₃PO₄ → PO₄³⁻)", "ATF da fosfat bog'i va energiya (30.5 kJ/mol)"],
    key_concepts="Kondensatsiya, polifosfat, metafosfat, gidroksiapatit, ATF",
    practical="Kola ichimligida H₃PO₄ — nega qo'shiladi, qancha?"
)

add_chapter_block(doc, 14, "Uglerod va kremniy kislotalari: H₂CO₃, HCN, H₄SiO₄", "Mavjud va yo'q kislotalar",
    [
        ("14.1", "H₂CO₃ — borliq bahsi: CO₂+H₂O ⇌ H₂CO₃ (K=1.7×10⁻³), lekin erkin ajratilmaydi"),
        ("14.2", "Karbonat buferi: qon (HCO₃⁻/CO₂) va okean (pH 8.1 → 7.9 atsidozlashish)"),
        ("14.3", "HCN — kuchsiz (pKa 9.2) lekin o'ta zaharli, KCN dan olinishi"),
        ("14.4", "H₄SiO₄ va polimerlanishi: monomer → dimer → silikagel → kvars (Si–O–Si)"),
    ],
    ["CO₂–H₂O–HCO₃⁻–CO₃²⁻ muvozanat diagrammasi", "Okean pH pasayish grafigi (1950→2050 prognoz)", "Silikat polimerlanish zanjiri (4 bosqich)"],
    key_concepts="Karbonat, sianid, silikat, polimerlanish, karbonat buferi",
    practical="Nima uchun gazlangan suv nordon?"
)

add_chapter_block(doc, 15, "Bor va alyuminiy kislotalari: H₃BO₃, HBF₄", "Lyuis kislotasi niqobida",
    [
        ("15.1", "H₃BO₃ — Brønsted emas, Lyuis: B(OH)₃ + H₂O → [B(OH)₄]⁻ + H⁺ (pKa 9.2)"),
        ("15.2", "Poliborlar: tetraborat [B₄O₅(OH)₄]²⁻ — boraks"),
        ("15.3", "HBF₄ — kuchli, superkislotalarga o'tish ko'prigi"),
    ],
    ["B(OH)₃ qatlamli tuzilishi (vodorod bog'i tarmog'i)", "Lyuis kislotaligi sxemasi (B + H₂O)"],
    key_concepts="Lyuis kislotasi, tetrahidroksoborat, boraks",
    practical="Bor kislota — antiseptik va olovga qarshi"
)

add_chapter_block(doc, 16, "Galogenlarning kislorodli kislotalari", "Beqarordan portlovchigacha",
    [
        ("16.1", "Qoidasi: oksidlanish darajasi ↑ → kislotalik ↑ va oksidlovchilik ↑ (HClO pKa 7.5 → HClO₄ pKa –10)"),
        ("16.2", "Xlor qatori: HClO (oqartiruvchi) → HClO₂ → HClO₃ → HClO₄ (raketa yoqilg'isi, portlovchi)"),
        ("16.3", "Brom va yod: HBrO₃, HIO₃, H₅IO₆ (ortoyod kislota — oktaedr!)"),
        ("16.4", "Olinishi: Cl₂ + H₂O → HClO + HCl, KClO₄ dan HClO₄"),
    ],
    ["Cl kislotalari zinapoyasi (pKa va E° birga)", "Termik barqarorlik grafigi (HClO < HClO₄)"],
    key_concepts="Oksokislota, perxlorat, periodat, orto-kislota",
    practical="Oqartiruvchi (NaClO) nega kislotali muhitda kuchliroq?"
)

add_chapter_block(doc, 17, "O'tish metallari kislotalari: H₂CrO₄, HMnO₄", "Kislota + oksidlovchi 2in1",
    [
        ("17.1", "Xrom: H₂CrO₄ ⇌ H₂Cr₂O₇, pH ga bog'liq muvozanat (sariq CrO₄²⁻ ↔ to'q sariq Cr₂O₇²⁻)"),
        ("17.2", "Marganets: HMnO₄ — binafsha, o'ta kuchli oksidlovchi, erkin holda portlovchi (Mn₂O₇)"),
        ("17.3", "Nega sof holda ajratilmaydi — konsentrlanganda parchalanish"),
    ],
    ["CrO₄²⁻ ⇌ Cr₂O₇²⁻ rang shkalasi (pH 2→12)", "Mn oksidlanish holatlari E–pH diagrammasi (Pourbaix)"],
    key_concepts="Xromat/dixromat, permanganat, Pourbaix",
    practical="Dixromat bilan spirtni aniqlash — alkomat qanday ishlaydi?"
)

# ============ QISM IV ============
add_paragraph(doc, "QISM IV", size=10, bold=True, color=BRONZE, space_after=1, font_name="Calibri")
add_paragraph(doc, "SUVSIZ MUHIT VA MAXSUS HOLATLAR", size=16, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Maqsad: kislota faqat suvdagi H⁺ emasligini ko'rsatish — suvsiz, qattiq, gaz fazadagi kislotalar va ularni o'lchash.", size=9, italic=True, color=GRAPHITE, space_after=8, font_name="Calibri")

add_chapter_block(doc, 18, "Suvsiz va noan'anaviy muhitda kislotalar", "Suvsiz ham kislota bo'ladi",
    [
        ("18.1", "Erituvchi-sistema: suvsiz H₂SO₄, HF, CH₃COOH, suyuq NH₃, SO₂ da avtoprotoliz"),
        ("18.2", "Superkislotalar: FSO₃H·SbF₅ («sehrli kislota» H₀=–23), HF·SbF₅ (H₀=–28) — alkanlarni protonlaydi"),
        ("18.3", "Qattiq kislotalar: seolit H-ZSM-5, sulfatlangan ZrO₂ — neft krekingi"),
        ("18.4", "Gaz faza: proton affinligi (PA), eng kuchli gaz kislotasi — H(CHB₁₁Cl₁₁)"),
    ],
    ["Superkislotalar kuchi shkalasi (H₂SO₄ dan HSbF₆ gacha, 10¹⁵ marta)", "Seolit g'ovagi taxminiy hisobi (kanallar kesimi)", "Hammett H₀ o'lchash sxemasi"],
    key_concepts="Superkislota, Hammett H₀, seolit, proton affinligi",
    practical="Superkislota plastik idishni eritadimi — PTFE nega chidaydi?"
)

add_chapter_block(doc, 19, "Analitik kimyo: aniqlash va o'lchash", "Kislotani qanday ushlaymiz",
    [
        ("19.1", "Klassik: titrlash (kislota-asos), gravimetriya (SO₄²⁻ → BaSO₄)"),
        ("19.2", "Zamonaviy: pH-metr (shisha elektrod), konduktometriya, ISE, NMR (¹H, ³¹P), IK"),
        ("19.3", "Spektroskopik «barmoq izi»: sulfat 1100 cm⁻¹, nitrat 1380 cm⁻¹, fosfat 1050 cm⁻¹ (IK)"),
    ],
    ["pH-metr ishlash sxemasi (shisha membrana kesimi)", "IK-spektrlar paneli (4 kislota anionlari)", "NMR kimyoviy siljish jadvali (³¹P)"],
    key_concepts="pH-metriya, ISE, gravimetriya, IK, NMR",
    practical="Laboratoriyada noma'lum kislotani 3 qadamda aniqlash"
)

add_chapter_block(doc, 20, "Biologik va tibbiy ahamiyati", "pH 1.5 da hayot",
    [
        ("20.1", "Oshqozon HCl: parietal hujayra H⁺/K⁺-ATPaza, pH 1.5–2, himoya shilliq qavati"),
        ("20.2", "Qon buferlari: bikarbonat (HCO₃⁻/CO₂), fosfat, oqsil — atsidoz/alkaloz (pH 7.35–7.45 dan chiqsa o'lim)"),
        ("20.3", "Suyak/tish: gidroksiapatit, DNK fosfodiester skeleti, ATF energiyasi"),
        ("20.4", "Dori: H₃BO₃ (antiseptik), Al(OH)₃ + kislota (antatsid)"),
    ],
    ["Oshqozon devori kesimi (parietal hujayra sxemasi)", "Qon buferi sikli (3 tizim)", "Suyak mineralizatsiyasi (kollagen + apatit)"],
    key_concepts="Atsidoz, bufer sig'imi, gidroksiapatit, fosfodiester",
    practical="Antatsid tabletkasi qancha HCl ni neytrallaydi — hisob"
)

# ============ QISM V ============
add_paragraph(doc, "QISM V", size=10, bold=True, color=BRONZE, space_after=1, font_name="Calibri")
add_paragraph(doc, "AMALIYOT, XAVFSIZLIK VA KELAJAK", size=16, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Maqsad: kitobni laboratoriyadan zavodga, zavoddan sayyoraga olib chiqish — kislotalar atrofimizda.", size=9, italic=True, color=GRAPHITE, space_after=8, font_name="Calibri")

add_chapter_block(doc, 21, "Metallar korroziyasi va himoya", "Kislota metallni yeyishi",
    [
        ("21.1", "Elektrokimyoviy korroziya: anod (Fe → Fe²⁺) + katod (2H⁺ → H₂) — pH ta'siri"),
        ("21.2", "Inhibitorlar: organik (benzotriazol), noorganik (xromat, fosfat) — sirtni qoplash"),
        ("21.3", "Passiv qoplamalar: ruxlash, xromlash, fosfatlash, polimer"),
    ],
    ["Korroziya elektrokimyoviy sxemasi (mikroelement)", "Inhibitor ta'siri diagrammasi (tezlik vs konsentratsiya)"],
    key_concepts="Korroziya, inhibitor, passivlanish, galvanik juft",
    practical="Nima uchun zanglagan mixni HCl da tozalash mumkin, H₂SO₄(kons.) da yo'q?"
)

add_chapter_block(doc, 22, "Ekologiya: kislotali yomg'ir, tuproq, suv", "Havodan yomg'irgacha",
    [
        ("22.1", "Atmosfera: SO₂ + OH· → H₂SO₄, NO₂ + OH· → HNO₃ — yomg'ir pH 5.6 → 4.2"),
        ("22.2", "Tuproq: pH 4.5 da Al³⁺ ajraladi — ildiz zaharlanishi, ohaklash (CaCO₃)"),
        ("22.3", "Okean: CO₂ + H₂O → H₂CO₃ → pH 8.1 → 7.9 (marjonlar erishi)"),
    ],
    ["Kislotali yomg'ir sikli (zavod → bulut → yomg'ir → o'rmon/ko'l)", "pH vs hosildorlik grafigi (bug'doy, kartoshka)", "Okean pH pasayish prognozi 2100 gacha"],
    key_concepts="Kislotali yomg'ir, atsidozlashish, ohaklash",
    practical="Yomg'ir pH sini uyda o'lchash — indikator qog'ozi bilan"
)

add_chapter_block(doc, 23, "Sanoat zavodlari ichidan: 3 ta zavod", "Qozondan tanker-gacha",
    [
        ("23.1", "H₂SO₄ zavodi (kontakt): pirit → SO₂ → SO₃ (4 qatlamli kontakt) → 98% + oleum"),
        ("23.2", "HNO₃ zavodi (Ostvald): NH₃ + havo (Pt-Rh to'r) → NO → NO₂ → 60% HNO₃ (absorber)"),
        ("23.3", "H₃PO₄ va o'g'itlar: apatit + H₂SO₄ → H₃PO₄ → ammofos, superfosfat"),
        ("23.4", "Iqtisodiyot va ekologiya: xomashyo, energiya, chiqindi (fosfogips, NOₓ)"),
    ],
    ["H₂SO₄ zavodi panoramasi (blok-sxema + absorber kesimi)", "HNO₃ Ostvald apparati (Pt to'r mikrofotosxemasi)", "H₃PO₄ ekstraksion liniyasi", "3 zavod iqtisodiy taqqos jadvali"],
    key_concepts="Kontakt apparati, Ostvald, absorber, fosfogips",
    practical="1 tonna H₂SO₄ uchun qancha pirit va suv kerak — texnik hisob"
)

add_chapter_block(doc, 24, "Xavfsizlik, saqlash, birinchi yordam", "Kislota kechirmaydi",
    [
        ("24.1", "15 oltin qoida: ko'zoynak → qo'lqop → xalat → suv → kislota (hech qachon aksincha emas!)"),
        ("24.2", "Saqlash mosligi: HF — PTFE, HCl — shisha/PE, H₂SO₄ — po'lat 316L, HNO₃ — alyuminiy (passiv)"),
        ("24.3", "To'kilish algoritmi: ogohlantir → ventilyatsiya → neytralla (Na₂CO₃) → yuv → hisobot"),
        ("24.4", "Kuyishda: 15 daqiqa oqim suv, ko'z — 20 daqiqa, shifokor; HF — kalsiy glyukonat geli"),
        ("24.5", "Chiqindi: neytrallash pH 6–8 gacha, suyultirish, litsenziyali utilizatsiya"),
    ],
    ["Xavfsizlik piktogrammalari (GHS, 8 ta)", "To'kilish algoritmi blok-sxemasi (qaror daraxti)", "Saqlash moslik matritsasi (kislota vs material, yashil/qizil)"],
    key_concepts="GHS, PTFE, neytrallash, kalsiy glyukonat",
    practical="Laboratoriya kundaligi: xavfsizlik tekshiruv varaqasi (checklist)"
)

add_chapter_block(doc, 25, "Kelajak: yangi energetika va materiallar", "Ertangi kislotalar",
    [
        ("25.1", "Yonilg'i elementi: Nafion proton-membranasi ( –SO₃H guruhi) — H₂ + ½O₂ → H₂O + tok"),
        ("25.2", "Akkumulyator: qo'rg'oshin-kislotali (Pb + H₂SO₄) va vanadiyli oqimli (V²⁺/V⁵⁺ + H₂SO₄)"),
        ("25.3", "CO₂ ushlash: amin + CO₂ → karbamat + kislota bilan regeneratsiya"),
        ("25.4", "Yashil kimyo: bio-H₂SO₄, qayta tiklanuvchi fosfat, chiqindisiz texnologiya"),
    ],
    ["PEM yonilg'i elementi kesimi (Nafion membranasi)", "Qo'rg'oshin-kislotali akkumulyator sikli (zaryad/razryad)", "CO₂ sikli (ushlash → aylantirish → yoqilg'i)"],
    key_concepts="Nafion, oqimli akkumulyator, yashil kimyo, dekarbonizatsiya",
    practical="Nima uchun elektromobil akkumulyatorida ham kislota bor?"
)

# ============ ILOVALAR ============
add_paragraph(doc, "ILOVALAR", size=16, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Kitobning ishchi qismi — har bob shu yerga tayanadi. O'qish shart emas, izlash uchun.", size=8, italic=True, color=GRAY, space_after=8, font_name="Calibri")

add_styled_table(doc,
    ["Ilova", "Nomi", "Nima bor"],
    [
        ["A1", "Asosiy kislotalar jadvali", "30 ta kislota: formula, tuzilish, pKa, zichlik, qaynash/suyuqlanish, LD₅₀"],
        ["A2", "Kuch qatori", "Kuchli → kuchsiz (suvda va gaz fazada), rangli shkala"],
        ["A3", "Suvsiz shkalalar", "Hammett H₀, Gutmann AN/DN, superkislotalar taqqosi"],
        ["B1", "Termodinamika", "ΔH°, ΔG°, S° — 25 ta kislota va ularning anionlari"],
        ["B2", "Spektrlar", "IK (400–4000 cm⁻¹) va NMR (¹H, ³¹P) «barmoq izlari»"],
        ["C1", "8 ta laboratoriya ishi", "Tajriba yo'riqnomasi: maqsad → reaktiv → xavfsizlik → hisobot andozasi"],
        ["C2", "Masalalar javoblari", "125 masala javobi (qisqa yechim, yakuniy javob)"],
        ["C3", "Glossariy (UZ/RU/EN)", "180 ta atama uch tilda: kislota — кислота — acid"],
        ["C4", "Indeks va adabiyotlar", "Mavzuli indeks + 60 ta manba (kitob, maqola, standart)"],
    ]
)

# ============ CHIZMA DASTURI ============
add_paragraph(doc, "CHIZMA VA GRAFIKLAR DASTURI", size=16, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Har bir chizma kitob uchun maxsus yaratiladi — yagona uslub, o'zbekcha izoh, chop etishga tayyor (300 dpi). Quyida to'liq reja.", size=8, italic=True, color=GRAY, space_after=6, font_name="Calibri")

add_styled_table(doc,
    ["Turi", "Soni", "Uslub", "Misollar"],
    [
        ["Tuzilish & Lewis", "~40", "Ko'k bog'lar, qizil O, sariq S, yashil N, oq fon", "H₂SO₄ (3 rezonans), HNO₃, HClO₄, H₃PO₄ zanjiri"],
        ["3D tasvirlar", "~20", "Shaffof sferalar, yumshoq soya, 30° perspektiva", "SO₄ tetraedr, PO₄, SiO₆ oktaedr, HF zanjiri"],
        ["Grafiklar", "~35", "Ko'k chiziq, bronza aksent, och kulrang panjara", "pKa shkalasi, titrlash, korroziya, Hammett"],
        ["Blok-sxemalar", "~18", "Yumaloq to'rtburchak, bronza strelka, ko'k ramka", "Kontakt usuli, Ostvald, fosfat ekstraksiyasi"],
        ["Jadvallar", "~45", "Ko'k sarlavha, zebra qator, yupqa chegara", "Tasnif, taqqoslash, termodinamika, xavfsizlik"],
        ["Foto/ilustratsiya", "~15", "Akvarel+foto aralash, o'zbekcha izoh", "Korroziya, zavod apparati, oshqozon kesimi"],
        ["JAMI", "~173", "Yagona dizayn tizimi", "Har bob o'rtacha 7 ta vizual"],
    ]
)

add_info_box(doc,
    "CHIZMA NAMUNASI — QANDAY KO'RINADI",
    [
        "•  Barcha formulalar Wordda yoziladi (H₂SO₄, SO₄²⁻) — rastr emas, masshtab buzilmaydi.",
        "•  3D tasvirlar — maxsus dasturda (Avogadro/VESTA uslubida) render qilinadi, keyin Wordga joylanadi.",
        "•  Grafiklar — toza chiziqli, raqamlar o'zbekcha (1,5 emas 1.5 — xalqaro standart).",
        "•  Har rasm ostida: «1.3-rasm. H₂SO₄ ning rezonans tuzilmalari» va kerak bo'lsa manba (masalan: «Rentgen ma'lumoti: Smith, 2019»)."
    ],
    bg_hex="F7F9FC", border_hex=BRONZE_HEX, icon="✎"
)

# ============ HAR BOB ANDOZASI ============
add_paragraph(doc, "HAR BIR BOBNING ICHKI ANDOZASI", size=14, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 1)
add_paragraph(doc, "25 bob bir xil tuzilma — o'quvchi 2-bobdan keyin avtomat o'rganadi.", size=8, italic=True, color=GRAY, space_after=6, font_name="Calibri")

add_styled_table(doc,
    ["Blok", "Hajm", "Nima bor"],
    [
        ["Epigraf / Kirish savoli", "½ sahifa", "O'ylatadigan muammo yoki tarixiy iqtibos. Masalan: «Nima uchun HF shishani yeydi, HCl esa yo'q?»"],
        ["Maqsadlar", "¼ sahifa", "«Ushbu bobda o'rganasiz» — 4–6 punkt (ko'k ramkali blok)"],
        ["Nazariya", "2–3 sahifa", "Tushuncha, formula (raqamli), jadval, eslatma bloklari"],
        ["Chuqur tahlil", "1 sahifa", "1–2 ta batafsil misol: hisob + grafik (masalan: Born sikli bilan HF anomaliyasi)"],
        ["Rasmlar paneli", "1 sahifa", "2–4 ta chizma/grafik/sxema — katta, izohli"],
        ["Amaliyot", "½ sahifa", "Sanoat / tabiat / organizm bilan bog'lash (1 hayotiy misol)"],
        ["Mashqlar", "1 sahifa", "5 toifa: nazariy savol, hisob, mantiqiy zanjir, laboratoriya, test (4 variant)"],
        ["Xulosa", "½ sahifa", "6–8 tayanch ibora (bronza nuqtalar bilan)"],
        ["Adabiyot", "¼ sahifa", "3–5 manba (kitob, maqola, standart) + QR-kod"],
    ]
)

add_info_box(doc,
    "MASHQLAR 5 TOIFASI — HAR BOBDA",
    [
        "1) Nazariy savol — ta'rifni qayta aytish emas, tushuntirish (masalan: «Nega H₂SO₄ da 2 ta pKa bor, HCl da 1 ta?»)",
        "2) Hisob — pH, Ka, titrlash, muvozanat (qadam-baqadam javob ilovada)",
        "3) Mantiqiy zanjir — A → B → C reaksiyalar zanjiri (olimpiada uslubi)",
        "4) Laboratoriya — uyda yoki maktabda bajariladigan tajriba (xavfsizlik bilan)",
        "5) Test — 4 variantli, 1 to'g'ri (DTM uslubi, izohli)"
    ],
    bg_hex="FFF8E1", border_hex=BRONZE_HEX
)

# ============ DIZAYN ============
add_paragraph(doc, "KITOB DIZAYNI — O'Z USLUBI", size=16, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 2)
add_paragraph(doc, "Kitobning yuzini belgilovchi dizayn tizimi — muqovadan to oxirgi sahifagacha bir xil.", size=8, italic=True, color=GRAY, space_after=6, font_name="Calibri")

add_styled_table(doc,
    ["Element", "Qanday ko'rinadi", "Kod"],
    [
        ["Ranglar", "Chuqur ko'k (asosiy) + bronza (aksent) + och ko'k (fon)", "#0B2C4A / #C28E3B / #E8F0F6"],
        ["Sarlavhalar", "Cambria Bold, ko'k, chap chiziqli", "18 pt / 14 pt / 11 pt"],
        ["Matn", "Times New Roman / Calibri, 11 pt, 1.15 interval", "Grafit #1A1A1A"],
        ["Formulalar", "Cambria Math, markazda, raqami o'ngda (4.2)", "LaTeX → Word"],
        ["Jadvallar", "Ko'k sarlavha, zebra qator, yupqa chegara", "Har jadvalda «1.2-jadval. Nomi»"],
        ["Rasmlar", "85% eni, markazda, ostida «1.3-rasm. Nomi»", "300 dpi, o'zbekcha izoh"],
        ["Bloklar", "Eslatma (ko'k), Muhim (sariq), Diqqat (qizil)", "Chapda qalin rangli chiziq"],
        ["Kolontitul", "Yuqorida bob nomi (kulrang), pastda sahifa (bronza chiziq ustida)", "Har sahifada"],
        ["Muqova", "Variant A: oq fonda H₂SO₄ tetraedri + davriy jadval xirasi", "Variant B/C ham mavjud"],
    ]
)

add_info_box(doc,
    "MUQOVA 3 VARIANTI — TANLANG",
    [
        "A) LABORATORIYA (tavsiya): Oq fonda markazda H₂SO₄ tetraedr 3D, orqada xira davriy jadval. Yuqorida bronza chiziq, pastda muallif. Ilmiy, toza, ishonchli.",
        "B) SANOAT: To'q ko'k fonda oq chiziqli zavod blok-sxemasi (kontakt apparati kesimi). Sarlavha oq, kuchli, texnologik.",
        "C) MINIMAL: Toza oq, faqat tipografika — katta sarlavha, ingichka bronza chiziqlar, burchaklarda molekula piktogrammalari. Premium, adabiy.",
        "→ Siz bittasini tanlaysiz, qolganini moslashtiraman. Hozir A asosida ishlaymiz."
    ],
    bg_hex="F7F9FC", border_hex=DARK_BG, icon="◆"
)

# ============ ISH REJASI ============
add_paragraph(doc, "KEYINGI QADAMLAR — QISMA-QISM ISH REJASI", size=14, bold=True, color=NAVY, space_after=2, font_name="Cambria")
add_horizontal_line(doc, BRONZE_HEX, 1)

add_styled_table(doc,
    ["Bosqich", "Nima qilinadi", "Muddat*", "Natija"],
    [
        ["1", "Mundarija va dizayn tasdig'i (hozir)", "1–2 kun", "Tasdiqlangan mundarija + muqova varianti"],
        ["2", "Qism I (1–5-bob) yozish", "Har bob 2–3 kun", "Matn + 15 chizma + DOCX yangilanishi"],
        ["3", "Qism II (6–9-bob)", "Har bob 2–3 kun", "Matn + 13 chizma + DOCX"],
        ["4", "Qism III (10–17-bob) — eng katta", "Har bob 3–4 kun", "Matn + 30 chizma + zavod sxemalari"],
        ["5", "Qism IV–V (18–25-bob)", "Har bob 2–3 kun", "Matn + 25 chizma + xavfsizlik plakatlari"],
        ["6", "Ilovalar va yakuniy tahrir", "1 hafta", "Glossariy, indeks, adabiyotlar, orfografiya"],
        ["7", "Chop etishga tayyorlash", "3–5 kun", "Yakuniy DOCX + PDF, bosmaxona talablari"],
    ]
)
add_paragraph(doc, "* Muddat taxminiy — har bob siz o'qib, izoh berganingizdan keyin keyingisiga o'tiladi. Qisma-qism, shoshilmasdan, chuqur.", size=7, italic=True, color=GRAY, space_after=6, font_name="Calibri")

add_info_box(doc,
    "SIZDAN KUTILAYOTGAN 3 TA QAROR",
    [
        "1) Mundarija ma'qulmi? Bob qo'shish/olib tashlash, tartibni o'zgartirish kerakmi?",
        "2) Muqova varianti: A / B / C — qaysi biri?",
        "3) Rang palitrasi yoqdimi yoki boshqa rang (masalan, yashil-kimyo, qora-oltin) xohlaysizmi?",
        "Shularni aytsangiz, darhol 1-bobni yozishga kirishaman — matn + 3 ta chizma (timeline, Venn, HSAB) bilan."
    ],
    bg_hex=LIGHT_HEX, border_hex=BRONZE_HEX, icon="✉"
)

add_paragraph(doc, "Taklif va savollar uchun:  @jdakimyo_quiz  •  d.jabborov@jdakimyo.uz  •  +998 ...", size=7, color=LIGHT_GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, font_name="Calibri")
add_paragraph(doc, "© 2026 Diyorbek Jabborov / JDA nashriyoti. Barcha huquqlar himoyalangan. Loyiha hujjati — chop etilmaydi.", size=7, italic=True, color=LIGHT_GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, font_name="Calibri")

# Footer for all sections - add page numbers via footer
for section in doc.sections:
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # bronze line above footer (simulated via bottom border)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '6')
    top.set(qn('w:color'), BRONZE_HEX)
    top.set(qn('w:space'), '4')
    pBdr.append(top)
    pPr.append(pBdr)
    run = p.add_run("Noorganik kislotalar  •  Mundarija loyihasi  •  JDA nashriyoti  •  2026")
    run.font.size = Pt(7)
    run.font.color.rgb = GRAY
    run.font.name = "Calibri"
    run.italic = True

# Header
for section in doc.sections:
    header = section.header
    header.is_linked_to_previous = False
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("NOORGANIK KISLOTALAR  —  MUNDARIJA LOYIHASI  v1.2")
    run.font.size = Pt(7)
    run.font.color.rgb = GRAY
    run.font.name = "Calibri"
    run.italic = True

# Save
doc.save(str(OUT))
print(f"Saved: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
