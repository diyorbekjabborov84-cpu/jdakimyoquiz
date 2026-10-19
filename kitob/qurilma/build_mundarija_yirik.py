#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yirik boblar, ko'p mavzular — to'la ochilgan klassik mundarija v3
12 ta yirik BOB, ~70 ta MAVZU, 5 QISM
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chiqish" / "Noorganik Kislotalar - Mundarija (yirik boblar).docx"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = RGBColor(0x1A,0x2E,0x4A)
BRONZE = RGBColor(0x8C,0x6A,0x2A)
GRAY = RGBColor(0x5A,0x5A,0x5A)
LIGHT = RGBColor(0x8A,0x8A,0x8A)
BLACK = RGBColor(0x1A,0x1A,0x1A)

def set_margins(sec):
    sec.top_margin = Cm(2)
    sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2)
    sec.header_distance = Cm(1.2)
    sec.footer_distance = Cm(1)

def add_para(doc, text, size=10, bold=False, italic=False, color=BLACK, align=WD_ALIGN_PARAGRAPH.LEFT, after=4, before=0, font="Times New Roman"):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.15
    pf.widow_control = True
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    r.font.color.rgb = color
    r.font.name = font
    rPr = r._r.get_or_add_rPr()
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), font); rf.set(qn('w:hAnsi'), font)
    rPr.append(rf)
    return p

def add_rule(doc, color="8C6A2A"):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '6'); b.set(qn('w:color'), color); b.set(qn('w:space'), '4')
    pBdr.append(b); pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(8)
    return p

def add_qism(doc, num, title, desc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"{num}  ")
    r1.font.size = Pt(9); r1.bold = True; r1.font.color.rgb = BRONZE; r1.font.name = "Times New Roman"
    r2 = p.add_run(title)
    r2.font.size = Pt(12); r2.bold = True; r2.font.color.rgb = NAVY; r2.font.name = "Times New Roman"
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(6)
    p2.paragraph_format.left_indent = Cm(0.3)
    r = p2.add_run(desc)
    r.font.size = Pt(8); r.italic = True; r.font.color.rgb = GRAY; r.font.name = "Times New Roman"
    add_rule(doc, "D9D9D9")
    for rr in p.runs + p2.runs:
        rPr = rr._r.get_or_add_rPr()
        rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman')
        rPr.append(rf)

def add_bob(doc, num, title, subtitle, bet):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    tabs = OxmlElement('w:tabs')
    t = OxmlElement('w:tab'); t.set(qn('w:val'), 'right'); t.set(qn('w:leader'), 'dot'); t.set(qn('w:pos'), '9350')
    tabs.append(t); pPr.append(tabs)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"{num}-BOB.  ")
    r1.font.size = Pt(10); r1.bold = True; r1.font.color.rgb = NAVY; r1.font.name = "Times New Roman"
    r2 = p.add_run(title)
    r2.font.size = Pt(10); r2.bold = True; r2.font.color.rgb = BLACK; r2.font.name = "Times New Roman"
    r3 = p.add_run(f"\t{bet}")
    r3.font.size = Pt(9); r3.font.color.rgb = GRAY; r3.font.name = "Times New Roman"
    if subtitle:
        p2 = doc.add_paragraph()
        p2.paragraph_format.space_before = Pt(1); p2.paragraph_format.space_after = Pt(4); p2.paragraph_format.left_indent = Cm(0.6)
        r = p2.add_run(subtitle)
        r.font.size = Pt(8); r.italic = True; r.font.color.rgb = GRAY; r.font.name = "Times New Roman"
        rPr = r._r.get_or_add_rPr(); rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rPr.append(rf)
    for rr in p.runs:
        rPr = rr._r.get_or_add_rPr(); rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rPr.append(rf)
    return p

