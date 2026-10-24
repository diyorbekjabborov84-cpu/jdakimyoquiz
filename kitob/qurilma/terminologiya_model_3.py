#!/usr/bin/env python3
"""Terminologiya tozartuvi — 3-davr: rasm ichidagi matn, sarlavha va imzo matnlari."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = []
for pat in ['matn/*.md', 'matn/*.json', 'qurilma/*.py', 'dizayn.md', 'reja.md', 'mundarija.md',
            'boblar/*.md', 'README.md']:
    TARGETS += sorted(ROOT.glob(pat))

REPL = [
    # --- umumiy iboralar ---
    ('(shartli hisob)', '(shartli hisob)'),
    ('(shartli hisob ', '(shartli hisob '),
    ('shartli hisob zanjiri', 'shartli hisob zanjiri'),
    ('shartli hisob zanjirdan', 'shartli hisob zanjirdan'),
    ('Shartli hisob zanjiri', 'Shartli hisob zanjiri'),
    ('shartli hisob energiyasi', 'shartli hisob energiyasi'),
    ('shartli hisob pH', 'shartli hisob pH'),
    ('shartli hisob ulushlari', 'shartli hisob ulushlari'),
    ('shartli hisob shartlari', 'shartli hisob shartlari'),
    ('shartli hisobga', 'shartli hisobga'),
    ('yondashuvga va', 'yondashuvga va'),
    ('Shartli hisobdan tekshiruvgacha', 'Shartli hisobdan tekshiruvgacha'),
    ('shartli hisobni dalil', 'shartli hisobni dalil'),
    ('shartli hisob tanlash', 'shartli hisob tanlash'),
    ('Shartli hisob tanlash', 'Shartli hisob tanlash'),
    ('shartli hisob zanjiri', 'shartli hisob zanjiri'),

    # --- rasm ichidagi matn (draw_*.py) ---
    ('Bog‘ energiyasi hisobi', 'Bog‘ energiyasi hisobi'),
    ('Teng bog‘ dipollari hisobi', 'Teng bog‘ dipollari hisobi'),
    ('Ko‘k: erkin X–H hisobi', 'Ko‘k: erkin X–H hisobi'),
    ('Bronza: bog‘langan hisob', 'Bronza: bog‘langan hisob'),
    ('O‘quv tasviri; masshtabsiz', 'O‘quv tasviri; masshtabsiz'),
    ('Nitrat: tekis tasvir', 'Nitrat: tekis tasvir'),
    ('Karbonat: tekis tasvir', 'Karbonat: tekis tasvir'),
    ('H₃O⁺: piramidal tasvir', 'H₃O⁺: piramidal tasvir'),
    ('Ideal bir bosqichli hisob', 'Ideal bir bosqichli hisob'),
    ('B(OH)₃: tekis tasvir', 'B(OH)₃: tekis tasvir'),
    ('HCl: molekulyar tasvir', 'HCl: molekulyar tasvir'),
    ('[SiF₆]²⁻: oktaedrik tasvir', '[SiF₆]²⁻: oktaedrik tasvir'),
    ('Ulanish tasviri; spektr hisoblanmagan', 'Ulanish tasviri; spektr hisoblanmagan'),
    ('Kuchli kislota–NaOH hisobi', 'Kuchli kislota–NaOH hisobi'),
    ('Ideal shartli hisob; tajriba shovqini yo‘q', 'Ideal shartli hisob; tajriba shovqini yo‘q'),
    ('Muvozanat hisobi', 'Muvozanat hisobi'),
    ('Shartli qaytar birinchi tartibli hisob', 'Shartli qaytar birinchi tartibli hisob'),
    ('1-bo‘limdagi K=4 ga mos shartli hisob emas', '1-bo‘limdagi K=4 ga mos shartli hisob emas'),
    ('doimiy shartli hisob', 'doimiy shartli hisob'),
    ('To‘g‘ri chiziq — shartli hisob;', 'To‘g‘ri chiziq — shartli hisob;'),
    ('Tuz bo‘yicha shartli hisob', 'Tuz bo‘yicha shartli hisob'),
    ('Sun’iy anod shartli hisob;', 'Sun’iy anod shartli hisob;'),
    ('Kesishishlar shartli hisobga tegishli', 'Kesishishlar shartli hisobga tegishli'),
    ('Ideal shartli hisob; o‘lchangan parda emas', 'Ideal shartli hisob; o‘lchangan parda emas'),
    ('berilgan shartli hisob', 'berilgan shartli hisob'),
    ('Shartli hisob egri chizig‘i;', 'Shartli hisob egri chizig‘i;'),
    ('Hisobiy shartli hisoblar, tajriba emas', 'Hisobiy shartli hisoblar, tajriba emas'),
    ('Solishtirma shartli hisob;', 'Solishtirma shartli hisob;'),
    ('Ta’rif, mezon va yondashuv', 'Ta’rif, mezon va yondashuv'),

    # --- DOCX imzo va sarlavhalar ---
    ('zarracha tasviri yo‘q', 'zarracha tasviri yo‘q'),
    ('Suvli eritmalar doirasidagi shartli hisob', 'Suvli eritmalar doirasidagi shartli hisob'),
    ('Shartli hisob shartlari asosiy matn', 'Shartli hisob shartlari asosiy matn'),
    ('Yondashuv tanlash yo‘li', 'Yondashuv tanlash yo‘li'),
    ('Suv dimerining idealizatsiyalangan tasviri', 'Suv dimerining idealizatsiyalangan tasviri'),
    ('piramidal tasviri', 'piramidal tasviri'),
    ('tekis tasviri', 'tekis tasviri'),
    ('ulanish tasviri', 'ulanish tasviri'),
    ('Material oqimi shartli hisobi', 'Material oqimi shartli hisobi'),
    ('McCabe-Thiele bosqichlari (shartli hisob)', 'McCabe-Thiele bosqichlari (shartli hisob)'),
    ('plug-flow shartli hisob', 'plug-flow shartli hisob'),
    ('Ishlangan hisob: shartli hisob zanjiri', 'Ishlangan hisob: shartli hisob zanjiri'),
    ('Ishlangan hisob: uch shartli hisob', 'Ishlangan hisob: uch shartli hisob'),
    ('Ishlangan hisob: to‘rt shartli hisob', 'Ishlangan hisob: to‘rt shartli hisob'),
    ('Ishlangan hisob: besh shartli hisob', 'Ishlangan hisob: besh shartli hisob'),
    ('Ideal shartli hisob (−lg c)', 'Ideal shartli hisob (−lg c)'),
    ('Klausius–Klapeiron shartli hisobi', 'Klausius–Klapeiron shartli hisobi'),
    ('25 ta 3D tasvir', '25 ta 3D tasvir'),
    ("[H⁺] hisoblashning 4 sharti", "[H⁺] hisoblashning 4 sharti"),
    ('Seolit g‘ovagi tasviri', 'Seolit g‘ovagi tasviri'),
    ('Hammett', 'Hammett'),
]

APPLY = '--apply' in sys.argv
total = 0
for path in TARGETS:
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    orig = text
    for old, new in REPL:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            total += n
    if text != orig:
        if APPLY:
            path.write_text(text)
        else:
            print('KO‘RILADI:', path.relative_to(ROOT))
print('Jami almashtirish: %d' % total)
print('O‘zgartirildi.' if APPLY else '(--apply bermasdan hech narsa o‘zgartirilmadi)')
