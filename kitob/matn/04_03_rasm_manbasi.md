# 4.3. Passivlanish — manbalar, taxminiy chegaralar va tasvirlar

## Tekshirilgan manbalar (2026-10-22)
1. IUPAC Gold Book, Passivation, https://goldbook.iupac.org/terms/view/P04443/plain , DOI 10.1351/goldbook.P04443. Joriy to‘liq plain matn o‘qildi: faol holatdan passiv parda bilan o‘tish; tashqi anod tok yoki qaytariluvchi oksidlovchi yordamida passivlanish. Ta’rif mustaqil qayta bayon qilingan.
2. John R. Scully, Katie Lutton, Polarization Behavior of Active Passive Metals and Alloys, ochiq bob qo‘lyozmasi: https://www.numis.northwestern.edu/MURI/Publications/Papers/Scully_IFCC.pdf . 0 va 1-chunk to‘liq o‘qildi: Pourbaix termodinamikasi bilan passiv kinetika farqi, oksid/gidroksid/adsorbat qatlamlari, Fe/Cr dagi murakkab sirt tarkibi, i_crit va i_pass, qaytariluvchi reagent tezligining roli, transpassiv Cr va kislorod ajralishi. Tayyor chizma, o‘lchangan tok/qalinlik sonlari yoki prose ko‘chirilmagan. Formal Cr₂O₃→Cr₂O₇²⁻ yarimreaksiyasi mustaqil atom/zaryad tekshiruvi bilan keltirilgan, manbadagi pH matnidagi noaniqlik takrorlanmagan.
3. IUPAC Gold Book, Pitting corrosion, https://goldbook.iupac.org/terms/view/P04679/plain , DOI 10.1351/goldbook.P04679. To‘liq matn o‘qildi: passiv metalldagi notekis chuqurchali korroziya, muayyan anionlar va kritik potensial. E_rp va tarixga bog‘liqlik umumiy korroziya nazariyasi sifatida bayon qilingan, bu ta’rifga ortiqcha da’vo yuklanmagan.
4. Gamry Instruments, Basics of Electrochemical Corrosion Measurements, https://www.gamry.com/application-notes/corrosion-coatings/basics-of-electrochemical-corrosion-measurements/ , 1-chunk to‘liq o‘qildi: Tafelning cheklovlari, massa transporti, sirt o‘zgarishi, R_p/Stern–Geary, Faraday qonuni va o‘rtacha erishdan mahalliy xavfni baholab bo‘lmasligi. Manbadagi tayyor tenglama rasmlari, jadvallar va o‘lchash protokoli ko‘chirilmagan. R_p ushbu matnda aniq maydon-normalangan Ω cm² ko‘rinishida qayta belgilangan.
5. Jones, D. A. Principles and Prevention of Corrosion, 2 ed., Prentice Hall 1996 — umumiy bibliografik tayanch, aniq sahifalar tekshirilmagan.

Izlanishda avval xato topilgan Gold Book P04440 aslida partition ratio bo‘lib chiqqan: bu mavzu dalili sifatida ishlatilmagan. OSU arxiv PDFiga to‘liq kirish 403 qaytargan, u to‘liq o‘qilgan manba yoki bevosita bibliografik dalil deb berilmagan. Qidiruvdagi tijorat saytlarining universal xavfsiz konsentratsiya/temperatura da’volari olinmagan.

## Asosiy ilmiy cheklovlar
- Immunlik termodinamik, passivlik kinetik sirt holati. Ochiq zanjirdagi barqaror metall oksidlanish shartli hisobi uchun i_a+i_c=0, ammo qisman toklar musbat moduli noldan farqli bo‘lishi mumkin.
- Real parda mutlaq sof Cr₂O₃ yoki bitta Fe oksidi deb olinmagan; gidratlanish, nuqson, tashqi/ichki qatlam va transport muhim. Zanglamas po‘latning hajmi emas, sirt holati nazarda tutilgan.
- Sovuq konsentrlangan HNO₃ misollari metall navi, harorat va sirt tarixisiz universal qilinmagan. Konsentrlangan H₂SO₄ dagi sekin erishning barcha mexanizmlari sof oksidli elektrokimyoviy passivlik bilan aynanlashtirilmagan. Tajriba/ishlov retsepti, kislota foizi yoki material tanlash jadvali yo‘q.
- Yuqori anod tok metall erishi, parda o‘sishi va O₂ ajralishining ayni biri emas. Cr(VI) xavfi aniq qayd etilgan.
- E_pit va E_rp tajriba sharoitlari hamda tarixga bog‘liq, universal material konstantalari emas. Chuqurchadagi gidroliz, ion ko‘chishi va ohmik tushuv tashqi muhitdan boshqa kimyo yaratishi mumkin.
- LPR/Stern–Geary faqat mos kichik-signal/kinetik shartlar bilan; oddiy Ω va maydon-normalangan Ω cm² ajratilgan.

## Original hisobiy grafiklar
`qurilma/passive_04_03.py`; rasmlar `qurilma/draw_04_03.py` orqali chizilgan. Tayyor tashqi tasvir yoki o‘lchov egri chizig‘i ishlatilmagan.

