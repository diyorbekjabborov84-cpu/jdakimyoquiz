#!/usr/bin/env python3
"""7.3 layout simulator: DOCX qurilishidan oldin sahifa sig'ishini bashorat qiladi.

Kalibratsiya: iter-1 PDF (google_drive/...7.3...) dan olingan qator balandliklari,
jadval qator chegaralari va rasm o'lchamlari asosida.
"""
from pathlib import Path
import re, json, math
import pymupdf as fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'rasmlar' / 'sulfat'
PDF = ROOT.parent / 'google_drive' / 'Noorganik kislotalar — 7.3. Sulfat kislota (tuzilishi)'

# ---------------------------------------------------------------- shrift
_FONTS = {}


def _load_fonts():
    if _FONTS:
        return _FONTS
    d = fitz.open(PDF)
    for x in range(1, d.xref_length()):
        try:
            k = d.xref_get_key(x, 'Type')
            bf = d.xref_get_key(x, 'BaseFont')
            df = d.xref_get_key(x, 'DescendantFonts')
        except Exception:
            continue
        if not k or k[1] != '/Font' or not bf or bf[1] == 'null':
            continue
        name = bf[1].strip('/').split('+')[-1]
        fd = None
        if df and df[1] != 'null':
            cid = int(df[1].strip('[] ').split()[0])
            f = d.xref_get_key(cid, 'FontDescriptor')
            if f and f[1] != 'null':
                fd = int(f[1].split()[0])
        else:
            f = d.xref_get_key(x, 'FontDescriptor')
            if f and f[1] != 'null':
                fd = int(f[1].split()[0])
        if fd is None:
            continue
        ff = d.xref_get_key(fd, 'FontFile2')
        if not ff or ff[1] == 'null':
            continue
        try:
            _FONTS[name] = fitz.Font(fontbuffer=d.xref_stream(int(ff[1].split()[0])))
        except Exception:
            pass
    return _FONTS


def _w(text, size, bold):
    fs = _load_fonts()
    f = fs.get('TimesNewRomanPS-BoldMT' if bold else 'TimesNewRomanPSMT')
    if f is None:
        return fitz.get_text_length(text, fontname='tiro', fontsize=size)
    return f.text_length(text, size)


# ---------------------------------------------------------------- segmentatsiya
SUB = dict(zip('₀₁₂₃₄₅₆₇₈₉ₐᵦₘⱼ', '0123456789abmj'))
SUP = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵐⁿ‡', '0123456789+−mn‡'))
TOKEN = re.compile(r'([A-Za-zΑ-Ωα-ωβγδΔ′][A-Za-zΑ-Ωα-ωβγδΔ′₀-₉]*)_([A-Za-z0-9′]+)')
SCR = 0.6   # indeks/ust-indeks kichikligi (PDF: 10pt -> 6pt)


def segments(text, bold=False):
    """Matnni (matn, kichiklik, qalin) segmentlariga bo'ladi — build_07_03_sidebar._segment ga o'xshash."""
    out = []

    def emit(chunk, b):
        buf = ''
        for ch in chunk:
            if ch in SUB:
                if buf:
                    out.append((buf, 1.0, b)); buf = ''
                out.append((SUB[ch], SCR, b))
            elif ch in SUP:
                if buf:
                    out.append((buf, 1.0, b)); buf = ''
                out.append((SUP[ch], SCR, b))
            else:
                buf += ch
        if buf:
            out.append((buf, 1.0, b))

    parts = text.split('**')
    for i, seg in enumerate(parts):
        if not seg:
            continue
        b = bold or (i % 2 == 1)
        pos = 0
        for m in TOKEN.finditer(seg):
            emit(seg[pos:m.start()], b)
            out.append((m.group(1), 1.0, b))
            out.append((m.group(2), SCR, b))
            pos = m.end()
        emit(seg[pos:], b)
    return out


def seg_width(segs, size):
    return sum(_w(t, size * s, b) for t, s, b in segs)


def wrap_lines(segs, size, avail, first_indent=0.0):
    """Greedy wrap — qatorlar soni."""
    # har segmentni so'zlarga ajratib, lekin segment chegarasini saqlab
    words = []
    for t, s, b in segs:
        parts = t.split(' ')
        for j, w in enumerate(parts):
            if w == '' and j > 0:
                continue
            words.append((w, s, b, j == 0 and len(words) == 0))
    n = 1
    cur = 0.0
    limit = avail - first_indent
    space = _w(' ', size, False)
    for i, (w, s, b, first) in enumerate(words):
        ww = _w(w, size * s, b)
        add = ww if cur == 0 else space + ww
        if cur + add <= limit or cur == 0:
            cur += add
        else:
            n += 1
            cur = ww
        # so'z satrga sig'maydi — kesib chiqarish (Word xuddi shunday qiladi)
        while cur > avail and len(w) > 1:
            k = len(w) - 1
            while k > 1 and _w(w[:k], size * s, b) > avail:
                k -= 1
            n += 1
            cur = _w(w[k:], size * s, b)
            w = w[k:]
    return n


def para_lines(text, size, avail, bold=False, first_indent=0.0):
    return wrap_lines(segments(text, bold), size, avail, first_indent)


# ---------------------------------------------------------------- konstantalar
LEAD10 = 11.73      # 10pt TNR qator oraliq'i (PDF'dan)
LEAD75 = 9.35       # 7.5pt (jadval) — PDF'dan
LEAD9 = 10.55       # 9pt
LEAD85 = 9.95       # 8.5pt
SUB_SUB = 1.0

LEFT_W = 373.7      # chap matn maydoni (PDF: 42.5 -> 416.2)
RIGHT_W = 116.6     # o'ng matn maydoni (PDF: 433.2 -> 549.8)
INDENT = 12.76      # 0.45 sm
CELL_RT = 7.0       # o'ng katak yuqori margini (140 dxa)
CELL_RB = 6.5       # pastki (130 dxa)

TOP_Y = 42.5        # sahifa matn boshlanishi
BOT_Y = 802.0       # sahifa matn tugashi
SEC_TOP = 92.9      # bo'lim kontenti (band + sarlavha dan keyin)
SEC_TOP1 = 146.5    # 1-bo'lim (2 ta band)
RIGHT_TOP = 99.6

PT_CM = 28.3465


def img_h(name, width_cm):
    with Image.open(ASSETS / (name + '.png')) as im:
        w, h = im.size
    return width_cm * PT_CM * h / w


def table_h(spec):
    """Jadval balandligi: sarlavha + qatorlar (har biri maksimal qator sonidan)."""
    widths = [c * PT_CM for c in spec['widths']]
    inner = [w - 2 * 0.123 * PT_CM for w in widths]
    total = 0.0
    nl = [para_lines(spec['headers'][i], 7.5, inner[i], True) for i in range(len(widths))]
    total += max(nl) * LEAD75 + 1.6
    for row in spec['rows']:
        nl = []
        for i, v in enumerate(row):
            nl.append(para_lines(v, 7.5, inner[i], i == 0))
        total += max(nl) * LEAD75 + 1.6
    return total


LEFT_BUDGET = BOT_Y - SEC_TOP     # chap ustun: 92.9 -> 802
RIGHT_BUDGET = BOT_Y - RIGHT_TOP  # o'ng ustun: 99.6 -> 802
