#!/usr/bin/env python3
"""6.4 "HBr — bromid kislota" — taxminiy hisob ma'lumotlari va CSV jadvallar.

Barcha sonli natijalar ochiq shartli hisoblar (o'lchov ma'lumoti emas).
Manbalar: Wikipedia (Hydrobromic acid, Hydrogen bromide, Bromine), Air Liquide/NOAA/NIOSH
(kritik nuqta, chegara va IDLH), Cheméo (NIST termokimyoviy ma'lumot), USGS (bromin ishlab chiqarish).
"""
from pathlib import Path
import csv, math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'hbr'
ASSETS.mkdir(parents=True, exist_ok=True)

# --- molar massalar (g/mol) -------------------------------------------------
M_HBR = 80.912
M_H2 = 2.016
M_BR2 = 159.808
M_NABR = 102.894
M_NACL = 58.44
M_CL2 = 70.906
M_NA2CO3 = 105.99
M_CAOH2 = 74.093
M_CABR2 = 199.892
M_CO2 = 44.009
M_H2O = 18.015
M_H2O2 = 34.0147
M_FE = 55.845
M_ZN = 65.38
M_AL = 26.9815
M_MG = 24.305
M_CU = 63.546
M_BR = 79.904

# --- kislota konstantalari --------------------------------------------------
PKA_HBR = -8.8                  # suvda (6.1-bo'lim jadvali)
KA_HBR = 10 ** (-PKA_HBR)        # 6,31·10^8
LOG_K_HBR2 = 0.7                # HBr + Br- ⇌ HBr2- (shartli hisob)
K_HBR2 = 10 ** LOG_K_HBR2
LOG_K_BR3 = 1.2                 # Br2 + Br- ⇌ Br3- (shartli hisob)
K_BR3 = 10 ** LOG_K_BR3

# --- fizik konstantalar (nashr ma'lumotlari) --------------------------------
PHYS = dict(m=80.912, tb=-66.8, tm=-86.9, tc=89.8, pc=85.0, rho_c=807.0,
            triple_t=186.2, triple_p=0.299, rho_g25=3.307, d_air=2.71,
            dipole=0.8272, r=1.414, d_bond=366.0, ie=11.66, s_g=198.70,
            sol0=221.0, sol15=204.0, sol100=130.0, sat=68.85,
            aze_pct=47.6, aze_tb=124.3, aze_c=8.77, aze_rho=1.49,
            rho48=1.49, mp48=-11.0, bp48=126.0)

# eritma ma'lumotlari (nashr: hujjat va kataloglar)
SOLUTIONS = [
    # (w %, rho, mol/L, bp_C, mp_C, manba)
    (40, 1.38, 7.0, None, None, 'katalog ma’lumoti'),
    (47.6, 1.49, 8.77, 124.3, -11.0, 'azeotrop (doimiy qaynash)'),
    (48, 1.49, 8.8, 126.0, -11.0, 'sanoat navi'),
    (68.85, None, None, None, None, 'to‘yingan eritma (xona harorati)'),
]

# guruh bo‘yicha ma’lumot (6.1-bo‘lim jadvali)
GROUP = [
    # (simvol, D, pKa_suv, pKa_DMSO, aze_pct, aze_tb, tb)
    ('HF', 569.0, 3.17, 15.0, 37.0, 120.0, 19.5),
    ('HCl', 432.0, -5.9, -2.0, 20.2, 108.6, -85.1),
    ('HBr', 366.0, -8.8, -6.8, 47.6, 124.3, -66.8),
    ('HI', 295.0, -9.5, -10.9, 56.9, 127.0, -35.4),
]

# --- metallar: HBr bilan erishi --------------------------------------------
METALS = [
    dict(name='Fe', m=M_FE, salt='FeBr₂', m_salt=M_FE + 2 * M_BR, n_cl=2, h2=1.0, o2=False),
    dict(name='Zn', m=M_ZN, salt='ZnBr₂', m_salt=M_ZN + 2 * M_BR, n_cl=2, h2=1.0, o2=False),
    dict(name='Al', m=M_AL, salt='AlBr₃', m_salt=M_AL + 3 * M_BR, n_cl=3, h2=1.5, o2=False),
    dict(name='Mg', m=M_MG, salt='MgBr₂', m_salt=M_MG + 2 * M_BR, n_cl=2, h2=1.0, o2=False),
    dict(name='Cu', m=M_CU, salt='CuBr₂', m_salt=M_CU + 2 * M_BR, n_cl=2, h2=0.0, o2=True),
]


