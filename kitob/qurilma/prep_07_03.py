#!/usr/bin/env python3
"""7.3 "H2SO4 — sulfat kislota (tuzilishi)" — taxminiy hisoblar va jadval ma'lumotlari.

Barcha natijalar ochiq shartli hisoblardan; o'lchov ma'lumoti emas.
Manbalar: NIST Chemistry WebBook (C7664939) — ΔfH°(g) -735,13 kJ/mol, S°(g) 298,78
J/(mol·K), proton affinity 699,4 kJ/mol, gaz fazidagi kislotalik ΔrG° 1265 ± 10 kJ/mol;
NIST JANAF (Chase, 1998) va Kuchitsu/Sue (1981) — r(S=O) 1,422 Å, r(S-O) 1,574 Å,
r(O-H) 0,970 Å, ∠OSO 123,3°/101,3°, ∠HOS 108,5°, τ(H-O-S-O) 89,1°, C2 simmetriya;
NIST CCCBDB (C7664939) — geometrik ma'lumotlar; ab initio muvozanat tuzilmasi
(2007) — r(S=O) 1,4099 Å, r(S-O) 1,5751 Å, τ -86,66°; Raman/IR ma'lumotlari
(Myhre, 2003; Attaia, 2020) — SO4^2- nu1 981, nu2 451, nu3 1104, nu4 617 cm^-1;
OSHA/NIOSH/ACGIH/AIHA ERPG — xavfsizlik chegaralari; USGS (2024), S&P Global (2025),
Glencore (2024) — sanoat statistikasi; IUCr (2012) — kristal tuzilmasi.
"""
from pathlib import Path
import csv
import math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'sulfat'
ASSETS.mkdir(parents=True, exist_ok=True)

R_GAS = 8.314462          # J/(mol*K)
F_CONST = 96485.332       # C/mol

# --- molekul va termodinamika ----------------------------------------------
M_H2SO4 = 98.078         # g/mol (S 32,06 + O4 64,00 + H2 2,02)
M_SO3 = 80.06
M_SO2 = 64.06
M_H2O = 18.015
M_S = 32.06
M_O = 16.00
M_H = 1.008

DFH_GAS = -735.13         # kJ/mol, gaz fazi (NIST WebBook, Chase 1998)
S_GAS = 298.78           # J/(mol*K)
PA = 699.4               # kJ/mol, proton affinity (Hunter & Lias, 1998)
GB = 666.9               # kJ/mol, gaz bazikligi
DG_DEPROT = 1265.0       # kJ/mol, gaz fazida deprotonatsiya erkinligi
HO_HO = -12.0            # Hammett kislotalik funksiyasi (100 % H2SO4)

# --- geometriya (Kuchitsu va Sue, 1981; ab initio, 2007) -------------------
R_SO = 142.2             # pm, S=O (terminal)
R_SOH = 157.4            # pm, S-OH
R_OH = 97.0              # pm, O-H
ANG_OSO_X = 123.3        # grad, ∠O=S=O (terminal)
ANG_OSO_H = 101.3        # grad, ∠O=S-OH
ANG_HOS = 108.5          # grad, ∠H-O-S
TAU_HOSO = 89.1          # grad, dihedral H-O-S-O (gauche-gauche)
TAU_AB = -86.66          # grad, ab initio dihedral
R_SO_AB = 140.99         # pm, ab initio r(S=O)
R_SOH_AB = 157.51        # pm, ab initio r(S-OH)
R_SO4 = 147.2            # pm, SO4^2- o'rtacha S-O
POINT_GROUP = 'C₂'
CRYSTAL_A = 818.1        # pm, monoklin H2SO4
CRYSTAL_B = 469.60
CRYSTAL_C = 856.3
CRYSTAL_BETA = 111.39
CRYSTAL_Z = 4

# --- kislotalik ------------------------------------------------------------
KA1 = 1.0e3              # pKa1 ~ -3 (birinchi dissotsiatsiya to'liq)
KA2 = 1.2e-2             # pKa2 = 1,99
PKA1 = -3.0
PKA2 = 1.99
KW = 1e-14
PAULING_RATIO = 1.0e5    # ketma-ket dissotsiatsiya konstantalari nisbiy oraliq