def add_mavzu(doc, num, title, note=None):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    tabs = OxmlElement('w:tabs')
    t = OxmlElement('w:tab'); t.set(qn('w:val'), 'right'); t.set(qn('w:leader'), 'dot'); t.set(qn('w:pos'), '9350')
    tabs.append(t); pPr.append(tabs)
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(1); p.paragraph_format.left_indent = Cm(0.6)
    r1 = p.add_run(f"{num}  ")
    r1.font.size = Pt(8.5); r1.font.color.rgb = BRONZE; r1.font.name = "Times New Roman"
    r2 = p.add_run(title)
    r2.font.size = Pt(9); r2.font.color.rgb = BLACK; r2.font.name = "Times New Roman"
    if note:
        r3 = p.add_run(f"  — {note}")
        r3.font.size = Pt(7.5); r3.italic = True; r3.font.color.rgb = LIGHT; r3.font.name = "Times New Roman"
    # bet joyi — hamma mavzular bob betiga kiradi, alohida bet qo'ymaymiz, bob beti yetarli
    for rr in p.runs:
        rPr = rr._r.get_or_add_rPr(); rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rPr.append(rf)
    return p

def add_toc_simple(doc, text, bet, bold=False, italic=False, indent=0):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    tabs = OxmlElement('w:tabs')
    t = OxmlElement('w:tab'); t.set(qn('w:val'), 'right'); t.set(qn('w:leader'), 'dot'); t.set(qn('w:pos'), '9350')
    tabs.append(t); pPr.append(tabs)
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
    if indent: p.paragraph_format.left_indent = Cm(indent)
    r = p.add_run(text + f"\t{bet}")
    r.font.size = Pt(9); r.bold = bold; r.italic = italic
    r.font.color.rgb = NAVY if bold else (GRAY if italic else BLACK)
    r.font.name = "Times New Roman"
    rPr = r._r.get_or_add_rPr(); rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rPr.append(rf)
    return p

# ================= BUILD =================
doc = Document()
sec = doc.sections[0]
set_margins(sec)
sec.page_height = Cm(29.7); sec.page_width = Cm(21)
st = doc.styles['Normal']
st.font.name = 'Times New Roman'; st.font.size = Pt(10); st.font.color.rgb = BLACK
st.paragraph_format.space_after = Pt(3); st.paragraph_format.line_spacing = 1.12

# Muqova
add_para(doc, "JDA NASHRIYOTI  •  YUQORI KIMYO SERIYASI", 7.5, False, False, BRONZE, WD_ALIGN_PARAGRAPH.CENTER, 18, 0, "Calibri")
add_rule(doc)
add_para(doc, "NOORGANIK", 26, True, False, NAVY, WD_ALIGN_PARAGRAPH.CENTER, 2, 0, "Times New Roman")
add_para(doc, "KISLOTALAR", 26, True, False, NAVY, WD_ALIGN_PARAGRAPH.CENTER, 4, 0, "Times New Roman")
add_rule(doc, "1A2E4A")
add_para(doc, "Nazariya  •  Tuzilish  •  Sanoat  •  Hayot", 9, False, True, GRAY, WD_ALIGN_PARAGRAPH.CENTER, 16, 0, "Times New Roman")
add_para(doc, "Yirik boblar — chuqur mavzular", 11, False, False, BLACK, WD_ALIGN_PARAGRAPH.CENTER, 4, 0, "Times New Roman")
add_para(doc, "Har bir kislota alohida mavzu sifatida ochilgan to'liq darslik", 8.5, False, True, GRAY, WD_ALIGN_PARAGRAPH.CENTER, 12, 0, "Times New Roman")
# muallif
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pPr = p._p.get_or_add_pPr(); pBdr = OxmlElement('w:pBdr')
for edge in ['top','bottom']:
    e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:color'), '8C6A2A'); e.set(qn('w:space'), '8'); pBdr.append(e)
pPr.append(pBdr); p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(8)
r = p.add_run("Diyorbek Jabborov"); r.font.size = Pt(11); r.bold = True; r.font.color.rgb = NAVY; r.font.name = "Times New Roman"
r2 = p.add_run("  •  JDA Kimyo Quiz muallifi"); r2.font.size = Pt(8.5); r2.font.color.rgb = GRAY; r2.font.name = "Times New Roman"
for rr in p.runs:
    rp = rr._r.get_or_add_rPr(); rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rp.append(rf)
