# 3.5. Buferlar va gidroliz — manbalar, rasmlar va hisob qaydi

## Ilmiy manbalar
- OpenStax Chemistry 2e, 14.6 Buffers, 2-chunk o‘qildi: tutash juftlikning kuchli kislota/asosga javobi va cheklangan zaxira. Mustaqil o‘zbekcha bayon; manba misollari, matni yoki rasmlari ko‘chirilmagan. [1](https://openstax.org/books/chemistry-2e/pages/14-6-buffers).
- OpenStax Chemistry 2e, 14.4 Hydrolysis of Salts, 2-chunk o‘qildi: anion/kation gidrolizi, ikki faol ion, amfiprot shakllar, metall akvakomplekslari. NH₄⁺ uchun 25 °C Kₐ=5.6×10⁻¹⁰ fakt qiymati ham shu parchada tekshirildi. [2](https://openstax.org/books/chemistry-2e/pages/14-4-hydrolysis-of-salts).
- OpenStax Appendix H, 1-chunk: HF uchun 25 °C Kₐ=6.4×10⁻⁴ tekshirildi. 6.3×10⁻⁴ dastlabki taxmin sifatida ishlatilmaydi; modul, grafiklar va misollar tekshirilgan 6.4 qiymat bilan qayta hisoblangan. 2-chunkdagi fosfat 7.5×10⁻³, 6.2×10⁻⁸, 4.2×10⁻¹³ qiymatlari 3.4 bosqichida to‘liq tekshirilgan. https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . Faqat fakt konstantalar ishlatildi, jadval/raster rasm ko‘chirilmadi.
- Atkins, de Paula, Keeler, Atkins’ Physical Chemistry, 11-nashr, OUP 2018 — faollik va muvozanatga umumiy bibliografik tayanch; aniq sahifalar bu bosqichda tekshirilmagan.

Differensial β formulasi matndagi konsentratsion balansdan mustaqil chiqarilgan va sonli hosila bilan tekshirilgan. IUPACning alohida buffer-capacity ta’rifi topilgani yoki o‘qilgani da’vo qilinmaydi. Mavzu β ni aniq operatsion ta’riflaydi: doimiy C_T va yakuniy hajmda kuchli asos ekvivalentlari konsentratsiyasining pH bo‘yicha hosilasi. Bu katta ΔpH uchun o‘rtacha sig‘im bilan aynanlashtirilmagan.

## Hisob modeli
`qurilma/buffer_03_05.py`: monoprotik/poliprotik neytral ota-kislotaning oilalari, BH⁺/B oilalari, suv va kuzatuvchi ionlar farqi D=[Na⁺]−[Cl⁻]. Log pH oralig‘ida monoton zaryad tenglamasi yechiladi. Poliprotik ulushlar log-vaznlar bilan normallanadi. Musbat konsentratsiyalar, barcha moddiy balanslar va ion zaryadlari tekshiriladi.

25 °C ideal konsentratsion model: Kw,c=10⁻¹⁴ (mol/L)²; Kc lar mol/L. Termodinamik Kₐ larning ideal konsentratsion moslari qabul qilingan; noideal eritma pH i da’vo qilinmagan. Kc=10⁻⁵ shartli HA; bu HF emas. HF faqat NH₄F misolida o‘z qiymati bilan ishlatiladi. Molallikdagi IUPAC pH ta’rifi o‘rniga molyar konsentratsiya exact ta’rif sifatida berilmagan.

## Original rasmlar
Barcha PNGlar `qurilma/draw_03_05.py` orqali Pillow da original chizildi. Tashqi kitob rasmi, fotosurat yoki o‘lchangan koordinata ishlatilmadi. Word matni Times New Roman, raster belgilar DejaVu Serif.

### 4 sxema
- `mexanizm.png`: tutash shakllarning kislota/asosga javobi.
- `anion.png`: erish, anion proton almashinuvi va balanslarni ajratish.
- `kation.png`: NH₄⁺ va akvakompleksdagi proton donorning farqi.
- `nazorat.png`: birlashgan oilalar/balanslar algoritmi.

### 5 grafik va tekshiriladigan CSV
- `nisbat.png` / `nisbat.csv`: 321 nuqta; C_T=0.1000 mol/L, analitik n(NaA)/n(HA)=0.01…100. To‘liq suvli muvozanat va analitik nisbat taqribi.
- `qoshish.png` / `qoshish.csv`: 481 nuqta; C_T=0.1000 mol/L, q=−0.06…+0.06 mol/L. Yakuniy tarkiblari bo‘yicha taqqoslanadigan ideal eritmalar qatori; real bir idishga hajmsiz reagent qo‘shish tajribasi emas. Manfiy q: HCl ekvivalentlari, musbat q: NaOH ekvivalentlari. HH taqribi ikki stexiometrik miqdor musbat bo‘lgandagina berilgan.
- `sigim.png` / `sigim.csv`: 361 nuqta; pH 2…8; C_T=0.1 va 0.01 mol/L. Grafik faqat juftlik hissalarini ko‘rsatadi. CSV da suv va jami β ham ochiq saqlangan. Juftlik maksimumi global umumiy β maksimumi deb talqin qilinmagan.
- `suyultirish.png` / `suyultirish.csv`: 361 nuqta; C_T=10⁻¹⁰…10⁻¹ mol/L; teng analitik HA/NaA. Suv saqlangan va nisbatdan pH=5 taqribi qiyoslangan.
- `ikkala.png` / `ikkala.csv`: 321 nuqta; NH₄F C=10⁻⁹…10⁻¹ mol/L. HF Kc=6.4×10⁻⁴, NH₄⁺ Kc=5.6×10⁻¹⁰ mol/L. To‘liq ikki oilali balans va suvni tashlagan pH=6.2228159995 taqribi. γ≈1 sharti, yuqori C da haqiqiy faolliklar cheklovi saqlanadi.

### 4 tuzilish tasviri
- `h2po4_model.png`: H₂PO₄⁻, ikki OH ulanishi.
- `hpo4_model.png`: HPO₄²⁻, bitta OH ulanishi.
- `akva_model.png`: [Al(H₂O)₆]³⁺, olti O ligand va 12 H bilan sxematik proyeksiya.
- `nh4_model.png`: NH₄⁺, to‘rtta N–H ulanishining shar–tayoqcha tasviri.

Tasvirlar ulanishga yo‘naltirilgan, real fazoviy burchaklar yoki elektron zichlik emas; tayoqchalar to‘liq bog‘ tartibi talqini emas. Formal ion zaryadlari sarlavhalarda berilgan, fosfat rezonansining barcha yozuvlari chizilmagan.

## Tekshiruv
`check_03_05.py`: 1845 grafik nuqtasi; moddiy/zaryad balanslari, qayta tiklangan K, monotonlik; β ning mustaqil sonli hosilasi; haqiqiy yakuniy 110.0 mL bilan reagent qo‘shish misollari; NaA, NH₄Cl, fosfat tuzlari; DOCX ZIP, 13 rasm, 9 jadval, 9 tenglama, 18 yonlavha, shriftlar va indekslar PASS. Kichik qolgan HA ulushi ayirishdagi raqam yo‘qotilishisiz C_T h/(Kc+h) orqali tekshirildi. Grafiklar va akvakompleks rasmi ochib ko‘rildi.

9 mazmuniy bo‘lim — 9 bosma sahifa degani emas. Word/LibreOffice paginatsion renderer mavjud emas; sahifa soni va barcha sahifalardagi joylashuv vizual renderer bilan tasdiqlanmagan. Native Google Docs matn eksporti alohida tekshiriladi.
