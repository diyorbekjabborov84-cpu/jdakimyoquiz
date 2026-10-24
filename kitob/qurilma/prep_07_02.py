#!/usr/bin/env python3
"""7.2 "H2SO3 — sulfit kislota" — taxminiy hisoblar va jadval ma'lumotlari.

Barcha natijalar ochiq shartli hisoblardan; o'lchov ma'lumoti emas.
Manbalar: NIST WebBook (C7446095) — SO2 termodinamikasi va fazaviy o'zgarishlar
(ΔfH° -296,81 kJ/mol; S° 248,223 J/(mol·K); Tb 263,1 K; Pc 78,79 bar);
NIST CCCBDB — r(S=O) 143,10 pm, burchak 119,47°; ATCT (ANL) — eritma va sulfit
kislota termodinamikasi (SO2(aq) -322,82; H2SO3(aq) -608,62 kJ/mol);
NIST Henry kengaytmalari va Maahs (1982) — k_H 1,242 M/atm (25 °C);
OSHA, NIOSH, ACGIH, AIHA ERPG, NAC AEGL, NJ DOH PAC — xavfsizlik chegaralari;
EPA (NAAQS, FGD), NASA (vulkan), EFSA (2016) — sanoat, ekologiya, oziq-ovqat.
"""
from pathlib import Path
import csv
import math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'sulfit'
ASSETS.mkdir(parents=True, exist_ok=True)

R_GAS = 8.314462          # J/(mol*K)
R_ATM = 0.0831446         # L*bar/(mol*K)
RT = 298.15

# --- molekul va termodinamika ----------------------------------------------
M_SO2 = 64.06             # g/mol
M_H2SO3 = 82.08           # g/mol (S 32,06 + O3 48,00 + H2 2,02)
M_SO3 = 80.06
M_H2SO4 = 98.08
M_NAOH = 39.997
M_CAOH2 = 74.093
M_CASO3 = 120.14       # CaSO3
M_N2S2O5 = 190.10
M_NA2SO3 = 126.04
M_NAHSO3 = 104.06
M_I2 = 253.809
M_THIO = 248.18           # Na2S2O3*5H2O
M_O2 = 31.998
M_H2O = 18.015
M_AIR = 28.965

BOND_R = 143.10           # pm, r(S=O)
BOND_ANGLE = 119.47       # grad, ∠O-S-O
BOND_R_SULFITE = 151.0    # pm, r(S-O) in SO3^2-
ANGLE_SULFITE = 106.0     # grad, ∠O-S-O in SO3^2-
DIPOLE = 1.63             # D
IE = 12.30                # eV
EA = 1.06                 # eV

DFH = -296.81             # kJ/mol, gaz fazi
DFG = -300.09             # kJ/mol
S_STD = 248.223           # J/(mol*K)
CP = 39.84                # J/(mol*K)
DFH_SO2_AQ = -322.82      # kJ/mol, SO2(aq, undissoc)
DFH_H2SO3_AQ = -608.62    # kJ/mol, H2SO3(aq, undissoc)

T_B = 263.15              # K, -10,0 °C
T_F = 200.75              # K, -72,4 °C
T_T = 197.70              # K, uchlik nuqtasi
T_C = 430.80              # K, 157,65 °C
P_C = 78.79               # bar
DH_VAP = 24.90            # kJ/mol (231,5-263 K)
RHO_LIQ = 1.434           # g/mL, suyuq SO2 (0 °C)
RHO_GAS_25 = 2.619        # g/L (25 °C, 1 bar)
VAP_TABLE = [(283.15, 230.0), (293.15, 330.0), (303.15, 462.0), (313.15, 630.0)]  # kPa

# --- kislotalik -------------------------------------------------------------
KA1 = 1.54e-2             # pKa1 = 1,81 (apparent, SO2(aq) + H2O ⇌ H+ + HSO3-)
KA2 = 6.3e-8              # pKa2 = 7,2
K1_MAAHS = 0.0132         # mol/L (Maahs, 1982)
HYDRATION_K = 1e-9        # kappa << 1e-9 (SO2 + H2O -> H2SO3)
KW = 1e-14

