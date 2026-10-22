# 3.6. Kinetika va kataliz — manbalar, tasvirlar va tekshiruv

## Ilmiy tayanchlar (2026-10-22)
1. IUPAC Gold Book, Catalyst, DOI 10.1351/goldbook.C00876: https://goldbook.iupac.org/terms/view/C00876/plain . To‘liq plain matn o‘qildi. Umumiy ΔG° o‘zgarmasligi, katalizatorning siklda reagent va mahsulot bo‘lishi, gomogen/geterogen farqi va stexiometrik sarflanadigan asosni katalizator bilan adashtirmaslik mustaqil o‘zbekcha bayon qilindi.
2. Specific acid–base catalysis, DOI 10.1351/goldbook.S05789: https://goldbook.iupac.org/terms/view/S05789/plain . To‘liq o‘qildi. Tasnif erituvchining o‘z ionlari katalitik hissasi bilan belgilanadi; kuchli kislota nomi yoki har doim H⁺ bo‘yicha birinchi tartib bilan aynanlashtirilmagan.
3. General acid catalysis, DOI 10.1351/goldbook.G02609: https://goldbook.iupac.org/terms/view/G02609/plain . To‘liq o‘qildi. Katalitik koeffitsiyentlar yig‘indisi va bufer konsentratsiyasi bilan farqlash mezoni. Ion kuchi/muhit nazorati, bir nisbatli chiziqdan k_HA va k_A ni alohida chiqara olmaslik mustaqil model tahlili bilan ochilgan.
4. Gibbs energy of activation, DOI 10.1351/goldbook.G02631: https://goldbook.iupac.org/terms/view/G02631/plain . To‘liq o‘qildi. Eyring talqinida tezlik konstantasining birliklari va standart holat muhim. Matnda birinchi tartibli ifoda bilan cheklangan.
5. Atkins, de Paula, Keeler, Atkins’ Physical Chemistry, 11-nashr, OUP 2018 — tezlik qonunlari, Arrhenius, o‘tish holati, Brønsted kinetik korrelyatsiyalariga bibliografik tayanch; aniq sahifalar tekshirilmagan.
6. Housecroft, Sharpe, Inorganic Chemistry, 5-nashr, Pearson 2018 — koordinatsiya, noorganik kataliz va sanoat kontekstiga umumiy bibliografik tayanch; aniq sahifalar tekshirilmagan.

IUPAC atamalari hozirgi Gold Book 5-nashr/5.0.0 (2025) sahifalaridan tekshirildi. Ta’riflar uzun iqtibos sifatida ko‘chirilmagan; rasm, jadval yoki tayyor grafik olinmagan. Formal NO/NO₂ sikli to‘liq sanoat mexanizmi yoki elementar tezlik bosqichlari deb taqdim etilmagan.

## Hisob moduli
`qurilma/kinetics_03_06.py`: vaqt s, T K, energiya J/mol (grafikda kJ/mol), konsentratsiya mol/L.
- Yopiq S⇌P: kf=0.0200 s⁻¹, kr=0.00500 s⁻¹, K=4, P_eq=0.8. Taqqoslashda ikkala k 10×, nisbat saqlanadi. Yarim vaqtlar muvozanatdan og‘ish uchun, qaytmas substratning yarmi sarflanishi uchun emas.
- Energiya profili — boshqa mustaqil o‘quv model: boshlanish 0, oxir −20 kJ/mol; katalizsiz maksimum 80; katalitik yo‘l maksimumlari 55/45, oraliq minimum 10. Kosinusli segmentlar bilan tushuntiruvchi shakl chizilgan; bu energiyalar S⇌P ning K=4 parametrlariga moslashtirilmagan. 10 kJ to‘siq pasayishi uchun 56.4838 tezlashish misoli ham shu chizmadagi 25 kJ farqidan alohida.
- Arrhenius: Ea=50000 J/mol, kref=0.001 s⁻¹, Tref=298.15 K. Doimiy Ea modeli, real kislota ma’lumoti emas.
- pH: k0=10⁻⁵ s⁻¹, kH=10 va kOH=100 L mol⁻¹ s⁻¹, Kw,c=10⁻¹⁴ (mol/L)²; h/c°≈10⁻pH, γ≈1, 25 °C. kobs=k0+kHh+kOHKw/h. Minimum pH=6.5. U shakli yagona mexanizm isboti emas.
- Bufer: aynan muvozanatdagi HA/A⁻=1, ideal pH=pKa=5, kHA=0.0200 L mol⁻¹ s⁻¹, kA=0. Bu kA qiymati tajribadan topilgan xulosa emas, berilgan parametr. Har xil C_T da pH va ion muhiti tajribada qanday saqlanishi chizmada idealizatsiya qilingan. C_T=0 nuqtada pH tashqi shart sifatida berilgan, eritma sof suv deb olinmagan.
- Eyring bo‘yicha qiyos faqat birinchi tartib va bir xil prefaktor/κ bilan. Standart holatsiz ikkinchi tartibli k bevosita formulaga qo‘yilmagan. κ=1 yordamchi sonli tekshiruv uchun qabul qilingan.

