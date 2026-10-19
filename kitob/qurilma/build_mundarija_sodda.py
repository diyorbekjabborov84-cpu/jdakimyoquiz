#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chiqish" / "Noorganik Kislotalar - Mundarija.docx"
OUT.parent.mkdir(parents=True, exist_ok=True)

BLACK = RGBColor(0x1A,0x1A,0x1A)
GRAY = RGBColor(0x5A,0x5A,0x5A)
NAVY = RGBColor(0x1A,0x2E,0x4A)

def add_p(doc, text, size=10, bold=False, italic=False, color=BLACK, align=WD_ALIGN_PARAGRAPH.LEFT, before=0, after=4, indent=0):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.12
    if indent:
        pf.left_indent = Cm(indent)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    r.font.color.rgb = color
    r.font.name = "Times New Roman"
    rPr = r._r.get_or_add_rPr()
    rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rPr.append(rf)
    return p

doc = Document()
sec = doc.sections[0]
sec.top_margin = Cm(2); sec.bottom_margin = Cm(2); sec.left_margin = Cm(2.5); sec.right_margin = Cm(2)
sec.page_height = Cm(29.7); sec.page_width = Cm(21)
st = doc.styles['Normal']
st.font.name = 'Times New Roman'; st.font.size = Pt(10); st.font.color.rgb = BLACK
st.paragraph_format.space_after = Pt(2); st.paragraph_format.line_spacing = 1.12

add_p(doc, "NOORGANIK KISLOTALAR", 14, True, False, NAVY, WD_ALIGN_PARAGRAPH.CENTER, 0, 2)
add_p(doc, "Ishchi mundarija — 5 qism, 12 bob, 68 mavzu", 9, False, True, GRAY, WD_ALIGN_PARAGRAPH.CENTER, 0, 12)

# QISM I
add_p(doc, "I QISM. NAZARIY POYDEVOR", 11, True, False, NAVY, WD_ALIGN_PARAGRAPH.LEFT, 10, 6)
add_p(doc, "1-bob. Kislota nima? Nazariyalar", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 4, 4, 0.3)
for t in ["1.1. Kislota tushunchasining kelib chiqishi","1.2. Arrhenius nazariyasi","1.3. Brønsted–Lowry nazariyasi","1.4. Lewis nazariyasi","1.5. Usanovich va Lyuks–Flud nazariyalari","1.6. Pearson HSAB nazariyasi","1.7. Superkislotalar","1.8. Nazariyalarni qiyoslash"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

add_p(doc, "2-bob. Tuzilish, tasnif, nomenklatura", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 6, 4, 0.3)
for t in ["2.1. Kimyoviy bog'lanish va fazoviy tuzilish","2.2. Rezonans va vodorod bog'i","2.3. Tasnif","2.4. Nomenklatura (IUPAC)","2.5. Oksidlanish darajasi va kislotalik"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

add_p(doc, "3-bob. Kislotalilik kuchi va muvozanatlar", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 6, 4, 0.3)
for t in ["3.1. Ka, pKa, alfa","3.2. Kuchga ta'sir etuvchi omillar","3.3. Dissotsiatsiya va pH","3.4. Titrlash va indikatorlar","3.5. Buferlar va gidroliz","3.6. Kinetika va kataliz"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

# QISM II
add_p(doc, "II QISM. UMUMIY KIMYO", 11, True, False, NAVY, WD_ALIGN_PARAGRAPH.LEFT, 10, 6)
add_p(doc, "4-bob. Umumiy kimyoviy xossalar", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 4, 4, 0.3)
for t in ["4.1. Neytrallanish va tuz hosil bo'lishi","4.2. Oksidlovchilik va qaytaruvchilik","4.3. Passivlanish","4.4. Kompleks va cho'kma hosil qilish","4.5. Parchalanish"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

add_p(doc, "5-bob. Olish, tozalash, konsentrlash", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 6, 4, 0.3)
for t in ["5.1. Olishning umumiy usullari","5.2. Tozalash","5.3. Quritish va suvsizlantirish","5.4. Sanoat prinsiplari"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

# QISM III
add_p(doc, "III QISM. ALOHIDA KISLOTALAR", 11, True, False, NAVY, WD_ALIGN_PARAGRAPH.LEFT, 10, 6)
add_p(doc, "6-bob. Vodorod galogenidlari", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 4, 4, 0.3)
for t in ["6.1. Guruhning umumiy tavsifi","6.2. HF — ftorid kislota","6.3. HCl — xlorid kislota","6.4. HBr — bromid kislota","6.5. HI — yodid kislota","6.6. Taqqoslash"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

add_p(doc, "7-bob. Oltingugurt kislotalari", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 6, 4, 0.3)
for t in ["7.1. H₂S — vodorod sulfid","7.2. H₂SO₃ — sulfit kislota","7.3. H₂SO₄ — sulfat kislota (tuzilishi)","7.4. H₂SO₄ — xossalari","7.5. Kontakt usuli","7.6. Oleum va pirosulfat","7.7. Tiosulfat va peroksokislotalar"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

add_p(doc, "8-bob. Azot kislotalari", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 6, 4, 0.3)
for t in ["8.1. HNO₃ — nitrat kislota (tuzilishi)","8.2. HNO₃ — oksidlovchilik","8.3. Ostvald usuli","8.4. NO⁺ va NO₂⁺","8.5. HNO₂ — nitrit kislota","8.6. Boshqa azot kislotalari"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

add_p(doc, "9-bob. Fosfor, uglerod, kremniy, bor kislotalari", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 6, 4, 0.3)
for t in ["9.1. Fosfor kislotalari — umumiy","9.2. H₃PO₄ — ortofosfat","9.3. Piro- va polifosfatlar","9.4. H₃PO₃ va H₃PO₂","9.5. H₂CO₃ — karbonat kislota","9.6. HCN — sianid kislota","9.7. Kremniy kislotalari","9.8. H₃BO₃ — bor kislotasi"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

add_p(doc, "10-bob. Galogen kislorodli va o'tish metallari kislotalari", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 6, 4, 0.3)
for t in ["10.1. Umumiy qonun","10.2. Xlor kislorodli kislotalari","10.3. Brom va yod kislorodli kislotalari","10.4. Xrom kislotalari","10.5. Marganets kislotasi","10.6. Boshqa o'tish metallari"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

# QISM IV
add_p(doc, "IV QISM. MAXSUS MUHIT VA TAHLIL", 11, True, False, NAVY, WD_ALIGN_PARAGRAPH.LEFT, 10, 6)
add_p(doc, "11-bob. Suvsiz muhit, superkislotalar, tahlil", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 4, 4, 0.3)
for t in ["11.1. Suvsiz erituvchilar","11.2. Superkislotalar","11.3. Qattiq kislotalar","11.4. Klassik tahlil","11.5. Zamonaviy usullar"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

# QISM V
add_p(doc, "V QISM. HAYOT, SANOAT, XAVFSIZLIK", 11, True, False, NAVY, WD_ALIGN_PARAGRAPH.LEFT, 10, 6)
add_p(doc, "12-bob. Ahamiyati va kelajak", 10, True, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 4, 4, 0.3)
for t in ["12.1. Tirik organizmdagi kislotalar","12.2. Dorivorlik","12.3. Korroziya va himoya","12.4. Ekologiya","12.5. Sanoat (uchta zavod)","12.6. Xavfsizlik","12.7. Kelajak texnologiyalari"]:
    add_p(doc, t, 9, False, False, BLACK, WD_ALIGN_PARAGRAPH.LEFT, 0, 1, 0.8)

doc.save(str(OUT))
print(f"Saved: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
