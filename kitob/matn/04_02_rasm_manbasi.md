# 4.2. Oksidlovchilik va qaytaruvchilik — ilmiy tayanchlar, tasvirlar va tekshiruv

## Manbalar va ulardan foydalanish
2026-10-22 kuni quyidagilar ko‘rildi:
- OpenStax Chemistry 2e 17.3, https://openstax.org/books/chemistry-2e/pages/17-3-electrode-and-cell-potentials — 2-chunk to‘liq o‘qildi: SHE ga nisbatan qaytarilish potensiali ta’rifi, Cu uchun +0.337 V, standart juftlar. 0-chunk asosan cookie banneri bo‘lgan va ilmiy dalil sifatida olinmagan.
- OpenStax 17.4, https://openstax.org/books/chemistry-2e/pages/17-4-potential-free-energy-and-equilibrium — 2-chunk to‘liq o‘qildi: Nernst, ΔG, nF va K bog‘lanishlari. Manba misollari yoki tayyor tasvirlari ko‘chirilmagan. K>1 umumiy stexiometriyada barcha mahsulotlar konsentratsiyalari reagentlardan katta bo‘lishi shart degan soddalashtirish takrorlanmagan.
- OpenStax Appendix L, https://openstax.org/books/chemistry-2e/pages/l-standard-electrode-half-cell-potentials — 0 va 1-chunk to‘liq ko‘rildi. Faqat tekshirilgan sonli faktlar olindi: Zn²⁺/Zn −0.7618 V; Cu²⁺/Cu +0.337 V; Fe³⁺/Fe²⁺ +0.771 V; NO₃⁻/NO +0.957 V; MnO₄⁻/Mn²⁺ +1.507 V; H₂O₂/H₂O +1.776 V; O₂/H₂O₂ +0.695 V. H⁺/H₂ 0 V. Qaytarilish yo‘nalishi va muhit yashirilmagan. Butun manba jadvali, prose yoki rasm ko‘chirilmagan; mahalliy jadval mustaqil izohlar bilan tuzilgan.
- OpenStax 4.2 redoks/kislota–asos tasnifi oldingi mavzularda ko‘rilgan nazariy tayanch.
- Housecroft & Sharpe, Inorganic Chemistry, 5 ed., Pearson 2018; Atkins, de Paula & Keeler, Physical Chemistry, 11 ed., OUP 2018 — umumiy bibliografik tayanch; aniq sahifalar tekshirilmagan. Bu nashrlardan matn yoki rasm ko‘chirilmagan.

## Muhim ilmiy ajratishlar
Kislota kuchi ≠ redoks potensial; proton manbai ≠ doimiy elektron qabul qiluvchi markaz; kuzatuvchi nitrat ≠ qaytarilgan nitrat; elektrod E si ≠ umumiy E_cell; potensial intensiv, ΔG va n tenglama ko‘lamiga bog‘liq. Bir atomga elektron sig‘imi mahsulotni oldindan bashorat qilmaydi. Daraja haqiqiy atom zaryadi yoki elementar mexanizm emas.

P–H uchun kitobning 2.5 dagi an’anaviy H(+1), O(−2), P(+1/+3/+5) konvensiyasi saqlangan va ochiq aytilgan. Boshqa P–H elektron taqsimoti formal markaz yorliqlarini o‘zgartirsa ham 2e/4e umumiy balans o‘zgarmaydi. P=O yozuvi d-orbital kengayishi bilan asoslanmagan. N₂O uchun N(+1) faqat o‘rtacha, ikki N atomining ekvivalentligini anglatmaydi.

Suvli «H₂SO₃» tarkibi erigan SO₂/gidrogensulfit/sulfit bilan izohlandi. Konsentrlangan H₂SO₄ da a(H₂O)≈1 va ideal suyultirilgan standartlarni avtomatik qo‘llash rad etildi. Passivlanish faqat tezlik chegarasi sifatida keltirilgan, batafsil mavzu 4.3 ga qoldirilgan. Zaharli gazlar uchun tajriba retsepti yoki aralashtirish ko‘rsatmasi yo‘q.

## Hisobiy modellar va ochiq ma’lumot
`qurilma/redox_04_02.py`: R=8.31446261815324 J/(mol K), T=298.15 K, F=96485.33212 C/mol; S=ln(10)RT/F=0.059159349686811843 V.

Barcha grafiklar original model; tajriba nuqtalari emas. `rasmlar/redoks/`:
- `energiya.png` + `.csv`: 281 qiymat; E_cell −0.2…1.2 V; n=1/2/5; ΔG=−nFE. Elektrodning tok–kuchlanish grafigi emas.
- `ph.png` + `.csv`: 201 qiymat, pH 0…4; H⁺/H₂, MnO₄⁻/Mn²⁺, NO₃⁻/NO. Boshqa faolliklar yoki mos nisbatlar bir, suv faolligi bir. To‘liq Pourbaix, faza yoki turlar ustunligi diagrammasi emas.
- `sigim.png` + `.csv`: 6 nishon; N(+5)→NO₂/NO/NH₄⁺ uchun 1/3/8; S(+6)→SO₂/S/H₂S uchun 2/6/8 elektron har markazga. Real mahsulot tanlash mezoni emas.
- `peroksid.png` + `.csv`: 201 qiymat, pH 0…4; boshqa faolliklar bir. H₂O₂/H₂O va O₂/H₂O₂ potensiallari; farq 1.081 V. Barqaror saqlash muddati yoki tajribaviy reaksiya tezligi aniqlanmaydi.

