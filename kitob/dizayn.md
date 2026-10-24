# NOORGANIK KISLOTALAR — Kitob dizayni konsepsiyasi (taklif)

> Tasdiqlangandan keyin `qurilma/build_docx.py` ga kod sifatida o'tkaziladi.

## 1. Umumiy g'oya
**Ilmiy, toza, ishonchli.** Oq fonda chuqur ko'k + bronza aksentlari. Har bir sahifa — darslik emas, laboratoriya jurnali va ilmiy atlas aralashmasi.

### Rang palitrasi
| Rol | Rang | Kod | Qaerda ishlatiladi |
|---|---|---|---|
| Asosiy ko'k | Chuqur dengiz ko'ki | `#0B2C4A` | Muqova, bob sarlavhalari, jadvallar sarlavhasi |
| Aksent | Bronza / oltin | `#C28E3B` | Raqamlar, chiziqlar, muhim bloklar |
| Yordamchi | Och ko'k-kulrang | `#E8F0F6` | Jadval fonlari, eslatma bloklari |
| Ogohlantirish | To'q qizil | `#8B1A1A` | Diqqat, xavfsizlik bloklari |
| Matn | Grafit | `#1A1A1A` | Asosiy matn |
| Izoh | Kulrang | `#5A5A5A` | Rasm osti, manba izohlari |

### Shriftlar (Word da mavjud, o'rnatish shart emas)
- **Sarlavhalar:** Cambria / Times New Roman, qalin (Bold), ko'k rang
- **Asosiy matn:** Times New Roman 11 pt, qator oralig'i 1.15
- **Formulalar:** Cambria Math, markazda, raqami o'ngda `(1.3)`
- **Jadvallar:** Calibri 9.5 pt, ixcham
- **Kod / misol:** Consolas 9 pt

