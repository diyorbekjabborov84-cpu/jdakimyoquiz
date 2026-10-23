#!/usr/bin/env python3
"""6.2 "HF — ftorid kislota" — model ma'lumotlari va CSV jadvallar.

Barcha sonli natijalar ochiq shartli model hisoblari (o'lchov ma'lumoti emas).
Manbalar: Housecroft (Liquid HF, self-ionization), Barron's (Compounds of Fluorine),
Kim et al. 2024 (SiO2 etch rate law), WHO/EPA (fluoride limits), NIST/CRC.
"""
from pathlib import Path
import csv, math

ASSETS = Path(__file__).resolve().parents[1] / 'rasmlar' / 'hf'
ASSETS.mkdir(parents=True, exist_ok=True)

M_HF = 20.006
KA_HF = 6.8e-4          # HF ⇌ H+ + F-   (suvda, 25 °C)
LOG_KF = 0.7            # HF + F- ⇌ HF2-  (hosillanish doimiysi, lgK)
KF = 10 ** LOG_KF       # M^-1
KSP_CAF2 = 3.9e-11      # CaF2 eruvchanligi ko'paytmasi
F_MASS = 18.998
M_CA = 40.078
M_CAOH2 = 74.093
M_CAF2 = 78.074
M_CAGLU = 448.39        # kalsiy glyukonat (C12H22CaO12)
M_CACL2 = 110.98
M_H2O = 18.015

# Anhidr HF fizik konstantalari (nashr ma'lumotlari)
AHF = dict(tb=19.5, tm=-83.6, eps_273=84.0, eps_200=175.0, k_self_273=2.0e-12,
           liq_lo=190.0, liq_hi=292.5, cond=1.4e-5, mu=1.9, dHvap=30.7,
           rho=0.99, visc=0.26, surface_tension=10.0, h0=-15.1, h0_sbF5=-21.0)

# SiO2 yemirish tezligi modeli: r (Angstrom/min) = 510[F-] + 610[HF] + 2890[HF2-]
ETCH_K = dict(f=510.0, hf=610.0, hf2=2890.0)

METALS = [
    dict(name='Al', m=26.9815, salt='AlF₃', m_salt=83.992, n_salt=1.0, h2=1.5),
    dict(name='Fe', m=55.845, salt='FeF₃', m_salt=129.901, n_salt=1.0, h2=1.5),
    dict(name='Ni', m=58.6934, salt='NiF₂', m_salt=96.693, n_salt=1.0, h2=0.5),
    dict(name='Cu', m=63.546, salt='CuF₂', m_salt=101.543, n_salt=1.0, h2=0.5),
]


# ---------------------------------------------------------------- spetsiatsiya
def speciation(c, ka=KA_HF, kf=KF):
    """Suvli HF: [H+], [F-], [HF], [HF2-] — ideal erituvchi modeli.

    Ka = h*f/[HF];  HF + F- ⇌ HF2- (Kf);  zaryad balansi h = f + [HF2-].
    """
    def f_of_h(h):
        a = kf * h / ka
        return (-1.0 + math.sqrt(1.0 + 4.0 * a * h)) / (2.0 * a)

    def total(h):
        f = f_of_h(h)
        hf = h * f / ka
        hf2 = kf * hf * f
        return hf + f + 2.0 * hf2, f, hf, hf2

    lo, hi = 1e-12, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if total(mid)[0] < c:
            lo = mid
        else:
            hi = mid
    h = (lo + hi) / 2.0
    c_tot, f, hf, hf2 = total(h)
    return dict(c=c, h=h, f=f, hf=hf, hf2=hf2,
                ph=-math.log10(h),
                w_hf=100 * hf / c_tot, w_f=100 * f / c_tot, w_hf2=100 * hf2 / c_tot)


def speciation_series(cs=(0.01, 0.05, 0.10, 0.50, 1.0, 2.0, 5.0, 10.0)):
    return [speciation(c) for c in cs]


def etch_rate(c, spec=None):
    """SiO2 yemirish tezligi modeli (Angstrom/min)."""
    s = spec or speciation(c)
    r_f = ETCH_K['f'] * s['f']
    r_hf = ETCH_K['hf'] * s['hf']
    r_hf2 = ETCH_K['hf2'] * s['hf2']
    return dict(c=c, f=s['f'], hf=s['hf'], hf2=s['hf2'],
                r_f=r_f, r_hf=r_hf, r_hf2=r_hf2, r=r_f + r_hf + r_hf2,
                r_nm_per_min=(r_f + r_hf + r_hf2) / 100.0)


def passivation(metal=1.0):
    """Metal -> fluorid: 1 g metall qancha fluorid hosil qiladi (model)."""
    out = []
    for mt in METALS:
        n_metal = metal / mt['m']
        n_salt = n_metal * mt['n_salt']
        m_salt = n_salt * mt['m_salt']
        n_hf = 2 * mt['n_salt'] * n_metal
        out.append(dict(metal=mt['name'], m_metal=metal, n_metal=n_metal,
                        salt=mt['salt'], m_salt=m_salt, ratio=m_salt / metal,
                        n_hf=n_hf, m_hf=n_hf * M_HF,
                        n_h2=mt['h2'] * n_metal, m_h2=mt['h2'] * n_metal * 2.016))
    return out


