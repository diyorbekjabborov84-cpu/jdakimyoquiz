#!/usr/bin/env python3
"""7.1 "H2S — vodorod sulfid" — taxminiy hisoblar va jadval ma'lumotlari.

Barcha natijalar ochiq shartli hisoblardan; o'lchov ma'lumoti emas.
Manbalar: NIST WebBook (C7783064) — termodinamika, fazaviy o'zgarishlar;
NIST CCCBDB (Coo/DeL 1975) — r(H-S) 1,3356 A, burchak 92,11°; EPA IRIS (0061tr) va
ATSDR (tp114-c4) — eruvchanlik 3,98 g/L (20 °C), pKa1 7,04, pKa2 11,96, bug' bosimi;
UMass / URI / OpenStax Ksp jadvallari; OSHA, NIOSH, ACGIH, ICSC 1326 — xavfsizlik;
Claus usuli (Wikipedia, US EPA AP-42 8.13) — sanoat ma'lumotlari.
"""
from pathlib import Path
import csv
import math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'h2s'
ASSETS.mkdir(parents=True, exist_ok=True)

R_GAS = 8.314462          # J/(mol*K)
R_ATM = 0.0831446         # L*bar/(mol*K)
RT = 298.15

# --- molekul va termodinamika ----------------------------------------------
M_H2S = 34.081
M_S = 32.06
M_H2O = 18.015
M_SO2 = 64.06
M_O2 = 31.998
M_I2 = 253.809
M_THIO = 248.18           # Na2S2O3*5H2O
M_NAOH = 39.997
M_CAOH2 = 74.093
M_CAS = 72.14

BOND_R = 1.3356           # A, NIST CCCBDB
BOND_ANGLE = 92.11        # grad
BOND_D = 347.0            # kJ/mol
DIPOLE = 0.97             # D
IE = 10.46                # eV
PA = 705.0                # kJ/mol
DFH = -20.6               # kJ/mol, gaz fazi
DFG = -37.28              # kJ/mol
S_STD = 205.81            # J/(mol*K)
CP = 34.25                # J/(mol*K)
T_B = 212.87              # K
T_F = 190.85              # K
T_T = 187.66              # K
T_C = 373.3               # K
P_C = 89.63               # bar
RHO_C = 10.2              # mol/L
DH_VAP = 19.5             # kJ/mol, 200 K
P_25 = 15600.0            # mmHg, 25 °C
AUTOIGN = 232.0           # °C
FLAM_LO, FLAM_HI = 4.0, 44.0   # % hajm, ICSC 1326
RHO_G_0 = 1.539           # g/L, 0 °C
RHO_G_25 = 1.39           # g/L, 25 °C
M_AIR = 28.965

KA1 = 9.1e-8              # pKa1 = 7,04
KA2 = 1.2e-12             # pKa2 = 11,96 (manbada 12-19)
SOL_20 = 3.98             # g/L
SOL_10 = 5.3              # g/L
SOL_25 = 1.22             # g/L

# --- metall sulfidlar: Ksp (25 °C) -----------------------------------------
SULFIDES = [
    ('CaS', 'CaS', 8.0e-6, 'Oq; suvda yaxshi eriydi'),
    ('MnS', 'MnS', 5.1e-15, 'Pushti (α) yoki yashil (β)'),
    ('FeS', 'FeS', 4.9e-18, 'Qora; sulfid kislota bilan oson eriydi'),
    ('CoS', 'CoS', 5.9e-21, 'Qora'),
    ('NiS', 'NiS', 3.0e-21, 'Qora'),
    ('ZnS', 'ZnS', 2.0e-25, 'Oq'),
    ('CdS', 'CdS', 1.0e-28, 'Sariq'),
    ('PbS', 'PbS', 3.2e-28, 'Qora'),
    ('CuS', 'CuS', 7.9e-37, 'Qora'),
    ('Ag₂S', 'Ag₂S', 1.0e-49, 'Qora'),
    ('HgS', 'HgS', 2.0e-53, 'Qora (sublimatsiyada qizil)'),
]

