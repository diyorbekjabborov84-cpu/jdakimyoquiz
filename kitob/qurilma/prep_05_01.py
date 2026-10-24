"""5.1 "Olishning umumiy usullari" — termodinamik va texnologik taxminiy hisob.

Barcha sonli egri chiziqlar shu modulda hisoblanadi: ular tajriba yoki
o'lchov ma'lumotlari EMAS. ΔfH° va S° — OpenStax Chemistry 2e, Appendix G
(298,15 K); savdo kislotalari tarkibi — Appendix F.
"""
from pathlib import Path
import csv
import math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'olish'
T0 = 298.15
R = 8.314462618          # J/(mol·K)
P0 = 1.0                # bar (standart bosim)

# ΔfH° (kJ/mol), S° (J/(mol·K)) — OpenStax Chemistry 2e, Appendix G
DATA = {
    'S8(s)':    (0.0,      256.8),
    'O2(g)':    (0.0,      205.2),
    'H2(g)':    (0.0,      130.7),
    'Cl2(g)':   (0.0,      223.1),
    'SO2(g)':   (-296.83,  248.2),
    'SO3(g)':   (-395.72,  256.76),
    'H2O(l)':   (-285.83,  70.0),
    'H2SO4(l)': (-813.989, 156.90),
    'NaCl(s)':  (-411.2,   72.1),
    'KCl(s)':   (-436.5,   82.6),
    'CaSO4(s)': (-1434.5,  106.5),
    'HCl(g)':   (-92.307,  186.9),
    'NH3(g)':   (-45.9,    192.8),
    'NO(g)':    (90.25,    210.8),
    'NO2(g)':   (33.2,     240.1),
    'HNO3(l)':  (-174.1,   155.6),
    'CO(g)':    (-110.52,  197.7),
    'CO2(g)':   (-393.51,  213.8),
    'H2S(g)':   (-20.6,    205.8),
    'N2O4(g)':  (11.1,     304.4),
    'Fe2O3(s)': (-824.2,   87.40),
    'H3PO4(s)': (-1279.0,  110.50),
    'HCN(l)':   (108.9,    112.8),
}

# --- Atom massalari (standart atom og'irliklari) --------------------------
M = {'FeS2': 119.98, 'SO2': 64.06, 'SO3': 80.06, 'H2SO4': 98.08,
     'H2O': 18.015, 'Fe2O3': 159.69, 'O2': 32.00, 'H2': 2.016}


def dH(left, right):
    """ΔH° = ΣΔfH°(mahsulot) − ΣΔfH°(reagent)."""
    return (sum(DATA[k][0] * v for k, v in right.items())
            - sum(DATA[k][0] * v for k, v in left.items()))


def dS(left, right):
    """ΔS° = ΣS°(mahsulot) − ΣS°(reagent)."""
    return (sum(DATA[k][1] * v for k, v in right.items())
            - sum(DATA[k][1] * v for k, v in left.items()))


def dG(dh, ds, T=T0):
    """Standart Gibbs energiya o'zgarishi, kJ/mol."""
    return dh - T * ds / 1000.0


def lgK(dh, ds, T=T0):
    """lg K = −ΔG°/(2,303·R·T)."""
    return -dG(dh, ds, T) * 1000.0 / (R * T * math.log(10))


def lnK(dh, ds, T=T0):
    return -dG(dh, ds, T) * 1000.0 / (R * T)


def t_star(dh, ds):
    """ΔG(T) = 0 bo'ladigan kesish nuqtasi (K)."""
    if dh * ds >= 0:
        return None
    return dh * 1000.0 / ds


def vanthoff(dh, T1, T2):
    """ln(K2/K1) = −ΔH°/R · (1/T2 − 1/T1)."""
    return -dh * 1000.0 / R * (1.0 / T2 - 1.0 / T1)


