"""5.4 «Sanoat prinsiplari» — model zaxirasi.

Barcha sonli natijalar ochiq shartli modeldan olingan; real zavod ko'rsatkichlari emas.
Manbalar: OpenStax App. G (ΔfH°), CRC (bug' jadvali), ISO 22400-2:2014 (OEE),
OPC UA OPC-40501-1 C.2.4, IUPAC Gold Book, Ph. Eur. 6.0.
"""
from pathlib import Path
import csv, math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'sanoat'
ASSETS.mkdir(parents=True, exist_ok=True)

# --- molar massalar (g/mol) -----------------------------------------------
M_NH3 = 17.031
M_HNO3 = 63.01
M_O2 = 32.00
M_N2 = 28.014
M_NO = 30.01
M_NO2 = 46.01
M_H2O = 18.015
M_TOLUENE = 92.14
M_CO2 = 44.01

# --- termodinamik (kJ/mol), OpenStax App. G -------------------------------
DFH_NH3_G = -45.90
DFH_HNO3_L = -174.10
DFH_H2O_L = -285.83
DFH_NO_G = 90.25
DFH_NO2_G = 33.20
DH_OXIDATION = -1170.38      # 4NH3 + 5O2 -> 4NO + 6H2O
DH_NO_OXID = -114.10        # 2NO + O2 -> 2NO2
DH_ABSORPTION = -71.72      # 3NO2 + H2O -> 2HNO3 + NO
DH_OVERALL = DFH_HNO3_L + DFH_H2O_L - DFH_NH3_G      # NH3 + 2O2 -> HNO3 + H2O

# --- qatnoq bug' jadvali (CRC / bug' jadvali) ----------------------------
STEAM = [   # (p, MPa), T (°C), h_fg (kJ/kg)
    (0.10, 99.63, 2257.5), (0.50, 151.83, 2108.0), (1.00, 179.89, 2014.6),
    (2.00, 212.42, 1888.7), (4.00, 250.40, 1713.0), (6.00, 275.64, 1565.8),
    (8.00, 295.06, 1441.0)]

# --- iqtisodiyot modeli ---------------------------------------------------
PLANT_TPY = 100000.0         # t/y (98 % li HNO3)
CAPEX_USD_PT = 1200.0        # USD / (t/y) quvvat
FOA_RATE = 0.08              # FOA = 8 % CAPEX / y
OPEX_USD_PT = 420.0          # umumiy ekspluatatsiya xarajati, USD/t
PRICE_USD_PT = 560.0         # model bozor narxi, USD/t
OEE_A, OEE_P, OEE_Q = 0.92, 0.95, 0.99

# --- OPEX tarkibi (model, %) ---------------------------------------------
OPEX_MIX = [('Xom ashyo', 42), ('Energiya', 26), ('Ish kuchi', 8),
            ('Ta’minot va xizmatlar', 9), ('Qurilma va IT', 5),
            ('Ekologik xarajatlar', 6), ('Boshqa', 4)]


# ======================================================================
# 1. Texnologik sxema
# ======================================================================
def conversion(n_in, n_out):
    return n_out / n_in * 100.0


def selectivity(n_desired, n_byproduct):
    return n_desired / (n_desired + n_byproduct) * 100.0


def stage_efficiency(n_out, n_in):
    return n_out / n_in


# ======================================================================
# 2. Mass balansi
# ======================================================================
def chain_balance(m_acid_solution=1000.0, w0=0.68, w1=0.98):
    """NH3 -> NO -> NO2 -> HNO3 (68 %) -> quritish -> 98 %: zanjir balansi."""
    m_hno3 = m_acid_solution * w0
    m_w0 = m_acid_solution - m_hno3
    n_hno3 = m_hno3 * 1000.0 / M_HNO3 / 1000.0   # kmol
    m_nh3 = n_hno3 * M_NH3                   # kmol x kg/kmol -> kg
    m_o2 = 2 * n_hno3 * M_O2
    m_n2 = 3.76 * m_o2
    m_water_formed = n_hno3 * M_H2O
    m_water_bound = 0.5 * n_hno3 * M_H2O
    m_water_in = m_w0 + m_water_bound
    m_water_external = m_water_in - m_water_formed
    m_final = m_hno3 / w1
    m_water_final = m_final - m_hno3
    m_water_removed = m_w0 - m_water_final
    m_toluene = m_water_removed * 0.802 / 0.198
    m_distillate = m_water_removed / 0.198
    return {'m_hno3': m_hno3, 'm_w0': m_w0, 'n_hno3': n_hno3, 'm_nh3': m_nh3, 'm_o2': m_o2,
            'm_n2': m_n2, 'm_water_formed': m_water_formed,
            'm_water_bound': m_water_bound, 'm_water_in': m_water_in,
            'm_water_external': m_water_external, 'm_final': m_final,
            'm_water_final': m_water_final, 'm_water_removed': m_water_removed,
            'm_toluene': m_toluene, 'm_distillate': m_distillate,
            'm_no': n_hno3 * M_NO,
            'm_no2': n_hno3 * M_NO2}


