# 2.5 — ilmiy tekshiruv, grafik va strukturalar

## Tekshirilgan birlamchi manba
Karen, P.; McArdle, P.; Takats, J. Comprehensive definition of oxidation state (IUPAC Recommendations 2016). Pure Appl. Chem. 88 (2016), 831–839. DOI 10.1515/pac-2015-1204.
To‘liq nashr PDF veb ekstraktining 0, 1, 2-chunklari o‘qildi: https://www.cup.lmu.de/ac/kluefers/homepage/L/kc2/literature/iupac_oxidation_state_2016.pdf . Nashr ma’lumoti IUPAC sahifasi bilan ham qidiruvda tasdiqlandi: https://iupac.org/recommendation/comprehensive-definition-of-oxidation-state/ . Provisional peer-review PDF asosiy manba sifatida ishlatilmadi.

Manbaning ushbu joylari matnning muhim qarorlarini belgiladi:
- 2–4-bo‘lim: ionli yaqinlashuv, geteroyadroli bog‘lar, homoyadroli juftlarni teng bo‘lish; bog‘ hissasiga formal zaryad qo‘shilishi.
- 5.3: S₂O₃²⁻ da amalda yakka S–S bog‘i algoritmik +5/−1 beradi. O‘rtacha +2 va nominal sistematik +6/−2 alohida ma’nolarga ega.
- 5.5 va 3-bo‘lim izohi: H–P elektrmanfiyliklari yaqin. H₃PO₃ da juftning H yoki P ga berilishi hisob tanlovi sifatida qayd etilgan. Shu sabab oddiy H(+1) konvensiyasi matnda ochiq belgilandi, muqobil P–H/H(−1) hisobi yashirilmadi.
- Allen jadvali: H 2,300; P 2,253. Bu chegaraviy misolni «elektrmanfiylik har doim bitta oddiy javob beradi» deb bayon qilishdan saqlanildi.

Qo‘shimcha nazariy tayanch: Housecroft & Sharpe, Inorganic Chemistry, 5-nashr, Pearson, 2018. Aniq sahifalari bu turnda tekshirilmagan.

## Grafikdagi sonlarning manbasi
Flowers va boshqalar. Chemistry 2e, OpenStax (2019), H ilova: https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . 2-chunkdagi 25 °C jadvalidan H₃PO₄ uchun uch faktik konstanta olindi: 7,5×10⁻³; 6,2×10⁻⁸; 4,2×10⁻¹³. Boshqa manbalardagi sonlar bilan aralashtirilmadi. pKₐ qiymatlari shu sonlardan qayta hisoblandi: 2,1249387; 7,2076083; 12,3767507.

OpenStaxning tayyor matni, jadval dizayni yoki rasm fayli ko‘chirilmagan; faqat uchta sonli faktga tayangan mustaqil grafik chizilgan. Ochilgan sahifada 2026-yilgi CC-BY-NC-SA qaydi ko‘rindi — uning rasmlarini butunlay erkin/CC-BY deb faraz qilish mumkin emas. Shu sahifadagi fosfit strukturasi tasvir izohi ham asos sifatida olinmadi; HP(O)(OH)₂ ulanishi IUPAC manbalari bilan izchil saqlandi.

## Grafik modeli va tekshiruv
h=10^(−pH); D=h³+K₁h²+K₁K₂h+K₁K₂K₃.
α₀=h³/D; α₁=K₁h²/D; α₂=K₁K₂h/D; α₃=K₁K₂K₃/D.
pH=0…14, qadam 0,025; 561 qator CSV. Berilgan pH dagi ideal ulushlar; massa/zaryad balansi orqali titrlash hisoblanmagan. Faollik koeffitsiyentlari, ion juftlanish, komplekslar va cho‘kma tashlab ketilgan. O‘lchangan egri chiziq emas.
Har qatorda α yig‘indisi 1 va uchala hαᵢ₊₁/αᵢ=Kᵢ munosabati sonli tekshirildi.

## 13 vizual
`qurilma/draw_02_05.py` va `rasmlar/oksidlanish/`:
- 8 sxema: `zaryadlar`, `balans`, `nitrat`, `xlor`, `perokso`, `fosfor`, `tiosulfat`, `algoritm`.
- 1 hisobiy grafik: `fosfat_ulush.png` va `.csv`.
- 4 shar–tayoqcha rasm: `hclo4_model`, `h2so5_model`, `ph_model`, `thio_model`.

Barcha tasvirlar original o‘quv chizmalari; tashqi fotosurat yoki tajribaviy koordinatalar ishlatilmagan. Ekran uchun qo‘lda idealizatsiyalangan proyeksiyalar. Tayoqcha atom ulanishini ko‘rsatadi, bog‘ tartibi yoki o‘lchangan elektron zichlikni emas. Rang: H oq, O qizil, P bronza, S sariq-bronza, Cl yashil. Rastrlar DejaVu Serif; Word matni, formulalari va jadvallari TNR.

Muhim strukturalar faqat rastrda emas: asosiy matn va tahrirlanadigan Word jadvallarida HO–S(=O)₂–O–OH; HO–S(=O)₂–O–O–S(=O)₂–OH; HP(=O)(OH)₂; ⁻O–S(=O)₂–S⁻; xlor oksokislotalari va nitrat yozuvlari ham berildi. S=O/P=O an’anaviy notatsiyasi d-orbital bog‘lanishning to‘liq fizik modeli deb ko‘rsatilmagan.

## Hujjat nazorati
9 mazmuniy bo‘lim, 9 jadval, 13 yon vizual, 18 yonlavha, 6 raqamlangan ifoda/muvozanat. Rekursiv DOCX matni 3233 so‘z; 464448 bayt. ZIP yaxlitligi, TNR, indekslar, rasm/jadval soni va eski mavzu markerlari tekshirildi. H₂SO₅ modeli, fosfat grafik va tiosulfat sxemasi alohida ko‘rildi. Word/PDF sahifalari render qilinmagan; bo‘limlar soni sahifalar soni deb da’vo qilinmaydi.