# --- Taxminiy hisob 1: N2O4 ⇌ 2 NO2 muvozanat konversiyasi ------------------------
RX_SO2 = ({'SO2(g)': 1.0, 'O2(g)': 0.5}, {'SO3(g)': 1.0})
RX_DIMER = ({'N2O4(g)': 1.0}, {'NO2(g)': 2.0})


def kp_so2(T):
    """Kp (p° = 1 bar) — SO2 oksidlanishining standart konstantasi."""
    return math.exp(lnK(dH(*RX_SO2), dS(*RX_SO2), T))


def kp_dimer(T):
    """Kp (p° = 1 bar) — N2O4 ⇌ 2 NO2 dissotsiatsiyasining konstantasi."""
    return math.exp(lnK(dH(*RX_DIMER), dS(*RX_DIMER), T))


def eq_conversion(T, P=1.0):
    """Muvozanatdagi N2O4 dissotsiatsiya darajasi (0…1).

    Basis: 1 mol N2O4; ideal gaz, P bar. Kp = (p_NO2/p°)^2/(p_N2O4/p°).
    """
    Kt = kp_dimer(T)

    def log_ratio(X):
        if X <= 0.0:
            return -1e9
        if X >= 1.0:
            return 1e9
        n_d, n_m = 1.0 - X, 2.0 * X
        n_tot = 1.0 + X
        y_d, y_m = n_d / n_tot, n_m / n_tot
        q = P / P0
        kp = (y_m * q) ** 2 / (y_d * q)
        return math.log(kp) - math.log(Kt)

    lo, hi = 1e-9, 1.0 - 1e-9
    if log_ratio(lo) > 0:
        return 0.0
    if log_ratio(hi) < 0:
        return 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if log_ratio(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# --- Taxminiy hisob 2: bosqichli kaskad — umumiy konversiya -----------------------
def cascade(x1, n):
    """N ta bir xil bosqich: X_umumiy = 1 − (1 − x1)^N."""
    return 1.0 - (1.0 - x1) ** n


# --- Taxminiy hisob 3: ajratish — minimal pog'onalar soni (Fenske, to'liq qaytish) -
def fenske(alpha, xD=0.95, xB=0.05):
    """Minimal (to'liq qaytish rejimidagi) pog'onalar soni."""
    if alpha <= 1.0:
        return float('inf')
    return (math.log(xD / (1 - xD)) + math.log((1 - xB) / xB)) / math.log(alpha)


# --- Taxminiy hisob 4: pyrit -> H2SO4 material balansi ----------------------------
def pyrite_chain(mass_pyrite_t=1000.0, x_so3=0.96, y_abs=0.98):
    """1 mol FeS2 -> 2 mol SO2 -> 2 mol SO3 -> 2 mol H2SO4 zanjiri.

    {'mass_pyrite_t': tonna, 'x_so3': SO2 -> SO3 konversiyasi,
     'y_abs': SO3 yutilish (absorbsiya) unumi} — barchasi ochiq shartli.
    """
    n_fes2 = mass_pyrite_t * 1000.0 / M['FeS2']          # kmol
    n_so2 = 2.0 * n_fes2
    n_so3 = x_so3 * n_so2
    n_so2_left = n_so2 - n_so3
    n_h2so4 = y_abs * n_so3
    n_o2 = 0.5 * n_so3
    n_h2o_used = n_h2so4
    n_fe2o3 = 0.5 * n_fes2
    m_h2so4 = n_h2so4 * M['H2SO4'] / 1000.0               # t
    m_theor = 2.0 * n_fes2 * M['H2SO4'] / 1000.0
    m_res = n_fe2o3 * M['Fe2O3'] / 1000.0                 # t
    m_so2_left = n_so2_left * M['SO2'] / 1000.0           # t
    m_o2 = n_o2 * M['O2'] / 1000.0                        # t
    m_h2o_used = n_h2o_used * M['H2O'] / 1000.0           # t
    waste = m_res + m_so2_left
    return {
        'n_fes2': n_fes2, 'n_so2': n_so2, 'n_so3': n_so3,
        'n_so2_left': n_so2_left, 'n_h2so4': n_h2so4, 'n_o2': n_o2,
        'n_fe2o3': n_fe2o3,
        'm_h2so4': m_h2so4, 'm_theoretical': m_theor,
        'm_residue': m_res, 'm_so2_left': m_so2_left, 'm_o2': m_o2,
        'm_h2o_used': m_h2o_used,
        'yield': m_h2so4 / m_theor,
        'E_factor': waste / m_h2so4,
    }


def efactor(x_so3, y_abs=0.98, mass_pyrite_t=1000.0):
    """1 t mahsulotga to'g'ri keladigan chiqindi massasi (kg/kg)."""
    r = pyrite_chain(mass_pyrite_t, x_so3, y_abs)
    return (r['m_residue'] + r['m_so2_left']) / r['m_h2so4']


def acid_water_96(m_h2so4_t):
    """96 % li sulfat kislotani tayyorlash uchun suv balansi, t."""
    m_sol = m_h2so4_t / 0.96
    water_in = m_sol - m_h2so4_t
    return {'m_solution': m_sol, 'm_water_in_product': water_in}


# --- CSV yozish ------------------------------------------------------------
def save_data():
    ASSETS.mkdir(parents=True, exist_ok=True)

    # 1) Muvozanat konversiyasi: 400…900 K, 401 nuqta
    with (ASSETS / 'mivozanat.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['T_K', 'X_1bar', 'X_10bar', 'X_100bar'])
        for i in range(401):
            T = 250.0 + i * (150.0 / 400.0)
            w.writerow([f'{T:.4f}', f'{eq_conversion(T, 1.0):.6f}',
                        f'{eq_conversion(T, 10.0):.6f}',
                        f'{eq_conversion(T, 100.0):.6f}'])

    # 2) Kaskad: umumiy konversiya bosqichlar soniga bog'liq
    with (ASSETS / 'kaskad.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['N', 'X_umumiy_x0.4', 'X_umumiy_x0.6', 'X_umumiy_x0.8'])
        for i in range(401):
            n = 1.0 + i * (39.0 / 400.0)
            w.writerow([f'{n:.4f}', f'{cascade(0.4, n):.6f}',
                        f'{cascade(0.6, n):.6f}',
                        f'{cascade(0.8, n):.6f}'])

    # 3) Chiqindi omili: konversiyaga bog'liq
    with (ASSETS / 'chiqindi.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['X_SO3', 'E_factor', 'm_h2so4_t'])
        for i in range(401):
            x = 0.50 + i * (0.499 / 400.0)
            r = pyrite_chain(1000.0, x, 0.98)
            w.writerow([f'{x:.6f}', f'{(r["m_residue"] + r["m_so2_left"]) / r["m_h2so4"]:.6f}',
                        f'{r["m_h2so4"]:.4f}'])

    # 5) Standart Gibbs energiyasi: haroratga bog'liqligi
    rx_hcl = ({'H2(g)': 1.0, 'Cl2(g)': 1.0}, {'HCl(g)': 2.0})
    rx_nh3 = ({'NH3(g)': 4.0, 'O2(g)': 5.0}, {'NO(g)': 4.0, 'H2O(l)': 6.0})
    with (ASSETS / 'dG.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['T_K', 'dG_SO2_kJ', 'dG_HCl_kJ', 'dG_N2O4_kJ', 'dG_NH3_kJ'])
        for i in range(251):
            T = 250.0 + i * 1.0
            w.writerow([f'{T:.2f}',
                        f'{dG(dH(*RX_SO2), dS(*RX_SO2), T):.4f}',
                        f'{dG(dH(*rx_hcl), dS(*rx_hcl), T):.4f}',
                        f'{dG(dH(*RX_DIMER), dS(*RX_DIMER), T):.4f}',
                        f'{dG(dH(*rx_nh3), dS(*rx_nh3), T):.4f}'])

    # 4) Ajratish: minimal pog'onalar soni nisbiy uchuvchanlikka bog'liq
    with (ASSETS / 'buglanish.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['alpha', 'N_min', 'N_min_xD99'])
        for i in range(401):
            a = 1.05 + i * (8.95 / 400.0)
            w.writerow([f'{a:.6f}', f'{fenske(a):.4f}', f'{fenske(a, 0.99, 0.01):.4f}'])


if __name__ == '__main__':
    save_data()
    dh, ds = dH(*RX_SO2), dS(*RX_SO2)
    print('SO2 + 1/2 O2 -> SO3: dH=%.2f dS=%.2f dG(298)=%.2f lgK=%.3f'
          % (dh, ds, dG(dh, ds), lgK(dh, ds)))
    for T in (250, 275, 298.15, 325, 350, 400):
        print('  T=%6.2f K  X(1 bar)=%.4f  X(10 bar)=%.4f  X(100 bar)=%.4f'
              % (T, eq_conversion(T, 1.0), eq_conversion(T, 10.0), eq_conversion(T, 100.0)))
    print('  vanthoff dimer 300->400: ln(K2/K1)=%.4f  K2/K1=%.1f'
          % (vanthoff(dH(*RX_DIMER), 300.0, 400.0), math.exp(vanthoff(dH(*RX_DIMER), 300.0, 400.0))))
    dh3, ds3 = dH({'H2(g)': 1.0, 'Cl2(g)': 1.0}, {'HCl(g)': 2.0}), dS({'H2(g)': 1.0, 'Cl2(g)': 1.0}, {'HCl(g)': 2.0})
    print('H2 + Cl2 -> 2 HCl: dH=%.2f dS=%.2f dG(298)=%.2f lgK=%.3f' % (dh3, ds3, dG(dh3, ds3), lgK(dh3, ds3)))
    dh4, ds4 = dH({'NH3(g)': 4.0, 'O2(g)': 5.0}, {'NO(g)': 4.0, 'H2O(l)': 6.0}), dS({'NH3(g)': 4.0, 'O2(g)': 5.0}, {'NO(g)': 4.0, 'H2O(l)': 6.0})
    print('4NH3 + 5O2 -> 4NO + 6H2O: dH=%.2f dS=%.2f dG(298)=%.2f lgK=%.2f' % (dh4, ds4, dG(dh4, ds4), lgK(dh4, ds4)))
    dh2, ds2 = dH(*RX_DIMER), dS(*RX_DIMER)
    print('N2O4 -> 2 NO2: dH=%.2f dS=%.2f dG(298)=%.2f lgK=%.4f K=%.4f'
          % (dh2, ds2, dG(dh2, ds2), lgK(dh2, ds2), math.exp(lnK(dh2, ds2))))
    for T1, T2 in ((600, 700), (700, 800)):
        print('  vanthoff %d->%d: ln(K2/K1)=%.4f' % (T1, T2, vanthoff(dh, T1, T2)))
    print('cascade: x1=0.6 ->', ['%.4f' % cascade(0.6, n) for n in (1, 2, 5, 10, 20)])
    print('fenske: ', [(a, round(fenske(a), 2)) for a in (1.1, 1.5, 2.0, 3.0, 5.0)])
    r = pyrite_chain()
    for k in ('n_fes2', 'n_so2', 'n_so3', 'n_so2_left', 'n_h2so4', 'n_o2', 'n_fe2o3',
              'm_h2so4', 'm_theoretical', 'm_residue', 'm_so2_left', 'm_o2',
              'm_h2o_used', 'yield', 'E_factor'):
        print('  %-14s %.4f' % (k, r[k]))
    w = acid_water_96(r['m_h2so4'])
    print('  96%% acid: solution %.2f t, water in product %.2f t' % (w['m_solution'], w['m_water_in_product']))
    print('  E-factor: X=0.90 %.4f; X=0.96 %.4f; X=0.99 %.4f'
          % (efactor(0.90), efactor(0.96), efactor(0.99)))
    print('CSV yozildi:', ASSETS)
