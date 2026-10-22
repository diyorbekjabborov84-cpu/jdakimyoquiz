from book_equations import seq,var,frac,chem,par,sup,text

def complex_equations():
    ksp=var('K','sp');kspc=var('K','sp,c');qsp=var('Q','sp')
    b2=var('β','2');b2c=var('β','2,c');b4=var('β','4,c');bp=var('β′','2,c')
    al=var('α','L');ka=var('K','a,c');fm=var('F','M');cm0=var('C','M,0')
    cmd=var('C','M,diss');bu=var('B','u');csat=var('C','sat');ns=var('n','s')
    ag=chem('Ag⁺');cl=chem('Cl⁻');nh=chem('NH₃');m2=chem('M²⁺');oh=chem('[OH⁻]')
    return [
      # 1 — mass balance of the dissolved metal
      [seq(cmd,' = [M] + [ML] + [ML₂] + …'),
       seq(var('C','M,0'),' = ',cmd,' + ',frac(ns,'V'))],
      # 2 — solubility product and ion product
      [chem('AgCl(s) ⇌ Ag⁺ + Cl⁻'),
       seq(ksp,' = ',chem('a(Ag⁺)'),'·',chem('a(Cl⁻)'),';   ',qsp,' = ',chem('a(Ag⁺)'),'·',chem('a(Cl⁻)'))],
      # 3 — stepwise and overall formation constants
      [seq(var('K','1'),' = ',frac(chem('[ML]'),chem('[M][L]')),';   ',var('K','2'),' = ',frac(chem('[ML₂]'),chem('[ML][L]'))),
       seq(b2,' = ',frac(chem('[ML₂]'),chem('[M][L]²')),' = ',var('K','1'),'·',var('K','2'),';   ',var('K','d'),' = 1/',b2)],
      # 4 — protonation of the ligand and the conditional constant
      [chem('NH₄⁺ ⇌ H⁺ + NH₃'),
       seq(al,' = ',frac(nh,bu),' = ',frac(ka,seq(ka,' + ',chem('[H⁺]'))),';   ',bp,' = ',b2c,'·',sup(al,'2'))],
      # 5 — acid anions as ligands and as precipitants
      [chem('HSO₄⁻ ⇌ H⁺ + SO₄²⁻'),
       chem('S²⁻ + 2H⁺ ⇌ H₂S'),
       seq(var('α','SO4'),' = ',frac(chem('[SO₄²⁻]'),var('C','S')))],
      # 6 — dissolution promoted by complex formation
      [chem('AgCl(s) + 2NH₃ ⇌ Ag(NH₃)₂⁺ + Cl⁻'),
       seq('K = ',ksp,'·',b2,';   ',sup('s','2'),' = ',kspc,'·',par(seq('1 + ',b2c,'·',sup(nh,'2'))))],
      # 7 — side-reaction factor and precipitation onset
      [seq(fm,' = ',frac(cmd,m2)),
       seq(sup(oh,'2'),' = ',frac(seq(kspc,'·',fm),cm0))],
      # 8 — amphoteric hydroxide
      [chem('Al(OH)₃(s) + 3H⁺ ⇌ Al³⁺ + 3H₂O'),
       chem('Al(OH)₃(s) + OH⁻ ⇌ Al(OH)₄⁻'),
       seq(csat,' = ',kspc,'·',par(seq(frac('1',sup('x','3')),' + ',b4,'·x')))],
      # 9 — stoichiometry decides the solubility formula
      [chem('CaSO₄(s) ⇌ Ca²⁺ + SO₄²⁻'),
       seq('s = ',sup(kspc,'1/2'),'   (CaSO₄);   s = ',sup(par(frac(kspc,'4')),'1/3'),'   (CaF₂)')],
      # 10 — phase condition
      [seq(ns,' ≥ 0;   ',qsp,' ≤ ',ksp,';   ',ns,'·',par(seq(ksp,' − ',qsp)),' = 0')],
      # 11 — worked example: ligand balance
      [seq(sup('s','2'),' = ',kspc,'·',par(seq('1 + ',b2c,'·',sup('l','2')))),
       seq(var('C','B,0'),' = ',frac('l',al),' + 2·',par(seq('s − ',frac(kspc,'s'))))]
    ]
