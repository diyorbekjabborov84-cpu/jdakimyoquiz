#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Klassik mundarija — sodda, toza, imlosi tekshirilgan.
Chiqish: kitob/chiqish/Noorganik Kislotalar - Mundarija (klassik).docx
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chiqish" / "Noorganik Kislotalar - Mundarija (klassik).docx"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = RGBColor(0x1A,0x2E,0x4A)
BRONZE = RGBColor(0x8C,0x6A,0x2A)
GRAY = RGBColor(0x4A,0x4A,0x4A)
LIGHT = RGBColor(0x6B,0x6B,0x6B)
BLACK = RGBColor(0x1A,0x1A,0x1A)

def set_margins(sec):
    sec.top_margin = Cm(2)
    sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2)
    sec.header_distance = Cm(1.2)
    sec.footer_distance = Cm(1)

def add_para(doc, text, size=10, bold=False, italic=False, color=BLACK, align=WD_ALIGN_PARAGRAPH.LEFT, after=4, before=0, font="Times New Roman", caps=False, spacing=1.0):
    p = doc.add_paragraph()
    p.alignment = align
    if before or after:
        pf = p.paragraph_format
        pf.space_before = Pt(before)
        pf.space_after = Pt(after)
        pf.line_spacing = spacing
        pf.widow_control = True
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    if caps:
        rPr = run._r.get_or_add_rPr()
        caps_el = OxmlElement('w:caps')
        caps_el.set(qn('w:val'), 'true')
        rPr.append(caps_el)
    # ensure font applied
    rPr = run._r.get_or_add_rPr()
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), font)
    rf.set(qn('w:hAnsi'), font)
    rf.set(qn('w:eastAsia'), font)
    rPr.append(rf)
    return p

def add_rule(doc, width=6, color="8C6A2A"):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:color'), color)
    bottom.set(qn('w:space'), '4')
    pBdr.append(bottom)
    pPr.append(pBdr)
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(8)
    return p

def add_toc_entry(doc, num, title, page, is_part=False, is_intro=False):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    # tab stop with dot leader at ~16cm
    tabs = OxmlElement('w:tabs')
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), 'right')
    tab.set(qn('w:leader'), 'dot')
    tab.set(qn('w:pos'), '9350')  # ~16.5cm
    tabs.append(tab)
    pPr.append(tabs)
    # spacing
    pf = p.paragraph_format
    pf.space_before = Pt(2 if not is_part else 8)
    pf.space_after = Pt(2 if not is_part else 4)
    pf.line_spacing = 1.0

    if is_part:
        run1 = p.add_run(f"{num}\t")
        run1.font.size = Pt(9)
        run1.bold = True
        run1.font.color.rgb = NAVY
        run1.font.name = "Times New Roman"
        run2 = p.add_run(title)
        run2.font.size = Pt(10)
        run2.bold = True
        run2.font.color.rgb = NAVY
        run2.font.name = "Times New Roman"
        # page on same line right
        run3 = p.add_run(f"\t{page}")
        run3.font.size = Pt(9)
        run3.bold = True
        run3.font.color.rgb = NAVY
        run3.font.name = "Times New Roman"
    else:
        # number
        if num:
            r = p.add_run(f"{num}  ")
            r.font.size = Pt(9.5)
            r.font.color.rgb = BLACK
            r.font.name = "Times New Roman"
        # title with tab then page
        r2 = p.add_run(title)
        r2.font.size = Pt(9.5)
        r2.italic = is_intro
        r2.font.color.rgb = BLACK if not is_intro else GRAY
        r2.font.name = "Times New Roman"
        r3 = p.add_run(f"\t{page}")
        r3.font.size = Pt(9)
        r3.font.color.rgb = GRAY
        r3.font.name = "Times New Roman"
        if is_intro:
            r2.italic = True
    # fix fonts
    for run in p.runs:
        rPr = run._r.get_or_add_rPr()
        rf = OxmlElement('w:rFonts')
        rf.set(qn('w:ascii'), 'Times New Roman')
        rf.set(qn('w:hAnsi'), 'Times New Roman')
        rPr.append(rf)
    return p