1. `qutblanish.png` + CSV, 501 nuqta. E_rel=E−E_ref, ixtiyoriy shartli etalon (SHE yoki SCE emas). i°=1 A/cm²; lg(i/i°) ning bo‘lakli taxminiy qiymati: E≤0.300 da −6+10E; 0.300…0.450 da 3−20E; 0.450…0.800 da −6; yuqorida −6+20(E−0.800). i_crit=10⁻³, i_pass=10⁻⁶ A/cm² shartli qiymatlar. Oxirgi ortish bir metallning aniq transpassiv kinetikasi deb berilmagan.
2. `aralash.png` + CSV, 501 nuqta. O‘sha anod egri chizig‘i; katod modulining sun’iy lg(|i_c|/i°) qiymatlari −3−10E va 1−10E. Kesishishlar E_rel=0.150 V / i=3.16227766×10⁻⁵ A/cm² va E_rel=0.700 V / i=10⁻⁶ A/cm². Real oksidlovchi faolligi bilan kalibrlanmagan yoki barcha potensialdagi haqiqiy transport tezligi deb olinmagan.
3. `qalinlik.png` + CSV, 301 nuqta (0…300 s). dL/dt=k_g(L_lim−L)−v_diss; L₀=0.500 nm, L_lim=4.00 nm, k_g=0.0200 s⁻¹. v_diss=0.0200/0.0600/0.0800 nm/s bilan limitlar 3/1/0 nm. Musbat limit himoya sifatini o‘zi tasdiqlamaydi. Atom ko‘lamidan kichik L da kontinuum yaqinlashuvi ekstrapolyatsiyasi real uzluksiz qatlam deb olinmagan.
4. `xlorid.png` + CSV, 301 nuqta; lg a(Cl⁻)=−3…0. E_pit,ref=0.650 V, E_rp,ref=0.350 V, a_ref=0.0100, qiyalik −0.0800 V/dekada. Mustaqil shartli etalon; 1–2 grafik etaloni bilan sonli birlashtirilmaydi. Materialning xavfsiz ishlash chegarasi, xizmat muddati yoki real o‘lchov emas.

Jami 1604 CSV satri. Grafiklardagi logarifmlar o‘lchamsiz i/i° yoki faollikka tegishli.

## Ishlangan hisoblar
Stern–Geary: b_a=b_c=0.120 V/dekada; B=0.0260576689142 V; R_p=26057.67 Ω cm² uchun i_corr≈9.99999958×10⁻⁷ A/cm². Bu uskunadan olingan qiymat emas.

Faraday: Al→Al³⁺, F=96485.33212 C/mol, M=26.9815385 g/mol, ρ=2.70 g/cm³. Berilgan metall erish tok komponenti 1.000 μA/cm², A=10.00 cm², t=86400 s. Q=0.8640 C; m=0.08053745494 mg; bir tekis h=0.02982868701 μm. f=0.001000 bo‘lsa faol maydon 0.01000 cm², mahalliy tok 1.000 mA/cm², o‘rtacha chuqurlik ekvivalenti 29.82868701 μm. Bu maksimal pit chuqurligi, real geometriya, o‘sish qonuni yoki xizmat muddati bashorati emas. Boshqa parda/O₂ toki metall erish komponentiga qo‘shilmagan, unga tegishli tok samaradorligi 100% berilgan.

## Sxemalar va rasmlar
- 5 original sxema: `holatlar`, `parda`, `yuqori`, `dalil`, `hisob`.
- 4 original jarayon kesimi: `kesim` (metall–parda–eritma); `tiklanish` (mos muhitda shikastning qoplanishi); `pit_kesim` (mahalliy muhit); `trans_kesim` (Cr(III) qatlamdan erigan Cr(VI) turiga formal yo‘l).
Rang va qalinliklar shartli; mikrofoto, masshtabli material kesimi yoki atom koordinatasi emas. Xavfli kislota ichidagi metallni tirnash tavsiyasi berilmagan. Word matni Times New Roman, native Equation Cambria Math, raster yozuv DejaVu Serif. Bob kirish rasmi mavzu DOCXiga qo‘shilmagan.

## QA
`check_04_03.py` PASS: 1604 ta shartli hisob satri, anod funksiya chegaralarida uzluksizlik, ikkita katod kesishishining yagonaligi, qalinlik ODE sini sonli differensial tekshirish, log-xlorid taxminiy hisobi, Stern va Faraday birlik-identiklari, 8 ta aniq atom/zaryad balansi. DOCX: 9 bo‘lim, 9 jadval, 8 raqamlangan tenglama (18 OMML qatori / 8 strukturali kasr), 13 tasvir, 18 yonlavha, aniq 13.5:4.5 cm ustun. Xom underscore faqat qonuniy URL fayl nomida qolishi mumkin; matematik yozuvlarda yo‘q. Asosiy grafik va pit kesimi ochib ko‘rildi.

Google Docs roundtrip/sahifa renderi yetkazish tekshiruvida qayd etiladi. Lokal MS Word/LibreOffice renderer yo‘q; bo‘lim soni sahifa soni emas.

### Yakuniy konvertatsiya tekshiruvi
Native Google Docs→DOCX 1573053 bayt; 18 OMML qatori, 8 strukturali kasr, 9 jadval va 8 tenglama raqami saqlangan. Google PDF 854274 bayt, 10 sahifa. Birinchi renderdagi kirish yakuni yolg‘iz ikki qatorli sahifaga oqishi takroriy iboralarni ixchamlashtirish bilan bartaraf qilindi; yakuniy sahifalar matnli, deyarli bo‘sh sahifa yo‘q. OCP, parda qalinligi ODE, Stern–Geary va Faraday sahifalari ochib ko‘rildi. Bu Google konvertori natijasi, lokal Word rendererida tekshiruv emas. Mahalliy DOCX 551260 bayt, 3850 so‘z (matematik matn bilan).
