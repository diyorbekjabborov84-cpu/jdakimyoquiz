#!/usr/bin/env python3
"""6.1 "Guruhning umumiy tavsifi" — taxminiy hisob ma'lumotlari va CSV jadvallar.

Barcha sonli natijalar ochiq shartli hisoblardir (o'lchov ma'lumoti emas).
Manbalar: OpenStax Chemistry 2e (7.5, 8.1, App. G), ChemGuide (gidratatsiya),
IUPAC/Gold Book va nashr jadvalari (S°, azeotroplar).
"""
from pathlib import Path
import csv, math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'galogenid'
ASSETS.mkdir(parents=True, exist_ok=True)

R = 8.314462618e-3          # kJ/(mol*K)
T0 = 298.15                # K
RT = R * T0                # kJ/mol

# ---------------------------------------------------------------- manba ma'lumotlari
# acid, M(HX), M(X), Pauling chi, r_cov(X) Angstrom, r_cov(H), r_exp(H-X) Angstrom,
# D(H-X) kJ/mol, EA(X) kJ/mol, dH_hyd(X-) kJ/mol, pKa suvda, pKa DMSO,
# mu (D), Tm, Tb, azeotrop %, azeotrop T, rho, dfH(g), dfG(g), S(g),
# dfH(X-,aq), dfG(X-,aq), S(X-,aq), Ka(suvda)
ACIDS = [
    dict(key='HF', name='F', full='Vodorod florid', hx='HF', m=20.006, mx=18.998,
         chi=3.98, rcov=0.57, rcov_h=0.31, rexp=0.917,
         d=569.0, ea=-328.0, hyd=-506.0, pka=3.17, pka_dmso=15.0,
         mu=1.82, tm=-83.6, tb=19.5, azeo=37.0, azeo_t=120.0, rho=1.15,
         dfh=-273.3, dfg=-275.4, s_g=173.8, dfh_ion=-332.6, dfg_ion=-278.8,
         s_ion=-13.8, ka=6.8e-4),
    dict(key='HCl', name='Cl', full='Vodorod xlorid', hx='HCl', m=36.461, mx=35.45,
         chi=3.16, rcov=1.02, rcov_h=0.31, rexp=1.2746,
         d=432.0, ea=-349.0, hyd=-364.0, pka=-5.9, pka_dmso=-2.0,
         mu=1.08, tm=-114.2, tb=-85.1, azeo=20.2, azeo_t=108.6, rho=1.102,
         dfh=-92.307, dfg=-95.299, s_g=186.9, dfh_ion=-167.2, dfg_ion=-131.2,
         s_ion=56.5, ka=1.3e6),
    dict(key='HBr', name='Br', full='Vodorod bromid', hx='HBr', m=80.912, mx=79.90,
         chi=2.96, rcov=1.20, rcov_h=0.31, rexp=1.414,
         d=370.0, ea=-324.0, hyd=-335.0, pka=-8.8, pka_dmso=-6.8,
         mu=0.82, tm=-86.9, tb=-66.8, azeo=47.6, azeo_t=124.3, rho=1.49,
         dfh=-36.3, dfg=-53.43, s_g=198.7, dfh_ion=-120.9, dfg_ion=-102.82,
         s_ion=80.71, ka=6.3e8),
    dict(key='HI', name='I', full='Vodorod iodid', hx='HI', m=127.912, mx=126.90,
         chi=2.66, rcov=1.39, rcov_h=0.31, rexp=1.609,
         d=295.0, ea=-295.0, hyd=-293.0, pka=-9.5, pka_dmso=-10.9,
         mu=0.44, tm=-50.8, tb=-35.4, azeo=56.9, azeo_t=127.0, rho=1.70,
         dfh=26.48, dfg=1.70, s_g=206.59, dfh_ion=-55.19, dfg_ion=-51.57,
         s_ion=11.13, ka=3.2e9),
]
BY_KEY = {a['key']: a for a in ACIDS}

