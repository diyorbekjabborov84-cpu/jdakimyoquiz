#!/usr/bin/env python3
"""Terminologiya tozartuvi — 2-davr: qo‘lda tekshirilgan aniq iboralar."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = []
for pat in ['matn/*.md', 'matn/*.json', 'qurilma/*.py', 'dizayn.md', 'reja.md', 'mundarija.md',
            'boblar/*.md', 'README.md']:
    TARGETS += sorted(ROOT.glob(pat))

REPL = [
    # --- qayta-qayta takrorlangan iboralar ---
    ('taxminiy hisobda', 'taxminiy hisobda'),
    ('taxminiy hisobda', 'taxminiy hisobda'),
    ('Taxminiy hisobda', 'Taxminiy hisobda'),
    ('Hisoblar va shartli taxminlar', 'Hisoblar va shartli taxminlar'),
    ('hisoblar va shartli taxminlar', 'hisoblar va shartli taxminlar'),
    ('Shartli hisob (lgK', 'Shartli hisob (lgK'),
    ('shartli hisob (lgK', 'shartli hisob (lgK'),
    ('ochiq shartli hisoblar;', 'ochiq shartli hisoblar;'),
    ('ochiq shartli hisoblar ', 'ochiq shartli hisoblar '),
    ('Taxminiy hisobda', 'Taxminiy hisobda'),

    # --- 1.1–1.8 ---
    ('bu yondashuv ham barcha', 'bu yondashuv ham barcha'),
    ('elektron juft tasviri bilan', 'elektron juft tasviri bilan'),
    ('oddiy eritma hisobi bilan', 'oddiy eritma hisobi bilan'),
    ('o‘z hisobi va ma’lumotlarini', 'o‘z hisobi va ma’lumotlarini'),
    ('tajribaviy hisobi emas', 'tajribaviy hisobi emas'),
    ('Lokal kvadratik konseptual tasvir;', 'Lokal kvadratik konseptual tasvir;'),
    ('to‘liq tasviri emas', 'to‘liq tasviri emas'),
    ('Yondashuv tanlashni', 'Yondashuv tanlashni'),
    ('boshqa ikki yondashuv', 'boshqa ikki yondashuv'),
    ('Javoblarda hisobni, fazani va yakuniy', 'Javoblarda hisobni, fazani va yakuniy'),
    ('dipol hisobi simmetriya', 'dipol hisobi simmetriya'),
    ('faraziy vektor hisobi', 'faraziy vektor hisobi'),
    ('chiroyli tasvir', 'chiroyli tasvir'),
    ('d-orbital tasviri isboti', 'd-orbital tasviri isboti'),
    ('ideal monoprotik HA hisobi', 'ideal monoprotik HA hisobi'),
    ('Fosfit tasviri va α grafik', 'Fosfit tasviri va α grafik'),
    ('elektron bog‘lanish tasviri turli', 'elektron bog‘lanish tasviri turli'),
    ('oktaedrik tasvir alohida', 'oktaedrik tasvir alohida'),
    ('to‘liq fizik tasviri deb', 'to‘liq fizik tasviri deb'),
    ('bu hisob shu tanlangan konstantalar bilan izchil olib borilgan',
     'bu hisob shu tanlangan konstantalar bilan izchil olib borilgan'),
    ('## Grafik hisobi va tekshiruv', '## Grafik hisobi va tekshiruv'),
    ('H₂SO₅ tasviri, fosfat grafik', 'H₂SO₅ tasviri, fosfat grafik'),

    # --- 3.1–3.6 ---
    ('qabul qilingan shart ichidagi', 'qabul qilingan shart ichidagi'),
    ('# 3.1. Kₐ, pKₐ, α — shartli hisob, manbalar', '# 3.1. Kₐ, pKₐ, α — shartli hisob, manbalar'),
    ('25 °C uchun', '25 °C uchun'),
    ('ikkita shartli hisob tanlandi', 'ikkita shartli hisob tanlandi'),
    ('Haqiqiy fosfat shu shartli hisob bilan', 'Haqiqiy fosfat shu shartli hisob bilan'),
    ('### Harorat hisobi', '### Harorat hisobi'),
    ('Endotermik holatda T ortishi bilan', 'Endotermik holatda T ortishi bilan'),
    ('ekzotermik holatda oshiradi', 'ekzotermik holatda oshiradi'),
    ('hisobni yondashuv bilan tanlash', 'hisobni yondashuv bilan tanlash'),
    ('faollik taxminlari faqat', 'faollik taxminlari faqat'),
    ('Tayoqchalar to‘liq bog‘ tartibini aks ettirmaydi',
     'Tayoqchalar to‘liq bog‘ tartibini aks ettirmaydi'),
    ('tarkib va balans hisobiy tekshiruv bilan tekshiriladi',
     'tarkib va balans hisobiy tekshiruv bilan tekshiriladi'),
    ('HIn/In⁻ hisobi,', 'HIn/In⁻ hisobi,'),
    ('aniq asbob chizmasi yoki', 'aniq asbob chizmasi yoki'),
    ('ulanish tasviri, nitro', 'ulanish tasviri, nitro'),
    ('ulanish tasviri, fenolyat', 'ulanish tasviri, fenolyat'),
    ('To‘liq fosfat hisobi', 'To‘liq fosfat hisobi'),
    ('noto‘g‘ri shartli hisob ham kalkulyatorda', 'noto‘g‘ri shartli hisob ham kalkulyatorda'),
    ('## Hisob usuli', '## Hisob usuli'),
    ('25 °C ideal konsentratsion hisob', '25 °C ideal konsentratsion hisob'),
    ('Taxminiy qiymatlar uchun k₀=', 'Taxminiy qiymatlar uchun k₀='),
    ('tushuntiradigan shartli hisob bilan', 'tushuntiradigan shartli hisob bilan'),
    ('mustaqil shartli hisob tahlili bilan', 'mustaqil shartli hisob tahlili bilan'),
    ('boshqa mustaqil o‘quv hisob', 'boshqa mustaqil o‘quv hisob'),
    ('Doimiy Ea taxminiy qiymati,', 'Doimiy Ea taxminiy qiymati,'),

    # --- 4.1–4.5 ---
    ('to‘liq suvli sharoitda neytral', 'to‘liq suvli sharoitda neytral'),
    ('kalorimetr hisobi', 'kalorimetr hisobi'),
    ('H₃O⁺ ulanish tasviri', 'H₃O⁺ ulanish tasviri'),
    ('Barcha grafiklar original taxminiy hisoblar;', 'Barcha grafiklar original taxminiy hisoblar;'),
    ('4 ta tasvir:', '4 ta tasvir:'),
    ('sun’iy taxminiy qiymatlar ishlatilgan', 'sun’iy taxminiy qiymatlar ishlatilgan'),
    ('shartli hisob: kuchliroq katod', 'shartli hisob: kuchliroq katod'),
    ('shu shartli hisob doirasida', 'shu shartli hisob doirasida'),
    ('shartli hisob parda saqlanishini', 'shartli hisob parda saqlanishini'),
    ('boshqa shartli etalon bilan', 'boshqa shartli etalon bilan'),
    ('mos kinetik shartli hisob va taxminan', 'mos kinetik shartli hisob va taxminan'),
    ('oksidlanish shartli hisobi uchun', 'oksidlanish shartli hisobi uchun'),
    ('ixtiyoriy shartli etalon', 'ixtiyoriy shartli etalon'),
    ('bo‘lakli taxminiy qiymati', 'bo‘lakli taxminiy qiymati'),
    ('1604 ta shartli hisob satri', '1604 ta shartli hisob satri'),
    ('qisqartirilgan shartli hisob olinadi', 'qisqartirilgan shartli hisob olinadi'),
    ('chizilgan shartli hisob', 'chizilgan shartli hisob'),
    ('**Erkin ligand bo‘yicha shartli hisob.**', '**Erkin ligand bo‘yicha shartli hisob.**'),
    ('**Amfoterlik bo‘yicha shartli hisob.**', '**Amfoterlik bo‘yicha shartli hisob.**'),
    ('**Tanlab cho‘ktirish bo‘yicha shartli hisob.**', '**Tanlab cho‘ktirish bo‘yicha shartli hisob.**'),
    ('**Termodinamik shartli hisob.**', '**Termodinamik shartli hisob.**'),
    ('**Kinetik shartli hisob.**', '**Kinetik shartli hisob.**'),
    ('Hisob chegarasini ham aytish kerak', 'Hisob chegarasini ham aytish kerak'),
    ('Shartli hisob uchun A=', 'Shartli hisob uchun A='),
    ('Bu shartli hisob to‘g‘ridan-to‘g‘ri', 'Bu shartli hisob to‘g‘ridan-to‘g‘ri'),

    # --- 5.1–5.4 ---
    ('Shartli hisobda (ideal gaz', 'Shartli hisobda (ideal gaz'),
    ('Shartli hisob zanjirdan', 'Shartli hisob zanjirdan'),
    ('Shartli hisob zanjir:', 'Shartli hisob zanjir:'),
    ('**Muvozanat bo‘yicha shartli hisob.**', '**Muvozanat bo‘yicha shartli hisob.**'),
    ('**Kaskad bo‘yicha shartli hisob.**', '**Kaskad bo‘yicha shartli hisob.**'),
    ('**Ajratish bo‘yicha shartli hisob.**', '**Ajratish bo‘yicha shartli hisob.**'),
    ('1000 t pyrit bo‘yicha shartli hisob', '1000 t pyrit bo‘yicha shartli hisob'),
    ('Ajratish zanjiri bo‘yicha shartli hisob:', 'Ajratish zanjiri bo‘yicha shartli hisob:'),
    ('**Erushchanlik bo‘yicha shartli hisob.**', '**Erushchanlik bo‘yicha shartli hisob.**'),
    ('**Kompleks niqoblash bo‘yicha shartli hisob.**', '**Kompleks niqoblash bo‘yicha shartli hisob.**'),
    ('**Tozalash kaskadi bo‘yicha shartli hisob.**', '**Tozalash kaskadi bo‘yicha shartli hisob.**'),
    ('**Rektifikatsiya bo‘yicha shartli hisob.**', '**Rektifikatsiya bo‘yicha shartli hisob.**'),
    ('**Ion almashinuv bo‘yicha shartli hisob.**', '**Ion almashinuv bo‘yicha shartli hisob.**'),
    ('Shartli hisob (ΔvapH = 40,657', 'Shartli hisob (ΔvapH = 40,657'),
    ('Shartli hisob (toluen bilan)', 'Shartli hisob (toluen bilan)'),
    ('Ushbu shartli hisob uchta xulosa beradi', 'Ushbu shartli hisob uchta xulosa beradi'),
    ('Taqsimot bo‘yicha shartli hisob:', 'Taqsimot bo‘yicha shartli hisob:'),
    ('Usullarning nisbiy energetik sarfi (shartli hisob,', 'Usullarning nisbiy energetik sarfi (shartli hisob,'),
    ('**QuRITish kinetikasi bo‘yicha shartli hisob.**', '**QuRITish kinetikasi bo‘yicha shartli hisob.**'),
    ('Shartli hisob: m₁ = 5,00 g', 'Shartli hisob: m₁ = 5,00 g'),
    ('to‘rt usulning shartli hisob energiyasi', 'to‘rt usulning shartli hisob energiyasi'),
    ('grafik hisobi. U uch savolga', 'grafik hisobi. U uch savolga'),
    ('virtual raqamli egizin', 'virtual raqamli egizin'),

    # --- 6.1–6.5 ---
    ('## 3. Suvli HI: kislotalik, shartli hisob va guruh taqqoslash',
     '## 3. Suvli HI: kislotalik, shartli hisob va guruh taqqoslash'),
    ('Shartli hisob bo‘yicha 1,000 g KIO₃', 'Shartli hisob bo‘yicha 1,000 g KIO₃'),
    ('Spetsiatsiya shartli hisobi faolik', 'Spetsiatsiya shartli hisobi faolik'),
    ('standartlash va yodometriya bo‘yicha shartli hisob', 'standartlash va yodometriya bo‘yicha shartli hisob'),
    ('standartlash bo‘yicha shartli hisob', 'standartlash bo‘yicha shartli hisob'),
    ('bog‘liqligi (shartli hisob);', 'bog‘liqligi (shartli hisob);'),
    ('Shartli hisob chegarasi: faolik', 'Shartli hisob chegarasi: faolik'),

    # --- qurilma generatorlarida ---
    ('Kₐ = 10⁻⁵ bo‘yicha shartli hisob.', 'Kₐ = 10⁻⁵ bo‘yicha shartli hisob.'),
    ('mualliflik hisobiy shartli hisobi;', 'mualliflik hisobiy shartli hisobi;'),
    ('Lokal kvadratik shartli hisob,', 'Lokal kvadratik shartli hisob,'),
    ('Ideal shartli hisob.', 'Ideal shartli hisob.'),
    ('Ikki shaklli shartli hisob.', 'Ikki shaklli shartli hisob.'),
    ('tarkibi aks ettirmaydi.', 'tarkibi aks ettirmaydi.'),
    ('normallangan shartli hisob.', 'normallangan shartli hisob.'),
    ('IR grafik — faraziy shartli hisob,', 'IR grafik — faraziy shartli hisob,'),
    ('α grafigi ideal shartli hisob,', 'α grafigi ideal shartli hisob,'),
    ('O–O bog‘isiz tasvir.', 'O–O bog‘isiz tasvir.'),
    ('Kontinuum hisobi', 'Kontinuum hisobi'),
    ('doimiy entalpiya bo‘yicha shartli hisob', 'doimiy entalpiya bo‘yicha shartli hisob'),
    ('1-bo‘lim K=4 shartli hisobi emas', '1-bo‘lim K=4 shartli hisobi emas'),
    ('doimiy erish bo‘yicha shartli hisob;', 'doimiy erish bo‘yicha shartli hisob;'),
    ('boshqa shartli etalon bilan', 'boshqa shartli etalon bilan'),
    ('shartli hisob egri chizig‘i.', 'shartli hisob egri chizig‘i.'),
    ('1,6×10⁻¹⁰ bo‘yicha shartli hisob.', '1,6×10⁻¹⁰ bo‘yicha shartli hisob.'),
    ('xayoliy shartli hisob.', 'xayoliy shartli hisob.'),
    ('shartli hisob egri chizig‘i.', 'shartli hisob egri chizig‘i.'),
    ('taxminiy hisob grafiklari', 'taxminiy hisob grafiklari'),
    ('taxminiy hisob grafigi', 'taxminiy hisob grafigi'),
    ('taxminiy hisoblar,', 'taxminiy hisoblar,'),
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
