#!/usr/bin/env python3
"""6.5 "HI — yodid kislota" — taxminiy hisob ma'lumotlari va CSV jadvallar.

Barcha sonli natijalar ochiq shartli hisoblar (o'lchov ma'lumoti emas).
Manbalar: Wikipedia (Hydroiodic acid, Hydrogen iodide, Iodine, Iodine compounds),
ICSC 1326 (ILO/WHO), NOAA/NIOSH (IDLH 2025-109, AEGL), USGS/ATSDR (yod ishlab chiqarish).
"""
from pathlib import Path
import csv, math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'hi'
ASSETS.mkdir(parents=True, exist_ok=True)

# --- molar massalar (g/mol) -------------------------------------------------
M_HI = 127.9125
M_H2 = 2.016
M_I2 = 253.809
M_P = 30.974
M_H2O = 18.015
M_H3PO3 = 81.996
M_H2S = 34.081
M_N2H4 = 32.045
M_S = 32.06
M_NAI = 149.894
M_NACL = 58.44
M_CL2 = 70.906
M_NA2CO3 = 105.99
M_NACO3 = 105.99
M_CO2 = 44.009
M_KIO3 = 214.001
M_KI = 166.003
M_I = 126.9045
M_FE = 55.845
M_ZN = 65.38
M_AL = 26.9815
M_MG = 24.305
M_CU = 63.546
M_CH3OH = 32.042
M_CO = 28.010
M_CH3COOH = 60.052
M_H2SO4 = 98.079
M_HNO3 = 63.013
M_NO = 30.006
M_CA = 40.078
M_CAI2 = M_CA + 2 * M_I
M_CAOH2 = 74.093
M_O2 = 31.998

# --- kislota konstantalari --------------------------------------------------
PKA_HI = -9.5                  # suvda (6.1-bo'lim guruh jadvali)
KA_HI = 10 ** (-PKA_HI)        # 3,16·10^9
LOG_K_HI2 = 0.7                # HI + I- ⇌ HI2- (shartli hisob)
K_HI2 = 10 ** LOG_K_HI2
LOG_K_I3 = 2.845               # I2 + I- ⇌ I3- (K ≈ 700, 20 °C — manba)
K_I3 = 10 ** LOG_K_I3

# --- fizik konstantalar (nashr ma'lumotlari) --------------------------------
PHYS = dict(m=127.9125, tb=-35.36, tm=-50.80, tc=151.0, pc=8.31, rho_liq=2.85,
            rho_g25=5.229, d_air=4.4, vp_atm=7.81, sol20=42.0, sol10=234.0,
            dipole=0.45, r=1.609, d_bond=295.0, ie=10.39, s_g=206.6,
            dfh=26.5, dfg=1.7, cp=29.2, aze_pct=56.7, aze_tb=126.7, aze_rho=1.70,
            aze_c=7.56, conc_lo=48.0, conc_hi=57.0)

# eritma ma'lumotlari (nashr va kataloglar)
SOLUTIONS = [
    (48.0, 1.60, None, None, None, 'konsentratsiyalangan kislota chegarasi'),
    (56.7, 1.70, 7.56, 126.7, None, 'azeotrop (doimiy qaynash)'),
    (57.0, 1.70, None, 127.0, None, 'sanoat navi (Ullmann)'),
    (10.0, 1.07, 1.24, None, None, 'taxminiy hisob: 10 % li eritma'),
]

# guruh bo‘yicha ma’lumot (6.1-bo‘lim jadvali + o‘lchangan qo‘shimchalar)
GROUP = [
    # (simvol, D, pKa_suv, pKa_DMSO, aze_pct, aze_tb, tb, dipole, r_pm)
    ('HF', 569.0, 3.17, 15.0, 37.0, 120.0, 19.5, 1.83, 92.0),
    ('HCl', 432.0, -5.9, -2.0, 20.2, 108.6, -85.1, 1.11, 127.5),
    ('HBr', 366.0, -8.8, -6.8, 47.6, 124.3, -66.8, 0.83, 141.5),
    ('HI', 295.0, -9.5, -10.9, 56.7, 126.7, -35.4, 0.45, 161.0),
]