# --- xavfsizlik chegaralari ------------------------------------------------
LIMITS = [
    ('OSHA PEL (yuqori chegar)', 20.0, '29 CFR 1910.1000, Z-2'),
    ('OSHA cho‘qqa istisno', 50.0, '10 daqiqa davomida'),
    ('NIOSH REL (10 daqiqa)', 10.0, 'Yuqori chegar'),
    ('ACGIH TLV-TWA (8 soat)', 1.0, '2010-yildan'),
    ('ACGIH TLV-STEL (15 daqiqa)', 5.0, '2010-yildan'),
    ('NIOSH IDLH', 100.0, 'Hayot uchun xavfli'),
    ('AIHA ERPG-1 / 2 / 3', 0.1, '0,1 / 30 / 100 ppm'),
    ('PAC-1 / 2 / 3', 0.51, '0,51 / 27 / 50 ppm'),
]
MG_PER_PPM = 1.40         # mg/m3 (1 ppm = 1,40 mg/m3)

# --- sanoat (Claus) --------------------------------------------------------
CLAUS_THERMAL = dict(dh=-518.0)
CLAUS_CAT = dict(dh=-1165.6)
CLAUS_STAGE_T = [315.0, 240.0, 200.0]     # °C, katalizator qatlamlari
CLAUS_RECOVERY = [(2, 90.0), (3, 95.5), (4, 96.5)]
CLAUS_LIMIT = 98.0
TAIL_GAS = (0.8, 1.5)


def num(x, n=3):
    """Nuqta -> vergul, o'zbekcha format."""
    return ('%.*f' % (n, x)).replace('.', ',')


# ---------------------------------------------------------------- kislotalik
def ph_of(c):
    """Kuchsiz kislota uchun kvadrat yechim (taxminiy hisob)."""
    h = (-KA1 + math.sqrt(KA1 ** 2 + 4.0 * KA1 * c)) / 2.0
    return dict(c=c, h=h, pct=100.0 * h / c, ph=-math.log10(h))


def ph_series(cs=(0.0005, 0.001, 0.002, 0.005, 0.010, 0.020, 0.050, 0.100,
                  0.200, 0.500, 1.000, 2.000)):
    return [ph_of(c) for c in cs]


def speciation(ph):
    """H2S / HS- / S2- ulushlari (taxminiy hisob)."""
    h = 10.0 ** (-ph)
    r1 = KA1 / h
    r2 = KA2 / h
    t = 1.0 + r1 + r1 * r2
    return dict(ph=ph, h2s=100.0 / t, hs=100.0 * r1 / t, s2=100.0 * r1 * r2 / t)


def saturated_solution():
    """To'yingan H2S eritmasi: c, pH (taxminiy hisob)."""
    c = SOL_20 / M_H2S
    p = ph_of(c)
    return dict(c=c, m_g_per_l=SOL_20, h=p['h'], ph=p['ph'], pct=p['pct'])


def sulfide_ion(c_h2s, ph):
    """[S2-] = Ka1*Ka2*[H2S]/[H+]^2 (taxminiy hisob)."""
    h = 10.0 ** (-ph)
    return KA1 * KA2 * c_h2s / (h * h)


# ---------------------------------------------------------------- fizik
def vapor_pressure(t_k, dh=DH_VAP, t_ref=T_B, p_ref=1.01325):
    """Clausius-Clapeyron bilan bug' bosimi (bar)."""
    return p_ref * math.exp(-dh * 1000.0 / R_GAS * (1.0 / t_k - 1.0 / t_ref))


def gas_density(t_k, p_bar=1.01325):
    """Ideal gaz zichligi (g/L)."""
    return p_bar * M_H2S / (R_ATM * t_k)


def henry_constant():
    """Suv bilan gaz muvozanati: H = p/c (taxminiy hisob)."""
    c = SOL_20 / M_H2S
    p_bar = P_25 / 760.0 * 1.01325
    return p_bar / c, p_bar, c


# ---------------------------------------------------------------- tahlil
def iodometric(v=0.1000, c=0.0500):
    """H2S + I2 -> S + 2HI  bo'yicha yodometrik aniqlash (taxminiy hisob)."""
    n = v * c
    n_i2 = n
    return dict(v=v, c=c, n_h2s=n, m_h2s=n * M_H2S,
                n_i2=n_i2, m_i2=n_i2 * M_I2,
                n_thio=2.0 * n_i2, m_thio=2.0 * n_i2 * M_THIO)


def iodometric_series(cs=(0.0100, 0.0250, 0.0500, 0.1000, 0.2500)):
    return [iodometric(0.1000, c) for c in cs]