def add_chapter_title(doc, number, title, subtitle=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    r1 = p.add_run(f"{number}.  ")
    r1.font.size = Pt(11)
    r1.bold = True
    r1.font.color.rgb = NAVY
    r1.font.name = "Times New Roman"
    r2 = p.add_run(title)
    r2.font.size = Pt(11)
    r2.bold = True
    r2.font.color.rgb = BLACK
    r2.font.name = "Times New Roman"
    for r in [r1,r2]:
        rPr = r._r.get_or_add_rPr()
        rf = OxmlElement('w:rFonts')
        rf.set(qn('w:ascii'), 'Times New Roman')
        rf.set(qn('w:hAnsi'), 'Times New Roman')
        rPr.append(rf)
    if subtitle:
        p2 = doc.add_paragraph()
        p2.paragraph_format.space_before = Pt(1)
        p2.paragraph_format.space_after = Pt(4)
        p2.paragraph_format.left_indent = Cm(0.8)
        r = p2.add_run(subtitle)
        r.font.size = Pt(8.5)
        r.italic = True
        r.font.color.rgb = LIGHT if False else GRAY
        r.font.name = "Times New Roman"
        rPr = r._r.get_or_add_rPr()
        rf = OxmlElement('w:rFonts')
        rf.set(qn('w:ascii'), 'Times New Roman')
        rf.set(qn('w:hAnsi'), 'Times New Roman')
        rPr.append(rf)
    return p

doc = Document()
sec = doc.sections[0]
set_margins(sec)
sec.page_height = Cm(29.7)
sec.page_width = Cm(21)

# Styles
st = doc.styles['Normal']
st.font.name = 'Times New Roman'
st.font.size = Pt(10)
st.font.color.rgb = BLACK
st.paragraph_format.space_after = Pt(4)
st.paragraph_format.line_spacing = 1.15
st.paragraph_format.widow_control = True

# ===== MUQOVA =====
# Ustki chiziq
add_para(doc, "JDA NASHRIYOTI  •  YUQORI KIMYO SERIYASI", size=7.5, color=BRONZE, align=WD_ALIGN_PARAGRAPH.CENTER, after=20, font="Calibri", caps=True, spacing=1.2)
add_rule(doc)

add_para(doc, "NOORGANIK", size=26, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, after=2, font="Times New Roman", spacing=1.0)
add_para(doc, "KISLOTALAR", size=26, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, after=6, font="Times New Roman", spacing=1.0)
add_rule(doc, color="1A2E4A")
add_para(doc, "Nazariya  •  Tuzilish  •  Sanoat  •  Hayot", size=9, italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, after=22, font="Times New Roman")

add_para(doc, "Chuqur ilmiy darslik", size=11, color=BLACK, align=WD_ALIGN_PARAGRAPH.CENTER, after=4, font="Times New Roman")
add_para(doc, "Universitet 1–2-kurs, olimpiada va o'qituvchilar uchun", size=8.5, italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, after=18, font="Times New Roman")

# Muallif bloki — klassik ramka
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pPr = p._p.get_or_add_pPr()
pBdr = OxmlElement('w:pBdr')
for edge in ['top','bottom']:
    el = OxmlElement(f'w:{edge}')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), '4')
    el.set(qn('w:color'), '8C6A2A')
    el.set(qn('w:space'), '8')
    pBdr.append(el)
pPr.append(pBdr)
p.paragraph_format.space_before = Pt(12)
p.paragraph_format.space_after = Pt(12)
r = p.add_run("Diyorbek Jabborov")
r.font.size = Pt(11)
r.bold = True
r.font.color.rgb = NAVY
r.font.name = "Times New Roman"
r2 = p.add_run("  •  JDA Kimyo Quiz muallifi")
r2.font.size = Pt(8.5)
r2.font.color.rgb = GRAY
r2.font.name = "Times New Roman"
for rr in p.runs:
    rPr = rr._r.get_or_add_rPr()
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), 'Times New Roman')
    rf.set(qn('w:hAnsi'), 'Times New Roman')
    rPr.append(rf)

add_para(doc, "Toshkent  —  2026", size=9, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, after=4, font="Times New Roman")
add_para(doc, "Mundarija  •  Loyiha nusxasi  •  Tasdiq uchun", size=7, color=LIGHT, align=WD_ALIGN_PARAGRAPH.CENTER, after=10, font="Calibri", caps=True)

