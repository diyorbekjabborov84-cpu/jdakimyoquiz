from book_equations import seq, var, frac, chem, par, sup, text

_xD = var('x', 'D')
_xB = var('x', 'B')
_ratio_term = seq('lg', par(seq(
    frac(_xD, seq('1 − ', _xD)),
    '·', frac(seq('1 − ', _xB), _xB))))


def preparation_equations():
    dg = sup('ΔG', '°'); dh = sup('ΔH', '°'); ds = sup('ΔS', '°')
    return [
      # 1 — umumiy sxema va unum tushunchasi
      [chem('Manba + reagent → kislota + yon mahsulot'),
       seq(text('η'), ' = ', frac(var('m', 'olingan'), var('m', 'nazariy')),
           ';   ', text('X'), ' = ', frac(var('n', 'reakt'), var('n', 'kir')))],
      # 2 — usullarning reaksion shablonlari
      [chem('H₂ + Cl₂ → 2HCl;   S + O₂ → SO₂'),
       chem('SO₃ + H₂O → H₂SO₄;   PCl₅ + 4H₂O → H₃PO₄ + 5HCl'),
       seq('Elektrokimyaviy usul:  ', text('m'), ' = ', frac(text('Q'), seq(text('z'), 'F')))],
      # 3 — termodinamik mezon
      [seq(dg, ' = ', dh, ' − T', ds),
       seq('ΔG = ', dg, ' + RT ln Q;   ', dg, ' = −RT ln K'),
       seq(var('ΔG', '°'), ' < 0  ⇔  K > 1')],
      # 4 — muvozanat va van 't Hoff
      [chem('N₂O₄ ⇌ 2 NO₂'),
       seq(var('K', 'p'), ' = ', frac(chem('(p(NO₂)/p°)²'), chem('p(N₂O₄)/p°'))),
       seq('ln(', frac(var('K', '2'), var('K', '1')), ') = −', frac(dh, 'R'),
           par(seq(frac('1', var('T', '2')), ' − ', frac('1', var('T', '1')))))],
      # 5 — kinetika
      [seq(text('k'), ' = A exp', par(seq('−', frac(var('E', 'a'), 'RT')))),
       seq(var('t', '½'), ' = ', frac('ln 2', text('k'))),
       seq('Tezlik chegarasi: reaksion bosqich yoki mass transfer')],
      # 6 — bloklar va kaskad
      [seq(var('X', 'umumiy'), ' = 1 − ', sup(par(seq('1 − ', var('x', '1'))), 'N')),
       seq(var('x', '1'), ' = 0,60:   N = 1 → 0,60;   N = 2 → 0,84;   N = 5 → 0,990'),
       seq(var('n', 'kir'), ' = ', var('n', 'reakt'), ' + ', var('n', 'qayt'))],
      # 7 — unum va chiqindi omili
      [seq(text('η'), ' = X · S = ', frac(var('m', 'haqiqiy'), var('m', 'nazariy'))),
       seq(var('E', 'chiq'), ' = ', frac(var('m', 'chiqindi'), var('m', 'mahsulot')),
           '   (kg/kg)'),
       seq('Atom iqtisodligi = 100 % · ',
           frac(var('m', 'kerakli mahsulot'), var('m', 'reagentlar')))],
      # 8 — ajratish
      [seq(text('α'), ' = ', frac(chem('(y₁/x₁)'), chem('(y₂/x₂)'))),
       seq(var('N', 'min'), ' = ', frac(_ratio_term, seq('lg ', text('α')))),
       seq(text('y'), ' = ', frac(text('α'), seq('1 + (', text('α'), ' − 1)', text('x'))),
           '   (muvozanat chizig‘i)')],
      # 9 — chiqindini ushlash
      [seq(var('n', 'yutilgan'), ' = ', var('V', 'gaz'), ' · ', var('y', 'ulushi'),
           ' · ', var('φ', 'yutilish')),
       seq(var('E', 'chiq'), ' = ', frac(var('m', 'chiqindi'), var('m', 'mahsulot'))),
       seq('Manbadan ushlash → yutish → tiklash yoki yo‘qotish')],
      # 10 — sifat ko‘rsatkichlari
      [seq(text('c'), ' = ', frac(var('n', 'titrant'), var('V', 'namuna'))),
       seq(text('w'), ' = ', frac(seq(text('c'), ' · ', text('M')), seq('1000 · ', text('ρ')))),
       seq('Titrlash — kislota miqdorining universal usuli')],
      # 11 — ishlangan hisob
      [seq('n(FeS₂) = 1000 t / 119,98 kg/kmol = 8334,72 kmol'),
       seq('n(SO₂) = 2 · n(FeS₂) = 16 669,44 kmol'),
       seq('n(SO₃) = 0,96 · n(SO₂) = 16 002,67 kmol'),
       seq('m(H₂SO₄) = 0,98 · n(SO₃) · 98,08 = 1538,15 t;   η = 0,9408')],
    ]