# --- 100 % sulfat kislotadagi turlar (mmol/kg) ------------------------------
SPECIES_100 = [
    ('HSO₄⁻', 15.0), ('H₃SO₄⁺', 11.3), ('H₃O⁺', 8.0),
    ('HS₂O₇⁻', 4.4), ('H₂S₂O₇', 3.6), ('H₂O', 0.1),
]

# --- gidratlar (massada ulushi %) -------------------------------------------
HYDRATES = [
    ('Monogidrat (SAM)', 'H₂SO₄·H₂O', 1, 84.5, 'H₃O⁺HSO₄⁻', 8.5),
    ('Digidrat (SAD)', 'H₂SO₄·2H₂O', 2, 73.1, 'H₃O⁺HSO₄⁻·H₂O', -39.5),
    ('Trigidrat (SATri)', 'H₂SO₄·3H₂O', 3, 64.5, 'H₃O⁺HSO₄⁻·2H₂O', -26.0),
    ('Tetragidrat (SAT)', 'H₂SO₄·4H₂O', 4, 57.6, '[H₅O₂⁺]₂SO₄²⁻', -28.2),
    ('Yarimtriskaidekagidrat (SAH)', 'H₂SO₄·6,5H₂O', 6.5, 45.6, 'H₃O⁺ + SO₄²⁻·5,5H₂O', -54.0),
    ('Oktagidrat (SAO)', 'H₂SO₄·8H₂O', 8, 40.5, 'H₃O⁺ + SO₄²⁻·7H₂O', -3.4),
]

# --- spektr bandlari (cm^-1) -----------------------------------------------
SPECTRA = [
    ('H₂SO₄ (g)', 'O–H cho‘zilishi (antisimmetrik)', 3603, 'kuchli, IR'),
    ('H₂SO₄ (g)', 'S=O cho‘zilishi (simmetrik)', 1248, 'kuchli, IR'),
    ('H₂SO₄ (g)', 'S–OH cho‘zilishi', 792, 'kuchli, IR'),
    ('H₂SO₄ (g)', 'SO₃ «shlyapa» deformatsiyasi', 499, 'o‘rtacha, IR'),
    ('HSO₄⁻ (aq)', 'ν(SOH) cho‘zilishi', 1055, 'kuchli, Raman'),
    ('HSO₄⁻ (aq)', 'ν(SO₄) cho‘zilishi (yon)', 1030, 'yondan, Raman'),
    ('HSO₄⁻ (aq)', 'ν₃′ — ion juftligi', 900, 'o‘rtacha, Raman'),
    ('HSO₄⁻ (aq)', 'Deformatsiya', 617, 'kuchli, IR'),
    ('SO₄²⁻ (aq)', 'ν₁ — simmetrik cho‘zilish (A₁)', 981, 'eng kuchli, Raman'),
    ('SO₄²⁻ (aq)', 'ν₂ — simmetrik egilish (E)', 451, 'kuchli, Raman'),
    ('SO₄²⁻ (aq)', 'ν₃ — asimmetrik cho‘zilish (F₂)', 1104, 'kuchli, IR'),
    ('SO₄²⁻ (aq)', 'ν₄ — asimmetrik egilish (F₂)', 617, 'o‘rtacha, IR'),
    ('SO₄²⁻ (aq)', 'χ — «chekilish» (chopping)', 450, 'kuchli, IR'),
    ('H₃O⁺ (aq)', 'Asimmetrik cho‘zilish', 3428, 'kuchli, IR'),
]

# --- xavfsizlik chegaralari (mg/m3) ----------------------------------------
LIMITS = [
    ('OSHA PEL (8 soat TWA)', 1.0, '29 CFR 1910.1000'),
    ('NIOSH REL (10 soat TWA)', 1.0, 'Tavsiya etilgan chegar'),
    ('ACGIH TLV-TWA (torakal fraksiya)', 0.2, 'A2 — kuchli kislota tumani'),
    ('NIOSH IDLH', 15.0, 'Hayot uchun xavfli'),
    ('AIHA ERPG-1', 2.0, 'Bir soatlik reaktsiya chegarasi'),
    ('AIHA ERPG-2', 10.0, 'Bir soatlik reaktsiya chegarasi'),
    ('AIHA ERPG-3', 120.0, 'Hayot uchun xavfli'),
    ('Carcinogenlik', 0.0, 'IARC 1; kuchli va noorganik kislota tumanlari'),
]

