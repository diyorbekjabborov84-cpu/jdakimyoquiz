#!/usr/bin/env python3
"""6.3 "HCl — xlorid kislota" — taxminiy hisob ma'lumotlari va CSV jadvallar.

Barcha sonli natijalar ochiq shartli hisoblar (o'lchov ma'lumoti emas).
Manbalar: Wikipedia (Hydrochloric acid — fizik jadval, ishlab chiqarish, qo'llanish),
Air Liquide / Messer / Cheméo (kritik nuqta), OSHA va NIOSH (chegaralar),
IPSI-2021 (spray roasting), Unipa (pickling koeffitsiyentlari), JACS (xloroaluminat).
"""
from pathlib import Path
import csv, math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'hcl'
ASSETS.mkdir(parents=True, exist_ok=True)

# --- molar massalar (g/mol) -------------------------------------------------
M_HCL = 36.461
M_NACL = 58.44
M_H2SO4 = 98.079
M_NA2SO4 = 142.04
M_NA2CO3 = 105.99
M_CACO3 = 100.086
M_CACL2 = 110.98
M_CAOH2 = 74.093
M_H2O = 18.015
M_O2 = 31.998
M_FE = 55.845
M_ZN = 65.38
M_AL = 26.9815
M_MG = 24.305
M_CU = 63.546
M_FECL2 = 126.751
M_FE2O3 = 159.688
M_CO2 = 44.009
M_NA2CO3_H2O = 226.0   # kristall soda (ikkilanma)

# --- kislota konstantalari --------------------------------------------------
PKA_HCL = -5.9                 # suvda, nazariy baho (Wikipedia/Trummal)
KA_HCL = 10 ** (-PKA_HCL)      # 7,9·10^5
LOG_K_CL2 = 0.7                # HCl + Cl- ⇌ HCl2- (taxminiy hisob; HF2- ga o'xshash)
K_CL2 = 10 ** LOG_K_CL2

# --- fizik konstantalar (nashr ma'lumotlari) --------------------------------
PHYS = dict(m=36.461, tb=-85.05, tm=-114.22, tc=51.4, pc=83.1, rho_c=450.14,
            triple_t=158.96, triple_p=0.138, rho_g0=1.627, rho_g15=1.534,
            d_air=1.2702, s_g=186.90, dh_f=-92.31, sol=720.0,
            aze_pct=20.2, aze_tb=108.6, aze_rho=1.0959)

# eritma jadvali: 20 °C, 1 atm (International Critical Tables; Wikipedia)
SOLUTIONS = [
    # (w %, kg/m3, mol/L, Baume, rho, pH, visc, cp, vp, tb, tm)
    (10, 104.80, 2.87, 6.6, 1.048, -0.5, 1.16, 3.47, 1.95, 103, -18),
    (20, 219.60, 6.02, 13, 1.098, -0.8, 1.37, 2.99, 1.40, 108, -59),
    (30, 344.70, 9.45, 19, 1.149, -1.0, 1.70, 2.60, 2.13, 90, -52),
    (32, 370.88, 10.17, 20, 1.159, -1.0, 1.80, 2.55, 3.73, 84, -43),
    (34, 397.46, 10.90, 21, 1.169, -1.0, 1.90, 2.50, 7.24, 71, -36),
    (36, 424.44, 11.64, 22, 1.179, -1.1, 1.99, 2.46, 14.5, 61, -30),
    (38, 451.82, 12.39, 23, 1.189, -1.1, 2.10, 2.43, 28.3, 48, -26),
]

# --- metallar: HCl bilan erishi --------------------------------------------
# (nom, M, tuz, n_salt, n_h2, kislorod bilan)
METALS = [
    dict(name='Fe', m=M_FE, salt='FeCl₂', m_salt=126.751, n_cl=2, h2=1.0, o2=False),
    dict(name='Zn', m=M_ZN, salt='ZnCl₂', m_salt=136.28, n_cl=2, h2=1.0, o2=False),
    dict(name='Al', m=M_AL, salt='AlCl₃', m_salt=133.34, n_cl=3, h2=1.5, o2=False),
    dict(name='Mg', m=M_MG, salt='MgCl₂', m_salt=95.21, n_cl=2, h2=1.0, o2=False),
    dict(name='Cu', m=M_CU, salt='CuCl₂', m_salt=134.45, n_cl=2, h2=0.0, o2=True),
]