add_para(doc, "Toshkent  —  2026", 9, False, False, GRAY, WD_ALIGN_PARAGRAPH.CENTER, 4, 0, "Times New Roman")
add_para(doc, "MUNDARIJA  •  YIRIK BOBLAR NASHRI  •  TASDIQ UCHUN", 7, False, False, LIGHT, WD_ALIGN_PARAGRAPH.CENTER, 10, 0, "Calibri")
# ichki titul
doc.add_page_break()
add_para(doc, "NOORGANIK KISLOTALAR", 11, True, False, NAVY, WD_ALIGN_PARAGRAPH.CENTER, 4, 0, "Times New Roman")
add_para(doc, "Yirik boblar — chuqur mavzular", 9, False, True, GRAY, WD_ALIGN_PARAGRAPH.CENTER, 4, 0, "Times New Roman")
add_rule(doc)
add_para(doc, "MUNDARIJA", 16, True, False, NAVY, WD_ALIGN_PARAGRAPH.CENTER, 6, 0, "Times New Roman")
add_para(doc, "Klassik shakl  •  5 qism  •  12 yirik bob  •  68 ta mavzu  •  Sahifalar taxminiy", 7.5, False, False, LIGHT, WD_ALIGN_PARAGRAPH.CENTER, 10, 0, "Calibri")
add_para(doc, "Ushbu mundarijada har bir bob yirik ilmiy blok, har bir mavzu esa mustaqil dars sifatida tuzilgan. Bir bob 12–20 sahifani, bir mavzu 2–4 sahifani egallaydi. Barcha muhim noorganik kislotalar — ftoriddan permanganatgacha — alohida mavzu sifatida ochilgan.", 8.5, False, True, GRAY, WD_ALIGN_PARAGRAPH.LEFT, 6, 0, "Times New Roman")
add_para(doc, "Qanday o'qiladi: Qism → Bob → Mavzu. Masalan, 7.3 — 7-bobning 3-mavzusi (Sulfat kislota). Har bir mavzu oxirida 3–5 ta mashq, har bob oxirida umumiy xulosa va test.", 8, False, False, GRAY, WD_ALIGN_PARAGRAPH.LEFT, 8, 0, "Times New Roman")

# Tezkor jadval
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(2)
r = p.add_run("M U N D A R I J A  —  QISQA KO'RINISHI"); r.font.size = Pt(9); r.bold = True; r.font.color.rgb = NAVY; r.font.name = "Times New Roman"
add_rule(doc, "D9D9D9")
add_toc_simple(doc, "So'z boshi", "5", italic=True)
add_toc_simple(doc, "Kirish. Kitobdan qanday foydalaniladi. Belgilar va birliklar", "7", italic=True)
add_toc_simple(doc, "Xavfsizlik haqida ogohlantirish", "8", italic=True)
add_toc_simple(doc, "I QISM  —  NAZARIY POYDEVOR", "9", bold=True)
add_toc_simple(doc, "1-bob. Kislota nima? Nazariyalar qiyosiy tahlili", "11", indent=0.3)
add_toc_simple(doc, "2-bob. Tuzilish, bog'lanish va tasnif", "27", indent=0.3)
add_toc_simple(doc, "3-bob. Kislotalilik kuchi va muvozanatlar", "41", indent=0.3)
add_toc_simple(doc, "II QISM  —  UMUMIY KIMYO", "59", bold=True)
add_toc_simple(doc, "4-bob. Umumiy kimyoviy xossalar", "61", indent=0.3)
add_toc_simple(doc, "5-bob. Olish, tozalash va konsentrlash", "75", indent=0.3)
add_toc_simple(doc, "III QISM  —  MUHIM KISLOTALARNING YAKKA KIMYOSI", "89", bold=True)
add_toc_simple(doc, "6-bob. Vodorod galogenidlari", "91", indent=0.3)
add_toc_simple(doc, "7-bob. Oltingugurt kislotalari oilasi", "105", indent=0.3)
add_toc_simple(doc, "8-bob. Azot kislotalari oilasi", "129", indent=0.3)
add_toc_simple(doc, "9-bob. Fosfor, uglerod, kremniy va bor kislotalari", "147", indent=0.3)
add_toc_simple(doc, "10-bob. Galogenlarning kislorodli kislotalari va o'tish metallari kislotalari", "167", indent=0.3)
add_toc_simple(doc, "IV QISM  —  MAXSUS MUHIT VA TAHLIL", "183", bold=True)
add_toc_simple(doc, "11-bob. Suvsiz muhit, superkislotalar va analitik kimyo", "185", indent=0.3)
add_toc_simple(doc, "12-bob. Biologik, tibbiy, ekologik va sanoat ahamiyati. Xavfsizlik va kelajak", "203", indent=0.3)
add_toc_simple(doc, "ILOVALAR  A–G", "221", bold=True)
add_toc_simple(doc, "Adabiyotlar • Ko'rsatkich • Lug'at", "243", italic=True)