# --- sanoat ----------------------------------------------------------------
WORLD_PRODUCTION = (260.0, 290.0)    # mln t/y
FERTILIZER_SHARE = (56.0, 60.0)      # % jami sarfdan
METALLURGY_SHARE = 30.0              # mln t
BATTERY_SHARE = 14.0                 # mln t
CONTACT_SHARE = 90.0                 # % (kontakt usuli)
CONV_99_7 = 99.7                    # % SO3 konversiyasi (DCDA)
SULFUR_TO_ACID = 85.0                # mln t/y oltingugurt
ACID_SHARE_SULFUR = 90.0             # % oltingugurt H2SO4 sifatida

# --- fizik (jami) ----------------------------------------------------------
T_M = 283.46              # K, 10,31 °C
T_B = 610.4               # K, 337 °C
RHO_LIQ = 1.8302          # g/cm3 (20 °C)
RHO_CONC = 1.84           # g/cm3 (96-98 %)
VISC_20 = 26.7            # cP
EPS = 100.0               # dielektrik doimiy (taxminiy)
P_VAP = 0.001             # mmHg (20 °C)
DH_VAP = 69.0             # kJ/mol ( kondensatsiya entalpisi)


def num(x, n=3):
    """Nuqta -> vergul, o'zbekcha format."""
    return ('%.*f' % (n, x)).replace('.', ',')


# --------------------------------------------------- kislotalik (taxminiy hisob)
def second_step(c, ka2=KA2):
    """Ikkinchi dissotsiatsiya: x = [SO4^2-] (taxminiy hisob).

    Birinchi dissotsiatsiya to'liq: h = c + x;  [HSO4-] = c - x;  [SO4^2-] = x.
    Ka2 = h*x/(c - x)  ->  x^2 + (c + Ka2)x - Ka2*c = 0.
    """
    b = c + ka2
    x = (-b + math.sqrt(b * b + 4.0 * ka2 * c)) / 2.0
    h = c + x
    return dict(c=c, x=x, h=h, ph=-math.log10(h),
                so4_pct=100.0 * x / c, hso4_pct=100.0 * (c - x) / c)


def dissolution_series(cs=(0.0010, 0.0020, 0.0050, 0.0100, 0.0200, 0.0500,
                           0.1000, 0.2000, 0.5000, 1.0000, 2.0000, 4.0000)):
    return [second_step(c) for c in cs]


def speciation_ph(ph):
    """pH bo'yicha HSO4-/SO4^2- ulushlari (taxminiy hisob, K_a1 to'liq)."""
    h = 10.0 ** (-ph)
    r = KA2 / h
    t = 1.0 + r
    return dict(ph=ph, hso4=100.0 / t, so4=100.0 * r / t)


# --------------------------------------------------- sufma kislota (taxminiy hisob)
def autoprotolysis():
    """100 % H2SO4 da avtoprotoliz doimiysi (taxminiy hisob).

    K_ap = [H3SO4+][HSO4-] (mol/kg)^2 — nashr etilgan turlar miqdoridan.
    """
    m_h3so4 = 11.3e-3
    m_hso4 = 15.0e-3
    c_total = 1000.0 / M_H2SO4          # mol/kg
    k_mol = m_h3so4 * m_hso4
    x_h3so4 = m_h3so4 / c_total
    x_hso4 = m_hso4 / c_total
    return dict(m_h3so4=m_h3so4, m_hso4=m_hso4, c_total=c_total,
                k_molal=k_mol, k_mole_fraction=x_h3so4 * x_hso4,
                x_h3so4=x_h3so4, x_hso4=x_hso4)


def acid_capacity():
    """Proton sig'imi (taxminiy hisob)."""
    c_100 = RHO_LIQ * 1000.0 / M_H2SO4     # mol/L (100 % kislota, 20 °C)
    c_1m = 1.0
    return dict(c_pure=c_100, h_per_l_pure=2.0 * c_100,
                c_1m=c_1m, h_per_l_1m=2.0 * c_1m,
                g_eq_per_l=2.0 * 98.08,
                f_per_mol=2.0 * F_CONST)


