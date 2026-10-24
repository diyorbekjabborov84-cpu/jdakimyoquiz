#!/usr/bin/env python3
"""6.6 "Taqqoslash" — vodorod galogenid kislotalarini qiyoslash.

Barcha sonli natijalar ochiq shartli hisoblar (o'lchov ma'lumoti emas).
Manbalar: kitobning 6.1-bo'lim guruh jadvali (prep_06_01.py), Ksp jadvallari
(UMass/URI/Wikipedia: BaF2 1,7e-6; CaF2 3,9e-11; PbF2 3,7e-8; AgCl 1,8e-10;
AgBr 5,4e-13; AgI 8,3e-17; AgF eruvchanligi ~1,8 kg/L), E°(X2/2X-) standart
qiymatlari (F2 2,87 V; Cl2 1,36 V; Br2 1,07 V; I2 0,54 V).
"""
from pathlib import Path
import csv, math

from prep_06_01 import (ACIDS, BY_KEY, RT, gas_to_ion, thermal_decomposition,
                        net_bond, oxidising_balance, hf_equilibrium)

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'taqqoslash'
ASSETS.mkdir(parents=True, exist_ok=True)

KEYS = ['HF', 'HCl', 'HBr', 'HI']
SALT_ANION = {'HF': 'F', 'HCl': 'Cl', 'HBr': 'Br', 'HI': 'I'}
ORDER = ['HF', 'HCl', 'HBr', 'HI']

# --- qo'shimcha massalar ----------------------------------------------------
M_NA2CO3 = 105.99
M_CO2 = 44.009
M_H2O = 18.015
M_CACO3 = 100.09
M_CAF2 = 78.074
M_FE = 55.845
M_H2 = 2.016
M_F2 = 37.996
M_CL2 = 70.906
M_BR2 = 159.808
M_I2 = 253.809
M_AG = 107.868
M_PB = 207.2

# --- eruvchanlik (Ksp, 25 °C) va qo'shimcha ---------------------------------
# (tuz, formulа, Ksp, izoh)
SOLUBILITY = [
    ('AgF', 'AgF', None, 'Yaxshi eriydi: ≈1,8 kg/L (20 °C); Ksp ko‘pincha keltirilmaydi'),
    ('AgCl', 'AgCl', 1.8e-10, 'Oq cho‘kma; klassik halogenid taqqoslash nuqtasi'),
    ('AgBr', 'AgBr', 5.4e-13, 'Och sariq cho‘kma'),
    ('AgI', 'AgI', 8.3e-17, 'Sariq cho‘kma — eng oz eriydi'),
    ('PbF₂', 'PbF₂', 3.7e-8, 'Oq; eruvchanligi 0,067 g/100 mL (20 °C)'),
    ('PbCl₂', 'PbCl₂', 1.6e-5, 'Oq; qaynoq suvda yaxshi eriydi'),
    ('PbBr₂', 'PbBr₂', 4.6e-6, 'Oq'),
    ('PbI₂', 'PbI₂', 7.9e-9, 'Sariq'),
    ('BaF₂', 'BaF₂', 1.7e-6, 'Oq; eruvchanligi 1,61 g/L (25 °C)'),
    ('CaF₂', 'CaF₂', 3.9e-11, 'Oq; deyarli erimaydi — HF ni neytralizatsiyada cho‘kma qiladi'),
]

# --- standart redoks potensiali (V), 25 °C, SHE ga nisbatan ------------------
E_REDUX = {'HF': 2.87, 'HCl': 1.36, 'HBr': 1.07, 'HI': 0.54}

M_X2 = {'HF': M_F2, 'HCl': M_CL2, 'HBr': M_BR2, 'HI': M_I2}


# ---------------------------------------------------------------- pH hisoblari
def ph_series(key, cs=(0.001, 0.010, 0.050, 0.100, 0.500, 1.000, 2.000)):
    """0,1 M dan boshqa konsentratsiyalarda pH (ideal erituvchi sharoiti).

    HF uchun to‘liq kvadrat yechim; HCl/HBr/HI uchun to‘liq dissotsiatsiya.
    """
    a = BY_KEY[key]
    out = []
    for c in cs:
        if key == 'HF':
            x = (-a['ka'] + math.sqrt(a['ka'] ** 2 + 4 * a['ka'] * c)) / 2.0
            out.append(dict(c=c, h=x, pct=100.0 * x / c, ph=-math.log10(x),
                            full=False))
        else:
            out.append(dict(c=c, h=c, pct=100.0, ph=-math.log10(c), full=True))
    return out


