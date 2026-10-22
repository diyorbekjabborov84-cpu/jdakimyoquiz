# 4.1. Neytrallanish va tuz hosil bo‘lishi — manbalar va QA

## Ilmiy tayanchlar (2026-10-22)
1. OpenStax Chemistry 2e, 4.2 Classifying Chemical Reactions: https://openstax.org/books/chemistry-2e/pages/4-2-classifying-chemical-reactions . 2-chunk to‘liq o‘qildi: ionli tenglamalar, suvdagi HCl va proton ko‘chishi; neytrallanish haqidagi sahifa qidiruv parchasi ham tekshirildi. Matn, rasm yoki tayyor jadval ko‘chirilmagan.
2. OpenStax Chemistry 2e, 14.4 Hydrolysis of Salts: https://openstax.org/books/chemistry-2e/pages/14-4-hydrolysis-of-salts . NH₄⁺ Kₐ=5.6×10⁻¹⁰ va tuz ionlarining ta’siri avvalgi 3.5 bosqichida o‘qilgan to‘liq parcha bilan tekshirilgan; joriy qidiruvda ham gidroliz bo‘limi qayta ko‘rildi.
3. Atkins, de Paula, Keeler, Atkins’ Physical Chemistry, 11-nashr, OUP 2018 — proton almashinuvi termodinamikasi, Hess qonuni va kalorimetriyaga bibliografik tayanch; aniq sahifalar tekshirilmagan.
4. OpenStax Appendix H: https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . Fosfatning 25 °C qiymatlari 7.5×10⁻³, 6.2×10⁻⁸, 4.2×10⁻¹³ avvalgi 3.4 bosqichida 2-chunkdan to‘liq tekshirilgan. Faqat fakt konstantalar ishlatilgan.
5. IUPAC Gold Book, Salt, DOI 10.1351/goldbook.S05447: https://goldbook.iupac.org/terms/view/S05447/plain . Joriy to‘liq plain matn o‘qildi. Tuzning kation/anion yig‘indisi ekanligi mustaqil bayon qilindi; ta’rifdan ortiq ilmiy dalil IUPACga yuklanmagan.

## Hisoblar va chegaralar
`qurilma/neutral_04_01.py`, avvalgi `buffer_03_05.py` dagi log-pH ildiz va poliprotik taqsimot yordamchilaridan foydalanadi.
- pH hisoblari ideal konsentratsion 25 °C, γ≈1, Kw,c=10⁻¹⁴ (mol/L)² modelidir; aniq termodinamik pH ta’rifi molyar konsentratsiya bilan almashtirilmagan.
- Proton ko‘chishi: K=10^ΔpKa; teng boshlang‘ich HA/B, mahsulotlar yo‘q, suv/yon jarayonlar tashlangan modelda x/C=√K/(1+√K). Grafik tajribaviy titrlash yoki muayyan HA uchun o‘lchov emas. K o‘lchamsiz; ΔG°=−RT ln K.
- Fosfat: yakuniy C_P=0.0100 mol/L saqlanadi, [Na⁺]=rC_P. Turli yakuniy eritmalar qatori, bir idishga o‘zgarmas hajmda quyish tajribasi emas. Barcha to‘rt shakl va suv saqlangan. r=3 da PO₄³⁻ ulushi 0.2415826733, HPO₄²⁻ 0.7584011983; formal Na₃PO₄ tarkibi bitta tur 100% ekanini bildirmaydi.
- Tuz pH qiyosi: 0.0100 mol/L NaCl (kuzatuvchi ionlar), shartli NaA (HA Kc=10⁻⁵), NH₄Cl va shartli BH⁺A⁻ (HA Kc=10⁻⁵; BH⁺ Kc=10⁻⁹). Shartli HA HF emas. Oxirgi juftlik neytral pH bersa ham, har bir neytral shaklning ulushi 1/101.
- Kalorimetriya: −57.0 va −42.0 kJ/mol **berilgan shartli** doimiylar. Ular real tajriba natijasi, universal standart qiymat yoki HF ga oid ma’lumot sifatida berilmagan. Ikkinchisi −57+15 Hess yig‘indisi. Grafikda ajralgan issiqlik musbat; q_rxn manfiy. 0.0100 mol, 200 g, cp=4.18 J/g/K, Ccal=20 J/K bilan ΔT=0.6658878505 K.
- Ishlangan aralashma: 40.00 mL 0.1500 M HCl + 25.00 mL 0.2000 M NaOH; yakuniy hajm qo‘shiluvchan. NaCl formal 5.000 mmol, kislota ortig‘i 1.000 mmol, ideal pH=1.8129133566. M(NaCl)=58.44 g/mol bilan nazariy suvsiz massa 0.2922 g, amaliy ajratilgan kristall massasi emas.