# ======================================================================
# 3. Energiya
# ======================================================================
def oxidation_heat(n_hno3_kmol):
    """NH3 + 2O2 -> HNO3 + H2O bo'yicha reaksion issig'i (GJ)."""
    return n_hno3_kmol * DH_OVERALL / 1000.0


def drying_heat(m_water, m_toluene=0.0):
    """Bug'latish + azeotrop bug'latish energiyasi (MJ)."""
    q_water = m_water * 2256.84 / 1000.0
    q_tol = m_toluene * 413.1 / 1000.0
    return {'Q_water': q_water, 'Q_toluene': q_tol, 'Q_total': q_water + q_tol}


def steam_duty(m_steam, level='2.00'):
    """Bug' sarfi: darajadagi bug' entalpiasidan foydalanib (MJ)."""
    h = dict((('%.2f' % p), hf) for p, t, hf in STEAM)[level]
    return m_steam * h / 1000.0


def pinch_profile():
    """Issiqlik integratsiyasi modeli: oqim haroratlari (°C) va bug' darajalari."""
    stream = [('NH3 kirish', 25), ('Oksidlash reaktori', 880), ('Issiq gaz', 400),
              ('SO2/N2 tozalash', 120), ('Absorbsiya', 60), ('Konsentratsiya', 84),
              ('Azeotrop reabiler', 84), ('Kondenser', 40), ('Mahsulot', 25)]
    return stream, STEAM


def whr_recovery(fraction=0.35):
    """Issiqlikni qayta foydalanish ulushi (model); qaytariladigan bug' massasi."""
    return {'fraction': fraction, 'note': 'model'}


# ======================================================================
# 4. Iqtisodiyot
# ======================================================================
def economics(plant_tpy=PLANT_TPY):
    capex = CAPEX_USD_PT * plant_tpy
    foa = capex * FOA_RATE
    foa_per_t = foa / plant_tpy
    c_var = OPEX_USD_PT - foa_per_t
    oee = OEE_A * OEE_P * OEE_Q
    eff_output = plant_tpy * oee
    margin = PRICE_USD_PT - (c_var + foa_per_t)
    return {'capex': capex, 'foa': foa, 'foa_per_t': foa_per_t,
            'c_var': c_var, 'c_total': c_var + foa_per_t, 'oee': oee,
            'eff_output': eff_output, 'margin': margin,
            'ebitda': margin * eff_output,
            'payback': capex / (margin * eff_output) if margin > 0 else None}


def unit_cost(volume):
    """Birlik FOA: c(V) = c_var + FOA/V (USD/t)."""
    e = economics()
    return e['c_var'] + e['foa'] / volume


# ======================================================================
# 5. Sifat va OEE (ISO 22400-2:2014)
# ======================================================================
def oee(availability, performance, quality):
    return availability * performance * quality


def cpk(cp, cpl, cpu, mean, spec_l, spec_u):
    lower = (mean - spec_l) / (3.0 * cp) if cp > 0 else 0.0
    upper = (spec_u - mean) / (3.0 * cpu) if cpu > 0 else 0.0
    return min(lower, upper)


# ======================================================================
# 6. Ekologiya (model)
# ======================================================================
def waste_factor(m_waste, m_product):
    return m_waste / m_product


def co2e(activity, factor, unit='kg'):
    return activity * factor