# X2(g) standart Gibbs energiyasi (kJ/mol): F2 0, Cl2 0, Br2 3.142, I2 19.3
DFG_X2 = {'HF': 0.0, 'HCl': 0.0, 'HBr': 3.142, 'HI': 19.3}
# M va mol massalar
M_SIO2 = 60.08
M_H2SIOF6 = 144.09
M_CACO3 = 100.09
M_CACL2 = 110.98
M_CO2 = 44.01
M_H2O = 18.015
M_BR2 = 159.808
M_I2 = 253.81
M_O2 = 31.998
M_CAF2 = 78.074
M_CASO4 = 136.14
M_H2SO4 = 98.08
DH_SOLN_HCL = -74.8          # kJ/mol (suvga yotqizish)
KA_HF = 6.8e-4


# ---------------------------------------------------------------- taxminiy hisob funksiyalari
def acid(key):
    return BY_KEY[key]


def ka_from_pka(pka):
    return 10.0 ** (-pka)


def hf_equilibrium(c, ka=KA_HF):
    """HF dissotsiatsiyasi: x^2/(c-x) = Ka -> x = (-Ka + sqrt(Ka^2+4Ka*c))/2."""
    x = (-ka + math.sqrt(ka * ka + 4 * ka * c)) / 2.0
    return dict(c=c, x=x, pct=100.0 * x / c, ph=-math.log10(x))


def hf_ionisation_series(cs=(0.010, 0.050, 0.100, 0.500, 1.000)):
    return [hf_equilibrium(c) for c in cs]


def gas_to_ion(key):
    """HX(g) -> H+(aq) + X-(aq) uchun standart Gibbs energiyasi va K."""
    a = acid(key)
    dg = a['dfg_ion'] - a['dfg']
    k = math.exp(-dg / RT)
    return dict(dg=dg, k=k, log10k=dg and (-dg / (RT * math.log(10))))


def net_bond(key):
    """D(H-X) + gidratatsiya entalpiasi — kislotalikning energetik balansi."""
    a = acid(key)
    return a['d'] + a['hyd']


def oxidising_balance(key):
    """Atomlanish + elektron affinigi + gidratatsiya (galogenning oksidlovchi xarakteri)."""
    a = acid(key)
    atom = {'HF': 79.4, 'HCl': 121.3, 'HBr': 111.88, 'HI': 106.84}[key]
    return atom + a['ea'] + a['hyd']


def thermal_decomposition(key):
    """2HX(g) -> H2(g) + X2(g) uchun dG° va K (298.15 K)."""
    a = acid(key)
    dg = 0.0 + DFG_X2[key] - 2 * a['dfg']
    k = math.exp(-dg / RT)
    return dict(dg=dg, k=k, log10k=-dg / (RT * math.log(10)))


def glass_model(m_sio2=1.0, hf_pct=48.0):
    """SiO2 + 6HF -> H2SiF6 + 2H2O — shishani eritish uchun HF miqdori (shartli hisob)."""
    n_sio2 = m_sio2 * 1000.0 / M_SIO2
    n_hf = 6 * n_sio2
    m_hf = n_hf * BY_KEY['HF']['m']
    return dict(m_sio2=m_sio2, n_sio2=n_sio2, n_hf=n_hf, m_hf=m_hf,
                m_solution=m_hf / (hf_pct / 100.0),
                m_h2siof6=n_sio2 * M_H2SIOF6, m_h2o=2 * n_sio2 * M_H2O)


def neutralisation_model(m_solution=1000.0, pct=10.0):
    """2HCl + CaCO3 -> CaCl2 + CO2 + H2O — neytralizatsiya mass balansi."""
    a = acid('HCl')
    m_hcl = m_solution * pct / 100.0
    n_hcl = m_hcl * 1000.0 / a['m']
    n_caco3 = n_hcl / 2.0
    m_caco3 = n_caco3 * M_CACO3 / 1000.0
    m_cacl2 = n_caco3 * M_CACL2 / 1000.0
    m_co2 = n_caco3 * M_CO2 / 1000.0
    m_h2o = n_caco3 * M_H2O / 1000.0
    return dict(m_solution=m_solution, pct=pct, m_hcl=m_hcl, n_hcl=n_hcl,
                m_caco3=m_caco3, m_cacl2=m_cacl2, m_co2=m_co2, m_h2o=m_h2o,
                m_input=m_hcl + m_caco3, m_output=m_cacl2 + m_co2 + m_h2o)


