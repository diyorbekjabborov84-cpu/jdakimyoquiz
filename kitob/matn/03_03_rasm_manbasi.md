# 3.3. Dissotsiatsiya va pH — rasm, hisob va manbalar qaydi

## Ilmiy tayanchlar
1. IUPAC Gold Book, **pH**, DOI 10.1351/goldbook.P04524, https://goldbook.iupac.org/terms/view/P04524/plain . Ta’rifning to‘liq plain matni tadqiqot bosqichida o‘qilgan. IUPAC ifodasi molal faollik shkalasida; yakka ion faolligi konvensiyalari va amaliy kalibrlash chegaralari mustaqil o‘zbekcha bayon qilindi. Molyar konsentratsiya exact IUPAC ta’rifi sifatida berilmagan.
2. Atkins, de Paula, Keeler, *Atkins’ Physical Chemistry*, 11-nashr, OUP, 2018. Muvozanat, faollik va elektrokimyo nazariyasiga bibliografik tayanch; aniq sahifa raqamlari tekshirilmagan.
3. OpenStax, *Chemistry 2e*, Appendix H, https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . HSO₄⁻, 25 °C, Kₐ₂=1.2×10⁻² fakt qiymati qidiruv natijasida tekshirilgan. Bu bosqichda sahifaning to‘liq matni olinmagan. Jadval yoki rasm ko‘chirilmagan; yagona fakt ideal hisob misolida ishlatildi.

## Barcha tasvirlar original
`qurilma/draw_03_03.py` Pillow yordamida tayyorlaydi. Foto, tashqi kitob rasmlari, optimallashtirilgan molekulyar koordinatalar yoki tajriba grafiklari ishlatilmagan. Matndagi bibliografiya rasmlarning tashqi manbadan olinganini anglatmaydi. Word matni va tahrirlanadigan formulalar Times New Roman; raster rasmlardagi belgilar DejaVu Serif.

### 5 sxema
- `shkala.png`: pH 2/3/4 uchun faolliklarning nisbiy 100/10/1 birliklari. Ustun uzunligi faolliklar nisbatini ifodalaydi; molekula sonini bevosita o‘lchamaydi.
- `balans.png`: faqat HA va suv uchun moddiy/zaryad balanslari hamda konsentratsion konstantalar.
- `miqdor.png`: kuchli bir asosli kislotalar aralashmasida miqdorlarni qo‘shish va yakuniy hajmga bo‘lish.
- `faollik.png`: berilgan shartli molal γₘ=0.75 misoli. Bu koeffitsiyent real namuna uchun o‘lchangan qiymat emas.
- `nazorat.png`: model va natijani qayta tekshirish ish tartibi.

### 4 hisobiy grafik va ochiq CSV
- `kuchli.png` / `kuchli.csv`: 321 nuqta, log₁₀(C/c°)=−10…−2. h=(C+sqrt(C²+4Kw))/2 va suvni tashlagan −lg(C/c°) qiyosi.
- `kuchsiz.png` / `kuchsiz.csv`: 321 nuqta; shartli HA, Kc=10⁻⁵ mol/L va ayni C dagi to‘liq ajralgan HX. Ikkala hisobda ham suv bor. HA HF emas.
- `umumiy_ion.png` / `umumiy_ion.csv`: 281 nuqta; HA ning yakuniy C=0.0100 mol/L, Kc=10⁻⁵ mol/L, kuchli kislotaning yakuniy Cs=10⁻⁸…10⁻¹ mol/L. α=Kc/(Kc+h).
- `sulfat.png` / `sulfat.csv`: 321 nuqta; birinchi bosqich to‘liq, ikkinchi bosqich K₂,c=0.012 mol/L bilan muvozanatda. C=10⁻⁵…10⁻¹ mol/L. Suv balansda saqlangan. h≈C va h≈2C chiziqlari faqat taqqoslash; haqiqiy faolliklar yoki o‘lchangan pH emas. Yuqori C da ideal modelning real eritmaga cheklovi matnda ochiq aytilgan.

Barcha hisoblar 25 °C dagi ideal konsentratsion o‘quv modelida; Kw,c=10⁻¹⁴ (mol/L)². Modul: `qurilma/ph_03_03.py`. Faollik koeffitsiyentlari bilan to‘liq noideal muvozanat hisoblanmagan. γₘ=0.75 alohida faollik misoli bo‘lib, ideal muvozanatga yashirin qo‘shilmagan.

### 4 molekulyar/ion tasviri
- `gidroksoniy_model.png`: H₃O⁺ ning sxematik shar–tayoqcha tasviri, aniq fazoviy geometriya yoki gidrat qobig‘i emas.
- `hcl_model.png`: neytral H–Cl molekulasining ulanishi; suyultirilgan suvdagi asosiy zarracha sifatida ko‘rsatilmagan.
- `hf_model.png`: H–F ulanishi. Grafikdagi shartli Kc qiymati HF ga tegishli emas.
- `sulfat_model.png`: neytral H₂SO₄ molekulasidagi ikki O–H ulanishi; yon grafikdagi eritma tarkibi bilan aynanlashtirilmagan. Tayoqchalar to‘liq bog‘ tartibi modeli emas.

## Tekshiruv
`check_03_03.py`: 1244 grafik nuqtasi uchun musbatlik, moddiy balans, elektr zaryad balansi, K ifodasini qayta tiklash va tegishli logarifmlar; grafikdan tashqari 15 ikki-kuchsiz-kislota aralashmasi; sonli misollar; DOCX ZIP, 13 tasvir, 9 jadval, 9 tenglama, shriftlar va yuqori/pastki indekslar tekshirildi. Asosiy grafiklarning tasvirlari ham ochib ko‘rildi.

DOCX da 9 mazmuniy bo‘lim bor; bu 9 bosma sahifa degani emas. LibreOffice/Word paginatsion renderer mavjud emasligi sabab yakuniy sahifa soni va har bir sahifa joylashuvi vizual renderer bilan tasdiqlanmagan. Google Docs konversiyasining matn eksporti alohida tekshiriladi.
