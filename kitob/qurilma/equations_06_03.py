from book_equations import seq, var, frac, chem, par, sup, text, sub

_ka = var('K', 'a')
_kf = var('K', 'f')
_h = var('h', '')
_c = var('c', '')
_n = var('n', '')
_m = var('m', '')
_v = var('V', '')
_dg = var('ΔG', '°')


def halide_equations():
    return [
      # 1 — molekula
      [seq('r(H–Cl) = 1,2746 Å;  ', var('D', ''), '(H–Cl) = 432 kJ/mol'),
       seq('μ = 1,08 D;  χ(Cl) = 3,16;  Δχ(H–Cl) = 0,96'),
       seq(chem('H–Cl···Cl–H'), '   (dipol–dipol, vodorod bog‘i yo‘q)'),
       seq('T', var('q', ''), ' :  HCl −85,1 °C  <  HBr −66,8 °C  <  HI −35,4 °C')],
      # 2 — fizik xossalar
      [seq('T', var('k', ''), ' = 51,4 °C;  ', var('p', 'k'), ' = 83,1 bar;  ρ', var('k', ''), ' = 450 kg/m³'),
       seq('Azeotrop:  ', _m, '(HCl) = 20,2 %;  T', var('q', ''), ' = 108,6 °C'),
       chem('[H₃O]Cl 68 %;  [H₅O₂]Cl 51 %;  [H₇O₃]Cl 41 %'),
       seq(chem('HCl(g) ⇌ HCl(aq)'), '   eruvchanlik 720 g/L (20 °C)')],
      # 3 — dissotsiatsiya
      [seq(chem('HCl + H₂O ⇌ H₃O⁺ + Cl⁻'), '   ', _ka, ' ≈ 7,9×10⁵ (pK', var('a', ''), ' −5,9)'),
       seq(chem('HCl + Cl⁻ ⇌ HCl₂⁻'), '   lg', _kf, ' = 0,7 (model)'),
       seq('zaryad:  ', _h, ' = [Cl⁻] + [HCl₂⁻]'),
       seq('massa:  ', _c, ' = [HCl] + [Cl⁻] + 2[HCl₂⁻]'),
       seq('Model: 0,100 M → pH 1,000;  12,000 M → pH −1,079, HCl₂⁻ 0,09 %')],
      # 4 — ishlab chiqarish
      [chem('2NaCl + H₂SO₄ → Na₂SO₄ + 2HCl↑'),
       seq(_n, '(NaCl) = ', _n, '(HCl);  ', _n, '(H₂SO₄) = ½ ', _n, '(HCl)'),
       seq('Model: 1000 kg HCl → NaCl 1602,8 kg;  H₂SO₄ 1345,0 kg;  Na₂SO₄ 1947,8 kg'),
       chem('H₂ + Cl₂ → 2HCl'),
       seq('Model: 1000 kg HCl → H₂ 27,6 kg;  Cl₂ 972,4 kg;  Δ', var('r', ''), 'H = −2531,7 MJ')],
      # 5 — tuzlar va komplekslar
      [chem('M + 2HCl → MCl₂ + H₂↑'),
       chem('MCO₃ + 2HCl → MCl₂ + CO₂↑ + H₂O'),
       seq(chem('M³⁺ + 4Cl⁻ ⇌ [MCl₄]⁻'), '   (Cu, Co, Fe, Zn)'),
       seq(chem('Al³⁺ + 6H₂O ⇌ [Al(H₂O)₆]³⁺'), '   → kislota muhiti')],
      # 6 — metallar
      [chem('Fe + 2HCl → FeCl₂ + H₂↑'),
       chem('2Al + 6HCl → 2AlCl₃ + 3H₂↑'),
       chem('2Cu + O₂ + 4HCl → 2CuCl₂ + 2H₂O'),
       seq('Model: 1 g Fe → 2,270 g FeCl₂ + 1,306 g HCl + 0,036 g H₂'),
       seq('Model: 1 g Cu → 1,148 g HCl + 0,252 g O₂ (havo ishtirokida)')],
      # 7 — pickling va tiklash
      [seq('1 t po‘lat:  ', _m, '(HCl) = 7,6 kg;  ', _m, '(Fe) = 5,8 kg;  ', _m, '(Cl⁻) = 7,4 kg'),
       chem('4FeCl₂ + 4H₂O + O₂ → 2Fe₂O₃ + 8HCl↑'),
       seq('Model: 1000 kg FeCl₂ → Fe₂O₃ 629,9 kg;  HCl 575,3 kg'),
       seq('Model: kirish 1205,2 kg ≈ chiqish 1205,2 kg'),
       chem('12FeCl₂ + 3O₂ → 8FeCl₃ + 2Fe₂O₃'), chem('2FeCl₃ + 3H₂O → 6HCl + Fe₂O₃')],
      # 8 — suvsiz muhit
      [seq(chem('HCl + CH₃OH → [CH₃OH₂]⁺ + Cl⁻'), '   (suvsiz dissotsiatsiya)'),
       seq('H', var('0', ''), ' (HCl/NaCl/AlCl₃) = −11,3;  (HCl/LiCl/AlCl₃) = −12,7'),
       seq('H', var('0', ''), ' (1 atm HCl, to‘yingan eritma) ≈ −18'),
       seq('Taqqoslash:  H', var('0', ''), ' (suyuq HF) = −15,1')],
      # 9 — qo‘llanish
      [chem('C₂H₂ + HCl → CH₂=CHCl (VCM)'),
       seq(chem('Cl₂ + H₂O ⇌ HCl + HOCl'), '   (dezinfektsiya ta’siri HOCl da)'),
       chem('MCO₃ + 2HCl → MCl₂ + CO₂ + H₂O'),
       seq('Ion almashinuv:  R–SO₃H + H⁺ → R–SO₃⁻ + H⁺ (kationit tiklash)')],
      # 10 — tahlil
      [chem('Na₂CO₃ + 2HCl → 2NaCl + CO₂↑ + H₂O'),
       seq('T = ', frac(_m, '(Na₂CO₃)'), ' / (2 ', _v, '(HCl) · ', var('M', 'Na₂CO₃'), ')'),
       seq('Model: 0,2500 g Na₂CO₃;  ', _v, '(HCl) = 24,85 mL → C = 0,18984 mol/L'),
       chem('Ag⁺ + Cl⁻ → AgCl↓'),
       seq(chem('NH₃ + HCl → NH₄Cl'), '   (Kjeldahl — qayta titrlash)')],
      # 11 — ishlangan hisob
      [seq('A:  1000 kg HCl → NaCl 1602,8 kg;  H₂SO₄ 1345,0 kg;  Na₂SO₄ 1947,8 kg'),
       seq('B:  1000 kg 10 % HCl → Na₂CO₃ 145,3 kg;  NaCl 160,3 kg;  CO₂ 60,4 kg'),
       seq('C:  1 g Fe → FeCl₂ 2,270 g;  HCl 1,306 g;  H₂ 0,036 g'),
       seq('D:  1000 kg FeCl₂ → Fe₂O₃ 629,9 kg;  HCl 575,3 kg')]
    ]
