from book_equations import seq, var, frac, chem, par, sup, text, sub

_ka = var('K', 'a')
_kp = var('K', 'sp')
_e = var('E', '°')
_dg = var('ΔG', '°')
_c = var('c', '')
_h = var('h', '')
_m = var('m', '')
_n = var('n', '')
_v = var('V', '')
_kg = var('m', '')
_pka = var('pK', 'a')


def comparison_equations():
    return [
      # 1 — guruhning umumiy ko‘rinishi
      [seq('r(H–X):  HF 0,917 Å;  HCl 1,2746 Å;  HBr 1,414 Å;  HI 1,609 Å'),
       seq('D(H–X):  569;  432;  370;  295 kJ/mol'),
       seq('χ:  F 3,98;  Cl 3,16;  Br 2,96;  I 2,66'),
       seq('μ:  1,82;  1,08;  0,82;  0,44 D'),
       seq('ΔfH°(g):  −273,3;  −92,3;  −36,3;  +26,5 kJ/mol')],
      # 2 — kislotalik
      [seq('pK', var('a', ''), ' (suv):  HF 3,17;  HCl −5,9;  HBr −8,8;  HI −9,5'),
       seq('pK', var('a', ''), ' (DMSO):  HF 15;  HCl −2,0;  HBr −6,8;  HI −10,9'),
       seq('K', var('a', ''), ' (suv):  6,8×10⁻⁴;  1,3×10⁶;  6,3×10⁸;  3,2×10⁹'),
       seq('ΔH', var('acid', ''), ' (gaz fazi):  1555;  1395;  1349;  1313 kJ/mol'),
       seq('Tartib (kuchli → kuchsiz):  HI > HBr > HCl > HF')],
      # 3 — fizik xossalar
      [seq('T', var('b', ''), ':  HF 19,5 °C;  HCl −85,1 °C;  HBr −66,8 °C;  HI −35,4 °C'),
       seq('T', var('m', ''), ':  HF −83,6 °C;  HCl −114,2 °C;  HBr −86,9 °C;  HI −50,8 °C'),
       seq('Azeotrop:  HF 37,0 %;  HCl 20,2 %;  HBr 47,6 %;  HI 56,9 %'),
       seq('Taxminiy hisob:  ', _c, ' = w·ρ/M  →  21,27;  6,11;  8,77;  7,56 mol/L'),
       seq('Taxminiy hisob: 1 L azeotrop —  426,0;  222,8;  710,0;  965,2 g')],
      # 4 — suvli eritmalar
      [seq(chem('HF + H₂O ⇌ H₃O⁺ + F⁻'), '   ', _ka, ' = 6,8×10⁻⁴'),
       seq(frac(_h, _h), '² / (', _c, ' − ', _h, ') = ', _ka),
       seq('Taxminiy hisob: 0,010 M → ', _h, ' = 0,002290 M;  pH 2,640;  α = 22,90 %'),
       seq('Taxminiy hisob: 0,100 M → ', _h, ' = 0,007913 M;  pH 2,102;  α = 7,91 %'),
       seq('Taxminiy hisob: 1,000 M → ', _h, ' = 0,025739 M;  pH 1,589;  α = 2,57 %'),
       seq('HCl, HBr, HI:  ', _h, ' ≈ ', _c, ';  pH = −lg ', _c, ' (taxminiy hisob)')],
      # 5 — metallarga ta’sir
      [chem('M + 2HX → MX₂ + H₂↑'),
       seq('Taxminiy hisob: 1 g Fe → kislota  HF 0,716 g;  HCl 1,306 g;  HBr 2,898 g;  HI 4,581 g'),
       seq('Taxminiy hisob: 1 g Fe → tuz  FeF₂ 1,680 g;  FeCl₂ 2,270 g;  FeBr₂ 3,861 g;  FeI₂ 5,545 g'),
       seq('Taxminiy hisob: 1 g Fe → H₂ 0,036 g — barcha kislotalarda bir xil'),
       chem('CaCO₃ + 2HF → CaF₂↓ + CO₂↑ + H₂O'),
       seq('Passivatsiya: faqat HF da (FeF₃ va CaF₂ qatlami)')],
      # 6 — redoks
      [seq('E', var('°', ''), '(X₂/2X⁻):  F 2,87 V;  Cl 1,36 V;  Br 1,07 V;  I 0,54 V'),
       seq('Qaytaruvchilik:  F⁻ < Cl⁻ < Br⁻ < I⁻'),
       seq('Taxminiy hisob: 1000 kg kislota → Cl₂ 972,4 kg;  Br₂ 987,5 kg;  I₂ 992,1 kg'),
       chem('4HI + O₂ → 2I₂ + 2H₂O'),
       seq('Taxminiy hisob: 1000 kg HI → I₂ 992,1 kg;  O₂ 62,5 kg'),
       seq('2HX ⇌ H₂ + X₂:  ΔG° = +550,8;  +190,6;  +110,0;  +15,9 kJ/mol')],
      # 7 — tuzlar va komplekslar
      [seq('Ag', var('X', ''), ' ⇌ Ag⁺ + X⁻;   ', _kp, ' = [Ag⁺][X⁻]'),
       seq('K', var('sp', ''), ':  AgCl 1,8×10⁻¹⁰;  AgBr 5,4×10⁻¹³;  AgI 8,3×10⁻¹⁷'),
       seq('K', var('sp', ''), ':  CaF₂ 3,9×10⁻¹¹;  BaF₂ 1,7×10⁻⁶;  PbF₂ 3,7×10⁻⁸'),
       seq('AgF — yaxshi eriydi: ≈1,8 kg/L (20 °C)'),
       seq(chem('M²⁺ + nX⁻ ⇌ [MX'), var('n', ''), ']'),
       seq('Ligandlik:  F⁻ < Cl⁻ < Br⁻ < I⁻')],
      # 8 — organik
      [chem('R–OH + HX → R–X + H₂O'),
       seq('Tartib:  HI > HBr > HCl >> HF'),
       chem('R–O–R′ + HX → R–X + R′–OH'),
       chem('R–CH=CH₂ + HI → R–CHI–CH₃'),
       seq('Nitroaromatik qaytarish:  ArNO₂ → ArNH₂ (HI + qizil fosfor)'),
       seq(chem('CH₃OH + CO → CH₃COOH'), '   — Cativa sikli, HI katalizator')],
      # 9 — tahlil usullari
      [chem('Na₂CO₃ + 2HX → 2NaX + CO₂↑ + H₂O'),
       seq('T = ', frac(_m, '(Na₂CO₃)'), ' / (2 ', _v, '(HX)·', var('M', 'Na₂CO₃'), ')'),
       chem('Ag⁺ + X⁻ → AgX↓'),
       chem('IO₃⁻ + 5I⁻ + 6H⁺ → 3I₂ + 3H₂O'),
       seq('Taxminiy hisob: 1,000 g KIO₃ → I₂ 0,712 g;  tiosulfat 0,887 g'),
       seq('Ion-elektrod va ICP-OES / ICP-MS:  F, Cl, Br, I')],
      # 10 — xavfsizlik va ekvivalent
      [seq('HF:  OSHA TWA 3 ppm;  ACGIH 0,5 ppm;  IDLH 30 ppm'),
       seq('HCl:  OSHA 5 ppm;  ACGIH 2,98 ppm;  IDLH 50 ppm (tarixiy)'),
       seq('HBr:  OSHA 3 ppm;  ACGIH 2 ppm;  IDLH 35 ppm (116 mg/m³)'),
       seq('HI:  ACGIH 0,01 ppm;  IDLH 35 ppm (183 mg/m³);  AEGL 1 / 150 / 740 ppm'),
       seq('Ekvivalent:  n(H⁺) = ', _m, '/M  →  49,985;  27,427;  12,359;  7,818 mol/kg')],
      # 11 — xulosa va ishlangan hisob
      [seq('A (metall):  1 g Fe → HF 0,716 g;  HCl 1,306 g;  HBr 2,898 g;  HI 4,581 g'),
       seq('B (neytralizatsiya):  1000 kg 10 % li eritma + Na₂CO₃'),
       seq('B:  HF 264,9 kg;  HCl 145,3 kg;  HBr 65,5 kg;  HI 41,4 kg (kirish = chiqish)'),
       seq('C (ekvivalent):  H⁺ 49,985;  27,427;  12,359;  7,818 mol/kg'),
       seq('D (halogen):  1000 kg kislota → Cl₂ 972,4;  Br₂ 987,5;  I₂ 992,1 kg;  HF uchun 0'),
       seq('E (eritma):  0,100 M → pH: HF 2,102;  HCl/HBr/HI 1,000')],
    ]
