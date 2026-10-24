# 3.1. Kₐ, pKₐ, α — shartli hisob, manbalar va tekshiruv

## Tayanch adabiyotlar
1. Atkins, P.; de Paula, J.; Keeler, J. Atkins’ Physical Chemistry. 11th ed. OUP, 2018. Muvozanat termodinamikasi, faollik va kislota–asos muvozanatlari.
2. Housecroft, C. E.; Sharpe, A. G. Inorganic Chemistry. 5th ed. Pearson, 2018. Suvli eritmalarda kislota–asos hisoblari.
Aniq sahifalar ushbu turnda tashqi manbadan tekshirilmagan va keltirilmagan. Nazariya mustaqil o‘zbekcha bayon qilindi. Sonli grafiklar tayyor adabiyot grafiklaridan olinmagan.

## Belgilashlar va birliklar
- Kₐ termodinamik, o‘lchamsiz; a(i)=γᵢ[i]/c°, c°=1 mol/L.
- K_c=[H⁺][A⁻]/[HA], birligi mol/L; K_c=Kₐc°γ(HA)/(γ(H⁺)γ(A⁻)).
- Konsentratsion K_w,c birligi (mol/L)². Barcha ideal hisoblarda 25 °C uchun 10⁻¹⁴ olindi.
- H⁺ odatiy suvli proton standart holati bilan ishlatiladi; to‘liq HA+H₂O reaksiya konstantasi bilan suv faolligi o‘z-o‘zidan yo‘qoladi degan da’vo qilinmadi.
- pH=−lg a(H⁺); γ=1 sharoitida pH=−lg(h/c°). Grafiklaridagi h mol/L da bo‘lgani va c° soni 1 bo‘lgani uchun −lg(h ning son qiymati) hisoblandi.
- α=[A⁻]/C faqat ma’nosi ko‘rsatilgan oilaviy ulush. Tuz va suv mavjudligida α=h/C tengligi shartsiz ishlatilmaydi.

## Sonli hisoblar
`qurilma/equilibria_03_01.py` yagona hisobiy manba:
- kvadrat yechim: x=2K_cC/[K_c+sqrt(K_c²+4K_cC)].
- suv bilan: h−K_w,c/h−CK_c/(K_c+h)=0; musbat monoton tenglama [sqrt(K_w,c), sqrt(K_w,c)+C] oralig‘ida biseksiya bilan yechiladi.
- diprotik: D=h²+K₁h+K₁K₂; α lar mos uch hadning D ga nisbati.

Shartli HA: Kₐ=10⁻⁵, γ=1, K_c=10⁻⁵ mol/L. Bu HF yoki rasmda ko‘rsatilgan haqiqiy modda konstantasi emas.
- C=0,01: kvadrat x=0,0003112672920; α=0,0311267292; pH=3,5068665126.
- C=0,0001: kvadrat x=0,00002701562119; α=0,2701562119; pH=4,5683850420.
- C=10⁻⁸: suvli ideal h=1,0507035031×10⁻⁷; pH=6,9785198198; α=0,9896022149. Suvsiz kvadrat pH=8,0004336445 — qo‘llanish chegarasidan chiqqan taxminiy natijasi sifatida ko‘rsatiladi.
Diprotik shartli H₂A: K₁=10⁻³, K₂=10⁻⁷ mol/L. pH=5 da α₀=α₂=1/102; α₁=100/102; ν=1. Bu H₃PO₄ konstantalari emas.
5% mezoni x/C ni tekshiradi. Taqribiy mezon C/K_c≥400, aniq α≤0,05 mezoni ≥380. α=0,05 da x taqribining nisbiy xatosi ≈2,60%, pH foiz xatosi emas.

## Original vizuallar
`qurilma/draw_03_01.py`, `rasmlar/ka_pka_alfa/`:
- 5 sxema: `uch_belgi`, `faollik`, `pka`, `umumiy_ion`, `algoritm`.
- 4 hisobiy grafik va CSV: `alfa_model` (321 nuqta), `taqrib_xato` (251 nuqta), `suv_tasiri` (321 nuqta), `diprotik` (481 nuqta).
- 4 hajmli tasvir: `suv_model`, `hf_model`, `gidroksoniy_model`, `fosfat_model`.
Grafiklar tajribaviy natija yoki titrlash egri chiziqlari emas. Molekulyar rasmlar qo‘lda idealizatsiyalangan ekran proyeksiyalari; koordinatalar tajriba yoki DFT dan olinmagan. Sharlardagi soya hajmni ko‘rsatish uchun; elektron zichlik sirtlari emas. HF rasmining Kₐ=10⁻⁵ ga, H₃PO₄ rasmining diprotik shartli grafik konstantalariga tenglashtirilmasligi alohida yozildi.

Barcha vizuallar 25% chetki ustunda. Asosiy matn va jadvallar TNR; rastr grafika DejaVu Serif. Word formulalaridagi indekslar tahrirlanadigan font xususiyatlari bilan berilgan; K_c va C_T indekslari ham alohida formatlanadi. Rasmlarda K_c indeksining literal pastki chiziq ko‘rinishi ko‘rib chiqilgach, grafik matn chizish funksiyasi haqiqiy kichik pastki c bilan tuzatildi.

## Tekshiruv va chegaralar
`qurilma/check_03_01.py` qayta ishga tushiriladigan tekshiruv:
- 321 monoprotik konsentratsiyada fizik oraliq, moddiy/zaryad balansi va K_c tiklanishi;
- 481 diprotik pH nuqtasida ulushlar yig‘indisi va ikkala konstanta tiklanishi;
- matndagi uch sonli misol;
- DOCX ZIP, 13 vizual, 9 jadval, TNR, sub/sup indekslar, markerlar va eski mavzu yorliqlari yo‘qligi.

9 bo‘lim, 9 jadval, 5 sxema, 4 grafik, 4 molekulyar rasm, 11 raqamlangan formula va 18 yonlavha. Rekursiv DOCX hisobida 2975 so‘z, yakuniy fayl 408808 bayt. Suv ta’siri, taqrib xatosi va diprotik grafiklar alohida ko‘rildi. Word/PDF sahifalari rendererda tekshirilmagan; 9 bo‘limni 9 sahifa deb talqin qilmaslik kerak.