Jami 689 grafik nuqtasi/satri. Mn–Fe umumiy standart reaksiya uchun n=5, E°_cell=0.736 V, ΔG°=−355066.0222016 J/mol, lgK=62.2048758055. Peroksidning 2H₂O₂→2H₂O+O₂ tenglamasi uchun n=2 va ΔG°=−208601.28804344 J/mol.

Ishlangan model: 0.4000 mmol MnO₄⁻ va 2.500 mmol Fe²⁺; 70.00 mL yakuniy hajm; 3.200 mmol H⁺ sarfi, yakuniy a(H⁺)=0.100 berilgan. γ≈1, komplekslanish va gidroliz tashlangan. [Fe³⁺]/[Fe²⁺]=4; E(Fe)=0.8066174776 V (SHE). Bir xil muvozanat potensiali sharti bilan [MnO₄⁻]≈3.65078×10⁻⁵⁴ M formal iz chiqadi. Bu makroskopik uzluksiz modelning ekstrapolyatsiyasi, real 70 mL da o‘lchanadigan ion konsentratsiyasi yoki butun ionlar soni deb olinmagan. Real eritma formal potensiallari bilan aynan tenglashtirilmagan.

## Original sxemalar va tuzilish rasmlari
`draw_04_02.py` Pillow orqali tashqi rasmlarsiz chizadi. Word matni TNR, Equation Cambria Math, raster yozuv DejaVu Serif.
- 5 sxema: `elektron`, `balans`, `nitrat`, `fosfor`, `hisob`.
- 4 model: `nitrat_model` — tekis uch ulanishli NO₃⁻; `fosfit_model` — H₃PO₃: bitta P–H, ikkita O–H; `gipofosfit_model` — H₃PO₂: ikkita P–H, bitta O–H; `peroksid_model` — H–O–O–H, haqiqiy molekula tekis emasligi aytilgan.
Molekulyar chiziqlar ulanishni bildiradi; to‘liq bog‘ tartibi, formal zaryadlarning to‘liq Lewis taqsimoti, optimallashtirilgan burchak yoki atom koordinatasi emas. P–H bronza rang bilan ajratilgan; ranglar shartli. Rasm huquqlari noma’lum fotosurat ishlatilmagan. Bob kirish rasmi alohida qolgan.

## DOCX va QA
`build_04_02_sidebar.py`: A4 13.5 cm + 4.5 cm; 9 bo‘lim, 9 tahrirlanadigan jadval, 8 raqamlangan tenglama (17 haqiqiy OMML qatori, 3 strukturali kasr), 13 tasvir, 18 mazmunli yonlavha.

`check_04_02.py` PASS: 689 grafik qiymati; 30 ta aniq molekulyar/ionli/yarimreaksiyada mustaqil formula-parser orqali atom va zaryad balansi; Fe/Mn moddiy va elektron/proton sarfi; Nernst va termodinamik identiklar; kichik musbat permanganat izi bilan ikki juftning umumiy muvozanati; ZIP, matematik obyektlar, formulalarda xom underscore/LaTeX yo‘qligi, raqamlar, TNR matni, 3:1 ustun va tasvir/jadval sonlari.

Asosiy grafiklar va fosfit modeli ochib ko‘rildi. Google Docs roundtrip va sahifa renderi tekshiruvi yetkazish bosqichida alohida qayd etiladi. Bo‘lim soni sahifa soni emas; lokal MS Word/LibreOffice renderer yo‘q.

### Yakuniy yetkazish tekshiruvi
Native Docs→DOCX 1564684 bayt; 17 OMML qatori, 3 kasr, 8 tenglama raqami, 9 jadval sarlavhasi saqlangan. Google PDF 855765 bayt, 10 sahifa; deyarli bo‘sh sahifa yo‘q. Nernst, nitrat, fosfor, peroksid sahifalari ochib ko‘rildi. Yon ustunda `fosfit_yon.png` va `gipofosfit_yon.png` to‘liq modelning barcha atom/ulanishlarini qoldiruvchi original crop, takroriy raster izohlar olib tashlangan; bob kirish rasmiga ta’sir qilinmagan. Birinchi maketdagi page-break bo‘sh sahifasi va 7-bo‘limdagi yonlavha oqishi yakuniy nusxada tuzatilgan. Lokal MS Word renderer emas, Google konvertori natijasi tekshirildi.