def waste_model(m_solution=1000.0, pct=10.0):
    """2HF + Ca(OH)2 -> CaF2 + 2H2O: chiqindi boshqaruv mass balansi."""
    m_hf = m_solution * pct / 100.0
    n_hf = m_hf * 1000.0 / M_HF
    n_cao = n_hf / 2.0
    return dict(m_solution=m_solution, pct=pct, m_hf=m_hf, n_hf=n_hf,
                m_caoh2=n_cao * M_CAOH2 / 1000.0, m_caf2=n_cao * M_CAF2 / 1000.0,
                m_h2o=n_hf * M_H2O / 1000.0,
                m_input=m_hf + n_cao * M_CAOH2 / 1000.0,
                m_output=n_cao * M_CAF2 / 1000.0 + n_hf * M_H2O / 1000.0)


def residual_fluoride(ca_free=0.010):
    """CaF2 cho'kmani muvozanatidagi qoldiq F- (mg/L) — Ksp asosida."""
    f = math.sqrt(KSP_CAF2 / ca_free)
    return dict(ca=ca_free, f_mol=f, f_mg=f * F_MASS * 1000.0)


def calcium_requirement(m_hf=20.0):
    """Kaltsiy bog'lash stoxiometriyasi (xavfsizlik modeli)."""
    n_hf = m_hf / M_HF
    n_ca = n_hf / 2.0
    return dict(m_hf=m_hf, n_hf=n_hf, n_ca=n_ca,
                m_ca=n_ca * M_CA, m_caglu=n_ca * M_CAGLU, m_cacl2=n_ca * M_CACL2,
                m_caf2=n_ca * M_CAF2)


def production_model(m_fluorspar=1000.0, purity=0.97, yield_pct=0.92):
    """CaF2 + H2SO4 -> 2HF + CaSO4: HF miqdori (model)."""
    m_f2 = m_fluorspar * purity
    n_f2 = m_f2 * 1000.0 / 78.074
    return dict(m_fluorspar=m_fluorspar, purity=purity, yield_pct=yield_pct,
                n_f2=n_f2, m_hf=2 * n_f2 * M_HF / 1000.0 * yield_pct,
                m_h2so4=n_f2 * 98.079 / 1000.0, m_caso4=n_f2 * 136.141 / 1000.0,
                m_hf_pure=2 * n_f2 * M_HF / 1000.0)


def glass_model(m_sio2=1.0, hf_pct=48.0):
    """SiO2 + 6HF -> H2SiF6 + 2H2O (model)."""
    n_sio2 = m_sio2 * 1000.0 / 60.084
    n_hf = 6 * n_sio2
    return dict(m_sio2=m_sio2, n_sio2=n_sio2, n_hf=n_hf,
                m_hf=n_hf * M_HF, m_solution=n_hf * M_HF / (hf_pct / 100.0),
                m_h2siof6=n_sio2 * 144.092, m_h2o=2 * n_sio2 * M_H2O)


# ---------------------------------------------------------------- CSV yozuvchi
def write(name, header, data):
    with (ASSETS / (name + '.csv')).open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