# ---------------------------------------------------------------- cho'qma
def precipitation(c_h2s=0.100, phs=(1.0, 3.0, 7.0, 10.0)):
    """Har bir sulfid uchun [M2+] chegari (taxminiy hisob)."""
    out = []
    for ph in phs:
        s2 = sulfide_ion(c_h2s, ph)
        row = dict(ph=ph, s2=s2)
        for name, formula, ksp, color in SULFIDES:
            row[name] = ksp / s2
        out.append(row)
    return out


# ---------------------------------------------------------------- neytralizatsiya
def neutralisation(m_solution=1000.0, w=0.10):
    """1000 kg 10 % li eritmada NaOH va Ca(OH)2 talabi (taxminiy hisob)."""
    m_h2s = m_solution * w
    n = m_h2s / M_H2S
    return dict(m_solution=m_solution, w=w, m_h2s=m_h2s, n=n,
                naoh_nash=n * M_NAOH, naoh_na2s=2.0 * n * M_NAOH,
                caoh2=n * M_CAOH2, cas=n * M_CAS,
                eq_mass=M_H2S / 2.0)


# ---------------------------------------------------------------- Claus
def claus(m_h2s=1000.0):
    """Claus usuli moddiy balansi (taxminiy hisob)."""
    n = m_h2s / M_H2S
    # termik bosqich: 2 H2S + 3 O2 -> 2 SO2 + 2 H2O (1/3 H2S yondiriladi)
    n_burn = n / 3.0
    n_so2_therm = n_burn
    n_h2o_therm = n_burn
    n_o2 = 1.5 * n_burn
    # katalitik bosqich: 2 H2S + SO2 -> 3 S + 2 H2O
    n_h2s_cat = n - n_burn
    n_so2_cat = n_h2s_cat / 2.0
    n_s = 3.0 * n_so2_cat
    n_h2o_cat = 2.0 * n_so2_cat
    m_in = m_h2s + n_o2 * M_O2
    m_out = n_s * M_S + (n_h2o_therm + n_h2o_cat) * M_H2O
    return dict(m_h2s=m_h2s, n=n, n_burn=n_burn, n_so2_therm=n_so2_therm,
                n_o2=n_o2, n_h2s_cat=n_h2s_cat, n_so2_cat=n_so2_cat,
                n_s=n_s, m_s=n_s * M_S, m_so2=n_so2_cat * M_SO2,
                m_h2o=(n_h2o_therm + n_h2o_cat) * M_H2O,
                m_o2=n_o2 * M_O2, m_in=m_in, m_out=m_out,
                balance=m_in - m_out)


def full_oxidation(m_h2s=1000.0):
    """3 H2S + 3/2 O2 -> 3 S + 3 H2O (taxminiy hisob)."""
    n = m_h2s / M_H2S
    m_s = n * M_S
    m_h2o = n * M_H2O
    m_o2 = 0.5 * n * M_O2
    return dict(m_h2s=m_h2s, n=n, m_s=m_s, m_h2o=m_h2o, m_o2=m_o2,
                m_in=m_h2s + m_o2, m_out=m_s + m_h2o, balance=m_h2s + m_o2 - m_s - m_h2o)


# ---------------------------------------------------------------- havo
def air_load(ppm, volume=1.0):
    """1 m3 (yoki boshqa hajm) havo massasining hisobi."""
    mg = ppm * MG_PER_PPM * volume
    return dict(ppm=ppm, volume=volume, mg=mg, g=mg / 1000.0)