# ---------------------------------------------------------------- spetsiatsiya
def speciation(c, ka=KA_HBR, kf=K_HBR2):
    """Suvli HBr: [H3O+], [Br-], [HBr], [HBr2-] — ideal erituvchi sharoiti."""
    def cl_of_h(h):
        a = kf * h / ka
        return 2.0 * h / (1.0 + math.sqrt(1.0 + 4.0 * a * h))

    def total(h):
        cl = cl_of_h(h)
        hcl = h * cl / ka
        cl2 = kf * hcl * cl
        return hcl + cl + 2.0 * cl2, cl, hcl, cl2

    lo, hi = 1e-14, 60.0
    for _ in range(300):
        mid = (lo + hi) / 2.0
        if total(mid)[0] < c:
            lo = mid
        else:
            hi = mid
    h = (lo + hi) / 2.0
    c_tot, cl, hcl, cl2 = total(h)
    return dict(c=c, h=h, cl=cl, hcl=hcl, cl2=cl2,
                ph=-math.log10(h),
                w_hbr=100 * hcl / c_tot, w_br=100 * cl / c_tot, w_hbr2=100 * cl2 / c_tot)


def speciation_series(cs=(0.10, 0.50, 1.0, 2.0, 4.0, 6.0, 8.0, 8.77, 10.0, 12.0)):
    return [speciation(c) for c in cs]


# ---------------------------------------------------------------- tribromid
def tribromide(c_br=8.77, m_br2=1.0, kf=K_BR3):
    """Br2 + Br- ⇌ Br3- (shartli hisob): eritilgan Br2 ning Br3- ulushi.

    Balans: x + y = v (eritilgan Br2), y = kf·x·(c_br − y).
    y ∈ [0, v] oralig‘ida bisеksiya bilan yechiladi.
    """
    v = m_br2 / M_BR2                     # kmol Br2 (1 L eritma)

    def f(y):
        return kf * (v - y) * (c_br - y) - y

    lo, hi = 0.0, v
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    y = (lo + hi) / 2.0                   # n(Br3-)
    x = v - y                             # n(Br2, erkin)
    return dict(c_br=c_br, m_br2=m_br2, br2=x, br3=y,
                w_br3=100 * y / v if v else 0.0,
                w_br2=100 * x / v if v else 0.0)


def tribromide_series(cs=(0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 8.77, 10.0, 12.0), m_br2=1.0):
    return [tribromide(c, m_br2) for c in cs]


# ---------------------------------------------------------------- ishlab chiqarish
def synthesis(m_hbr=1000.0):
    """H2 + Br2 -> 2HBr (200-400 °C, Pt katalizatori) — taxminiy hisob."""
    n_hbr = m_hbr / M_HBR                      # kmol
    return dict(m_hbr=m_hbr, n_hbr=n_hbr,
                m_h2=0.5 * n_hbr * M_H2,          # kg
                m_br2=0.5 * n_hbr * M_BR2,        # kg
                dh_mj=51.745 * n_hbr)              # MJ (eksotermik)


def lab_method(m_hbr=1000.0):
    """Br2 + SO2 + 2H2O -> H2SO4 + 2HBr — taxminiy hisob."""
    n_hbr = m_hbr / M_HBR
    n_br2 = 0.5 * n_hbr
    return dict(m_hbr=m_hbr, n_hbr=n_hbr,
                m_br2=n_br2 * M_BR2, m_so2=n_br2 * 64.066, m_h2o=n_br2 * 2 * M_H2O,
                m_h2so4=0.5 * n_hbr * 98.079)


def bromide_oxidation(m_nabr=1000.0):
    """2NaBr + Cl2 -> 2NaCl + Br2 (bromin ishlab chiqarish) — taxminiy hisob."""
    n = m_nabr / M_NABR                       # kmol
    m_br2 = 0.5 * n * M_BR2
    m_cl2 = 0.5 * n * M_CL2
    m_nacl = n * M_NACL
    return dict(m_nabr=m_nabr, n=n, m_br2=m_br2, m_cl2=m_cl2, m_nacl=m_nacl,
                m_input=m_nabr + m_cl2, m_output=m_br2 + m_nacl)


def h2o2_bromination(m_hbr=1000.0):
    """2HBr + H2O2 -> Br2 + 2H2O — taxminiy hisob (aromatik bromlanish uchun)."""
    n_hbr = m_hbr / M_HBR
    n_h2o2 = 0.5 * n_hbr
    return dict(m_hbr=m_hbr, n_hbr=n_hbr,
                m_h2o2=n_h2o2 * M_H2O2, m_br2=0.5 * n_hbr * M_BR2,
                m_h2o=n_hbr * M_H2O)