# ===== QISM I =====
add_qism(doc, "I QISM", "NAZARIY POYDEVOR — KISLOTA NIMA?", "Maqsad: o'quvchi «kislota» deganda bitta ta'rif emas, 5 ta nazariya xaritasini va ularning qachon ishlashini bilsin.")
add_bob(doc, 1, "Kislota nima? Nazariyalar qiyosiy tahlili", "Tarixdan zamonaviylikgacha — barcha nazariyalar bir bobda, qiyosiy", "11")
add_mavzu(doc, "1.1", "Kislota tushunchasining kelib chiqishi", "«acidus», alkimyo, Lavuazye xatosi, Devi tuzatmasi")
add_mavzu(doc, "1.2", "Arrhenius nazariyasi — suvda dissotsiatsiya", "H⁺ va OH⁻, kuchli/kuchsiz, chegarasi nimada")
add_mavzu(doc, "1.3", "Brønsted–Lowry nazariyasi — proton beruvchi va oluvchi", "Konjugat juftliklar, suv amfolitligi")
add_mavzu(doc, "1.4", "Lewis nazariyasi — elektron juft nazariyasi", "Elektron donor/akseptor, BF₃, AlCl₃, komplekslar")
add_mavzu(doc, "1.5", "Umumlashgan nazariyalar: Usanovich, Lyuks–Flud", "Kation/anion almashinuvi, oksidlar talqini")
add_mavzu(doc, "1.6", "Pearsonning HSAB nazariyasi — qattiq va yumshoq kislotalar", "HSAB jadvali, amaliy bashorat")
add_mavzu(doc, "1.7", "Superkislotalar va o'ta kuchli muhit", "H₀ shkalasi, sehrli kislota, karboran kislotalar")
add_mavzu(doc, "1.8", "Qaysi nazariya qachon ishlaydi — tanlash algoritmi", "Taqqoslash jadvali, misollar bilan")

add_bob(doc, 2, "Tuzilish, bog'lanish va tasnif", "Atomdan molekulagacha — qanday tuzilgan, qanday nomlanadi", "27")
add_mavzu(doc, "2.1", "Kimyoviy bog'lanish va fazoviy tuzilish", "O–H bog'i, gibridlanish, VSEPR, tetraedr/piramida")
add_mavzu(doc, "2.2", "Rezonans, delokalizatsiya va vodorod bog'i", "Nima uchun H₂SO₄ kuchli, H₂SO₃ kuchsiz")
add_mavzu(doc, "2.3", "Tasnifning 4 o'lchovi", "Asoslilik, kislorod, kuch, barqarorlik bo'yicha")
add_mavzu(doc, "2.4", "Nomenklatura — IUPAC qoidalari", "An'anaviy va sistematik nomlar, misollar")
add_mavzu(doc, "2.5", "Oksidlanish darajasi va kislotalik bog'liqligi", "Cl +1 dan +7 gacha, xrom, marganets misolida")