# ===== ICHKI TITUL =====
doc.add_page_break()
add_para(doc, "NOORGANIK KISLOTALAR", size=11, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, after=4, font="Times New Roman", caps=True)
add_para(doc, "Chuqur ilmiy darslik", size=9, italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, after=6, font="Times New Roman")
add_rule(doc)
add_para(doc, "MUNDARIJA", size=18, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, after=6, font="Times New Roman", spacing=1.0)
add_para(doc, "Klassik shakl  •  To'liq tarkib  •  Sahifalar taxminiy", size=7.5, color=LIGHT, align=WD_ALIGN_PARAGRAPH.CENTER, after=12, font="Calibri")
# Kitob haqida qisqa
add_para(doc, "Kitob haqida", size=10, bold=True, color=NAVY, after=4, font="Times New Roman")
add_para(doc, "Ushbu darslik noorganik kislotalarni alohida moddalar to'plami sifatida emas, balki yagona tizim sifatida yoritadi: proton nazariyasidan tortib sanoat texnologiyasigacha, laboratoriya tajribasidan tirik organizmdagi o'rnigacha. Har bir nazariya o'z o'rnida, har bir kislota o'z monografiyasida, har bir sanoat jarayoni o'z sxemasida beriladi.", size=9, color=BLACK, after=6, font="Times New Roman", spacing=1.15)
add_para(doc, "Auditoriya: universitetning kimyo yo'nalishi 1–2-kurs talabalari, kimyo olimpiadasi ishtirokchilari va o'qituvchilar. Matn sodda o'zbek tilida, atamalar uch tilda (o'zbekcha — ruscha — inglizcha) izohlanadi.", size=8.5, italic=True, color=GRAY, after=6, font="Times New Roman", spacing=1.15)
add_para(doc, "Qanday tuzilgan: 5 qism, 25 bob, 7 ilova. Har bob 4–8 sahifa, yakunida mashqlar (javoblari ilovada). Barcha formulalar, jadvallar va rasmlar matnga mos, yagona uslubda.", size=8.5, color=GRAY, after=10, font="Times New Roman")

# ===== KLASIK MUNDARIJA JADVALI =====
# Sarlavha
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(8)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("M U N D A R I J A")
r.font.size = Pt(12)
r.bold = True
r.font.color.rgb = NAVY
r.font.name = "Times New Roman"
r.letter_spacing = Pt(2)

add_rule(doc, color="D9D9D9")
add_para(doc, "Sahifa raqamlari taxminiy — yakuniy sahifalash tahrirdan keyin qo'yiladi", size=7, italic=True, color=LIGHT, align=WD_ALIGN_PARAGRAPH.CENTER, after=10, font="Calibri")

# Ustki sarlavha
p = doc.add_paragraph()
pPr = p._p.get_or_add_pPr()
tabs = OxmlElement('w:tabs')
tab = OxmlElement('w:tab')
tab.set(qn('w:val'), 'right')
tab.set(qn('w:leader'), 'clear')
tab.set(qn('w:pos'), '9350')
tabs.append(tab)
pPr.append(tabs)
pf = p.paragraph_format
pf.space_after = Pt(4)
pf.space_before = Pt(6)
r1 = p.add_run("Bob nomi")
r1.font.size = Pt(7.5)
r1.bold = True
r1.font.color.rgb = GRAY
r1.font.name = "Calibri"
r1.all_caps = True
r2 = p.add_run("\tBet")
r2.font.size = Pt(7.5)
r2.bold = True
r2.font.color.rgb = GRAY
r2.font.name = "Calibri"
r2.all_caps = True
for rr in p.runs:
    rPr = rr._r.get_or_add_rPr()
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), 'Calibri')
    rf.set(qn('w:hAnsi'), 'Calibri')
    rPr.append(rf)

# So'z boshi
add_toc_entry(doc, "", "So'z boshi", "5", is_intro=True)
add_toc_entry(doc, "", "Kirish. Kitobdan qanday foydalaniladi. Belgilar va birliklar", "7", is_intro=True)
add_toc_entry(doc, "", "Xavfsizlik haqida ogohlantirish", "8", is_intro=True)

# QISM I
add_toc_entry(doc, "I QISM", "NAZARIY POYDEVOR — KISLOTA NIMA?", "9", is_part=True)
add_chapter_title(doc, "1-bob", "Kislota tushunchasining shakllanishi va tarixi", "“Acidus”dan superkislotagacha — 300 yillik yo'l")
add_toc_entry(doc, "1-bob", "Kislota tushunchasining shakllanishi va tarixi", "11")
add_toc_entry(doc, "2-bob", "Arrheniusning elektrolitik dissotsiatsiya nazariyasi", "15")
add_toc_entry(doc, "3-bob", "Brønsted–Lowry proton nazariyasi", "21")
add_toc_entry(doc, "4-bob", "Lewis elektron juft nazariyasi", "27")
add_toc_entry(doc, "5-bob", "Umumlashgan va zamonaviy talqinlar: Usanovich, Pearson (HSAB), Lyuks–Flud", "33")
add_toc_entry(doc, "6-bob", "Nomenklatura va tasnif. IUPAC qoidalari", "39")

