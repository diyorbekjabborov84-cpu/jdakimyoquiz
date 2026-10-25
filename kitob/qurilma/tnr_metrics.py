#!/usr/bin/env python3
"""TNR metrikasi: PDF dan haqiqiy Times New Roman shriftini chiqarib,
matn qatorlarini aniq bashorat qilish (kalibratsiya 7.3 uchun)."""
from pathlib import Path
import pymupdf as fitz

PDF = Path('google_drive/Noorganik kislotalar — 7.3. Sulfat kislota (tuzilishi)')
CACHE = Path('/tmp/tnr_metrics.json')


def _extract():
    """PDF ichidagi shriftlarni topadi: /Font -> /FontDescriptor -> /FontFile2."""
    d = fitz.open(PDF)
    out = {}
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
            cid = int(df[1].split()[0])
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
            out[name] = d.xref_stream(int(ff[1].split()[0]))
        except Exception:
            pass
    return out


def build():
    raw = _extract()
    fonts = {}
    for name, buf in raw.items():
        try:
            f = fitz.Font(fontbuffer=buf)
            fonts[name] = f
        except Exception as e:
            print('font skip', name, e)
    return fonts


FONTS = None


def _get():
    global FONTS
    if FONTS is None:
        FONTS = build()
    return FONTS


def width(text, size=10.0, bold=False):
    """Matn kengligi (pt)."""
    fs = _get()
    key = 'TimesNewRomanPS-BoldMT' if bold else 'TimesNewRomanPSMT'
    f = fs.get(key)
    if f is None:
        f = fs.get('TimesNewRomanPSMT')
    if f is None:
        return fitz.get_text_length(text, fontname='tiro', fontsize=size)
    return f.text_length(text, size)


def lines(text, size=10.0, avail=371.7, bold=False, first_indent=0.0):
    """Matn qatorlar soni (TNR metrikasi bilan, greedy wrap)."""
    if avail - first_indent <= 4:
        first_indent = 0.0
    total = 0
    for hard in text.split('\n'):
        words = hard.split(' ')
        cur = ''
        n = 1
        limit = avail - first_indent
        for word in words:
            trial = word if not cur else cur + ' ' + word
            if width(trial, size, bold) <= limit:
                cur = trial
            else:
                n += 1
                cur = word
                while width(cur, size, bold) > avail and len(cur) > 1:
                    n += 1
                    cur = cur[1:]
                limit = avail
        total += n
    return total


def para_h(text, size=10.0, avail=371.7, bold=False, first_indent=0.0, lead=1.155):
    """Paragraf balandligi (pt) — Word line spacing 1.0, TNR."""
    return lines(text, size, avail, bold, first_indent) * size * lead


if __name__ == '__main__':
    fs = _get()
    print('shriftlar:', list(fs))
    # kalibratsiya: 10pt TNR bir qatori
    print('100 x "n" =', round(width('n' * 100, 10), 2))
    print('Jadval 7.5pt "Taxminiy hisob: massadagi ulush" =',
          round(width('Taxminiy hisob: massadagi ulush', 7.5), 2))