add_bob(doc, 3, "Kislotalilik kuchi va muvozanatlar", "Nima uchun biri kuchli, biri kuchsiz — hisob bilan", "41")
add_mavzu(doc, "3.1", "Ka, pKa, α — ta'riflar va ma'nosi", "O'lchov shartlari, suvning roli")
add_mavzu(doc, "3.2", "Kuchga ta'sir etuvchi 6 omil", "Elektrmanfiylik, radius, zaryad, rezonans, gibridlanish, erituvchi")
add_mavzu(doc, "3.3", "Suvli eritmalarda muvozanat: dissotsiatsiya va pH", "Bir va ko'p bosqichli, Kuchli vs kuchsiz hisoblash")
add_mavzu(doc, "3.4", "Titrlash va indikatorlar", "3 tur egri chiziq, indikator tanlash qoidasi")
add_mavzu(doc, "3.5", "Buferlar va gidroliz", "Henderson–Hasselbalch, qon va okean misolida, tuzlar gidrolizi")
add_mavzu(doc, "3.6", "Kinetika va kataliz", "Proton ko'chishi, kislota katalizi, neytrallanish issiqligi")

# ===== QISM II =====
add_qism(doc, "II QISM", "UMUMIY KIMYO — HAMMA KISLOTAGA TEGISHLI QONUNLAR", "Bu qismdan keyin har qanday yangi kislotaning xossasini oldindan aytish mumkin.")
add_bob(doc, 4, "Umumiy kimyoviy xossalar", "Bitta bobda — barcha reaksiya turlari", "61")
add_mavzu(doc, "4.1", "Neytrallanish va tuz hosil bo'lishi", "To'liq va nordon tuzlar, neytrallanish turlari")
add_mavzu(doc, "4.2", "Oksidlovchilik va qaytaruvchilik", "HNO₃, H₂SO₄(kons.), HClO₄ qatori, metallar bilan")
add_mavzu(doc, "4.3", "Passivlanish va korroziya asoslari", "Fe, Al, Cr da himoya pardasi")
add_mavzu(doc, "4.4", "Kompleks va cho'kma hosil qilish", "Galogenid, sulfat, fosfat komplekslari")
add_mavzu(doc, "4.5", "Issiqlik va yorug'lik ta'sirida parchalanish", "H₂CO₃, HNO₃, HClO ning beqarorligi")

add_bob(doc, 5, "Olish, tozalash va konsentrlash", "Laboratoriyadan zavodgacha", "75")
add_mavzu(doc, "5.1", "Olishning 4 umumiy usuli", "Tuz+kislota, oksid+suv, sintez, elektroliz")
add_mavzu(doc, "5.2", "Tozalash: haydash, rektifikatsiya, kristallash", "Azeotrop muammosi — HNO₃–H₂O, HCl–H₂O")
add_mavzu(doc, "5.3", "Quritish va suvsizlantirish", "Konsentrlangan H₂SO₄, CaCl₂, P₂O₅ bilan")
add_mavzu(doc, "5.4", "Sanoat prinsiplari: xomashyo, katalizator, ekologiya", "Umumiy blok-sxema andozasi")

# ===== QISM III =====
add_qism(doc, "III QISM", "MUHIM NOORGANIK KISLOTALARNING YAKKA KIMYOSI", "Har bir bob — monografiyalar turkumi. Har bir kislota: tarixi → tuzilishi → xossalari → olinishi → qo'llanilishi → xavfsizligi.")
add_bob(doc, 6, "Vodorod galogenidlari", "Eng oddiy — eng ayyor guruh", "91")
add_mavzu(doc, "6.1", "Guruhning umumiy tavsifi", "H–X bog'i, fizik anomaliyalar, kislotalik qatori")
add_mavzu(doc, "6.2", "Ftorid kislota — HF", "Vodorod bog'i zanjiri, shishani eritishi, o'ta xavfli")
add_mavzu(doc, "6.3", "Xlorid kislota — HCl", "Oshqozondan sanoatgacha, H₂+Cl₂ sintezi")
add_mavzu(doc, "6.4", "Bromid kislota — HBr", "Qaytaruvchilik, olinishi, qo'llanilishi")
add_mavzu(doc, "6.5", "Yodid kislota — HI", "Eng kuchli qaytaruvchi, beqarorligi")
add_mavzu(doc, "6.6", "Taqqoslash va tanlash", "Jadval: pKa, qaynash, E°, qo'llash sohasi")