# --- eruvchanlik ------------------------------------------------------------
SOL_25 = 94.0             # g/L (25 °C, jadval)
KH = 1.242                # mol/(L*atm), 25 °C (Maahs, 1982); NIST: 1,2-1,3 mol/(kg*bar)
H_HENRY = 1.0 / KH        # atm*L/mol
P_SAT_20 = 330.0          # kPa (20 °C, jadval)

# --- sulfit, bisulfit va metabisulfit tuzlari --------------------------------
SALTS = [
    ('Natriy sulfit', 'Na₂SO₃', M_NA2SO3, 1, 'Oq kristall; 27 g/100 mL (20 °C)', 'Alkalin (pH ~9-10)'),
    ('Natriy bisulfit', 'NaHSO₃', M_NAHSO3, 1, 'Oq-sarg‘ish kristall; SO₂ hidli', 'Kislik (pH ~4)'),
    ('Natriy metabisulfit', 'Na₂S₂O₅', M_N2S2O5, 2, 'Oq kristall; SO₂ hidi kuchli', 'Kislik (pH ~4-5)'),
    ('Kalsiy sulfit', 'CaSO₃', M_CASO3, 1, 'Oq, suvda kam eriydi', 'Alkalin'),
    ('Ammoniy sulfit', '(NH₄)₂SO₃', 116.14, 1, 'Oq kristall', 'Alkalin'),
    ('Kaliy sulfit', 'K₂SO₃', 158.26, 1, 'Oq kristall', 'Alkalin'),
    ('Runk sulfit', 'ZnSO₃', 145.45, 1, 'Oq kristall', 'Kislik (amfoter)'),
    ('Kalsiy bisulfit eritmasi', 'Ca(HSO₃)₂', 202.09, 2, 'Faqat eritmada', 'Kislik'),
]

# --- xavfsizlik chegaralari (ppm) ------------------------------------------
LIMITS = [
    ('OSHA PEL (8 soat TWA)', 5.0, '29 CFR 1910.1000; 13 mg/m³'),
    ('NIOSH REL (10 soat TWA)', 2.0, '5 mg/m³'),
    ('NIOSH REL (STEL)', 5.0, '13 mg/m³; 15 daqiqa'),
    ('ACGIH TLV-STEL (2008)', 0.25, 'Shift chegarasi; A4'),
    ('NIOSH IDLH', 100.0, 'Hayot uchun xavfli'),
    ('AIHA ERPG-1 / 2 / 3', 0.3, '0,3 / 3 / 25 ppm'),
    ('NAC AEGL-1 / 2 / 3', 0.2, '0,2 / 0,75 / 30 ppm'),
    ('PAC-1 / 2 / 3', 0.2, '0,2 / 0,75 / 30 ppm'),
]
MG_PER_PPM = 2.62         # mg/m3 (1 ppm = 2,62 mg/m3)
ODOR_THRESHOLD = (0.3, 5.0)

# --- sanoat va ekologiya ----------------------------------------------------
ADI_SULFITE = 0.7         # mg/kg tana vazni (EFSA, 2016; SO2 hisobida)
FGD_WET = (92.0, 99.0)    # % olib tashlash
FGD_DRY = (50.0, 95.0)
FGD_SHARE_WET = 79.0      # % dunyo FGD quvvatida nam skrubber
VOLCANIC_SO2 = (20.0, 25.0)   # mln t/y
COAL_SHARE = (45.0, 50.0)      # % antropogen chiqarishda ko‘mir
US_CUT = 95.0             # % 1995-2023 (ARP + CSAPR)
US_2023 = 0.65            # mln ton (ARP + CSAPR, 2023)
SULFITE_PULP_SHARE = 10.0  # % (suli̇fit usuli bilan kimyoviy pulps)
SMBS_PROD = (2.0, 3.0)    # mln t (2016 -> 2023)
NAAQS_1H = 75.0           # ppb, asosiy standart (2010)
NAAQS_SEC_ANNUAL = 10.0   # ppb, ikkilamchi yillik standart (2024)


def num(x, n=3):
    """Nuqta -> vergul, o'zbekcha format."""
    return ('%.*f' % (n, x)).replace('.', ',')


