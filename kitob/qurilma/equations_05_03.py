from book_equations import seq, var, frac, chem, par, sup, text, sub

_hvap = var('ΔH', 'vap')
_c = var('c', '0')
_wm = var('w', 'm')
_weq = var('w', 'eq')
_pi = var('Π', 'osm')


def drying_equations():
    return [
      # 1 — namlik ko'rsatkichlari
      [seq(var('X', ''), ' = ', frac('m(suv)', 'm(namuna)'), ';   ',
           var('w', ''), ' = ', frac('m(suv)', 'm(quruq modda)')),
       seq(var('X', ''), ' = ', frac(var('w', ''), seq('1 + ', var('w', ''))),
           '   (model: 0,35 kg / 1,00 kg → 0,2593)'),
       seq('Quruq qoldig‘ (2.2.32):  ',
           frac(seq('m₀ − m₁'), 'm₀'), ' × 100 %  →  0,50 %')],
      # 2 — higroskopiklik
      [seq('Δm = ', frac(seq('m₃ − m₂'), seq('m₂ − m₁')), ' × 100 %'),
       seq('Model: (15,35 − 15,00)/(15,00 − 5,00) = 3,50 %'),
       seq('Sinflar:  deliquescent;  ≥ 15 %;  2–15 %;  0,2–2 %'),
       seq('Sharoit:  25 ± 1 °C,  80 ± 2 % RH,  24 h')],
      # 3 — usul tanlash va umumiy balans
      [seq('m(namuna) = m(quruq modda) + m(suv)'),
       seq('m(chiqindi) = m(namuna) − m(mahsulot)'),
       seq('E = m(suv) · ', _hvap, ' / M(H₂O)'),
       seq('m(suv)/m(entrainer) = 0,2469 (toluen)  →  entrainer sarfi')],
      # 4 — vakuum va bug'lanish
      [seq('Δ', sup('fH', '°'), '(g) − Δ', sup('fH', '°'), '(l) = 44,01 kJ/mol (25 °C)'),
       seq('ln(p₂/p₁) = −(', _hvap, '/R)(1/T₂ − 1/T₁);  ', sup('p', '°'), ' = 101,325 kPa'),
       seq('Model:  1,5 kPa → 9,22 °C;  0,1 kPa → −28,96 °C'),
       seq(_weq, ' = ', frac(seq(_wm, '·C·x'), seq('1 + (C − 1)x')),
           ';   x = p/p₀,  w_m = 0,05,  C = 10')],
      # 5 — azeotropik quritish
      [seq('Toluen–suv:  84,1 °C,  ', var('w', 'suv'), ' = 0,198 (x = 0,444)'),
       seq('Sikloheksan–suv:  69,5 °C,  8,4 %;  n-geptan–suv:  70,9 °C,  12,5 %'),
       seq('m(distillat) = m(suv)/0,198 = 1598,90 kg'),
       seq('m(toluen) = 1282,32 kg;  yo‘qotish 0,158 kg')],
      # 6 — quritgichlar
      [chem('P₂O₅ + 3H₂O → 3H₃PO₄'),
       seq('Sig‘im:  54,05/141,94 = 38,08 % massa'),
       seq('CaCl₂: 0,974 kg/kg;  MgSO₄: 1,048 kg/kg suv'),
       seq('m(4A) = m(suv)/0,205 = 487,8 kg (100,0 kg suv)')],
      # 7 — gidrat quritish
      [seq('CuSO₄·5H₂O: M = 249,68 g/mol;  ·H₂O: 177,62;  anh.: 159,61'),
       seq('n = 1000,0/249,68 = 4,0051 kmol'),
       seq('m(H₂O) = 4 × 4,0051 × 18,015 = 288,60 kg'),
       seq('m(mahsulot) = 4,0051 × 177,62 = 711,40 kg')],
      # 8 — ekstraksiya, adsorbsiya, membrana
      [seq('D = ', frac('c(org faza)', 'c(suv fazasi)'), '  (taqsimot koeffitsienti)'),
       seq('q = ', frac(frac(var('q', 'max'), 'K·C'), seq('1 + K·C')),
           '  (adsorbsiya izotermasi)'),
       seq(_pi, ' = cRT  (osmotik bosim)'),
       seq('Tartib:  tozalash → quritish')],
      # 9 — suv miqdori nazorati
      [chem('I₂ + H₂O + SO₂ + 3Py → 2Py·HI + Py·SO₃'),
       seq('n(I₂) = 0,50 × 22,2/1000 = 0,0111 mol'),
       seq('m(H₂O) = 0,0111 × 18,015 = 0,2000 g  →  10,00 %'),
       seq('KF — faqat suv;  LOD — barcha uchuvchi;  TGA — haroratga bog‘liq')],
      # 10 — energetika
      [seq('Q = m(H₂O)·', _hvap, '/M = m × 2,2568 MJ/kg'),
       seq('1 kg suv → 2,2568 MJ = 0,6269 kWh'),
       seq('Model (kWh/kg suv):  sital 0,18;  vakuum 0,85;  shkaf 1,05;  azeotrop 1,55'),
       seq(var('E', 'chiq'), ' = ', frac('m(chiqindi)', 'm(mahsulot)'))],
      # 11 — ishlangan hisob
      [seq('A: n = 4,0051 kmol;  m(H₂O) = 288,60 kg;  m = 711,40 kg'),
       seq('A: w 36,08 % → 10,14 %;  Q = 651,3 MJ = 180,9 kWh'),
       seq('B: m(suv) = 316,58 kg;  distillat 1598,90 kg'),
       seq('B: toluen 1282,32 kg;  yo‘qotish 0,158 kg;  Q = 1244,2 MJ')],
    ]
