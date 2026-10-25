#!/usr/bin/env python3
"""Iter-1 PDF dan span-asosida aniq o'lchov (simulator kalibratsiyasi uchun)."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layout_07_03 as L
import pymupdf as fitz

d = fitz.open(L.PDF)
SEC_PAGES = [(1, [1, 2]), (2, [3]), (3, [4]), (4, [5]), (5, [6]), (6, [7]),
             (7, [8]), (8, [9]), (9, [10, 11]), (10, [12]), (11, [13, 14])]

print("=== Chap/o'ng ustun kontent balandligi (span klassifikatsiyasi bilan) ===")
data = {}
for sec, pages in SEC_PAGES:
    L_top, R_top = None, None
    L_bot, R_bot = 0, 0
    L_pages, R_pages = {}, {}
    for pi in pages:
        page = d[pi - 1]
        for bl in page.get_text('dict')['blocks']:
            if bl['type'] != 0:
                continue
            for ln in bl['lines']:
                for s in ln['spans']:
                    x0, y0, x1, y1 = s['bbox']
                    if y1 > 805 or y0 < 35:
                        continue
                    cx = (x0 + x1) / 2
                    side = 'L' if cx < 430 else 'R'
                    if sec == 1 and y0 < 140:
                        continue           # band + sarlavha
                    if sec > 1 and y0 < 92:
                        continue           # band + sarlavha
                    if side == 'L':
                        L_top = y0 if L_top is None else min(L_top, y0)
                        L_bot = max(L_bot, y1)
                        L_pages.setdefault(pi, [y0, y1])
                        L_pages[pi][0] = min(L_pages[pi][0], y0)
                        L_pages[pi][1] = max(L_pages[pi][1], y1)
                    else:
                        R_top = y0 if R_top is None else min(R_top, y0)
                        R_bot = max(R_bot, y1)
                        R_pages.setdefault(pi, [y0, y1])
                        R_pages[pi][0] = min(R_pages[pi][0], y0)
                        R_pages[pi][1] = max(R_pages[pi][1], y1)
    lh = sum(v[1] - v[0] for v in L_pages.values())
    rh = sum(v[1] - v[0] for v in R_pages.values())
    data[sec] = dict(L=lh, R=rh, L_pages=L_pages, R_pages=R_pages)
    print(f"SEC{sec:2d}  L={lh:7.1f} (bud {L.LEFT_BUDGET:5.1f}, {L.LEFT_BUDGET-lh:+6.1f})   "
          f"R={rh:7.1f} (bud {L.RIGHT_BUDGET:5.1f}, {L.RIGHT_BUDGET-rh:+6.1f})")

Path('/tmp/p73_heights.json').write_text(json.dumps(data, ensure_ascii=False, indent=1))
