from book_equations import seq, var, frac, chem, par, sup, text, sub

_ka = var('K', 'a')
_kf = var('K', 'f')
_k3 = var('K', 'f')
_h = var('h', '')
_c = var('c', '')
_n = var('n', '')
_m = var('m', '')
_v = var('V', '')


def halide_equations():
    return [
      # 1 — molekula
      [seq('r(H–I) = 1,609 Å;  ', var('D', ''), '(H–I) = 295 kJ/mol'),
       seq('μ = 0,45 D;  χ(I) = 2,66;  I.E. = 10,39 eV'),
       seq('T', var('q', ''), ' :  HCl −85,1 °C  <  HBr −66,8 °C  <  HI −35,4 °C'),
       seq('pK', var('a', ''), ' (suv):  HCl −5,9  <  HBr −8,8  <  HI −9,5')],
      # 2 — fizik xossalar
      [seq('T', var('k', ''), ' = 151 °C;  ', var('p', 'k'), ' = 8,31 MPa;  ρ', var('k', ''), ' = 1,70 g/cm³'),
       seq('ρ', var('g', '25'), ' = 5,23 g/L;  d', var('g', ''), '/d', var('h', ''), ' = 4,4;  p = 7,81 atm'),
       seq('Azeotrop:  ', _m, '(HI) = 56,7 %;  T', var('q', ''), ' = 126,7 °C;  c = 7,56 mol/L'),
       seq('Eruvchanlik:  42 g/100 mL (20 °C);  234 g/100 mL (10 °C)'),
       seq(chem('ΔfH°(g) = +26,5 kJ/mol'), '   ', chem('ΔfG°(g) = +1,7 kJ/mol'))],
      # 3 — dissotsiatsiya
      [seq(chem('HI + H₂O ⇌ H₃O⁺ + I⁻'), '   ', _ka, ' ≈ 3,2×10⁹ (pK', var('a', ''), ' −9,5)'),
       seq(chem('HI + I⁻ ⇌ HI₂⁻'), '   lg', _kf, ' = 0,7 (shartli hisob)'),
       seq('zaryad:  ', _h, ' = [I⁻] + [HI₂⁻]'),
       seq('massa:  ', _c, ' = [HI] + [I⁻] + 2[HI₂⁻]'),
       seq('Taxminiy hisob: 0,100 M → pH 1,000;  7,560 M → pH −0,879;  12,000 M → pH −1,079'),
       seq('pK', var('a', ''), ' (DMSO):  HF 15;  HCl −2,0;  HBr −6,8;  HI −10,9')],
      # 4 — ishlab chiqarish
      [chem('H₂ + I₂ ⇌ 2HI'),
       seq('Taxminiy hisob: 1000 kg HI → H₂ 7,88 kg;  I₂ 992,1 kg;  Δ', var('r', ''), 'H = −9,44 kJ (2 mol HI)'),
       seq('Muvozanat:  K(298 K) = 0,254 — to‘liq konversiya kutilmaydi'),
       chem('2I₂ + N₂H₄ → 4HI + N₂'),
       seq('Taxminiy hisob: 1000 kg HI → I₂ 992,1 kg;  N₂H₄ 62,6 kg'),
       chem('3I₂ + 2P + 6H₂O → 6HI + 2H₃PO₃'),
       seq('Taxminiy hisob: I₂ 992,1 kg;  P 80,7 kg;  H₂O 140,8 kg;  H₃PO₃ 213,7 kg'),
       chem('2NaI + Cl₂ → 2NaCl + I₂'),
       seq('Taxminiy hisob: 1000 kg NaI + Cl₂ 236,5 kg → I₂ 846,6 kg + NaCl 389,9 kg')],
      # 5 — tuzlar va yod komplekslari
      [chem('M + 2HI → MI₂ + H₂↑'),
       seq(chem('AlI₃ ⇌ ½Al₂I₆'), '   (dimer)'),
       seq(chem('M²⁺ + 4I⁻ ⇌ [MI₄]²⁻'), '   (Hg, Pb, Bi, Zn)'),
       seq(chem('I₂ + I⁻ ⇌ I₃⁻'), '   lg', _k3, ' = 2,845 (K ≈ 700)'),
       seq('Taxminiy hisob: I₃⁻ ulushi 98,54 % (0,10 M) va 99,98 % (7,56 M)'),
       chem('Ag⁺ + I⁻ → AgI↓  (sariq cho‘kma)')],
      # 6 — metallar
      [chem('Fe + 2HI → FeI₂ + H₂↑'),
       chem('2Al + 6HI → 2AlI₃ + 3H₂↑'),
       chem('2Cu + O₂ + 4HI → 2CuI₂ + 2H₂O'),
       seq('Taxminiy hisob: 1 g Fe → 5,545 g FeI₂ + 4,581 g HI + 0,036 g H₂'),
       seq('1 g Al → 15,110 g AlI₃ + 14,222 g HI;  1 g Cu → 4,026 g HI + 0,252 g O₂'),
       seq('I⁻ — guruhning eng kuchli qaytaruvchisi: korroziya tezroq')],
      # 7 — redoks
      [chem('4HI + O₂ → 2I₂ + 2H₂O'),
       seq('Taxminiy hisob: 1000 kg HI → I₂ 992,1 kg;  O₂ 62,5 kg'),
       chem('6HI + 2HNO₃ → 3I₂ + 2NO + 4H₂O'),
       seq('Taxminiy hisob: 1000 kg HI → I₂ 992,1 kg;  HNO₃ 164,2 kg'),
       chem('IO₃⁻ + 5I⁻ + 6H⁺ → 3I₂ + 3H₂O'),
       seq('Qaytaruvchilik:  F⁻ < Cl⁻ < Br⁻ < I⁻'),
       chem('2HI ⇌ H₂ + I₂   (ΔfH°(g) = +26,5 kJ/mol)')],
      # 8 — organik
      [seq(chem('R–OH + HI → R–I + H₂O')),
       chem('R–CH=CH₂ + HI → R–CHI–CH₃'),
       seq(chem('CH₃I + H₂O → CH₃OH + HI'), '   — Cativa sikli, HI regeneratsiyasi'),
       seq('Nitroaromatik qaytarish:  ArNO₂ → ArNH₂ (HI + qizil fosfor)'),
       seq('Muhim mahsulotlar:  CH₃I;  metil va etil iodidlari'),
       chem('I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻')],
      # 9 — qo‘llanish
      [seq(chem('CH₃OH + CO → CH₃COOH'), '   — Cativa jarayoni, HI kofizayqin'),
       seq('Yodlangan tuz:  1 t tuz + 30 g I → 39,2 g KI yoki 50,6 g KIO₃ (shartli hisob)'),
       seq('Tibbiyot:  KI — tireotrop modda; radioaktiv holatda qalqon himoyasi'),
       seq('Kontrast moddalari; suyuq kristal ekranlari; dezinfectantlar'),
       chem('2NaI + Cl₂ → 2NaCl + I₂'),
       seq('Nazorat:  HI — AQSh (DEA) I ro‘yxatidagi modda')],
      # 10 — tahlil
      [chem('Na₂CO₃ + 2HI → 2NaI + CO₂↑ + H₂O'),
       seq('T = ', frac(_m, '(Na₂CO₃)'), ' / (2 ', _v, '(HI) · ', var('M', 'Na₂CO₃'), ')'),
       seq('Taxminiy hisob: 0,2000 g Na₂CO₃;  ', _v, '(HI) = 30,00 mL → C = 0,12580 mol/L'),
       chem('IO₃⁻ + 5I⁻ + 6H⁺ → 3I₂ + 3H₂O'),
       seq('Taxminiy hisob: 1,000 g KIO₃ → I₂ 0,712 g;  tiosulfat 0,887 g'),
       seq(chem('Ag⁺ + I⁻ → AgI↓'), '   (gravimetriya)')],
      # 11 — ishlangan hisob
      [seq('A:  1000 kg HI → H₂ 7,88 kg;  I₂ 992,1 kg;  K(298 K) = 0,254'),
       seq('B:  1000 kg NaI + Cl₂ 236,5 kg → I₂ 846,6 kg + NaCl 389,9 kg'),
       seq('C:  1 g Fe → FeI₂ 5,545 g;  HI 4,581 g;  H₂ 0,036 g'),
       seq('D:  1000 kg 10 % HI → Na₂CO₃ 41,4 kg;  NaI 117,2 kg;  CO₂ 17,2 kg'),
       seq('E:  1,000 g KIO₃ → I₂ 0,712 g;  tiosulfat 0,887 g')]
    ]