# ---------------------------------------------------------------- kislotalik
def ph_of(c):
    """Birinchi dissotsiatsiya uchun kvadrat yechim (taxminiy hisob)."""
    h = (-KA1 + math.sqrt(KA1 ** 2 + 4.0 * KA1 * c)) / 2.0
    return dict(c=c, h=h, pct=100.0 * h / c, ph=-math.log10(h))


def ph_series(cs=(0.0010, 0.0050, 0.0100, 0.0200, 0.0500, 0.1000,
                  0.2000, 0.5000, 1.0000, 1.2000, 1.4674)):
    return [ph_of(c) for c in cs]


def speciation(ph):
    """SO2(aq) / HSO3- / SO3^2- ulushlari (taxminiy hisob)."""
    h = 10.0 ** (-ph)
    r1 = KA1 / h
    r2 = KA2 / h
    t = 1.0 + r1 + r1 * r2
    return dict(ph=ph, so2=100.0 / t, hso3=100.0 * r1 / t, so3=100.0 * r1 * r2 / t)


def saturated_solution():
    """To'yingan SO2 eritmasi: c, pH, dissotsiatsiya (taxminiy hisob)."""
    c = SOL_25 / M_SO2
    p = ph_of(c)
    return dict(c=c, m_g_per_l=SOL_25, h=p['h'], ph=p['ph'], pct=p['pct'])


def sulfite_ion(c_so2, ph):
    """[SO3^2-] = Ka2*[HSO3-]/[H+] (taxminiy hisob)."""
    h = 10.0 ** (-ph)
    hso3 = KA1 * c_so2 / h
    return KA2 * hso3 / h


# ---------------------------------------------------------------- fizik
def vapor_pressure(t_k, dh=DH_VAP, t_ref=T_B, p_ref=1.01325):
    """Clausius-Clapeyron bilan bug' bosimi (bar), Tb dan boshlanadi."""
    return p_ref * math.exp(-dh * 1000.0 / R_GAS * (1.0 / t_k - 1.0 / t_ref))


def vapor_pressure_table_25():
    """Jadval qiymatlari orasida geometrik interpolatsiya (kPa)."""
    (t1, p1), (t2, p2) = VAP_TABLE[1], VAP_TABLE[2]
    return p1 * (p2 / p1) ** ((298.15 - t1) / (t2 - t1))


def gas_density(t_k, p_bar=1.01325):
    """Ideal gaz zichligi (g/L)."""
    return p_bar * M_SO2 / (R_ATM * t_k)


def henry_constant():
    """Henry qonuni: c = k_H*p va H = p/c (taxminiy hisob)."""
    c = KH * 1.0                      # 1 atm SO2 qism bosimi
    return dict(kh=KH, c=c, m_g_per_l=c * M_SO2, h=H_HENRY)


# ---------------------------------------------------------------- tahlil
def iodometric(v=0.02500, c=0.1000):
    """Ripper usuli: SO3^2- + I2 + H2O -> SO4^2- + 2I- + 2H+ (taxminiy hisob)."""
    n = v * c
    return dict(v=v, c=c, n_so3=n, m_so3=n * M_NA2SO3,
                n_i2=n, m_i2=n * M_I2, n_thio=2.0 * n, m_thio=2.0 * n * M_THIO)


def iodometric_series(cs=(0.0200, 0.0500, 0.1000, 0.2000, 0.2500)):
    return [iodometric(0.02500, c) for c in cs]


# ---------------------------------------------------------------- neytralizatsiya
def neutralisation(m_solution=1000.0, w=0.10):
    """1000 kg 10 % li SO2 eritmasini neytralizatsiya qilish (taxminiy hisob)."""
    m_so2 = m_solution * w
    n = m_so2 / M_SO2
    return dict(m_solution=m_solution, w=w, m_so2=m_so2, n=n,
                naoh_nahs3=n * M_NAOH, naoh_na2so3=2.0 * n * M_NAOH,
                caoh2=n * M_CAOH2, casao3=n * M_CASO3,
                na2s2o5=0.5 * n * M_N2S2O5)


