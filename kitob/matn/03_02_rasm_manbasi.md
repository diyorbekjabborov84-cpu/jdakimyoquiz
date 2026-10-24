# 3.2. Kuchga ta’sir etuvchi omillar — manbalar va tekshiruv

## Ilmiy manbalar
1. Atkins, P.; de Paula, J.; Keeler, J. Atkins’ Physical Chemistry. 11th ed. OUP, 2018. Solvatlanish sikllari, Born kontinuum yondashuvi, muvozanatning haroratga bog‘liqligi. Aniq sahifalar bu turnda ochib tekshirilmagan va keltirilmagan.
2. Housecroft, C. E.; Sharpe, A. G. Inorganic Chemistry. 5th ed. Pearson, 2018. HX va HOX oilalari, oksokislotalar, zaryad va suvli kislota–asos tizimlari. Bu turnda matn sahifalari qayta ochilmagan; bayon mustaqil tuzilgan.
3. IUPAC Gold Book, levelling effect, DOI 10.1351/goldbook.L03506. https://goldbook.iupac.org/terms/view/L03506/plain — ushbu turnda to‘liq qisqa ta’rif o‘qildi. Asosiy natija: erituvchidan yetarlicha kuchli Brønsted donorlar protonni erituvchiga deyarli to‘liq berib, ularning kislotaligi bir xil mo‘tadil past konsentratsiyalarda o‘xshash ko‘rinadi. Ta’rif uzun iqtibos qilinmadi; mustaqil o‘zbekcha izoh va manba qaydi berildi.

## Muhim ilmiy chegaralar
- Gomolitik H–X energiyasi eritmadagi proton berish ΔG°/pKₐ bilan tenglashtirilmadi.
- Qiyos oilasi ajratildi: HX bo‘ylab bog‘/o‘lcham/solvatlanish; HOX bo‘ylab markaziy atomning elektron xossalari; bir markazli oksokislotalarda terminal O va asos tuzilishi.
- HNO₃ va NO₃⁻ ning ikkalasi ham elektron tuzilish nuqtayi nazaridan tahlil qilinadi; rezonans yozuvlarining sonidan pKₐ topilmaydi.
- Markaziy P(+5) ning saqlanishi ketma-ket Kₐ lar tengligini bildirmaydi.
- Kₐ₁=2k, Kₐ₂=k/2 va nisbat 4 faqat ikki mustaqil ekvivalent donor joyli ideal statistik tasvir. Haqiqiy fosfat shu shartli hisob bilan tenglashtirilmagan.
- Akvakompleksning sxematik proton ajralishida H⁺ mahsuloti ham yozildi; atom va zaryad saqlanishi e’tiborga olindi.
- Solvatlanish siklida HA, H⁺ va A⁻ hissalari hamda izchil standart holatlar birgalikda ko‘rsatiladi. Yakka-ion solvatlanish qiymatlaridagi konvensiya chegarasi aytildi.
- Vodorod bog‘i HA yoki A⁻ tomonini turlicha barqarorlashtirishi mumkin. HF₂⁻ barcha suyultirilgan HF eritmalarida ustun deb ko‘rsatilmagan.
- Muvozanat konstantasi reaksiya tezligi va oddiy kataliz bilan almashtirilmadi.

## Ikki shartli egri chiziq
Hisob manbasi `qurilma/effects_03_02.py`; chizish `qurilma/draw_03_02.py`.

### Bornning o‘lchamsiz omili
ρ=r/r₀; z=1, B=(1−1/εᵣ)/ρ; εᵣ=2 va 80; ρ=0,5…3 qadam 0,01 (251 qator).
To‘liq sodda kontinuum ifodasida ΔG_Born=−[N_A z²e²/(8π ε₀r₀)]B. B musbat, uning ortishi shu bitta elektrostatik hissani manfiyroq qiladi. εᵣ qiymatlari aniq ikkita haqiqiy erituvchi uchun o‘lchov sifatida nomlanmagan. Atom radiuslari, birinchi solvat qobig‘i va maxsus H-bog‘lar bu taxminiy hisobda yo‘q. Grafik real kislotalarning pKₐ reytingi emas.

### Harorat hisobi
T₀=298,15 K; pKₐ(T₀)=5; ΔH°=±10000 J mol⁻¹; R=8,314462618 J mol⁻¹ K⁻¹. ΔH° o‘zgarmas:
pKₐ(T)=5+[ΔH°/(R ln10)](1/T−1/T₀).
T=273,15…333,15 K qadam 0,25 (241 qator). Endotermik holatda T ortishi bilan pKₐ ni pasaytiradi; ekzotermik holatda oshiradi. Ikkalasi ham shartli; HF, HOCl yoki fosfatning haqiqiy tajribaviy egri chiziqlari emas. Issiqlik sig‘imi farqi va boshqa muvozanatlar kiritilmagan.

## Rasmlar
Jami 13 yon vizual, barchasi 25% chetki ustunda:
- 7 sxema: `umumiy`, `boglar`, `oksokislota`, `delokallashuv`, `zaryad`, `mahalliy`, `algoritm`.
- 2 hisobiy grafik va CSV: `born`, `harorat`.
- 4 shar–tayoqcha rasm: `hf_model`, `hocl_model`, `nitrat_model`, `fosfat_model`.

Barcha chizmalar original o‘quv tasvirlari. Koordinatalar qo‘lda idealizatsiyalangan ekran proyeksiyasi, tajriba yoki DFT natijasi emas. Tayoqchalar ulanishni ko‘rsatadi, bog‘ tartibi yoki elektron zichlikni emas. Ranglar: H oq, O qizil, N ko‘k, F/Cl yashil, P bronza. Word matn/formula/jadvallari TNR; rastrlarda DejaVu Serif.

## Qayta ishlab chiqariladigan nazorat
`qurilma/check_03_02.py`:
- 251 Born nuqtasida normalizatsiya va radius ortganda kamayish;
- 241 harorat nuqtasida integral van’t Hoff tengligi;
- tayanch T₀ va differensial van’t Hoff ishorasi sonli hosila orqali;
- DOCX ZIP, TNR, indekslar, 13 rasm/9 jadval, eski yorliq va markerlar yo‘qligi.
9 bo‘lim, 9 jadval, 7 sxema, 2 grafik, 4 molekulyar rasm, 8 raqamlangan ifoda, 18 yonlavha. Rekursiv matn 3264 so‘z; 462231 bayt. Mahalliy muhit sxemasi va ikkala grafik ko‘rildi. Word/PDF sahifalari rendererda tekshirilmagan; bo‘limlar soni sahifa soni deb da’vo qilinmaydi.