# ======================================================================
# CSV yozuv
# ======================================================================
def save_data():
    with (ASSETS / 'oqim.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['bosqich', 'ogilma', 'kirish_kg', 'chiqish_kg', 'izoh'])
        c = chain_balance()
        w.writerow(['Absorbsiya (kirish)', 'NH3', f'{c["m_nh3"]:.2f}', '0',
                    'Katalitik oksidlashdan keyin'])
        w.writerow(['Absorbsiya (kirish)', 'O2', f'{c["m_o2"]:.2f}', '0', 'Havo tarkibida'])
        w.writerow(['Absorbsiya (kirish)', 'N2 (ortiqcha)', f'{c["m_n2"]:.2f}', '0', 'Model: N2/O2 = 3,76'])
        w.writerow(['Absorbsiya (kirish)', 'H2O', f'{c["m_water_external"]:.2f}', '0',
                    'Havo namligi va kislot qaytishi hisobiga'])
        w.writerow(['68 % li eritma', 'HNO3', f'{c["m_hno3"]:.2f}', f'{c["m_hno3"]:.2f}',
                    'Absorbsiya natijasi'])
        w.writerow(['68 % li eritma', 'H2O', f'{c["m_water_final"] + c["m_water_removed"]:.2f}',
                    f'{c["m_w0"]:.2f}', 'Model'])
        w.writerow(['Konsentratsiya', 'H2O (chiqarilgan)', f'{c["m_water_removed"]:.2f}', '0',
                    'Azeotrop yoki konsentratsiya'])
        w.writerow(['Konsentratsiya', 'Toluen', f'{c["m_toluene"]:.2f}', f'{c["m_toluene"]:.2f}',
                    'Aylanadi; yo‘qotish model'])
        w.writerow(['98 % li mahsulot', 'HNO3', f'{c["m_hno3"]:.2f}', f'{c["m_hno3"]:.2f}', 'Tayyor mahsulot'])
        w.writerow(['98 % li mahsulot', 'H2O', f'{c["m_water_final"]:.2f}',
                    f'{c["m_water_final"]:.2f}', 'Tayyor mahsulot'])
    with (ASSETS / 'bug.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['p_MPa', 'T_C', 'h_fg_kJ_kg'])
        for p, t, h in STEAM:
            w.writerow([f'{p:.2f}', f'{t:.2f}', f'{h:.1f}'])
    with (ASSETS / 'opex.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['element', 'ulush_%', 'izoh'])
        for name, pct in OPEX_MIX:
            w.writerow([name, f'{pct}', 'model'])
    with (ASSETS / 'birlik_qiymat.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['V_tpy', 'c_var', 'c_FOA', 'c_total'])
        e = economics()
        for V in (40000, 60000, 80000, 100000, 120000, 150000, 200000, 250000):
            w.writerow([f'{V}', f'{e["c_var"]:.2f}', f'{e["foa"]/V:.2f}',
                        f'{e["c_var"] + e["foa"]/V:.2f}'])
    with (ASSETS / 'issiqlik.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['ogilma', 'T_C', 'tip'])
        stream, _ = pinch_profile()
        for name, t in stream:
            w.writerow([name, f'{t}', 'oqim'])
        for p, t, h in STEAM:
            w.writerow([f'Bug\' {p:.2f} MPa', f'{t}', 'bug\' darajasi'])
    return ASSETS


if __name__ == '__main__':
    save_data()
    c = chain_balance()
    print('— zanjir balansi —')
    for k, v in c.items():
        print('  %-18s %s' % (k, round(v, 4) if isinstance(v, float) else v))
    print('— energiya —')
    print('  oksidlash:', round(oxidation_heat(c['n_hno3']), 1), 'GJ')
    print('  quritish:', {k: round(v, 1) for k, v in drying_heat(c['m_water_removed'], c['m_toluene']).items()})
    print('— iqtisodiyot —')
    e = economics()
    for k, v in e.items():
        print('  %-12s %s' % (k, round(v, 4) if isinstance(v, float) else v))
    print('  birlik FOA:', {V: round(unit_cost(V), 2) for V in (50000, 100000, 200000)})
    print('  OEE:', round(oee(OEE_A, OEE_P, OEE_Q), 4))
    print('  CSV:', sorted(p.name for p in ASSETS.glob('*.csv')))