# --------------------------------------------------- gidratlar
def hydrate_composition():
    """Gidratlar massadagi ulushini molekulyar tarkibdan tekshirish (taxminiy hisob)."""
    out = []
    for name, formula, n, wt, structure, tm in HYDRATES:
        m = M_H2SO4 + n * M_H2O
        out.append(dict(name=name, formula=formula, n=n, m=m,
                        wt_calc=100.0 * M_H2SO4 / m, wt_tab=wt,
                        structure=structure, tm=tm,
                        n_h2o_per_s=n))
    return out


# --------------------------------------------------- kontakt usuli (taxminiy hisob)
def contact(m_acid=1000.0):
    """1 t H2SO4 uchun xom ashyo va reagentlar (taxminiy hisob)."""
    n = m_acid / M_H2SO4
    return dict(m_acid=m_acid, n=n,
                m_s=n * M_S, m_so2=n * M_SO2, m_so3=n * M_SO3,
                m_o2=0.5 * n * 2.0 * M_O, m_h2o=n * M_H2O,
                m_oleum=n * (M_H2SO4 + M_SO3) - n * M_H2SO4,
                balance=m_acid - n * M_H2SO4)


def oleum(free_so3=20.0, m_acid=1000.0):
    """Oleum (H2S2O7) tarkibi (taxminiy hisob)."""
    n_so3 = free_so3 / 100.0 * m_acid / M_H2SO4
    m_oleum = m_acid + n_so3 * M_SO3
    w_so3 = 100.0 * n_so3 * M_SO3 / m_oleum
    return dict(free_so3=free_so3, m_acid=m_acid, n_so3=n_so3,
                m_oleum=m_oleum, w_so3=w_so3,
                m_h2so4_final=m_oleum + n_so3 * M_H2O)


# --------------------------------------------------- ekvivalent
def equivalents():
    """Ekvivalent massa va proton zaxirasi (taxminiy hisob)."""
    return dict(h2so4=M_H2SO4 / 2.0, hso4=97.07, so4=96.06,
                n_protons=2, n_electrons=2,
                eq_per_kg=M_H2SO4 / 2.0,
                t_equivalent=1000.0 / (M_H2SO4 / 2.0))