def oxidation_by_oxygen(m_hbr=1000.0):
    """4HBr + O2 -> 2Br2 + 2H2O — taxminiy hisob (termofil/katalitik yo'l)."""
    n_hbr = m_hbr / M_HBR
    return dict(m_hbr=m_hbr, n_hbr=n_hbr,
                m_br2=0.5 * n_hbr * M_BR2, m_h2o=0.5 * n_hbr * M_H2O,
                m_o2=0.25 * n_hbr * 31.998)


# ---------------------------------------------------------------- neytralizatsiya
def neutralisation(m_solution=1000.0, pct=10.0, agent='Na2CO3'):
    m_hbr = m_solution * pct / 100.0
    n_hbr = m_hbr / M_HBR                     # kmol
    if agent == 'Na2CO3':
        n_ag = n_hbr / 2.0
        return dict(agent=agent, m_solution=m_solution, pct=pct, m_hbr=m_hbr,
                    n_hbr=n_hbr, m_agent=n_ag * M_NA2CO3, m_salt=n_hbr * M_NABR,
                    m_gas=n_ag * M_CO2, m_h2o=n_ag * M_H2O,
                    m_input=m_hbr + n_ag * M_NA2CO3,
                    m_output=n_hbr * M_NABR + n_ag * M_CO2 + n_ag * M_H2O)
    n_ag = n_hbr / 2.0
    return dict(agent=agent, m_solution=m_solution, pct=pct, m_hbr=m_hbr,
                n_hbr=n_hbr, m_agent=n_ag * M_CAOH2, m_salt=n_ag * M_CABR2,
                m_gas=0.0, m_h2o=n_hbr * M_H2O,
                m_input=m_hbr + n_ag * M_CAOH2,
                m_output=n_ag * M_CABR2 + n_hbr * M_H2O)


def titration_standardisation(m_naco3=0.2000, v_hbr_ml=30.00):
    n_naco3 = m_naco3 / M_NA2CO3
    n_hbr = 2.0 * n_naco3
    v_l = v_hbr_ml / 1000.0
    return dict(m_naco3=m_naco3, n_naco3=n_naco3, n_hbr=n_hbr,
                v_hbr_ml=v_hbr_ml, c_hbr=n_hbr / v_l,
                m_hbr_g=n_hbr * M_HBR, ph=-math.log10(n_hbr / v_l))


# ---------------------------------------------------------------- metall yemirilishi
def metal_dissolution(m_metal=1.0):
    out = []
    for mt in METALS:
        n_metal = m_metal / mt['m']
        n_hbr = mt['n_cl'] * n_metal
        n_h2 = mt['h2'] * n_metal
        n_o2 = 0.5 * n_metal if mt['o2'] else 0.0
        out.append(dict(metal=mt['name'], m_metal=m_metal, salt=mt['salt'],
                        m_salt=n_metal * mt['m_salt'], n_hbr=n_hbr,
                        m_hbr=n_hbr * M_HBR, n_h2=n_h2, m_h2=n_h2 * M_H2,
                        m_o2=n_o2 * 31.998, need_o2=mt['o2']))
    return out


# ---------------------------------------------------------------- CSV yozuvchi
def write(name, header, data):
    with (ASSETS / (name + '.csv')).open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


