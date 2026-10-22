"""Ideal aqueous buffers/hydrolysis: C,Kc mol/L; Kw (mol/L)^2; fixed final volume."""
import math
KW=1e-14
PHOS=(7.5e-3,6.2e-8,4.2e-13)
K_NH4=5.6e-10
K_HF=6.4e-4

def fractions(h,ks):
    logs=[0.];x=0.
    for k in ks:
        if k<=0:raise ValueError('Positive constants required')
        x+=math.log(k/h);logs.append(x)
    m=max(logs);w=[math.exp(t-m) for t in logs];s=sum(w)
    return tuple(t/s for t in w)

def solve(acids=(),cations=(),spectator=0.,kw=KW):
    """Neutral-parent acids [(C,(K1,K2,...))], BH+ [(C,Ka)]; spectator=[Na+]-[Cl-]."""
    if kw<=0 or any(c<0 or not ks for c,ks in acids) or any(c<0 or k<=0 for c,k in cations):raise ValueError('Invalid inputs')
    def f(p):
        h=10**(-p)
        pos=sum(c*h/(h+k) for c,k in cations)
        neg=sum(c*sum(i*a for i,a in enumerate(fractions(h,ks))) for c,ks in acids)
        return h+spectator+pos-kw/h-neg
    lo=-2.;hi=16.
    if f(lo)<0 or f(hi)>0:raise ValueError('Root outside teaching interval')
    for _ in range(130):
        p=(lo+hi)/2
        if f(p)>0:lo=p
        else:hi=p
    return (lo+hi)/2

def buffer(c=.1,k=1e-5,ratio=1,added=0):
    if c<0 or ratio<=0:raise ValueError('Invalid concentration/ratio')
    return solve([(c,(k,))],spectator=c*ratio/(1+ratio)+added)

def beta(p,c,k=1e-5,kw=KW):
    h=10**(-p);acid=math.log(10)*c*k*h/(k+h)**2;water=math.log(10)*(h+kw/h)
    return acid,water,acid+water

if __name__=='__main__':
    for q in [0,-.01,.01,.05,.06]:print('buffer',q,buffer(added=q))
    for c in [.1,.001,1e-5,1e-7,1e-9]:print('dilution',c,buffer(c=c))
    print('NaA .01',solve([(.01,(1e-5,))],spectator=.01))
    print('NH4Cl .01',solve(cations=[(.01,K_NH4)],spectator=-.01))
    print('NH4F .01',solve([(.01,(K_HF,))],[(.01,K_NH4)]))
    for d in [1,2]:print('Na phosphate .01',d,solve([(.01,PHOS)],spectator=d*.01))
