from book_equations import seq, var, frac, chem, par, sup, text, sub

_ka1 = var('K', 'a1')
_ka2 = var('K', 'a2')
_kb = var('K', 'b')
_kw = var('K', 'w')
_e = var('E', '°')
_h = var('h', '')
_c = var('c', '')
_n = var('n', '')
_v = var('V', '')
_pka = var('pK', 'a')
_so3 = var('[SO', '3²−]')
_hso3 = var('[HSO', '3−]')
_so2 = var('[SO', '2(aq)]')
_ppm = var('C', '')
_kh = var('k', 'H')


def sulfite_equations():
    return [
      # 1 — umumiy tavsif
      [seq('H₂SO₃: 82,08 g/mol;  S — +IV daraja;  SO₂ — UN 1079'),
       seq('H₂SO₃ ⇌ SO₂ + H₂O   (κ ≪ 10⁻⁹)'),
       seq(chem('S + O₂ → SO₂'), '   ;   ', chem('4FeS₂ + 11O₂ → 2Fe₂O₃ + 8SO₂')),
       seq('Taxminiy hisob:  1000 kg 10 % li eritma → 100 kg SO₂ = 1,5610 kmol')],
      # 2 — tuzilish va spektroskopiya
      [seq('SO₂:  burchak 119,47°;  r(S=O) = 143,10 pm;  μ = 1,63 D'),
       seq('SO₃²⁻:  piramida, ∠O–S–O = 106°;  r(S–O) = 151 pm'),
       seq('HSO₃⁻:  H–SO₃⁻ (', var('C', 's'), ');  [H–OSO₂]⁻ ⇌ [H–SO₃]⁻'),
       seq('ΔfH°(g) = −296,81 kJ/mol;  ΔfG° = −300,09 kJ/mol;  S° = 248,223 J/(mol·K)'),
       seq('Gidratatsiya:  ΔfH = −608,62 − (−322,82) = −285,8 kJ/mol')],
      # 3 — agregat holatlari
      [seq('Tf = 200,75 K (−72,4 °C);  Tb = 263,15 K (−10,0 °C)'),
       seq('Tc = 430,80 K;  Pc = 78,79 bar;  ρ(suyuq) = 1,434 g/mL'),
       seq('ΔvapH = 24,90 kJ/mol'),
       seq('ln(p₂/p₁) = −(ΔvapH/R)·(1/T₂ − 1/T₁)'),
       seq('Taxminiy hisob: p(25 °C) = 3,85 bar — jadval interpolatsiyasi 3,85 bar (farq 0,01 %)')],
      # 4 — eruvchanlik
      [seq('S(25 °C) = 94 g/L  →  ', _c, ' = 1,4674 mol/L'),
       seq('Henry:  ', _c, ' = ', _kh, '·p;  ', _kh, ' = 1,242 mol/(L·atm);  H = ',
           frac('p', _c), ' = 0,805 atm·L/mol'),
       seq('Taxminiy hisob: ', _h, ' = 0,1428 mol/L;  pH = 0,845;  α = 9,7 %'),
       seq('Klathrat:  4SO₂·23H₂O   (7 °C dan yuqorida buziladi)')],
      # 5 — kislotalik
      [seq(chem('SO₂(aq) + H₂O ⇌ H⁺ + HSO₃⁻'), '   ', _ka1, ' = 1,54×10⁻²  (pK',
           sub('a', '1'), ' = 1,81)'),
       seq(chem('HSO₃⁻ ⇌ H⁺ + SO₃²⁻'), '   ', _ka2, ' = 6,3×10⁻⁸  (pK',
           sub('a', '2'), ' = 7,2)'),
       seq(chem('SO₃²⁻ + H₂O ⇌ HSO₃⁻ + OH⁻'), '   ', _kb, ' = ', _kw, '/', _ka2, ' = 1,59×10⁻⁷'),
       seq('Taxminiy hisob (pH 2):  SO₂(aq) 39,4 %;  HSO₃⁻ 60,6 %'),
       seq('Taxminiy hisob (pH 7):  HSO₃⁻ 61,3 %;  SO₃²⁻ 38,7 %')],
      # 6 — hosilalish
      [seq(chem('Na₂SO₃ + 2HCl → 2NaCl + H₂O + SO₂↑')),
       seq(chem('SO₂ + NaOH → NaHSO₃')),
       seq(chem('2NaHSO₃ + Na₂CO₃ → 2Na₂SO₃ + H₂O + CO₂↑')),
       seq(chem('2NaHSO₃ → Na₂S₂O₅ + H₂O')),
       seq('Tabiiy:  H₂S + SO₂ + suv → polissulfidlar (Sₙ²⁻)')],
      # 7 — redoks xossalari
      [seq(chem('2SO₂ + O₂ → 2SO₃')),
       seq(chem('H₂SO₃ + I₂ + H₂O → H₂SO₄ + 2HI')),
       seq(chem('2H₂S + H₂SO₃ → 3S + 2H₂O')),
       seq('Latimer:  SO₄²⁻ (+0,17 V) → SO₂ (+0,45 V) → S (+0,14 V) → H₂S'),
       seq('Bisulfit + aldehyd ⇌ α-gidroksisulfonat   (K = 10²–10⁶ M⁻¹)')],
      # 8 — tuzlar
      [seq(chem('Na₂S₂O₅ + H₂O → 2Na⁺ + 2HSO₃⁻')),
       seq('SO₂ mazmuni:  Na₂SO₃ 50,8 %;  NaHSO₃ 61,6 %;  Na₂S₂O₅ 67,4 %'),
       seq(var('K', 'b'), '(SO₃²⁻) = 1,59×10⁻⁷  →  Na₂SO₃ eritmasi alkalik'),
       seq('Taxminiy hisob:  1000 kg 10 % li eritma → Na₂S₂O₅ 148,4 kg')],
      # 9 — tahlil usullari
      [seq(chem('SO₃²⁻ + I₂ + H₂O → SO₄²⁻ + 2I⁻ + 2H⁺')),
       seq('Taxminiy hisob:  25,00 mL × 0,1000 M → ', _n, ' = 0,002500 mol'),
       seq('I₂ 0,6345 g;  Na₂S₂O₃ 1,2409 g'),
       seq('West–Gaeke:  SO₂ + pararosanilin + formaldehid → qizil-binafsha kompleks, 560 nm')],
      # 10 — xavfsizlik
      [seq('OSHA 5 ppm (TWA);  NIOSH 2/5 ppm;  ACGIH STEL 0,25 ppm;  IDLH 100 ppm'),
       seq('ERPG 0,3 / 3 / 25 ppm;  AEGL 0,2 / 0,75 / 30 ppm;  PAC 0,2 / 0,75 / 30 ppm'),
       seq('Taxminiy hisob:  1 ppm ≈ 2,62 mg/m³'),
       seq('Taxminiy hisob:  1 m³ da 5 ppm → 13,1 mg;  100 ppm → 262 mg')],
      # 11 — xulosa va ishlangan hisob
      [seq('A (kislotalik):  0,100 M → ', _h, ' = 0,03229 M;  pH = 1,49;  α = 32,3 %'),
       seq('B (spetsiatsiya):  pH 2 → 39,4 / 60,6 %;  pH 7 → 61,3 / 38,7 %'),
       seq('C (yodometriya):  25,00 mL 0,1000 M Na₂SO₃ → 0,002500 mol;  I₂ 0,6345 g'),
       seq('D (neytralizatsiya):  NaOH 62,4 / 124,9 kg;  Ca(OH)₂ 115,7 kg;  Na₂S₂O₅ 148,4 kg'),
       seq('E (kontakt):  1000 kg SO₂ → SO₃ 1249,8 kg;  O₂ 249,8 kg;  H₂SO₄ 1531,1 kg'),
       seq('F (ekvivalent):  ', frac('82,08', '2'), ' = 41,04 g/eq;  ',
           frac('64,06', '2'), ' = 32,03 g/eq')],
    ]