def build_csvs():
    p = PHYS
    write('fizik_hbr', ['parametr', 'qiymat', 'birlik'],
          [['molar mass', p['m'], 'g/mol'],
           ['qaynash harorati (1 atm)', p['tb'], '°C'],
           ['suyuqlash harorati', p['tm'], '°C'],
           ['triya nuqtasi harorati', p['triple_t'], 'K'],
           ['triya nuqtasi bosimi', p['triple_p'], 'bar'],
           ['kritik harorat', p['tc'], '°C'],
           ['kritik bosim', p['pc'], 'bar'],
           ['kritik zichlik', p['rho_c'], 'kg/m³'],
           ['gaz zichligi (25 °C, 1 atm)', p['rho_g25'], 'g/L'],
           ['nisbiy gaz zichligi (havoga nisbatan)', p['d_air'], ''],
           ['bog‘ uzunligi r(H–Br)', p['r'], 'Å'],
           ['bog‘ energiyasi D(H–Br)', p['d_bond'], 'kJ/mol'],
           ['dipol moment', p['dipole'], 'D'],
           ['ionlanish potensiali', p['ie'], 'eV'],
           ['standart entropiya S°(g)', p['s_g'], 'J/(mol·K)'],
           ['eruvchanlik 0 °C', p['sol0'], 'g/100 mL'],
           ['eruvchanlik 15 °C', p['sol15'], 'g/100 mL'],
           ['eruvchanlik 100 °C', p['sol100'], 'g/100 mL'],
           ['to‘yingan eritma (xona harorati)', p['sat'], '%'],
           ['azeotrop konsentratsiyasi', p['aze_pct'], '%'],
           ['azeotrop qaynash harorati', p['aze_tb'], '°C'],
           ['azeotrop molyar konsentratsiyasi', p['aze_c'], 'mol/L']])

    rows = [[w, rho, c, bp, mp, src] for (w, rho, c, bp, mp, src) in SOLUTIONS]
    write('eritma', ['w_pct', 'rho', 'mol_L', 'tb_C', 'tm_C', 'manba'], rows)

    rows = [[s['c'], s['h'], s['cl'], s['hcl'], s['cl2'], s['ph'],
             s['w_hbr'], s['w_br'], s['w_hbr2']] for s in speciation_series()]
    write('spetsiatsiya', ['c_HBr', 'h_H3O', 'br', 'hbr', 'hbr2', 'pH',
                           'w_hbr_pct', 'w_br_pct', 'w_hbr2_pct'], rows)

    rows = []
    for g in GROUP:
        rows.append([g[0], g[1], g[2], g[3], g[4], g[5], g[6]])
    write('guruh', ['kislota', 'D_kJ', 'pKa_suv', 'pKa_DMSO',
                    'aze_pct', 'aze_tb_C', 'tb_C'], rows)

    sy = synthesis(1000.0)
    lb = lab_method(1000.0)
    bo = bromide_oxidation(1000.0)
    rows = [['H₂ (sintetik usul)', sy['m_h2'], 'kg / 1000 kg HBr'],
            ['Br₂ (sintetik usul)', sy['m_br2'], 'kg / 1000 kg HBr'],
            ['ΔrH (H₂ + Br₂ → 2HBr)', sy['dh_mj'], 'MJ / 1000 kg HBr'],
            ['Br₂ (laboratoriya usuli)', lb['m_br2'], 'kg / 1000 kg HBr'],
            ['SO₂ (laboratoriya usuli)', lb['m_so2'], 'kg / 1000 kg HBr'],
            ['H₂SO₄ (laboratoriya usuli)', lb['m_h2so4'], 'kg / 1000 kg HBr'],
            ['NaBr (bromin sikli)', bo['m_nabr'], 'kg / partiya'],
            ['Cl₂ (bromin sikli)', bo['m_cl2'], 'kg / partiya'],
            ['Br₂ (bromin sikli)', bo['m_br2'], 'kg / partiya'],
            ['NaCl (bromin sikli)', bo['m_nacl'], 'kg / partiya'],
            ['Br₂ (H₂O₂ bilan)', h2o2_bromination(1000.0)['m_br2'], 'kg / 1000 kg HBr'],
            ['Br₂ (O₂ bilan)', oxidation_by_oxygen(1000.0)['m_br2'], 'kg / 1000 kg HBr']]
    write('ishlabchiqarish', ['element', 'miqdor', 'izoh'], rows)

    rows = []
    for md in metal_dissolution(1.0):
        rows.append([md['metal'], md['m_metal'], md['salt'], md['m_salt'],
                     md['m_hbr'], md['m_h2'], md['m_o2']])
    write('metallar', ['metal', 'm_metal_g', 'salt', 'm_salt_g', 'm_HBr_g', 'm_H2_g', 'm_O2_g'], rows)

    n1 = neutralisation(1000.0, 10.0, 'Na2CO3')
    n2 = neutralisation(1000.0, 10.0, 'Ca(OH)2')
    t = titration_standardisation(0.2000, 30.00)
    rows = [['HBr (kirish)', n1['m_hbr'], 'kg'],
            ['Na₂CO₃ (neytralizator)', n1['m_agent'], 'kg'],
            ['NaBr (chiqish)', n1['m_salt'], 'kg'],
            ['CO₂ (chiqish)', n1['m_gas'], 'kg'],
            ['H₂O (chiqish)', n1['m_h2o'], 'kg'],
            ['Ca(OH)₂ (neytralizator)', n2['m_agent'], 'kg'],
            ['CaBr₂ (chiqish)', n2['m_salt'], 'kg'],
            ['H₂O (Ca(OH)₂ bilan)', n2['m_h2o'], 'kg'],
            ['kirish (Na₂CO₃ bilan)', n1['m_input'], 'kg'],
            ['chiqish (Na₂CO₃ bilan)', n1['m_output'], 'kg'],
            ['standartlash: Na₂CO₃', t['m_naco3'], 'g'],
            ['standartlash: V(HBr)', t['v_hbr_ml'], 'mL'],
            ['standartlash: C(HBr)', t['c_hbr'], 'mol/L']]
    write('chiqindi', ['element', 'miqdor', 'izoh'], rows)

    rows = []
    for tb in tribromide_series():
        rows.append([tb['c_br'], tb['m_br2'], tb['br2'], tb['br3'], tb['w_br3']])
    write('tribromid', ['c_Br', 'm_Br2_g', 'n_Br2', 'n_Br3', 'w_Br3_pct'], rows)
    return 7


