from book_equations import seq, var, frac, chem, par, sup, text, sub

_ka = var('K', 'a')
_kf = var('K', 'f')
_ks = var('K', 'self')
_h = var('h', '')
_f = var('f', '')
_c = var('c', '')
_dg = var('ΔG', '°')
_m = var('m', '')
_n = var('n', '')
_r = var('r', '')
_dh = var('ΔH', 'hyd')


def halide_equations():
    return [
      # 1 — molekula
      [seq('r(H–F) = 0,917 Å;  ', var('D', ''), '(H–F) = 569 kJ/mol'),
       seq('χ(F) = 3,98;  Δχ(H–F) = 1,78;  ', var('μ', ''), ' = 1,8–1,9 D'),
       seq(chem('H–F···H–F···H–F'), '   (vodorod bog‘i zanjiri)'),
       seq('T', var('q', ''), ' :  HF 19,5 °C  >  HCl −85,1 °C')],
      # 2 — anhidr HF
      [chem('3HF ⇌ H₂F⁺ + HF₂⁻'),
       seq(_ks, ' = 2×10⁻¹² (273 K)'),
       seq('ε = 84 (273 K);  175 (200 K);  suyuqlanish 190–292,5 K'),
       seq('Λ', var('eq', ''), ' = 1,4×10⁻⁵ Ω⁻¹')],
      # 3 — superkislotalar
      [seq('H', var('0', ''), '(HF) = −15,1   ·   H', var('0', ''), '(SbF₅) = −21'),
       chem('SbF₅ + 2HF ⇌ H₂F⁺ + SbF₆⁻'),
       seq(chem('HF + F⁻ ⇌ HF₂⁻'), '   (kuchli bog‘langan konjugat asos)'),
       seq('K', var('a', ''), ' + F⁻ bog‘lanishi = kislotalik kuchayishi')],
      # 4 — suvli HF spetsiatsiyasi
      [seq(chem('HF + H₂O ⇌ H₃O⁺ + F⁻'), '   ', _ka, ' = 6,8×10⁻⁴'),
       seq(chem('HF + F⁻ ⇌ HF₂⁻'), '   lg', _kf, ' = 0,7'),
       seq('zaryad:  ', _h, ' = ', _f, ' + [HF₂⁻]'),
       seq('massa:  ', _c, ' = [HF] + [F⁻] + 2[HF₂⁻]')],
      # 5 — ishlab chiqarish
      [chem('CaF₂ + H₂SO₄ → 2HF + CaSO₄'),
       seq(_n, '(HF) = 2 ', _n, '(CaF₂)'),
       seq(_m, '(HF) = ', _n, '(CaF₂) · 2 · ', var('M', 'HF'), ' · η'),
       seq('Taxminiy hisob: 1000 kg fluorit (97 %) → HF 457,3 kg (unum 92 %)')],
      # 6 — shishani yemirish
      [chem('SiO₂ + 6HF → H₂SiF₆ + 2H₂O'),
       seq(chem('SiO₂ + 4HF → SiF₄↑ + 2H₂O'), '  (gaz fazasida)'),
       seq(_r, ' = 510[F⁻] + 610[HF] + 2890[HF₂⁻]   (Å/min)'),
       seq('Selektivlik SiO₂ : Si₃N₄ : Si ≈ 1 : >100 : 0,1')],
      # 7 — passivatsiya
      [chem('2Al + 6HF → 2AlF₃ + 3H₂↑'),
       seq('m(AlF₃) / m(Al) = 3,113;  m(FeF₃) / m(Fe) = 2,326'),
       seq('m(NiF₂) / m(Ni) = 1,647;  m(CuF₂) / m(Cu) = 1,598'),
       seq('Qatlam — zich fluorid plyonki: reaksiyani to‘xtatadi')],
      # 8 — floridlar
      [chem('Na₃AlF₆ (kriyolit): Al₂O₃ ning eritilishini ta’minlaydi'),
       seq(chem('Al³⁺ + 6F⁻ ⇌ [AlF₆]³⁻'), '   (barqaror kompleks)'),
       seq('Suv chegaralari:  WHO 1,5 mg/L · AQSh MCL 4,0 mg/L'),
       seq(chem('SiO₂ + 6HF → H₂SiF₆'), '   (suv tozalashda ishlatiladi)')],
      # 9 — sanoat
      [seq('Yarim o‘tkazgich: SiO₂ qatlami — ', var('m', ''), ' = ', var('r', ''), ' · τ'),
       seq('Maskalanish: SiO₂ : Si₃N₄ : Si ≈ 1 : >100 : 0,1'),
       seq('Optika: profil shakli materiallarning yemirilishiga bog‘liq'),
       seq('Farmatsevtika: flnor atomining metabolizmga ta’siri')],
      # 10 — xavfsizlik va chiqindi
      [seq(chem('2HF + Ca(OH)₂ → CaF₂↓ + 2H₂O')),
       seq('K', var('sp', ''), '(CaF₂) = 3,9×10⁻¹¹  ⇒  [F⁻] = ', var('√', ''),
           seq('(K', var('sp', ''), '/[Ca²⁺])')),
       seq('Taxminiy hisob: Ca²⁺ 0,010 M → [F⁻] = 1,186 mg/L (chegara 1,5 mg/L)'),
       seq(chem('2HF + Ca²⁺ → CaF₂'), '   (kalsiy bog‘lanishi)'),
       seq('Taxminiy hisob: 20 g HF → 0,500 mol Ca²⁺ → 224,1 g kalsiy glyukonat')],
      # 11 — ishlangan hisob
      [seq('A:  ', _h, ' = ', frac(seq('−', _ka, ' + ', var('√', ''),
           seq('(', _ka, '² + 4', _ka, _c, ')')), '2'), '  (yakka HF uchun)'),
       seq('A:  1,000 M → HF 89,5 % · F⁻ 1,1 % · HF₂⁻ 4,7 % · pH 1,238'),
       seq('B:  1 kg SiO₂ → HF 1997,8 g · H₂SiF₆ 2398,2 g · H₂O 599,6 g'),
       seq('C:  1000 kg 10 % HF → Ca(OH)₂ 185,2 kg · CaF₂ 195,1 kg'),
       seq('D:  20 g HF → Ca²⁺ 0,500 mol → kalsiy glyukonat 224,1 g')]
    ]