def ph_at(key, c):
    return ph_series(key, (c,))[0]


# ---------------------------------------------------------------- metall bilan
def metal_demand(m_metal=1.0, metal='Fe'):
    """1 g metallni eritish uchun har bir kislotaning mass talabi.

    M + 2HX -> MX2 + H2  (taxminiy hisob, to‘liq dissotsiatsiya va to‘liq reaksiya).
    """
    m_m = M_FE if metal == 'Fe' else 55.845
    n_metal = m_metal / m_m
    out = []
    for key in KEYS:
        a = BY_KEY[key]
        n_hx = 2.0 * n_metal
        m_hx = n_hx * a['m']
        m_salt = n_metal * (m_m + 2.0 * a['mx'])
        out.append(dict(key=key, metal=metal, m_metal=m_metal, n_metal=n_metal,
                        m_acid=m_hx, m_acid_kg=m_hx / 1000.0,
                        m_salt=m_salt, m_h2=n_metal * M_H2,
                        salt='Fe' + SALT_ANION[key] + '₂'))
    return out


# ---------------------------------------------------------------- halogen ajratish
def halogen_from_acid(m_acid=1000.0):
    """1000 kg kislotadan ajratiladigan X2 massasi (shartli hisob).

    F- oksidlanmaydi: HF dan F2 olish mumkin emas.
    """
    out = []
    for key in KEYS:
        a = BY_KEY[key]
        n_acid = m_acid / a['m']
        if key == 'HF':
            out.append(dict(key=key, m_acid=m_acid, n_acid=n_acid, m_x2=0.0,
                            possible=False,
                            note='F⁻ oksidlanmaydi — HF dan F₂ olish mumkin emas'))
        else:
            m_x2 = 0.5 * n_acid * M_X2[key]
            out.append(dict(key=key, m_acid=m_acid, n_acid=n_acid, m_x2=m_x2,
                            possible=True,
                            note='Kislota qaytaruvchi: X₂ ajratiladi'))
    return out


def oxygen_oxidation(m_acid=1000.0):
    """Havodagi kislorod bilan oksidlanish: 4HX + O2 -> 2X2 + 2H2O."""
    out = []
    for key in KEYS:
        a = BY_KEY[key]
        n_acid = m_acid / a['m']
        if key == 'HF':
            out.append(dict(key=key, m_acid=m_acid, m_x2=0.0, m_o2=0.0,
                            possible=False, note='F⁻ oksidlanmaydi'))
        else:
            m_x2 = 0.5 * n_acid * M_X2[key]
            m_o2 = 0.25 * n_acid * 31.998
            out.append(dict(key=key, m_acid=m_acid, m_x2=m_x2, m_o2=m_o2,
                            possible=(key == 'HI'),
                            note=('Havodan o‘zi oksidlanadi' if key == 'HI'
                                  else 'Kuchli oksidlovchi talab qiladi')))
    return out


# ---------------------------------------------------------------- neytralizatsiya
def neutralisation_demand(m_solution=1000.0, pct=10.0):
    """1000 kg 10 % li eritmada neytrallash uchun Na2CO3 va Ca(OH)2 talabi."""
    out = []
    for key in KEYS:
        a = BY_KEY[key]
        m_acid = m_solution * pct / 100.0
        n_acid = m_acid / a['m']
        n_co3 = n_acid / 2.0
        m_co3 = n_co3 * M_NA2CO3
        m_co2 = n_co3 * M_CO2
        m_h2o = n_co3 * M_H2O
        m_caoh2 = n_co3 * 74.093
        m_caco3 = n_co3 * M_CACO3
        m_salt = n_acid * (22.9898 + a['mx'])            # NaX
        if key == 'HF':
            m_ca_salt = n_co3 * M_CAF2                  # CaF2 — cho‘kma
        else:
            m_ca_salt = n_co3 * (40.078 + 2 * a['mx'])  # CaX2 — eruvchan
        out.append(dict(key=key, m_solution=m_solution, pct=pct,
                        m_acid=m_acid, n_acid=n_acid,
                        m_naco3=m_co3, m_co2=m_co2, m_h2o=m_h2o,
                        m_caoh2=m_caoh2, m_caco3=m_caco3, m_ca_salt=m_ca_salt,
                        m_salt=m_salt,
                        m_input=m_acid + m_co3,
                        m_output=m_salt + m_co2 + m_h2o,
                        precipitate=(key == 'HF')))
    return out