# --- metallar: HI bilan erishi --------------------------------------------
METALS = [
    dict(name='Fe', m=M_FE, salt='FeI₂', m_salt=M_FE + 2 * M_I, n_cl=2, h2=1.0, o2=False),
    dict(name='Zn', m=M_ZN, salt='ZnI₂', m_salt=M_ZN + 2 * M_I, n_cl=2, h2=1.0, o2=False),
    dict(name='Al', m=M_AL, salt='AlI₃', m_salt=M_AL + 3 * M_I, n_cl=3, h2=1.5, o2=False),
    dict(name='Mg', m=M_MG, salt='MgI₂', m_salt=M_MG + 2 * M_I, n_cl=2, h2=1.0, o2=False),
    dict(name='Cu', m=M_CU, salt='CuI₂', m_salt=M_CU + 2 * M_I, n_cl=2, h2=0.0, o2=True),
]


# ---------------------------------------------------------------- spetsiatsiya
def speciation(c, ka=KA_HI, kf=K_HI2):
    """Suvli HI: [H3O+], [I-], [HI], [HI2-] — ideal erituvchi sharoiti."""
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
                w_hi=100 * hcl / c_tot, w_i=100 * cl / c_tot, w_hi2=100 * cl2 / c_tot)


def speciation_series(cs=(0.10, 0.50, 1.0, 2.0, 4.0, 6.0, 7.56, 8.0, 10.0, 12.0)):
    return [speciation(c) for c in cs]


# ---------------------------------------------------------------- triiodid
def triiodide(c_i=7.56, m_i2=1.0, kf=K_I3):
    """I2 + I- ⇌ I3- (K ≈ 700): eritilgan I2 ning I3- ulushi."""
    v = m_i2 / M_I2                     # kmol I2 (1 L eritma)

    def f(y):
        return kf * (v - y) * (c_i - y) - y

    lo, hi = 0.0, v
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    y = (lo + hi) / 2.0
    x = v - y
    return dict(c_i=c_i, m_i2=m_i2, i2=x, i3=y,
                w_i3=100 * y / v if v else 0.0,
                w_i2=100 * x / v if v else 0.0)


def triiodide_series(cs=(0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 7.56, 10.0, 12.0), m_i2=1.0):
    return [triiodide(c, m_i2) for c in cs]


# ---------------------------------------------------------------- ishlab chiqarish
def direct_synthesis(m_hi=1000.0):
    """H2 + I2 ⇌ 2HI (qaytariluvchi, deyarli termoneutral) — taxminiy hisob."""
    n_hi = m_hi / M_HI
    dh = 2 * 26.5 - 62.44                      # kJ / 2 mol HI
    dg = 2 * 1.7 - 0.0                        # kJ / 2 mol HI
    k = math.exp(-dg * 1000.0 / (8.314 * 298.15))
    return dict(m_hi=m_hi, n_hi=n_hi,
                m_h2=0.5 * n_hi * M_H2, m_i2=0.5 * n_hi * M_I2,
                dh_kj=dh, dh_mj=dh / 2 * n_hi,
                dg_kj=dg, k_eq=k)


def hydrazine_method(m_hi=1000.0):
    """2I2 + N2H4 -> 4HI + N2 — sanoat usuli (shartli hisob)."""
    n_hi = m_hi / M_HI
    return dict(m_hi=m_hi, n_hi=n_hi,
                m_i2=0.5 * n_hi * M_I2, m_n2h4=0.25 * n_hi * M_N2H4,
                m_n2=0.25 * n_hi * 28.014)


def phosphorus_method(m_hi=1000.0):
    """3I2 + 2P + 6H2O -> 6HI + 2H3PO3 — laboratoriya usuli (shartli hisob)."""
    n_hi = m_hi / M_HI
    return dict(m_hi=m_hi, n_hi=n_hi,
                m_i2=0.5 * n_hi * M_I2, m_p=(1.0 / 3.0) * n_hi * M_P,
                m_h2o=n_hi * M_H2O, m_h3po3=(1.0 / 3.0) * n_hi * M_H3PO3)


def h2s_method(m_hi=1000.0):
    """H2S + I2 -> 2HI + S — tarixiy usul (shartli hisob)."""
    n_hi = m_hi / M_HI
    return dict(m_hi=m_hi, n_hi=n_hi,
                m_i2=0.5 * n_hi * M_I2, m_h2s=0.5 * n_hi * M_H2S,
                m_s=0.5 * n_hi * M_S)


def iodine_from_iodide(m_nai=1000.0):
    """2NaI + Cl2 -> 2NaCl + I2 (brindan yod olish) — taxminiy hisob."""
    n = m_nai / M_NAI
    return dict(m_nai=m_nai, n=n,
                m_cl2=0.5 * n * M_CL2, m_i2=0.5 * n * M_I2, m_nacl=n * M_NACL,
                m_input=m_nai + 0.5 * n * M_CL2,
                m_output=0.5 * n * M_I2 + n * M_NACL)


