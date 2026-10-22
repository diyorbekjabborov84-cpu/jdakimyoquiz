"""5.3 «QuRITish va suvsizlantirish» — model zaxirasi.

Barcha sonli natijalar ochiq shartli modeldan olingan; tajriba ma’lumoti emas.
Manbalar: OpenStax App. G (ΔfH°), CRC (ΔvapH, molar massalar),
Ph. Eur. 6.0 (2.2.32, 2.5.12, 5.11), USP <731>, EPA Method 9000,
IUPAC Gold Book (D01582, E01909, D01618).
"""
from pathlib import Path
import csv, math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'quritish'
ASSETS.mkdir(parents=True, exist_ok=True)

# --- molar massalar (g/mol), CRC Handbook 97th ed. -----------------------
M_H2O = 18.015
M_CUSO4 = 159.61
M_H2SO4 = 98.08
M_HNO3 = 63.01
M_TOLUENE = 92.14
M_P2O5 = 141.94
M_H3PO4 = 97.99
M_CACL2 = 110.98
M_MGSO4 = 120.37
R = 8.314462618            # J/(mol·K)

# --- termodinamik (OpenStax App. G, 298,15 K) ---------------------------
DFH_H2O_L = -285.83        # kJ/mol
DFH_H2O_G = -241.82        # kJ/mol
DVAP_H2O_25 = DFH_H2O_G - DFH_H2O_L          # 44,01 kJ/mol
DVAP_H2O_100 = 40.657      # kJ/mol (CRC, 373,15 K)
DSUB_H2O_0 = 51.06         # kJ/mol (CRC, muz sublimatsiyasi, 273,15 K)
DVAP_TOLUENE = 38.06       # kJ/mol (CRC, qaynash haroratida)

# --- azeotroplar: T (°C) va bug fazasidagi suv mass ulushi (w, %) ---------
AZEOTROPE = {
    'toluen':      {'T': 84.1, 'w_water': 0.198, 'x_water': 0.444},
    'sikloheksan': {'T': 69.5, 'w_water': 0.084, 'x_water': 0.300},
    'n-geptan':    {'T': 70.9, 'w_water': 0.125, 'x_water': 0.376},
}

# --- molekulyar sitalar: pora o'lchami (Å) va suv sig'imi (mass %) -------
SIEVES = [
    ('3A',  3.0, 19.5, 'K shakli, A turi', 'faqat suv'),
    ('4A',  4.0, 20.5, 'Na shakli, A turi', 'suv, CO₂, SO₂'),
    ('5A',  5.0, 21.0, 'Ca shakli, A turi', 'suv, n-paraffinlar'),
    ('13X', 10.0, 23.5, 'Na shakli, X turi', 'suv, CO₂, kattaroq molekulalar'),
]

# ======================================================================
# 1. namlik ko'rsatkichlari
# ======================================================================
def water_fraction(wet, dry):
    """Suv ulushi: nam asosda X va quruq asosda w (kg/kg)."""
    return {'X_wet': wet / (wet + dry), 'w_dry': wet / dry}


def loss_on_drying(m0, m1):
    """Ph. Eur. 2.2.32: quruq qoldig' (m/m %)."""
    return (m0 - m1) / m0 * 100.0


def hygroscopicity(m1, m2, m3):
    """Ph. Eur. 5.11: 25 °C, 80 ± 2 % RH, 24 h -> massa o'sishi (%) va sinf."""
    d = (m3 - m2) / (m2 - m1) * 100.0
    if d >= 15.0:
        cls = 'juda higroskopik'
    elif d >= 2.0:
        cls = 'higroskopik'
    elif d >= 0.2:
        cls = 'biroz higroskopik'
    else:
        cls = 'higroskopik emas'
    return {'increase': d, 'class': cls}


def karl_fischer(m_sample, c_titrant, v_titrant):
    """Karl Fischer: 1 mol H2O <-> 1 mol I2. c (mol/L), V (mL), m (g)."""
    n = c_titrant * v_titrant / 1000.0
    m_water = n * M_H2O
    return {'n': n, 'm_water': m_water, 'w_percent': m_water / m_sample * 100.0}


# ======================================================================
# 2. bug'lanish termodinamikasi
# ======================================================================
def vapour_pressure(T, dHvap=DVAP_H2O_100, T_ref=373.15):
    """Klausius–Klapeiron (integral, doimiy ΔvapH)."""
    return 101.325 * math.exp(-dHvap * 1000.0 / R * (1.0 / T - 1.0 / T_ref))


def boiling_temperature(P_kPa, dHvap=DVAP_H2O_100, T_ref=373.15):
    """Bosimdan qaynash harorati (K)."""
    return 1.0 / (1.0 / T_ref - R / (dHvap * 1000.0) * math.log(P_kPa / 101.325))


def equilibrium_moisture(rh, wm=0.05, C=10.0):
    """BET/Langmuir tipidagi muvozanat namligi (kg suv / kg quruq modda)."""
    x = min(max(rh, 0.0), 0.99)
    return wm * C * x / (1.0 + (C - 1.0) * x)


