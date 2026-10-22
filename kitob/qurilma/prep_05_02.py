"""5.2 "Kislotalarni tozalash" — tozalash modeli va ma'lumotlar.

Barcha sonli egri chiziqlar shu modulda hisoblanadi: ular tajriba yoki
o'lchov ma'lumotlari EMAS. Ksp va Kf — OpenStax Chemistry 2e, Appendix J
va K (25 °C). Azeotrop va xususiyatlar — CRC Handbook; sifat chegaralari —
European Pharmacopoeia 6.0 monografiyasi.
"""
from pathlib import Path
import csv
import math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'tozalash'
T0 = 298.15

# --- Eriganlik mahsulotlari Ksp (25 °C) — OpenStax App. J, Table J1 --------
KSP = {
    'Fe(OH)3': 4.0e-38, 'Fe(OH)2': 1.8e-15, 'FeS': 3.7e-19,
    'Cu(OH)2': 2.2e-20, 'CuS': 8.5e-45,
    'Ni(OH)2': 1.6e-16, 'NiS(a)': 4.0e-20,
    'Cd(OH)2': 5.9e-15, 'CdS': 1.0e-28,
    'Pb(OH)2': 1.2e-15, 'PbS': 7.0e-29,
    'Co(OH)2': 2.5e-16, 'CoS(a)': 5.0e-22,
    'MnS': 2.3e-13,
    'Ca(OH)2': 1.3e-6, 'CaCO3': 8.7e-9, 'CaSO4*2H2O': 6.1e-5,
    'Ba(OH)2*8H2O': 5.0e-3, 'BaSO4': 2.3e-8,
    'Al(OH)3': 2.0e-32, 'Ag2O': 2.0e-8, 'Ag2S': 1.6e-49,
    'HgS': 1.6e-54,
}

# --- Kompleks ionlar hosil qilish konstantalari — OpenStax App. K ---------
KF = {
    'Cu2+ + 4NH3': 1.7e13,       # [Cu(NH3)4]2+
    'Cd2+ + 4NH3': 1.3e7,        # [Cd(NH3)4]2+
    'Ni2+ + 6NH3': 2.0e8,        # [Ni(NH3)6]2+
    'Ag+ + 2NH3': 1.7e7,         # [Ag(NH3)2]+
    'Al3+ + 6F-': 7.0e19,        # [AlF6]3-
    'Fe3+ + SCN-': 8.9e2,        # [Fe(SCN)]2+
    'Hg2+ + 4Cl-': 1.1e16,       # [HgCl4]2-
}

# --- Molyar massalar (g/mol) ---------------------------------------------
M = {'HNO3': 63.01, 'NO2': 46.01, 'N2O4': 92.02, 'H2O': 18.015,
     'O2': 32.00, 'H2SO4': 98.08, 'Fe': 55.85, 'Fe(OH)3': 106.87,
     'CaO': 56.08, 'CaCO3': 100.09, 'CaSO4': 136.14, 'CO2': 44.01,
     'HCl': 36.46, 'H2S': 34.08, 'S': 32.06, 'Cu': 63.55, 'Zn': 65.38}

# --- Azeotrop nuqtalari (1 atm) -------------------------------------------
AZEO = {'HNO3-H2O': (0.688, 120.5), 'HCl-H2O': (0.202, 108.6),
        'H2SO4-H2O': (0.983, 337.0)}


# --- 1) Cho'ktirish: metall qoldig'i pH ga bog'liqligi -------------------
def ph_to_oh(pH):
    return 10.0 ** (pH - 14.0)


def metal_solubility(pH, ksp, n):
    """[M^n+] = Ksp / [OH-]^n (cho'ktirish sharoitida)."""
    return ksp / ph_to_oh(pH) ** n


def cu_with_ammonia(pH, nh3=1.0):
    """Cu(OH)2 ning ammiak kompleksi hisobga olingan eruvchanligi.

    Faqat eng yuqori darajali kompleks hisobga olingan (taxmin):
    alpha = 1 + beta4*[NH3]^4.
    """
    alpha = 1.0 + KF['Cu2+ + 4NH3'] * nh3 ** 4
    return KSP['Cu(OH)2'] / (alpha * ph_to_oh(pH) ** 2)


# --- 2) Tozalash kaskadi: ifloslik pasayishi ----------------------------
def cascade_purity(n, phi):
    """n ta bir xil ajratish bosqichidan keyingi ifloslik ulushi."""
    return phi ** (-n)


def stages_for(phi, target_ratio):
    """target_ratio (c/c0) gacha pasaytish uchun zarur bosqichlar soni."""
    return math.log(target_ratio) / math.log(1.0 / phi)