def main():
    # 1) dissotsiatsiya: konsentratsiya -> pH va SO4^2- ulushi
    with open(ASSETS / 'dissotsiatsiya.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['c, mol/L', 'h, mol/L', 'pH', '[SO4^2-], mol/L', 'SO4^2-, %'])
        for r in dissolution_series():
            w.writerow([num(r['c'], 4), num(r['h'], 6), num(r['ph'], 3),
                        num(r['x'], 6), num(r['so4_pct'], 2)])

    # 2) kislotalik jadvali
    with open(ASSETS / 'kislotalik.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Reaksion / kislota', 'Qiymat', 'Izoh'])
        w.writerow(['H₂SO₄ → H⁺ + HSO₄⁻', 'K_a1 ≈ %s' % num(KA1, 0), 'pK_a1 ≈ %s; birinchi bosqich to‘liq' % num(PKA1, 0)])
        w.writerow(['HSO₄⁻ → H⁺ + SO₄²⁻', 'K_a2 = %s' % num(KA2, 3), 'pK_a2 = %s' % num(PKA2, 2)])
        w.writerow(['Paulining qoidasi', '≈ 10⁵', 'Ketma-ket bosqichlar orasidagi nisbiy farq'])
        w.writerow(['H₂SO₄ (g) deprotonatsiyasi', 'ΔrG° = %s kJ/mol' % num(DG_DEPROT, 0), 'NIST: 1265 ± 10 kJ/mol'])
        w.writerow(['H₂SO₄ proton affinity', '%s kJ/mol' % num(PA, 1), 'NIST (Hunter & Lias, 1998)'])
        w.writerow(['H₂SO₄ gaz bazikligi', '%s kJ/mol' % num(GB, 1), 'NIST'])
        w.writerow(['Hammett H₀ (100 % H₂SO₄)', '%s' % num(HO_HO, 0), 'Superkislotalik chegarasi'])
        w.writerow(['ΔfH°(g)', '%s kJ/mol' % num(DFH_GAS, 2), 'NIST-JANAF (Chase, 1998)'])
        w.writerow(['S°(g)', '%s J/(mol·K)' % num(S_GAS, 2), 'NIST-JANAF (Chase, 1998)'])

    # 3) geometriya
    with open(ASSETS / 'geometriya.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Parametr', 'Qiymat', 'Manba / izoh'])
        w.writerow(['Nuqta guruhi', POINT_GROUP, 'gauche-gauche konformatsiya; C₂ o‘qi oltingugurt atomidan o‘tadi'])
        w.writerow(['r(S=O)', '%s pm' % num(R_SO, 1), 'Kuchitsu va Sue, 1981 (NIST-JANAF)'])
        w.writerow(['r(S–OH)', '%s pm' % num(R_SOH, 1), 'Kuchitsu va Sue, 1981'])
        w.writerow(['r(O–H)', '%s pm' % num(R_OH, 1), 'Kuchitsu va Sue, 1981'])
        w.writerow(['∠O=S=O', '%s°' % num(ANG_OSO_X, 1), 'Terminal kislorodlar orasida'])
        w.writerow(['∠O=S–OH', '%s°' % num(ANG_OSO_H, 1), 'Gidroksil guruhi bilan burchak'])
        w.writerow(['∠H–O–S', '%s°' % num(ANG_HOS, 1), 'O–H bog‘i egilishi'])
        w.writerow(['τ(H–O–S–O)', '%s°' % num(TAU_HOSO, 1), 'Dihedral burchak (gauche-gauche)'])
        w.writerow(['r(S=O), ab initio', '%s pm' % num(R_SO_AB, 2), 'Muvozanat tuzilmasi (2007)'])
        w.writerow(['r(S–OH), ab initio', '%s pm' % num(R_SOH_AB, 2), 'Muvozanat tuzilmasi (2007)'])
        w.writerow(['τ, ab initio', '%s°' % num(TAU_AB, 2), 'Muvozanat tuzilmasi (2007)'])
        w.writerow(['SO₄²⁻ o‘rtacha r(S–O)', '%s pm' % num(R_SO4, 1), 'T_d simmetriya; to‘rtala bog‘ teng'])
        w.writerow(['Kristal', 'monoklin, C2/c', 'Z = %s; a = %s, b = %s, c = %s pm; β = %s°' %
                    (num(CRYSTAL_Z, 0), num(CRYSTAL_A, 1), num(CRYSTAL_B, 2),
                     num(CRYSTAL_C, 1), num(CRYSTAL_BETA, 2))])

    # 4) spektr bandlari
    with open(ASSETS / 'spektra.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Spekies', 'Tayinlash', 'ν, cm⁻¹', 'Kuchli/intensitet'])
        for sp, name, nu, kind in SPECTRA:
            w.writerow([sp, name, num(nu, 0), kind])

    # 5) gidratlar
    with open(ASSETS / 'gidratlar.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Gidrat', 'Formula', 'M, g/mol', 'H₂SO₄, % (hisob)',
                    'H₂SO₄, % (jadval)', 'Tuzilma', 'T_erish, °C'])
        for r in hydrate_composition():
            w.writerow([r['name'], r['formula'], num(r['m'], 2),
                        num(r['wt_calc'], 2), num(r['wt_tab'], 1),
                        r['structure'], num(r['tm'], 1)])

    # 6) 100 % kislotadagi turlar
    with open(ASSETS / 'sufma.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Tur', 'Miqdor, mmol/kg', 'X, mol ulushi'])
        ap = autoprotolysis()
        c_total = ap['c_total']
        for name, mmol in SPECIES_100:
            w.writerow([name, num(mmol, 1), num(mmol * 1e-3 / c_total, 6)])
        w.writerow(['K_ap (molal, taxminiy hisob)', num(ap['k_molal'], 8), 'mol/kg²'])
        w.writerow(['K_ap (mole ulushi, taxminiy hisob)', num(ap['k_mole_fraction'], 9), '—'])

    # 7) kristal va fazalar
    with open(ASSETS / 'kristal.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Parametr', 'Qiymat', 'Izoh'])
        w.writerow(['Kristal tizimi', 'monoklin', 'C2/c fazoviy guruhi'])
        w.writerow(['a', '%s pm' % num(CRYSTAL_A, 1), '—'])
        w.writerow(['b', '%s pm' % num(CRYSTAL_B, 2), '—'])
        w.writerow(['c', '%s pm' % num(CRYSTAL_C, 1), '—'])
        w.writerow(['β', '%s°' % num(CRYSTAL_BETA, 2), '—'])
        w.writerow(['Z', num(CRYSTAL_Z, 0), 'Formula birliklari soni'])
        w.writerow(['V_hujra (taxminiy hisob)', '%s pm³' % num(CRYSTAL_A * CRYSTAL_B * CRYSTAL_C * math.sin(math.radians(CRYSTAL_BETA)) / 1000.0, 1), 'abc·sinβ'])
        w.writerow(['T_erish (H₂SO₄)', '%s °C' % num(T_M - 273.15, 2), 'Molekulyar qattiq'])
        w.writerow(['T_qaynash', '%s °C' % num(T_B - 273.15, 0), 'SO₃ ajralishi bilan'])
        w.writerow(['ρ (suyuq, 20 °C)', '%s g/cm³' % num(RHO_LIQ, 4), '—'])
        w.writerow(['Viskozitet (20 °C)', '%s cP' % num(VISC_20, 1), '—'])

    # 8) xavfsizlik
    with open(ASSETS / 'xavfsizlik.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Chegara', 'Qiymat, mg/m³', 'Izoh'])
        for name, value, note in LIMITS:
            w.writerow([name, num(value, 2), note])

    # 9) sanoat
    with open(ASSETS / 'sanoat.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Ko‘rsatkich', 'Qiymat', 'Manba / izoh'])
        w.writerow(['Dunyoda ishlab chiqarish', '%s-%s mln t/y' % (num(WORLD_PRODUCTION[0], 0), num(WORLD_PRODUCTION[1], 0)), 'USGS / bozor ma\'lumotlari'])
        w.writerow(['Kontakt usuli ulushi', '~ %s %%' % num(CONTACT_SHARE, 0), 'Dunyodagi eng katta sintetik kislota'])
        w.writerow(['Fosfat o‘g‘itlari', '%s-%s %%' % (num(FERTILIZER_SHARE[0], 0), num(FERTILIZER_SHARE[1], 0)), 'Fosfor kislotasi ishlab chiqarish'])
        w.writerow(['Metallurgiya', '%s mln t' % num(METALLURGY_SHARE, 0), 'Rudani yig‘ish (leaching)'])
        w.writerow(['Akkumulatorlar', '%s mln t' % num(BATTERY_SHARE, 0), 'Qo‘rg‘o‘l-akkumulatorlar'])
        w.writerow(['SO₃ konversiyasi (DCDA)', '%s %%' % num(CONV_99_7, 1), 'Ikki pog‘onali kontakt usuli'])
        w.writerow(['Oltingugurt ishlab chiqarish', '%s mln t/y' % num(SULFUR_TO_ACID, 0), 'Neft qayta ishlash va gazni tozalash'])
        w.writerow(['H₂SO₄ sifatida sarflangan oltingugurt', '~ %s %%' % num(ACID_SHARE_SULFUR, 0), 'Qolgani kislot sifatida emas'])
        w.writerow(['Vulkan SO₂ → stratosferadagi H₂SO₄', 'tropopozada', 'Aerol izotog‘i manbai'])

    # 10) ekvivalent
    with open(ASSETS / 'ekvivalent.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Shakl', 'M, g/mol', 'Proton/elektron', 'Ekvivalent, g/eq'])
        eq = equivalents()
        w.writerow(['H₂SO₄ (kislota)', num(M_H2SO4, 3), 2, num(eq['h2so4'], 3)])
        w.writerow(['HSO₄⁻ (kislota)', '97,070', 1, '97,070'])
        w.writerow(['SO₄²⁻ (tuz)', '96,060', 0, '—'])
        ac = acid_capacity()
        w.writerow(['1 L 1 M H₂SO₄', num(M_H2SO4, 3), 2, num(ac['g_eq_per_l'], 2) + ' g/eq/L'])
        w.writerow(['1 mol H₂SO₄', num(M_H2SO4, 3), 2, num(ac['f_per_mol'] / 2.0, 1) + ' C/mol'])

    print('10 CSV yozildi:', ASSETS)


if __name__ == '__main__':
    main()