def oxidation_by_oxygen(m_hi=1000.0):
    """4HI + O2 -> 2I2 + 2H2O — taxminiy hisob (havo bilan oksidlanish)."""
    n_hi = m_hi / M_HI
    return dict(m_hi=m_hi, n_hi=n_hi,
                m_i2=0.5 * n_hi * M_I2, m_h2o=0.5 * n_hi * M_H2O,
                m_o2=0.25 * n_hi * M_O2)


def oxidation_by_nitric(m_hi=1000.0):
    """6HI + 2HNO3 -> 3I2 + 2NO + 4H2O — taxminiy hisob (kislota bilan oksidlanish)."""
    n_hi = m_hi / M_HI
    return dict(m_hi=m_hi, n_hi=n_hi,
                m_i2=0.5 * n_hi * M_I2, m_hno3=(1.0 / 3.0) * n_hi * M_HNO3,
                m_no=(1.0 / 3.0) * n_hi * M_NO, m_h2o=(2.0 / 3.0) * n_hi * M_H2O)


# ---------------------------------------------------------------- neytralizatsiya
def neutralisation(m_solution=1000.0, pct=10.0, agent='Na2CO3'):
    m_hi = m_solution * pct / 100.0
    n_hi = m_hi / M_HI
    if agent == 'Na2CO3':
        n_ag = n_hi / 2.0
        return dict(agent=agent, m_solution=m_solution, pct=pct, m_hi=m_hi,
                    n_hi=n_hi, m_agent=n_ag * M_NA2CO3, m_salt=n_hi * M_NAI,
                    m_gas=n_ag * M_CO2, m_h2o=n_ag * M_H2O,
                    m_input=m_hi + n_ag * M_NA2CO3,
                    m_output=n_hi * M_NAI + n_ag * M_CO2 + n_ag * M_H2O)
    n_ag = n_hi / 2.0
    return dict(agent=agent, m_solution=m_solution, pct=pct, m_hi=m_hi,
                n_hi=n_hi, m_agent=n_ag * M_CAOH2, m_salt=n_ag * M_CAI2,
                m_gas=0.0, m_h2o=n_hi * M_H2O,
                m_input=m_hi + n_ag * M_CAOH2,
                m_output=n_ag * M_CAI2 + n_hi * M_H2O)


def iodometry_sample(m_kio3=1.0):
    """IO3- + 5I- + 6H+ -> 3I2 + 3H2O: 1 g KIO3 dan ajraladigan I2 (shartli hisob)."""
    n = m_kio3 / M_KIO3
    n_i2 = 0.6 * n
    return dict(m_kio3=m_kio3, n=n, n_i2=n_i2, m_i2=n_i2 * M_I2,
                n_thio=2.0 * n_i2, m_thio=2.0 * n_i2 * 158.207)


def iodized_salt(m_salt=1000.0, mg_i_per_kg=30.0):
    """Yodlangan tuz: 1 t tuzga qo'shiladigan KI / KIO3 (shartli hisob)."""
    m_i_g = m_salt * mg_i_per_kg / 1000.0     # g I (1000 kg × 30 mg/kg = 30 g)
    return dict(m_salt=m_salt, mg_i_per_kg=mg_i_per_kg, m_i=m_i_g,
                m_ki=m_i_g * M_KI / M_I, m_kio3=m_i_g * M_KIO3 / M_I)


def titration_standardisation(m_naco3=0.2000, v_hi_ml=30.00):
    n_naco3 = m_naco3 / M_NACO3
    n_hi = 2.0 * n_naco3
    v_l = v_hi_ml / 1000.0
    return dict(m_naco3=m_naco3, n_naco3=n_naco3, n_hi=n_hi,
                v_hi_ml=v_hi_ml, c_hi=n_hi / v_l,
                m_hi_g=n_hi * M_HI, ph=-math.log10(n_hi / v_l))


# ---------------------------------------------------------------- metall yemirilishi
def metal_dissolution(m_metal=1.0):
    out = []
    for mt in METALS:
        n_metal = m_metal / mt['m']
        n_hi = mt['n_cl'] * n_metal
        n_h2 = mt['h2'] * n_metal
        n_o2 = 0.5 * n_metal if mt['o2'] else 0.0
        out.append(dict(metal=mt['name'], m_metal=m_metal, salt=mt['salt'],
                        m_salt=n_metal * mt['m_salt'], n_hi=n_hi,
                        m_hi=n_hi * M_HI, n_h2=n_h2, m_h2=n_h2 * M_H2,
                        m_o2=n_o2 * M_O2, need_o2=mt['o2']))
    return out


