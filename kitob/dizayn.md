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
  - **Grafiklar:** toza chiziqli, ko'k/bронза ranglarda, panjara och kulrang
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