def main():
    build_csvs()
    print('— suvli HBr spetsiatsiyasi (shartli hisob) —')
    for s in speciation_series():
        print('  c=%5.2f M  h=%.4f  Br-=%.4f  HBr=%.6f  HBr2-=%.6f  pH=%7.3f  ulushlar: Br- %6.3f %% HBr2- %6.4f %%'
              % (s['c'], s['h'], s['cl'], s['hcl'], s['cl2'], s['ph'], s['w_br'], s['w_hbr2']))
    sy = synthesis(1000.0)
    print('— sintetik usul: H2 %.2f kg; Br2 %.1f kg; ΔrH %.1f MJ' % (sy['m_h2'], sy['m_br2'], sy['dh_mj']))
    lb = lab_method(1000.0)
    print('— laboratoriya usuli: Br2 %.1f kg; SO2 %.1f kg; H2SO4 %.1f kg' % (lb['m_br2'], lb['m_so2'], lb['m_h2so4']))
    bo = bromide_oxidation(1000.0)
    print('— bromin sikli: 1000 kg NaBr + Cl2 %.1f kg -> Br2 %.1f kg + NaCl %.1f kg (kirish %.1f = chiqish %.1f)'
          % (bo['m_cl2'], bo['m_br2'], bo['m_nacl'], bo['m_input'], bo['m_output']))
    h2 = h2o2_bromination(1000.0)
    print('— H2O2 bilan: 1000 kg HBr -> H2O2 %.1f kg; Br2 %.1f kg' % (h2['m_h2o2'], h2['m_br2']))
    o2 = oxidation_by_oxygen(1000.0)
    print('— O2 bilan: 1000 kg HBr -> Br2 %.1f kg; O2 %.1f kg' % (o2['m_br2'], o2['m_o2']))
    print('— metall yemirilishi (1 g metall) —')
    for md in metal_dissolution(1.0):
        extra = ' (O₂ kerak)' if md['need_o2'] else ''
        print('  %-3s -> %-6s %7.3f g tuz, HBr %7.3f g, H2 %5.3f g%s'
              % (md['metal'], md['salt'], md['m_salt'], md['m_hbr'], md['m_h2'], extra))
    n1 = neutralisation(1000.0, 10.0, 'Na2CO3')
    n2 = neutralisation(1000.0, 10.0, 'Ca(OH)2')
    print('— neytralizatsiya: Na2CO3 %.1f kg; NaBr %.1f kg; CO2 %.1f kg; H2O %.1f kg (kirish %.1f = chiqish %.1f)'
          % (n1['m_agent'], n1['m_salt'], n1['m_gas'], n1['m_h2o'], n1['m_input'], n1['m_output']))
    print('  Ca(OH)2 bilan: Ca(OH)2 %.1f kg; CaBr2 %.1f kg; H2O %.1f kg (kirish %.1f = chiqish %.1f)'
          % (n2['m_agent'], n2['m_salt'], n2['m_h2o'], n2['m_input'], n2['m_output']))
    t = titration_standardisation(0.2000, 30.00)
    print('— standartlash: %.4f g Na2CO3, V(HBr) %.2f mL -> C(HBr) = %.5f mol/L' % (t['m_naco3'], t['v_hbr_ml'], t['c_hbr']))
    print('— tribromid (shartli hisob) —')
    for tb in tribromide_series():
        print('  [Br-]=%5.2f M: Br3- ulushi %6.2f %%' % (tb['c_br'], tb['w_br3']))
    print('CSV:', ', '.join(sorted(p.name for p in ASSETS.glob('*.csv'))))


if __name__ == '__main__':
    main()
