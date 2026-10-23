from book_equations import seq, var, frac, chem, par, sup, text, sub

_chi = var('χ', 'X')
_r = var('r', 'H–X')
_pka = var('pK', 'a')
_ka = var('K', 'a')
_x = var('x', '')
_c = var('c', '')
_dg = var('ΔG', '°')
_kt = var('K', '')
_dh = var('ΔH', 'hyd')
_d = var('D', 'H–X')
_m = var('m', '')
_n = var('n', '')


def halide_equations():
    return [
      # 1 — guruhning umumiy o'lchamlari
      [seq(_chi, ' = ', var('χ', 'X'), ' − ', var('χ', 'H'), '   (F 3,98 → Cl 3,16 → Br 2,96 → I 2,66)'),
       seq(_r, ' = ', var('r', 'H'), ' + ', var('r', 'X'), '   (model; tajribiy qiymatdan kichik)'),
       seq(_pka, ' = 3,17 → −5,9 → −8,8 → −9,5   (suvda)'),
       seq('Tartib:  kislotalik ↑  ·  termik barqarorlik ↓  ·  qaytaruvchilik ↑')],
      # 2 — molekulyar tuzilish
      [seq(chem('H–X'), ':  bitta ', text('σ'), ' bog‘;  chiziqli, ikkiatomli molekula'),
       seq(var('μ', ''), ' = ', var('q', ''), ' · ', var('d', ''), '   (1,82 → 1,08 → 0,82 → 0,44 D)'),
       seq(_r, ' (tajribiy) = 0,917 / 1,2746 / 1,414 / 1,609 Å'),
       seq(var('Δr', ''), ' = ', var('r', 'sum'), ' − ', var('r', 'exp'), ' = +0,037 / −0,055 / −0,096 / −0,091 Å')],
      # 3 — kislotalik
      [chem('HX + H₂O ⇌ H₃O⁺ + X⁻'),
       seq(_ka, ' = ', frac(var('x', '²'), seq(_c, ' − ', var('x', ''))), '   (HF: ', _ka, ' = 6,8×10⁻⁴)'),
       seq(var('x', ''), ' = ', frac(seq('−', _ka, ' + ', text('√'), seq('(', var('K', 'a'), '² + 4', _ka, _c, ')')), '2')),
       seq(var('α', '%'), ' = 100 · ', frac(var('x', ''), _c), ';   pH = −lg ', var('x', ''))],
      # 4 — gidratatsiya
      [seq(_dh, '(X⁻) = −506 / −364 / −335 / −293 kJ/mol'),
       seq(_d, ' + ', _dh, ' = 63 / 68 / 35 / 2 kJ/mol   (model balansi)'),
       seq(chem('HF + F⁻ ⇌ HF₂⁻'), '   (bifluorid; konsentratsiya oshganda)'),
       seq(chem('HF + H⁺ ⇌ H₂F⁺'), '   (protonlangan shakl)')],
      # 5 — termik barqarorlik
      [chem('2HX(g) ⇌ H₂(g) + X₂(g)'),
       seq(_dg, ' = Δ', var('f', ''), var('G', '°'), '(X₂) − 2 Δ', var('f', ''), var('G', '°'), '(HX)'),
       seq(_dg, ' = +550,8 / +190,6 / +110,0 / +15,9 kJ/mol'),
       seq('lg ', _kt, ' = −', frac(_dg, seq('2,303 · R · T', '')), '   (T = 298,15 K)')],
      # 6 — olish
      [chem('CaF₂ + H₂SO₄ → 2HF + CaSO₄'),
       seq(_n, '(HF) = 2 ', _n, '(CaF₂)'),
       seq(_m, '(HF) = ', _n, '(CaF₂) · 2 · ', var('M', 'HF'), ' · η   (model: 447,4 kg)'),
       seq(chem('Cl₂ + H₂ → 2HCl'), '   ·   ', chem('Br₂ + SO₂ + 2H₂O → H₂SO₄ + 2HBr'))],
      # 7 — kislota xossalari
      [chem('2HX + M → MX₂ + H₂↑'),
       seq(_n, '(HX) = ', frac(_m, var('M', 'HX')), ';   ', _n, '(CaCO₃) = ', frac(_n, '(HX)'), ' / 2'),
       seq(chem('CaCO₃ + 2HX → CaX₂ + CO₂↑ + H₂O')),
       seq(_m, '(CaCO₃) = 137,3 kg;  ', _m, '(CaCl₂) = 152,2 kg;  ', _m, '(CO₂) = 60,4 kg   (model)')],
      # 8 — redoks
      [chem('2HBr + H₂SO₄ → Br₂ + SO₂ + 2H₂O'),
       seq(_m, '(Br₂) = ', frac(_n, '(HBr)'), ' · ', var('M', 'Br₂'), '   (1 kg HBr → 987,5 g)'),
       seq(chem('4HI + O₂ → 2I₂ + 2H₂O')),
       seq(_m, '(I₂) = ', frac(_n, '(HI)'), ' · ', var('M', 'I₂'), ';   ', _m, '(O₂) = ', frac(_n, '(HI)'), ' / 4 · ', var('M', 'O₂'))],
      # 9 — materiallar
      [chem('SiO₂ + 6HF → H₂SiF₆ + 2H₂O'),
       seq(_m, '(HF) = 6 · ', _n, '(SiO₂) · ', var('M', 'HF'), '   (1 kg SiO₂ → 1997,9 g)'),
       seq(_m, '(eritma, 48 %) = ', frac(_m, '(HF)'), ' / 0,48   = 4162,4 g'),
       seq(_m, '(H₂SiF₆) = ', _n, '(SiO₂) · ', var('M', 'H₂SiF₆'), ' = 2398,3 g')],
      # 10 — xavfsizlik va ekologiya
      [seq(chem('2HF + Ca²⁺ → CaF₂'), '   (Ca²⁺ ni bog‘lash; gipokalsemiya mexanizmi)'),
       seq(chem('2HCl + CaCO₃ → CaCl₂ + CO₂↑ + H₂O')),
       seq(_m, '(CO₂) = ', frac(_n, '(HCl)'), ' / 2 · ', var('M', 'CO₂'), '   (60,4 kg / 1000 kg eritma)'),
       seq('HF:  OSHA TWA 3 ppm;  NIOSH IDLH 30 ppm   (manba chegaralari)')],
      # 11 — ishlangan hisob
      [seq('A:  ', var('x', ''), ' = ', frac(seq('−', _ka, ' + ', text('√'), seq('(', _ka, '² + 4', _ka, _c, ')')), '2'),
           ';   ', _c, ' = 0,010 / 0,100 / 1,000 M  →  22,90 / 7,91 / 2,57 %'),
       seq('B:  ', _m, '(qoldiq) = ', _m, '(HCl) / 0,202;  1000 kg 10 % → 495,0 kg (suv 505,0 kg)'),
       seq('B:  37 % li eritma uchun 1831,7 kg kerak > 1000 kg → distillatsiya bilan imkonsiz'),
       seq('C:  D + ΔH', var('hyd', ''), ' = 63 / 68 / 35 / 2 kJ/mol'),
       seq('C:  ΔG° = −3,4 / −35,9 / −49,4 / −53,3 kJ/mol')]
    ]
