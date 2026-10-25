from book_equations import seq, var, frac, chem, par, sup, text, sub

_ka1 = var('K', 'a1')
_ka2 = var('K', 'a2')
_kap = var('K', 'ap')
_pka1 = seq('p', var('K', 'a1'))
_pka2 = seq('p', var('K', 'a2'))
_h = var('h', '')
_x = var('x', '')
_c = var('c', '')
_n = var('n', '')
_v = var('V', '')
_w = var('w', '')
_m = var('m', '')
_teq = var('T', 'erish')
_tqa = var('T', 'qaynash')


def sulfate_equations():
    return [
      # 1 — umumiy tavsif va identifikatsiya
      [seq('H₂SO₄: 98,078 g/mol;  S — +VI daraja;  CAS 7664-93-9;  UN 1830 / 1831 / 1832'),
       seq('M = 32,06 + 4×16,00 + 2×1,008 = 98,08 g/mol'),
       seq('Taxminiy hisob: moniklik massasi 97,9674 — 98,08 dan 0,11 % farq'),
       seq('ΔfH°(g) = −735,13 kJ/mol;  S°(g) = 298,78 J/(mol·K)'),
       seq(chem('H₂SO₄ + H₂O → H₃O⁺ + HSO₄⁻'), '   (1-bosqich, to‘liq)')],
      # 2 — molekula geometriyasi
      [seq('C₂ simmetriya;  gauche-gauche konformatsiya;  τ(H–O–S–O) = 89,1°'),
       seq('r(S=O) = 142,2 pm;  r(S–OH) = 157,4 pm;  r(O–H) = 97,0 pm'),
       seq('∠O=S=O = 123,3°;  ∠O=S–OH = 101,3°;  ∠H–O–S = 108,5°'),
       seq('Ab initio:  r(S=O) 140,99 pm;  r(S–OH) 157,51 pm;  τ = −86,66°'),
       seq('Taxminiy hisob: 123,3 + 101,3 + 106,4 + 108,7 = 439,7°;  ideal 4 × 109,47° = 437,9°;  farq +1,8°')],
      # 3 — elektron tuzilma
      [seq('Proton affinity = 699,4 kJ/mol;  gaz bazikligi = 666,9 kJ/mol'),
       seq('ΔrG°(deprotonatsiya, g) = 1265 ± 10 kJ/mol'),
       seq('Taxminiy hisob (gaz fazasi): ΔG = 1265 − 691 = +574 kJ/mol — endotermik'),
       seq('Taxminiy hisob (suv fazasi): proton gidratsiyasi ≈ −1091 kJ/mol — kamomad qoplanadi'),
       seq('Pauling yondashuvi: S=O π → S–OH σ* uzatilishi;  S–OH bog‘i uzayadi')],
      # 4 — spektroskopiya
      [seq('SO₄²⁻ (', sub('T', 'd'), '):  ν₁ 981;  ν₂ 451;  ν₃ 1104;  ν₄ 617 sm⁻¹'),
       seq('HSO₄⁻ (', sub('C', 's'), '):  1055;  1030;  900 sm⁻¹ (Raman)'),
       seq('H₂SO₄ (g):  O–H 3603;  S=O 1248;  S–OH 792;  SO₃ 499 sm⁻¹'),
       seq('Taxminiy hisob: 3N − 6 = 6 = 1 (A₁) + 2 (E) + 3 (F₂);  IR’da faol 3 ta'),
       seq('Taxminiy hisob: H₂SO₄ — 3N − 6 = 15 oddiy tebranish;  C₂ da hammasi IR’da faol'),
       seq('³³S NMR: sulfat ioni 328 ppm (suyultirilgan H₂SO₄ ga nisbatan)')],
      # 5 — kislotalik
      [seq(chem('H₂SO₄ + H₂O → H₃O⁺ + HSO₄⁻'), '   ', _ka1, ' ≈ 10³   (', _pka1, ' ≈ −3)'),
       seq(chem('HSO₄⁻ + H₂O ⇌ H₃O⁺ + SO₄²⁻'), '   ', _ka2, ' = 1,2×10⁻²   (', _pka2, ' = 1,99)'),
       seq('Taxminiy hisob: 10³ / 1,2×10⁻² = 8,3×10⁴ ≈ 10⁵ (Paulining qoidasi)'),
       seq('Solishtirish (7.2-bo‘lim): sulfit kislota K', sub('a', '1'), ' 1,54×10⁻²;  K',
           sub('a', '2'), ' 6,3×10⁻⁸ — konjugat asos ~10⁵ barobar barqarorroq'),
       seq('Taxminiy hisob: 1,000 M eritmada pH = −0,01;  SO₄²⁻ ulushi 1,17 %')],
      # 6 — suvdagi dissotsiatsiya
      [seq(_ka2, ' = ', frac(seq(_h, '·', _x), seq(_c, ' − ', _x)),
           '   →   ', seq(_x, '² + (', _c, ' + K', sub('a', '2'), ')', _x,
                          ' − K', sub('a', '2'), '·', _c, ' = 0')),
       seq('Taxminiy hisob: 0,001 M → ', _h, ' = 0,001865;  pH = 2,73;  SO₄²⁻ 86,55 %'),
       seq('Taxminiy hisob: 0,010 M → ', _h, ' = 0,014524;  pH = 1,84;  SO₄²⁻ 45,24 %'),
       seq('Taxminiy hisob: 0,100 M → ', _h, ' = 0,109848;  pH = 0,96;  SO₄²⁻ 9,85 %'),
       seq('Taxminiy hisob: 1,000 M → ', _h, ' = 1,011722;  pH = −0,01;  SO₄²⁻ 1,17 %'),
       seq('Taxminiy hisob: 4,000 M → ', _h, ' = 4,011929;  pH = −0,60;  SO₄²⁻ 0,30 %')],
      # 7 — sufma kislota
      [seq(chem('2H₂SO₄ ⇌ H₃SO₄⁺ + HSO₄⁻'), '   — avtoprotoliz'),
       seq('100 % kislota (mmol/kg):  HSO₄⁻ 15,0;  H₃SO₄⁺ 11,3;  H₃O⁺ 8,0;  HS₂O₇⁻ 4,4'),
       seq('Taxminiy hisob: ', _kap, ' = 0,0113 × 0,0150 = 1,70×10⁻⁴ mol²/kg²'),
       seq('Taxminiy hisob: x(H₃SO₄⁺) = 1,11×10⁻³;  ', _kap, '(x) = 1,63×10⁻⁶'),
       seq('Hammett H₀ = −12 — superkislotalik chegarasi;  proton solvatsiyasi ≈85 kJ/mol zaif'),
       seq('Taxminiy hisob: ', _c, ' = 1,8302×1000/98,08 = 18,66 mol/L → 37,3 mol H⁺/L')],
      # 8 — ionlar tuzilishi
      [seq('SO₄²⁻: ', sub('T', 'd'), ';  r(S–O) = 147,2 pm;  ∠O–S–O = 109,47°'),
       seq('HSO₄⁻: ', sub('C', 's'), ';  Γ', sub('Γ', 'vib'), ' = 8a′ + 4a″;  12 ta chastota'),
       seq('Taxminiy hisob: rezonans shakllari 4! / (2!·2!) = 6'),
       seq('Taxminiy hisob: zaryad taqsimoti −2/4 = −0,5 e har bir kislorodda (sodda yondashuv)'),
       seq('Taxminiy hisob: r(S=O) 142,2 vs 147,2 → 5,0 pm qisqa;  r(S–OH) 157,4 → 10,2 pm uzun'),
       seq('Pauling yondashuvi: S=O π → S–OH σ* — S–OH bog‘i uzayadi va kuchsizlanadi')],
      # 9 — gidratlar
      [seq('H₂SO₄·', _n, 'H₂O:  ', _w, '(H₂SO₄) = 100·98,08/(98,08 + 18,015', _n, ') %'),
       seq('Taxminiy hisob: ', _n, ' = 1 → 84,48 %;  ', _n, ' = 2 → 73,13 %;  ', _n, ' = 3 → 64,47 %'),
       seq('Taxminiy hisob: ', _n, ' = 4 → 57,65 %;  ', _n, ' = 6,5 → 45,58 %;  ', _n, ' = 8 → 40,49 %'),
       seq('Taxminiy hisob: 60 % eritmada ', _n, ' = (98,08/18,015)·(40/60) = 3,63'),
       seq('SAM: H₃O⁺HSO₄⁻;  SAT: [H₅O₂⁺]₂SO₄²⁻;  SAO: H₃O⁺ + SO₄²⁻·7H₂O'),
       seq('Evteklar: muz–SAH 211 K (36 %);  muz–SAT 199 K (38 %)')],
      # 10 — kristal tuzilma
      [seq('Monoklin, C2/c;  a = 818,1;  b = 469,60;  c = 856,3 pm;  β = 111,39°;  Z = 4'),
       seq('Taxminiy hisob: V = a·b·c·sinβ = 306 313 pm³'),
       seq('Taxminiy hisob: V/Z = 76 578 pm³ = 76,54 Å³'),
       seq('Taxminiy hisob: ρ = M/(V·', sub('N', 'A'), ') ≈ 2,13 g/cm³'),
       seq(_teq, ' = 10,31 °C;  ', _tqa, ' = 337 °C;  ρ(suyuq) = 1,8302 g/cm³'),
       seq('Viskozitet 26,7 cP;  ΔvapH ≈ 69 kJ/mol;  p(20 °C) = 0,001 mmHg')],
      # 11 — xulosa va ishlangan hisob
      [seq('A (tuzilma):  C₂;  142,2 / 157,4 / 97,0 pm;  τ = 89,1°;  burchaklar yig‘indisi 439,7°'),
       seq('B (spektr):  SO₄²⁻ 981 / 451 / 1104 / 617 sm⁻¹;  H₂SO₄ 3603 / 1248 / 792 / 499 sm⁻¹'),
       seq('C (kislotalik):  K', sub('a', '1'), ' ≈ 10³;  K', sub('a', '2'),
           ' = 1,2×10⁻²;  farq 8,3×10⁴ ≈ 10⁵'),
       seq('D (dissotsiatsiya):  0,001 M → pH 2,73 (86,55 %);  1,000 M → pH −0,01 (1,17 %)'),
       seq('E (sufma, gidrat, kristal):  ', _kap, ' = 1,70×10⁻⁴ mol²/kg²;  H₀ = −12;  84,48 → 40,49 %;  V = 306 313 pm³'),
       seq('F (sanoat):  1000 kg H₂SO₄ → S 326,9 kg;  oleum 1163,3 kg (SO₃ 14,0 %)')],
    ]
