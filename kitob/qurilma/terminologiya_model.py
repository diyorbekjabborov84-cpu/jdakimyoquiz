#!/usr/bin/env python3
"""Terminologiya tozartuvi: «taxminiy hisob» → o‘zbekcha ekvivalentlar.

Kitob bo‘ylab ishlatilgan «taxminiy hisob» so‘zi o‘zbek kimyo terminologiyasida
ma’lum emas. Bu skript so‘zni kontekstga qarab almashtiradi:

  nazariy kontekst   : Arrhenius/Lewis nazariyasi → «... nazariyasi»
  hisobiy kontekst   : taxminiy hisoblar → taxminiy hisoblar; taxminiy egri chiziq →
                        taxminiy egri chiziq; taxminiy chegarasi → taxminiy chegarasi;
                        Taxmin A–E → Taxmin A–E
  boshqa kontekst     : qo‘lda qolgan barcha holatlar uchun «taxminiy hisob» oilasi.

Foydalanish:  python3 terminologiya_model.py            (quruq ko‘rish, o‘zgartirmaydi)
               python3 terminologiya_model.py --apply    (fayllarni o‘zgartiradi)
"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

TARGETS = []
for pat in ['matn/*.md', 'matn/*.json', 'qurilma/*.py', 'dizayn.md', 'reja.md', 'mundarija.md',
            'boblar/*.md', 'README.md']:
    TARGETS += sorted(ROOT.glob(pat))

# (qidiruv, almashtirish) — tartib muhim: ko‘p so‘zli iboralar avval.
RULES = [
    # --- nazariy kontekst (1–2-bob) ---
    (r'Arrhenius nazariyasining', 'Arrhenius nazariyasining'),
    (r'Arrhenius nazariyasiga', 'Arrhenius nazariyasiga'),
    (r'Arrhenius nazariyasi', 'Arrhenius nazariyasi'),
    (r'Brønsted[–-]Lowry taxminiy hisobi', 'Brønsted–Lowry nazariyasi'),
    (r'Lewis nazariyasi', 'Lewis nazariyasi'),
    (r'Usanovich nazariyasi', 'Usanovich nazariyasi'),
    (r'Lyuks[–-]Flud taxminiy hisobi', 'Lyuks–Flud nazariyasi'),
    (r'Pearson nazariyasi', 'Pearson nazariyasi'),
    (r'zarrachalar tasviri', 'zarrachalar tasviri'),
    (r'ion tasviri', 'ion tasviri'),
    (r'kristall fazaning tuzilmasi', 'kristall fazaning tuzilmasi'),
    (r'fosfit tuzilmasi', 'fosfit tuzilmasi'),
    (r'endotermik holat', 'endotermik holat'),
    (r'kontinuum yaqinlashuvi ekstrapolyatsiyasi', 'kontinuum yaqinlashuvi ekstrapolyatsiyasi'),
    (r'ideal erituvchi sharoitida', 'ideal erituvchi sharoitida'),
    (r'ideal erituvchi sharoiti', 'ideal erituvchi sharoiti'),
    (r'ideal suvli sharoitida', 'ideal suvli sharoitida'),
    (r'ideal sharoitning', 'ideal sharoitning'),
    (r'ideal sharoitda', 'ideal sharoitda'),
    (r'ideal sharoit', 'ideal sharoit'),
    (r'ideal konsentratsiyon sharoitiga', 'ideal konsentratsiyon sharoitiga'),
    (r'statistik tasvir', 'statistik tasvir'),

    # --- tasvir / sharoit / yondashuv konteksti (1–3-bob nazariy qismi) ---
    (r'shar[–-]tayoqcha taxminiy hisobi', 'shar–tayoqcha tasviri'),
    (r'shar[–-]tayoqcha taxminiy hisob', 'shar–tayoqcha tasvir'),
    (r'molekulyar tasviri', 'molekulyar tasviri'),
    (r'o[ʻ‘\'’]quv taxminiy hisobi', 'o‘quv tasviri'),
    (r'hajmli tasvirlar', 'hajmli tasvirlar'),
    (r'hajmli tasvir', 'hajmli tasvir'),
    (r'eritmadagi ionlar tasviri', 'eritmadagi ionlar tasviri'),
    (r'suyultirilgan eritma sharoiti', 'suyultirilgan eritma sharoiti'),
    (r'kislota sharoiti', 'kislota sharoiti'),
    (r'shartli ifoda', 'shartli ifoda'),
    (r'kvadrat yechim', 'kvadrat yechim'),
    (r'Born kontinuum yondashuvi', 'Born kontinuum yondashuvi'),
    (r'kontinuum yondashuv', 'kontinuum yondashuv'),
    (r'1:1 tizimi', '1:1 tizimi'),
    (r'ikki shaklli tizim', 'ikki shaklli tizim'),
    (r'ideal monoprotik sharoit', 'ideal monoprotik sharoit'),
    (r'ideal suvli sharoit', 'ideal suvli sharoit'),
    (r'soddalashtirilgan sharoit', 'soddalashtirilgan sharoit'),
    (r'shartli farazlar', 'shartli farazlar'),
    (r'shartli faraz', 'shartli faraz'),
    (r'yondashuv tanlashni', 'yondashuv tanlashni'),
    (r'yondashuv tanlash', 'yondashuv tanlash'),
    (r'yondashuvni tanlang', 'yondashuvni tanlang'),
    (r'yondashuvni tanlash', 'yondashuvni tanlash'),
    (r'yondashuvni aniqlash', 'yondashuvni aniqlash'),
    (r'taxminiy hisob va boshlang[ʻ‘\'’]ich tarkib', 'sharoit va boshlang‘ich tarkib'),
    (r'Nazariy yondashuv', 'Nazariy yondashuv'),
    (r'yagona yondashuv', 'yagona yondashuv'),
    (r'bir yondashuvda', 'bir yondashuvda'),
    (r'boshqa yondashuvda', 'boshqa yondashuvda'),
    (r'har qanday yondashuv', 'har qanday yondashuv'),
    (r'ikki yondashuvni', 'ikki yondashuvni'),
    (r'bitta yondashuvni', 'bitta yondashuvni'),
    (r'asosiy yondashuvni', 'asosiy yondashuvni'),
    (r'hisobiy grafik', 'hisobiy grafik'),
    (r'hisobiy grafiklar', 'hisobiy grafiklar'),
    (r'Ikki shartli egri chiziq', 'Ikki shartli egri chiziq'),
    (r'kristall tuzilmasi', 'kristall tuzilmasi'),
    (r'tuzilma tasviri', 'tuzilma tasviri'),
    (r'elektron energiyasi tasviri', 'elektron energiyasi tasviri'),
    (r'lokal sharoitda', 'lokal sharoitda'),
    (r'faraziy tizimni', 'faraziy tizimni'),
    (r'sodda tasvir', 'sodda tasvir'),
    (r'ideal statistik tasvir', 'ideal statistik tasvir'),
    (r'tuzilmalar tasvirlari', 'tuzilmalar tasvirlari'),
    (r'faqat yondashuv', 'faqat yondashuv'),

    # --- taxminiy hisob A–E (hisob etiketalari) ---
    (r'\bModel ([A-Z])\b', r'Taxmin \1'),

    # --- hisobiy kontekst ---
    (r'taxminiy hisob egri chizig[ʻ‘\'’]i', 'taxminiy egri chiziq'),
    (r'taxminiy egri chiziqlar', 'taxminiy egri chiziqlar'),
    (r'taxminiy hisob chizig[ʻ‘\'’]i', 'taxminiy chiziq'),
    (r'taxminiy chiziqlar', 'taxminiy chiziqlar'),
    (r'taxminiy hisoblar', 'taxminiy hisoblar'),
    (r'taxminiy hisoblar', 'taxminiy hisoblar'),
    (r'taxminiy hisobda', 'taxminiy hisobda'),
    (r'taxminiy hisob uchun', 'taxminiy hisob uchun'),
    (r'taxminiy hisob', 'taxminiy hisob'),
    (r'taxminiy chegarolar', 'taxminiy chegarolar'),
    (r'taxminiy chegarasi', 'taxminiy chegarasi'),
    (r'taxminiy chegaralar', 'taxminiy chegaralar'),
    (r'taxminiy natijalar', 'taxminiy natijalar'),
    (r'taxminiy natija', 'taxminiy natija'),
    (r'taxminiy parametrlar', 'taxminiy parametrlar'),
    (r'taxminiy parametrlar', 'taxminiy parametrlar'),
    (r'taxminiy qiymat', 'taxminiy qiymat'),
    (r'taxminiy qiymat', 'taxminiy qiymat'),
    (r'taxminiy hisob bo[ʻ‘\'’]yicha', 'taxminiy hisob bo‘yicha'),
    (r'shartli hisoblardan olingan', 'shartli hisoblardan olingan'),
    (r'taxminiy hisoblash', 'taxminiy hisoblash'),
    (r'taxminiy hisoblashda', 'taxminiy hisoblashda'),

    # --- qolgan ko‘pliklar ---
    (r'taxminiy hisobda', 'taxminiy hisobda'),
    (r'taxminiy hisobdan', 'taxminiy hisobdan'),
    (r'taxminiy hisobning', 'taxminiy hisobning'),
    (r'taxminiy hisobningi', 'taxminiy hisobningi'),
    (r'taxminiy hisobni', 'taxminiy hisobni'),
    (r'taxminiy hisobini', 'taxminiy hisobini'),
    (r'taxminiy hisobidan', 'taxminiy hisobidan'),
    (r'taxminiy hisobdagi', 'taxminiy hisobdagi'),
    (r'taxminiy hisobiga', 'taxminiy hisobiga'),
    (r'taxminiy hisobi\b', 'taxminiy hisobi'),
    (r'taxminiy hisoblari', 'taxminiy hisoblari'),
    (r'taxminiy hisoblarning', 'taxminiy hisoblarning'),
    (r'taxminiy hisoblarni', 'taxminiy hisoblarni'),
    (r'taxminiy hisoblarda', 'taxminiy hisoblarda'),
    (r'taxminiy hisoblarga', 'taxminiy hisoblarga'),
    (r'taxminiy hisoblarni', 'taxminiy hisoblarni'),
    (r'taxminiy hisobimizda', 'taxminiy hisobimizda'),
    (r'taxminiy hisobining', 'taxminiy hisobining'),
    (r'shartli hisobga', 'shartli hisobga'),
    (r'taxminiy hisoblar', 'taxminiy hisoblar'),
    (r'taxminiy hisobmi', 'taxminiy hisobmi'),
    (r'\bmodel\b', 'taxminiy hisob'),
    (r'\bModel\b', 'Taxminiy hisob'),
]

APPLY = '--apply' in sys.argv
report = {}
leftovers = []
total = 0

for path in TARGETS:
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    orig = text
    for pat, rep in RULES:
        text, n = re.subn(pat, rep, text)
        if n:
            report[(pat, rep)] = report.get((pat, rep), 0) + n
            total += n
    if text != orig:
        if APPLY:
            path.write_text(text)
        else:
            leftovers.append(path)

print('Topilgan o‘zgarishlar: %d' % total)
for (pat, rep), n in sorted(report.items(), key=lambda x: -x[1]):
    print('  %4d  %-42s → %s' % (n, pat, rep))

# qolgan «taxminiy hisob» so‘zlari — qo‘lda ko‘rib chiqish uchun
print('\nQolgan «taxminiy hisob» qatlamlari (qo‘lda tekshirish):')
left = 0
for path in TARGETS:
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    for i, line in enumerate(text.split('\n'), 1):
        if re.search(r'taxminiy hisob', line, re.I) and 'peroksid_model' not in line:
            print('  %s:%d: %s' % (path.relative_to(ROOT), i, line.strip()[:190]))
            left += 1
print('\nJami qolgan qator: %d' % left)
if APPLY:
    print('O‘zgartirish qo‘llandi.')
else:
    print('(--apply bermasdan hech narsa o‘zgartirilmadi)')