def redox_model(m_hbr=1.0, m_hi=1.0):
    """2HBr + H2SO4 -> Br2 + SO2 + 2H2O;  4HI + O2 -> 2I2 + 2H2O (shartli hisob)."""
    n_hbr = m_hbr * 1000.0 / BY_KEY['HBr']['m']
    n_hi = m_hi * 1000.0 / BY_KEY['HI']['m']
    return dict(m_br2=n_hbr / 2 * M_BR2, m_i2=n_hi / 2 * M_I2,
                m_so2_hbr=n_hbr / 2 * M_CO2, m_so2_hi=n_hi / 2 * M_CO2,
                m_o2=n_hi / 4 * M_O2,
                m_h2o_hbr=n_hbr * M_H2O, m_h2o_hi=n_hi / 2 * M_H2O)


def azeotrope_model(m_solution=1000.0, pct=10.0):
    """Oddiy distillatsiya bilan HCl konsentratsiyasining chegarasi (azeotrop)."""
    a = acid('HCl')
    m_hcl = m_solution * pct / 100.0
    azeo = a['azeo']
    residue = m_hcl / (azeo / 100.0)
    return dict(m_solution=m_solution, pct=pct, m_hcl=m_hcl, azeo=azeo,
                azeo_t=a['azeo_t'], residue=residue,
                distilled_water=m_solution - residue,
                feasible=residue <= m_solution,
                note=('suv haydash mumkin' if residue <= m_solution
                      else 'suv haydash bilan mumkin emas — HCl gazi yutiladi'))


def absorption_heat():
    """HCl ning suvga yotqizish entalpisi (kJ/mol va kJ/kg)."""
    a = acid('HCl')
    return dict(dh_mol=DH_SOLN_HCL, dh_kg=DH_SOLN_HCL / (a['m'] / 1000.0))


def production_model(m_fluorspar=1000.0, purity=0.97, yield_pct=0.90):
    """CaF2 + H2SO4 -> 2HF + CaSO4: HF miqdori (shartli hisob)."""
    a = acid('HF')
    m_f2 = m_fluorspar * purity
    n_f2 = m_f2 * 1000.0 / M_CAF2
    m_hf = 2 * n_f2 * a['m'] / 1000.0 * yield_pct
    return dict(m_fluorspar=m_fluorspar, purity=purity, yield_pct=yield_pct,
                n_f2=n_f2, m_hf=m_hf, m_hf_pure=m_hf / yield_pct,
                m_h2so4=n_f2 * M_H2SO4 / 1000.0, m_caso4=n_f2 * M_CASO4 / 1000.0)


# ---------------------------------------------------------------- CSV yozuvchi
def write(name, header, data):
    with (ASSETS / (name + '.csv')).open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


def build_csvs():
    rows = []
    for a in ACIDS:
        rows.append([a['key'], a['pka'], a['pka_dmso'], a['ka'],
                     ka_from_pka(a['pka_dmso'])])
    write('kislotalik',
          ['acid', 'pKa_suv', 'pKa_DMSO', 'Ka_suv', 'Ka_DMSO'], rows)

    rows = []
    for a in ACIDS:
        g = gas_to_ion(a['key'])
        rows.append([a['key'], a['d'], a['ea'], a['hyd'], net_bond(a['key']),
                     oxidising_balance(a['key']), g['dg'], g['log10k']])
    write('energiya',
          ['acid', 'D_HX', 'EA_X', 'dH_hyd', 'D_plus_hyd', 'oks_balans', 'dG_gaz_ion', 'lgK_gaz_ion'], rows)

    rows = []
    for a in ACIDS:
        rows.append([a['key'], a['m'], a['mx'], a['chi'], a['rcov'] + a['rcov_h'],
                     a['rexp'], a['mu'], a['tm'], a['tb']])
    write('fizik',
          ['acid', 'M_HX', 'M_X', 'chi', 'r_sum', 'r_exp', 'mu_D', 'Tm_C', 'Tb_C'], rows)

    rows = []
    for a in ACIDS:
        c_mol = (a['azeo'] / 100.0) * a['rho'] / (a['m'] / 1000.0)
        rows.append([a['key'], a['azeo'], a['azeo_t'], a['rho'], a['tb'],
                     a['m'], c_mol])
    write('azeotrop',
          ['acid', 'azeotrop_pct', 'azeotrop_T_C', 'rho_g_ml', 'Tb_C', 'M_g_mol', 'c_mol_l'], rows)

    rows = []
    for r in hf_ionisation_series():
        rows.append([r['c'], r['x'], r['pct'], r['ph']])
    write('dissotsiatsiya', ['c_HF', 'x_H3O', 'ionizatsiya_pct', 'pH'], rows)

    rows = []
    for a in ACIDS:
        t = thermal_decomposition(a['key'])
        rows.append([a['key'], t['dg'], t['log10k'], a['dfh'], a['s_g'],
                     a['dfh_ion'], a['dfg_ion']])
    write('termik',
          ['acid', 'dG_dekomp', 'lgK_dekomp', 'dfH_gas', 'S_gas', 'dfH_ion', 'dfG_ion'], rows)
    return 6