## Original tasvirlar
`qurilma/draw_03_06.py` Pillow orqali barcha PNGlarni original chizadi. Tashqi surat yoki optimallashtirilgan molekulyar koordinata ishlatilmagan. Word matni Times New Roman; raster belgilar DejaVu Serif.

### 5 grafik va CSV
- `muvozanat.png` / `muvozanat.csv`: 481 nuqta, 0…240 s, 0.5 s qadam; ikki tezlik modelida bir xil K.
- `energiya.png` / `energiya.csv`: 1001 nuqta, shartli koordinata 0…1; ikki erkin energiya yo‘li.
- `harorat.png` / `harorat.csv`: 241 nuqta, 278.15…338.15 K, 0.25 K qadam; ln[k(T)/kref] va 1000 K/T o‘lchamsiz o‘qlar.
- `ph_tezlik.png` / `ph_tezlik.csv`: 401 nuqta, pH 2…12. lg(kobs/k°), k°=1 s⁻¹; CSV da barcha kanallar alohida.
- `bufer.png` / `bufer.csv`: 301 nuqta, C_T=0…0.1000 mol/L; maxsus kanallar va qo‘shimcha umumiy HA katalizi. Grafik tezlik birligi 10⁻³ s⁻¹.

### 4 sxema
`tezlik.png`: signal va tartiblar; `sikl.png`: formal proton tashish; `noorganik.png`: NO/NO₂ balans sikli; `nazorat.png`: mexanistik dalillarni tekshirish.

### 4 molekulyar tasvir
- `gidroksoniy_model.png`: H₃O⁺ — suvli proton tashuvchisi.
- `fosfat_model.png`: H₂PO₄⁻ — proton donor misoli. Yon grafikdagi shartli pKa=5 shu ionga tegishli emasligi captionda aniq aytilgan.
- `ammiak_model.png`: NH₃ — proton akseptor misoli, formal sikldagi S yoki P ning aniq moddasi emas.
- `no2_model.png`: neytral NO₂ radikali; to‘liq Lewis modeli, spin/elektron zichlik yoki bog‘ tartibi chizmasi emas.

Barcha molekulalar ulanishga yo‘naltirilgan sxematik proyeksiyalar; aniq burchaklar, energiya minimumlari va tajribaviy tuzilishlar deb da’vo qilinmagan. NOₓ sikli zaharli gazlar bilan amaliy tajriba bajarish yo‘riqnomasi emas.

## QA
`check_03_06.py`: 2425 grafik nuqtasi; S+P=1, muvozanat va vaqt masshtabi; Arrhenius qiyaligidan Ea ni mustaqil qayta chiqarish; Eyring nisbatidan to‘siq pasayishi; pH minimumi va kanal yig‘indilari; bufer qiyaligi; NO/NO₂ bosqichlari va yig‘indining atom balansi; ishlangan yarim vaqtlar; DOCX ZIP, 13 rasm, 9 jadval, 8 tenglama, 18 yonlavha, TNR va yuqori/pastki indekslar PASS.

Asosiy grafiklar ochib ko‘rildi; raster va Word indekslar tuzatildi. 9 mazmuniy bo‘lim 9 bosma sahifa degani emas. Word/LibreOffice paginatsion renderer yo‘q; barcha sahifalardagi joylashuv va sahifa soni vizual renderer bilan tasdiqlanmagan. Native Google Docs matn eksporti alohida tekshiriladi.

2026-10-22: foydalanuvchi tekshiruvidan so‘ng matematik terim tuzatildi; asosiy tenglamalar OMML, strukturali kasr/indeks/darajalar bilan almashtirildi. Ilmiy qiymatlar va tasvirlar o‘zgarmagan. Google Docs→DOCX qayta eksportida matematik strukturalar saqlangan; Google PDF sahifalarida muhim formulalar vizual tekshirildi. Yangilangan havolalar va texnik tafsilotlar `dizayn.md` ning ta’mir yozuvida.
