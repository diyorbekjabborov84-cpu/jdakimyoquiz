#!/usr/bin/env python3
"""Iter-1 PDF: har bir sahifa uchun chap/o'ng ustun kontent chegaralari (validatsiya)."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layout_07_03 as L
import pymupdf as fitz

d = fitz.open(L.PDF)
print('sahifalar:', d.page_count)
print("sah |  CHAP y0-y1 (h)          |  O'NG y0-y1 (h)          | izoh")
for pi in range(d.page_count):
    page = d[pi]
    Lspans, Rspans = [], []
    for bl in page.get_text('dict')['blocks']:
        if bl['type'] != 0:
            continue
        for ln in bl['lines']:
            for s in ln['spans']:
                x0, y0, x1, y1 = s['bbox']
                if y1 > 806 or y0 < 34:
                    continue
                cx = (x0 + x1) / 2
                (Lspans if cx < 430 else Rspans).append((y0, y1, s['text']))
    def rng(sp):
        if not sp:
            return '—'
        return f"{min(a for a,_,_ in sp):6.1f}-{max(b for _,b,_ in sp):6.1f} ({max(b for _,b,_ in sp)-min(a for a,_,_ in sp):5.1f})"
    # birinchi qator matni
    first = ''
    allsp = sorted(Lspans + Rspans)
    if allsp:
        first = allsp[0][2][:34]
    print(f"{pi+1:3d} | {rng(Lspans):26s} | {rng(Rspans):26s} | {first}")
