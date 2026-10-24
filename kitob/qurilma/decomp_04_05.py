"""Termodinamik va kinetik o'quv taxminiy hisoblari — 4.5 "Parchalanish".
Qiymatlar: OpenStax Chemistry 2e, Appendix G (standart termodinamik xossalar)
va Appendix H (kislotalik konstantalari). Har bir egri chiziq taxminiy hisobidir,
tajriba ma'lumoti emas.
"""
import math, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'rasmlar' / 'parchalanish'
ASSETS.mkdir(parents=True, exist_ok=True)

R = 8.314          # J mol^-1 K^-1
T0 = 298.15        # K, standart holat harorati

# Appendix G: modda -> (ΔfH° kJ/mol, S° J/(mol·K))
DATA = {
    'HNO3(l)':  (-174.10, 155.60),
    'HNO3(g)':  (-133.90, 266.90),
    'NO2(g)':   (33.20, 240.10),
    'H2O(l)':   (-285.83, 70.00),
    'H2O(g)':   (-241.82, 188.80),
    'O2(g)':    (0.00, 205.20),
    'H2SO4(l)': (-813.989, 156.90),
    'SO3(g)':   (-395.72, 256.76),
    'SO2(g)':   (-296.83, 248.20),
    'H2O2(l)':  (-187.78, 109.60),
    'H3PO4(s)': (-1279.00, 110.50),
    'H4P2O7(s)': (-2241.00, None),
    'HPO3(s)':  (-948.50, None),
    'H2S2O7(s)': (-1273.60, None),
    'H2SiO3(s)': (-1188.67, 133.89),
    'SiO2(s)':  (-910.70, 41.50),
    'H3BO3(s)': (-1094.33, 88.83),
    'HBO2(s)':  (-794.25, 37.66),
    'B2O3(s)':  (-1273.50, 53.97),
}
# Appendix H: sulfit tizimi (25 °C)
KA1 = 1.6e-2      # H2SO3 ⇌ H+ + HSO3-
KA2 = 6.4e-8      # HSO3- ⇌ H+ + SO3^2-

# Kinetik shartli hisob (faqat o'quv uchun): A va Ea — real bir kislotga tegishli emas
A_MODEL = 1.0e13      # s^-1
EA_MODEL = 100.0e3    # J/mol


def dH(reagents, products):
    """Reaktsiya entalpiyasi, kJ/mol (mahsulotlar minus reagentlar)."""
    return sum(DATA[m][0] * n for m, n in products.items()) - \
           sum(DATA[m][0] * n for m, n in reagents.items())


def dS(reagents, products):
    """Reaktsiya entropiyasi, J/(mol·K) (mahsulotlar minus reagentlar)."""
    for m in list(products) + list(reagents):
        if DATA[m][1] is None:
            raise ValueError('S° topilmadi: ' + m)
    return sum(DATA[m][1] * n for m, n in products.items()) - \
           sum(DATA[m][1] * n for m, n in reagents.items())


def dG(dh, ds, T=T0):
    """Gibbs energiyasi o'zgarishi, kJ/mol."""
    return dh - T * ds / 1000.0


def lnK(dh, ds, T=T0):
    """Muvozanat konstantasining tabiiy logarifmi."""
    return -dG(dh, ds, T) * 1000.0 / (R * T)


def lgK(dh, ds, T=T0):
    return lnK(dh, ds, T) / math.log(10.0)


def t_star(dh, ds):
    """ΔG(T) = 0 bo'ladigan harorat, K (ΔH va ΔS bir xil ishorada bo'lganda)."""
    return dh * 1000.0 / ds


def arrhenius_k(T, Ea=EA_MODEL, A=A_MODEL):
    """Birinchi tartibli parchalanish uchun taxminiy hisob tezlik konstantasi, s^-1."""
    return A * math.exp(-Ea / (R * T))


def half_life(T, Ea=EA_MODEL, A=A_MODEL):
    """Yarim parchalanish vaqti, s."""
    return math.log(2.0) / arrhenius_k(T, Ea, A)


