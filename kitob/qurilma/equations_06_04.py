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
      [seq('r(H–Br) = 1,4144 Å;  ', var('D', ''), '(H–Br) = 366 kJ/mol'),
       seq('μ = 0,8272 D;  χ(Br) = 2,96;  I.E. = 11,66 eV'),
       seq('T', var('q', ''), ' :  HCl −85,1 °C  <  HBr −66,8 °C  <  HI −35,4 °C'),
       seq('pK', var('a', ''), ' (suv):  HCl −5,9  <  HBr −8,8  <  HI −9,5')],
      # 2 — fizik xossalar
      [seq('T', var('k', ''), ' = 89,8 °C;  ', var('p', 'k'), ' = 85,0 bar;  ρ', var('k', ''), ' = 807 kg/m³'),
       seq('ρ', var('g', '25'), ' = 3,307 g/L;  d', var('g', ''), '/d', var('h', ''), ' = 2,71'),
       seq('Azeotrop:  ', _m, '(HBr) = 47,6 %;  T', var('q', ''), ' = 124,3 °C;  c = 8,77 mol/L'),
       seq('Eruvchanlik:  221 / 204 / 130 g/100 mL  (0 / 15 / 100 °C)'),
       chem('HBr·nH₂O,  n = 1, 2, 3, 4, 6')],
      # 3 — dissotsiatsiya
      [seq(chem('HBr + H₂O ⇌ H₃O⁺ + Br⁻'), '   ', _ka, ' ≈ 6,3×10⁸ (pK', var('a', ''), ' −8,8)'),
       seq(chem('HBr + Br⁻ ⇌ HBr₂⁻'), '   lg', _kf, ' = 0,7 (shartli hisob)'),
       seq('zaryad:  ', _h, ' = [Br⁻] + [HBr₂⁻]'),
       seq('massa:  ', _c, ' = [HBr] + [Br⁻] + 2[HBr₂⁻]'),
       seq('Taxminiy hisob: 0,100 M → pH 1,000;  8,770 M → pH −0,943;  12,000 M → pH −1,079'),
       seq('pK', var('a', ''), ' (DMSO):  HF 15;  HCl −2,0;  HBr −6,8;  HI −10,9')],
      # 4 — ishlab chiqarish
      [chem('H₂ + Br₂ → 2HBr'),
       seq('Taxminiy hisob: 1000 kg HBr → H₂ 12,46 kg;  Br₂ 987,5 kg;  Δ', var('r', ''), 'H = −639,5 MJ'),
       chem('Br₂ + SO₂ + 2H₂O → H₂SO₄ + 2HBr'),
       seq('Taxminiy hisob: Br₂ 987,5 kg;  SO₂ 395,9 kg;  H₂SO₄ 606,1 kg'),
       chem('H₂SO₄ + KBr → KHSO₄ + HBr'), seq('unum ≈ 85 %;  > 75 °C da HBr oksidlanadi'),
       chem('2NaBr + Cl₂ → 2NaCl + Br₂'),
       seq('Taxminiy hisob: 1000 kg NaBr + Cl₂ 344,6 kg → Br₂ 776,6 kg + NaCl 568,0 kg')],
      # 5 — tuzlar va bromokomplekslar
      [chem('M + 2HBr → MBr₂ + H₂↑'),
       seq(chem('AlBr₃ ⇌ ½Al₂Br₆'), '   (dimer)'),
       seq(chem('M²⁺ + 4Br⁻ ⇌ [MBr₄]²⁻'), '   (Cu, Co, Zn, Pd)'),
       seq(chem('Br₂ + Br⁻ ⇌ Br₃⁻'), '   lg', _k3, ' = 1,2 (shartli hisob)'),
       seq('Taxminiy hisob: Br₃⁻ ulushi 60,40 % (0,10 M) va 99,29 % (8,77 M)')],
      # 6 — metallar
      [chem('Fe + 2HBr → FeBr₂ + H₂↑'),
       chem('2Al + 6HBr → 2AlBr₃ + 3H₂↑'),
       chem('2Cu + O₂ + 4HBr → 2CuBr₂ + 2H₂O'),
       seq('Taxminiy hisob: 1 g Fe → 3,862 g FeBr₂ + 2,898 g HBr + 0,036 g H₂'),
       seq('1 g Al → 9,884 g AlBr₃ + 8,996 g HBr;  1 g Cu → 2,547 g HBr + 0,252 g O₂'),
       chem('Ag⁺ + Br⁻ → AgBr↓  (och sariq cho‘kma)')],
      # 7 — redoks
      [chem('4HBr + O₂ → 2Br₂ + 2H₂O'),
       seq('Taxminiy hisob: 1000 kg HBr → Br₂ 987,5 kg;  O₂ 98,9 kg'),
       chem('2HBr + H₂O₂ → Br₂ + 2H₂O'),
       seq('Taxminiy hisob: 1000 kg HBr → H₂O₂ 210,2 kg;  Br₂ 987,5 kg'),
       chem('2NaBr + Cl₂ → 2NaCl + Br₂'),
       seq('Qaytaruvchilik:  F⁻ < Cl⁻ < Br⁻ < I⁻'),
       chem('O₃ + 2Br⁻ + H₂O → Br₂ + O₂ + 2OH⁻')],
      # 8 — organik
      [seq(chem('R–OH + HBr → R–Br + H₂O')),
       chem('R–CH=CH₂ + HBr → R–CHBr–CH₃'),
       seq('peroksidlar ishtirokida:  R–CH=CH₂ + HBr → R–CH₂–CH₂Br'),
       chem('2ArH + 2HBr + H₂O₂ → 2ArBr + 2H₂O'),
       seq('Muhim mahsulotlar:  allil bromid;  tetrabromobisfenol A;  CH₃Br (ODP 0,6)')],
      # 9 — qo‘llanish
      [chem('AgNO₃ + HBr → AgBr↓ + HNO₃'),
       seq(chem('Pd + 2HBr + ½O₂ → PdBr₂ + H₂O'), '   (HBr muhitida)'),
       seq(chem('Pd²⁺ + 4Br⁻ ⇌ [PdBr₄]²⁻'), '   — noble metall eritiladi'),
       chem('2NaBr + Cl₂ → 2NaCl + Br₂'),
       seq('Fotografiya: AgBr — yorug‘likka sezgir qatlam;  dori: KBr, NaBr')],
      # 10 — tahlil
      [chem('Na₂CO₃ + 2HBr → 2NaBr + CO₂↑ + H₂O'),
       seq('T = ', frac(_m, '(Na₂CO₃)'), ' / (2 ', _v, '(HBr) · ', var('M', 'Na₂CO₃'), ')'),
       seq('Taxminiy hisob: 0,2000 g Na₂CO₃;  ', _v, '(HBr) = 30,00 mL → C = 0,12580 mol/L'),
       chem('Ag⁺ + Br⁻ → AgBr↓  (gravimetriya)'),
       seq(chem('NH₃ + HBr → NH₄Br'), '   (Kjeldahl — qayta titrlash)')],
      # 11 — ishlangan hisob
      [seq('A:  1000 kg HBr → H₂ 12,46 kg;  Br₂ 987,5 kg;  Δ', var('r', ''), 'H −639,5 MJ'),
       seq('B:  1000 kg NaBr + Cl₂ 344,6 kg → Br₂ 776,6 kg + NaCl 568,0 kg'),
       seq('C:  1 g Fe → FeBr₂ 3,862 g;  HBr 2,898 g;  H₂ 0,036 g'),
       seq('D:  1000 kg 10 % HBr → Na₂CO₃ 65,5 kg;  NaBr 127,2 kg;  CO₂ 27,2 kg'),
       seq('E:  1000 kg HBr + H₂O₂ 210,2 kg → Br₂ 987,5 kg')]
    ]