# --- 3) Bug'lash va rektifikatsiya ---------------------------------------
def y_eq(x, alpha):
    """Doimiy nisbiy uchuvchanlikdagi muvozanat egri chizig'i."""
    return alpha * x / (1.0 + (alpha - 1.0) * x)


def x_eq_of_y(y, alpha):
    """y_eq ning teskari funksiyasi."""
    return y / (alpha - y * (alpha - 1.0))


def fenske(alpha, xD=0.95, xB=0.05):
    """Minimal (to'liq qaytish) pog'onalar soni."""
    if alpha <= 1.0:
        return float('inf')
    return (math.log(xD / (1 - xD)) + math.log((1 - xB) / xB)) / math.log(alpha)


def r_min(alpha, xD=0.95, xF=0.50):
    """Minimal qaytish nisbati (q = 1, to'g'ridan-to'g'ri oziq)."""
    slope = (xD - y_eq(xF, alpha)) / (xD - xF)
    if slope >= 1.0:
        return float('inf')
    return slope / (1.0 - slope)


def mccabe_thiele(alpha, xD=0.95, xB=0.05, xF=0.50, R=2.0):
    """McCabe-Thiele bosqichlari (q = 1, doimiy molal oqim).

    {'N': pog'onalar soni, 'points': [(x, y), ...], 'rect': ..., 'strip': ...}
    """
    rm = r_min(alpha, xD, xF)
    if R < rm:
        return {'N': None, 'points': [], 'rect': None, 'strip': None,
                'xq': xF, 'r_min': rm, 'feasible': False}
    a_rect = R / (R + 1.0)
    b_rect = xD / (R + 1.0)
    y_int = a_rect * xF + b_rect
    a_strip = (y_int - xB) / (xF - xB)
    b_strip = -a_strip * xB

    def op(x):
        return a_rect * x + b_rect if x >= xF else a_strip * x + b_strip

    x, y = xD, xD
    points = [(x, y)]
    n = 0
    for _ in range(400):
        xq = x_eq_of_y(y, alpha)
        points.append((xq, y))
        yn = op(xq)
        points.append((xq, yn))
        n += 1
        x, y = xq, yn
        if xq <= xB:
            break
    return {'N': n, 'points': points, 'rect': (a_rect, b_rect),
            'strip': (a_strip, b_strip), 'xq': xF, 'r_min': rm,
            'feasible': True}


# --- 4) Suvni olib tashlash (bug'lash orqali konsentratsiyalash) ----------
def water_removal(w0, w1, basis=100.0):
    """w0 -> w1 mass ulushiga o'tish uchun olib tashlanadigan suv (kg)."""
    m_acid = basis * w0
    m_final = m_acid / w1
    m_water_out = basis - m_final
    return {'m_acid': m_acid, 'm_final': m_final, 'm_water_out': m_water_out,
            'm_distillate': m_water_out}


# --- 5) Ion almashinuv: fronti kiring egri chizig'i ------------------------
def thomas(c0, q_max=50.0, K=0.5, m_ads=2.0, v_void=0.2, v_end=None,
           steps=4000):
    """Ion almashinuv kolonkasining fronti kiring egri chizig'i.

    Plug-flow model: dq/dV = C0 - C(q), C = q/[K(q_max - q)] (Langmuir
    izotermasi, darhol muvozanat). V - adsorbent massi (g).
    Qaytaradi: {'points': [(bed hajmi, C/C0), ...], 'q_end': ..., 'area': ...}
    """
    v_end = m_ads if v_end is None else v_end
    h = v_end / steps
    q_eq = q_max * K * c0 / (1.0 + K * c0)      # oziq bilan muvozanatdagi yuk

    def conc(q):
        if q >= q_max:
            return c0
        return q / (K * (q_max - q))

    def rk4(q):
        def dq(x):
            if x >= q_eq:
                return 0.0
            return max(0.0, c0 - conc(x))
        k1 = dq(q)
        k2 = dq(q + h / 2 * k1)
        k3 = dq(q + h / 2 * k2)
        k4 = dq(q + h * k3)
        return q + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    q = 0.0
    Q = 0.0                      # yig'ilgan adsorbsiya (mg)
    area = 0.0                   # integral (C0 - C) dV
    out = []
    for _ in range(steps):
        q_new = min(rk4(q), q_eq)
        c_old = conc(q)
        c_new = conc(q_new)
        Q_new = Q + 0.5 * (q + q_new) * h
        v_feed = Q_new / (c0 - c_new) if c0 > c_new else float('inf')
        out.append((v_feed / v_void, c_new / c0))
        area += (c0 - 0.5 * (c_old + c_new)) * h
        Q = Q_new
        q = q_new
    return {'points': out, 'q_end': q, 'area': area, 'q_eq': q_eq}


