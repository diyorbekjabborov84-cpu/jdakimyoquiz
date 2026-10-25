#!/usr/bin/env python3
"""Simulator validatsiyasi: iter-1 PDF qator sonlari bilan bashoratni solishtiradi."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layout_07_03 as L
import pymupdf as fitz

d = fitz.open(L.PDF)
md = (L.ROOT / 'matn' / '07_03.md').read_text()
secs = []
for raw in md.split('## ')[1:]:
    t, b = raw.split('\n', 1)
    secs.append((t, b.strip().split('\n\n')))

SEC_PAGES = [(1, [1, 2]), (2, [3]), (3, [4]), (4, [5]), (5, [6]), (6, [7]),
             (7, [8]), (8, [9]), (9, [10, 11]), (10, [12]), (11, [13, 14])]

print("=== Har bir bo'lim: PDF chap qatorlari (10pt) vs simulator ===")
tot_ok = tot_bad = 0
for si, (title, paras) in enumerate(secs, 1):
    pages = SEC_PAGES[si - 1][1]
    # PDF: 10pt chap qatorlar
    pdf_lines = []
    for pi in pages:
        for bl in d[pi - 1].get_text('dict')['blocks']:
            if bl['type'] != 0:
                continue
            x0, y0, x1, y1 = bl['bbox']
            if x0 > 430 or y1 > 805 or y0 < 35:
                continue
            for ln in bl['lines']:
                if any(round(s['size'], 1) == 10.0 for s in ln['spans']):
                    pdf_lines.append((pi, round(ln['bbox'][1], 1), round(ln['bbox'][3], 1)))
    n_pdf = len(pdf_lines)
    # Simulator: faqat matn paragraphlari (jadval 7.5pt va formulalar alohida)
    sim = 0
    first = True
    for p in paras:
        if p.startswith('[['):
            continue
        sim += L.para_lines(p, 10, L.LEFT_W, False, 0 if first else L.INDENT)
        first = False
    ok = 'OK ' if abs(sim - n_pdf) <= 0 else 'DIFF'
    if sim == n_pdf:
        tot_ok += 1
    else:
        tot_bad += 1
    print(f"{ok} SEC{si:2d}  pdf={n_pdf:3d}  sim={sim:3d}  diff={sim-n_pdf:+d}  | {title[:44]}")
print(f"\nMOS: {tot_ok}/11")

print("\n=== Jadval qator balandligi: PDF chiziqlari vs simulator ===")
tabs = json.loads((L.ROOT / 'matn' / '07_03_jadvallar.json').read_text())
for pi, (lo, hi) in [(1, (440, 802)), (10, (350, 680)), (13, (410, 700))]:
    ys = sorted({round(dr['rect'].y0, 1) for dr in d[pi - 1].get_drawings()
                 if dr['rect'].y0 > lo and dr['rect'].y1 < hi and dr['rect'].width > 200})
    print(f"s{pi}: PDF qator chegaralari ({len(ys)}): {ys}")