def main():
    # 1) kislotalik: pH bo'yicha spetsiatsiya
    with open(ASSETS / 'kislotalik.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['pH', 'H2S, %', 'HS-, %', 'S2-, %'])
        for ph in [i * 0.25 for i in range(0, 57)]:
            s = speciation(ph)
            w.writerow([num(s['ph'], 2), num(s['h2s'], 3), num(s['hs'], 3), num(s['s2'], 4)])

    # 2) fizik: bug' bosimi va gaz zichligi
    with open(ASSETS / 'fizik.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['T, K', 'T, °C', 'p_sat, bar', 'rho_gaz, g/L'])
        for i in range(0, 21):
            t = 185.0 + i * 10.0
            w.writerow([num(t, 1), num(t - 273.15, 2),
                        num(vapor_pressure(t), 4), num(gas_density(t), 4)])

    # 3) eritma: pH va dissotsiatsiya
    with open(ASSETS / 'eritma.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['c, mol/L', 'h, mol/L', 'dissotsiya, %', 'pH'])
        for p in ph_series():
            w.writerow([num(p['c'], 4), num(p['h'], 6), num(p['pct'], 2), num(p['ph'], 3)])

    # 4) metall sulfidlar: Ksp
    with open(ASSETS / 'metall.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['sulfid', 'Ksp', 'lg Ksp', 'rang'])
        for name, formula, ksp, color in SULFIDES:
            w.writerow([formula, ('%.1e' % ksp).replace('e-', '×10⁻').replace('e+', '×10'),
                        num(math.log10(ksp), 2), color])

    # 5) sulfidlar: [M2+] chegari pH bo'yicha
    with open(ASSETS / 'sulfidlar.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['pH', '[S2-], mol/L'] + [s[1] for s in SULFIDES])
        for row in precipitation():
            w.writerow([num(row['ph'], 1), '%.2e' % row['s2']] +
                       ['%.2e' % row[s[0]] for s in SULFIDES])

    # 6) yodometriya
    with open(ASSETS / 'yodometriya.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['c(H2S), mol/L', 'n(H2S), mol', 'm(I2), g',
                                       'm(Na2S2O3*5H2O), g'])
        for r in iodometric_series():
            w.writerow([num(r['c'], 4), num(r['n_h2s'], 6), num(r['m_i2'], 4),
                        num(r['m_thio'], 4)])

    # 7) neytralizatsiya
    with open(ASSETS / 'neytralizatsiya.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['parametr', 'qiymat, kg'])
        nn = neutralisation()
        w.writerow(['m(H2S) 10 % li 1000 kg eritmada', num(nn['m_h2s'], 1)])
        w.writerow(['NaOH (NaHS gacha)', num(nn['naoh_nash'], 1)])
        w.writerow(['NaOH (Na2S gacha)', num(nn['naoh_na2s'], 1)])
        w.writerow(['Ca(OH)2', num(nn['caoh2'], 1)])
        w.writerow(['CaS', num(nn['cas'], 1)])

    # 8) ekvivalent
    with open(ASSETS / 'ekvivalent.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['parametr', 'qiymat'])
        nn = neutralisation()
        w.writerow(['molar massa, g/mol', num(M_H2S, 3)])
        w.writerow(['ekvivalent massa, g/eq', num(nn['eq_mass'], 3)])
        w.writerow(['n(H2S) 1 kg da, mol', num(1.0 / M_H2S, 3)])
        w.writerow(['H+ ekvivalenti 1 kg da, mol', num(2.0 / M_H2S, 3)])

    # 9) xavfsizlik
    with open(ASSETS / 'xavfsizlik.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['chegara', 'ppm', 'mg/m3', 'mg 1 m3 da', 'izoh'])
        for name, ppm, note in LIMITS:
            w.writerow([name, num(ppm, 2), num(ppm * MG_PER_PPM, 2),
                        num(ppm * MG_PER_PPM, 2), note])

    # 10) sanoat (Claus)
    with open(ASSETS / 'sanoat.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['parametr', 'qiymat'])
        cl = claus(); fo = full_oxidation()
        w.writerow(['1000 kg H2S -> S (Claus), kg', num(cl['m_s'], 1)])
        w.writerow(['1000 kg H2S -> S (to‘liq oksidlanish), kg', num(fo['m_s'], 1)])
        w.writerow(['1000 kg H2S -> H2O (Claus), kg', num(cl['m_h2o'], 1)])
        w.writerow(['1000 kg H2S uchun SO2, kg', num(cl['m_so2'], 1)])
        w.writerow(['1000 kg H2S uchun O2, kg', num(cl['m_o2'], 1)])
        w.writerow(['kirish − chiqish (Claus), kg', num(cl['balance'], 2)])

    # --- konsol chiqishi ---------------------------------------------------
    print('— molekula va termodinamika —')
    print('  M = %s g/mol;  r(H–S) = %s A;  burchak %s°;  D = %s kJ/mol;  mu = %s D'
          % (num(M_H2S, 3), num(BOND_R, 4), num(BOND_ANGLE, 2), num(BOND_D, 1), num(DIPOLE, 2)))
    print('  ΔfH°(g) = %s kJ/mol;  ΔfG° = %s kJ/mol;  S° = %s J/mol*K;  Cp = %s J/mol*K'
          % (num(DFH, 1), num(DFG, 2), num(S_STD, 2), num(CP, 2)))
    print('  Tb = %s K;  Tf = %s K;  Pc = %s bar;  rho_c = %s mol/L'
          % (num(T_B, 2), num(T_F, 2), num(P_C, 2), num(RHO_C, 1)))
    print('— kislotalik —')
    ss = saturated_solution()
    print('  to‘yingan eritma: c = %s mol/L;  pH (taxminiy hisob) = %s;  haqiqiy ~4,5'
          % (num(ss['c'], 4), num(ss['ph'], 3)))
    for ph in (1.0, 4.0, 7.4, 10.0, 13.0):
        s = speciation(ph)
        print('  pH %s: H2S %s %%;  HS- %s %%;  S2- %s %%'
              % (num(ph, 1), num(s['h2s'], 2), num(s['hs'], 2), num(s['s2'], 4)))
    print('— eritma pH —')
    for p in ph_series((0.001, 0.010, 0.100, 1.000)):
        print('  c = %s M -> h = %s M;  diss = %s %%;  pH = %s'
              % (num(p['c'], 3), num(p['h'], 6), num(p['pct'], 2), num(p['ph'], 3)))
    print('— bug‘lanish (taxminiy hisob) —')
    for t in (190.0, 200.0, 212.87, 240.0, 298.15):
        print('  T = %s K (%s °C):  p = %s bar;  rho_gaz = %s g/L'
              % (num(t, 2), num(t - 273.15, 2), num(vapor_pressure(t), 4),
                 num(gas_density(t), 4)))
    h_const, p_bar, c_sat = henry_constant()
    print('  Henry (taxminiy hisob): H = p/c = %s kPa*L/mol' % num(h_const * 100.0, 0))
    p_calc = vapor_pressure(298.15)
    print('  p(25 °C): hisoblangan %s bar;  jadvaldagi %s bar;  farq %s %%'
          % (num(p_calc, 2), num(P_25 / 760.0 * 1.01325, 2),
             num(100.0 * (p_calc - P_25 / 760.0 * 1.01325) / (P_25 / 760.0 * 1.01325), 1)))
    print('— yodometriya —')
    io = iodometric()
    print('  100,0 mL 0,0500 M:  n(H2S) = %s mol;  m(I2) = %s g;  tiosulfat = %s g'
          % (num(io['n_h2s'], 5), num(io['m_i2'], 4), num(io['m_thio'], 4)))
    print('— cho‘qma chegarasi (taxminiy hisob) —')
    for row in precipitation(0.100, (1.0, 7.0)):
        print('  pH %s: [S2-] = %s mol/L;  PbS uchun [Pb2+] chegari = %s mol/L'
              % (num(row['ph'], 1), '%.2e' % row['s2'], '%.2e' % row['PbS']))
    print('— neytralizatsiya va ekvivalent —')
    nn = neutralisation()
    print('  1000 kg 10 %% li eritma: H2S %s kg;  NaOH %s kg (NaHS) / %s kg (Na2S);'
          '  Ca(OH)2 %s kg;  ekvivalent massa %s g/eq'
          % (num(nn['m_h2s'], 1), num(nn['naoh_nash'], 1), num(nn['naoh_na2s'], 1),
             num(nn['caoh2'], 1), num(nn['eq_mass'], 3)))
    print('— Claus moddiy balansi —')
    cl = claus(); fo = full_oxidation()
    print('  1000 kg H2S -> S %s kg;  H2O %s kg;  SO2 %s kg;  O2 %s kg;  kirish-chiqish %s kg'
          % (num(cl['m_s'], 1), num(cl['m_h2o'], 1), num(cl['m_so2'], 1),
             num(cl['m_o2'], 1), num(cl['balance'], 2)))
    print('  to‘liq oksidlanish: S %s kg;  H2O %s kg;  O2 %s kg;  balans %s kg'
          % (num(fo['m_s'], 1), num(fo['m_h2o'], 1), num(fo['m_o2'], 1), num(fo['balance'], 2)))
    print('CSV: eritma.csv, ekvivalent.csv, fizik.csv, kislotalik.csv, metall.csv,')
    print('     neytralizatsiya.csv, sanoat.csv, sulfidlar.csv, xavfsizlik.csv, yodometriya.csv')


if __name__ == '__main__':
    main()