add_toc_entry(doc, "II QISM", "TUZILISH VA UMUMIY QONUNIYATLAR", "47", is_part=True)
add_toc_entry(doc, "7-bob", "Kimyoviy bog'lanish va fazoviy tuzilish", "49")
add_toc_entry(doc, "8-bob", "Kislotalilik kuchi termodinamikasi. Ka, pKa va Hammett shkalasi", "57")
add_toc_entry(doc, "9-bob", "Suvli eritmalarda muvozanat: dissotsiatsiya, pH, titrlash va buferlar", "65")
add_toc_entry(doc, "10-bob", "Kislota–asos muvozanatlari va tuzlar. Gidroliz", "75")
add_toc_entry(doc, "11-bob", "Oksidlovchilik va qaytaruvchilik xossalari. Passivlanish", "83")
add_toc_entry(doc, "12-bob", "Olish usullari: laboratoriya va sanoat", "91")

add_toc_entry(doc, "III QISM", "ALOHIDA KISLOTALARNING KIMYOSI", "99", is_part=True)
add_toc_entry(doc, "13-bob", "Vodorod galogenidlari: HF, HCl, HBr, HI", "101")
add_toc_entry(doc, "14-bob", "Oltingugurt kislotalari: vodorod sulfid, sulfit va sulfat kislota, oleum", "111")
add_toc_entry(doc, "15-bob", "Azot kislotalari: nitrat va nitrit kislota", "125")
add_toc_entry(doc, "16-bob", "Fosfor kislotalari: orto-, piro-, meta- va polifosfat kislotalar", "137")
add_toc_entry(doc, "17-bob", "Uglerod va kremniy kislotalari", "149")
add_toc_entry(doc, "18-bob", "Bor kislotasi va uning hosilalari", "157")
add_toc_entry(doc, "19-bob", "Galogenlarning kislorodli kislotalari", "163")
add_toc_entry(doc, "20-bob", "O'tish metallari kislotalari: xrom va marganets misolida", "171")

add_toc_entry(doc, "IV QISM", "MAXSUS MUHIT VA TAHLIL", "179", is_part=True)
add_toc_entry(doc, "21-bob", "Suvsiz va noan'anaviy muhitdagi kislotalar. Superkislotalar", "181")
add_toc_entry(doc, "22-bob", "Kislotalarni aniqlash va miqdoriy tahlil usullari", "191")
add_toc_entry(doc, "23-bob", "Biologik va tibbiy ahamiyati", "199")

add_toc_entry(doc, "V QISM", "AMALIYOT, XAVFSIZLIK VA KELAJAK", "207", is_part=True)
add_toc_entry(doc, "24-bob", "Korroziya, ekologiya va atrof-muhit muhofazasi", "209")
add_toc_entry(doc, "25-bob", "Sanoat ishlab chiqarishi, xavfsizlik va kelajak texnologiyalari", "221")

# Ilovalar
p = doc.add_paragraph()
pPr = p._p.get_or_add_pPr()
tabs = OxmlElement('w:tabs')
tab = OxmlElement('w:tab')
tab.set(qn('w:val'), 'right')
tab.set(qn('w:leader'), 'dot')
tab.set(qn('w:pos'), '9350')
tabs.append(tab)
pPr.append(tabs)
p.paragraph_format.space_before = Pt(10)
p.paragraph_format.space_after = Pt(6)
r = p.add_run("ILOVALAR")
r.font.size = Pt(9)
r.bold = True
r.font.color.rgb = NAVY
r.font.name = "Times New Roman"
r.all_caps = True
rPr = r._r.get_or_add_rPr()
rf = OxmlElement('w:rFonts')
rf.set(qn('w:ascii'), 'Times New Roman')
rf.set(qn('w:hAnsi'), 'Times New Roman')
rPr.append(rf)

add_toc_entry(doc, "A", "Asosiy kislotalar jadvali. Fizik-kimyoviy kattaliklar", "233")
add_toc_entry(doc, "B", "Kuchlilik qatori va kislotalilik shkalalari", "239")
add_toc_entry(doc, "C", "Termodinamik va spektral ma'lumotlar", "243")
add_toc_entry(doc, "D", "Laboratoriya ishlari (8 ta tajriba)", "247")
add_toc_entry(doc, "E", "Mashqlar javoblari", "255")
add_toc_entry(doc, "F", "Atamalar lug'ati: o'zbekcha–ruscha–inglizcha", "263")
add_toc_entry(doc, "", "Adabiyotlar ro'yxati", "271")
add_toc_entry(doc, "", "Mavzuli ko'rsatkich (indeks)", "277")
add_toc_entry(doc, "", "Shartli belgilar va qisqartmalar", "282")