# ---------------------------------------------------------------- ekvivalent
def equivalents():
    """Ekvivalent massa (taxminiy hisob)."""
    return dict(h2so3=M_H2SO3 / 2.0, so2_redox=M_SO2 / 2.0,
                hso3=M_NAHSO3, so3=M_NA2SO3,
                n_protons=2, n_electrons=2,
                eq_per_kg=M_H2SO3 / 2.0)


# ---------------------------------------------------------------- kontakt usuli
def contact(m_so2=1000.0):
    """Kontakt usuli: SO2 -> SO3 -> H2SO4 moddiy balansi (taxminiy hisob)."""
    n = m_so2 / M_SO2
    m_so3 = n * M_SO3
    m_o2 = 0.5 * n * M_O2
    m_h2o = n * M_H2O
    m_h2so4 = n * M_H2SO4
    return dict(m_so2=m_so2, n=n, m_so3=m_so3, m_o2=m_o2, m_h2o=m_h2o,
                m_h2so4=m_h2so4,
                balance=m_so2 + m_o2 + m_h2o - m_h2so4)


# ---------------------------------------------------------------- havo
def air_load(ppm, volume=1.0):
    """Havo massasining hisobi (mg/m3 -> mg)."""
    mg = ppm * MG_PER_PPM * volume
    return dict(ppm=ppm, volume=volume, mg=mg, g=mg / 1000.0)


