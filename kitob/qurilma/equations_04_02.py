from book_equations import seq,sub,sup,frac,chem,var

def redox_equations():
    ec=var('E','cell');ec0=sup(ec,'°')
    return [
      [chem('Zn + 2H⁺ → Zn²⁺ + H₂')],
      [seq(ec,' = ',var('E','kat'),' − ',var('E','an')),seq('ΔG = −nF',ec),seq('lg K = ',frac(seq('nF',ec0),'RT ln 10'))],
      [seq('E = ',sup('E','°'),' − ',frac('RT','nF'),' ln Q'),seq('E = ',sup('E','°'),' − ',frac('0,05915935 V','n'),' lg Q')],
      [chem('MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O'),chem('Fe²⁺ → Fe³⁺ + e⁻')],
      [chem('Cu + 4HNO₃ → Cu(NO₃)₂ + 2NO₂ + 2H₂O'),chem('3Cu + 8HNO₃ → 3Cu(NO₃)₂ + 2NO + 4H₂O')],
      [chem('Cu + 2H₂SO₄ → CuSO₄ + SO₂ + 2H₂O'),chem('SO₂ + 2H₂O → SO₄²⁻ + 4H⁺ + 2e⁻')],
      [chem('H₃PO₃ + H₂O → H₃PO₄ + 2H⁺ + 2e⁻'),chem('H₃PO₂ + 2H₂O → H₃PO₄ + 4H⁺ + 4e⁻')],
      [chem('3HNO₂ → HNO₃ + 2NO + H₂O'),chem('H₂O₂ + 2H⁺ + 2e⁻ → 2H₂O'),chem('H₂O₂ → O₂ + 2H⁺ + 2e⁻')]
    ]