# ======================================================================
# 3. quritish kinetikasi modeli
# ======================================================================
def drying_curve(t, X0=0.35, Xc=0.20, Xe=0.02, k1=0.015, k2=0.080):
    """Ikki bosqichli model: doimiy tezlik + birinchi pasayish bosqichi."""
    if t <= 0:
        return X0
    tc = (X0 - Xc) / k1
    if t <= tc:
        return X0 - k1 * t
    return Xe + (Xc - Xe) * math.exp(-k2 * (t - tc))


def drying_at_temperature(T, t, T_ref=373.15, Ea=30.0, **kw):
    """Arrhenius koeffitsienti bilan kinetik tezlikni haroratga bog'lash (model)."""
    f = math.exp(-Ea * 1000.0 / R * (1.0 / T - 1.0 / T_ref))
    p = dict(kw)
    p['k1'] = kw.get('k1', 0.015) * f
    p['k2'] = kw.get('k2', 0.080) * f
    return drying_curve(t, **p)


# ======================================================================
# 4. kimyoviy quritgichlar
# ======================================================================
def p2o5_capacity():
    """P2O5 + 3H2O -> 3H3PO4: sig'im (massa ulushi, %)."""
    m = 3 * M_H2O
    return {'m_water': m, 'capacity': m / M_P2O5 * 100.0}


def salt_capacity(m_salt, m_hydrate, n_water):
    """Gidratlanuvchi tuz: sig'im (1 g tuzga necha g suv)."""
    return {'capacity': n_water * M_H2O / m_salt, 'm_water': n_water * M_H2O}


def sieve_demand(m_water, capacity_percent):
    """Molekulyar sital massasi (kg) berilgan suv massasini yig'ish uchun."""
    return m_water / (capacity_percent / 100.0)


# ======================================================================
# 5. gidrat quritish
# ======================================================================
HYDRATES = {
    'CuSO4': (M_CUSO4, [('5H2O', 5), ('3H2O', 3), ('H2O', 1), ('0', 0)]),
    'FeSO4': (96.06, [('7H2O', 7), ('H2O', 1), ('0', 0)]),
    'MgSO4': (120.37, [('7H2O', 7), ('H2O', 1), ('0', 0)]),
    'Na2CO3': (105.99, [('10H2O', 10), ('H2O', 1), ('0', 0)]),
}


def hydrate_mass(m_salt_formula, m_start, form_from, form_to):
    """Gidrat quritish mass balansi (kg)."""
    M0, forms = HYDRATES[m_salt_formula]
    n = dict(forms)
    m0 = M0 + n[form_from] * M_H2O
    m1 = M0 + n[form_to] * M_H2O
    kmol = m_start / m0
    m_product = kmol * m1
    m_water = m_start - m_product
    return {'kmol': kmol, 'm_product': m_product, 'm_water': m_water,
            'w_start': n[form_from] * M_H2O / m0 * 100.0,
            'w_end': n[form_to] * M_H2O / m1 * 100.0,
            'water_per_mol': n[form_from] - n[form_to]}


# ======================================================================
# 6. azeotropik quritish
# ======================================================================
def azeotropic_drying(m_solution, w0, w1, entrainer='toluen'):
    """Azeotropik quritish mass balansi (kg)."""
    a = AZEOTROPE[entrainer]
    m_acid = m_solution * (1 - w0)
    m_final = m_acid / (1 - w1)
    m_water_out = m_solution - m_final
    m_dist = m_water_out / a['w_water']
    m_ent_total = m_dist - m_water_out
    # faza ajratish: suv fazasi ~99,95 % suv, organik faza ~99,95 % entrainer
    m_water_phase = m_water_out / 0.9995
    m_org_phase = m_dist - m_water_phase
    m_ent_loss = m_water_phase * 0.0005
    return {'m_acid': m_acid, 'm_final': m_final, 'm_water_out': m_water_out,
            'm_distillate': m_dist, 'm_entrainer': m_ent_total,
            'm_water_phase': m_water_phase, 'm_org_phase': m_org_phase,
            'm_entrainer_loss': m_ent_loss, 'azeo': a}


# ======================================================================
# 7. energetika
# ======================================================================
def evaporation_energy(m_water, dHvap=DVAP_H2O_100):
    """Bug'latish issiqligi (MJ)."""
    n = m_water / M_H2O            # kmol
    return {'n': n, 'Q_MJ': n * dHvap,
            'q_MJ_per_kg': dHvap * 1000.0 / M_H2O / 1000.0}


def energy_kwh(m_water, dHvap=DVAP_H2O_100):
    """1 kg suv bug'latishga kWh ekvivalenti."""
    return m_water * (dHvap * 1000.0 / M_H2O) / 3600.0


def equivalent_heat(m_water, q_MJ):
    """Isitish + bug'latish: model (q_MJ — jami)."""
    return {'Q_MJ': q_MJ, 'kWh': q_MJ * 1000.0 / 3.6}