# ---------------------------------------------------------------- spetsiatsiya
def speciation(c, ka=KA_HCL, kf=K_CL2):
    """Suvli HCl: [H3O+], [Cl-], [HCl], [HCl2-] — ideal erituvchi sharoiti.

    Ka = h*cl/[HCl];  HCl + Cl- ⇌ HCl2- (Kf);  zaryad h = cl + [HCl2-].
    """
    def cl_of_h(h):
        # a·f² + f − h = 0  →  f = 2h/(1 + sqrt(1+4a·h))  (rational shakl, beqaror)
        a = kf * h / ka
        return 2.0 * h / (1.0 + math.sqrt(1.0 + 4.0 * a * h))

    def total(h):
        cl = cl_of_h(h)
        hcl = h * cl / ka
        cl2 = kf * hcl * cl
        return hcl + cl + 2.0 * cl2, cl, hcl, cl2

    lo, hi = 1e-14, 50.0
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
                w_hcl=100 * hcl / c_tot, w_cl=100 * cl / c_tot, w_cl2=100 * cl2 / c_tot)


def speciation_series(cs=(0.10, 0.50, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0)):
    return [speciation(c) for c in cs]


# ---------------------------------------------------------------- ishlab chiqarish
def mannheim(m_hcl=1000.0, yield_pct=0.98):
    """2NaCl + H2SO4 -> Na2SO4 + 2HCl (Mannheim/so'k usuli) — taxminiy hisob."""
    n_hcl = m_hcl / M_HCL                      # kmol
    m_nacl = n_hcl * M_NACL                    # kg  (n(NaCl) = n(HCl))
    m_h2so4 = 0.5 * n_hcl * M_H2SO4            # kg
    m_na2so4 = 0.5 * n_hcl * M_NA2SO4          # kg
    # Delta_rH (standart hosil entalpiyalaridan): +64,52 kJ / 2 mol HCl
    dh = 32.26 * n_hcl                          # MJ (32,26 MJ/kmol HCl)
    m_hcl_ideal = m_hcl / yield_pct
    return dict(m_hcl=m_hcl, yield_pct=yield_pct, n_hcl=n_hcl,
                m_nacl=m_nacl, m_h2so4=m_h2so4, m_na2so4=m_na2so4,
                m_hcl_ideal=m_hcl_ideal,
                m_nacl_ideal=m_hcl_ideal / M_HCL * M_NACL,
                dh_mj=dh, dh_kj_per_mol=64.52 / 2.0)


def synthesis(m_hcl=1000.0):
    """H2 + Cl2 -> 2HCl (HCl pechi) — taxminiy hisob: xom ashyosiz yo'l."""
    n_hcl = m_hcl / M_HCL                      # kmol
    return dict(m_hcl=m_hcl, n_hcl=n_hcl,
                m_h2=0.5 * n_hcl * 2.016,       # kg
                m_cl2=0.5 * n_hcl * 70.906,     # kg
                dh_mj=92.31 * n_hcl)            # MJ (eksotermik)


def pickling_balance(m_steel=1.0):
    """1 t po'latni kislorod bilan tozalash koeffitsiyentlari (adabiyot ma'lumoti)."""
    k_hcl = 7.6      # kg HCl / t po'lat
    k_fe = 5.8       # kg Fe / t po'lat
    k_cl = 7.4       # kg Cl- / t po'lat
    n_fecl2 = m_steel * k_fe / M_FE          # kmol
    return dict(m_steel=m_steel, m_hcl=m_steel * k_hcl, m_fe=m_steel * k_fe,
                m_cl=m_steel * k_cl, m_fecl2=n_fecl2 * M_FECL2,
                n_fecl2=n_fecl2)


def regeneration(m_fecl2=1000.0):
    """4FeCl2 + 4H2O + O2 -> 2Fe2O3 + 8HCl (spray roasting) — taxminiy hisob."""
    n = m_fecl2 / M_FECL2                    # kmol
    m_fe2o3 = 0.5 * n * M_FE2O3
    m_hcl = 2.0 * n * M_HCL
    m_h2o = 1.0 * n * M_H2O
    m_o2 = 0.25 * n * M_O2
    return dict(m_fecl2=m_fecl2, n_fecl2=n, m_fe2o3=m_fe2o3, m_hcl=m_hcl,
                m_h2o=m_h2o, m_o2=m_o2,
                m_input=m_fecl2 + m_h2o + m_o2, m_output=m_fe2o3 + m_hcl,
                ratio_hcl=m_hcl / m_fecl2)