def sulfite_fractions(pH):
    """S(IV) ning uch shakli ulushlari (erkin SO2·H2O, HSO3-, SO3^2-)."""
    h = 10.0 ** (-pH)
    d = h * h + KA1 * h + KA1 * KA2
    return h * h / d, KA1 * h / d, KA1 * KA2 / d


# --- O'quv uchun tayyor reaksiyalar -------------------------------------
RX_HNO3 = ({'HNO3(l)': 1}, {'NO2(g)': 1, 'H2O(l)': 1, 'O2(g)': 0.5})
RX_H2SO4 = ({'H2SO4(l)': 1}, {'SO3(g)': 1, 'H2O(l)': 1})
RX_H2O2 = ({'H2O2(l)': 1}, {'H2O(l)': 1, 'O2(g)': 0.5})


def worked():
    """11-bo'limdagi to'liq hisob: termodinamik chegara + kinetik blok."""
    out = {}
    for name, rx in (('hno3', RX_HNO3), ('h2so4', RX_H2SO4), ('h2o2', RX_H2O2)):
        dh = dH(*rx); ds = dS(*rx)
        out[name] = dict(dH=dh, dS=ds, dG=dG(dh, ds), lgK=lgK(dh, ds),
                         lnK=lnK(dh, ds), tstar=t_star(dh, ds))
    ks = {}
    for T in (600, 700, 780, 900, 1000, 1200):
        ks[T] = math.exp(lnK(out['h2so4']['dH'], out['h2so4']['dS'], T))
    out['K_H2SO4'] = ks
    out['kin'] = {T: dict(k=arrhenius_k(T), t_half=half_life(T))
                  for T in (298.15, 320, 350, 400)}
    return out


def save_data():
    sets = {
        'dG': ('T_K', 'dG_HNO3_kJ', 'dG_H2SO4_kJ'),
        'K': ('T_K', 'lgK_H2SO4', 'K_H2SO4'),
        'kinetics': ('T_K', 'k_s-1', 'log10_k', 't_half_s'),
        'sulfite': ('pH', 'alpha_SO2aq', 'alpha_HSO3', 'alpha_SO3'),
    }
    for name, header in sets.items():
        rows = []
        if name == 'dG':
            dh1, ds1 = dH(*RX_HNO3), dS(*RX_HNO3)
            dh2, ds2 = dH(*RX_H2SO4), dS(*RX_H2SO4)
            for j in range(401):
                T = 250.0 + 750.0 * j / 400.0
                rows.append((T, dG(dh1, ds1, T), dG(dh2, ds2, T)))
        elif name == 'K':
            dh, ds = dH(*RX_H2SO4), dS(*RX_H2SO4)
            for j in range(401):
                T = 550.0 + 650.0 * j / 400.0
                lg = lgK(dh, ds, T)
                rows.append((T, lg, 10.0 ** lg))
        elif name == 'kinetics':
            for j in range(401):
                T = 250.0 + 200.0 * j / 400.0
                k = arrhenius_k(T)
                rows.append((T, k, math.log10(k), math.log(2.0) / k))
        else:
            for j in range(401):
                pH = 1.0 + 11.0 * j / 400.0
                a2, ah, a3 = sulfite_fractions(pH)
                rows.append((pH, a2, ah, a3))
        with (ASSETS / (name + '.csv')).open('w', newline='') as f:
            w = csv.writer(f); w.writerow(header); w.writerows(rows)


if __name__ == '__main__':
    save_data()
    w = worked()
    for k in ('hno3', 'h2so4', 'h2o2'):
        v = w[k]
        print(k, 'dH=%.3f kJ  dS=%.2f J/K  dG=%.2f kJ  lgK=%.3f  T*=%.1f K'
              % (v['dH'], v['dS'], v['dG'], v['lgK'], v['tstar']))
    print('K(H2SO4):', {T: '%.3g' % k for T, k in w['K_H2SO4'].items()})
    print('kinetics:', {T: ('%.3g' % v['k'], '%.4g s' % v['t_half'])
                        for T, v in w['kin'].items()})
    print('sulfite pH=1,7,12:', [tuple(round(x, 6) for x in sulfite_fractions(p))
                                 for p in (1, 7, 12)])