def breakthrough_bv(c0, **kw):
    """C/C0 = 0,5 ga ko'tarilgan bed hajmi (fronti kiring nuqtasi)."""
    r = thomas(c0, **kw)
    pts = r['points']
    for i in range(1, len(pts)):
        if pts[i - 1][1] < 0.5 <= pts[i][1]:
            return pts[i][0]
    return float('nan')


# --- 6) Ishlangan hisob: NO2 ni HNO3 ga qaytarish ------------------------
def no2_to_hno3(m_sol_t, w_hno3, m_no2_t):
    """4NO2 + O2 + 2H2O -> 4HNO3 (rang beruvchi NO2 ni HNO3 ga aylantirish)."""
    n_no2 = m_no2_t * 1000.0 / M['NO2']                      # kmol
    n_h2o = n_no2 / 2.0
    n_o2 = n_no2 / 4.0
    n_hno3 = n_no2
    m_hno3_new = n_hno3 * M['HNO3'] / 1000.0                 # t
    m_h2o_used = n_h2o * M['H2O'] / 1000.0
    m_o2 = n_o2 * M['O2'] / 1000.0
    m_final = m_sol_t + m_o2 - m_h2o_used
    m_acid = m_sol_t * w_hno3 + m_hno3_new
    return {'n_no2': n_no2, 'n_h2o': n_h2o, 'n_o2': n_o2,
            'm_hno3_new': m_hno3_new, 'm_h2o_used': m_h2o_used,
            'm_o2': m_o2, 'm_final': m_final, 'm_acid': m_acid,
            'w_final': m_acid / m_final,
            'w_start': w_hno3, 'm_no2': m_no2_t}


# --- 7) Ishlangan hisob: Fe ni cho'ktirish --------------------------------
def fe_precipitation(m_sol_t, w_fe, m_h2so4_t=None):
    """Fe2(SO4)3 + 3CaO + 3H2O -> 2Fe(OH)3 + 3CaSO4  (CaO yo'li).

    Taqqoslash: CaCO3 yo'li — kislotaning o'zi sulfat manbai bo'lib,
    mahsulot yo'qoladi.
    """
    m_fe = m_sol_t * w_fe                                    # t
    n_fe = m_fe * 1000.0 / M['Fe']
    m_feoh3 = n_fe * M['Fe(OH)3'] / 1000.0
    n_caso4 = 1.5 * n_fe
    m_caso4 = n_caso4 * M['CaSO4'] / 1000.0
    m_cao = n_caso4 * M['CaO'] / 1000.0
    m_caco3 = n_caso4 * M['CaCO3'] / 1000.0
    m_h2so4_lost = n_caso4 * M['H2SO4'] / 1000.0
    m_h2o = 1.5 * n_fe * M['H2O'] / 1000.0
    m_final = m_sol_t + m_cao + m_h2o - m_feoh3 - m_caso4
    return {'m_fe': m_fe, 'n_fe': n_fe, 'm_feoh3': m_feoh3,
            'm_caso4': m_caso4, 'm_cao': m_cao, 'm_caco3': m_caco3,
            'm_h2so4_lost': m_h2so4_lost, 'm_h2o': m_h2o,
            'm_final': m_final,
            'E_factor': (m_feoh3 + m_caso4) / m_sol_t,
            'loss_caco3': m_h2so4_lost / m_sol_t}


