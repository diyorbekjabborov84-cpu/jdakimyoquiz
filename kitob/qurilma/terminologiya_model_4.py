#!/usr/bin/env python3
"""Terminologiya tozartuvi — 4-davr: qolgan «model» ko‘pliklari va noqulay
«taxminiy hisob» iboralari (asosan JSON matnlari va yon lavhalar)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = []
for pat in ['matn/*.md', 'matn/*.json', 'qurilma/*.py', 'dizayn.md', 'reja.md',
            'mundarija.md', 'boblar/*.md', 'README.md']:
    TARGETS += sorted(ROOT.glob(pat))

REPL = [
    # --- qolgan «model» ko‘pliklari (nazariy/tasvir konteksti) ---
    ('ion tasviri orqali tushuntiriladi', 'ion tasviri orqali tushuntiriladi'),
    ('yagona yondashuvda tushuntirishga', 'yagona yondashuvda tushuntirishga'),
    ('Chiziq Kₐ = 10⁻⁵ bo‘yicha shartli hisob', 'Chiziq Kₐ = 10⁻⁵ bo‘yicha shartli hisob'),
    ('Bu sharoitda suvning avtoionlanishi', 'Bu sharoitda suvning avtoionlanishi'),
    ('ionlangan kislota sharoitidagi pH qiymati', 'ionlangan kislota sharoitidagi pH qiymati'),
    ('ideal sharoitda HA va A⁻ ulushlari', 'ideal sharoitda HA va A⁻ ulushlari'),
    ('bog‘lanish tasviri va kislota–asos qarashi', 'bog‘lanish tasviri va kislota–asos qarashi'),
    ('Bu sharoitda a(O²⁻) = 0,01', 'Bu sharoitda a(O²⁻) = 0,01'),
    ('muvozanat yoki kinetik yondashuvni tanlang', 'muvozanat yoki kinetik yondashuvni tanlang'),
    ('Suvli ion tasviri', 'Suvli ion tasviri'),
    ('Proton tasviri', 'Proton tasviri'),
    ('Elektron tasviri', 'Elektron tasviri'),
    ('Proton va elektron tasvirlari bir-birini', 'Proton va elektron tasvirlari bir-birini'),
    ('Ideal ikki shaklli HA/A⁻ tizimi', 'Ideal ikki shaklli HA/A⁻ tizimi'),
    ('pH = pKₐ bo‘lganda ideal sharoitda ulushlar teng', 'pH = pKₐ bo‘lganda ideal sharoitda ulushlar teng'),
    ('Birinchi yondashuvda 90,91%', 'Birinchi yondashuvda 90,91%'),
    ('faraziy ideal tasvirlar', 'faraziy ideal tasvirlar'),
    ('asosiy yondashuvni boshqa darajadagi izoh bilan', 'asosiy yondashuvni boshqa darajadagi izoh bilan'),
    ('Morse funksiyasi', 'Morse funksiyasi'),
    ('Vektor yig‘indisi', 'Vektor yig‘indisi'),
    ('Karbonat tasvirida kulrang', 'Karbonat tasvirida kulrang'),
    ('Dimer tasviri', 'Dimer tasviri'),
    ('H₃O⁺ tasviri', 'H₃O⁺ tasviri'),
    ('proton holatlarining yagona tasviri emas', 'proton holatlarining yagona tasviri emas'),
    ('H₃PO₄ tasvirida P — bronza', 'H₃PO₄ tasvirida P — bronza'),
    ('Fosfit tasviridagi pastki oq H', 'Fosfit tasviridagi pastki oq H'),
    ('B(OH)₃ ning tekis tasvirida uch OH bor', 'B(OH)₃ ning tekis tasvirida uch OH bor'),
    ('HCl tasviri neytral molekulani ifodalaydi', 'HCl tasviri neytral molekulani ifodalaydi'),
    ('H₂SO₄ tasvirida ikki O atomiga H ulangan', 'H₂SO₄ tasvirida ikki O atomiga H ulangan'),
    ('HClO₄ tasvirida O atomlari', 'HClO₄ tasvirida O atomlari'),
    ('Suv tasvirida O qizil', 'Suv tasvirida O qizil'),
    ('HF tasviri monoprotik modda tuzilishini', 'HF tasviri monoprotik modda tuzilishini'),
    ('25 °C sharoitida K_w,c', '25 °C sharoitida K_w,c'),
    ('Born kontinuum grafigi', 'Born kontinuum grafigi'),
    ('HF tasvirini o‘qing', 'HF tasvirini o‘qing'),
    ('Nitrat tasviri', 'Nitrat tasviri'),
    ('Fosfat tasviri', 'Fosfat tasviri'),
    ('joyning ideal tasviri. Haqiqiy fosfatni', 'joyning ideal tasviri. Haqiqiy fosfatni'),
    ('Harorat hisobi', 'Harorat hisobi'),
    ('ikki tezlikli tizimda bir xil K', 'ikki tezlikli tizimda bir xil K'),
    ('Perokso tasvir', 'Perokso tasvir'),
    ('Hajmli tasvir', 'Hajmli tasvir'),
    ('Shartli hisob parametrlari', 'Shartli hisob parametrlari'),
    ('Shartli hisobning ma’nosi', 'Shartli hisobning ma’nosi'),
    ('Shartli hisobning ideal sharti bilan', 'Shartli hisobning ideal sharti bilan'),
    ('Uni yopadigan tenglamalar', 'Uni yopadigan tenglamalar'),
    ('Uni qayta tiklang', 'Uni qayta tiklang'),
    ('Shartli hisobning maqsadi', 'Shartli hisobning maqsadi'),
    ('Yondashuv tanlash', 'Yondashuv tanlash'),
    ('yondashuv tanlashni', 'yondashuv tanlashni'),
    ('Taxminiy hisobda bozor', 'Taxminiy hisobda bozor'),

    # --- noqulay «taxminiy hisob» iboralari (JSON matnlari) ---
    ('Bu shartli hisob emas', 'Bu shartli hisob emas'),
    ('Taxminiy hisob', 'Taxminiy hisob'),
    ('taxminiy hisob', 'taxminiy hisob'),
    ('Shartli hisob mantiqi', 'Shartli hisob mantiqi'),
    ('Shartli hisob sodda', 'Shartli hisob sodda'),
    ('Shartli hisob maqsadi', 'Shartli hisob maqsadi'),
    ('Shartli hisob nuqtasi', 'Shartli hisob nuqtasi'),
    ('Shartli hisob prefaktori A', 'Shartli hisob prefaktori A'),
    ('Shartli hisob faolik koeffitsiyent', 'Shartli hisob faolik koeffitsiyent'),
    ('Shartli hisob aktivatsiya energiyasi', 'Shartli hisob aktivatsiya energiyasi'),
    ('Shartli hisob asosida bashorat', 'Shartli hisob asosida bashorat'),
    ('Shartli hisob ildizining yozilishi', 'Shartli hisob ildizining yozilishi'),
    ('Shartli hisob misoli shu sinfda', 'Shartli hisob misoli shu sinfda'),
    ('Shartli hisob parametrlari', 'Shartli hisob parametrlari'),
    ('Taxminiy qiymatlar', 'Taxminiy qiymatlar'),
    ('Shartli hisob shartlarini tekshirish', 'Shartli hisob shartlarini tekshirish'),
    ('Shartli hisob sxemasi asosida', 'Shartli hisob sxemasi asosida'),
    ('Shartli hisob tavsifi', 'Shartli hisob tavsifi'),
    ('Shartli hisob ta’rifi', 'Shartli hisob ta’rifi'),
    ('Shartli hisob uchun berilgan dozalar', 'Shartli hisob uchun berilgan dozalar'),
    ('Shartli hisob uchun tanlangan', 'Shartli hisob uchun tanlangan'),
    ('Shartli hisob va jadval', 'Shartli hisob va jadval'),
    ('Bu shartli hisob emas, o‘quv tax', 'Bu shartli hisob emas, o‘quv tax'),
    ('Erta shartli hisob', 'Erta shartli hisob'),
    ('Empirik kinetik shartli hisob', 'Empirik kinetik shartli hisob'),
    ('Bir fazali shartli hisob shartsiz', 'Bir fazali shartli hisob shartsiz'),
    ('Har qanday yondashuv', 'Har qanday yondashuv'),
    ('Faqat shu ideal statistik tasvir', 'Faqat shu ideal statistik tasvir'),
    ('Ikki molekulali sodda shartli hisob', 'Ikki molekulali sodda shartli hisob'),
    ('Ideal konsentratsion hisob', 'Ideal konsentratsion hisob'),
    ('Ikkala shartli hisob pKₐ', 'Ikkala shartli hisob pKₐ'),
    ('1-bo‘limdagi shartli hisob', '1-bo‘limdagi shartli hisob'),
    ('Ayni shartli hisob minimumi', 'Ayni shartli hisob minimumi'),
    ('Birinchi tartibli shartli hisob', 'Birinchi tartibli shartli hisob'),
    ('Chiqindi omili bo‘yicha shartli hisob', 'Chiqindi omili bo‘yicha shartli hisob'),
    ('Mos shartli hisobda i_corr bahosi', 'Mos shartli hisobda i_corr bahosi'),
    ('Kinetik shartli hisob', 'Kinetik shartli hisob'),
    ('Standart holat shartli hisobi', 'Standart holat shartli hisobi'),
    ('Sun’iy ikki katod shartli hisobi', 'Sun’iy ikki katod shartli hisobi'),
    ('Mis bo‘yicha shartli hisob', 'Mis bo‘yicha shartli hisob'),
    ('Na⁺ bo‘yicha shartli hisob', 'Na⁺ bo‘yicha shartli hisob'),
    ('O‘quv tasviri', 'O‘quv tasviri'),
    ('Ideal erituvchi shartli hisobi', 'Ideal erituvchi shartli hisobi'),
    ('K_sp bo‘yicha shartli hisob', 'K_sp bo‘yicha shartli hisob'),
    ('Mos k_obs bilan ishchi shartli hisob', 'Mos k_obs bilan ishchi shartli hisob'),
    ('shartli hisob ildizining', 'shartli hisob ildizining'),
    ('taxminiy hisob nuqtasi', 'taxminiy hisob nuqtasi'),
    ('taxminiy hisob tuzilishi', 'taxminiy hisob tuzilishi'),
    ('taxminiy hisob shakli', 'taxminiy hisob shakli'),
    ('Taxminiy hisob tizimi', 'Taxminiy hisob tizimi'),
    ('Shartli hisob sxemasi', 'Shartli hisob sxemasi'),
    ('Shartli hisob kerak', 'Shartli hisob kerak'),
    ('shartli hisob kerak', 'shartli hisob kerak'),
    ('Shartli hisob mumkin', 'Shartli hisob mumkin'),
    ('shartli hisob mumkin', 'shartli hisob mumkin'),
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