## Original tasvirlar
`qurilma/draw_04_01.py` Pillow orqali chizadi. Tashqi kitob fotosi, rasmi yoki tayyor grafigi ishlatilmagan. Word matni Times New Roman; raster matn DejaVu Serif.

### 5 sxema
`ionli.png`: uch darajadagi tenglama; `ekvivalent.png`: nishon bosqichga bog‘liq sarf; `yollar.png`: gidroksid/ammiak/oksid/gidrokarbonat yo‘llari; `faza.png`: formula, kristall va erigan ionlar; `nazorat.png`: hisobni tekshirish.

### 4 grafik va CSV
- `yonalish.png` / `yonalish.csv`: 481 nuqta, ΔpKa=−6…+6; K, x/C va ΔG° ochiq saqlangan.
- `fosfat.png` / `fosfat.csv`: 301 nuqta, r=0…3; barcha ulushlar va pH saqlangan.
- `tuz_ph.png` / `tuz_ph.csv`: 4 modelning ustunli pH qiyosi, 25 °C ideal hisob.
- `issiqlik.png` / `issiqlik.csv`: 201 nuqta, ξ=0…10 mmol, ikki shartli entalpiya bilan issiqlik qiyosi.

### 4 qo‘shimcha tuzilish tasviri
- `gidroksoniy_model.png`: H₃O⁺ ulanish modeli.
- `fosfat_model.png`: HPO₄²⁻, bitta O–H ulanishi. Tayoqchalar to‘liq bog‘ tartibi yoki rezonans tasviri emas.
- `ammoniy_model.png`: NH₄⁺, to‘rtta N–H ulanishi.
- `panjara_model.png`: NaCl panjarasining 3×3×2 tugunli cheklangan bo‘lagi, 9 Na va 9 Cl ion tuguni. Ranglar shartli, chiziqlar qo‘shnichilikni ko‘rsatadi; alohida NaCl molekulalari, neytral atomlar aralashmasi yoki to‘liq elementar yacheyka deb olinmagan.

Molekulyar tasvirlar ulanishga yo‘naltirilgan sxemalar; optimallashtirilgan burchak/koordinata, elektron zichlik yoki tajribaviy tuzilish emas. Bob kirish konsept-arti bu mavzu DOCXiga kiritilmadi.

## Tekshiruv
`check_04_01.py`: 987 grafik qiymati, K va ΔG°, fosfat ulushlari/K/zaryad balansi, issiqlik va energiya saqlanishi, chegaralovchi reagent va ikki tomondagi barqaror suvli kvadrat yechim; 10 ta reaksiyaning atom va zaryad balanslari; neytral kuchsiz juftlikda qoldiq turlar; DOCX ZIP, 13 tasvir, 9 jadval, 8 tenglama, 18 yonlavha, TNR va indekslar PASS.

Yangi builderda asosiy ustun aniq 13.5 cm va yon ustun 4.5 cm ekani test qilindi; matndagi bob raqamlarini almashtirish kenglik sonlariga ta’sir qilmaydigan usulda bajarildi. Asosiy grafiklar va panjara rasmi ochib ko‘rildi.

9 mazmuniy bo‘lim — 9 bosma sahifa degani emas. Word/LibreOffice paginatsion renderer yo‘q; sahifa soni va barcha sahifalardagi joylashuv vizual renderer bilan tasdiqlanmagan. Native Google Docs matn eksporti alohida tekshiriladi.

Native Google Docs eksporti PASS: 25796 bayt; 9 jadval sarlavhasi, tayanch sonlar, tenglama raqamlari va adabiyotlar saqlangan.

2026-10-22: foydalanuvchi tekshiruvidan so‘ng matematik terim tuzatildi; asosiy tenglamalar OMML, strukturali kasr/indeks/darajalar bilan almashtirildi. Ilmiy qiymatlar va tasvirlar o‘zgarmagan. Google Docs→DOCX qayta eksportida matematik strukturalar saqlangan; Google PDF sahifalarida muhim formulalar vizual tekshirildi. Yangilangan havolalar va texnik tafsilotlar `dizayn.md` ning ta’mir yozuvida.
