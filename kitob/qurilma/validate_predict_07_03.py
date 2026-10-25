#!/usr/bin/env python3
"""Prediktor validatsiyasi: chap ustun balandligini iter-1 PDF bilan solishtiradi.

Faqat MD o'zgarmagan bo'limlar (2,3,5,7,8,9,10) solishtiriladi — ular uchun
PDF o'lchovi ham prediktorga mos bo'lishi kerak.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layout_07_03 as L
import predict_07_03 as P

PDF_L = {2: 610.2, 3: 581.9, 5: 557.9, 7: 655.6, 8: 599.4, 9: 706.8, 10: 594.9}
PDF_R = {2: 527.4, 3: 384.0, 5: 372.3, 7: 384.6, 8: 508.1, 10: 384.0}

rows = P.predict(verbose=False)
print("SEC | pred_L   PDF_L   xato | pred_R   PDF_R   xato")
errs = []
for i, t, Lh, R in rows:
    if i not in PDF_L:
        continue
    dl = Lh - PDF_L[i]
    dr = R - PDF_R.get(i, 0)
    errs.append(abs(dl))
    print(f"{i:3d} | {Lh:6.1f} {PDF_L[i]:7.1f} {dl:+6.1f} | {R:6.1f} {PDF_R.get(i,0):7.1f} {dr:+6.1f}")
if errs:
    print(f"\nO'rtacha |xato| (chap): {sum(errs)/len(errs):.1f} pt;  maksimal: {max(errs):.1f} pt")
