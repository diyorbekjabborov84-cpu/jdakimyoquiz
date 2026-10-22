"""Ideal teaching models. Concentrations and Kc in mol/L, Kwc in (mol/L)^2."""
import math
KC=1e-5
KWC=1e-14

def quadratic(c,k=KC):
    if c<=0 or k<=0: raise ValueError('Positive C and Kc required')
    return 2*k*c/(k+math.sqrt(k*k+4*k*c))

def with_water(c,k=KC,kw=KWC):
    if c<0 or k<=0 or kw<=0:raise ValueError('Invalid parameters')
    lo=math.sqrt(kw);hi=lo+c
    for _ in range(160):
        h=(lo+hi)/2
        if h-kw/h-c*k/(k+h)>0:hi=h
        else:lo=h
    h=(lo+hi)/2
    return h,k/(k+h)

def diprotic(ph,k1=1e-3,k2=1e-7):
    h=10**(-ph);terms=[h*h,k1*h,k1*k2];den=sum(terms)
    return tuple(t/den for t in terms)

if __name__=='__main__':
    for c in [.01,1e-4,1e-8]:
        h,a=with_water(c)
        print(c,quadratic(c),h,-math.log10(h),a)