# ---------------------------------------------------------------- neytralizatsiya
def neutralisation(m_solution=1000.0, pct=10.0, agent='Na2CO3'):
    """Chiqindini neytralizatsiya qilish mass balansi (shartli hisob)."""
    m_hcl = m_solution * pct / 100.0
    n_hcl = m_hcl / M_HCL                     # kmol
    if agent == 'Na2CO3':
        n_ag = n_hcl / 2.0
        m_ag = n_ag * M_NA2CO3
        m_salt = n_hcl * M_NACL
        m_co2 = n_ag * M_CO2
        m_h2o = n_ag * M_H2O
        return dict(agent=agent, m_solution=m_solution, pct=pct, m_hcl=m_hcl,
                    n_hcl=n_hcl, m_agent=m_ag, m_salt=m_salt, m_gas=m_co2,
                    m_h2o=m_h2o, m_input=m_hcl + m_ag,
                    m_output=m_salt + m_co2 + m_h2o)
    n_ag = n_hcl / 2.0
    m_ag = n_ag * M_CAOH2
    m_salt = n_ag * M_CACL2
    m_h2o = n_hcl * M_H2O
    return dict(agent=agent, m_solution=m_solution, pct=pct, m_hcl=m_hcl,
                n_hcl=n_hcl, m_agent=m_ag, m_salt=m_salt, m_gas=0.0,
                m_h2o=m_h2o, m_input=m_hcl + m_ag,
                m_output=m_salt + m_h2o)


def residual_chloride(na_free=0.050):
    """Neytralizatsiyadan keyingi qoldiq Cl- (mg/L) — taxminiy hisob: 1 L da."""
    return dict(na=na_free, cl_mg=na_free * 35.453 * 1000.0)


def titration_standardisation(m_naco3=0.2500, v_hcl_ml=24.85):
    """Na2CO3 bilan HCl titrlash (standartlash) taxminiy hisobi."""
    n_naco3 = m_naco3 / M_NA2CO3
    n_hcl = 2.0 * n_naco3
    v_l = v_hcl_ml / 1000.0
    return dict(m_naco3=m_naco3, n_naco3=n_naco3, n_hcl=n_hcl,
                v_hcl_ml=v_hcl_ml, c_hcl=n_hcl / v_l,
                m_hcl_g=n_hcl * M_HCL, ph=-math.log10(n_hcl / v_l))


