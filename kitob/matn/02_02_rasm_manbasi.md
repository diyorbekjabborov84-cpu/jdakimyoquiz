# 2.2. Rezonans va vodorod bog‘i — manbalar va tasvirlar

## Ilmiy manbalar
1. Housecroft, C. E.; Sharpe, A. G. Inorganic Chemistry. 5th ed. Pearson, 2018. Rezonans, molekulyar bog‘lanish va noorganik ionlar.
2. Atkins, P.; de Paula, J.; Keeler, J. Atkins’ Physical Chemistry. 11th ed. OUP, 2018. Elektron tuzilish, spektroskopiya va eritmalar. Kitob sahifalari bu turnda tekshirilmagan; aniq sahifa raqamlari berilmadi.
3. Arunan, E. et al. Definition of the hydrogen bond (IUPAC Recommendations 2011). Pure and Applied Chemistry 83, 1637–1641. DOI 10.1351/PAC-REC-10-01-02. https://publications.iupac.org/pac/pdf/2011/pdf/8308x1637.pdf — qidiruv natijasida ta’rifning matni, X–H···Y yozuvi va nazariy/eksperimental dalil zarurati tekshirildi. To‘liq PDF mazmuni qayta ko‘rib chiqilgani da’vo qilinmaydi.

## Vizuallar kelib chiqishi
Barcha 11 tasvir `qurilma/draw_02_02.py` orqali original chizildi; tashqi fotosurat emas. Diagramma va hajmli shar–tayoqcha ko‘rinishlari alohida belgilandi. Atomlar koordinatalari qo‘lda idealizatsiya qilingan proyeksiyalar; rentgen, DFT yoki PubChem koordinatalari emas. Sharlardagi yorug‘lik badiiy chuqurlik effekti bo‘lib, elektron zichlik sirtini bildirmaydi. Rasmlar DejaVu Serif, Word asosiy matni/formulalari/jadvallari Times New Roman.

- `hissalar.png`: nitratning uch Lewis hissasi; atomlar siljimaydi, qo‘sh bog‘ning formal joyi almashadi. Yakka elektron juftlar berilmagan, formal zaryadlar ko‘rsatilgan.
- `tekshiruv.png`: rezonansning saqlanish shartlari.
- `delokal.png`: teng yo‘nalishlar, formal o‘rtacha 4/3. Uzuq chiziq elektron zichlik hisoblash natijasi emas.
- `geometriya.png`: ikki vodorod bog‘i yo‘nalishi; burchak va masofa sonli o‘lchovlari berilmagan.
- `ir_model.png` va CSV: A₁=0,85 exp[−(ν−3700)²/(2×35²)]; A₂=exp[−(ν−3300)²/(2×145²)], ν cm⁻¹; 2800…4000 diapazon. Ikki faraziy Gaussian tasma; real modda yoki tajriba emas. IR o‘qi chapdan o‘ngga kamayadi.
- `proton.png`: O–H···O bo‘ylab proton joylashuvining ikki shartli tasviri; chizmada boshqa H atomlar tashlab ketilgan. Barcha protonlar sinxron almashishi talab qilinmaydi.
- `qiyos.png`: ichki elektron tuzilish va donor–akseptor ta’siri farqi.
- `nitrat_model.png`: N ko‘k, O qizil; trigonal tekis proyeksiya. Tayoqchalar bog‘ yo‘nalishlari, yakka bog‘lar haqidagi mutlaq da’vo emas.
- `karbonat_model.png`: C kulrang, O qizil; trigonal tekis proyeksiya.
- `dimer_model.png`: ikki neytral suv molekulasi; O–H uzluksiz, H···O bronza uzuq chiziq; masshtabsiz.
- `gidroksoniy_model.png`: H₃O⁺ piramidal ko‘rinishining o‘quv tasviri; eritmadagi yagona proton holati emas.

## Maket va tekshiruv
3+1 ustun nisbati saqlandi. Qo‘shimcha to‘rtta molekulyar rasm aynan chetki 25% ustunga, nitrat/delokallashuv/vodorod bog‘i/proton solvatlanishi bo‘limlariga kiritildi. Yonlavhalar soni 14 taga tushirilib, rasm uchun joy ko‘paytirildi. 7 bo‘lim, 7 jadval, 6 sxema, 1 hisobiy grafik, 4 molekulyar rasm, 2 raqamlangan formula. ZIP yaxlitligi, TNR, indekslar, eski markerlar yo‘qligi tekshirildi; dimer, rezonans va IR tasvirlari ko‘rildi. Word/PDF sahifalari rendererda tekshirilmagan.
