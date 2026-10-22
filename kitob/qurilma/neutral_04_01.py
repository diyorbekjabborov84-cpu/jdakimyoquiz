"""Neutralization teaching models; ideal water at 25 C. No experimental data."""
import math
from buffer_03_05 import solve,fractions,PHOS,K_NH4,KW
R=8.31446261815324
T=298.15

def proton_transfer(dpka):
    k=10**dpka
    f=1/(1+10**(-dpka/2))
    return k,f,-R*T*math.log(k)

def phosphate(r,c=.01):
    if r<0 or c<=0:raise ValueError('Invalid composition')
    p=solve([(c,PHOS)],spectator=r*c)
    return p,fractions(10**(-p),PHOS)

def strong_mix(ca,va,cb,vb,kw=KW):
    if min(ca,va,cb,vb)<=0:raise ValueError('Positive inputs required')
    na=ca*va;nb=cb*vb;v=va+vb;d=(na-nb)/v
    # Stable root also on the basic side.
    root=math.hypot(d,2*math.sqrt(kw))
    h=(d+root)/2 if d>=0 else 2*kw/(root-d)
    return min(na,nb),h,-math.log10(h),nb/v,na/v

def calorimetry(xi=.01,dh=-57000,m=200,cp=4.18,c_cal=20):
    if xi<0 or min(m,cp)<=0 or c_cal<0:raise ValueError('Invalid calorimetry parameters')
    q_reaction=xi*dh;q_absorbed=-q_reaction
    return q_reaction,q_absorbed,q_absorbed/(m*cp+c_cal)

def salt_ph():
    return {'NaCl':solve(), 'NaA':solve([(.01,(1e-5,))],spectator=.01),
            'NH4Cl':solve(cations=[(.01,K_NH4)],spectator=-.01),
            'BHA':solve([(.01,(1e-5,))],[(.01,1e-9)])}

if __name__=='__main__':
    print('mixed',strong_mix(.15,.04,.2,.025))
    print('calorimetry',calorimetry())
    print('salts',salt_ph())
    for r in [1,2,3]:print('phosphate',r,phosphate(r))