add_bob(doc, 7, "Oltingugurt kislotalari oilasi", "«Kimyo qoni» va uning qarindoshlari", "105")
add_mavzu(doc, "7.1", "Vodorod sulfid — H₂S", "Kuchsiz, uchuvchan, zaharli kislota")
add_mavzu(doc, "7.2", "Sulfit kislota — H₂SO₃", "Faqat eritmadagi kislota, SO₂+H₂O muvozanati")
add_mavzu(doc, "7.3", "Sulfat kislota — H₂SO₄: tuzilishi", "Rezonans, 2 proton, 5 ta rol")
add_mavzu(doc, "7.4", "Sulfat kislota: xossalari", "Kislota, oksidlovchi, suvsizlantiruvchi, sulfonlovchi")
add_mavzu(doc, "7.5", "Kontakt usuli — piritdan sulfat kislotagacha", "To'liq zavod texnologiyasi")
add_mavzu(doc, "7.6", "Oleum, pirosulfat va polisulfatlar", "H₂S₂O₇, oleum tarkibi")
add_mavzu(doc, "7.7", "Tiosulfat va peroksokislotalar", "H₂S₂O₃, H₂S₂O₈, H₂SO₅ — oksidlovchi bombalar")

add_bob(doc, 8, "Azot kislotalari oilasi", "Oksidlovchi malika va uning oilasi", "129")
add_mavzu(doc, "8.1", "Nitrat kislota — HNO₃: tuzilishi", "Tekis molekula, rezonans, N +5")
add_mavzu(doc, "8.2", "Nitrat kislota: oksidlovchilik", "Cu bilan kons. vs suyultirilgan — farqi")
add_mavzu(doc, "8.3", "Ostvald usuli — ammiakdan nitrat kislotagacha", "Pt–Rh to'r, 3 bosqich")
add_mavzu(doc, "8.4", "Nitrosoniy va nitroniy ionlari — nitrolash", "NO⁺, NO₂⁺ mexanizmi")
add_mavzu(doc, "8.5", "Nitrit kislota — HNO₂", "Beqarorlik, disproporsiya, diazotlash")
add_mavzu(doc, "8.6", "Boshqa azot kislotalari", "HN₃, H₂N₂O₂, gidroksilamin hosilalari")

add_bob(doc, 9, "Fosfor, uglerod, kremniy va bor kislotalari", "Tiriklik va toshlar kimyosi", "147")
add_mavzu(doc, "9.1", "Fosfor kislotalari umumiy — kondensatsiya zanjiri", "Orto → piro → meta → poli")
add_mavzu(doc, "9.2", "Ortofosfat kislota — H₃PO₄", "Tuzilish, 3 bosqich dissotsiatsiya, biologik rol")
add_mavzu(doc, "9.3", "Piro- va polifosfat kislotalar", "H₄P₂O₇, ATF, DNK skeleti")
add_mavzu(doc, "9.4", "Fosfit va gipofosfit kislotalar — H₃PO₃, H₃PO₂", "P–H bog'i, qaytaruvchilik")
add_mavzu(doc, "9.5", "Karbonat kislota — H₂CO₃", "CO₂+H₂O muvozanati, okean va qon buferi")
add_mavzu(doc, "9.6", "Sianid kislota — HCN", "Kuchsiz lekin o'ta zaharli")
add_mavzu(doc, "9.7", "Kremniy kislotalari", "H₄SiO₄, polimerlanish, silikagel")
add_mavzu(doc, "9.8", "Bor kislotasi — H₃BO₃ va hosilalari", "Lyuis kislotasi, boraks, HBF₄")

add_bob(doc, 10, "Galogenlarning kislorodli kislotalari va o'tish metallari kislotalari", "Beqarordan portlovchigacha, rangli oksidlovchilar", "167")
add_mavzu(doc, "10.1", "Umumiy qonun: oksidlanish darajasi oshsa — kislotalik va oksidlovchilik oshadi", "HClO dan HClO₄ gacha")
add_mavzu(doc, "10.2", "Xlorning kislorodli kislotalari", "HClO, HClO₂, HClO₃, HClO₄ — alohida")
add_mavzu(doc, "10.3", "Brom va yodning kislorodli kislotalari", "HBrO₃, HIO₃, H₅IO₆ — ortoyod kislota")
add_mavzu(doc, "10.4", "Xrom kislotalari — H₂CrO₄, H₂Cr₂O₇", "Xromat/dixromat muvozanati, rang o'tishi")
add_mavzu(doc, "10.5", "Marganets kislotasi — HMnO₄", "Binafsha, o'ta kuchli oksidlovchi, beqarorligi")
add_mavzu(doc, "10.6", "Boshqa o'tish metallari: texnetsiy, reniy", "HReO₄, HTcO₄ — qisqacha")