def main():
    build_csvs()
    print('— kislotalik —')
    for a in ACIDS:
        g = gas_to_ion(a['key'])
        print('  %-4s pKa(suv)=%6.2f  pKa(DMSO)=%6.2f  K_gaz=%.3e  dG=%8.2f kJ/mol  net=%6.1f'
              % (a['key'], a['pka'], a['pka_dmso'], g['k'], g['dg'], net_bond(a['key'])))
    print('— HF muvozanati —')
    for r in hf_ionisation_series():
        print('  c=%.3f M  x=%.6f M  %.2f %%  pH=%.3f' % (r['c'], r['x'], r['pct'], r['ph']))
    print('— termik dekompozitsiya —')
    for a in ACIDS:
        t = thermal_decomposition(a['key'])
        print('  %-4s dG=%8.2f kJ/mol  lgK=%8.2f' % (a['key'], t['dg'], t['log10k']))
    print('— shisha taxminiy hisobi —')
    g = glass_model(1.0, 48.0)
    print('  1 kg SiO2 uchun HF: %.1f g (48 %% li eritmada %.1f g); H2SiF6 %.1f g'
          % (g['m_hf'], g['m_solution'], g['m_h2siof6']))
    print('— neytralizatsiya —')
    n = neutralisation_model(1000.0, 10.0)
    print('  1000 kg 10 %% HCl: CaCO3 %.1f kg, CaCl2 %.1f kg, CO2 %.1f kg, H2O %.1f kg (kirish %.1f = chiqish %.1f)'
          % (n['m_caco3'], n['m_cacl2'], n['m_co2'], n['m_h2o'], n['m_input'], n['m_output']))
    print('— redoks —')
    r = redox_model(1.0, 1.0)
    print('  1 kg HBr -> Br2 %.1f g;  1 kg HI -> I2 %.1f g; 1 kg HI uchun O2 %.2f g'
          % (r['m_br2'], r['m_i2'], r['m_o2']))
    print('— azeotrop —')
    for pct in (10.0, 37.0):
        z = azeotrope_model(1000.0, pct)
        print('  1000 kg %4.1f %% HCl -> qoldiq %.1f kg; suv haydami %.1f kg; mumkin: %s'
              % (pct, z['residue'], z['distilled_water'], z['feasible']))
    print('— yotqizish issig‘i —')
    ab = absorption_heat()
    print('  HCl: %.1f kJ/mol = %.0f kJ/kg' % (ab['dh_mol'], ab['dh_kg']))
    print('— olish taxminiy hisobi —')
    pr = production_model(1000.0, 0.97, 0.90)
    print('  1000 kg fluorit (97 %%): HF %.1f kg, H2SO4 %.1f kg, CaSO4 %.1f kg'
          % (pr['m_hf'], pr['m_h2so4'], pr['m_caso4']))
    print('CSV fayllar yozildi:', ', '.join(sorted(p.name for p in ASSETS.glob('*.csv'))))


if __name__ == '__main__':
    main()
