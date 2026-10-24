from book_equations import seq, var, frac, chem, par, sup, text, sub

_ka1 = var('K', 'a1')
_ka2 = var('K', 'a2')
_kb = var('K', 'b')
_ksp = var('K', 'sp')
_e = var('E', '°')
_h = var('h', '')
_c = var('c', '')
_m = var('m', '')
_n = var('n', '')
_v = var('V', '')
_pka = var('pK', 'a')
_s2 = var('[S', '2−]')
_h2s = var('[H', '2S]')
_ppm = var('C', '')
_i2 = var('I', '2')


def h2s_equations():
    return [
      # 1 — umumiy tavsif
      [seq('M(H₂S) = 34,081 g/mol;  CAS 7783-06-4;  UN 1053'),
       seq('ρ(H₂S) = 1,539 g/L (0 °C)  /  1,39 g/L (25 °C)  →  havo ostida ~1,2 marta og‘ir'),
       seq('1 ppm ≈ 1,40 mg/m³'),
       seq('Oltinugurt zanjiri:  H₂S → SO₂ → S → H₂SO₄'),
       seq('Taxminiy hisob: 1000 kg H₂S → 940,7 kg S (Claus usuli)')],
      # 2 — molekula tuzilishi
      [seq('H–S–H:  r = 1,3356 Å;  ∠H–S–H = 92,11°;  C₂ᵥ'),
       seq('D(H–S) ≈ 347 kJ/mol;  μ = 0,97 D;  IE = 10,46 eV'),
       seq('PA(H₂S) = 705 kJ/mol'),
       seq('Taxminiy hisob: molekulalar orasidagi ta’sir < 2 kJ/mol'),
       seq('IR:  δ = 1183 cm⁻¹;  ν = 2615–2626 cm⁻¹'),
       seq('ΔfH°(g) = −20,6 kJ/mol;  ΔfG° = −37,28 kJ/mol;  S° = 205,81 J/(mol·K)')],
      # 3 — agregat holatlari
      [seq('Tf = 190,85 K (−82,3 °C);  Tb = 212,87 K (−60,28 °C)'),
       seq('Tc = 373,3 K;  Pc = 89,63 bar;  ', var('ρ', 'c'), ' = 10,2 mol/L'),
       seq('ΔvapH ≈ 19,5 kJ/mol (200 K)'),
       seq('ln(p₂/p₁) = −(ΔvapH/R)·(1/T₂ − 1/T₁)'),
       seq('Taxminiy hisob: p(25 °C) = 23,68 bar — jadvaldagi 20,80 bar dan 13,8 % yuqori')],
      # 4 — eruvchanlik
      [seq('S(20 °C) = 3,98 g/L  →  c = ', _c, ' = 0,1168 mol/L'),
       seq('Taxminiy hisob: ', _h, ' = √(', _ka1, '·', _c, ') = 1,03×10⁻⁴ mol/L;  pH = 3,99'),
       seq('Henry:  H = ', frac('p', _c), ' ≈ 17 800 kPa·L/mol'),
       seq('Suvning protoni kuchli:  H₂S + H₂O ⇌ HS⁻ + H₃O⁺')],
      # 5 — kislotalik
      [seq(chem('H₂S + H₂O ⇌ HS⁻ + H₃O⁺'), '   ', _ka1, ' = 9,1×10⁻⁸  (pK', sub('a', '1'), ' = 7,04)'),
       seq(chem('HS⁻ + H₂O ⇌ S²⁻ + H₃O⁺'), '   ', _ka2, ' ≈ 1,2×10⁻¹²  (pK', sub('a', '2'), ' = 11,96)'),
       seq(chem('S²⁻ + H₂O ⇌ HS⁻ + OH⁻'), '   ', _kb, ' = ', var('K', 'w'), '/', _ka2, ' ≈ 8,3×10⁻³'),
       seq('Taxminiy hisob (pH 7,4):  H₂S 30,4 %;  HS⁻ 69,6 %;  S²⁻ 0,0021 %'),
       seq('Taxminiy hisob (pH 10):  HS⁻ 98,7 %;  S²⁻ 1,18 %')],
      # 6 — hosilalish
      [seq(chem('FeS + 2HCl → FeCl₂ + H₂S↑')),
       seq(chem('Al₂S₃ + 6H₂O → 2Al(OH)₃ + 3H₂S↑')),
       seq(chem('H₂ + S → H₂S')),
       seq('Sanoat: absorber + stripper → “acid gas” (H₂S 82,1 mol% yoki 26,7 mol%)'),
       seq('Tabiiy:  SO₄²⁻ → S²⁻ (bakterial sulfat-reduksiya, anaerob sharoit)')],
      # 7 — redoks
      [seq(chem('2H₂S + 3O₂ → 2SO₂ + 2H₂O'), '   (ΔH ≈ −518 kJ/mol)'),
       seq(chem('2H₂S + O₂ → 2S + 2H₂O')),
       seq(chem('H₂S + I₂ → S↓ + 2HI')),
       seq('E', _e, '(S + 2H⁺ + 2e⁻ ⇌ H₂S) = +0,14 V;   E', _e, '(S + 2e⁻ ⇌ S²⁻) = −0,407 V'),
       seq(chem('2H₂S + SO₂ ⇌ 3S + 2H₂O'), '   (ΔH ≈ −1165,6 kJ/mol)')],
      # 8 — metall sulfidlar
      [seq('M²⁺ + H₂S → MS↓ + 2H⁺'),
       seq(_ksp, ' = [M²⁺][S²⁻]'),
       seq('Ksp:  ZnS 2,0×10⁻²⁵;  PbS 3,2×10⁻²⁸;  CuS 7,9×10⁻³⁷;  HgS 2×10⁻⁵³'),
       seq('Taxminiy hisob:  ', _s2, ' = ', _ka1, '·', _ka2, '·', _h2s, '/[H⁺]²'),
       seq('Taxminiy hisob:  pH 1 → [S²⁻] = 1,09×10⁻¹⁸;  pH 7 → 1,09×10⁻⁶ mol/L')],
      # 9 — xavfsizlik
      [seq('OSHA: 20 ppm (yuqori chegar; 50 ppm — 10 daqiqa);  NIOSH REL: 10 ppm'),
       seq('ACGIH: TWA 1 ppm, STEL 5 ppm;  IDLH 100 ppm'),
       seq('ERPG 0,1 / 30 / 100 ppm;  PAC 0,51 / 27 / 50 ppm'),
       seq('Taxminiy hisob: m = ', _ppm, '·1,40 mg/m³·', _v),
       seq('Taxminiy hisob: 1 m³ da 20 ppm → 28 mg;  100 ppm → 140 mg')],
      # 10 — sanoat
      [seq(chem('2H₂S + 3O₂ → 2SO₂ + 2H₂O'), '   (termik bosqich, 1/3 H₂S)'),
       seq(chem('2H₂S + SO₂ ⇌ 3S + 2H₂O'), '   (katalitik bosqich, Al₂O₃)'),
       seq('T:  1-bosqich 315–330 °C;  2-bosqich ~240 °C;  3-bosqich ~200 °C'),
       seq('Qaytarish:  3 qatlam 95–96 %;  chegara 97–98 %;  qoldiq gaz 0,8–1,5 %'),
       seq('Taxminiy hisob: 1000 kg H₂S → S 940,7 kg;  H₂O 528,6 kg;  O₂ 469,4 kg')],
      # 11 — xulosa va ishlangan hisob
      [seq('A (yodometriya):  H₂S + I₂ → S + 2HI'),
       seq('A: 0,0500 M × 100,0 mL → 0,00500 mol;  I₂ 1,2690 g;  Na₂S₂O₃ 2,4818 g'),
       seq('B (cho‘qma):  ', _s2, ' = ', _ka1, '·', _ka2, '·', _h2s, '/[H⁺]² → PbS chegarasi'),
       seq('C (Claus):  1000 kg H₂S → S 940,7 kg;  H₂O 528,6 kg;  O₂ 469,4 kg'),
       seq('D (neytralizatsiya):  1000 kg 10 % li eritma → NaOH 117,4 / 234,7 kg'),
       seq('E (ekvivalent):  34,081/2 = 17,041 g/eq;  1 kg da 58,680 mol H⁺ ekvivalenti')],
    ]
