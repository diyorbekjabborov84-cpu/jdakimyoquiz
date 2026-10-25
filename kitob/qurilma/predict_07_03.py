#!/usr/bin/env python3
"""7.3 layout prediktori: DOCX qurilishidan oldin har bir bo'limning
chap/o'ng ustun balandligini bashorat qiladi (iter-1 PDF bilan kalibratsiya qilingan).

Kalibratsiya: chap qator oraliqlari, jadval qator balandligi, rasm balandligi va
o'ng ustun elementlari PDF'dan olingan; xatolik ~±6 pt.
"""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layout_07_03 as L
from layout_07_03 import (segments, para_lines, LEAD10, LEAD75, LEFT_W, RIGHT_W,
                          INDENT, BOT_Y, SEC_TOP, SEC_TOP1, RIGHT_TOP,
                          LEFT_BUDGET, RIGHT_BUDGET, PT_CM, img_h)
import equations_07_03 as EQ

ROOT = L.ROOT

# ------------------------------------------------------------------ konstantalar
LEAD9 = 10.35     # 9pt TNR qator oraliq'i
LEAD85 = 9.8      # 8.5pt
LEAD8 = 9.2       # 8pt
LEAD7 = 8.05      # 7pt
LEAD_MATH = 10.4  # OMML (9pt Cambria Math) + subscript kengayishi 4.2

TABLE_CAPTION_H = 11.0   # sarlavha qatori + space_before 6 + space_after 4
IMG_PAD = 2.0            # rasm qatori qo'shimcha bo'shliq

MAIN_W = 3.95            # sm — asosiy panel
EXTRA_W = 2.90           # sm — qo'shimcha sxema/rasm
REF_LEAD = 7.65          # 7pt, line_spacing 0.95

PANELS = [
 (0, 'tabiiyx.png', 'rasm'), (1, 'molekulax.png', 'rasm'), (2, 'rezonansx.png', 'sxema'),
 (3, 'spektr.png', 'grafik'), (4, 'kislotalik.png', 'grafik'), (5, 'dissotsiatsiya.png', 'grafik'),
 (6, 'sufmax.png', 'sxema'), (7, 'tuzlarilx.png', 'rasm'), (8, 'gidratlar.png', 'grafik'),
 (9, 'kristalx.png', 'sxema'), (10, 'sanoat.png', 'grafik')]

# (rasm_nomi, kenglik_sm)
EXTRA = {1: [('geometriax.png', 2.90)], 7: [('ionlarx.png', 2.90)],
         8: [('gidratx.png', 2.55)],
         9: [('gidratilx.png', 2.20)],
         10: [('xavfsizlikx.png', 2.10), ('zavodx.png', 2.10)]}

# asosiy panel kengligi (sm) — bo'limlararo vizual muvozanat uchun
MAIN_WS = [3.95, 3.95, 3.95, 3.95, 3.95, 3.95, 3.95, 3.95, 3.40, 2.95, 3.15]

# build_07_03_sidebar.py dagi panel matnlari (build skriptidan olinadi)
PANEL_TITLE = [
 'Manbalar va ishlab chiqarish.', 'Molekula geometriyasi.', 'Elektron tuzilma.',
 'Spektroskopiya.', 'Kislotalik va spetsiatsiya.', 'Suvdagi dissotsiatsiya.',
 'Sufma kislota va superkislotalik.', 'Sulfat tuzlari.', 'Gidratlar va fazaviy tarkib.',
 'Kristal tuzilma.', 'Sanoat va ekvivalent.']

LABEL = {'grafik': 'HISOBIY GRAFIK', 'sxema': 'TUSHUNTIRUVCHI SXEMA', 'rasm': 'CHIZMA VA IZOH'}

NOTE = [
 '7.3.1-rasm. Oltingugurt manbalari va sulfat kislota ishlab chiqarish (sxematik, original).',
 '7.3.2-rasm. H₂SO₄ molekulasi: C₂ simmetriya va gauche-gauche konformatsiya (sxematik, original).',
 '7.3.3-sxema. S–O bog‘lar, rezonans va gaz fazidagi kislotalik (sxematik).',
 '7.3.4-grafik. SO₄²⁻, HSO₄⁻ va H₂SO₄ tebranish bandlari (taxminiy chizma).',
 '7.3.5-grafik. HSO₄⁻ / SO₄²⁻ ulushlari pH bo‘yicha va 2-bosqich ulushi (taxminiy egri chiziq).',
 '7.3.6-grafik. pH va sulfat ioni miqdori konsentratsiya bo‘yicha (taxminiy egri chiziq).',
 '7.3.7-sxema. Avtoprotoliz, turlar va proton zaxirasi (sxematik).',
 '7.3.8-rasm. Sulfat tuzlari: kristallar va eruvchanlik (sxematik, original).',
 '7.3.9-grafik. Gidratlardagi H₂SO₄ ulushi va suv molekulasi soni (taxminiy egri chiziq).',
 '7.3.10-sxema. Monoklin hujra, vodorod bog‘i zanjiri va fazalar (sxematik).',
 '7.3.11-grafik. Sarf ulushlari, moddiy balans va ekvivalent (taxminiy hisob).']

