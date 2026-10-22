from book_equations import seq, var, frac, chem, par, sup, text

def decomposition_equations():
    dg = sup('ΔG', '°'); dh = sup('ΔH', '°'); ds = sup('ΔS', '°')
    h = sup(chem('[H⁺]'), '2')
    return [
      # 1 — parchalanish va uning qarindoshlari
      [chem('HNO₃ ⇌ H⁺ + NO₃⁻   (dissotsiatsiya)'),
       seq('Parchalanishda ', var('n', 'acid'),
           ' kamayadi, mahsulotlar paydo bo‘ladi')],
      # 2 — termodinamik mezon va parchalanish harorati
      [seq(dg, ' = ', dh, ' − T', ds),
       seq('ΔG = ', dg, ' + RT ln Q;   ', dg, ' = −RT ln K'),
       seq(var('T', '*'), ' = ', frac(dh, ds), '   (ΔG(T) = 0)')],
      # 3 — van 't Hoff
      [seq('ln K = −', frac(dh, 'RT'), ' + ', frac(ds, 'R')),
       seq('ln(', frac(var('K', '2'), var('K', '1')), ') = −', frac(dh, 'R'),
           par(seq(frac('1', var('T', '2')), ' − ', frac('1', var('T', '1')))))],
      # 4 — Arrhenius va birinchi tartibli parchalanish
      [seq('k = A exp', par(seq('−', frac(var('E', 'a'), 'RT')))),
       seq(var('c', 't'), ' = ', var('c', '0'), ' exp(−kt);   ',
           var('t', '½'), ' = ', frac('ln 2', 'k'))],
      # 5 — fotokimyoviy parchalanish
      [seq('E = hν = ', frac('hc', 'λ'), ';   faqat yutilgan foton ta’sir qiladi'),
       seq(text('Φ'), ' = ', frac('mol mahsulot', 'mol yutilgan foton'))],
      # 6 — dismutatsiya
      [chem('3HNO₂ → HNO₃ + 2NO + H₂O'),
       chem('3HClO₃ → HClO₄ + 2ClO₂ + H₂O'),
       chem('2H₂O₂ → 2H₂O + O₂')],
      # 7 — kondensatsiya
      [chem('2H₃PO₄ → H₄P₂O₇ + H₂O'),
       chem('H₄P₂O₇ → 2HPO₃ + H₂O'),
       chem('H₂SO₄ + SO₃ → H₂S₂O₇'),
       chem('H₂SiO₃ → SiO₂ + H₂O')],
      # 8 — pH bilan bog'lanish: S(IV) speciation
      [chem('SO₂·H₂O ⇌ H⁺ + HSO₃⁻;   HSO₃⁻ ⇌ H⁺ + SO₃²⁻'),
       seq(var('α', 'SO2'), ' = ', frac(h, par(seq(h, ' + ', var('K', 'a1'),
           chem('[H⁺]'), ' + ', var('K', 'a1'), var('K', 'a2')))))],
      # 9 — saqlash: kinetik chegara
      [chem('HNO₃ → NO₂ + H₂O + ½O₂   (yorug‘likda, qizdirilganda)'),
       seq('Saqlash muddati: ', var('t', 'muddat'), ' ≈ ', frac('ln 2', 'k'),
           ' — kinetik nazorat bilan cheklangan')],
      # 10 — tahlil: o'lchanadigan kattalik
      [seq(text('α'), ' = 1 − ', frac(var('c', 't'), var('c', '0')), ';   ',
           var('c', 't'), ' = ', var('c', '0'), ' exp(−kt)'),
       seq('O‘lchanadigan kattalik: qolgan kislota yoki hosil bo‘lgan mahsulot — bittasi tanlanadi')],
      # 11 — ishlangan hisob
      [seq(dh, ' = −395,72 − 285,83 + 813,99 = +132,44 kJ/mol'),
       seq(ds, ' = 256,76 + 70,00 − 156,90 = 169,86 J/(mol·K)'),
       seq(dg, ' = +81,80 kJ/mol;   ', var('T', '*'), ' = 779,7 K;   lg K = −14,33')]
    ]
