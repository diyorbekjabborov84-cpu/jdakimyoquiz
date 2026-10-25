#!/usr/bin/env python3
"""7.3 PDF sahifa xaritasi: har bo‘limning chap/o‘ng ustun zichligi (footer/header chiqarilgan)."""
import sys, re
import fitz

BOTTOM = 802.0   # pastki kontent chekkasi (842 - 1.4 sm)

path = sys.argv[1]
d = fitz.open(path)
print('FAYL: %s  |  sahifalar: %d' % (path, d.page_count))

sec_re = re.compile(r'^(\d+)\.\s')
sections = []
for pi in range(d.page_count):
    for bl in d[pi].get_text('dict')['blocks']:
        if bl['type'] != 0:
            continue
        for ln in bl['lines']:
            sp = ln['spans'][0]
            if 12.5 < sp['size'] < 14.5 and sp['bbox'][0] < 60:
                t = ''.join(s['text'] for s in ln['spans']).strip()
                m = sec_re.match(t)
                if m:
                    sections.append((int(m.group(1)), pi, t))

print('bo‘lim boshlanish sahifalari:', [s[1] + 1 for s in sections])
print()
print('SEC  sahifa          chap_y0   chap_y1  chap_h   o‘ng_y1  o‘ng_h   joy_mavjud  xulosa')
for k, (num, start, title) in enumerate(sections):
    end = sections[k + 1][1] if k + 1 < len(sections) else d.page_count
    pages = list(range(start, end))
    lmin, lmax = 1e9, 0.0
    rmin, rmax = 1e9, 0.0
    for pi in pages:
        for bl in d[pi].get_text('dict')['blocks']:
            if bl['type'] != 0:
                continue
            x0, y0, y1 = bl['bbox'][0], bl['bbox'][1], bl['bbox'][3]
            if y1 > 805 or y0 < 35:      # footer / header
                continue
            if x0 < 430:
                lmin = min(lmin, y0); lmax = max(lmax, y1)
            else:
                rmin = min(rmin, y0); rmax = max(rmax, y1)
        for im in d[pi].get_images(full=True):
            for r in d[pi].get_image_rects(im[0]):
                if r.y1 > 805 or r.y0 < 35:
                    continue
                if r.x0 < 430:
                    lmin = min(lmin, r.y0); lmax = max(lmax, r.y1)
                else:
                    rmin = min(rmin, r.y0); rmax = max(rmax, r.y1)
    lh = lmax - lmin
    rh = rmax - rmin
    avail = BOTTOM - lmin
    ok = 'OK' if (lh <= avail and rh <= avail) else 'OVERFLOW'
    print('SEC %2d  %-14s %7.1f %8.1f %7.1f %8.1f %7.1f   %7.1f   %s  %s' % (
        num, ','.join(str(p + 1) for p in pages), lmin, lmax, lh, rmax, rh, avail, ok, title[:40]))

print('\nrasmlar (balandlik pt):')
for pi in range(d.page_count):
    for im in d[pi].get_images(full=True):
        for r in d[pi].get_image_rects(im[0]):
            print('  s.%d  x0=%.0f y=%.0f-%.0f  h=%.0f w=%.0f' % (
                pi + 1, r.x0, r.y0, r.y1, r.height, r.width))