# ===== QISM IV =====
add_qism(doc, "IV QISM", "MAXSUS MUHIT VA TAHLIL", "Kislota faqat suvdagi H⁺ emas — suvsiz, qattiq, gaz fazada ham bor.")
add_bob(doc, 11, "Suvsiz muhit, superkislotalar va analitik kimyo", "Chegaradan tashqaridagi kislotalar", "185")
add_mavzu(doc, "11.1", "Suvsiz erituvchilar: H₂SO₄, HF, CH₃COOH, suyuq NH₃", "Erituvchi-sistema nazariyasi")
add_mavzu(doc, "11.2", "Superkislotalar", "Sehrli kislota FSO₃H·SbF₅, HF·SbF₅, karboran")
add_mavzu(doc, "11.3", "Qattiq kislotalar: seolitlar, sulfatlangan sirkoniy", "Neft krekingi, kataliz")
add_mavzu(doc, "11.4", "Klassik tahlil: titrlash, gravimetriya", "SO₄²⁻→BaSO₄, Cl⁻→AgCl")
add_mavzu(doc, "11.5", "Zamonaviy usullar: pH-metriya, IK, NMR", "Spektroskopik «barmoq izi»")

add_bob(doc, 12, "Biologik, tibbiy, ekologik va sanoat ahamiyati. Xavfsizlik va kelajak", "Laboratoriyadan sayyoragacha", "203")
add_mavzu(doc, "12.1", "Tirik organizmdagi kislotalar", "Oshqozon HCl, qon buferlari, suyak va DNK fosfatlari")
add_mavzu(doc, "12.2", "Dorivorlik va oziq-ovqat", "H₃BO₃, fosfatlar, antatsidlar")
add_mavzu(doc, "12.3", "Metallar korroziyasi va himoya", "Kislotali korroziya, inhibitorlar, qoplamalar")
add_mavzu(doc, "12.4", "Ekologiya: kislotali yomg'ir, tuproq, okean", "SOₓ/NOₓ → H₂SO₄/HNO₃, okean atsidozlashishi")
add_mavzu(doc, "12.5", "Uchta zavod ichidan: sulfat, nitrat, fosfat", "Kontakt, Ostvald, ekstraksion — blok-sxemalar")
add_mavzu(doc, "12.6", "Xavfsizlik, saqlash va birinchi yordam", "15 qoida, moslik matritsasi, neytrallash")
add_mavzu(doc, "12.7", "Kelajak: energetika va yashil kimyo", "Nafion membranasi, akkumulyatorlar, CO₂ ushlash")

# ILOVALAR
p = doc.add_paragraph()
pPr = p._p.get_or_add_pPr()
tabs = OxmlElement('w:tabs'); t = OxmlElement('w:tab'); t.set(qn('w:val'), 'right'); t.set(qn('w:leader'), 'dot'); t.set(qn('w:pos'), '9350'); tabs.append(t); pPr.append(tabs)
p.paragraph_format.space_before = Pt(14); p.paragraph_format.space_after = Pt(6)
r = p.add_run("ILOVALAR"); r.font.size = Pt(10); r.bold = True; r.font.color.rgb = NAVY; r.font.name = "Times New Roman"
rPr = r._r.get_or_add_rPr(); rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rPr.append(rf)
add_toc_simple(doc, "A. Asosiy kislotalar jadvali (30 ta kislota, pKa, zichlik, LD₅₀)", "223", italic=True)
add_toc_simple(doc, "B. Kuchlilik qatori va kislotalilik shkalalari (suvda, gaz fazada, H₀)", "227", italic=True)
add_toc_simple(doc, "C. Termodinamik va spektral ma'lumotlar (ΔH, ΔG, IK, NMR)", "231", italic=True)
add_toc_simple(doc, "D. Laboratoriya ishlari — 8 ta tajriba yo'riqnomasi", "235", italic=True)
add_toc_simple(doc, "E. Mashqlar javoblari (har mavzu bo'yicha)", "241", italic=True)
add_toc_simple(doc, "F. Atamalar lug'ati: o'zbekcha — ruscha — inglizcha (180 ta atama)", "253", italic=True)
add_toc_simple(doc, "G. Adabiyotlar, indeks va shartli belgilar", "263", italic=True)

