from book_equations import seq, var, frac, chem, par, sup, text, sub

_ph = var('φ', 'konv')
_sel = var('S', 'sel')
_foa = var('FOA', '')
_cvar = var('c', 'o‘z')
_cfoa = var('c', 'FOA')
_oee = var('OEE', '')
_q = var('Q', '')
_mh = var('m', 'H₂O')


def industry_equations():
    return [
      # 1 — texnologik sxema
      [seq(var('n', 'kirish'), ' → ', var('n', 'chiqish'), '  (modda oqimi)'),
       seq(_ph, ' = ', frac(var('n', 'chiqish'), var('n', 'kirish')), ' × 100 %'),
       seq(_sel, ' = ', frac(var('n', 'kerakli'), seq(var('n', 'kerakli'), ' + ', var('n', 'begona'))), ' × 100 %'),
       seq('Darajalar:  birinchi → ikkinchi → oxirgi')],
      # 2 — apparatlar va OEE
      [seq(_oee, ' = ', var('A', ''), ' × ', var('P', ''), ' × ', var('Q', '')),
       seq('Model:  0,92 × 0,95 × 0,99 = 0,8653'),
       seq('Savdo hajmi = ', var('V', 'reja'), ' × ', _oee, ' = 86 526 t/y'),
       seq('Sahifalash', 'A = 0,92;  P = 0,95;  Q = 0,99', ' (ISO 22400-2:2014)')],
      # 3 — mass balansi
      [seq('Σ', var('m', 'kirish'), ' = Σ', var('m', 'chiqish'), ' + ', var('m', 'yig‘ilgan')),
       seq('n(HNO₃) = 680,0 × 1000/63,01 = 10,7919 kmol'),
       seq('m(NH₃) = 183,80 kg;  m(O₂) = 690,68 kg;  m(N₂) = 2596,97 kg'),
       seq('Suv:  hosil 194,42 + tashqari 222,79 = bog‘langan 97,21 + eritmada 320,00 kg')],
      # 4 — energiya
      [chem('NH₃ + 2O₂ → HNO₃ + H₂O'),
       seq('Δ', sup('fH', '°'), ' = Δ', sup('fH', '°'), '(l) − Δ', sup('fH', '°'), '(g) = −414,03 kJ/mol'),
       seq('Model: 10,7919 kmol → −4468,2 MJ (≈ −4,47 GJ)'),
       seq('Bug‘latish: 306,12 kg → 690,9 MJ;  toluen 1239,95 kg → 512,2 MJ'),
       seq('Qatnoq bug‘: 0,10→99,63 °C;  2,00→212,42 °C;  8,00→295,06 °C')],
      # 5 — materiallar va korroziya
      [seq('m = ', frac(seq('m₀ − m₁'), seq('S·τ')), '   (korroziya mass yo‘qotishi)'),
       seq('Model: ', frac('0,12', seq('100 × 0,100 m² × 1000 s')), ' = 0,0012 g/(m²·soat)'),
       seq('Ierarxiya:  po‘lat → 316L → Hastelloy → PTFE/grafit'),
       seq('Loyihada material va sharoit birga baholanadi'),
       seq('S — namuna yuzasi (m', sup('2', ''), ');  τ — vaqt (soat)')],
      # 6 — xavfsizlik
      [seq('O₂ (jarayonda) < ', var('O', '2 krit'), '  →  yonish chegarasi'),
       seq('Inertlash:  havo chiqariladi,  N₂ suriladi'),
       seq('Xavf baholash:  oqibat × ehtimollik  (model)'),
       seq('Kuzatuv:  hodisa chastotasi,  to‘xtash davomiyligi,  bajarilgan harakat')],
      # 7 — ekologiya
      [seq('Chiqindi omili = ', frac(var('m', 'chiqindi'), var('m', 'mahsulot')), '   (model: 0,012)'),
       seq('CO₂e = faolitet × emissiya koeffitsienti  (model)'),
       seq('Suv sarfi = ', frac(var('m', 'suv'), var('m', 'mahsulot')), '  (qaytish bilan kamayadi)'),
       seq('NOₓ kamaytirish:  4NH₃ + 4NO + O₂ → 4N₂ + 6H₂O')],
      # 8 — sifat
      [seq(_oee, ' = ', frac(var('t', 'ish'), var('t', 'reja')), ' × ',
           frac(seq(var('t', 'ideal'), ' × ', var('N', '')), var('t', 'ish')), ' × ',
           frac(var('N', 'yaxshi'), var('N', ''))),
       seq('Cpk = min[', frac(seq('x̄ − ', var('L', 'spec')), seq('3', var('σ', 'L'))), '; ',
           frac(seq(var('U', 'spec'), ' − x̄'), seq('3', var('σ', 'U'))), ']  (model: 1,39)'),
       seq('Izchillik:  xom ashyo → reaktiv → apparat → operator → natija')],
      # 9 — raqamli boshqaruv
      [seq('Sensor → PLC/DCS → MES/ERP → reja'),
       seq('Soft sensor:  ŷ = f(x₁, x₂, …)  + model xatosi'),
       seq('PI:  birlik amallar soni ↓,  apparat hajmi ↓,  xotira ↓'),
       seq('Ramshaw (1995):  zavod hajmini va amallar sonini kamaytirish strategiyasi')],
      # 10 — iqtisodiyot
      [seq('CAPEX = 120,0 mln USD;  FOA = 0,08 · CAPEX = 9,60 mln USD/y'),
       seq(_cfoa, ' = ', frac(_foa, var('V', 'yil')), '  (model: 96 USD/t)'),
       seq('c(V) = ', _cvar, ' + ', frac(_foa, var('V', 'yil')), '  (model: 324 + FOA/V)'),
       seq('50 000→516;  100 000→420;  200 000→372 USD/t')],
      # 11 — ishlangan hisob
      [seq('A:  HNO₃ 680,00 kg;  n = 10,7919 kmol;  NH₃ 183,80 kg'),
       seq('A:  suv hosil 194,42;  bog‘langan 97,21;  tashqari 222,79 kg'),
       seq('A:  mahsulot 693,88 kg;  suv chiqarilgan 306,12 kg'),
       seq('A:  energiya:  −4468,2 MJ (reaksiya)  +  1203,1 MJ (konsentratsiya)'),
       seq('B:  FOA 96 USD/t;  OEE 0,8653;  savdo 86 526 t/y;  qaytish 9,9 yil')],
    ]