# --- CSV yozish ------------------------------------------------------------
def save_data():
    ASSETS.mkdir(parents=True, exist_ok=True)

    # 1) Tozalash kaskadi: n bosqich va ajratish faktori
    with (ASSETS / 'kaskad.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['N', 'log10_c_phi10', 'log10_c_phi100',
                    'log10_c_phi1000', 'log10_c_phi10000'])
        for i in range(401):
            n = 1.0 + i * (39.0 / 400.0)
            w.writerow([f'{n:.4f}'] + [f'{math.log10(cascade_purity(n, p)):.6f}'
                                       for p in (10, 100, 1000, 10000)])

    # 2) Cho'ktirish: metall qoldig'i pH ga bog'liqligi
    with (ASSETS / 'choqish.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['pH', 'Fe3', 'Cu2', 'Ni2', 'Cd2', 'Pb2', 'Cu2_NH3'])
        for i in range(281):
            pH = i * 0.05
            w.writerow([f'{pH:.3f}',
                        f'{metal_solubility(pH, KSP["Fe(OH)3"], 3):.6e}',
                        f'{metal_solubility(pH, KSP["Cu(OH)2"], 2):.6e}',
                        f'{metal_solubility(pH, KSP["Ni(OH)2"], 2):.6e}',
                        f'{metal_solubility(pH, KSP["Cd(OH)2"], 2):.6e}',
                        f'{metal_solubility(pH, KSP["Pb(OH)2"], 2):.6e}',
                        f'{cu_with_ammonia(pH, 1.0):.6e}'])

    # 3) Rektifikatsiya: muvozanat egri chizig'lari
    with (ASSETS / 'rektifikatsiya.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['x', 'y_a1.5', 'y_a2', 'y_a3'])
        for i in range(201):
            x = i / 200.0
            w.writerow([f'{x:.5f}', f'{y_eq(x, 1.5):.6f}',
                        f'{y_eq(x, 2.0):.6f}', f'{y_eq(x, 3.0):.6f}'])

    # 3b) McCabe-Thiele bosqichlari
    mct = mccabe_thiele(2.0)
    assert mct['feasible']
    with (ASSETS / 'mcbabgele.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['i', 'x', 'y'])
        for i, (x, y) in enumerate(mct['points']):
            w.writerow([i, f'{x:.6f}', f'{y:.6f}'])

    # 4) Suvni olib tashlash: bug'lash orqali konsentratsiyalash
    with (ASSETS / 'buglash.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['w0', 'out_to_0.68', 'out_to_0.90', 'out_to_0.98',
                    'out_to_0.99'])
        for i in range(401):
            w0 = 0.10 + i * (0.798 / 400.0)
            row = [f'{w0:.5f}']
            for w1 in (0.68, 0.90, 0.98, 0.99):
                if w0 >= w1:
                    row.append('0.000')
                else:
                    row.append(f'{water_removal(w0, w1)["m_water_out"]:.4f}')
            w.writerow(row)

    # 5) Ion almashinuv: fronti kiring egri chizig'i
    with (ASSETS / 'ionalmashinuv.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['BV', 'c50', 'c100', 'c200'])
        r50 = thomas(50.0)['points']
        r100 = thomas(100.0)['points']
        r200 = thomas(200.0)['points']
        for i in range(len(r50)):
            w.writerow([f'{r50[i][0]:.5f}',
                        f'{r50[i][1]:.6f}', f'{r100[i][1]:.6f}',
                        f'{r200[i][1]:.6f}'])


if __name__ == '__main__':
    save_data()
    print('Cho\'ktirish (pH = 2,0):')
    for k, n in (('Fe(OH)3', 3), ('Cu(OH)2', 2), ('Ni(OH)2', 2),
                 ('Cd(OH)2', 2), ('Pb(OH)2', 2)):
        print('  %-10s [M] = %.3e M' % (k, metal_solubility(2.0, KSP[k], n)))
    print('  Cu2+ (NH3 1,0 M bilan) = %.3e M' % cu_with_ammonia(2.0, 1.0))
    print('Kaskad: Phi = 1000 uchun 10^-6 gacha %d bosqich' %
          stages_for(1000, 1e-6))
    print('Fenske (xD=0,95; xB=0,05): ',
          [(a, round(fenske(a), 2)) for a in (1.2, 1.5, 2.0, 3.0)])
    for a in (1.5, 2.0, 3.0):
        m = mccabe_thiele(a)
        if m['feasible']:
            print('  alpha = %.1f: N = %d pog\'ona, R_min = %.3f' %
                  (a, m['N'], m['r_min']))
        else:
            print('  alpha = %.1f: R = 2,0 < R_min = %.3f — dizayn mumkin emas' %
                  (a, m['r_min']))
    for w0 in (0.5, 0.68, 0.75):
        r = water_removal(w0, 0.98)
        print('  w0 = %.2f -> 0,98: suv %.2f kg / 100 kg, qoldiq %.2f kg' %
              (w0, r['m_water_out'], r['m_final']))
    for c0 in (100.0, 200.0, 400.0):
        r = thomas(c0)
        print('  C0 = %g mg/L: fronti kiring BV = %.3f; q_end = %.3f mg/g' %
              (c0, breakthrough_bv(c0), r['q_end']))
    r = thomas(200.0)
    print('  mass balance: integral (C0-C)dV = %.4f mg/g (q_max = 50)' % r['area'])
    h = no2_to_hno3(1000.0, 0.68, 4.0)
    print('NO2 -> HNO3: HNO3 +%.4f t, suv -%.4f t, O2 +%.4f t, w = %.5f' %
          (h['m_hno3_new'], h['m_h2o_used'], h['m_o2'], h['w_final']))
    f = fe_precipitation(1000.0, 0.0003)
    print('Fe choqish: Fe(OH)3 %.4f t, CaSO4 %.4f t, CaO %.4f t, E = %.5f' %
          (f['m_feoh3'], f['m_caso4'], f['m_cao'], f['E_factor']))
    print('  CaCO3 yo\'li: reagent %.4f t, yo\'qotilgan H2SO4 %.4f t (%.5f%%)' %
          (f['m_caco3'], f['m_h2so4_lost'], 100 * f['loss_caco3']))
    print('CSV yozildi:', ASSETS)