# Izoh
add_para(doc, "Izoh: har bir mavzu 2–4 sahifa, har bir bob 12–20 sahifa. To'liq kitob ~280–320 sahifa. Har bir bobda 4–8 ta chizma/grafik, har bir mavzuda 1 ta jadval yoki sxema bor. Barcha chizmalar kitob uchun yagona uslubda, o'zbek tilida tayyorlanadi.", 7.5, False, True, LIGHT, WD_ALIGN_PARAGRAPH.LEFT, 10, 6, "Times New Roman")

# Annotatsiya
doc.add_page_break()
add_para(doc, "ANNOTATSIYA", 12, True, False, NAVY, WD_ALIGN_PARAGRAPH.CENTER, 8, 0, "Times New Roman")
add_rule(doc)
add_para(doc, "Ushbu darslik noorganik kislotalarni to'liq ochib beradi: 7 ta nazariya (Arrhenius, Brønsted–Lowry, Lewis, Usanovich, Pearson HSAB, Lyuks–Flud, superkislotalar) va 30 dan ortiq kislotaning yakka kimyosi. Har bir kislota alohida mavzu sifatida — tuzilishi, olinishi, xossalari, qo'llanilishi va xavfsizligi bilan yoritilgan. Kitob laboratoriya tajribasini sanoat texnologiyasi (kontakt, Ostvald, ekstraksion) va hayotiy misollar (qon buferi, kislotali yomg'ir, akkumulyator) bilan bog'laydi.", 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 8, 0, "Times New Roman")
add_para(doc, "Kalit so'zlar: noorganik kislota, Lewis, Brønsted–Lowry, pKa, H₂SO₄, HNO₃, H₃PO₄, superkislota, korroziya, titrlash.", 8, False, True, GRAY, WD_ALIGN_PARAGRAPH.LEFT, 6, 0, "Times New Roman")
add_para(doc, "Taqrizchilar:", 9, True, False, NAVY, WD_ALIGN_PARAGRAPH.LEFT, 6, 0, "Times New Roman")
add_para(doc, "•  Kimyo fanlari doktori, professor — ____________________", 8.5, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 3, 0, "Times New Roman")
add_para(doc, "•  Kimyo fanlari nomzodi, dotsent — ____________________", 8.5, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 8, 0, "Times New Roman")

# footer/header
for sec in doc.sections:
    hdr = sec.header; hdr.is_linked_to_previous = False
    p = hdr.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("D. Jabborov  •  Noorganik kislotalar  •  Mundarija  •  Yirik boblar nashri")
    r.font.size = Pt(7); r.font.color.rgb = LIGHT; r.font.name = "Calibri"; r.italic = True
    rPr = r._r.get_or_add_rPr(); rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Calibri'); rPr.append(rf)
    ftr = sec.footer; ftr.is_linked_to_previous = False
    p = ftr.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr(); pBdr = OxmlElement('w:pBdr')
    t = OxmlElement('w:top'); t.set(qn('w:val'), 'single'); t.set(qn('w:sz'), '4'); t.set(qn('w:color'), 'D9D9D9'); t.set(qn('w:space'), '4'); pBdr.append(t); pPr.append(pBdr)
    r = p.add_run("JDA nashriyoti  •  Toshkent, 2026"); r.font.size = Pt(7); r.font.color.rgb = LIGHT; r.font.name = "Calibri"
    rPr = r._r.get_or_add_rPr(); rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Calibri'); rPr.append(rf)

doc.save(str(OUT))
print(f"Saved: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
