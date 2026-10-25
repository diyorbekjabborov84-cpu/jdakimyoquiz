#!/usr/bin/env python3
"""Bo'lim bo'yicha chap/o'ng ustun balandligi taqsimoti (qaysi element qancha egallashi)."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layout_07_03 as L
from layout_07_03 import para_lines, LEAD10, LEFT_W, RIGHT_W, INDENT, BOT_Y, SEC_TOP, SEC_TOP1, RIGHT_TOP
import predict_07_03 as P

secs = P.md_sections()
tables = json.loads((L.ROOT / 'matn' / '07_03_jadvallar.json').read_text())
notes = json.loads((L.ROOT / 'matn' / '07_03_yonlavhalar.json').read_text())

want = [int(x) for x in sys.argv[1:]] or list(range(1, 12))
for idx in want:
    title, paras = secs[idx - 1]
    print(f"\n===== SEC{idx}: {title} =====")
    tot = 0.0
    first = True
    for p in paras:
        if p.startswith('[[TABLE:'):
            key = p[len('[[TABLE:'):-2]
            h = P.TABLE_CAPTION_H + P.table_h(tables[key]) + 4.5
            n_rows = len(tables[key]['rows'])
            print(f"  jadval {key:14s} {h:7.1f} pt ({n_rows} qator)  {p[:40]}")
            tot += h
            first = False
            continue
        if p.startswith('[[EQ:'):
            key = p[5:-2]
            h = P.eq_group_h(key)
            print(f"  formula {key:13s} {h:7.1f} pt ({len(P.EQ.sulfate_equations()[P.EQ_KEYS.index(key)])} qator)")
            tot += h
            first = False
            continue
        n = para_lines(p, 10, LEFT_W, False, 0 if first else INDENT)
        h = n * P.LEAD10 + 1.5
        print(f"  matn  {len(p):4d} belgi  {n:2d} qator  {h:7.1f} pt  | {p[:52]}")
        tot += h
        first = False
    if idx == 11:
        h = 4.0 + para_lines(P.DISCLAIMER, 8, LEFT_W) * P.LEAD8
        print(f"  disclaimer            {h:7.1f} pt")
        tot += h
        h = 5.0 + P.LEAD9 + 1.0
        print(f"  «Manbalar» sarlavhasi {h:7.1f} pt")
        tot += h
        for ref in P.REFS:
            n = para_lines(ref, 7, LEFT_W)
            h = n * P.REF_LEAD
            print(f"  manba {len(ref):4d} belgi  {n} qator  {h:7.1f} pt | {ref[:44]}")
            tot += h
    bud = BOT_Y - (SEC_TOP1 if idx == 1 else SEC_TOP)
    print(f"  JAMI: {tot:7.1f} pt  |  budjet {bud:7.1f}  |  slack {bud-tot:+7.1f}")
