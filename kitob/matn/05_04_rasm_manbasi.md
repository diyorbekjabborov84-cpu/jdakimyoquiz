# 5.4. Sanoat prinsiplari — manba va rasm izohi

## Manbalar (to‘liq o‘qilgan)
1. **ISO 22400-2:2014 — Automation systems and integration — Key performance indicators (KPI) for manufacturing operations management — Part 2: Definitions and descriptions.** OEE ta’rifi: **OEE = Availability × Performance × Quality**; Availability — ish vaqti / rejalashtirilgan vaqt; Performance — haqiqiy natija / imkoniyat; Quality — mahsulot / yaratilgan natija. U shuningdek «mahsulot sifati, jarayon barqarorligi va resurs samaradorligi» o‘lchovlari uchun umumiy til beradi.
2. **OPC UA OPC-40501-1, C.2.4 — Machine Monitoring and Job Management.** APT (Actual Production Time) va PBT (Planned Production Time) dan OEE hisoblash: OEE = PRI × PQ / APT (Performance = Actual Production Time / Planned Production Time; Quality = Good Quantity / Production Quantity).
3. **Luis (2013), J. Chem. Technol. Biotechnol. 88(11), 1711–1718 — «Exergy as a tool for measuring process intensification in chemical engineering».** Eksergiya — atrof-muhit sharoitida muvozanatga kelguncha olinishi mumkin bo‘lgan maksimal foydali ish; eksergiya yo‘qotilishi qaytarilmas jarayonlar bilan bog‘liq.
4. **IUPAC Gold Book — «exergy»**, «process intensification» (Ramshaw, 1995; Stankiewicz & Moulijn, 2000), «waste», «hazard». PI — texnologik jihatdan kuchaytirish, uning asosiy vositasi hajmni kamaytirish (kichik o‘lchamli apparatlar).
5. **OpenStax, Chemistry 2e, Appendix G — Standard Thermodynamic Properties** (https://openstax.org/books/chemistry-2e/pages/g-standard-thermodynamic-properties-for-selected-substances). ΔfH° (25 °C): HNO₃(l) −174,10; HNO₃(g) −80,73; H₂O(l) −285,83; H₂O(g) −241,82; NH₃(g) −45,90; NO(g) +90,25; NO₂(g) +33,18; O₂(g) 0 kJ/mol.
6. **CRC Handbook of Chemistry and Physics, 97th ed. — Saturated steam table.** p (MPa) / T (°C) / h_fg (kJ/kg): 0,10 → 99,63 → 2257,5; 0,50 → 151,83 → 2108,0; 1,00 → 179,89 → 2015,3; 2,00 → 212,42 → 1888,6; 4,00 → 250,40 → 1713,0; 6,00 → 275,64 → 1565,3; 8,00 → 295,06 → 1441,0.
7. **ISO 9001, ISO 14001, ISO 45001, WHO GMP, CFR Part 211 (cGMP)** — sifat, atrof-muhit va mehnat xavfsizligi tizimlari hamda farmatsevtika ishlab chiqarish amaliyoti (GMP) talablari; ular tizim darajasida keltirilgan, kislota ishlab chiqarishga xos texnik retsept emas.
8. **Ph. Eur. 6.0 umumiy bo‘limlari — 2.2.32 (quruq qoldig‘), 2.5.12 (suv miqdori), 5.11 (higroskopiklik)** — 5.1–5.3-bo‘limlarida batafsil ko‘rib chiqilgan; 5.4-bo‘limda sifat boshqaruvi tizimi ichida qisqa chaqiriladi.
9. **SPE (Society of Petroleum Engineers) va umumiy sanoat amaliyoti** — apparat tanlash ierarxiyasi (po‘lat → 316L → Hastelloy → PTFE/grafit), korroziya tezligi, DCS/PI/DCS-safety kontsepsiyalari umumiy tamoyil darajasida keltirilgan; kislota ishlab chiqarish retsepti va texnologik parametrlar berilmagan.

## Model va hisoblar (barchasi ochiq shartli, o‘lchov ma’lumoti emas)
- **Zanjir mass balansi (1000,0 kg 68 % li HNO₃).** Kirish: HNO₃ 680,00 kg + suv 320,00 kg = 1000,00 kg; n(HNO₃) = 10,7919 kmol. Reagentlar: NH₃ 183,80 kg, O₂ 690,68 kg; N₂ (ortiqcha) 2596,97 kg (N₂/O₂ = 3,76). Suv: hosil 194,42 kg + tashqaridan 222,79 kg = kiruvchi 417,21 kg; absorberda bog‘lanadigan 97,21 kg, eritmada qoladigan 320,00 kg. Chiqish: 68 % li eritma 1000,00 kg; keyin konsentratsiya — suv chiqariladi 306,12 kg, mahsulot 693,88 kg (HNO₃ 680,00 + suv 13,88); azeotrop distillati 1546,07 kg, toluen 1239,95 kg. Oraliq mahsulotlar: NO 323,87 kg, NO₂ 496,54 kg.
- **Energetika.** ΔfH°(NH₃ + 2O₂ → HNO₃(l) + H₂O(l)) = −174,10 + (−285,83) − (−45,90) = **−414,03 kJ/mol**; 10,7919 kmol uchun **−4468,2 MJ (≈ −4,47 GJ)**. Konsentratsiya bug‘latishi: 306,12 kg suv → 690,9 MJ (2,2568 MJ/kg); 1239,95 kg toluen → 512,2 MJ; jami 1203,1 MJ. Qatnoq bug‘ darajalari: 0,10 MPa → 99,63 °C; 0,50 → 151,83; 1,00 → 179,89; 2,00 → 212,42; 4,00 → 250,40; 6,00 → 275,64; 8,00 → 295,06 °C; h_fg 2257,5 → 1441,0 kJ/kg.
- **Korroziya modeli.** m = (m₀ − m₁)/(S·τ): 0,12 g / (100 × 0,100 m² × 1000 s) = **0,0012 g/(m²·soat)** — model qiymat, materialni real korroziy tezligi emas.
- **Sifat modeli.** Cpk = min[(USL − x̄)/(3σ), (x̄ − LSL)/(3σ)]; model: x̄ = 68,40 %, USL = 70,0 %, LSL = 66,0 %, σ = 0,38 % → **Cpk = 1,39**.
- **OEE va iqtisodiyot.** OEE = 0,92 × 0,95 × 0,99 = **0,8653**; quvvat 100 000 t/y → savdo hajmi **86 526 t/y**. CAPEX **120,0 mln USD**; FOA 8 % = **9,60 mln USD/y** = 96 USD/t; o‘zgaruvchi xarajat 324 USD/t; jami 420 USD/t. Narx (model) 560 USD/t → marja 140 USD/t; yillik foyda (EBITDA) 12,11 mln USD; qaytish muddati 9,9 yil. Hajmga bog‘liqlik: 50 000 t/y → 516 USD/t; 100 000 → 420; 200 000 → 372. OPEX tuzilmasi (model): xom ashyo 42 %, energiya 26 %, xodimlar 8 %, texnik xizmat 9 %, rezerv 5 %, logistika 6 %, boshqa 4 %.

## Grafiklar (5 ta, model chizig‘i — tajriba ma’lumoti EMAS)
1. `oqim.png` / `oqim.csv` — modda oqimi: 10 bosqich bo‘ylab kirish/chiqish massalari (NH₃ 183,80 → NO/NO₂ → HNO₃ 680,00 → mahsulot 693,88 kg).
2. `bug.png` / `bug.csv` — qatnoq bug‘: 7 nuqta (p, T, h_fg) va bug‘latish entalpiyasining bosimga bog‘liqligi.
3. `issiqlik.png` / `issiqlik.csv` — jarayon harorati profili (16 nuqta: kirish 25 °C → oksidlash reaktori 880 °C → absorber/konsentrator) va qatnoq bug‘ darajalari.
4. `opex.png` / `opex.csv` — OPEX tuzilmasi (7 element, ulushlar 100 %).
5. `birlikqiymat.png` / `birlik_qiymat.csv` — birlik FOA va jami birlik narx hajmga bog‘liqligi (8 nuqta: 40 000–240 000 t/y).
Har bir grafikda «model egri chizig‘i; o‘lchov ma’lumoti emas» degan belgi bor.

## Sxemalar (7 ta, original o‘quv ishlari)
`sxematurlari.png` (sxemaning to‘rt darajasi va oqim modeli), `oqsxemasi.png` (Ostwald tipidagi zanjir: reaktor → absorber → konsentrator → azeotrop quritish), `materiallar.png` (material ierarxiyasi va korroziya mexanizmlari), `xavf.png` (xavfsizlik zonalari: inertlash, yonishdan himoya, monitoring, favqulodda holatlar), `bugtizimi.png` (bug‘ darajalari, kondenser va issiqlik integratsiyasi sxemasi), `raqamlisx.png` (DCS/soft sensor/raqamli egizin/PI darajalari), `chiqindisx.png` (chiqindi va resurs aylanmasi).

## Illyustratsiyalar (5 ta, original; mikrofoto/atom tuzilishi emas)
`oqimsx.png` (kirish–chiqish oqimini ko‘rsatuvchi sxematik chizma), `xotira.png` (operator xotirasi va ish stansiyasi sxemasi), `izchillik.png` (izchillik va traceability zanjiri), `logistikax.png` (xom ashyo va mahsulot logistikasi sxemasi), `hisob.png` (Model A mass balansi va Model B FOA hisobining blokli diagrammasi). Rang, o‘lcham va geometriya shartli.

## Cheklovlar
- Sonli egri chiziqlar, massalar, haroratlar va iqtisodiy ko‘rsatkichlar — ochiq shartli model hisoblari; real o‘lchov, reyting yoki texnologik parametr emas.
- FOA, narx, foyda va qaytish muddati — model ssenariysi; moliy ma’lumot emas.
- Qurilma, apparat parametrlari, xom ashyo nisbatlari, mahsulot narxi va amaliy tayyorlash bo‘yicha amaliyot tavsiyalari berilmadi; xavfsizlik faqat umumiy tamoyil darajasida.
- Ekologiya, sifat va raqamli boshqaruv bo‘limlari standartlar tili (ISO 9001/14001/45001, GMP, OPC UA) asosida yozilgan; kislota ishlab chiqarishga xos retsept yoki texnologik kartalar keltirilmagan.
