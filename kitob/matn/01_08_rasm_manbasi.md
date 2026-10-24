# 1.8. Nazariyalarni qiyoslash — jadvallar, chizmalar va grafiklar

## Vizual tuzilma
- 7 ta tahrirlanadigan qiyosiy jadval: `matn/01_08_jadvallar.json`.
- 5 ta tushuntiruvchi sxema va 2 ta hisobiy grafik: `qurilma/draw_01_08.py`.
- 21 ta yonlavha: `matn/01_08_yonlavhalar.json`.
- Nazariyalarni bitta «kuch» shkalasiga yoki qat’iy qamrov pog‘onasiga joylashtiruvchi sun’iy grafik ishlatilmaydi.
- Portret o‘rniga mezonlar va reaksiyalar orasidagi bog‘lanishlar chizildi; mavzu olimlar tarjimayi holi emas, nazariy vositalarni qiyoslashga qaratilgan.

## Grafik 1: protonlanish shakllari
- Ideal, bir protonli, ikki shaklli HA/A− tizimi.
- x=pH−pKa, x=−3…3.
- Ko‘k: f(HA)=1/(1+10^x); bronza: f(A−)=10^x/(1+10^x).
- Bu titrlash egri chizig‘i ham, HSAB qattiqlik grafigi ham emas.
- Ion kuchi/faollik koeffitsiyentlari uchun idealga yaqinlik qabul qilingan; boshqa kimyoviy shakllar yo‘q.

## Grafik 2: boshlang‘ich shartlari boshqa ikki yondashuv
- x=lg q, x=−4…4.
- Ko‘k: teng miqdorli A+B⇌C+D ideal almashinuvi; boshlang‘ich mahsulotlar yo‘q; q=K; f=√q/(1+√q).
- Bronza: ideal A+L⇌AL va erkin ligand faolligi tashqaridan berilgan; q=K·a(L); θ=q/(1+q).
- K har ikki yozuvda o‘lchamsiz termodinamik konstantadir, ammo q ning fizik ma’nosi har bir yondashuvda boshqa. Grafik sonli funksiyalar qiyosi, bir xil reaksiya uchun zid bashorat emas.
- q=100 da ko‘k: 90,91%; bronza: 99,01%.
- Barcha hisob nuqtalari rasm papkasida CSV fayllarda saqlanadi.

## Ilmiy tayanchlar
- Housecroft & Sharpe. Inorganic Chemistry, 5-nashr, 2018.
- Pearson, R. G. Hard and Soft Acids and Bases. JACS 85 (1963), 3533–3539.
- IUPAC Gold Book, acidity function, DOI 10.1351/goldbook.A00081; superacid, DOI 10.1351/goldbook.S06135.
- Atkins, de Paula & Keeler. Atkins’ Physical Chemistry, 11-nashr, 2018.

## Tekshiruvlar
- Formulalar Word quyi/yuqori indeks xususiyatlari bilan yoziladi; jadvallar rasm emas.
- Ichma-ich jadvallar rekursiv tekshirilib, 7 ta mazmuniy jadval sarlavhasi, shriftlar, indekslar va DOCX ZIP yaxlitligi tasdiqlandi.
- Word yoki PDF rendererida sahifalar vizual tekshirildi deb da’vo qilinmaydi; grafik va sxemalarning o‘zi rasm ko‘rinishida ko‘rib chiqildi.
