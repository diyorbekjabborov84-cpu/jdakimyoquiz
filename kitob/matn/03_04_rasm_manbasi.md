# 3.4. Titrlash va indikatorlar — manbalar va tasvirlar

## Ilmiy manbalar va tekshirilgan faktlar
- OpenStax, Chemistry 2e, 14.7, Acid-Base Titrations: indikatorning HIn/In⁻ modeli, taxminiy pK±1 oralig‘i va kuchli/kuchsiz titrlash nazariyasi. 3-chunk to‘liq o‘qilgan; matn mustaqil o‘zbekcha yozildi, hech bir rasm yoki namuna jadvali ko‘chirilmadi. Manba: [1](https://openstax.org/books/chemistry-2e/pages/14-7-acid-base-titrations).
- David Harvey, Analytical Chemistry 2.1, 9-bob: qidiruvda PDF jadvalidagi odatiy intervallar tekshirildi: metiloranj 3.1–4.4, bromtimol ko‘ki 6.0–7.6, fenolftalein 8.3–10.0. Jadvaldagi faktlar va rang nomlari ishlatildi, jadval dizayni ko‘chirilmadi. Manba: [16](https://www.asdlib.org/onlineArticles/ecourseware/Text_Files_files/Chapter9.pdf). PDFning butun bobi bu bosqichda to‘liq o‘qilgani da’vo qilinmaydi.
- OpenStax Appendix H, 2-chunk: H₃PO₄ ning 25 °C konstantalari 7.5×10⁻³, 6.2×10⁻⁸, 4.2×10⁻¹³ to‘liq jadval parchasidan qayta tekshirildi. https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . Faqat fakt qiymatlar, tasvirlar emas, ishlatildi.
- OpenStax 14.7 alt-matnida metiloranjga 4.2–6.3 intervali xato moslangan; undan foydalanilmadi. Fenolftalein chegaralari manbalarda farqlanishi matnda ko‘rsatildi. Asosiy jadval Harvey tizimidagi 8.3–10.0 qiymatini izchil ishlatadi.

## Original tasvirlar
Barcha PNGlar `qurilma/draw_03_04.py` bilan Pillow da chizilgan. Tashqi fotosurat, tayyor kitob rasmi yoki kimyoviy tasvir ko‘chirilmagan. Word matni Times New Roman, raster tasvir belgilarida DejaVu Serif.

### 4 tushuntiruvchi sxema
`nuqtalar.png`: ekvivalentlik/oxirgi nuqta; `intervallar.png`: ma’lumotnoma intervallari pH shkalasida, rang intensivligi emas; `xato.png`: og‘ish ishorasi; `nazorat.png`: analitik sifat zanjiri.

### 5 hisobiy grafik va ochiq CSV
Barcha hajmlar hisob modulida L, chizmada mL. Boshlang‘ich namuna 25.00 mL 0.1000 mol/L, NaOH 0.1000 mol/L; 25 °C, Kw,c=10⁻¹⁴ (mol/L)², γ≈1, hajmlar qo‘shiluvchan.
- `kuchli.png` / `kuchli.csv`, 1001 nuqta: kuchli bir asosli kislota–NaOH, 0…50 mL.
- `kuchsiz.png` / `kuchsiz.csv`, 1001 nuqta: shartli HA, Kc=10⁻⁵ mol/L. Bu HF yoki aniq noorganik kislota tajribasi emas. To‘liq suvli moddiy/zaryad balansi.
- `fosfat.png` / `fosfat.csv`, 701 nuqta: 0…87.5 mL, uchta muvozanat bosqichi va suv. Bronza chiziqlar 25/50/75 mL stexiometrik hajmlar, uchta teng analitik sakrash degani emas.
- `indikator.png` / `indikator.csv`, 321 nuqta: shartli pK_In=7, HIn/In⁻ ulushlari. Grafik spektr, haqiqiy rang yoki yon tuzilishdagi para-nitrofenol konstantasi emas.
- `hosila.png` / `hosila.csv`, 401 nuqta: kuchli juftlikning 24.999…25.001 mL juda yaqin sohasida sonli birinchi hosila. Simmetrik differensiallash δV=10⁻⁷ mL. Asbob yozuvi yoki tajribaviy shovqin emas. Analitik hosila bilan mustaqil taqqoslandi.

### 4 qo‘shimcha rasm
- `qurilma.png`: byuretka/kolbaning original sxematik illyustratsiyasi; fotosurat, aniq asbob modeli yoki masshtabli texnik chizma emas.
- `fosfat_model.png`: H₃PO₄ ning ulanishga yo‘naltirilgan shar–tayoqcha modeli, uch OH. Optimallashtirilgan geometriya emas; tayoqchalar to‘liq bog‘ tartibi talqini emas.
- `hin_tuzilish.png`: para-nitrofenol ulanish modeli, nitro guruhida N⁺ va O⁻ formal zaryadlari aniq ko‘rsatilgan.
- `in_tuzilish.png`: para-nitrofenolyat ulanish modeli, fenolyat O⁻ va nitro formal zaryadlari bilan. Faqat bitta rezonans yozuvi; elektron zichlik yoki real spektr emas.

## Hisobiy mezonlar va natijalar
`qurilma/titration_03_04.py` log pH oralig‘ida musbat fizik ildizni topadi; poliprotik ulushlar log-vaznlar bilan normallanadi. Kc lar konsentratsion ideal moslar; muvozanatga keyinchalik bitta ion uchun yashirin noideal tuzatish kiritilmagan.

`check_03_04.py`: 3425 nuqtada balanslar, K nisbatlari, ulush yig‘indisi, monotonlik; sonli hosilaga qarshi analitik hosila; tanlangan pH dan hajmga 8 ta teskari hisob; analitik konsentratsiya va noaniqlik; DOCX ZIP, shriftlar, indekslar, 9 jadval, 8 tenglama, 13 tasvir va 18 yonlavha PASS. Asosiy egri chiziqlar, hosila va nitrofenol rasmi ko‘z bilan ham ko‘rildi.

Standart noaniqlik misolining aniq hisobiy qiymati u_r=0.1755649956%, matnda 0.1756%. Hajm va titrant noaniqliklari mustaqil; tuzatilmagan sistematik xato o‘z-o‘zidan yo‘qolmaydi.

9 mazmuniy bo‘lim 9 bosma sahifa degani emas. Word/LibreOffice paginatsion renderer yo‘q; sahifa soni va barcha sahifalardagi joylashuv vizual renderer bilan tasdiqlanmagan. Native Google Docs matn eksporti alohida tekshiriladi.