# ---------------------------------------------------------------- CSV yozuvchi
def write(name, header, data):
    with (ASSETS / (name + '.csv')).open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


def build_csvs():
    p = PHYS
    write('fizik_hi', ['parametr', 'qiymat', 'birlik'],
          [['molar mass', p['m'], 'g/mol'],
           ['qaynash harorati (1 atm)', p['tb'], '°C'],
           ['suyuqlash harorati', p['tm'], '°C'],
           ['kritik harorat', p['tc'], '°C'],
           ['kritik bosim', p['pc'], 'MPa'],
           ['suyuq zichligi (−47 °C)', p['rho_liq'], 'g/cm³'],
           ['gaz zichligi (25 °C, 1 atm)', p['rho_g25'], 'g/L'],
           ['nisbiy bug‘ zichligi (havoga nisbatan)', p['d_air'], ''],
           ['bug‘ bosimi (25 °C)', p['vp_atm'], 'atm'],
           ['eruvchanlik 20 °C', p['sol20'], 'g/100 mL'],
           ['eruvchanlik 10 °C', p['sol10'], 'g/100 mL'],
           ['bog‘ uzunligi r(H–I)', p['r'], 'Å'],
           ['bog‘ energiyasi D(H–I)', p['d_bond'], 'kJ/mol'],
           ['dipol moment', p['dipole'], 'D'],
           ['ionlanish potensiali', p['ie'], 'eV'],
           ['standart entropiya S°(g)', p['s_g'], 'J/(mol·K)'],
           ['ΔfH°(g)', p['dfh'], 'kJ/mol'],
           ['ΔfG°(g)', p['dfg'], 'kJ/mol'],
           ['moliyar issiqlik sig‘imi Cp', p['cp'], 'J/(mol·K)'],
           ['azeotrop konsentratsiyasi', p['aze_pct'], '%'],
           ['azeotrop qaynash harorati', p['aze_tb'], '°C'],
           ['azeotrop zichligi', p['aze_rho'], 'g/cm³'],
           ['azeotrop molyar konsentratsiyasi', p['aze_c'], 'mol/L'],
           ['konsentratsiyalangan kislota', '48–57 %', 'mass %']])

    rows = [[w, rho, c, bp, mp, src] for (w, rho, c, bp, mp, src) in SOLUTIONS]
    write('eritma', ['w_pct', 'rho', 'mol_L', 'tb_C', 'tm_C', 'manba'], rows)

    rows = [[s['c'], s['h'], s['cl'], s['hcl'], s['cl2'], s['ph'],
             s['w_hi'], s['w_i'], s['w_hi2']] for s in speciation_series()]
    write('spetsiatsiya', ['c_HI', 'h_H3O', 'i', 'hi', 'hi2', 'pH',
                           'w_hi_pct', 'w_i_pct', 'w_hi2_pct'], rows)

    rows = [list(g) for g in GROUP]
    write('guruh', ['kislota', 'D_kJ', 'pKa_suv', 'pKa_DMSO', 'aze_pct', 'aze_tb_C',
                    'tb_C', 'dipole_D', 'r_pm'], rows)

    ds = direct_synthesis(1000.0)
    hz = hydrazine_method(1000.0)
    ph = phosphorus_method(1000.0)
    hs = h2s_method(1000.0)
    ii = iodine_from_iodide(1000.0)
    o2 = oxidation_by_oxygen(1000.0)
    hn = oxidation_by_nitric(1000.0)
    rows = [['H₂ (to‘g‘ridan-to‘g‘ri usul)', ds['m_h2'], 'kg / 1000 kg HI'],
            ['I₂ (to‘g‘ridan-to‘g‘ri usul)', ds['m_i2'], 'kg / 1000 kg HI'],
            ['ΔrH (H₂ + I₂ ⇌ 2HI)', ds['dh_kj'], 'kJ / 2 mol HI'],
            ['K (298 K)', '%.3f' % ds['k_eq'], '—'],
            ['I₂ (gidrazin usuli)', hz['m_i2'], 'kg / 1000 kg HI'],
            ['N₂H₄ (gidrazin usuli)', hz['m_n2h4'], 'kg / 1000 kg HI'],
            ['I₂ (fosfor usuli)', ph['m_i2'], 'kg / 1000 kg HI'],
            ['P (fosfor usuli)', ph['m_p'], 'kg / 1000 kg HI'],
            ['H₂O (fosfor usuli)', ph['m_h2o'], 'kg / 1000 kg HI'],
            ['H₃PO₃ (fosfor usuli)', ph['m_h3po3'], 'kg / 1000 kg HI'],
            ['I₂ (H₂S usuli)', hs['m_i2'], 'kg / 1000 kg HI'],
            ['H₂S (H₂S usuli)', hs['m_h2s'], 'kg / 1000 kg HI'],
            ['NaI (yod olish sikli)', ii['m_nai'], 'kg / partiya'],
            ['Cl₂ (yod olish sikli)', ii['m_cl2'], 'kg / partiya'],
            ['I₂ (yod olish sikli)', ii['m_i2'], 'kg / partiya'],
            ['NaCl (yod olish sikli)', ii['m_nacl'], 'kg / partiya'],
            ['I₂ (O₂ bilan oksidlanish)', o2['m_i2'], 'kg / 1000 kg HI'],
            ['O₂ (O₂ bilan oksidlanish)', o2['m_o2'], 'kg / 1000 kg HI'],
            ['I₂ (HNO₃ bilan oksidlanish)', hn['m_i2'], 'kg / 1000 kg HI'],
            ['HNO₃ (HNO₃ bilan oksidlanish)', hn['m_hno3'], 'kg / 1000 kg HI']]
    write('ishlabchiqarish', ['element', 'miqdor', 'izoh'], rows)

    rows = []
    for md in metal_dissolution(1.0):
        rows.append([md['metal'], md['m_metal'], md['salt'], md['m_salt'],
                     md['m_hi'], md['m_h2'], md['m_o2']])
    write('metallar', ['metal', 'm_metal_g', 'salt', 'm_salt_g', 'm_HI_g', 'm_H2_g', 'm_O2_g'], rows)

    rows = []
    for tb in triiodide_series():
        rows.append([tb['c_i'], tb['m_i2'], tb['i2'], tb['i3'], tb['w_i3']])
    write('triiodid', ['c_I', 'm_I2_g', 'n_I2', 'n_I3', 'w_I3_pct'], rows)

    n1 = neutralisation(1000.0, 10.0, 'Na2CO3')
    n2 = neutralisation(1000.0, 10.0, 'Ca(OH)2')
    t = titration_standardisation(0.2000, 30.00)
    io = iodometry_sample(1.0)
    iz = iodized_salt(1000.0, 30.0)
    rows = [['HI (kirish)', n1['m_hi'], 'kg'],
            ['Na₂CO₃ (neytralizator)', n1['m_agent'], 'kg'],
            ['NaI (chiqish)', n1['m_salt'], 'kg'],
            ['CO₂ (chiqish)', n1['m_gas'], 'kg'],
            ['H₂O (chiqish)', n1['m_h2o'], 'kg'],
            ['Ca(OH)₂ (neytralizator)', n2['m_agent'], 'kg'],
            ['CaI₂ (chiqish)', n2['m_salt'], 'kg'],
            ['H₂O (Ca(OH)₂ bilan)', n2['m_h2o'], 'kg'],
            ['kirish (Na₂CO₃ bilan)', n1['m_input'], 'kg'],
            ['chiqish (Na₂CO₃ bilan)', n1['m_output'], 'kg'],
            ['standartlash: Na₂CO₃', t['m_naco3'], 'g'],
            ['standartlash: V(HI)', t['v_hi_ml'], 'mL'],
            ['standartlash: C(HI)', t['c_hi'], 'mol/L'],
            ['yodometriya: KIO₃ namuni', io['m_kio3'], 'g'],
            ['yodometriya: ajralgan I₂', io['m_i2'], 'g'],
            ['yodometriya: tiosulfat', io['m_thio'], 'g'],
            ['yodlangan tuz (1 t)', iz['m_salt'], 'kg'],
            ['yodlangan tuz: I miqdori', iz['m_i'], 'g'],
            ['yodlangan tuz: KI', iz['m_ki'], 'g'],
            ['yodlangan tuz: KIO₃', iz['m_kio3'], 'g']]
    write('chiqindi', ['element', 'miqdor', 'izoh'], rows)
    return 8