# ===== ANNOTATSIYA KARTA =====
doc.add_page_break()
add_para(doc, "ANNOTATSIYA", size=12, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, after=8, font="Times New Roman", caps=True)
add_rule(doc)
add_para(doc, "Noorganik kislotalar — chuqur ilmiy darslik laboratoriya tajribasini sanoat texnologiyasi va nazariy hisob bilan birlashtiradi. Kitobda Arrheniusdan Lyuisgacha bo'lgan barcha klassik nazariyalar, zamonaviy talqinlar (Usanovich, Pearson, superkislotalar) va 20 dan ortiq muhim kislotaning monografiyasi berilgan. Har bir bob mustaqil o'rganiladigan tarzda tuzilgan: nazariya, misol, rasm, mashq va xulosa.", size=9, color=BLACK, after=6, font="Times New Roman", spacing=1.15)
add_para(doc, "Kalit so'zlar: noorganik kislota, Arrhenius, Brønsted–Lowry, Lewis, pKa, titrlash, sulfat kislota, nitrat kislota, superkislota, korroziya.", size=8, italic=True, color=GRAY, after=8, font="Times New Roman")

add_para(doc, "Taqrizchilar:", size=9, bold=True, color=NAVY, after=4, font="Times New Roman")
add_para(doc, "•  Kimyo fanlari doktori, professor — ____________________", size=8.5, color=BLACK, after=3, font="Times New Roman")
add_para(doc, "•  Kimyo fanlari nomzodi, dotsent — ____________________", size=8.5, color=BLACK, after=10, font="Times New Roman")

# Qism izohi
add_para(doc, "Qismlar bo'yicha qisqacha annotatsiya", size=10, bold=True, color=NAVY, after=4, font="Times New Roman")
qismlar = [
    ("I QISM — Nazariy poydevor (1–6-bob)", "Kislota tushunchasining tarixi va barcha asosiy nazariyalar: Arrhenius, Brønsted–Lowry, Lewis, Usanovich, Pearson, Lyuks–Flud. Nomenklatura va tasnif (IUPAC)."),
    ("II QISM — Tuzilish va umumiy qonuniyatlar (7–12-bob)", "Bog'lanish, geometriya, termodinamika (Ka, pKa), suvli muhit (pH, titrlash, bufer, gidroliz), oksidlovchilik va olish usullari."),
    ("III QISM — Alohida kislotalar (13–20-bob)", "Har bir kislota oilasi alohida monografiya: tuzilishi, xossalari, olinishi, qo'llanilishi va xavfsizligi. HF dan HMnO₄ gacha."),
    ("IV QISM — Maxsus muhit va tahlil (21–23-bob)", "Suvsiz muhit, superkislotalar, analitik usullar (pH-metriya, IK, NMR), biologik ahamiyat."),
    ("V QISM — Amaliyot va kelajak (24–25-bob)", "Korroziya, kislotali yomg'ir, uchta zavod texnologiyasi, xavfsizlik, yangi energetika va yashil kimyo."),
]
for sar, txt in qismlar:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(0.5)
    r1 = p.add_run(sar + " — ")
    r1.font.size = Pt(8.5)
    r1.bold = True
    r1.font.color.rgb = NAVY
    r1.font.name = "Times New Roman"
    r2 = p.add_run(txt)
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = BLACK
    r2.font.name = "Times New Roman"
    for rr in p.runs:
        rPr = rr._r.get_or_add_rPr()
        rf = OxmlElement('w:rFonts')
        rf.set(qn('w:ascii'), 'Times New Roman')
        rf.set(qn('w:hAnsi'), 'Times New Roman')
        rPr.append(rf)

# ===== FOOTER/HEADER =====
for sec in doc.sections:
    hdr = sec.header
    hdr.is_linked_to_previous = False
    p = hdr.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("D. Jabborov  •  Noorganik kislotalar  •  Mundarija  •  Loyiha nusxasi")
    r.font.size = Pt(7)
    r.font.color.rgb = LIGHT
    r.font.name = "Calibri"
    r.italic = True
    rPr = r._r.get_or_add_rPr()
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), 'Calibri')
    rPr.append(rf)

    ftr = sec.footer
    ftr.is_linked_to_previous = False
    p = ftr.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '4')
    top.set(qn('w:color'), 'D9D9D9')
    top.set(qn('w:space'), '4')
    pBdr.append(top)
    pPr.append(pBdr)
    r = p.add_run("JDA nashriyoti  •  Toshkent, 2026")
    r.font.size = Pt(7)
    r.font.color.rgb = LIGHT
    r.font.name = "Calibri"
    rPr = r._r.get_or_add_rPr()
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), 'Calibri')
    rPr.append(rf)

doc.save(str(OUT))
print(f"Saved: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