def acid_equivalents(m_acid=1000.0):
    """1 kg kislotadagi proton ekvivalenti (mol H+ / kg) — to‘liq dissotsiatsiya chegarasi."""
    out = []
    for key in KEYS:
        a = BY_KEY[key]
        n_acid = m_acid / a['m']
        out.append(dict(key=key, m_acid=m_acid, n_acid=n_acid,
                        eq_per_kg=n_acid * 1000.0 / m_acid,
                        eq_per_t=n_acid * 1000.0,
                        m_equivalent=m_acid / n_acid))
    return out


# ---------------------------------------------------------------- tuzlar
def salt_rows():
    out = []
    for name, formula, ksp, note in SOLUBILITY:
        out.append(dict(name=name, formula=formula, ksp=ksp, note=note,
                        lg=(math.log10(ksp) if ksp else None)))
    return out


def complex_stability():
    """X- ning kompleks hosil qilish qobiliyati (taxminiy reyting, 0–5)."""
    return [dict(key='HF', value=1, comment='F⁻ kuchli, qat’iy elektron juftligi'),
            dict(key='HCl', value=2, comment='Cl⁻ o‘rtacha; [CuCl₄]²⁻, [PtCl₆]²⁻'),
            dict(key='HBr', value=3, comment='Br⁻ yaxshi ligand; [AgBr₂]⁻'),
            dict(key='HI', value=5, comment='I⁻ eng kuchli; [HgI₄]²⁻, [BiI₄]⁻')]


# ---------------------------------------------------------------- termik barqarorlik
def thermal_rows():
    out = []
    for key in KEYS:
        a = BY_KEY[key]
        t = thermal_decomposition(key)
        g = gas_to_ion(key)
        out.append(dict(key=key, d=a['d'], dfh=a['dfh'], dfg=a['dfg'], s=a['s_g'],
                        dg_dec=t['dg'], lgk_dec=t['log10k'],
                        dg_ion=g['dg'], lgk_ion=g['log10k'],
                        net=net_bond(key), redox=oxidising_balance(key),
                        e=E_REDUX[key]))
    return out


# ---------------------------------------------------------------- CSV yozuvchi
def write(name, header, data):
    with (ASSETS / (name + '.csv')).open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


def build_csvs():
    rows = []
    for key in KEYS:
        a = BY_KEY[key]
        g = gas_to_ion(key)
        rows.append([key, a['pka'], a['pka_dmso'], a['ka'], 10.0 ** (-a['pka_dmso']),
                     g['dg'], g['log10k'], net_bond(key)])
    write('kislotalik', ['acid', 'pKa_suv', 'pKa_DMSO', 'Ka_suv', 'Ka_DMSO',
                         'dG_gaz_ion_kJ', 'lgK_gaz_ion', 'D_plus_hyd'], rows)

    rows = []
    for key in KEYS:
        a = BY_KEY[key]
        rows.append([key, a['m'], a['mx'], a['chi'], a['rexp'], a['rcov'] + a['rcov_h'],
                     a['d'], a['mu'], a['tm'], a['tb'], a['azeo'], a['azeo_t'], a['rho'],
                     (a['azeo'] / 100.0) * a['rho'] / (a['m'] / 1000.0)])
    write('fizik', ['acid', 'M_HX', 'M_X', 'chi_Pauling', 'r_exp_A', 'r_cov_sum_A',
                    'D_HX_kJ', 'mu_D', 'Tm_C', 'Tb_C', 'azeo_pct', 'azeo_T_C',
                    'rho_g_ml', 'c_azeo_mol_l'], rows)

    rows = []
    for s in salt_rows():
        rows.append([s['name'], s['formula'], s['ksp'] if s['ksp'] else '',
                     ('%.2f' % s['lg']) if s['lg'] is not None else '', s['note']])
    write('eruvchanlik', ['tuz', 'formula', 'Ksp', 'lgKsp', 'izoh'], rows)

    rows = []
    for key in KEYS:
        for p in ph_series(key):
            rows.append([key, p['c'], p['h'], p['pct'], p['ph'],
                         'to‘liq' if p['full'] else 'kvadrat yechim'])
    write('ph', ['acid', 'c_M', 'h_M', 'dissotsiatsiya_pct', 'pH', 'usul'], rows)

    rows = []
    for md in metal_demand(1.0):
        rows.append([md['key'], md['m_metal'], md['salt'], md['m_acid'],
                     md['m_acid_kg'], md['m_salt'], md['m_h2']])
    write('metal', ['acid', 'm_metal_g', 'tuz', 'm_kislota_g', 'm_kislota_kg',
                    'm_tuz_g', 'm_H2_g'], rows)

    rows = []
    for h in halogen_from_acid(1000.0):
        rows.append([h['key'], h['m_acid'], h['m_x2'], 'ha' if h['possible'] else 'yo‘q',
                     h['note']])
    write('galogen', ['acid', 'm_kislota_kg', 'm_X2_kg', 'ajratish', 'izoh'], rows)

    rows = []
    for n in neutralisation_demand(1000.0, 10.0):
        rows.append([n['key'], n['m_acid'], n['m_naco3'], n['m_co2'], n['m_h2o'],
                     n['m_caoh2'], n['m_ca_salt'], n['m_input'], n['m_output'],
                     'CaF₂ cho‘kma' if n['precipitate'] else 'eruvchan tuz'])
    write('neytralizatsiya', ['acid', 'm_kislota_kg', 'm_Na2CO3_kg', 'm_CO2_kg',
                              'm_H2O_kg', 'm_CaOH2_kg', 'm_CaF2_kg',
                              'kirish_kg', 'chiqish_kg', 'tuz'], rows)

    rows = []
    for e in acid_equivalents(1000.0):
        rows.append([e['key'], e['m_acid'], e['n_acid'], e['eq_per_kg'],
                     e['eq_per_t'], e['m_equivalent']])
    write('ekvivalent', ['acid', 'm_kislota_kg', 'n_kislota_kmol', 'mol_H_per_kg',
                         'mol_H_per_t', 'ekvivalent_massa_g'], rows)

    rows = []
    for t in thermal_rows():
        rows.append([t['key'], t['d'], t['dfh'], t['dfg'], t['s'], t['dg_dec'],
                     t['lgk_dec'], t['e'], t['redox'], t['net']])
    write('termik', ['acid', 'D_HX', 'dfH_gas', 'dfG_gas', 'S_gas', 'dG_dekomp',
                     'lgK_dekomp', 'E_redox_V', 'oks_balans', 'D_plus_hyd'], rows)
    return 8