def main():
    build_csvs()
    print('— suvli HI spetsiatsiyasi (shartli hisob) —')
    for s in speciation_series():
        print('  c=%5.2f M  h=%.4f  I-=%.4f  HI=%.8f  HI2-=%.8f  pH=%7.3f  ulushlar: I- %6.3f %% HI2- %6.5f %%'
              % (s['c'], s['h'], s['cl'], s['hcl'], s['cl2'], s['ph'], s['w_i'], s['w_hi2']))
    ds = direct_synthesis(1000.0)
    print('— to‘g‘ridan-to‘g‘ri usul: H2 %.2f kg; I2 %.1f kg; ΔrH %.2f kJ (2 mol HI); K(298 K) = %.3f'
          % (ds['m_h2'], ds['m_i2'], ds['dh_kj'], ds['k_eq']))
    hz = hydrazine_method(1000.0)
    print('— gidrazin usuli: I2 %.1f kg; N2H4 %.1f kg' % (hz['m_i2'], hz['m_n2h4']))
    ph = phosphorus_method(1000.0)
    print('— fosfor usuli: I2 %.1f kg; P %.1f kg; H2O %.1f kg; H3PO3 %.1f kg'
          % (ph['m_i2'], ph['m_p'], ph['m_h2o'], ph['m_h3po3']))
    hs = h2s_method(1000.0)
    print('— H2S usuli: I2 %.1f kg; H2S %.1f kg; S %.1f kg' % (hs['m_i2'], hs['m_h2s'], hs['m_s']))
    ii = iodine_from_iodide(1000.0)
    print('— yod olish sikli: 1000 kg NaI + Cl2 %.1f kg -> I2 %.1f kg + NaCl %.1f kg (kirish %.1f = chiqish %.1f)'
          % (ii['m_cl2'], ii['m_i2'], ii['m_nacl'], ii['m_input'], ii['m_output']))
    o2 = oxidation_by_oxygen(1000.0); hn = oxidation_by_nitric(1000.0)
    print('— O2 bilan: I2 %.1f kg, O2 %.1f kg;  HNO3 bilan: I2 %.1f kg, HNO3 %.1f kg'
          % (o2['m_i2'], o2['m_o2'], hn['m_i2'], hn['m_hno3']))
    print('— metall yemirilishi (1 g metall) —')
    for md in metal_dissolution(1.0):
        extra = ' (O₂ kerak)' if md['need_o2'] else ''
        print('  %-3s -> %-6s %7.3f g tuz, HI %7.3f g, H2 %5.3f g%s'
              % (md['metal'], md['salt'], md['m_salt'], md['m_hi'], md['m_h2'], extra))
    n1 = neutralisation(1000.0, 10.0, 'Na2CO3'); n2 = neutralisation(1000.0, 10.0, 'Ca(OH)2')
    print('— neytralizatsiya: Na2CO3 %.1f kg; NaI %.1f kg; CO2 %.1f kg; H2O %.1f kg (kirish %.1f = chiqish %.1f)'
          % (n1['m_agent'], n1['m_salt'], n1['m_gas'], n1['m_h2o'], n1['m_input'], n1['m_output']))
    print('  Ca(OH)2 bilan: %.1f kg Ca(OH)2, %.1f kg CaI2, %.1f kg H2O (kirish %.1f = chiqish %.1f)'
          % (n2['m_agent'], n2['m_salt'], n2['m_h2o'], n2['m_input'], n2['m_output']))
    t = titration_standardisation(0.2000, 30.00)
    print('— standartlash: %.4f g Na2CO3, %.2f mL -> C(HI) = %.5f mol/L' % (t['m_naco3'], t['v_hi_ml'], t['c_hi']))
    io = iodometry_sample(1.0); iz = iodized_salt(1000.0, 30.0)
    print('— yodometriya: 1 g KIO3 -> I2 %.3f g; tiosulfat %.3f g' % (io['m_i2'], io['m_thio']))
    print('— yodlangan tuz: 1 t tuz + %.0f g I -> KI %.1f g yoki KIO3 %.1f g' % (iz['m_i'], iz['m_ki'], iz['m_kio3']))
    print('— triiodid (shartli hisob) —')
    for tb in triiodide_series():
        print('  [I-]=%5.2f M: I3- ulushi %6.2f %%' % (tb['c_i'], tb['w_i3']))
    print('CSV:', ', '.join(sorted(p.name for p in ASSETS.glob('*.csv'))))


if __name__ == '__main__':
    main()
