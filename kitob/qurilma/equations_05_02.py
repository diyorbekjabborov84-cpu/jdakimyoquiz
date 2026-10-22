from book_equations import seq, var, frac, chem, par, sup, text, sub

# --- umumiy o'zgaruvchilar -------------------------------------------------
_ksp = var('K', 'sp')
_kf = var('K', 'f')
_eta = text('η')
_e_ch = var('E', 'chiq')
_c0 = var('c', '0')
_cN = var('c', 'N')
_xD = var('x', 'D')
_xB = var('x', 'B')
_alpha = text('α')
_phi = text('Φ')
_ratio = seq(frac(_xD, seq('1 − ', _xD)), '·', frac(seq('1 − ', _xB), _xB))


def purification_equations():
    return [
      # 1 — tozalash o'lchovi
      [seq(var('w', 'i'), ' = ', frac(var('m', 'i'), 'm(eritma)'),
           ';   ', _eta, ' = ', frac(chem('c(kirish) − c(chiqish)'),
                                    'c(kirish)')),
       seq('Tozalik darajasi (ppm) = ', frac('m(ifloslik)', 'm(namuna)'),
           '·10⁶')],
      # 2 — ifloslik manbalari
      [chem('Fe + 2HCl → FeCl₂ + H₂ ↑'),
       chem('4HNO₃ → 4NO₂ + 2H₂O + O₂ ↑'),
       chem('H₂SO₄ + H₂O → HSO₄⁻ + H₃O⁺')],
      # 3 — usullarning fizik-kimyoviy asosi
      [seq('m(kirish) = m(mahsulot) + m(chiqindi)'),
       seq(var('E', 'chiq'), ' = ', frac('m(chiqindi)', 'm(mahsulot)'),
           '   (kg/kg)'),
       seq('Ekstraksiya:  D = ', frac('c(org faza)', 'c(suv fazasi)'),
           ';   membrana:  J = A·ΔP')],
      # 4 — bug'lash va rektifikatsiya
      [chem('p_i = x_i · γ_i · p_i°'),
       seq(_alpha, ' = ', frac(chem('(y₁/x₁)'), chem('(y₂/x₂)')),
           ';   ', var('N', 'min'), ' = ', frac(seq('lg ', par(_ratio)),
                                                seq('lg ', _alpha))),
       seq('Azeotrop:  x = y  ⇔  ', _alpha, ' = 1'),
       seq('McCabe-Thiele:  α = 2,0 → N = 16;  R_min = 1,70')],
      # 5 — cho'ktirish
      [seq(_ksp, ' = ', chem('[Mⁿ⁺][OH⁻]ⁿ')),
       seq(chem('[Mⁿ⁺]'), ' = ', frac(_ksp, chem('[OH⁻]ⁿ')),
           ';   pH + 1 → 100 marta (n = 2)'),
       seq(_kf, ' = ', frac(chem('[Cu(NH₃)₄²⁺]'),
                            chem('[Cu²⁺][NH₃]⁴')), ' = 1,7·10¹³'),
       seq('CuS: K', sub('sp', ''), ' = 8,5·10⁻⁴⁵;  Zn(OH)₂ + 2OH⁻ → [Zn(OH)₄]²⁻')],
      # 6 — kimyoviy tozalash
      [chem('4NO₂ + O₂ + 2H₂O → 4HNO₃'),
       chem('3HNO₂ → HNO₃ + 2NO ↑ + H₂O'),
       chem('2Fe³⁺ + Cu → 2Fe²⁺ + Cu²⁺'),
       chem('M²⁺ + H₂S → MS ↓ + 2H⁺;   Al³⁺ + 6F⁻ → [AlF₆]³⁻')],
      # 7 — adsorbsiya va ion almashinuv
      [seq(frac(text('q'), var('q', 'max')), ' = ',
           frac(frac('K', 'C'), seq('1 + ', frac('K', 'C')))),
       seq(var('q', 'max'), ' = 50 mg/g;  K = 0,5 L/mg (model)'),
       seq(var('k', 'Mg/Ca'), ' = ',
           frac(frac(var('[Mg]', 'S'), var('[Ca]', 'S')),
                frac(var('[Mg]', 'M'), var('[Ca]', 'M')))),
       seq('Fronti kiring:  C/C₀ = 0,5 → BV = 4,96 / 1,28 / 0,34')],
      # 8 — kislota oilalari
      [chem('Ca²⁺ + 2F⁻ → CaF₂ ↓'),
       chem('2As³⁺ + 3H₂S → As₂S₃ ↓ + 6H⁺'),
       chem('Fe₂(SO₄)₃ + 3CaO + 3H₂O → 2Fe(OH)₃ ↓ + 3CaSO₄'),
       seq('Azeotroplar:  HNO₃ 68,8 %;  HCl 20,2 %;  H₂SO₄ 98,3 %')],
      # 9 — zanjir va resurs samaradorligi
      [seq(_c0, ' = ', _c0, '·', sup(par(seq('1', '/', _phi)), 'N')),
       seq('N = ', frac(seq('lg ', frac(_cN, _c0)), seq('lg ', frac('1', _phi)))),
       seq('Φ = 1000 → 10⁻⁶ gacha 2 bosqich;  Φ = 10 → 6 bosqich'),
       seq(_e_ch, ' = ', frac('m(chiqindi)', 'm(mahsulot)'),
           '   (model: 0,00167 kg/kg)')],
      # 10 — sifat nazorati
      [seq('c = ', frac(var('n', 'titrant'), var('V', 'namuna'))),
       seq(text('w'), ' = ', frac(seq(text('c'), '·', text('M')),
                                 seq('1000·', text('ρ')))),
       seq('ppm:  ', frac('m(ifloslik)', 'm(namuna)'), '·10⁶'),
       seq('Ph. Eur. HNO₃:  68,0–70,0 %;  Cl⁻ ≤ 0,5 ppm;  Fe ≤ 10 ppm')],
      # 11 — ishlangan hisob
      [seq('n(NO₂) = 4000 kg / 46,01 kg/kmol = 86,938 kmol'),
       seq('m(HNO₃) = 86,938 · 63,01 = 5477,9 kg = 5,4779 t;  w = 68,55 %'),
       seq('n(Fe) = 300 kg / 55,85 = 5,3715 kmol;  Fe(OH)₃ = 0,5741 t'),
       seq('E = 0,00167 kg/kg;  CaCO₃ → 0,7903 t')],
    ]