def main():
    # 1) kislotalik: pH bo'yicha spetsiatsiya
    with open(ASSETS / 'kislotalik.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['pH', 'SO2(aq), %', 'HSO3-, %', 'SO3^2-, %'])
        for ph in [i * 0.25 for i in range(0, 57)]:
            s = speciation(ph)
            w.writerow([num(s['ph'], 2), num(s['so2'], 3),
                        num(s['hso3'], 3), num(s['so3'], 4)])

    # 2) fizik: bug' bosimi va gaz zichligi
    with open(ASSETS / 'fizik.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['T, K', 'T, °C', 'p_sat, bar', 'rho_gaz, g/L'])
        for i in range(0, 21):
            t = 185.0 + i * 10.0
            w.writerow([num(t, 1), num(t - 273.15, 2),
                        num(vapor_pressure(t), 4), num(gas_density(t), 4)])

    # 3) eritma: konsentratsiya, pH va dissotsiatsiya
    with open(ASSETS / 'eritma.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['c, mol/L', 'h, mol/L', 'dissotsiatsiya, %', 'pH'])
        for p in ph_series():
            w.writerow([num(p['c'], 4), num(p['h'], 6), num(p['pct'], 2), num(p['ph'], 3)])

    # 4) tuzlar: sulfit, bisulfit, metabisulfit
    with open(ASSETS / 'tuzlar.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Tuz', 'Formula', 'M, g/mol', 'SO2 mazmuni, %', 'Xususiyat'])
        for name, formula, m, ns, note, character in SALTS:
            so2 = M_SO2 * ns / m * 100.0
            w.writerow([name, formula, num(m, 2), num(so2, 1), note + '; ' + character])

    # 5) ekvivalent
    with open(ASSETS / 'ekvivalent.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Shakl', 'M, g/mol', 'Proton/elektron soni', 'Ekvivalent, g/eq'])
        for name, m, n in [('H₂SO₃ (kislota)', M_H2SO3, 2), ('SO₂ (redoks)', M_SO2, 2),
                           ('HSO₃⁻ (kislota)', M_NAHSO3, 1), ('SO₃²⁻ (redoks)', M_NA2SO3, 2)]:
            w.writerow([name, num(m, 2), n, num(m / n, 3)])

    # 6) yodometriya (Ripper)
    with open(ASSETS / 'yodometriya.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['V, mL', 'c, mol/L', 'n(SO3^2-), mol', 'm(I2), g', 'm(Na2S2O3), g'])
        for r in iodometric_series():
            w.writerow([num(r['v'] * 1000.0, 2), num(r['c'], 4), num(r['n_so3'], 5),
                        num(r['m_i2'], 4), num(r['m_thio'], 4)])

    # 7) neytralizatsiya
    with open(ASSETS / 'neytralizatsiya.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Mahsulot', 'Reaksiyon', 'Massa, kg'])
        nn = neutralisation()
        w.writerow(['NaHSO₃', 'SO₂ + NaOH → NaHSO₃', num(nn['naoh_nahs3'], 1)])
        w.writerow(['Na₂SO₃', 'SO₂ + 2NaOH → Na₂SO₃ + H₂O', num(nn['naoh_na2so3'], 1)])
        w.writerow(['CaSO₃', 'SO₂ + Ca(OH)₂ → CaSO₃ + H₂O', num(nn['caoh2'], 1)])
        w.writerow(['CaSO₃ (hosil)', 'Ca(OH)₂ + SO₂ → CaSO₃ + H₂O', num(nn['casao3'], 1)])
        w.writerow(['Na₂S₂O₅', '2NaOH + 2SO₂ → Na₂S₂O₅ + H₂O', num(nn['na2s2o5'], 1)])

    # 8) kontakt usuli
    with open(ASSETS / 'kontakt.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Bosqich', 'Reaksiyon', 'Massa, kg'])
        cc = contact()
        w.writerow(['Kirish', '1000 kg SO₂', num(cc['m_so2'], 1)])
        w.writerow(['Oksidlanish', '2SO₂ + O₂ ⇌ 2SO₃', num(cc['m_so3'], 1)])
        w.writerow(['Katalizator', 'V₂O₅ / Pt, 400-450 °C', '—'])
        w.writerow(['Gidratlanish', 'SO₃ + H₂O → H₂SO₄', num(cc['m_h2o'], 1)])
        w.writerow(['Mahsulot', 'H₂SO₄ (100 %)', num(cc['m_h2so4'], 1)])
        w.writerow(['Kirish - chiqish', 'moddiy balans', num(cc['balance'], 2)])

    # 9) xavfsizlik
    with open(ASSETS / 'xavfsizlik.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Chegara', 'Qiymat, ppm', 'Izoh'])
        for name, value, note in LIMITS:
            w.writerow([name, num(value, 2), note])

    # 10) sanoat va ekologiya
    with open(ASSETS / 'sanoat.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Ko‘rsatkich', 'Qiymat', 'Manba / izoh'])
        w.writerow(['Vulkan SO₂', '%s-%s mln t/y' % (num(VOLCANIC_SO2[0], 0), num(VOLCANIC_SO2[1], 0)), 'NASA, 2017'])
        w.writerow(['Ko‘hir hissasi', '%s-%s %%' % (num(COAL_SHARE[0], 0), num(COAL_SHARE[1], 0)), 'Antropogen chiqarish'])
        w.writerow(['AQSh elektr stansiyalari', '−%s %% (1995-2023)' % num(US_CUT, 0), 'EPA ARP + CSAPR'])
        w.writerow(['AQSh 2023 yili', '%s mln ton' % num(US_2023, 2), 'ARP + CSAPR'])
        w.writerow(['Nam skrubber (FGD)', '%s-%s %%' % (num(FGD_WET[0], 0), num(FGD_WET[1], 0)), 'Ohak / ohakli tosh'])
        w.writerow(['Sulfit usuli bilan pulps', '< %s %%' % num(SULFITE_PULP_SHARE, 0), 'Kimyoviy pulpsning ulushi'])
        w.writerow(['Na₂S₂O₅ ishlab chiqarish', '%s-%s mln t' % (num(SMBS_PROD[0], 1), num(SMBS_PROD[1], 1)), '2016 -> 2023'])
        w.writerow(['NAAQS (asosiy, 1 soat)', '%s ppb' % num(NAAQS_1H, 0), 'EPA, 2010'])
        w.writerow(['NAAQS (ikkilamchi, yillik)', '%s ppb' % num(NAAQS_SEC_ANNUAL, 0), 'EPA, 2024'])
        w.writerow(['ADI (sulfitlar)', '%s mg/kg tana vazni' % num(ADI_SULFITE, 1), 'EFSA, 2016 (SO₂ hisobida)'])

    print('10 CSV yozildi:', ASSETS)


if __name__ == '__main__':
    main()
