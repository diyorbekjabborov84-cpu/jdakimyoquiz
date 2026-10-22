"""Ideal concentration titration models, 25 C; all volumes in L."""
import math
KW=1e-14
V0=.025;CA=.1;CB=.1
PHOS=(7.5e-3,6.2e-8,4.2e-13)
def fractions(h,ks):
    logs=[0.0];v=0.0
    for k in ks:
        if k<=0:raise ValueError('K must be positive')
        v+=math.log(k)-math.log(h);logs.append(v)
    m=max(logs);w=[math.exp(l-m) for l in logs];s=sum(w)
    return tuple(t/s for t in w)
def ph(vb,ks=None,ca=CA,cb=CB,v0=V0,kw=KW):
    """None means strong monoprotic acid; tuple ks means polyprotic acid."""
    if vb<0 or ca<=0 or cb<=0 or v0<=0 or kw<=0:raise ValueError('Invalid inputs')
    vol=v0+vb;c=ca*v0/vol;na=cb*vb/vol
    def f(p):
        h=10**(-p)
        charge=1 if ks is None else sum(i*a for i,a in enumerate(fractions(h,ks)))
        return h+na-kw/h-c*charge
    lo=-2.;hi=16.
    if f(lo)<0 or f(hi)>0:raise ValueError('Root outside teaching interval')
    for _ in range(120):
        mid=(lo+hi)/2
        if f(mid)>0:lo=mid
        else:hi=mid
    return (lo+hi)/2

def endpoint_volume(p, k=None,ca=CA,cb=CB,v0=V0,kw=KW):
    """Volume to reach chosen pH for strong or weak monoprotic acid."""
    h=10**(-p);d=h-kw/h;a=1 if k is None else k/(k+h)
    v=v0*(ca*a-d)/(cb+d)
    if v<0:raise ValueError('Target is before initial state or invalid')
    return v

def indicator_fraction(p,pka=7):return 1/(1+10**(pka-p))
if __name__=='__main__':
    for ml in [0,12.5,24.9,25,25.1,50]:print(ml,ph(ml/1000),ph(ml/1000,(1e-5,)))
    for p in [4,7,8.3,10]:
        v=endpoint_volume(p,1e-5);print('weak endpoint',p,1000*v,100*(v/.025-1))
    for ml in [25,50,75]:print('phosphate',ml,ph(ml/1000,PHOS))