EXTRA_CAPTION = {
 'geometriax.png': '7.3.2-sxema. Geometrik o‘lchovlar va simmetriya (sxematik).',
 'ionlarx.png': '7.3.8-sxema. Sulfat va gidrosulfat ionlari: tuzilma va rezonans (sxematik).',
 'gidratx.png': '7.3.9-sxema. Gidrat tarkibi va fazaviy hodisalar.',
 'gidratilx.png': '7.3.10-rasm. Gidrat kristallari: tuzilma va fazaviy tuzilma (sxematik).',
 'xavfsizlikx.png': '7.3.11-sxema. Xavfsizlik chegaralari va favqulodda holat (sxematik).',
 'zavodx.png': '7.3.11-rasm. Kontakt usuli: oltingugurtdan kislotagacha (sxematik).'}

REFS = [
 '[1] NIST Chemistry WebBook (CAS 7664-93-9) va NIST-JANAF (Chase, 1998): ΔfH°(g) −735,13 kJ/mol;  S° 298,78 J/(mol·K);  proton affinity 699,4 kJ/mol;  gaz bazikligi 666,9 kJ/mol;  ΔrG°(deprotonatsiya) 1265 ± 10 kJ/mol (Hunter & Lias, 1998).',
 '[2] NIST CCCBDB (C7664939):  C₂ simmetriya;  r(S=O) 142,2 pm;  r(S–OH) 157,4 pm;  r(O–H) 97,0 pm;  ∠O=S=O 123,3°;  ∠H–O–S 108,5°;  τ 89,1°;  kristal C2/c: a 818,1, b 469,60, c 856,3 pm, β 111,39°, Z 4.',
 '[3] Ab initio muvozanat tuzilmasi (2007): r(S=O) 140,99 pm;  τ −86,66°.  Raman/IR: SO₄²⁻ ν₁ 981, ν₂ 451, ν₃ 1104, ν₄ 617 sm⁻¹;  HSO₄⁻ 1055/1030/900 sm⁻¹ (Myhre va b., 2003; Attaia va b., 2020).',
 '[4] Kislotalik: K_a2 = 1,2×10⁻² (pK_a2 1,99);  K_a1 ≈ 10³;  H₀ = −12;  proton solvatatsiyasi ≈ −995 kJ/mol;  100 % kislota tarkibi (mmol/kg): HSO₄⁻ 15,0, H₃SO₄⁺ 11,3, H₃O⁺ 8,0, HS₂O₇⁻ 4,4, H₂S₂O₇ 3,6, H₂O 0,1.',
 '[5] Gidratlar va fazaviy diagramma (IUCr, 2012): SAM 84,5 %, SAD 73,1 %, SATri 64,5 %, SAT 57,6 %, SAH 45,6 %, SAO 40,5 %;  muz–SAH 211 K, muz–SAT 199 K.  Sanoat: USGS (2024), S&P Global — 260–290 mln t/y, fosfat o‘g‘itlari 56–60 %.',
 '[6] OSHA (29 CFR 1910.1000), NIOSH NPG/IDLH, ACGIH TLV, AIHA ERPG: PEL 1 mg/m³;  REL 1 mg/m³;  TLV-TWA 0,2 mg/m³ (torakal, A2);  IDLH 15 mg/m³;  ERPG 2/10/120 mg/m³;  IARC 1 — kuchli noorganik kislota tumanlari.']

DISCLAIMER = ('Barcha grafik, sxema va rasmlar original o‘quv ishlanmalari; sonli egri chiziqlar '
 'taxminiy hisoblar (o‘lchov ma’lumotlari emas). Rasmlar mikrofoto yoki atom tuzilmasi tasviri emas. '
 'Qu-rilma, texnologik parametrlar, konsentratsiya tanlash, idish materiallari, dozalar va tibbiy '
 'tavsiyalar bo‘yicha amaliyot tavsiyalari berilmaydi; xavfli kislotalar bilan ishlash tartibi 12-bo‘limda.')


