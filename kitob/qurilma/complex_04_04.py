"""Ideal, truncated equilibrium teaching models for 4.4 (not measured data).
Constant values are tabulated literature values used only inside explicit
models; every curve is declared as illustrative in the document."""
import math,csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'rasmlar'/'kompleks';ASSETS.mkdir(parents=True,exist_ok=True)

# AgCl / Ag(NH3)2+ (25 C, tabulated values used inside explicit models).
KSP=1.6e-10;BETA2=1.7e7;PKA_NH4=9.25
# Hypothetical M(OH)3 / M(OH)4- model for the amphoteric U-curve.
KSP_M=1.0e-30;BETA4=1.0e34;CM0=1.0e-3

def alpha_nh3(pH):
    """Fraction of unbound ammonia present as free NH3."""
    return 1.0/(1.0+10**(PKA_NH4-pH))

def conditional_beta(pH):
    return BETA2*alpha_nh3(pH)**2

def complex_fraction(L):
    """Fraction of dissolved silver bound as [Ag(NH3)2]+."""
    return BETA2*L**2/(1.0+BETA2*L**2)

def saturation_s(L):
    """Saturated AgCl solubility with excess solid, free ligand L (mol/L)."""
    return math.sqrt(KSP*(1.0+BETA2*L*L))

def amph_csat(pH):
    """Saturated solubility of the hypothetical M(OH)3 amphoteric model."""
    x=10**(pH-14.0)
    return KSP_M*(x**-3+BETA4*x)

def amph_minimum():
    """Stationary point of Csat(x) = Ksp(x^-3 + beta4 x)."""
    x=(3.0/BETA4)**0.25
    return x,14.0+math.log10(x),amph_csat(14.0+math.log10(x))

def separation_onset(Ksp,C0,F=1.0):
    """pH at which a divalent hydroxide starts to precipitate."""
    oh=math.sqrt(Ksp*F/C0)
    return 14.0+math.log10(oh)

def separation_quantitative(Ksp,C0,F=1.0,fraction=0.999):
    """pH at which a given fraction is precipitated."""
    rem=C0*(1.0-fraction)
    oh=math.sqrt(Ksp*F/rem)
    return 14.0+math.log10(oh)

def worked(alpha_pH=10.0,C_B0=0.01):
    """Ligand-balanced AgCl/ammonia problem; returns the physical root."""
    a=alpha_nh3(alpha_pH);lo=0.0;hi=a*C_B0
    for _ in range(200):
        l=(lo+hi)/2.0;s=saturation_s(l);bound=2.0*(s-KSP/s)
        if l/a+bound>C_B0:hi=l
        else:lo=l
    l=(lo+hi)/2.0;s=saturation_s(l);free_ag=KSP/s;cx=s-free_ag
    naive=saturation_s(a*C_B0)
    return dict(alpha=a,free_NH3=l,s=s,free_Ag=free_ag,complex=cx,
                unbound=l/a,bound=2*cx,complex_percent=100*cx/s,
                naive_s=naive,naive_error_percent=100*(naive/s-1.0),
                total=l/a+2*cx)

def save_data():
    sets={
      'species':('log_free_L','free_L_M','fraction_free_Ag','fraction_complex'),
      'proton':('pH','alpha_NH3','log_beta_conditional'),
      'solubility':('log_free_L','free_L_M','saturated_s_M','log_s'),
      'amph':('pH','Csat_M','log_Csat','Cdiss_M')}
    for name,header in sets.items():
        rows=[]
        for j in range(401):
            if name in ('species','solubility'):
                lg=-7.0+5.0*j/400.0;L=10**lg
                if name=='species':
                    rows.append((lg,L,1.0-complex_fraction(L),complex_fraction(L)))
                else:
                    s=saturation_s(L);rows.append((lg,L,s,math.log10(s)))
            elif name=='proton':
                pH=2.0+10.0*j/400.0;a=alpha_nh3(pH)
                rows.append((pH,a,math.log10(conditional_beta(pH))))
            else:
                pH=4.5+3.0*j/400.0;c=amph_csat(pH)
                rows.append((pH,c,math.log10(c),min(c,CM0)))
        with (ASSETS/(name+'.csv')).open('w',newline='') as f:
            w=csv.writer(f);w.writerow(header);w.writerows(rows)

if __name__=='__main__':
    save_data();print(worked());print(amph_minimum())
