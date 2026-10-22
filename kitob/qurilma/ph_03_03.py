"""Ideal aqueous pH teaching models: concentrations/Kc in mol/L, Kw in (mol/L)^2."""
import math
KW=1e-14

def strong_h(c,kw=KW):
    if c<0 or kw<=0:raise ValueError('Invalid concentration or Kw')
    return (c+math.hypot(c,2*math.sqrt(kw)))/2

def mono_mix(acids,cs=0.0,kw=KW):
    """acids = [(analytical C, concentration Kc), ...]; strong acid anions = cs."""
    if cs<0 or kw<=0 or any(c<0 or k<=0 for c,k in acids):raise ValueError('Invalid parameters')
    lo=strong_h(cs,kw);hi=lo+sum(c for c,k in acids)
    for _ in range(160):
        h=(lo+hi)/2
        f=h-cs-kw/h-sum(c*k/(h+k) for c,k in acids)
        if f>0:hi=h
        else:lo=h
    h=(lo+hi)/2
    return h,tuple(c*k/(h+k) for c,k in acids)

def first_complete_diprotic(c,k2,kw=KW):
    """First proton complete; second in equilibrium; no neutral H2A retained."""
    if c<0 or k2<=0 or kw<=0:raise ValueError('Invalid parameters')
    lo=strong_h(c,kw);hi=strong_h(2*c,kw)
    for _ in range(160):
        h=(lo+hi)/2
        if h-kw/h-c-c*k2/(h+k2)>0:hi=h
        else:lo=h
    h=(lo+hi)/2;a2=c*k2/(h+k2);ha=c-a2
    return h,ha,a2

if __name__=='__main__':
    for c in [.001,1e-8]:
        h=strong_h(c);print('strong',c,h,-math.log10(h))
    for cs in [0,.001]:
        h,a=mono_mix([(.01,1e-5)],cs);print('mono',cs,h,a,-math.log10(h))
    h,ha,a2=first_complete_diprotic(.01,.012);print('sulfate ideal',h,ha,a2,-math.log10(h))
