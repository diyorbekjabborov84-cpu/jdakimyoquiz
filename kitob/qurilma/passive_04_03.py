"""Illustrative passivity models, not fitted corrosion data or material ratings."""
from pathlib import Path
import math,csv
F=96485.33212;M=26.9815385;RHO=2.70

def log_anodic(e):
    if e<=.3:return -6+10*e
    if e<=.45:return 3-20*e
    if e<=.8:return -6.
    return -6+20*(e-.8)

def log_cathodic(e,strength):return strength-10*e

def thickness(t,vd,kg=.02,llim=4.,l0=.5):
    linf=llim-vd/kg
    return linf+(l0-linf)*math.exp(-kg*t)

def pitting(loga):
    offset=.08*(loga+2)
    return .65-offset,.35-offset

def worked(i=1e-6,a=10,t=86400,n=3,f=.001):
    q=i*a*t;m=q*M/(n*F);h=m/(RHO*a)*1e4
    return dict(Q=q,m_g=m,m_mg=m*1e3,h_um=h,active_area=a*f,local_i=i/f,local_h_um=h/f)

def stern(ba=.12,bc=.12,rp=26057.67):
    b=ba*bc/(math.log(10)*(ba+bc));return b,b/rp

def save_data():
    a=Path(__file__).resolve().parents[1]/'rasmlar/passivlanish';a.mkdir(parents=True,exist_ok=True)
    def put(n,h,rr):
        with (a/(n+'.csv')).open('w',newline='') as f:
            w=csv.writer(f);w.writerow(h);w.writerows(rr)
    put('qutblanish',['E_relative_V','log_i_anodic','i_anodic_Acm2'],[[e,log_anodic(e),10**log_anodic(e)] for e in [j/500 for j in range(501)]])
    put('aralash',['E_relative_V','log_i_anodic','log_abs_i_weak','log_abs_i_strong'],[[e,log_anodic(e),log_cathodic(e,-3),log_cathodic(e,1)] for e in [j/500 for j in range(501)]])
    put('qalinlik',['time_s','L_v002_nm','L_v006_nm','L_v008_nm'],[[t,*[thickness(t,v) for v in [.02,.06,.08]]] for t in range(301)])
    put('xlorid',['log_a_Cl','a_Cl','E_pit_model_V','E_rp_model_V'],[[x,10**x,*pitting(x)] for x in [-3+j/100 for j in range(301)]])
if __name__=='__main__':save_data();print(worked());print(stern())