# ---------------------------------------------------------------- metall yemirilishi
def metal_dissolution(m_metal=1.0):
    """1 g metallning HCl bilan erishi (shartli hisob)."""
    out = []
    for mt in METALS:
        n_metal = m_metal / mt['m']
        n_salt = n_metal
        n_hcl = mt['n_cl'] * n_metal
        n_h2 = mt['h2'] * n_metal
        n_o2 = 0.5 * n_metal if mt['o2'] else 0.0
        out.append(dict(metal=mt['name'], m_metal=m_metal, salt=mt['salt'],
                        m_salt=n_salt * mt['m_salt'], n_hcl=n_hcl,
                        m_hcl=n_hcl * M_HCL, n_h2=n_h2, m_h2=n_h2 * 2.016,
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
    write('fizik_hcl',
          ['parametr', 'qiymat', 'birlik'],
          [['molar mass', p['m'], 'g/mol'],
           ['qaynash harorati (1 atm)', p['tb'], '°C'],
           ['suyuqlash harorati', p['tm'], '°C'],
           ['triya nuqtasi harorati', p['triple_t'], 'K'],
           ['triya nuqtasi bosimi', p['triple_p'], 'bar'],
           ['kritik harorat', p['tc'], '°C'],
           ['kritik bosim', p['pc'], 'bar'],
           ['kritik zichlik', p['rho_c'], 'kg/m³'],
           ['gaz zichligi (0 °C, 1 atm)', p['rho_g0'], 'kg/m³'],
           ['gaz zichligi (15 °C, 1 bar)', p['rho_g15'], 'kg/m³'],
           ['nisbiy gaz zichligi (havoga nisbatan)', p['d_air'], ''],
           ['standart entropiya S°(g)', p['s_g'], 'J/(mol·K)'],
           ['hosil entalpiasi ΔfH°(g)', p['dh_f'], 'kJ/mol'],
           ['suvdagi eruvchanlik (20 °C)', p['sol'], 'g/L'],
           ['azeotrop konsentratsiyasi', p['aze_pct'], '%'],
           ['azeotrop qaynash harorati', p['aze_tb'], '°C']])

    rows = []
    for (w, kgm3, mol, be, rho, ph, visc, cp, vp, tb, tm) in SOLUTIONS:
        rows.append([w, kgm3, mol, be, rho, ph, visc, cp, vp, tb, tm])
    write('eritma',
          ['w_pct', 'kg_m3', 'mol_L', 'baume', 'rho', 'pH', 'visc_mPa_s',
           'cp_kJ_kgK', 'vp_kPa', 'tb_C', 'tm_C'], rows)

    rows = []
    for s in speciation_series():
        rows.append([s['c'], s['h'], s['cl'], s['hcl'], s['cl2'], s['ph'],
                     s['w_hcl'], s['w_cl'], s['w_cl2']])
    write('spetsiatsiya',
          ['c_HCl', 'h_H3O', 'cl', 'hcl', 'cl2', 'pH',
           'w_hcl_pct', 'w_cl_pct', 'w_cl2_pct'], rows)

    mn = mannheim(1000.0, 0.98)
    sy = synthesis(1000.0)
    rg = regeneration(1000.0)
    pk = pickling_balance(1.0)
    rows = [['NaCl (kirish)', mn['m_nacl'], 'kg / 1000 kg HCl'],
            ['H₂SO₄ (kirish)', mn['m_h2so4'], 'kg / 1000 kg HCl'],
            ['Na₂SO₄ (chiqish)', mn['m_na2so4'], 'kg / 1000 kg HCl'],
            ['ΔrH (Manheim)', mn['dh_mj'], 'MJ / 1000 kg HCl'],
            ['H₂ (sintetik usul)', sy['m_h2'], 'kg / 1000 kg HCl'],
            ['Cl₂ (sintetik usul)', sy['m_cl2'], 'kg / 1000 kg HCl'],
            ['Fe₂O₃ (regeneratsiya)', rg['m_fe2o3'], 'kg / 1000 kg FeCl₂'],
            ['HCl (regeneratsiya)', rg['m_hcl'], 'kg / 1000 kg FeCl₂'],
            ['HCl (pickling)', pk['m_hcl'], 'kg / t po‘lat'],
            ['Fe (pickling)', pk['m_fe'], 'kg / t po‘lat'],
            ['Cl⁻ (pickling)', pk['m_cl'], 'kg / t po‘lat'],
            ['FeCl₂ (pickling)', pk['m_fecl2'], 'kg / t po‘lat']]
    write('ishlabchiqarish',
          ['element', 'miqdor', 'izoh'], rows)

    rows = []
    for md in metal_dissolution(1.0):
        rows.append([md['metal'], md['m_metal'], md['salt'], md['m_salt'],
                     md['m_hcl'], md['m_h2'], md['m_o2']])
    write('metallar',
          ['metal', 'm_metal_g', 'salt', 'm_salt_g', 'm_HCl_g', 'm_H2_g', 'm_O2_g'], rows)

    n1 = neutralisation(1000.0, 10.0, 'Na2CO3')
    n2 = neutralisation(1000.0, 10.0, 'Ca(OH)2')
    rows = [['HCl (kirish)', n1['m_hcl'], 'kg'],
            ['Na₂CO₃ (neytralizator)', n1['m_agent'], 'kg'],
            ['NaCl (chiqish)', n1['m_salt'], 'kg'],
            ['CO₂ (chiqish)', n1['m_gas'], 'kg'],
            ['H₂O (chiqish)', n1['m_h2o'], 'kg'],
            ['Ca(OH)₂ (neytralizator)', n2['m_agent'], 'kg'],
            ['CaCl₂ (chiqish)', n2['m_salt'], 'kg'],
            ['H₂O (Ca(OH)₂ bilan)', n2['m_h2o'], 'kg'],
            ['kirish (Na₂CO₃ bilan)', n1['m_input'], 'kg'],
            ['chiqish (Na₂CO₃ bilan)', n1['m_output'], 'kg'],
            ['FeCl₂ (regeneratsiya)', 1000.0, 'kg / partiya'],
            ['Fe₂O₃ (regeneratsiya)', rg['m_fe2o3'], 'kg / partiya'],
            ['HCl tikilgan (regeneratsiya)', rg['m_hcl'], 'kg / partiya']]
    write('chiqindi',
          ['element', 'miqdor', 'izoh'], rows)
    return 6


def main():
    build_csvs()
    print('— suvli HCl spetsiatsiyasi (shartli hisob) —')
    for s in speciation_series():
        print('  c=%5.2f M  h=%.4f  Cl-=%.4f  HCl=%.4f  HCl2-=%.4f  pH=%6.3f  ulushlar: HCl %5.2f %% Cl- %5.2f %% HCl2- %5.2f %%'
              % (s['c'], s['h'], s['cl'], s['hcl'], s['cl2'], s['ph'],
                 s['w_hcl'], s['w_cl'], s['w_cl2']))
    mn = mannheim(1000.0, 0.98)
    print('— Mannheim usuli: 1000 kg HCl —')
    print('  NaCl %.1f kg, H2SO4 %.1f kg, Na2SO4 %.1f kg, ΔrH %.1f MJ (%.1f kJ/mol HCl)'
          % (mn['m_nacl'], mn['m_h2so4'], mn['m_na2so4'], mn['dh_mj'], mn['dh_kj_per_mol']))
    sy = synthesis(1000.0)
    print('— sintetik usul: H2 %.1f kg, Cl2 %.1f kg, ΔrH %.1f MJ'
          % (sy['m_h2'], sy['m_cl2'], sy['dh_mj']))
    print('— metall yemirilishi (1 g metall) —')
    for md in metal_dissolution(1.0):
        extra = ' (O₂ kerak)' if md['need_o2'] else ''
        print('  %-3s -> %-6s %6.3f g tuz, HCl %6.3f g, H2 %5.3f g%s'
              % (md['metal'], md['salt'], md['m_salt'], md['m_hcl'], md['m_h2'], extra))
    n1 = neutralisation(1000.0, 10.0, 'Na2CO3')
    n2 = neutralisation(1000.0, 10.0, 'Ca(OH)2')
    print('— neytralizatsiya: 1000 kg 10 % HCl —')
    print('  Na2CO3 bilan: Na2CO3 %.1f kg, NaCl %.1f kg, CO2 %.1f kg, H2O %.1f kg (kirish %.1f = chiqish %.1f)'
          % (n1['m_agent'], n1['m_salt'], n1['m_gas'], n1['m_h2o'], n1['m_input'], n1['m_output']))
    print('  Ca(OH)2 bilan: Ca(OH)2 %.1f kg, CaCl2 %.1f kg, H2O %.1f kg (kirish %.1f = chiqish %.1f)'
          % (n2['m_agent'], n2['m_salt'], n2['m_h2o'], n2['m_input'], n2['m_output']))
    rg = regeneration(1000.0)
    print('— regeneratsiya: 1000 kg FeCl2 —')
    print('  Fe2O3 %.1f kg, HCl %.1f kg, H2O %.1f kg, O2 %.1f kg (kirish %.1f ≈ chiqish %.1f)'
          % (rg['m_fe2o3'], rg['m_hcl'], rg['m_h2o'], rg['m_o2'], rg['m_input'], rg['m_output']))
    pk = pickling_balance(1.0)
    print('— pickling (1 t po‘lat): HCl %.1f kg, Fe %.1f kg, Cl- %.1f kg, FeCl2 %.1f kg'
          % (pk['m_hcl'], pk['m_fe'], pk['m_cl'], pk['m_fecl2']))
    t = titration_standardisation(0.2500, 24.85)
    print('— standartlash: %.4f g Na2CO3, V(HCl) %.2f mL -> C(HCl) = %.5f mol/L (pH %.3f)'
          % (t['m_naco3'], t['v_hcl_ml'], t['c_hcl'], t['ph']))
    print('CSV fayllar yozildi:', ', '.join(sorted(p.name for p in ASSETS.glob('*.csv'))))


if __name__ == '__main__':
    main()