def md_sections():
    src = (ROOT / 'matn' / '07_03.md').read_text()
    out = []
    for raw in src.split('## ')[1:]:
        t, b = raw.split('\n', 1)
        out.append((t, b.strip().split('\n\n')))
    return out


def eq_group_h(key):
    """Formula guruhi balandligi (OMML)."""
    groups = EQ.sulfate_equations()
    idx = EQ_KEYS.index(key)
    lines = groups[idx]
    h = 0.0
    for i, line in enumerate(lines):
        txt = ''.join(t for t in segments(''.join(
            x if isinstance(x, str) else '' for x in [])) ) if False else None
        sub = has_sub(line)
        h += (LEAD_MATH + (4.2 if sub else 0.0)) + (1.0 if i else 3.0) + 3.0
    return h


def has_sub(line):
    s = str(line)
    return 'sSub' in s or 'sub' in s


EQ_KEYS = ['umumiy', 'geometriya', 'rezonans', 'spektr', 'kislotalik', 'dissotsiatsiya',
           'sufma', 'ionlar', 'gidratlar', 'kristal', 'xulosa']


def predict(verbose=True):
    secs = md_sections()
    tables = json.loads((ROOT / 'matn' / '07_03_jadvallar.json').read_text())
    notes = json.loads((ROOT / 'matn' / '07_03_yonlavhalar.json').read_text())
    rows = []
    for idx, (title, paras) in enumerate(secs):
        # ---------------- CHAP ----------------
        L = 0.0
        first = True
        for p in paras:
            if p.startswith('[[TABLE:'):
                key = p[len('[[TABLE:'):-2]
                L += TABLE_CAPTION_H + table_h(tables[key]) + 3.0 + 1.5
                first = False
                continue
            if p.startswith('[[EQ:'):
                key = p[5:-2]
                L += eq_group_h(key)
                first = False
                continue
            n = para_lines(p, 10, LEFT_W, False, 0 if first else INDENT)
            L += n * LEAD10 + 1.5
            first = False
        if idx == 10:
            L += 4.0 + para_lines(DISCLAIMER, 8, LEFT_W) * LEAD8
            L += 5.0 + LEAD9 + 1.0
            for ref in REFS:
                L += para_lines(ref, 7, LEFT_W) * REF_LEAD
        # ---------------- O'NG ----------------
        R = 0.0
        R += para_lines(PANEL_TITLE[idx], 10, RIGHT_W, True) * LEAD10 + 9.0
        pic = PANELS[idx][1]
        R += img_h(pic[:-4], MAIN_WS[idx]) + IMG_PAD
        R += para_lines(LABEL[PANELS[idx][2]], 9, RIGHT_W, True) * LEAD9 + 10.0
        R += para_lines(NOTE[idx], 9, RIGHT_W) * LEAD9 + 1.5
        for ex, ew in EXTRA.get(idx, []):
            R += 8.0 + img_h(ex[:-4], ew) + IMG_PAD
            R += para_lines(EXTRA_CAPTION[ex] + ' Rang shartli.', 9, RIGHT_W) * LEAD9 + 1.5
        for label, body in notes[idx]:
            R += 10.0 + para_lines(label, 9, RIGHT_W, True) * LEAD9 + 4.0
            R += para_lines(body, 9, RIGHT_W) * (LEAD9 * 1.05) + 4.0
        rows.append((idx + 1, title, L, R))
    if verbose:
        print("=== BASHORAT (patchli build) ===")
        print("SEC |     L     bud    slack |     R     bud    slack | nomi")
        for i, t, L, R in rows:
            lb = BOT_Y - (SEC_TOP1 if i == 1 else SEC_TOP)
            rb = BOT_Y - RIGHT_TOP
            flag = '  <<< OVER' if (L > lb or R > rb) else ''
            print(f"{i:3d} | {L:7.1f} {lb:6.1f} {lb-L:+7.1f} | {R:7.1f} {rb:6.1f} {rb-R:+7.1f} | {t[:40]}{flag}")
    return rows


def table_h(spec):
    widths = [c * PT_CM for c in spec['widths']]
    inner = [w - 2 * 0.123 * PT_CM for w in widths]
    total = 0.0
    nl = [para_lines(spec['headers'][i], 7.5, inner[i], True) for i in range(len(widths))]
    total += max(nl) * LEAD75 + 1.6
    for row in spec['rows']:
        nl = [para_lines(v, 7.5, inner[i], i == 0) for i, v in enumerate(row)]
        total += max(nl) * LEAD75 + 1.6
    return total


if __name__ == '__main__':
    predict()