# ======================================================================
# CSV yozuv
# ======================================================================
def save_data():
    with (ASSETS / 'vakuum.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['P_kPa', 'lgP', 'T_K', 'T_C'])
        P = 101.325
        while P >= 0.10:
            T = boiling_temperature(P)
            w.writerow([f'{P:.5f}', f'{math.log10(P):.5f}', f'{T:.3f}', f'{T - 273.15:.3f}'])
            P *= 0.88
    with (ASSETS / 'azeotrop.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['entrainer', 'T_C', 'w_water', 'x_water',
                                       'kg_water_per_kg_entrainer'])
        for name, a in AZEOTROPE.items():
            w.writerow([name, f'{a["T"]:.1f}', f'{a["w_water"]:.4f}',
                        f'{a["x_water"]:.3f}',
                        f'{a["w_water"] / (1 - a["w_water"]):.4f}'])
    with (ASSETS / 'kinetika.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['t_min', 'X_333', 'X_353', 'X_373', 'X_eq'])
        t = 0.0
        while t <= 60.0:
            w.writerow([f'{t:.3f}',
                        f'{drying_at_temperature(333.15, t):.5f}',
                        f'{drying_at_temperature(353.15, t):.5f}',
                        f'{drying_at_temperature(373.15, t):.5f}',
                        f'{equilibrium_moisture(0.8):.5f}'])
            t += 0.5
    with (ASSETS / 'adsorbsiya.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['RH', 'w_0.03', 'w_0.05', 'w_0.08'])
        for i in range(50):
            rh = i * 0.02
            w.writerow([f'{rh:.4f}',
                        f'{equilibrium_moisture(rh, 0.03):.6f}',
                        f'{equilibrium_moisture(rh, 0.05):.6f}',
                        f'{equilibrium_moisture(rh, 0.08):.6f}'])
            rh += 0.02
    with (ASSETS / 'energiya.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['usul', 'kWh_per_kg', 'q_MJ_per_kg'])
        for name, kwh in [('shkaf, 105 °C', 1.05), ('vakuum', 0.85),
                          ('azeotrop', 1.55), ('molekulyar sital', 0.18)]:
            w.writerow([name, f'{kwh:.3f}', f'{kwh * 3.6:.3f}'])
    return ASSETS


if __name__ == '__main__':
    save_data()
    print('— namlik —')
    print(' X/w:', water_fraction(0.35, 1.0))
    print(' LOD:', round(loss_on_drying(10.0, 9.95), 3), '%')
    print(' higroskopiklik:', hygroscopicity(5.0, 15.0, 15.35))
    print(' KF:', karl_fischer(2.0, 0.5, 0.0222))
    print('— buglanish —')
    print(' ΔvapH(25 °C) =', round(DVAP_H2O_25, 2), 'kJ/mol')
    print(' p(25 °C) =', round(vapour_pressure(298.15, DVAP_H2O_25), 5), 'kPa')
    for P in (101.325, 10.0, 2.5, 1.5, 0.1):
        print('  P =', P, 'kPa -> T =', round(boiling_temperature(P) - 273.15, 2), '°C')
    print(' muvozanat namligi (wm=0,05, C=50):',
          {f'{int(r*100)}%': round(equilibrium_moisture(r), 5) for r in (0.2, 0.5, 0.8, 0.95)})
    print('— kinetika —')
    print(' X(0), X(10), X(20), X(40):',
          [round(drying_curve(t), 4) for t in (0, 10, 20, 40)])
    print('— quritgich —')
    print(' P2O5:', {k: round(v, 3) for k, v in p2o5_capacity().items()})
    print(' CaCl2 (6H2O):', {k: round(v, 3) for k, v in salt_capacity(M_CACL2, 0, 6).items()})
    print(' MgSO4 (7H2O):', {k: round(v, 3) for k, v in salt_capacity(M_MGSO4, 0, 7).items()})
    print(' sital 4A (100 kg suv):', round(sieve_demand(100.0, 20.5), 1), 'kg')
    print('— gidrat —')
    h = hydrate_mass('CuSO4', 1000.0, '5H2O', 'H2O')
    print(' CuSO4·5H2O -> ·H2O:', {k: round(v, 4) for k, v in h.items()})
    h0 = hydrate_mass('CuSO4', 1000.0, '5H2O', '0')
    print(' CuSO4·5H2O -> anhyd:', {k: round(v, 4) for k, v in h0.items()})
    print('— azeotrop —')
    a = azeotropic_drying(1000.0, 0.32, 0.005, 'toluen')
    print(' ', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in a.items() if k != 'azeo'})
    print('— energiya —')
    e = evaporation_energy(316.58)
    print(' ', e)
    print(' kWh/kg suv:', round(energy_kwh(1.0), 4))
    print(' azeotrop Model B energiya: suv', round(316.5829*2.25684, 1),
          'MJ + tol', round(1282.3207*0.4131, 1), 'MJ')
    print(' CSV yozildi:', sorted(p.name for p in ASSETS.glob('*.csv')))