### Sahifa
- O'lcham: A4, hoshiyalar 2 sm (ichki 2.5 sm tikish uchun)
- Kolontitul: yuqorida — bob nomi (kulrang, 8 pt), pastda — sahifa raqami (o'rtada, bronza chiziq ustida)
- Har bob yangi sahifadan boshlanadi, bob raqami katta (48 pt, och kulrang watermark uslubida)

## 2. Muqova (3 ta variant — tanlang)

**Variant A — «Laboratoriya» (tavsiya):**
Oq fonda markazda H₂SO₄ tetraedr modeli (3D, yarim shaffof), orqada xira davriy jadval fragmenti. Yuqorida seriya chizig'i (bronza), pastda muallif. Orqa muqovada anotatsiya + 3 ta ikonka (nazariya / tajriba / sanoat).

**Variant B — «Sanoat»:**
To'q ko'k fonda oq chiziqli zavod blok-sxemasi (kontakt apparati kesimi). Sarlavha oq, aksent bronza.

**Variant C — «Minimal ilmiy»:**
Toza oq, faqat tipografika: katta sarlavha, ingichka bronza chiziqlar, kichik molekula piktogrammalari burchaklarda.

> Siz bittasini tanlaysiz, qolganini moslashtiraman. Hozir A ni asos qilib olaman.

## 3. Ichki elementlar dizayni

### Bob kirishi
Har bob boshida:
- Katta bob raqami (masalan `01` — 48 pt, #E8F0F6 rangda)
- Sarlavha (18 pt, #0B2C4A, Bold)
- Taglavha / epigraf (italic, kulrang, chap chiziq bilan)
- «Ushbu bobda o'rganasiz» — 4–6 punktli ko'k ramkali blok (och ko'k fon #E8F0F6, chapda qalin ko'k chiziq)

### Formulalar
- Blokli: markazda, raqami o'ngda `(bob.formula)` — masalan `(4.2)`
- Inline: matn ichida, subscript/superscript Word formatida (H₂SO₄, SO₄²⁻, Eₐ)

### Jadvallar
- Sarlavha yuqorida: **1.2-jadval. Nomi** (10 pt, Bold, ko'k, markazda)
- Bosh qator: to'q ko'k fon (#0B2C4A), oq matn, Bold
- Qolgan qatorlar: juft qatorlar och ko'k fon (#E8F0F6) — zebra
- Chegaralar: faqat gorizontal, ingichka (0.5 pt, #0B2C4A)

### Rasmlar / chizmalar / grafiklar
- Markazda, 85% eni
- Ostida: **1.3-rasm. Nomi** (10 pt, kulrang, markazda, italic)
- Har rasmda manba izohi (agar kerak bo'lsa): 7 pt kulrang
- Turlari:
  - **Tuzilish sxemalari:** oq fonda, ko'k bog'lar, qizil kislorod, sariq oltingugurt
  - **Grafiklar:** toza chiziqli, ko'k/bronza ranglarda, panjara och kulrang
  - **Blok-sxemalar:** yumaloq burchakli to'rtburchaklar, strelkalar bronza
  - **3D modellar:** oq fon, yumshoq soya

### Maxsus bloklar
```
> [!NOTE]      → Eslatma (ko'k, ℹ️, och ko'k fon)
> [!IMPORTANT] → Muhim (bronza, ⭐, och sariq fon)
> [!TIP]       → Maslahat (yashil, 💡)
> [!WARNING]  → Diqqat (qizil, ⚠️, och qizil fon)
> [!EXAMPLE]  → Misol (kulrang, och kulrang fon, chap chiziq)
```

### Mashqlar
- Har bir topshiriq: **1.1-masala.** qalin, keyin matn
- Test variantlari: A) B) C) D) — osilgan indent, Variant uslubida
- Javoblar ilovada — bobda faqat savol

### Xulosa
- Ko'k ramkali blok, ichida 6–8 punkt (har punkt boshida bronza nuqta •)
- Pastda ingichka bronza chiziq

## 4. Chizma uslubi (barcha rasmlar uchun yagona)

- **Chiziq qalinligi:** 1.5 pt (asosiy), 1 pt (yordamchi)
- **Strelkalar:** uchburchak, 8 pt
- **Ranglar:** ko'k (#0B2C4A) — bog'lar/ramkalar, bronza (#C28E3B) — aksent, qizil (#D32F2F) — O atomi, sariq (#FBC02D) — S atomi, yashil (#388E3C) — N, h.k.
- **Fon:** har doim oq, soyasiz (chop etishga qulay)
- **Izohlar:** rasm ichida o'zbekcha, 8 pt Calibri, qisqa

## 5. Mundarija (TOC) dizayni
- Qism nomi: 14 pt, ko'k, Bold, ustidan bronza chiziq
- Bob qatori: 11 pt, chapda bob raqami (bronza), o'ngda sahifa raqami (nuqtalar bilan)
- Ilovalar: italic, kulrang

## 6. Texnik amalga oshirish
`build_docx.py` da quyidagilar sozlanadi:
- Sahifa o'lchami va hoshiyalar (A4)
- Barcha uslublar (Heading 1/2/3, Normal, Caption, Variant, Admonition)
- Ranglar RGBColor orqali
- Kolontitul va sahifa raqami (footer, bronza chiziq)
- Jadval uslubi (zebra, ko'k sarlavha)
- Muqova sahifasi (jadval yoki rasm bilan)

> Tasdiqlasangiz, 1-bob yozilishi bilan birga dizayn ham kodga o'tadi — birinchi namuna DOCX da jonli ko'rasiz.

## 7. Sizdan kerak
1. Muqova varianti: **A / B / C** (yoki aralash)
2. Rang bo'yicha izoh: shu palitra ma'qulmi yoki boshqa rang xohlaysizmi (masalan, yashil kimyo, qora-oltin premium)
3. Mundarijada bob qo'shish/olib tashlash istagi bormi

Keyin darhol 1-bobga o'tamiz.

## 2026-10-20 — yangi yo‘nalish: 3+1 maket

- Eski davrga xos haddan tashqari klassik maketdan voz kechiladi.
- Sahifaning yozuv maydoni eni bo‘yicha to‘rt ulush: 75% asosiy matn, o‘ngdagi 25% mavzuga oid chizma, rasm va grafiklar.
- Bob va mavzu sarlavhalari alohida ramkali/rangli tasmali bloklarda.
- Times New Roman; formulalar Word quyi/yuqori indekslari bilan, matn sifatida.
- Ilmiy grafiklarga haqiqiy hisob yoki ma’lumot zarur; tarixiy mavzuda sxema va struktur formulalar ishlatiladi.
- Har bir mavzu alohida tayyorlanadi; yakunda umumiy kitobga birlashtiriladi.
- Birinchi namuna: `qurilma/build_01_01_sidebar.py`; matn manbasi `matn/01_01.md`.
- Drive namuna: https://drive.google.com/file/d/1jrr95xAb2yxh1PyYPEROrnU2WzEfZSeh/view

### Tasdiqlangan ish tartibi (1.2-mavzudan boshlab)

- Foydalanuvchi boyitilgan 3+1 maketni tasdiqladi; uslub qayta o‘zgartirilmaydi.
- Yon ustunlar bo‘sh qoldirilmaydi: mavzuga bevosita tegishli tarixiy lavhalar, tushuntirishlar, misollar, savol-javoblar qo‘shiladi.
- Mavzuga mos ilmiy grafiklar, struktur rasmlar va olimlarning haqiqiy portretlari qo‘llanadi; tarixiy shaxsning uydirma portreti ishlatilmaydi.
- Har bir mavzu alohida DOCX; keyin umumiy kitobga birlashtiriladi.
- 1.2-mavzu: `matn/01_02.md`, `matn/01_02_yonlavhalar.json`, `qurilma/build_01_02_sidebar.py`.
- Grafiklarning farazlari, hisobiy ma’lumotlari va portret manbalari `matn/01_02_rasm_manbasi.md` da.

### 1.3-mavzu tayyor
- Mavzu: Brønsted–Lowry nazariyasi. 3+1 maket o‘zgartirilmadi.
- Alohida Word: `chiqish/Noorganik-kislotalar-1.3-Bronsted-Lowry.docx`.
- Ikki haqiqiy olim fotografiyasi, 2 hisobiy grafik, 3 tushuntiruvchi sxema, 21 yonlavha.
- Manbalar va litsenziya izohlari `matn/01_03_rasm_manbasi.md` da.
- Word Drive: https://drive.google.com/file/d/16zLDd3ds5tD4Bb-okztwKZtKmUsdHocm/view
- Onlayn Google Docs: https://docs.google.com/document/d/1W9bGrzb3vwS5OQ18I3AYAl5dkLK6ApePTXd4fh_v4Rk/edit
- Keyingi mavzu: 1.4. Lewis nazariyasi.

### 1.4-mavzu tayyor — Lewis nazariyasi
- Asosiy manba: `matn/01_04.md`; yonlavhalar `matn/01_04_yonlavhalar.json`.
- Qurilchi: `qurilma/build_01_04_sidebar.py`; grafika: `qurilma/draw_01_04.py`.
- Alohida Word: `chiqish/Noorganik-kislotalar-1.4-Lewis.docx`.
- 3+1 maket, Times New Roman, 7 vizual: tarixiy portret, 2 donor–akseptor chizmasi, 2 hisobiy grafik, 2 sxema; 21 yonlavha.
- DOCX yaxlitligi, indeksli formulalar, shriftlar va hisoblar tekshirildi; sahifalar Word/PDF rendererida ko‘rib chiqilgani da’vo qilinmaydi.
- Portret va grafik manbalari `matn/01_04_rasm_manbasi.md` da. Portretning ommaviy/tijoriy nashr huquqi alohida aniqlashtirilishi kerak.
- Word hamda Google Docs nusxalarini Drive’ga yuklash urinishlari `rate_limited` bilan rad etildi. Ular uchun yangi Drive ID yoki havola yaratilgani tasdiqlanmagan. Shu turn davomida takroriy yuklash amalga oshirilmadi.
- Fayl foydalanuvchiga present_file orqali ochildi.
- Keyingi mavzu: 1.5. Usanovich va Lyuks–Flud nazariyalari.

### 1.5-mavzu — Usanovich va Lyuks–Flud
- Alohida Word: `chiqish/Noorganik-kislotalar-1.5-Usanovich-Lyuks-Flud.docx`.
- Manba: `matn/01_05.md`, yonlavhalar `matn/01_05_yonlavhalar.json`.
- Qurilchi: `qurilma/build_01_05_sidebar.py`; chizma va grafiklar: `qurilma/draw_01_05.py`.
- 3+1 maket, Times New Roman, 7 vizual, 21 yonlavha; tasdiqlanmagan portretlar ishlatilmadi.
- Manbalar va model farazlari: `matn/01_05_rasm_manbasi.md`.
- Word Drive: https://drive.google.com/file/d/1blYMdIGjaq9YIDR-bbmUFm1SmLHJ1xyv/view
- Onlayn nusxa: https://docs.google.com/document/d/1z3PdmEamX_3nbSzMxzBq9OtyRRUFsGmuISmN9NOijQk/edit
- Keyingi mavzu: 1.6. Pearson HSAB nazariyasi.

### 1.6-mavzu — Pearson HSAB nazariyasi
- Alohida Word: `chiqish/Noorganik-kislotalar-1.6-Pearson-HSAB.docx`.
- Manba: `matn/01_06.md`; yonlavhalar: `matn/01_06_yonlavhalar.json`.
- Qurilchi: `qurilma/build_01_06_sidebar.py`; vizual qurilchi: `qurilma/draw_01_06.py`.
- Tasdiqlangan 3+1 maket va Times New Roman saqlandi; 7 vizual, 21 yonlavha, 6 raqamlangan ifoda.
- HSAB qattiqligi kislota kuchi emasligi, muhit/miqdor/redoks/cho‘kma ta’siri alohida tushuntirildi.
- Pearsonning UCSB profilidagi haqiqiy portreti ishlatildi; nashr huquqini ommaviy/tijoriy nashrdan oldin aniqlashtirish zarur. Manba `matn/01_06_rasm_manbasi.md` da.
- Ikki grafik faraziy hisobiy model; CSV va model shartlari saqlangan.
- Word shrift/indeks/ZIP yaxlitligi tekshirildi; sahifalar Word rendererida ko‘rilgani da’vo qilinmaydi.
- Drive Word: https://drive.google.com/file/d/17YLKFNhlENGV9jlDuNI_y2Azbb7-rbIE/view
- Google Docs: https://docs.google.com/document/d/1ohefBtyiYufFTf83Xx94ksHLlKWKoLygacRizYzobd8/edit
- Ikkala nusxaga link orqali reader ruxsati berildi; onlayn nusxadan matn eksporti muvaffaqiyatli.
- Keyingi mavzu: 1.7. Superkislotalar.

### 1.7-mavzu — Superkislotalar
- Alohida Word: `chiqish/Noorganik-kislotalar-1.7-Superkislotalar.docx`.
- Manba: `matn/01_07.md`; yonlavhalar: `matn/01_07_yonlavhalar.json`.
- Qurilchi: `qurilma/build_01_07_sidebar.py`; vizuallar: `qurilma/draw_01_07.py`.
- 3+1 maket, Times New Roman, 7 vizual, 21 yonlavha va 8 raqamlangan tenglama/ifoda.
- H0 va pH aynan bir kattalik emasligi, indikatorlar oilasi va muhitga bog‘liqlik alohida tushuntirildi.
- 11.2 bilan takrorlanmaslik uchun bu mavzu nazariy ta’rif va o‘lchash mantig‘iga qaratildi; amaliy tayyorlash ko‘rsatmalari yo‘q.
- Olahning tasdiqlangan biografik ma’lumoti bor; noto‘g‘ri shaxs portretlari ishlatilmadi. Vizual manbalar va farazlar `matn/01_07_rasm_manbasi.md` da.
- Word ZIP/shrift/indeks tekshiruvlari va model sonlari tekshirildi. Word rendererida sahifalar tekshirilgani da’vo qilinmaydi.
- Drive Word: https://drive.google.com/file/d/1ZzJ6NlcLv-n6sjYBOa8icPPuy0_LQk_U/view
- Onlayn Google Docs: https://docs.google.com/document/d/1vVJ-KY7VpWEsyaxWss3i41yFKTjj1B-ZgugRSMrVIRE/edit
- Ikkala nusxa link bilan o‘qishga ochiq; onlayn matn eksporti muvaffaqiyatli.
- Keyingi mavzu: 1.8. Nazariyalarni qiyoslash.

### 1.8-mavzu — Nazariyalarni qiyoslash
- Birinchi bobning yakuniy mavzusi alohida hujjatda tayyorlandi.
- Word: `chiqish/Noorganik-kislotalar-1.8-Nazariyalarni-qiyoslash.docx`.
- Manba `matn/01_08.md`; 7 tahrirlanadigan jadval manbasi `matn/01_08_jadvallar.json`; yonlavhalar `matn/01_08_yonlavhalar.json`.
- Qurilchi `qurilma/build_01_08_sidebar.py`; vizuallar `qurilma/draw_01_08.py`.
- 3+1 maket, Times New Roman; 7 qiyosiy jadval, 5 sxema, 2 hisobiy grafik va 21 yonlavha.
- HSAB va superkislotalilik umumiy reaksiya ta’riflari bilan bir xil maqomda emasligi ochiq ajratildi.
- Grafiklar ideal modellar; matematik o‘xshashlik kimyoviy shartlar tengligini anglatmasligi ta’kidlandi. Manbalar va farazlar `matn/01_08_rasm_manbasi.md` da.
- Rekursiv jadval/shrift/indeks va DOCX yaxlitlik tekshiruvlari muvaffaqiyatli; rasm fayllari ko‘rib chiqildi. Word rendererida sahifalar tekshirilgani da’vo qilinmaydi.
- Drive Word: https://drive.google.com/file/d/1lw7XnGWe1a3wYSM5NFgV0Wf98-WtygtF/view
- Google Docs: https://docs.google.com/document/d/1oV3k_vFUe-w5JIVKLw__fiXo7utcsCNt5HnsFpoO7Eg/edit
- Ikkala fayl havola orqali o‘qishga ochildi; onlayn matn eksporti muvaffaqiyatli.
- 1.1–1.8 mavzular tayyor. Keyingi mavzu: 2.1. Kimyoviy bog‘lanish va fazoviy tuzilish.

### 2.1 — Kimyoviy bog‘lanish va fazoviy tuzilish
- Alohida modul tayyor: `chiqish/Noorganik-kislotalar-2.1-Boglanish-va-fazoviy-tuzilish.docx`.
- 7 bo‘lim, 7 tahrirlanadigan jadval, 5 sxema, 2 faraziy hisobiy grafik, 6 raqamlangan tenglama va 21 yonlavha; rekursiv hisobda 2544 so‘z.
- 3+1 ramkali maket; TNR asosiy matn/formula/jadvallar; indekslar Word xususiyatlari bilan. Grafik rastrlarida DejaVu Serif.
- Asosiy mazmun: ulanish, qutblilik va uzilish yo‘llari, Lewis/formal zaryad, VSEPR, dipol vektorlari, kislotalik termodinamikasi va tekshirish algoritmi. Rezonans hamda vodorod bog‘i 2.2 uchun qoldirildi.
- `matn/02_01*`, `qurilma/build_02_01_sidebar.py`, `qurilma/draw_02_01.py`, `rasmlar/boglanish/` — qayta ishlab chiqarish manbalari.
- ZIP, 7 rasm/7 jadval, TNR, indekslar va eski yorliqlar yo‘qligi tekshirildi. Word sahifa renderi qilinmagan.
- Word: https://drive.google.com/file/d/1JSeLvvj5x18lCx6lJWwoCiZ6EiugNG1Y/view
- Docs: https://docs.google.com/document/d/1xlbkt07deVAsmOlIPM6OTlYX4Awmy57xZqZUpBig3Ek/edit
- Ikkala nusxa havola orqali reader; Docs text eksporti muvaffaqiyatli.

### 2.2 — Rezonans va vodorod bog‘i
- User chetki ajratilgan joyga ko‘proq rasmlar so‘radi. Doimiy uslubga qo‘shimcha: mavzuga mos hajmli molekulyar modellarni ham 25% yon ustunda berish; ular fotosurat yoki hisoblangan elektron zichlik deb ko‘rsatilmasin.
- Alohida hujjat: `chiqish/Noorganik-kislotalar-2.2-Rezonans-va-vodorod-bogi.docx` (340840 bayt; rekursiv hisob 2454 so‘z).
- 7 bo‘lim, 7 tahrirlanadigan jadval, 6 sxema, 1 faraziy IR grafik va 4 qo‘shimcha hajmli shar–tayoqcha rasm (jami 11 vizual), 14 yonlavha va 2 raqamlangan yozuv.
- Qo‘shimcha molekulyar rasmlar: nitrat, karbonat, suv dimeri, gidroksoniy. Barchasi 25% chetki ustunda. Yonlavhalar kamaytirilib, rasmlar uchun joy ajratildi.
- `matn/02_02*`, `qurilma/build_02_02_sidebar.py`, `qurilma/draw_02_02.py`, `rasmlar/rezonans/` qayta qurish manbalari.
- IUPAC 2011 vodorod bog‘i ta’rifi manbasi qo‘shildi. Rezonans muvozanat emasligi, to‘liq proton almashinuvi bilan vodorod bog‘i bir xil emasligi ajratildi.
- ZIP/shrift/indeks/11 rasm/7 jadval va eski markerlar tekshirildi; alohida rasmlar ko‘rildi. Word sahifa renderi qilinmagan.
- Word: https://drive.google.com/file/d/1e4icsnJU0COAjQYxYpCaNALP7LerM6rC/view
- Docs: https://docs.google.com/document/d/1vONKhYpoSiE1lD-GBNLUpbGQEcUoe6ZtYX50jAq0nGs/edit
- Ikkala nusxa reader havola bilan ochildi; native Docs text eksporti muvaffaqiyatli. Keyingi mavzu 2.3. Tasnif.

### 2.3 — Tasnif
- Alohida modul tayyor: `chiqish/Noorganik-kislotalar-2.3-Tasnif.docx` (375032 bayt; rekursiv hisobda 2438 so‘z).
- 7 bo‘lim, 7 tahrirlanadigan jadval, 6 sxema, 1 ideal hisobiy grafik, 4 hajmli molekulyar rasm (jami 11 vizual), 14 yonlavha, 6 raqamlangan ifoda.
- Tarkib/asoslilik/kuch/konsentratsiya/tuzilish/redoks/fizik xossa/xavflilik alohida mezonlarda berildi. Borat kislota va P–H/O–H farqi ochiq izohlandi.
- 3+1 maket; HF, fosfat, fosfit va borat modellari aynan 25% chetki ustunda. TNR matn/formulalar/jadvallar; rastrlarda DejaVu Serif.
- Grafikda c=C/c° o‘lchamsiz konsentratsiya; Q=Kₐ/c=α²/(1−α) sonli tekshirildi. Tajribaviy natija emas.
- Manbalar: `matn/02_03*`, `qurilma/build_02_03_sidebar.py`, `qurilma/draw_02_03.py`, `rasmlar/tasnif/`.
- ZIP, rasm/jadval sonlari, TNR, indekslar, eski markerlar yo‘qligi tekshirildi. Word sahifa rendererida tekshirilmagan.
- Word: https://drive.google.com/file/d/1QcqID9tmRcCdjjHFohzy4RwSG1ofrNd9/view
- Docs: https://docs.google.com/document/d/1kzZPrevNyGjCCVI_PBK5l06Nng-A4EHx4jxRCFMF-nE/edit
- Ikkala fayl havola orqali reader; Docs matn eksporti muvaffaqiyatli. Keyingi mavzu — 2.4. Nomenklatura (IUPAC).

### 2.4 — Nomenklatura (IUPAC)
- Alohida modul: `chiqish/Noorganik-kislotalar-2.4-Nomenklatura-IUPAC.docx`, 381141 bayt, rekursiv hisob 2424 so‘z.
- 7 bo‘lim, 7 tahrirlanadigan jadval, 7 nomlash sxemasi, 4 hajmli molekulyar rasm (jami 11 yon vizual), 3 raqamlangan muvozanat va 14 yonlavha. Mazmunga zarur bo‘lmagan grafik qo‘shilmadi.
- Saqlangan/tarkibiy/additiv nomlar; faza belgisi; kislota–anion qatori; hydrogen nomlari; per-/perokso-/tio-; kompleks qavs/zaryad va nomdan formulaga o‘tish.
- IUPAC qisqa qo‘llanmasining veb matni tekshirildi; fosfit kislota/phosphonic acid va phosphorous acid tarixiy noaniqligi tuzilish bilan ochildi. Inglizcha tizimli nomlar saqlandi; o‘zbekcha terminlar rasmiy IUPAC til standarti deb da’vo qilinmadi.
- HCl, SO₄²⁻, H₂SO₄, [SiF₆]²⁻ modellari 25% chetki ustunda. 3+1 maket, TNR matn va tahrirlanadigan formulalar; rastrlarda DejaVu Serif.
- Manbalar: `matn/02_04*`, `qurilma/build_02_04_sidebar.py`, `qurilma/draw_02_04.py`, `rasmlar/nomenklatura/`.
- ZIP/shrift/indeks/11 rasm/7 jadval/markerlar tekshirildi; Word sahifa renderi qilinmagan.
- Word: https://drive.google.com/file/d/1e3AymcpT2cm3z3Mrg5Xq5JgDe49p7PML/view
- Docs: https://docs.google.com/document/d/1QwWf907Mxnfv9XuI0I5bhELVpfYXOOBfXY_OkMQomKI/edit
- Ikkala nusxa havola orqali reader; Docs text eksporti muvaffaqiyatli. Keyingi mavzu — 2.5. Oksidlanish darajasi va kislotalik.

### 2.5 — Oksidlanish darajasi va kislotalik (kengaytirilgan)
- User ushbu mavzuni jiddiy, ko‘p ishlatiladigan va strukturalar bilan chuqur ishlashni so‘radi. 7 o‘rniga 9 mazmuniy bo‘lim, rekursiv hisob 3233 so‘z tayyorlandi.
- Hujjat: `chiqish/Noorganik-kislotalar-2.5-Oksidlanish-darajasi-va-kislotalik.docx` (464448 bayt).
- 9 tahrirlanadigan jadval, 8 sxema, 1 hisobiy grafik, 4 molekulyar rasm (13 yon vizual), 18 yonlavha va 6 raqamlangan ifoda.
- Oksidlanish darajasi/formal/qisman zaryad; Lewis yozuvidan hisob; xlor oksokislotalari tendensiyasi; bir xil P(+5) da turli Kₐ; perokso O; P–H hisob konvensiyasi; S–S va noekvivalent S atomlari chuqurlashtirildi.
- IUPAC 2016 nashri 2–5-bo‘limlari tekshirildi: H₃PO₃ ning ikki hisob konvensiyasi hamda S₂O₃²⁻ ning algoritmik +5/−1, nominal +6/−2 va o‘rtacha +2 farqi yashirilmadi.
- Muhim ulanishlar asosiy matn va Word jadvallarida ham tahrirlanadigan yozuvlar bilan berildi. 3+1 maket, TNR matn/jadval; rastrlarda DejaVu Serif.
- Fosfat ulushlari grafigi [OpenStax H ilovasi] dagi uch Kₐ sonidan mustaqil hisoblandi; 561 CSV satrda ulushlar yig‘indisi va uch muvozanat tekshirildi. Tayyor rasm yoki jadval dizayni ko‘chirilmadi.
- Manbalar: `matn/02_05*`, `qurilma/build_02_05_sidebar.py`, `qurilma/draw_02_05.py`, `rasmlar/oksidlanish/`.
- ZIP, TNR, indekslar, 13 rasm/9 jadval va markerlar tekshirildi; uch rasm ko‘rildi. Word sahifalari rendererda tekshirilmagan.
- Word: https://drive.google.com/file/d/1nw9HhwVEaLomKUBKvno66FYWZctAlHb9/view
- Docs: https://docs.google.com/document/d/1SwvsVQ42tnaSlCD1K3_bDbyegQ_kzMHiuTDE7PHCVm4/edit
- Ikkala nusxa havola orqali reader; Docs eksporti muvaffaqiyatli. 2-bob yakunlandi; keyingi 3.1. Ka, pKa, alfa (mundarija nomi).

### 3.1 — Kₐ, pKₐ, α
- Alohida modul: `chiqish/Noorganik-kislotalar-3.1-Ka-pKa-alfa.docx` (408808 bayt, rekursiv hisob 2975 so‘z).
- 9 bo‘lim, 9 tahrirlanadigan jadval, 5 sxema, 4 hisobiy grafik, 4 molekulyar rasm (13 yon vizual), 11 raqamlangan formula va 18 yonlavha.
- Kₐ/pKₐ/α ta’riflari, faollik va K_c birliklari, aniq kvadrat yechim, ildiz taqribi va 5% mezoni, suv avtoprotolizi, umumiy ion va diprotik shakllar taqsimoti.
- Grafiklar shartli HA/H₂A uchun hisoblandi. HF va H₃PO₄ rasmlarining konstantalari bu sonlarga teng emasligi ochiq yozildi. Ildiz taqribining x xatosi bilan pH xatosi ajratildi.
- 3+1 maket; rasmlar 25% chetki ustunda; TNR matn/formula/jadvallar, rastrlarda DejaVu Serif. K_c va C_T Word indekslari formatlandi.
- Manbalar: `matn/03_01*`, `qurilma/build_03_01_sidebar.py`, `qurilma/draw_03_01.py`, `qurilma/equilibria_03_01.py`, `qurilma/check_03_01.py`, `rasmlar/ka_pka_alfa/` (4 CSV).
- 321 monoprotik va 481 diprotik nuqtada balans/muvozanat, misollar, DOCX ZIP, TNR, indekslar, 13 rasm/9 jadval tekshirildi. Grafiklar ko‘rildi; Word/PDF sahifalari render qilinmagan.
- Word: https://drive.google.com/file/d/1vcT8mjsVDEu1UE6EQRhEIVFJ1G1f8XGr/view
- Docs: https://docs.google.com/document/d/177bxh8XsRYZibTsKy3fjt_E0fZ0ggXrCZMfkQxCtzsI/edit
- Ikkala nusxa reader havola bilan ochildi; Docs text eksporti muvaffaqiyatli. Keyingi mavzu — 3.2. Kuchga ta’sir etuvchi omillar.

### 3.2 — Kuchga ta’sir etuvchi omillar
- Alohida modul: `chiqish/Noorganik-kislotalar-3.2-Kuchga-tasir-etuvchi-omillar.docx` (462231 bayt; rekursiv hisob 3264 so‘z).
- 9 bo‘lim, 9 tahrirlanadigan jadval, 7 sxema, 2 model grafik, 4 molekulyar rasm (13 yon vizual), 8 raqamlangan ifoda va 18 yonlavha.
- Bog‘ qutbliligi/mustahkamligi, HX va HOX oilalaridagi farqli tendensiyalar, oksokislotalar, HA va A⁻ nisbiy delokallashuvi, zaryad/statistika, solvatlanish sikli, tekislovchi ta’sir, vodorod bog‘i/assotsiatsiya, harorat va kinetikadan farq.
- HF, HOCl, NO₃⁻ va H₃PO₄ modellari 25% chetki ustunda. 3+1 maket; TNR matn/formula/jadval, rastrlarda DejaVu Serif.
- IUPAC Gold Book L03506 to‘liq qisqa ta’rifi o‘qildi. Keltirilgan Born va van’t Hoff grafiklari shartli modellar, haqiqiy kislota tajribasi emas.
- `qurilma/effects_03_02.py` va `check_03_02.py`: 251 Born va 241 harorat nuqtasi, integral/differensial van’t Hoff va DOCX tekshiruvlari muvaffaqiyatli.
- Qayta qurish manbalari: `matn/03_02*`, `qurilma/build_03_02_sidebar.py`, `qurilma/draw_03_02.py`, `rasmlar/kuch_omillari/` (2 CSV).
- Rasmlar ko‘rildi; ZIP, TNR, indekslar, 13 rasm/9 jadval va markerlar tekshirildi. Word/PDF sahifalari render qilinmagan.
- Word: https://drive.google.com/file/d/14u7jv8i8_Lgp4VbZR9y7rtRHg3K6XU-l/view
- Docs: https://docs.google.com/document/d/1p9zufInryPJou3UI1wQu-0lc_zcrpIpEylMqM2YdzEI/edit
- Ikkala nusxa reader havolasi bilan ochildi; Docs text eksporti muvaffaqiyatli. Keyingi mavzu — 3.3. Dissotsiatsiya va pH.

### 3.3 — Dissotsiatsiya va pH (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-3.3-Dissotsiatsiya-va-pH.docx` (466028 bayt; rekursiv hisobda 2997 so‘z).
- Tasdiqlangan A4 13.5 + 4.5 cm maket, ko‘k/bronza ramkalar, Word matni Times New Roman; 9 mazmuniy bo‘lim, 9 tahrirlanadigan jadval, 9 tahrirlanadigan tenglama, 18 yonlavha.
- Yon ustun: 5 sxema, 4 ideal hisobiy grafik, H₃O⁺/HCl/HF/H₂SO₄ uchun 4 original molekulyar-ion tasviri. Raster belgilar DejaVu Serif. Grafiklar tajriba emas; strukturalar optimallashtirilgan koordinatalar emas.
- Kuchli kislota+suv, kuchsiz kislota, aralashmalar, H₂SO₄ ikkinchi bosqichi; molal IUPAC faollik ta’rifi va ideal molyar yaqinlashuv ajratilgan. Shartli HA Kc=10⁻⁵ HF ga tegishli emas.
- `ph_03_03.py`, `draw_03_03.py`, `build_03_03_sidebar.py`, `check_03_03.py`: 1244 grafik nuqtasi, 15 qo‘shimcha aralashma, modda/zaryad/K va DOCX tuzilishi tekshiruvlari PASS.
- DOCX Drive ID: `1HzqUrxMSaFzdQHH2_oZgc0Fpmtw3HfoB`.
- Native Google Docs ID: `1uUKIk8rEFQzxu-JrvEGGQYJrpI1zOGpTckHi32GxJMk`.
- Ikkala nusxa havola bilan reader, qidiruvda topilmaydi. Native matn eksporti 24209 bayt; 9 jadval sarlavhasi va asosiy sonli misollar saqlangani tekshirildi. Paginatsion renderer yo‘q; 9 bo‘limni 9 sahifa deb talqin qilmaslik kerak.
- Keyingi tasdiqlanishi kerak bo‘lgan mavzu: 3.4 — Titrlash va indikatorlar.

### 3.4 — Titrlash va indikatorlar (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-3.4-Titrlash-va-indikatorlar.docx`, 452236 bayt, rekursiv hisobda 2847 so‘z.
- A4 13.5+4.5 cm asosiy/yon ustun, ko‘k/bronza ramkalar, Word matni Times New Roman. 9 mazmuniy bo‘lim, 9 tahrirlanadigan jadval, 8 tahrirlanadigan tenglama, 18 yonlavha.
- 5 hisobiy grafik: kuchli/kuchsiz titrlash, H₃PO₄ bosqichlari, shartli indikator ulushlari, sonli hosila. 4 sxema; byuretka–kolba va H₃PO₄/para-nitrofenol/para-nitrofenolyat uchun 4 original qo‘shimcha tasvir.
- Ekvivalentlik ≠ oxirgi nuqta; yarim ekvivalentlik taqribi; indikator intervalini hajm og‘ishiga o‘tkazish; instrumental aniqlash; standartlash va noaniqlik yoritildi. HA Kc=10⁻⁵, indikator pK_In=7 shartli, real HF/nitrofenol o‘lchovi emas.
- `titration_03_04.py`, `draw_03_04.py`, `build_03_04_sidebar.py`, `check_03_04.py`: 3425 grafik nuqtasi, balanslar/K, analitik hosila bilan qiyos, 8 teskari endpoint hisobi, noaniqlik va DOCX tekshiruvi PASS.
- DOCX Drive ID: `1fZGHWwGHbrB7imhLT7CQPv4_fKBk01vo`.
- Native Google Docs ID: `1lRnQXj8EQmO-bxnWlwm0G1VTxreb3EfNefDvle99c5I`.
- Ikkala nusxa havola bilan reader, qidiruvda topilmaydi. Native matn eksporti 24259 bayt; 9 jadval sarlavhasi, ishlangan misollar va adabiyotlar saqlangani tekshirildi. Paginatsion renderer yo‘q: 9 bo‘lim ≠ 9 sahifa.
- Keyingi tasdiqlanishi kerak bo‘lgan mavzu: 3.5 — Buferlar va gidroliz.

### 3.5 — Buferlar va gidroliz (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-3.5-Buferlar-va-gidroliz.docx`, 523932 bayt, rekursiv hisobda 3017 so‘z.
- A4 13.5+4.5 cm asosiy/yon ustun, ko‘k/bronza ramkalar, Word matni Times New Roman. 9 mazmuniy bo‘lim, 9 tahrirlanadigan jadval, 9 tahrirlanadigan tenglama, 18 yonlavha.
- 5 hisobiy grafik: analitik nisbat/to‘liq balans, reagent ekvivalentlari, β juftlik hissasi, suyultirish, NH₄F ikki ionli gidrolizi. 4 sxema va H₂PO₄⁻/HPO₄²⁻/NH₄⁺/[Al(H₂O)₆]³⁺ uchun 4 original tuzilish tasviri.
- HH ning muvozanat faollik ifodasi va analitik miqdorlar taqribi ajratilgan; β ning aniq differensial ta’rifi/suv hadlari; yakuniy 110 mL bilan qo‘shish misoli; amfiprot ionlar, metall gidrolizi va ochiq/yopiq tizim chegaralari.
- HF 25 °C uchun OpenStax Appendix H da qayta tekshirilgan Kₐ=6.4×10⁻⁴ ishlatilgan. Shartli HA Kc=10⁻⁵ boshqa model; u HF emas.
- `buffer_03_05.py`, `draw_03_05.py`, `build_03_05_sidebar.py`, `check_03_05.py`: 1845 grafik nuqtasi, balanslar/K, β ga qarshi sonli hosila, ishlangan misollar, fosfat va DOCX tekshiruvlari PASS.
- DOCX Drive ID: `19E2mj1T2vl4275b52oxl4Re6s6Lhtjdj`.
- Native Google Docs ID: `1zcqap_KWm_OKbJqNGWYk3cjQGhfsycFd6bSKQm-z_V8`.
- Ikkala nusxa havola bilan reader, qidiruvda topilmaydi. Native matn eksporti 24768 bayt; 9 jadval sarlavhasi, ishlangan misollar va adabiyotlar saqlangani tekshirildi. Paginatsion renderer yo‘q; 9 bo‘lim ≠ 9 sahifa.
- Keyingi tasdiqlanishi kerak bo‘lgan mavzu: 3.6 — Kinetika va kataliz.

### 3.6 — Kinetika va kataliz (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-3.6-Kinetika-va-kataliz.docx`, 493146 bayt, rekursiv hisobda 3141 so‘z.
- Tasdiqlangan A4 13.5+4.5 cm maket, ko‘k/bronza ramkalar, TNR Word matni. 9 mazmuniy bo‘lim, 9 tahrirlanadigan jadval, 8 tahrirlanadigan tenglama, 18 yonlavha.
- 5 grafik: bir xil K bilan muvozanatga yaqinlashish, mustaqil energiya profillari, Arrhenius, pH–tezlik va doimiy pH da umumiy bufer katalizi. 4 sxema; H₃O⁺/H₂PO₄⁻/NH₃/NO₂ uchun 4 original molekulyar tasvir.
- IUPAC catalyst/specific/general acid catalysis/Gibbs energy of activation plain sahifalari to‘liq tekshirildi. Katalizator K ni o‘zgartirmasligi, k_obs ning shartlari, to‘yinish, standart holat va birliklar, bir nisbatli bufer chizig‘ining cheklovi ochilgan.
- Energiya profili (0→−20; 80/55/45) 1-bo‘limdagi K=4 modeli emasligi aniq aytilgan. Bufer pKa=5 H₂PO₄⁻ ning qiymati emas; NO₂ tasviri to‘liq Lewis modeli emas. Formal NO/NO₂ sikli to‘liq sanoat mexanizmi deb olinmagan.
- `kinetics_03_06.py`, `draw_03_06.py`, `build_03_06_sidebar.py`, `check_03_06.py`: 2425 nuqta, massa/muvozanat, Arrhenius qiyaligi, Eyring nisbati, pH minimumi, bufer qiyaligi, NOx atom balanslari va DOCX tekshiruvlari PASS.
- DOCX Drive ID: `1nQeKj-F6zpd6bF4JXzlUrbE53TkFfFdq`.
- Native Google Docs ID: `1ewYx98ZD4yND8iKLIvhJGwKqjlU3RNRgUSngD4SEMos`.
- Ikkala nusxa havola bilan reader, qidiruvda topilmaydi. Native eksport 25968 bayt; 9 jadval sarlavhasi, asosiy misollar va adabiyotlar saqlangani tekshirildi. Paginatsion renderer yo‘q; bo‘limlar sahifa soni emas.
- Shu bilan 3-bobning 3.1–3.6 mavzulari alohida hujjatlarda tayyor. Keyingi tasdiqlanishi kerak bo‘lgan mavzu: 4.1 — Neytrallanish va tuz hosil bo‘lishi; 4-bob kirish rasmi hali yaratilmagan.

### 4-bob kirish vizuali (2026-10-22)
- `rasmlar/4-bob-kirish-sarlavhali.png`: oldingi 3-bob vizuali uslubiy referens sifatida ishlatilib yaratilgan alohida bob kirish rasmi. Foydalanuvchi ikki variantdan 2-variantni tanladi; present_file bilan ko‘rsatildi.
- II QISM — UMUMIY KIMYO; 4-BOB — Umumiy kimyoviy xossalar; 4.1–4.5 mavzulari reja asosida so‘ralgan. Och krem/to‘q ko‘k/bronza kompozitsiya, eritmalar, kristallar va metall sirtiga oid konseptual kimyoviy illyustratsiya.
- AI konsept-art; tajribaviy foto yoki kimyoviy mexanizmning ilmiy dalili emas. Mavzu DOCXlariga kiritilmadi; bob kirishi sifatida alohida saqlandi.


## 4.1 — Neytrallanish va tuz hosil bo‘lishi (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-4.1-Neytrallanish-va-tuz-hosil-bolishi.docx`, 546352 bayt, 3099 so‘z (barcha matnlar bilan).
- 9 bo‘lim, 9 jadval, 8 raqamlangan tahrirlanadigan tenglama, 5 sxema, 4 hisobiy grafik, 4 original tuzilish tasviri, 18 yonlavha. Bob kirish rasmi alohida qoldi.
- A4, asosiy ustun 13.5 cm + yon ustun 4.5 cm, ko‘k/bronza ramkalar, Word Times New Roman; raster DejaVu Serif.
- Ajratishlar: neytrallanish ≠ pH=7; formal fosfat tuzi ≠ yagona erigan tur; ξ_max ≠ har qanday muvozanatdagi haqiqiy ξ; nazariy NaCl ≠ ajratilgan kristall. Shartli issiqlik sonlari tajriba yoki HF ga bog‘lanmagan.
- `check_04_01.py` PASS: 987 grafik qiymati, fosfat taqsimoti, zaryad balansi, kalorimetriya, chegaralovchi reagent, 10 reaksiyada atom/zaryad balansi, Word tuzilmasi, indekslar, TNR va 3:1 kenglik. Manbalar `matn/04_01_rasm_manbasi.md` da.
- DOCX: https://drive.google.com/uc?id=1tKOIfSGWxQasVL4eDj3l9uKSUxQM84JR&export=download
- Google Docs: https://docs.google.com/document/d/1Y7TKMJm8ze2igBRc-nEtjOCkEaat8zI0G6M4GmiQ7lA/edit
- Ikkala nusxa havolaga ega o‘quvchi uchun ochiq, qidiruvga chiqarilmaydi. Native matn eksporti 25796 bayt; 9 jadval sarlavhasi, tayanch hisoblar, tenglamalar va adabiyotlar saqlangan. Dastlabki QA kutilgan yaxlitlangan 1,813/0,666 o‘rniga hujjatda mavjud aniqroq 1,81291/0,66589 yozuvlari bilan tuzatildi; hujjat to‘g‘ri bo‘lgan.
- Paginatsion renderer yo‘q; 9 bo‘lim sahifa soni emas.
- Keyingi mavzu: 4.2 — Oksidlovchilik va qaytaruvchilik.


## 3.6 va 4.1 — matematik terim ta’miri (2026-10-22)
Foydalanuvchi indekslar va matematik kontekst buzilganini bildirdi. Asosiy tenglamalarning eski oddiy-run renderi almashtirildi: `qurilma/book_equations.py` endi haqiqiy tahrirlanadigan Word OMML (`m:oMath`, `m:f`, `m:sSub`, `m:sSup`) yaratadi. Har mavzuda 8 raqamlangan tenglama saqlandi; uzun ifodalar bir nechta qatorga bo‘lindi (3.6: 10 OMML qatori / 9 kasr; 4.1: 13 qator / 5 kasr). Surat-maxrajlar struktural, chiziqli slash emas. Asosiy matn TNR; native Equation obyektlarida matematik shrift Cambria Math.

Matn/jadval/yonlavha tokenlari uzunligiga qarab ajratiladi: `k_ref` endi `k_r`+`ef` ga bo‘linmaydi. `ν_S` va yetishmagan indekslar, `10⁻pH` butun darajasi tuzatildi. 3.6 ning asosiy ustuni ham 13.5 cm ga tenglashtirildi (yon 4.5 cm). Ilmiy mazmun, konstantalar, grafik va jadvallar o‘zgartirilmadi.

`check_03_06.py`, `check_04_01.py`, yangi `check_formula_repairs.py` PASS. Google Docs orqali qayta DOCX eksportida OMML sonlari va fraction/subscript/superscript strukturalari saqlanganligi tekshirildi. Google Docs PDF renderlari olindi (har ikkisi 10 sahifa); Eyring/Arrhenius, integral/yarim vaqt, pH katalizi, proton almashinuvi, fosfat, Hess/kalorimetriya va yakuniy aralashma formulalari sahifalarda ko‘rib tekshirildi. Bu Google renderi, lokal MS Word renderi emas.

**Quyidagi yangi havolalar eski nusxalarni almashtiradi:**
- 3.6 DOCX: https://drive.google.com/uc?id=1awW8lhvTH0I--QQBvgI9i9cGW1qin88T&export=download
- 3.6 Google Docs: https://docs.google.com/document/d/1zZrcAJoPGla1Hmegu8UA_QkCzcnnImtroc6VetMzDWE/edit
- 4.1 DOCX: https://drive.google.com/uc?id=1IbeLeEPCA71-Oi5J569Ktapv1jL2gXd0&export=download
- 4.1 Google Docs: https://docs.google.com/document/d/1pR4yp47Hs3KjcJePBo_8kAHOC5hSIeG0RMlCH1uZbuQ/edit
Hamma yangi nusxalar reader/discovery=false. Oldingi Drive fayllari o‘chirilmagan yoki ustidan yozilmagan.


## 4.2 — Oksidlovchilik va qaytaruvchilik (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-4.2-Oksidlovchilik-va-qaytaruvchilik.docx`, 561634 bayt, 4191 so‘z (matematik matnni qo‘shib hisoblagan).
- 9 mazmuniy bo‘lim: kislota kuchi/redoks roli, E–ΔG–K, Nernst/pH, ion–elektron balans, nitrat mahsulotlari, S oilasi, P–H/O–H, disproportsiyalanish/peroksid, Mn–Fe ishlangan hisob. Passivlanish batafsil 4.3 ga qoldirildi.
- A4 13.5:4.5 cm; 9 jadval, 8 raqamlangan Equation (17 native OMML qatori / 3 strukturali kasr), 4 model grafik + CSV, 5 sxema, 4 original tuzilish tasviri, 18 yonlavha. Word matni TNR, matematik shrift Cambria Math; raster DejaVu Serif.
- H₃PO₃/H₃PO₂ ulanishlari va P–H soni alohida rasmlar bilan; 2.5 dagi H(+1) konvensiyasi aniq saqlandi. P–H modellari yon ustun uchun faqat ulanishni qoldiradigan crop orqali kattaroq ko‘rinishda berildi; to‘liq modellar saqlangan.
- `check_04_02.py` PASS: 689 grafik qiymati, 30 reaksiyada atom va zaryad balansi, proton/elektron/moddiy sarf, Nernst/ΔG identiklari, native math, jadvallar/tasvirlar/ustunlar. 3.6/4.1 formula ta’miri regressiyasi ham PASS.
- Yakuniy Google Docs→DOCX eksporti 1564684 bayt; 17 native Equation qatori, 3 kasr, 9 jadval sarlavhasi va 8 raqam saqlangan.
- Yakuniy Google PDF renderi 855765 bayt, 10 sahifa. Dastlab aniqlangan bo‘sh sahifa (standart o‘lchamli page-break paragrafi) 1 pt break bilan tuzatildi; 7-bo‘lim yonlavhasining alohida sahifaga oqishi ikki rasmning takroriy umumiy captionlarini ixchamlashtirish bilan bartaraf qilindi. Hech bir sahifa deyarli bo‘sh emas. Nernst, nitrat, fosfor va peroksid sahifalari rasmlar orqali ko‘rildi; lokal MS Word renderi bajarilmagan.
- Yakuniy DOCX: https://drive.google.com/uc?id=1qcX-44D6YlvIHTsoXnmYUqWGEu6eOOcL&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1sJyLjLwpMDH0GePMj_2hiqby1i3jRrAhUMZn2RmSkvg/edit
- Ikkala yakuniy nusxa reader/discovery=false. QA jarayonida yuklangan oldingi 4.2 juftliklari (`1a_jdk0eK2SiQsKN5z70tTnH40tkLS6bV`/`1eLVmRsGA9Ihna91P2WmioiWeT8ifbm3q57JfHRqZrG0` va `1ypkfIZYh_IjZapWgWuhfn6Ao3s87H8BL`/`1L5_QsJM-oVPOfE_AxjIHpFJAFrH35XT3caXS0qlnbUI`) yakuniy emas; foydalanuvchiga faqat yuqoridagi yakuniy havolalar beriladi. Eski fayllar o‘chirilmagan.
- Keyingi mavzu: 4.3 — Passivlanish.


## 4.3 — Passivlanish (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-4.3-Passivlanish.docx`; 551260 bayt, 3850 so‘z (matematik matn bilan).
- 9 bo‘lim: immun/faol/passiv holat; real parda va transport; faol–passiv egri; oksidlovchi kislota va aralash potensial; dinamik qalinlik; Cl⁻/pitting/tirqish; transpassivlik; dalillar/LPR; Faraday va mahalliy maydon hisobi.
- A4 13.5:4.5 cm, ko‘k/bronza ramkalar. 9 jadval, 8 raqamlangan Equation (18 OMML qatori, 8 haqiqiy kasr), 4 hisobiy grafik+CSV, 5 sxema, 4 original jarayon kesimi, 18 yonlavha. TNR matn, Cambria Math Equation, DejaVu Serif raster. Bob kirish rasmi alohida.
- Noldan farqli ichki korroziya toklari, immun≠passiv, oksid cho‘kmasi≠himoya parda, E°≠passivlanish tezligi, transpassiv tok≠faqat metall yo‘qotilishi, o‘rtacha massa≠maksimal pitting chuqurligi ajratildi. Sovuq konsentrlangan H₂SO₄ dagi barcha sekin erish sof oksid passivligi deb umumlashtirilmagan. Amaliy reagent/ishlov/idish tanlash retsepti berilmagan.
- `check_04_03.py` PASS: 1604 model nuqtasi; funksiyalar uzluksizligi, ikki katod kesishishi, qalinlik ODE, Stern va Faraday, maydon masshtabi; 8 atom/zaryad balansi; Word matematikasi, indekslar, jadvallar/rasmlar/ustunlar. 4.2 va 3.6/4.1 formula regressiyalari ham PASS.
- Ishlangan model: Al³⁺ nishoni, 10 cm², 1 μA/cm² metall toki, 24 soat → 0.08053745 mg; bir tekis 0.02982869 μm; f=0.001 bo‘lsa mahalliy o‘rtacha 29.82869 μm. Eksperimental qiymat yoki maksimal pit chuqurligi emas.
- Native Google Docs→DOCX eksporti 1573053 bayt; 18 native math qatori, 8 kasr, 9 jadval sarlavhasi, 8 tenglama raqami va tayanch sonlar saqlangan. Google PDF 854274 bayt, 10 sahifa; birinchi OCP, parda ODE, Stern–Geary va Faraday sahifalari ko‘rib tekshirildi. Lokal MS Word renderer yo‘q.
- Birinchi QA renderida 1-bo‘limning oxirgi ikki qatori alohida sahifaga oqqan; kirishdagi takroriy iboralar ma’no saqlangan holda ixchamlashtirildi, yakuniy renderda deyarli bo‘sh sahifa yo‘q. Oldingi xususiy QA Docs `1IH-9LcTKgSoa9xo3oZgIQSMIrVTjoodLFfjwuWyN2QU` foydalanuvchiga yetkazilmaydi.
- Yakuniy DOCX: https://drive.google.com/uc?id=1YaglOXDRIVgq-Lz4GCXPWpmfPpi8ddXM&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1801Z2svEZdCHeVt4P433UcueH3L4H_FzdHZJkFhrdXQ/edit
- Ikkala yakuniy nusxa reader/discovery=false. Manbalar va model cheklovlari `matn/04_03_rasm_manbasi.md` da.
- Keyingi mavzu: 4.4 — Kompleks va cho‘kma hosil qilish.


## 4.4 — Kompleks va cho‘kma hosil qilish (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-4.4-Kompleks-va-chokma-hosil-bolish.docx`; 732603 bayt, 5071 so‘z (matematik matn bilan).
- 11 bo‘lim: kislota roli va metall turlari; Q_sp/K_sp va to‘yinganlik; bosqichli va umumiy β konstantalari; protonlanish va shartli konstanta; kislota anioni (kuzatuvchi/ligand/cho‘ktiruvchi); komplekslanish orqali erish; tanlab cho‘ktirish; amfoterlik; kislota eruvchanlikka ta’siri; muvozanatni yechish tartibi; AgCl–ammiak ligand balansi ishlangan hisobi.
- A4 13.5:4.5 cm, ko‘k/bronza ramkalar. 11 jadval, 11 raqamlangan Equation (23 native OMML qatori, 13 haqiqiy kasr), 4 hisobiy grafik+CSV, 7 sxema, 5 original jarayon tasviri, 22 yonlavha. TNR matn, Cambria Math Equation, DejaVu Serif raster.
- Kislota faqat proton manbai emasligi markaziy g‘oya: anion kuzatuvchi, ligand yoki cho‘ktiruvchi bo‘lishi mumkin; komplekslanish erkin ionni kamaytirib umumiy eruvchanlikni oshiradi; pH va protonlanish yo‘nalishni o‘zgartiradi. Tanlab cho‘ktirishda faqat K_sp farqi yetarli emas (F_M yon reaksiyasi); amfoterlik redoks emas. Modda balansi, faza mavjudligi (n_s≥0, Q_sp≤K_sp) va ligand sarfi birga tekshiriladi.
- Model qiymatlari: AgCl K_sp,c=1,6×10⁻¹⁰, β₂,c=1,7×10⁷, pK_a,c=9,25; amfoterlik uchun xayoliy K_sp,c=10⁻³⁰, β₄,c=10³⁴ (minimum pH≈5,619, C_sat≈5,55×10⁻⁵); tanlab cho‘ktirish A²⁺/B²⁺ K_sp,c 10⁻¹⁸/10⁻¹², C_M,0=0,0100. Ishlanga hisob: l=0,00779980, s=0,000406984, [Ag⁺]=3,93136×10⁻⁷, kompleks ulushi 99,903%; ligand sarfini e’tiborsiz qoldirishda s=0,000442976 (+8,84%). Barchasi ochiq shartli model; tajriba ma’lumoti emas.
- `check_04_04.py` PASS: 1604 model nuqtasi; spetsiasiya/protonlanish/eruvchanlik/amfoterlik minimumi/tanlab cho‘ktirish/ligand balansi identiklari; 7 atom va zaryad balansi; Word matematikasi, indekslar, jadvallar/rasmlar/3:1 ustunlar.
- Native Google Docs→DOCX roundtrip 1723450 bayt; 23 OMML qatori, 13 kasr, 11 jadval sarlavhasi va (4.4.1)…(4.4.11) raqamlari saqlangan. Yakuniy Google PDF 1092341 bayt, 12 sahifa; har bir bo‘lim bitta sahifada, bo‘sh sahifa yo‘q. Sahifalar 1, 2, 3, 5, 6, 9, 11 ko‘z bilan tekshirildi (formulalar, jadvallar, yon ustun rasmlari). Lokal MS Word renderer yo‘q.
- Dastlabki renderda 16 sahifa bo‘lib, 1/3/4/5-bo‘limlar ikkinchi bo‘sh sahifaga oqqan; matn ixchamlashtirish, jadval qatorlarini kamaytirish va `space_after` 5→4 pt orqali yakuniy 12 sahifaga yetildi. Jadval raqamlari bo‘limlar bilan moslashishi uchun 9-bo‘limga alohida jadval qo‘shildi (jami 11 jadval). Yon ustun yorlig‘i “HISOBIY GRAFIK/TUSHUNTIRUVCHI SXEMA” bo‘lim turiga qarab avtomatik to‘g‘rilanganda “HISOBIY GRAFIK” har doim chiqayotgani aniqlanib, tuzatildi.
- QA paytida yuklangan 9 ta oraliq Docs/DOCX juftlik muxlatga solindi; foydalanuvchiga faqat quyidagi yakuniy havolalar beriladi.
- Yakuniy DOCX: https://drive.google.com/uc?id=15CqV8Ym67612CPd6kTYRqjOwe-5qNBvk&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1O4VZZNWnTCzlX2aaOCrhlOTW-82GfWFzVOOXRavOZK8/edit
- Ikkala yakuniy nusxa reader/discovery=false. Manbalar, model va render QA `matn/04_04_rasm_manbasi.md` da.
- Keyingi mavzu: 4.5 — Parchalanish.


## 4.5 — Parchalanish (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-4.5-Parchalanish.docx`; 695093 bayt, 4771 so‘z (matematik matn bilan).
- 11 bo‘lim: parchalanish va uning qarindoshlari; termodinamik mezon (ΔG, T*); muvozanat konstantasi (van ’t Hoff); kinetika: termodinamika bilan farqi; yorug‘lik, radiatsiya va zanjirli fotokimyo; dismutatsiya; kondensatsiya; muhitning ta’siri (pH, katalizator, konsentratsiya); barqarorlik ierarxiyasi; parchalanish mahsulotlarini aniqlash; ishlangan hisob (termodinamik chegara va kinetik blok).
- A4 13.5:4.5 cm, ko‘k/bronza ramkalar. 11 jadval, 11 raqamlangan Equation (27 native OMML qatori, 14 haqiqiy kasr, 63 pastki, 25 yuqori), 4 hisobiy grafik + CSV (401 nuqta har biri), 7 sxema, 5 original illyustratsiya, 22 yon lavha. TNR matn, Cambria Math Equation, DejaVu Serif raster. Bob kirish rasmi alohida.
- Markaziy g‘oya: termodinamik qulaylik va kinetik blok — boshqa savollar. HNO₃ uchun ΔG°(298,15)=−155,18 kJ/mol va lg K≈27,2, ammo yuqori aktivatsiya to‘sig‘i uni idishda saqlanishga imkon beradi; H₂SO₄ uchun T*=779,7 K (≈507 °C) va lg K(298,15)=−14,33. Kimyoviy «kislota o‘zgardi» holatlari dissotsiatsiya, gidroliz, redoks, kondensatsiya va polimerlashdan aniq ajratildi; dismutatsiya IUPAC D01799/C01217 asosida berildi.
- Model qiymatlari: ΔH°, ΔS° OpenStax App. G dan (HNO₃(l) −174,1/155,6 — suyuq qiymat, eritma qiymati emas); ΔG° qayta hisoblangan; kinetika A=1,0×10¹³ s⁻¹, E_a=100 kJ/mol (o‘quv); sulfit ulushlari K_a1=1,6×10⁻², K_a2=6,4×10⁻⁸ bo‘yicha, pH 7 da α(SO₂·H₂O)=3,81×10⁻⁶; kondensatsiya entalpiyalari +31,2/+58,2/−63,9/−7,9/+14,3/+57,7 kJ/mol. 14 ta atom va zaryad balansi o‘tkazildi (HNO₃: 4HNO₃→4NO₂+2H₂O+O₂; H₂S+H₂SO₃: 2H₂S+H₂SO₃→3S+3H₂O). Barchasi ochiq shartli model; tajriba ma’lumoti emas.
- `check_04_05.py` PASS: 1604 model nuqtasi; termodinamik, kinetik va sulfit identifikatsiyalari; 14 atom/zarjad balansi; Word matematikasi, indekslar, jadvallar/rasmlar/3:1 ustunlar.
- Native Google Docs→DOCX roundtrip 1687218 bayt; 27 OMML qatori, 14 kasr, 11 jadval sarlavhasi va (4.5.1)…(4.5.11) raqamlari saqlangan. Yakuniy Google PDF 1076162 bayt, 12 sahifa; har bir bo‘lim bitta sahifada, bo‘sh sahifa yo‘q. Sahifalar 1, 5, 8, 11, 12 ko‘z bilan tekshirildi. Lokal MS Word renderer yo‘q.
- Dastlabki render 16 sahifa bo‘lib, 1/2/4/7-bo‘limlar ikkinchi sahifaga oqqan; matn ixchamlashtirish, jadval katak bo‘shliqlarini 70→50 twips ga qisqartirish, jadval qatorlarini birlashtirish va sxema balandligini 5 qatorga moslash orqali yakuniy 12 sahifaga yetildi. Besh qatorli sxemalarda oxirgi blok kesilib qolgani topildi va tuzatildi; sxema matnidagi «Fotoskimyoviy», «Nitrit», «Xron kislota», «Notheri yo‘l», «To‘sig‘ katalizator» kabi xatolar tuzatildi.
- Xavfsizlik: HNO₃, HClO₃/HClO₄, HCN va H₂S uchun tayyorlash yoki qayta ishlash ko‘rsatmasi berilmadi; saqlash faqat umumiy tamoyil darajasida.
- QA paytida yuklangan oraliq Docs/DOCX juftliklar muxlatga solindi; foydalanuvchiga faqat quyidagi yakuniy havolalar beriladi.
- Yakuniy DOCX: https://drive.google.com/uc?id=1JqmkA5dppBO9ZL17VVYMZ_BBI7DDpr5T&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/13khlAyiQBp8-D-MT0Z1vdqlyCb4cbVCFLufVPTMFdlM/edit
- Ikkala yakuniy nusxa reader/discovery=false. Manbalar, model va render QA `matn/04_05_rasm_manbasi.md` da.
- Keyingi mavzu: 5.1 — Olishning umumiy usullari.


## 5.1 — Olishning umumiy usullari (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-5.1-Olishning-umumiy-usullari.docx`; 797217 bayt, ~3817 so‘z (matematik matn bilan).
- 11 bo‘lim: umumiy tamoyillar (uch o‘lchak va mahsulot talablari); usullarning tasnifi (5 oila + tiklash); termodinamik mezon (ΔG°, K); muvozanatni boshqarish (T, p, konsentratsiya, mahsulot chiqarish); kinetika: tezlik va to‘siq (reagent usuli, qalqon usuli, mass transfer, issiq nuqta); reaksion sxemadan oluvga (bloklar, kaskad); unum, qaytarilish va resurs samaradorligi; ajratish (Fenske, bug‘lash, ekstraksiya, cho‘ktirish, adsorbsiya, membrana); ekologiya va xavfsizlik tamoyillari; tayyor kislota sifati va hujjatlashtirish; ishlangan hisob (pyritdan H₂SO₄ material balansi).
- A4 13.5:4.5 cm, ko‘k/bronza ramkalar. 11 jadval, 11 raqamlangan Equation (33 native OMML qatori, 21 haqiqiy kasr, 61 pastki, 8 yuqori), 5 hisobiy grafik + CSV (mivozanat 401, kaskad 401, chiqindi 401, buglanish 401, dG 251 nuqta), 6 sxema + 1 qo‘shimcha sxema, 5 original illyustratsiya, 22 yon lavha. TNR matn, Cambria Math Equation, DejaVu Serif raster. Bob kirish rasmi alohida.
- Markaziy g‘oya: usul tanlash uch o‘lchakdan o‘tadi — termodinamik (ΔG°, K), kinetik (to‘siq) va texnologik (ajratish, konsentratsiya, chiqindi, xavfsizlik). Termodinamik qulaylik tezlikni belgilamaydi; muvozanat faqat to‘rt dastak bilan boshqariladi; tozalash va konsentratsiya 5.2–5.4 ga, kislota oilalari 6–10 ga, xavfsizlik 12-bo‘limga yo‘naltiriladi.
- Model qiymatlari: ΔH°/ΔS° OpenStax App. G dan, ΔG° va lg K qayta hisoblangan (SO₂+½O₂→SO₃: ΔH°=−98,89, ΔS°=−94,04, ΔG°(298,15)=−70,85, lg K=12,413; H₂+Cl₂→2HCl: −184,61/+20,00, −190,58, 33,39; 4NH₃+5O₂→4NO+6H₂O: −1170,38/−534,00, −1011,17, 177,15; N₂O₄⇌2NO₂: +55,30/+175,80, +2,89, −0,506). Muvozanat modeli N₂O₄⇌2NO₂ (ideal gaz): X 250 K da 0,0326/0,0103/0,0033 va 298,15 K da 0,2691/0,0880/0,0279 (1/10/100 bar); van ’t Hoff 300→400 K da K 255 marta. Fenske: α=1,1→61,79; 2,0→8,50; 5,0→3,66 pog‘ona. Pyrit balansi (1000 t FeS₂, X=0,96, yutilish 0,98): H₂SO₄ 1538,15 t (nazariy 1634,94), Fe₂O₃ 665,49 t, unum 94,08 %, chiqindi omili 0,4604 kg/kg, 96 % eritma uchun suv 346,61 t. Barchasi ochiq shartli model; tajriba ma’lumoti emas.
- Modelda topilgan xato tuzatildi: `prep_05_01.py` da SO₂ oksidlanishida O₂ reagent emas, mahsulot tomonida yozilgan edi (ΔS°=+111,16, ΔG°=−132,03 chiqgan). To‘g‘rilgan: ΔS°=−94,04, ΔG°=−70,85, lg K=12,413; matn, jadval va grafiklar qayta yig‘ildi.
- `check_05_01.py` PASS: model nuqtalari (termodinamik, muvozanat, van ’t Hoff, kaskad, Fenske, pyrit zanjiri, E-faktor, suv balansi), CSV qator sonlari, matndagi barcha asosiy raqamlar, Word matematikasi (33 OMML/21 kasr/61 pastki/8 yuqori), 11 jadval sarlavhasi, 11 formula raqami, 17 rasm, 22 yon lavha, 3:1 ustunlar, TNR/Cambria Math shriftlari.
- Native Google Docs→DOCX roundtrip 1773629 bayt; 33 OMML qatori, 21 kasr, 61 pastki, 8 yuqori, 17 rasm, 11 jadval sarlavhasi va (5.1.1)…(5.1.11) raqamlari saqlangan. Yakuniy Google PDF 1169077 bayt, 11 sahifa; har bir bo‘lim aynan bitta sahifada, bo‘sh sahifa yo‘q. Sahifalar 1, 3, 4, 5, 6, 8, 9, 11 ko‘z bilan tekshirildi.
- Dastlabki renderda 12 sahifa bo‘lib, 11-bo‘limning adabiyotlari ikkinchi sahifaga oqqan; hisob jadvali qatorlari birlashtirildi, adabiyotlar 9→8,5 pt ga tushirildi, ogohlantirish qisqartirildi. (5.1.11) formulasi ikkinchi qatori ustun chegarasidan chiqqan edi — qatorga bo‘lib yozildi.
- Xavfsizlik: konsentratsiya tanlash, texnologik parametr, reaktorni yig‘ish, idish materiali va amaliy tayyorlash ko‘rsatmasi berilmadi; xavfsizlik faqat umumiy tamoyil (yopiq tizim, ikki pog‘onali himoya, kislotani suvga quyish tartibi) darajasida. OpenStax App. F savdo kislotalari tarkibi faqat taqqoslash ma’lumoti sifatida.
- QA paytida yuklangan 4 ta oraliq native Docs muxlatga solindi; foydalanuvchiga faqat quyidagi yakuniy havolalar beriladi.
- Yakuniy DOCX: https://drive.google.com/uc?id=1WpGu528y6v8T3xSSz0ofIQhymf337cGV&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1RdFsZCju6_YqF6m7yVq79gr5v6B3DgXP75e-B8HY54A/edit
- Ikkala yakuniy nusxa reader/discovery=false. Manbalar, model va render QA `matn/05_01_rasm_manbasi.md` da.
- Keyingi mavzu: 5.2 — Tozalash.

### 5-bob kirish vizuali (2026-10-22)
- `rasmlar/5-bob-kirish-sarlavhali.png` (1664×2496, A4 150 dpi): 4-bob vizuali uslubiy referens sifatida ishlatilib yaratilgan 5-bob kirish rasmi. Alohida saqlanadi, mavzu DOCXlariga kiritilmaydi.
- Kompozitsiya: yuqorida «II QISM · UMUMIY KIMYO» (bronza, letter-spacing 7 px), ostida ingichka qo‘ng‘iroq chizig‘i va olmos; «5-BOB»; katta to‘q ko‘k sarlavha «Olish, tozalash, / konsentrlash» (Playfair Display 160 px, ikki qator, 190 px qator oralig‘i); chiziq + olmos; «BOB MAVZULARI»; 4 ta mavzu (5.1 Olishning umumiy usullari, 5.2 Tozalash, 5.3 Quritish va suvsizlantirish, 5.4 Sanoat prinsiplari) — raqamlar bronza, nomlar to‘q ko‘k, har biri ostida ingichka qo‘ng‘iroq chizig‘i.
- Fon: `rasmlar/5-bob-fon.png` — AI konsept-art (distillatsion ustun, mis kondenser, amber/teal suyuqli kolbalar, kristallar, oltin nur). AI rasmga matn joylanmagan: barcha yozuvlar dasturiy tipografiya bilan qo‘shilgan, shuning uchun o‘zbekcha imlo aniq.
- Fon kadrga solindi va kattalashtirildi (chapdan 0–844 px, 100–1366 qatori) — jihozlar o‘ng pastki burchakka surilib, sarlavha va mavzular ro‘yxati toza krem maydonda qoldi; yuqoriga yengil krem parda qo‘llandi.
- Shriftlar: `rasmlar/shriftlar/` — Playfair Display (400/500/600) va Libre Baskerville (400/700) latin TTF; @fontsource woff2 paketlaridan fontTools yordamida TTF ga o‘tkazildi. Sil OFL 1.1 (fayllar `OFL-PlayfairDisplay.txt`, `OFL-LibreBaskerville.txt`).
- Generator: `qurilma/kirish_5_bob.py` (Pillow; deterministik, qayta ishga tushirilsa bir xil natija).
- QA: birinchi renderda sarlavha qatorlari ustma-ust tushgan (104 px qator oralig‘i), ro‘yxat apparat ustiga chiqqan, chiziq+olmos birinchi mavzu ustiga tushgan edi — barchasi tuzatildi (qator oralig‘i 190 px, fon kadrga solindi, element tartibi 4-bobdagidek qilindi).
- AI konsept-art; tajribaviy foto yoki mexanizmning ilmiy dalili emas.

## 5.2 — Kislotalarni tozalash (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-5.2-Kislotalarni-tozalash.docx`; 910584 bayt; 11 sahifa (har bir bo‘lim aynan bitta sahifada).
- 11 bo‘lim: tozalash o‘lchovi va sifat chegaralari; ifloslik manbalari; usullarning tasnifi (mexanik / fizik-kimyoviy / kimyoviy / membranaviy / kombinatsiyalangan); bug‘lash, azeotrop va rektifikatsiya; cho‘ktirish, Ksp va kompleks niqoblash; kimyoviy tozalash (redoks, sulfid, NO₂ qaytarish); adsorbsiya, ion almashinuv va membrana; kislota oilalari bo‘yicha tozalash; tozalash zanjiri va resurs samaradorligi; sifat nazorati va hujjatlashtirish; ishlangan hisob (rangli HNO₃ + sulfat kislotadagi Fe).
- A4 13,5:4,5 cm, ko‘k/bronza ramkalar. 11 jadval, 11 raqamlangan Equation guruh (40 native OMML qatori, 25 kasr, 63 pastki, 24 yuqori), 5 hisobiy grafik + 6 CSV, 7 sxema, 5 original illyustratsiya, 22 yon lavha. TNR matn (10,5 pt), Cambria Math Equation (9,5 pt), DejaVu Serif raster. Bob kirish rasmi alohida (5-bob).
- Markaziy g‘oya: tozalash — bitta usul emas, zanjir; har bir usul ifloslik turiga, reagent sarfi va chiqindi tarkibiga bog‘liq tanlanadi. Azeotrop, Ksp va selektivlik — uchta asosiy chegara; resurs samaradorligi (chiqindi omili) usul tanlash mezoni.
- Model qiymatlari: Ksp/Kf — OpenStax App. J/K dan; azeotroplar (68,8 %/120,5 °C; 20,2 %/108,6 °C; 98,3 %/337 °C) va Ph. Eur. 6.0 HNO₃ monografiyasi (68,0–70,0 %, ρ≈1,41, Cl⁻ ≤ 0,5 ppm, SO₄²⁻ ≤ 10 ppm, Fe ≤ 10 ppm, og‘ir metallar ≤ 2 ppm, kul ≤ 0,01 %, rang ≤ Y6) manbalardan. Model: Fe³⁺ pH 2 da 4,0×10⁻² M; Cu²⁺ pH 7 da 2,2×10⁻⁶ M; Cd²⁺ pH 8 da 5,9×10⁻³ M; Cu²⁺+4NH₃ pH 2 da 1,29×10⁻⁹ M; kaskad Φ=10/100/1000/10000 → 6/3/2/1,5 bosqich; Fenske α=1,2/1,5/2,0/3,0 → 32,3/14,52/8,5/5,36 pog‘ona; R_min α=1,5/2,0/3,0 → 3,50/1,70/0,80; McCabe-Thiele α=2,0 → 16 pog‘ona, α=3,0 → 7, α=1,5 da R_min > R — dizayn mumkin emas; suv balansi 100 kg da 48,98/30,61/23,47 kg; ion almashinuv fronti kiring BV = 4,96/1,28/0,34 (C₀ = 50/100/200 mg/L), q_eq 48,08/49,02/49,51 mg/g; Model A: n(NO₂) 86,938 kmol, H₂O 0,7831 t, O₂ 0,6955 t, HNO₃ +5,4779 t, w = 68,55 %; Model B: n(Fe) 5,3715 kmol, Fe(OH)₃ 0,5741 t, CaSO₄ 1,0969 t, CaO 0,4519 t, E = 0,00167 kg/kg, CaCO₃ yo‘li 0,8065 t reagent va 0,7903 t H₂SO₄ yo‘qotish. Barchasi ochiq shartli model; tajriba ma’lumoti emas.
- Modelda topilgan xatolar tuzatildi: (1) kaskad signi — log(1/Φ) emas, log(target/1) yo‘nalishi; (2) McCabe-Thiele α=1,5 da 400 qadamli iteratsiya limitiga urilib, R_min > R holati «dizayn mumkin emas» deb aniq belgilandi; (3) ion almashinuvning dastlabki kinetik Thomas modeli beqaror bo‘lib, plug-flow Langmuir modeliga almashtirildi (C₀ = 50/100/200 mg/L, q_max = 50 mg/g); (4) fronti kiring qiymati 4,965 → 4,96 ga yaxlitlandi va matn, jadval, grafik hamohishtirildi; (5) massa balansi ko‘rsatkichi 49,5 → 48,08 mg/g ga tuzatildi.
- `check_05_02.py` PASS: model nuqtalari (eruvchanlik, Ksp sulfidlari, kaskad, Fenske, R_min, McCabe-Thiele, suv balansi, fronti kiring, Model A/B), CSV qator sonlari, matndagi barcha asosiy raqamlar, Word matematiği (40 OMML/25 kasr/63 pastki/24 yuqori), 11 jadval sarlavhasi, 11 formula raqami (5.2.1)…(5.2.11), 17 rasm, 22 yon lavha, TNR/Cambria Math shriftlari, xavfsizlik chegarasi matni.
- Sahifalash: dastlabki render 18 sahifa bo‘ldi (har bir bo‘limdan keyin ortiqcha sahifa). Tuzatishlar: matn 11 → 10,5 pt, qator oralig‘i 1,12 → 1,05, jadval shrifti 9,5 → 8 pt va katak chekkasi 50 → 28 dxa, formula shrifti 11 → 9,5 pt va qator oralig‘i 1,15 → 1,0, 7 ta bo‘lim matni qisqartirildi, 11-bo‘limning adabiyotlar bloki bo‘sh yon ustunga ko‘chirildi → 11 sahifa, bo‘sh sahifa yo‘q.
- Native Google Docs → DOCX roundtrip 1875624 bayt: 40 OMML qatori, 25 kasr, 63 pastki, 24 yuqori, 17 rasm saqlangan. Yakuniy Google PDF 1309423 bayt, 11 sahifa. Sahifalar 1, 4, 7, 11 ko‘z bilan tekshirildi.
- Xavfsizlik: konsentratsiya tanlash, texnologik parametr, reaktorni yig‘ish, idish materiali va amaliy tayyorlash ko‘rsatmasi berilmadi; sulfid va ammiak usullari faqat nazariy (selektivlik, Ksp/Kf, chegaralar) darajasida; xavfsizlik umumiy tamoyil darajasida.
- QA paytida yuklangan 5 ta oraliq native Docs muxlatga solindi; foydalanuvchiga faqat quyidagi yakuniy havolalar beriladi.
- Yakuniy DOCX: https://drive.google.com/uc?id=1Xc1ihq0351786K_dmu8G-y3mWmaMBCsi&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1pDaJYemFzSD60Y2JR2WNtb4DZPsPCb0e7YUUeddUgHM/edit
- Ikkala yakuniy nusxa reader/discovery=false. Manbalar, model va render QA `matn/05_02_rasm_manbasi.md` da.
- Keyingi mavzu: 5.3 — Quritish va suvsizlantirish.

## 5.3 — Quritish va suvsizlantirish (2026-10-22)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-5.3-Quritish-va-suvsizlantirish.docx`; 890756 bayt; 11 sahifa (har bir bo‘lim aynan bitta sahifada).
- 11 bo‘lim: suvning holatlari va namlik o‘lchovi; higroskopiklik, deliquescence va efflorescence; quritish usullarining tasnifi; bug‘latish, vakuum va desiccator usullari; azeotropik quritish; kimyoviy quritgichlar va molekulyar sitalar; kristall gidratlarini quritish; ekstraksiya, adsorbsiya va membrana; suv miqdori nazorati, namuna va hujjat; energetika, iqtisodiyot va resurs; ishlangan hisob (gidrat quritish + azeotrop).
- A4 13,5:4,5 cm, ko‘k/bronza ramkalar. 11 jadval, 11 raqamlangan Equation guruh (43 native OMML qatori, 10 kasr, 23 pastki, 3 yuqori), 5 hisobiy grafik + 5 CSV, 7 sxema, 5 original illyustratsiya, 22 yon lavha. TNR matn (10 pt), Cambria Math Equation (9,5 pt), DejaVu Serif raster. Bob kirish rasmi alohida (5-bob).
- Markaziy g‘oya: quritish — ifloslikni yo‘qotish emas, kislotaning o‘ziga xos komponentini (suvni) kamaytirish; usul tanlash uch o‘lchakdan o‘tadi — talab darajasi (namlik o‘lchovi), muvozanat chegarasi (azeotrop, adsorbsiya izotermasi) va resurs balansi (energiya + chiqindi). Azeotropik quritish 5.2-bo‘limdagi kislotaning o‘z azeotrop chegarasini yorib o‘tadi.
- Model qiymatlari: ΔvapH = 44,01 kJ/mol (25 °C, OpenStax App. G) va 40,657 kJ/mol (100 °C, CRC); p_sat(25 °C) = 2,858 kPa; Klausius–Klapeiron modeli: 101,325 kPa → 100,0 °C; 10,0 → 43,96; 2,5 → 17,80; 1,5 → 9,22; 0,1 kPa → −28,96 °C. Muvozanat namligi (w_m = 0,05, C = 10): 20/50/80/95 % RH → 0,0357/0,0455/0,0488/0,0497 kg/kg. Higroskopiklik (Ph. Eur. 5.11): model 3,50 % → «higroskopik». Karl Fischer: 2,000 g namuna, 0,50 mol/L, 22,2 mL → 0,2000 g suv → 10,00 %. P₂O₅ sig‘imi 38,08 %; CaCl₂ 0,974 kg/kg; MgSO₄ 1,048 kg/kg; sital 3A/4A/5A/13X — 19,5/20,5/21,0/23,5 %, 100 kg suv uchun 487,8 kg 4A. CuSO₄·5H₂O → ·H₂O: n = 4,0051 kmol, suv 288,60 kg, mahsulot 711,40 kg, suv ulushi 36,08 % → 10,14 %; anhiddirgacha 360,75 kg suv va 639,25 kg mahsulot. Azeotrop (toluen): 84,1 °C, suv 19,8 %, 1 kg toluen → 0,2469 kg suv; 1000 kg 68 % li HNO₃ → 0,5 %: suv 316,58 kg, distillat 1598,90 kg, toluen 1282,32 kg, yo‘qotish 0,158 kg. Energetika: 1 kg suv 2,2568 MJ = 0,6269 kWh; Model A 651,3 MJ (180,9 kWh); Model B 1244,2 MJ (345,6 kWh). Barchasi ochiq shartli model; tajriba ma’lumoti emas.
- Modelda topilgan xato tuzatildi: (1) `evaporation_energy` da MJ hisobi 1000 barobar xato edi (n[kmol]·ΔvapH[kJ/mol] → MJ to‘g‘ri koeffitsiyatsiz); (2) Karl Fischer hisobida V birligi (mL/L) chalkashtirilgan edi; (3) vakuum grafigi CSV’dagi lgP ustuni ishlatilmagandi — egri chiziq koordinatadan chetga chiqqan; (4) adsorbsiya izotermasida C = 50 juda tekis egri chiziq bergani uchun C = 10 ga o‘zgartirildi; (5) faza ajratish modelidagi toluen yo‘qotishi 0,0015 kg emas, 0,158 kg ekani aniqlanib matn va jadvalga tarqatildi.
- `check_05_03.py` PASS: model nuqtalari (namlik asoslari, quruq qoldig‘, higroskopiklik sinflari, Karl Fischer, ΔvapH, p_sat, vakuum qaynash haroratları, muvozanat namligi, kinetika, quritgich sig‘imlari, sital massasi, gidrat balansi, azeotrop balansi, energiya), CSV qator sonlari, matndagi barcha asosiy raqamlar, Word matematiği (43 OMML/10 kasr/23 pastki/3 yuqori), 11 jadval sarlavhasi, 11 formula raqami (5.3.1)…(5.3.11), 17 rasm, 22 yon lavha, TNR/Cambria Math shriftlari, xavfsizlik chegarasi matni.
- Sahifalash: dastlabki render 12 sahifa bo‘ldi — 1-bo‘limning yon ustunidagi ikkinchi yon lavha ikkinchi sahifaga oqqan. Tuzatishlar: matn 10,5 → 10 pt, qator oralig‘i 1,05 → 1,03, chekkalar 1,6/1,5 → 1,5/1,4, jadval qatorlari 10 → 8 (ikki qator birlashtirildi), 1-bo‘lim matni qisqartirildi, yon ustunidagi qo‘shimcha rasm 3,92 → 3,30 sm qilib kichiklashtirildi → 11 sahifa, bo‘sh sahifa yo‘q.
- Native Google Docs→DOCX roundtrip 1841545 bayt: 43 OMML qatori, 10 kasr, 23 pastki, 3 yuqori, 17 rasm saqlangan. Yakuniy Google PDF 1282113 bayt, 11 sahifa. Sahifalar 1, 6 ko‘z bilan tekshirildi.
- Xavfsizlik: quritish rejasi, texnologik parametrlar, konsentratsiya tanlash, idish materiali va saqlash bo‘yicha amaliyot tavsiyalari berilmadi; faqat tamoyillar, modellarning ko‘rsatkichlari va chegara qiymatlari.
- QA paytida yuklangan 5 ta oraliq native Docs muxlatga solindi; foydalanuvchiga faqat quyidagi yakuniy havolalar beriladi.
- Yakuniy DOCX: https://drive.google.com/uc?id=1fqhK2bmFs__p-VRR2WOPf5aqgCX_8SVa&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/14rzFw0NBRL00rpcB2w-J_n2Id56wGXykiKi3dKhLbjw/edit
- Ikkala yakuniy nusxa reader/discovery=false. Manbalar, model va render QA `matn/05_03_rasm_manbasi.md` da.
- Keyingi mavzu: 5.4 — Sanoat prinsiplari.

## 5.4 — Sanoat prinsiplari (2026-10-23)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-5.4-Sanoat-prinsiplari.docx`; 998413 bayt; 11 sahifa (har bir bo‘lim aynan bitta sahifada).
- 11 bo‘lim: sanoat ishlab chiqarish maqsadi va sxema turlari; texnologik sxema va apparatlar (oqim modeli, OEE); mass va materiallar balansi; energiya balansi va issiqlik integratsiyasi; materiallar, korroziya va apparat tanlash; xavfsizlik (inertlash, yonishdan himoya, monitoring); ekologiya (chiqindilar, chiqindi suyuqlari, resurs samaradorligi); sifat boshqaruvi, standartlar va izchillik; raqamli boshqaruv (DCS, soft sensor, raqamli egizin, PI); iqtisodiyot, xom ashyo va logistika; ishlangan hisob (zanjir mass balansi va FOA).
- A4 13,5:4,5 cm, ko‘k/bronza ramkalar. 11 jadval, 11 raqamlangan Equation guruh (46 native OMML qatori, 10 kasr, 92 pastki, 2 yuqori), 5 hisobiy grafik + 5 CSV, 7 sxema, 5 original illyustratsiya, 22 yon lavha, 8 ta adabiyot 11-bo‘lim yon ustunda. TNR matn (10 pt), Cambria Math Equation, DejaVu Serif raster. Bob kirish rasmi alohida (5-bob).
- Markaziy g‘oya: sanoat prinsiplari — sxemadan boshqaruvgacha uzluksiz zanjir; sxema darajasi (to‘g‘ridan-to‘g‘ri → oraliq → qaytma) modda oqimini, unum darajasini, OEE ni, ekologik yukni va FOA ni bir vaqtda belgilaydi. Barcha ko‘rsatkichlar ochiq shartli modelga bog‘langan: 1000,0 kg 68 % li HNO₃ zanjiri.
- Model qiymatlari: kirish HNO₃ 680,00 kg (n = 10,7919 kmol) + suv 320,00 kg; NH₃ 183,80 kg, O₂ 690,68 kg, N₂ 2596,97 kg (N₂/O₂ = 3,76); suv hosil 194,42 + tashqari 222,79 = kiruvchi 417,21 kg, bog‘langan 97,21 kg; NO 323,87 kg, NO₂ 496,54 kg; chiqish eritma 1000,00 kg → konsentratsiya: suv chiqariladi 306,12 kg, mahsulot 693,88 kg (suv 13,88 kg), distillat 1546,07 kg, toluen 1239,95 kg. ΔfH° = −414,03 kJ/mol → −4468,2 MJ (≈ −4,47 GJ); bug‘latish 690,9 MJ (suv) + 512,2 MJ (toluen) = 1203,1 MJ; qatnoq bug‘ 0,10–8,00 MPa → 99,63–295,06 °C, h_fg 2257,5 → 1441,0 kJ/kg. Korroziya modeli 0,0012 g/(m²·soat); Cpk modeli 1,39. Iqtisodiyot: CAPEX 120,0 mln USD, FOA 8 % = 9,60 mln USD/y = 96 USD/t, o‘zgaruvchi 324 USD/t, jami 420 USD/t; OEE = 0,92 × 0,95 × 0,99 = 0,8653 → 86 526 t/y; narx (model) 560 USD/t → marja 140 USD/t; yillik foyda 12,11 mln USD; qaytish 9,9 yil; c(V): 50 000 → 516, 100 000 → 420, 200 000 → 372 USD/t; OPEX 42/26/8/9/5/6/4 %.
- Modelda topilgan xato tuzatildi: (1) zanjir massalarida 1000 barobar xato (m[kg] = n[kmol]·M[g/mol]/1000 emas, n[kmol]·M) — NH₃ 0,1838 kg emas, 183,80 kg bo‘ldi; (2) n(HNO₃) kmolga o‘tkazildi (10,7919 kmol); (3) reaksion issig‘i birligi: −4468,2 MJ, «GJ» emas (≈ −4,47 GJ) — matn, jadval, yon lavha, grafik va formulalar birga tuzatildi; (4) `birlikqiymat.png` egri chizig‘i o‘q koordinatadan (0–250) tashqarida edi, 0–250000 ga to‘g‘rilandi; (5) `issiqlik.png` da yorliq va bug‘ yorliqlari to‘qnashdi — 2 ustunli yorliq va navbatlashgan yorliq offsetlari qo‘llandi; (6) `oqim.png` da bar ustunidagi yorliq ustiga tushdi — «HNO₃ (68 %)» ga qisqartirilib, canvas 1180 → 880 px qilindi.
- `check_05_04.py` PASS: model nuqtalari (zanjir balansi, energiya, bug‘ jadvali, FOA, OEE, birlik narx), 5 CSV qator sonlari va OPEX yig‘indisi 100 %, matndagi barcha asosiy raqamlar va atamalar (ISO 22400, ISO 9001/14001/45001, Ph. Eur. 2.2.32/5.11, Ostwald, eksergiya/exergy, Ramshaw), Word matematiği (46 OMML/10 kasr/92 pastki/2 yuqori), 11 jadval sarlavhasi, 11 formula raqami (5.4.1)…(5.4.11), 17 rasm, 22 yon lavha, TNR/Cambria Math shriftlari, xavfsizlik chegarasi matni («amaliyot tavsiyalari berilmaydi»).
- Sahifalash: birinchi render 11 sahifa — har bir bo‘lim aynan bitta sahifada, bo‘sh sahifa yo‘q. Sahifalar 1, 4 va 11 ko‘z bilan tekshirildi (sarlavha, yon ustundagi sxema va grafiklar, jadval, formulalar, adabiyotlar bloki).
- Xavfsizlik: qurilma, apparat parametrlari, xom ashyo nisbatlari, mahsulot narxi va amaliy tayyorlash bo‘yicha amaliyot tavsiyalari berilmadi; ekologiya, sifat va raqamli boshqaruv faqat tamoyil va standartlar tili darajasida.
- Yakuniy DOCX: https://drive.google.com/uc?id=1YgTcvKvWpu0KAfK5a7Rge5SyI8Drz0VD&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1apQpCNVwh83kPhvSzjYufL60xzjsjL0YRYCi4MQQgAA/edit
- Ikkala yakuniy nusxa reader/discovery=false. Google PDF (11 sahifa) `google_drive/5.4 qoralamalar/5.4 final.pdf` da. Manbalar, model va render QA `matn/05_04_rasm_manbasi.md` da.
- Keyingi mavzu: 5.5 — Kislotalarni saqlash, logistika va xavfsizlik (mundarija bo‘yicha tekshiriladi).

## 6.1 — Guruhning umumiy tavsifi (2026-10-23)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-6.1-Guruhning-umumiy-tavsifi.docx`; 987775 bayt; 11 sahifa (har bir bo‘lim aynan bitta sahifada). III QISM (Alohida kislotalar), 6-bob «Vodorod galogenidlari»ning birinchi mavzusi.
- 11 bo‘lim: guruhning umumiy tavsifi va mavzu chegarasi; molekulyar tuzilish va fizik xossalar; bog‘ kuchi va kislotalik (suvda va DMSO da); gidratatsiya va eritmada spetsiatsiya; termik barqarorlik; sanoat va laboratoriya olish usullari; kislota xossalari (metallar, oksidlar, tuzlar); redoks xossalari va qaytaruvchi xarakter; materiallar, idish va korroziya; xavfsizlik, ekologiya va logistika; sifat, saqlash va ishlangan hisob.
- A4 13,5:4,5 cm, ko‘k/bronza ramkalar. 11 jadval, 11 raqamlangan Equation guruh (45 native OMML qatori, 12 kasr, 121 pastki, 28 yuqori), 5 hisoblangan grafik + 6 CSV, 7 sxema, 5 original illyustratsiya, 22 yon lavha, 11-bo‘limda 7 ta adabiyot bloki. TNR matn (10 pt), Cambria Math Equation, DejaVu Serif raster.
- Markaziy g‘oya: guruh bitta tuzilma oilasi bo‘lib, beshta ko‘rsatkich bir-biriga teskari bog‘lanadi — elektronegativlik va kislotalik pastdan yuqoriga kuchayadi, bog‘ energiyasi va termik barqarorlik susayadi, qaytaruvchilik kuchayadi. Kislotalik bitta omilga emas, ikki omilga bog‘liq: H–X bog‘ quyuqligi va konjugat asosning gidratatsiyasi (D + ΔH_hyd: 63 / 68 / 35 / 2 kJ/mol). Suv kuchli kislotalarni tekislaydi (leveling effect) — farq faqat DMSO da ochiladi.
- Model qiymatlari: M(HX) 20,006 / 36,461 / 80,912 / 127,912 g/mol; D(H–X) 569 / 432 / 370 / 295 kJ/mol; ΔH_hyd(X⁻) −506 / −364 / −335 / −293; r(H–X) 0,917 / 1,2746 / 1,414 / 1,609 Å (radiuslar yig‘indisi 0,88 / 1,33 / 1,51 / 1,70); μ 1,82 / 1,08 / 0,82 / 0,44 D; Tm −83,6 / −114,2 / −86,9 / −50,8 °C; Tb 19,5 / −85,1 / −66,8 / −35,4 °C; pK_a (suv) 3,17 / −5,9 / −8,8 / −9,5, (DMSO) 15 / −2,0 / −6,8 / −10,9; ΔG°(HX(g) → H⁺+X⁻) −3,4 / −35,9 / −49,4 / −53,3 kJ/mol (K 3,94 / 1,95×10⁶ / 4,50×10⁸ / 2,15×10⁹); 2HX ⇌ H₂+X₂ dekompozitsiyasi ΔG° 550,8 / 190,6 / 110,0 / 15,9 kJ/mol (lgK −96,50 / −33,39 / −19,27 / −2,79); HF muvozanati 0,010 M → 22,90 % (pH 2,640), 0,100 M → 7,91 % (2,102), 1,000 M → 2,57 % (1,589); azeotrop HF 37 % / 120 °C, HCl 20,2 % / 108,6 °C, HBr 47,6 % / 124,3 °C, HI 56,9 % / 127 °C; HCl 1000 kg 10 % → qoldiq 495,0 kg (suv 505,0 kg), 37 % uchun 1831,7 kg kerak (> 1000 kg, imkonsiz), yotqizish −74,8 kJ/mol (−2052 kJ/kg); 1 kg SiO₂ uchun HF 1997,9 g (48 % da 4162,4 g), H₂SiF₆ 2398,3 g, H₂O 599,6 g; neytralizatsiya 1000 kg 10 % HCl → CaCO₃ 137,3 kg, CaCl₂ 152,2 kg, CO₂ 60,4 kg, H₂O 24,7 kg (kirish 237,3 = chiqish 237,2 kg); redoks 1 kg HBr → 987,5 g Br₂, 1 kg HI → 992,1 g I₂ (62,54 g O₂); olish modeli 1000 kg fluorit (97 %, unum 90 %) → HF 447,4 kg, H₂SO₄ 1218,6 kg, CaSO₄ 1691,4 kg. Barchasi ochiq shartli model; tajriba ma’lumoti emas.
- Modelda topilgan xatolar tuzatildi: (1) neytralizatsiyada CaCl₂ va H₂O miqdori CaCO₃ moli bo‘yicha hisoblash kerak edi (kirish 237,3 kg ≠ chiqish 414,1 kg xatosi) — tuzatildi; (2) `oxidising_balance` funksiyasida shartli ifoda faqat else tarmog‘iga qo‘llanib, HF uchun −754,6 o‘rniga 79,4 chiqardi — qavslab yozildi; (3) olish modelida g→kg konversiyasi (1000 barobar) tuzatildi; (4) HCl yotqizish entalpisi kg/ga o‘tkazilganda 1000 ga ko‘paytirildi (−2 o‘rniga −2052 kJ/kg); (5) grafiklarda manfiy ustunlar `min/max` bilan chizilmagani uchun ko‘rinmas edi — barcha grafiklar qayta chizildi; (6) `fizik.png` da o‘ng panel chap panelga ustma-ust tushdi — ikkita ustki panelli ko‘rinishga o‘tkazildi; (7) `termik.png` da kislota nomlari ikki marta chiqqan, yorliq matn o‘ng chetdan kesilgan — tuzatildi.
- `check_06_01.py` PASS: model nuqtalari (molekulyar o‘lchamlar, kislotalik, gidratatsiya balansi, termik dekompozitsiya, HF muvozanati 5 nuqta, shisha modeli, neytralizatsiya mass balansi, redoks, azeotrop, yotqizish issig‘i, olish modeli), 6 CSV qator sonlari, 17 PNG, matndagi barcha asosiy raqamlar va atamalar (OpenStax, ChemGuide, Ph. Eur., leveling effect, gipokalsemiya, kalsiy glyukonat, OSHA TWA/IDLH), Word matematiği (45 OMML/12 kasr/121 pastki/28 yuqori), 11 jadval sarlavhasi, 11 formula raqami (6.1.1)…(6.1.11), 17 rasm, 22 yon lavha, TNR/Cambria Math shriftlari, xavfsizlik chegarasi matni.
- Sahifalash: dastlabki render 12 sahifa bo‘ldi — 11-bo‘lim yon ustundagi adabiyotlar va yopuvchi izoh 12-sahifaga oqqan. Tuzatishlar: 11-bo‘lim matni qisqartirildi (sifat/azeotrop/model paragraflari), adabiyotlar ro‘yxati 8 → 7 qisqartirilgan qilib yozildi, yopuvchi izoh 3 qatorga tushirildi → 11 sahifa, bo‘sh sahifa yo‘q. Sahifalar 1, 5 va 11 ko‘z bilan tekshirildi.
- Native Google Docs→DOCX roundtrip 1930336 bayt: 45 OMML qatori, 12 kasr, 121 pastki, 28 yuqori, 17 rasm saqlangan. Yakuniy Google PDF 1 394 441 bayt, 11 sahifa. PDF `google_drive/6.1 qoralamalar/6.1 final.pdf` da.
- Xavfsizlik: HF uchun tizimli toksiklik va chegaralar (OSHA TWA 3 ppm, IDLH 30 ppm) manbaga asosida keltirilgan; olish usullari va materiallar faqat sxematik tarzda; konsentratsiya, idish tanlash, saqlash va amaliy tayyorlash bo‘yicha amaliyot tavsiyalari berilmaydi.
- QA paytida yuklangan 3 ta oraliq native Docs va 3 ta oraliq DOCX muxlatga solindi; foydalanuvchiga faqat quyidagi yakuniy havolalar beriladi.
- Yakuniy DOCX: https://drive.google.com/uc?id=1rlHTOfIq3R3lspPglH4K5v-zaxrRRaFp&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1PT_X45Tw_cwl5VQnDFM0El62SrY7Nlzgls4gA0N5Y_E/edit
- Ikkala yakuniy nusxa reader/discovery=false. Manbalar, model va render QA `matn/06_01_rasm_manbasi.md` da.
- Keyingi mavzu: 6.2 — HF, ftorid kislota.

## 6.2 — HF, ftorid kislota (2026-10-23)
- Alohida DOCX: `chiqish/Noorganik-kislotalar-6.2-HF-florid-kislota.docx`; 958 892 bayt; 11 sahifa (har bir bo‘lim aynan bitta sahifada). 6-bobning ikkinchi mavzusi.
- 11 bo‘lim: molekulaning maxsusligi va vodorod bog‘i; anhidr HF erituvchi tizimi; HF asosidagi superkislotalar; suvli HF spetsiatsiyasi; ishlab chiqarish, tozalash va qayta foydalanish; shisha va keramikaga ta’sir (yemirish modeli); metallarga ta’sir (fluoridli passivatsiya); floridlar, komplekslar va qo‘llanish; sanoat sohalari; xavfsizlik, ekologiya va chiqindilar; sifat, tahlil va ishlangan hisob.
- A4 13,5:4,5 cm, ko‘k/bronza ramkalar. 11 jadval, 11 raqamlangan Equation guruh (46 native OMML qatori), 5 hisoblangan grafik + 6 CSV, 7 sxema, 5 original illyustratsiya (17 PNG), 22 yon lavha, 11-bo‘limda 6 ta adabiyot bloki. TNR matn (10 pt), Cambria Math Equation, DejaVu Serif raster.
- Markaziy g‘oya: HF boshqa galogenidlardan ikki tomonlama farqlanadi — suvda kuchsiz kislota (Ka = 6,8×10⁻⁴, ion juftlari [H₃O⁺·F⁻]), quruq holda kuchli kislota va kuchli erituvchi; vodorod bog‘i tufayli qaynash harorati 19,5 °C (guruhda eng yuqori). Anhidr HF o‘z-o‘zini ionlashadi (3HF ⇌ H₂F⁺ + HF₂⁻, K_self = 2×10⁻¹²) va kuchsiz, kichik F⁻ ioni bilan kuchli bog‘lanadi — shuning uchun HF + SbF₅ superkislota beradi (H₀ = −15,1 → −21 → < −28).
- Model qiymatlari: speksiatsiya modeli 0,010 M → HF 76,0 % / F⁻ 22,3 % / HF₂⁻ 0,8 % (pH 2,635), 1,000 M → 89,5 / 1,1 / 4,7 % (1,238), 10,000 M → HF₂⁻ 5,2 % (0,277); yemirish r = 510[F⁻] + 610[HF] + 2890[HF₂⁻] Å/min → 1,000 M: 687,8; 4,000 M: 2778,7; 8,000 M: 5567,7 Å/min; 1 kg SiO₂ → HF 1997,8 g (48 % da 4162,1 g), H₂SiF₆ 2398,2 g, H₂O 599,6 g; passivatsiya 1 g Al → 3,113 g AlF₃, Fe → 2,326 g FeF₃, Ni → 1,647 g NiF₂, Cu → 1,598 g CuF₂; chiqindi 1000 kg 10 % HF → Ca(OH)₂ 185,2 kg, CaF₂ 195,1 kg, H₂O 90,0 kg (kirish 285,2 = chiqish 285,2 kg); qoldiq F⁻: Ca²⁺ 0,001 M → 3,752 mg/L, 0,010 M → 1,186 mg/L, 0,100 M → 0,375 mg/L (K_sp = 3,9×10⁻¹¹); kaltsiy 20 g HF → 0,500 mol Ca²⁺ → 224,1 g glyukonat, 100 g HF → 2,499 mol → 1120,6 g; olish 1000 kg fluorit (97 %, unum 92 %) → HF 457,3 kg, H₂SO₄ 1218,5 kg, CaSO₄ 1691,4 kg. Barchasi ochiq shartli model; tajriba ma’lumoti emas.
- Modelda topilgan xatolar tuzatildi: (1) chiqindi modelida CaF₂ stöchiometriya noto‘g‘ri hisoblangan (n(HF) emas n(CaF₂) = n(HF)/2) — kirish 285,2 kg ≠ chiqish 480,3 kg xatosi tuzatildi; (2) g→kg konversiyasi (Ca(OH)₂ 185 176,9 kg → 185,2 kg) tuzatildi; (3) grafiklarda teg takrorlanishi va yon ustun bilan ustma-ust tushishi tuzatildi (grafiklar qayta chizildi, chiqindi grafigi ikki ustki panelli qilindi); (4) `Selekтивlik` yozuvida kirill harflar aralashgan — barcha 6.2 fayllarida `Selektivlik` ga tuzatildi; (5) butun kitob bo‘yicha kirill qoldiqlari tekshirildi — `dizayn.md`, 4.4 jadval/generator/draw fayllaridagi «Fazа» va «bронза» xatolari tuzatildi (build_01_01.py, build_docx.py, build_mundarija_docx.py dagi kirill atamalar ataylab qoldirildi).
- `check_06_02.py` PASS: model nuqtalari (spetsiatsiya 8 konsentratsiya, yemirish tezligi, passivatsiya 4 metall, chiqindi mass balansi, qoldiq fluorid 5 nuqta, kaltsiy talabi, olish va shisha modellari, anhidr HF konstantalari), 6 CSV qator sonlari, 17 PNG, matndagi barcha asosiy raqamlar va atamalar (WHO 1,5 mg/L, AQSh 4,0 mg/L, OSHA 3 ppm, IDLH 30 ppm, kalsiy glyukonat, gipokalsemiya, Na₃AlF₆, H₂SiF₆), Word matematiği (46 OMML qatori), 11 jadval sarlavhasi, 11 formula raqami (6.2.1)…(6.2.11), 17 rasm, 22 yon lavha, TNR/Cambria Math shriftlari, xavfsizlik chegarasi matni.
- Sahifalash: dastlabki render 13 sahifa bo‘ldi (7- va 11-bo‘limlar yon ustuni to‘shdi) → 7-bo‘limdan ikkinchi rasm (grafik) 8-bo‘limga ko‘chirildi; 11-bo‘limda adabiyotlar 8 → 6 qisqartirildi va 7 pt qilindi, jadval 11 → 9 qator; kalsiy grafigi 3-bo‘limga ko‘chirildi → 11 sahifa, bo‘sh sahifa yo‘q. Sahifalar 1, 6 va 11 ko‘z bilan tekshirildi.
- Xavfsizlik: HF ning tizimli toksikligi (Ca²⁺/Mg²⁺, gipokalsemiya), chegaralar (OSHA 3 ppm, ACGIH 0,5 ppm (F), TLV-C 2 ppm, IDLH 30 ppm) va kalsiy glyukonat manbaga asosida keltirilgan; davolash dozalari va amaliyot tavsiyalari berilmadi; tibbiy yordam — shifokor qarori bilan.
- Manbalar, model va render QA `matn/06_02_rasm_manbasi.md` da. PDF: `google_drive/6.2 qoralamalar/6.2 final.pdf` (1 358 786 B, 11 sahifa).
- Yakuniy DOCX: https://drive.google.com/uc?id=1fSrPnvKLpSbEyJ0Ddhl7DH9u3rxB24bD&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1G2kYZd1m26cKCou4EIECkNVDdI2vYpIOeucfJmnx5DQ/edit
- Ikkala yakuniy nusxa reader/discovery=false. Keyingi mavzu: 6.3 — HCl, xlorid kislota.

## Terminologiya tuzatuvi: «hydrogen bog‘i» → «vodorod bog‘i» (2026-10-23)
- Foydalanuvchi izohi bo‘yicha yarim tarjima qilingan «hydrogen bog‘i» atamasi kitob bo‘ylab to‘liq o‘zbekchaga o‘tkazildi: **vodorod bog‘i** (vodorod bog‘lanishi, vodorod bog‘langan).
- Almashgan 20 ta joy: `matn/06_02.md` (4), `matn/06_02_jadvallar.json` (1), `matn/06_02_rasm_manbasi.md` (4), `matn/06_01_rasm_manbasi.md` (1), `qurilma/content_06_02.py` (1), `qurilma/equations_06_02.py` (1), `qurilma/draw_06_02.py` (1), `qurilma/build_06_02_sidebar.py` (3), `qurilma/build_06_01_sidebar.py` (1), `qurilma/check_06_02.py` (1), `dizayn.md` (2).
- Atama nomi, bibliografik sarlavhalar («Wikipedia — Hydrogen fluoride», «Definition of the hydrogen bond (IUPAC)») va 2.4-bo‘limdagi nomlash qoidalari (hydrogen chloride, hydrogenphosphate, dihydrogenphosphate) o‘zgartirilmadi — ular inglizcha rasmiy nomlar va manba sarlavhalari.
- 6.1 va 6.2 hujjatlari qayta qurildi, `check_06_01.py` va `check_06_02.py` PASS (11 sahifa saqlanadi, Google PDF’lar qayta eksport qilinib tekshirildi: 6.1 — 1 394 441 B, 6.2 — 1 358 786 B, ikkalasi 11 sahifa).
- Yangilangan Drive havolalari:
  - 6.1 Google Docs: https://docs.google.com/document/d/1PT_X45Tw_cwl5VQnDFM0El62SrY7Nlzgls4gA0N5Y_E/edit ; DOCX: https://drive.google.com/uc?id=1rlHTOfIq3R3lspPglH4K5v-zaxrRRaFp&export=download
  - 6.2 Google Docs: https://docs.google.com/document/d/1G2kYZd1m26cKCou4EIECkNVDdI2vYpIOeucfJmnx5DQ/edit ; DOCX: https://drive.google.com/uc?id=1fSrPnvKLpSbEyJ0Ddhl7DH9u3rxB24bD&export=download
  - Eski (muxlatga solingan) nusxalar: 1MkYjXOpbSIXM_D64UzQjZULXjdxQHcXAof5ckT6lPxs, 17T_Tq_DJexBIxnphYJvM_MkIFdNv3QEj, 1F2ru0JIcN-JfPg25n4D-FQte931ZPSVj0mYKi6u2my0, 13xSUPEFnN6r9RPSxMHNSHmPTwOnvtcdJ.

### 6-bob kirish vizuali (2026-10-23)
- `rasmlar/6-bob-kirish-sarlavhali.png` (1664×2496, A4 150 dpi): 5-bob vizuali uslubiy referens sifatida ishlatilib yaratilgan 6-bob kirish rasmi. Alohida saqlanadi, mavzu DOCXlariga kiritilmaydi.
- Kompozitsiya: yuqorida «III QISM · ALOHIDA KISLOTALAR» (bronza, letter-spacing 7,5 px), ostida ingichka qo‘ng‘iroq chizig‘i va olmos; «6-BOB»; katta to‘q ko‘k sarlavha «Vodorod / galogenidlari» (Playfair Display 168 px, ikki qator, 196 px qator oralig‘i, oq soya konturi); chiziq + olmos; «BOB MAVZULARI»; 6 ta mavzu (6.1 Guruhning umumiy tavsifi, 6.2 HF — ftorid kislota, 6.3 HCl — xlorid kislota, 6.4 HBr — bromid kislota, 6.5 HI — yodid kislota, 6.6 Taqqoslash) — raqamlar bronza, nomlar to‘q ko‘k, har biri ostida ingichka qo‘ng‘iroq chizig‘i.
- Fon: `rasmlar/6-bob-fon.png` — AI konsept-art: bronza armaturali to‘rtta shisha idishda galogenlarga xos ranglar (F — yashil, Cl — sariq-yashil, Br — amber, I — binafsha), oltin kristallar to‘plami, krem/navy/bronza palitra, oltin nur va bokeh. AI rasmga matn joylanmagan: barcha yozuvlar dasturiy tipografiya bilan qo‘shilgan, shuning uchun o‘zbekcha imlo aniq.
- Fon kadrga solindi va kattalashtirildi (chapdan 114 px kesilgan, 910×1365 → 1664×2496, proporziya saqlangan) — idishlar o‘ng pastki burchakka surilib, sarlavha va mavzular ro‘yxati toza krem maydonda qoldi; yuqoriga krem parda (640 px to‘liq, 1150 px gacha yumshoq tushish), mavzular ro‘yxati zonasi uchun yumshoq krem dog‘ (GaussianBlur 105 px, alpha 132) qo‘llandi.
- Shriftlar: `rasmlar/shriftlar/` — Playfair Display 500 (sarlavha) va Libre Baskerville 400 (qism, bob raqami, mavzular) latin TTF; SIL OFL 1.1.
- Generator: `qurilma/kirish_6_bob.py` (Pillow; deterministik, qayta ishga tushirilsa bir xil natija).
- QA: birinchi urinishda fonning yuqori chizig‘i vertik cho‘zildi (tik chiziqli artefaktlar), idishlar kadrga chegarasiz yopishtirildi va mavzular ro‘yxati to‘q fonda o‘qilmas edi — fon qayta generatsiya qilindi (yuqori chap bo‘sh, idishlar pastki o‘ngda), idishlar guruhi alohida qirqim bilan yumshoq qo‘shildi va ro‘yxat uchun krem dog‘ qo‘llandi.
- AI konsept-art; tajribaviy foto yoki mexanizmning ilmiy dalili emas.
- Yakuniy fayl: https://drive.google.com/uc?id=1jdpAZh6JtumM_-3Z6sMFD9PyKlSkLIIQ&export=download (reader, allow_file_discovery=false).

### 6.3 — HCl, xlorid kislota (2026-10-23)
- Mavzu hujjati: `kitob/chiqish/Noorganik-kislotalar-6.3-HCl-xlorid-kislota.docx` (995 365 B) — 11 sahifa, har bir bo‘lim bitta sahifada.
- Tuzilma: 11 bo‘lim / 11 jadval (3 ustun, 10–11 qator) / 22 yon lavha / 5 hisoblangan grafik + 7 sxema + 5 original illyustratsiya (jami 17 PNG) / 11 ta native OMML formula guruhi (50 qator, Cambria Math) / 6 ta manba.
- Layout: A4, asosiy matn 13,5 sm + vizual yon ustun 4,5 sm; matn 10 pt Times New Roman (qator oralig‘i 1,03), jadval 8 pt; to‘q ko‘k `#0B2C4A` / bronza `#B37C2D` ramkalar; sarlavha «6-BOB / VODOROD GALOGENIDLARI» bandi bilan.
- Generatorlar: `qurilma/prep_06_03.py` (model + 6 CSV), `content_06_03.py` (11 jadval, 22 yon lavha → JSON), `equations_06_03.py` (11 formula guruhi), `draw_06_03.py` (17 PNG), `build_06_03_sidebar.py` (DOCX), `check_06_03.py` (QA — PASS).
- `qurilma/book_equations.py` ga `'6.3'` varianti qo‘shildi (native formula dispetcheri).
- Asosiy model natijalari: Mannheim 1000 kg HCl → NaCl 1602,8 / H₂SO₄ 1345,0 / Na₂SO₄ 1947,8 kg (ΔrH +884,8 MJ); sintetik → H₂ 27,6 / Cl₂ 972,4 kg (−2531,7 MJ); spetsiatsiya 0,1 M → pH 1,000, 12 M → pH −1,079 va HCl₂⁻ 0,09 %; metall: 1 g Fe → 2,270 g FeCl₂ / 1,306 g HCl, 1 g Al → 4,054 g HCl, 1 g Cu → 1,148 g HCl + 0,252 g O₂; neytralizatsiya Na₂CO₃ 145,3 kg (kirish = chiqish 245,3 kg), Ca(OH)₂ 101,6 kg (201,6 kg); tiklash 1000 kg FeCl₂ → Fe₂O₃ 629,9 / HCl 575,3 kg; standartlash 0,2500 g Na₂CO₃ va 24,85 mL → 0,18984 mol/L.
- Manbalar, model va render QA `matn/06_03_rasm_manbasi.md` da (Wikipedia — Hydrochloric acid va uning fizik jadvali; Air Liquide/Messer/Cheméo/NOAA — kritik nuqta; OSHA va NIOSH (IDLH 2025-yilda 45 ppm) — chegaralar; JACS va adabiyotlar — xloroaluminat H₀; Journal of Cleaner Production va patentlar — spray roasting va pickling koeffitsiyentlari).
- PDF: `google_drive/6.3 qoralamalar/6.3 final.pdf` (1 399 917 B, 11 sahifa, 1 sahifa/bo‘lim).
- Yakuniy DOCX: https://drive.google.com/uc?id=1Gg35Vm5gX1QAdjZU-UQac73u4TTKiKPE&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1NyH_8laOkKMMCeEoHvuh_8DHYzbO_vY1FhA6C6XnZrk/edit
- Ikkala yakuniy nusxa reader/discovery=false. Keyingi mavzu: 6.4 — HBr, bromid kislota.

### 6.4 — HBr, bromid kislota (2026-10-23)
- Mavzu hujjati: `kitob/chiqish/Noorganik-kislotalar-6.4-HBr-bromid-kislota.docx` (981 324 B) — 11 sahifa, har bir bo‘lim bitta sahifada.
- Tuzilma: 11 bo‘lim / 11 jadval (3 ustun) / 22 yon lavha / 5 hisoblangan grafik + 7 sxema + 5 original illyustratsiya (jami 17 PNG) / 11 ta native OMML formula guruhi (61 qator, Cambria Math) / 4 manba + to‘liq ro‘yxat `matn/06_04_rasm_manbasi.md` da.
- Layout: A4, asosiy matn 13,5 sm + vizual yon ustun 4,5 sm; matn 10 pt TNR (qator oralig‘i 1,03), jadval 8 pt; to‘q ko‘k `#0B2C4A` / bronza `#B37C2D`; sarlavha «6-BOB / VODOROD GALOGENIDLARI» bandi bilan.
- Generatorlar: `qurilma/prep_06_04.py` (model + 8 CSV), `content_06_04.py` (11 jadval, 22 yon lavha → JSON), `equations_06_04.py` (11 formula guruhi), `draw_06_04.py` (17 PNG), `build_06_04_sidebar.py` (DOCX; panel va qo‘shimcha rasm kengligi ixtiyoriy parametr sifatida), `check_06_04.py` (QA — PASS; ichki jadvallar matni ham tekshiriladi).
- `qurilma/book_equations.py` ga `'6.4'` varianti qo‘shildi.
- Asosiy model natijalari: sintetik 1000 kg HBr → H₂ 12,46 kg, Br₂ 987,5 kg (ΔrH −639,5 MJ); laboratoriya usuli → Br₂ 987,5 kg, SO₂ 395,9 kg, H₂SO₄ 606,1 kg; bromin sikli 1000 kg NaBr + Cl₂ 344,6 kg → Br₂ 776,6 + NaCl 568,0 kg; spetsiatsiya 0,1 M → pH 1,000, 8,770 M → pH −0,943, 12 M → pH −1,079 (HBr₂⁻ 0,0001 %); tribromid 0,10 M → 60,40 %, 8,77 M → 99,29 %; metall: 1 g Fe → FeBr₂ 3,862 g / HBr 2,898 g, 1 g Al → 9,884 g AlBr₃ / 8,996 g HBr, 1 g Cu → HBr 2,547 g + O₂ 0,252 g; neytralizatsiya Na₂CO₃ 65,5 kg (kirish = chiqish 165,5 kg), Ca(OH)₂ 45,8 kg (145,8 kg); standartlash 0,2000 g Na₂CO₃ va 30,00 mL → 0,12580 mol/L.
- Manbalar: Wikipedia (Hydrobromic acid / Hydrogen bromide / Bromine — fizik ma’lumot, azeotrop, gidratlar, ishlab chiqarish, qo‘llanish), NOAA CAMEO va Wikidata/Cheméo-NIST (kritik nuqta, S°, IE), OSHA va NIOSH (3 ppm ceiling/TWA, ACGIH 2 ppm, IDLH 30→35 ppm, 2025), USGS (bromin ishlab chiqarishi ≈440 000 t/y), NOAA/UNEP (metilbromid ODP 0,6, BrO katalizatori).
- PDF: `google_drive/6.4 qoralamalar/6.4 final.pdf` (1 395 901 B, 11 sahifa).
- Yakuniy DOCX: https://drive.google.com/uc?id=1Rd0_6i3l0_7hlcNN9ZuTI1yXZkco5cPd&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1jbL2UpO601HOV-P9ST3PA7gBHGy4tVn91aAEI368x34/edit
- Ikkala yakuniy nusxa reader/discovery=false. Keyingi mavzu: 6.5 — HI, yodid kislota.

### 6.5 — HI, yodid kislota (2026-10-24)
- Mavzu hujjati: `kitob/chiqish/Noorganik-kislotalar-6.5-HI-yodid-kislota.docx` (949 633 B) — 11 sahifa, har bir bo‘lim bitta sahifada.
- Tuzilma: 11 bo‘lim / 11 jadval (3 ustun) / 22 yon lavha / 5 hisoblangan grafik + 7 sxema + 5 original illyustratsiya (jami 17 PNG) / 11 ta native OMML formula guruhi (66 qator, Cambria Math) / 4 manba + to‘liq ro‘yxat `matn/06_05_rasm_manbasi.md` da.
- Layout: A4, asosiy matn 13,5 sm + vizual yon ustun 4,5 sm; matn 10 pt TNR (qator oralig‘i 1,03), jadval 8 pt; to‘q ko‘k `#0B2C4A` / bronza `#B37C2D`; sarlavha «6-BOB / VODOROD GALOGENIDLARI» bandi bilan.
- Generatorlar: `qurilma/prep_06_05.py` (model + 8 CSV), `content_06_05.py` (11 jadval, 22 yon lavha → JSON), `equations_06_05.py` (11 formula guruhi), `draw_06_05.py` (17 PNG), `build_06_05_sidebar.py` (DOCX; panel va qo‘shimcha rasm kengligi ixtiyoriy parametr), `check_06_05.py` (QA — PASS; ichki jadvallar matni ham tekshiriladi).
- `qurilma/book_equations.py` ga `'6.5'` varianti qo‘shildi.
- Asosiy model natijalari: to‘g‘ridan-to‘g‘ri usul 1000 kg HI → H₂ 7,88 kg, I₂ 992,1 kg (ΔrH −9,44 kJ, K(298 K) = 0,254); gidrazin usuli → N₂H₄ 62,6 kg; fosfor usuli → P 80,7 kg, H₂O 140,8 kg, H₃PO₃ 213,7 kg; H₂S usuli → H₂S 133,2 kg, S 125,3 kg; yod sikli 1000 kg NaI + Cl₂ 236,5 kg → I₂ 846,6 + NaCl 389,9 kg (1236,5 = 1236,5); spetsiatsiya 0,1 M → pH 1,000, 7,560 M → pH −0,879, 12 M → pH −1,079 (HI₂⁻ 0,00002 %); triiodid 0,10 M → 98,54 %, 7,56 M → 99,98 %; metall: 1 g Fe → FeI₂ 5,545 g / HI 4,581 g, 1 g Al → AlI₃ 15,110 g / 14,222 g HI, 1 g Cu → HI 4,026 g + O₂ 0,252 g; neytralizatsiya Na₂CO₃ 41,4 kg (kirish = chiqish 141,4 kg), Ca(OH)₂ 29,0 kg (129,0 kg); yodometriya 1,000 g KIO₃ → I₂ 0,712 g, tiosulfat 0,887 g; standartlash 0,2000 g Na₂CO₃ va 30,00 mL → 0,12580 mol/L; yodlangan tuz 1 t + 30 g I → KI 39,2 g yoki KIO₃ 50,6 g.
- Manbalar: Wikipedia (Hydroiodic acid / Hydrogen iodide / Iodine compounds / Iodine — fizik ma’lumot, azeotrop 56,7 % / 126,7 °C / 7,56 mol/L, sintez usullari, Cativa jarayoni, DEA I ro‘yxati, jahon yod ishlab chiqarishi ≈30 000 t/y), ICSC 1326 (ILO/WHO: DANGER, TLV 0,01 ppm, teri absorbsiyasi), NIOSH IDLH 2025-109 (35 ppm / 183 mg/m³; AEGL 1 / 150 / 740 ppm), OSHA/NIOSH yod chegaralari (0,1 ppm; ACGIH 0,01 ppm; IDLH 2 ppm), Cheméo/NIST (r 1,609 Å, D 299 kJ/mol, μ 0,45 D, IE 10,39 eV), USGS/ATSDR (yod ishlab chiqarishi, radioyod).
- PDF: `google_drive/6.5 qoralamalar/6.5 final.pdf` (1 378 708 B, 11 sahifa).
- Yakuniy DOCX: https://drive.google.com/uc?id=1GrOUsrR2E4fFH6JFfcUgBMFaPmirx_uL&export=download
- Yakuniy Google Docs: https://docs.google.com/document/d/1PgL2upJnPfdKfqZWbrNxkomzPJmf69mfGWwFxbTnMhg/edit
- Ikkala yakuniy nusxa reader/discovery=false. Keyingi mavzu: 6.6 — Taqqoslash.