def main():
    build_csvs()
    print('— kislotalik (suv / DMSO / gaz fazi) —')
    for key in KEYS:
        a = BY_KEY[key]
        g = gas_to_ion(key)
        print('  %-4s pKa(suv)=%6.2f  pKa(DMSO)=%6.2f  lgK(gaz)=%12.2f  D+h=%7.1f'
              % (key, a['pka'], a['pka_dmso'], g['log10k'], net_bond(key)))
    print('— pH (ideal erituvchi) —')
    for key in KEYS:
        for c in (0.010, 0.100, 1.000):
            p = ph_at(key, c)
            print('  %-4s c=%5.3f M  h=%9.6f  diss=%6.2f %%  pH=%7.3f'
                  % (key, c, p['h'], p['pct'], p['ph']))
    print('— metall talabi (1 g Fe) —')
    for md in metal_demand(1.0):
        print('  %-4s -> %-6s kislota %9.3f g;  tuz %9.3f g;  H2 %6.3f g'
              % (md['key'], md['salt'], md['m_acid'], md['m_salt'], md['m_h2']))
    print('— halogen ajratish (1000 kg kislota) —')
    for h in halogen_from_acid(1000.0):
        print('  %-4s X2 = %8.1f kg  (%s)' % (h['key'], h['m_x2'], h['note']))
    print('— neytralizatsiya (1000 kg 10 % li eritma) —')
    for n in neutralisation_demand(1000.0, 10.0):
        print('  %-4s Na2CO3 %7.1f kg; CO2 %6.1f; H2O %5.1f; Ca(OH)2 %6.1f; CaX2 %6.1f (kirish %7.1f = chiqish %7.1f)'
              % (n['key'], n['m_naco3'], n['m_co2'], n['m_h2o'], n['m_caoh2'],
                 n['m_ca_salt'], n['m_input'], n['m_output']))
    print('— ekvivalent (1 kg kislota) —')
    for e in acid_equivalents(1000.0):
        print('  %-4s n = %8.3f kmol;  H+ ekv. %6.3f mol/kg;  ekvivalent massa %7.3f g/mol'
              % (e['key'], e['n_acid'], e['eq_per_kg'], e['m_equivalent']))
    print('— termik —')
    for t in thermal_rows():
        print('  %-4s dG(dekomp)=%9.2f kJ;  lgK=%10.2f;  E°=%5.2f V;  oks balans=%8.1f'
              % (t['key'], t['dg_dec'], t['lgk_dec'], t['e'], t['redox']))
    print('CSV:', ', '.join(sorted(p.name for p in ASSETS.glob('*.csv'))))


if __name__ == '__main__':
    main()