def build_csvs():
    rows = []
    for s in speciation_series():
        rows.append([s['c'], s['h'], s['f'], s['hf'], s['hf2'], s['ph'],
                     s['w_hf'], s['w_f'], s['w_hf2']])
    write('spetsiatsiya',
          ['c_HF', 'h_H3O', 'f_F', 'hf', 'hf2', 'pH', 'w_hf_pct', 'w_f_pct', 'w_hf2_pct'], rows)

    rows = []
    for c in (0.05, 0.10, 0.25, 0.50, 1.0, 2.0, 4.0, 8.0):
        e = etch_rate(c)
        rows.append([e['c'], e['f'], e['hf'], e['hf2'], e['r_f'], e['r_hf'],
                     e['r_hf2'], e['r'], e['r_nm_per_min']])
    write('yemirish',
          ['c_HF', 'f_F', 'hf', 'hf2', 'r_F', 'r_HF', 'r_HF2', 'r_total', 'r_nm_min'], rows)

    rows = []
    for p in passivation(1.0):
        rows.append([p['metal'], p['m_metal'], p['salt'], p['m_salt'], p['ratio'],
                     p['m_hf'], p['m_h2']])
    write('passivatsiya',
          ['metal', 'm_metal_g', 'salt', 'm_salt_g', 'ratio_g_g', 'm_HF_g', 'm_H2_g'], rows)

    w = waste_model(1000.0, 10.0)
    rows = [['HF', w['m_hf'], 'kislota'],
            ['Ca(OH)₂', w['m_caoh2'], 'neytralizator'],
            ['CaF₂', w['m_caf2'], 'cho‘kma'],
            ['H₂O', w['m_h2o'], 'hosil bo‘ladi'],
            ['kirish', w['m_input'], 'kg'],
            ['chiqish', w['m_output'], 'kg']]
    for ca in (0.001, 0.005, 0.010, 0.050, 0.100):
        r = residual_fluoride(ca)
        rows.append(['F⁻ qoldig‘i', r['f_mg'], 'mg/L (Ca²⁺ = %.3f M)' % ca])
    write('chiqindi',
          ['element', 'miqdor', 'izoh'], rows)

    rows = []
    for m in (1.0, 5.0, 10.0, 20.0, 50.0, 100.0):
        c = calcium_requirement(m)
        rows.append([m, c['n_hf'], c['n_ca'], c['m_ca'], c['m_caglu'], c['m_cacl2'], c['m_caf2']])
    write('kalsiy',
          ['m_HF_g', 'n_HF', 'n_Ca', 'm_Ca_g', 'm_Ca_glyukonat_g', 'm_CaCl2_g', 'm_CaF2_g'], rows)

    a = AHF
    write('fizik_hf',
          ['parametr', 'qiymat', 'birlik'],
          [['qaynash harorati', a['tb'], '°C'],
           ['suyuqlash harorati', a['tm'], '°C'],
           ['suyuqlanish diapazoni', a['liq_lo'], 'K'],
           ['suyuqlanish diapazoni (yuqori)', a['liq_hi'], 'K'],
           ['nisbiy o‘tkazuvchanlik (273 K)', a['eps_273'], ''],
           ['nisbiy o‘tkazuvchanlik (200 K)', a['eps_200'], ''],
           ['o‘z-o‘zini ionlashuv doimiysi', a['k_self_273'], ''],
           ['ekvivalent elektr o‘tkazuvchanlik', a['cond'], 'Ω⁻¹'],
           ['dipol moment', a['mu'], 'D'],
           ['bug‘lanish entalpiyasi', a['dHvap'], 'kJ/mol'],
           [' zichlik (qaynashda)', a['rho'], 'g/cm³'],
           ['Hammett kislotalik H₀', a['h0'], ''],
           ['H₀ (SbF₅ bilan)', a['h0_sbF5'], '']])
    return 6


def main():
    build_csvs()
    print('— spetsiatsiya (suvli HF modeli) —')
    for s in speciation_series():
        print('  c=%5.2f M  h=%.3e  F-=%.4f  HF=%.4f  HF2-=%.4f  pH=%6.3f  ulushlar: HF %.1f %% F- %.1f %% HF2- %.1f %%'
              % (s['c'], s['h'], s['f'], s['hf'], s['hf2'], s['ph'], s['w_hf'], s['w_f'], s['w_hf2']))
    print('— yemirish tezligi modeli —')
    for c in (0.10, 0.50, 1.0, 4.0, 8.0):
        e = etch_rate(c)
        print('  c=%4.2f M  r=%7.1f Angstrom/min = %6.1f nm/min (HF2- ulushi %.0f %%)'
              % (c, e['r'], e['r_nm_per_min'], 100 * e['r_hf2'] / e['r']))
    print('— passivatsiya (1 g metall) —')
    for p in passivation(1.0):
        print('  %-3s -> %-5s %6.3f g  (HF kerak %6.3f g, H2 %5.3f g)'
              % (p['metal'], p['salt'], p['m_salt'], p['m_hf'], p['m_h2']))
    print('— chiqindi modeli —')
    w = waste_model(1000.0, 10.0)
    print('  1000 kg 10 %% HF: Ca(OH)2 %.1f kg, CaF2 %.1f kg, H2O %.1f kg (kirish %.1f = chiqish %.1f)'
          % (w['m_caoh2'], w['m_caf2'], w['m_h2o'], w['m_input'], w['m_output']))
    for ca in (0.001, 0.010, 0.100):
        r = residual_fluoride(ca)
        print('  Ca2+ = %.3f M -> F- qoldig‘i %.3f mg/L' % (ca, r['f_mg']))
    print('— kaltsiy talabi —')
    for m in (20.0, 100.0):
        c = calcium_requirement(m)
        print('  %5.1f g HF -> n(Ca2+) %.3f mol, Ca %.2f g, kalsiy glyukonat %.1f g'
              % (m, c['n_ca'], c['m_ca'], c['m_caglu']))
    print('— olish modeli —')
    p = production_model(1000.0, 0.97, 0.92)
    print('  1000 kg fluorit (97 %%, unum 92 %%): HF %.1f kg, H2SO4 %.1f kg, CaSO4 %.1f kg'
          % (p['m_hf'], p['m_h2so4'], p['m_caso4']))
    g = glass_model(1.0, 48.0)
    print('— shisha modeli —')
    print('  1 kg SiO2: HF %.1f g (48 %% da %.1f g), H2SiF6 %.1f g'
          % (g['m_hf'], g['m_solution'], g['m_h2siof6']))
    print('CSV fayllar yozildi:', ', '.join(sorted(p.name for p in ASSETS.glob('*.csv'))))


if __name__ == '__main__':
    main()
