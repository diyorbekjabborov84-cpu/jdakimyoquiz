from book_equations import seq,var,frac,chem,par

def passive_equations():
    ia=var('i','a');ic=var('i','c');ec=var('E','corr');kg=var('k','g');ll=var('L','lim');li=var('L','∞');vd=var('v','diss');hu=var('h','uniform')
    return [
      [seq(var('i','net'),' = ',ia,' + ',ic,' = 0'),seq(var('i','corr'),' = ',ia,' = |',ic,'|')],
      [chem('2Cr + 3H₂O → Cr₂O₃ + 6H⁺ + 6e⁻'),chem('Al₂O₃ + 6H⁺ → 2Al³⁺ + 3H₂O')],
      [chem('NO₃⁻ + 2H⁺ + e⁻ → NO₂ + H₂O'),seq(ia,par(ec),' = |',ic,par(ec),'|')],
      [seq(frac('dL','dt'),' = ',kg,par(seq(ll,' − L')),' − ',vd),seq(li,' = ',ll,' − ',frac(vd,kg)),seq('L(t) = ',li,' + ',par(seq(var('L','0'),' − ',li)),' exp',par(seq('−',kg,' t')))],
      [chem('Fe³⁺ + H₂O ⇌ FeOH²⁺ + H⁺'),seq(var('E','pit'),' = ',var('E','pit,ref'),' − b lg',par(frac(var('a','Cl'),var('a','Cl,ref'))))],
      [chem('Cr₂O₃ + 4H₂O → Cr₂O₇²⁻ + 8H⁺ + 6e⁻'),chem('2H₂O → O₂ + 4H⁺ + 4e⁻')],
      [seq(var('i','corr'),' = ',frac('B',var('R','p'))),seq('B = ',frac(seq(var('b','a'),' ',var('b','c')),seq('ln(10)',par(seq(var('b','a'),' + ',var('b','c'))))))],
      [seq('m = ',frac(seq(var('i','M'),' A t M'),'nF')),seq(hu,' = ',frac('m','ρA')),seq(var('h','local'),' = ',frac(hu,'f'))]
    ]
