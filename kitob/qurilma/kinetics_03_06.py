"""Original teaching models, not fitted kinetic data. Time s; T K; concentrations mol/L."""
import math
R=8.31446261815324
T0=298.15
KW=1e-14
KB=1.380649e-23
PLANCK=6.62607015e-34

def reversible(t,kf=.02,kr=.005,factor=1,p0=0):
    if t<0 or kf<=0 or kr<=0 or factor<=0 or not 0<=p0<=1:raise ValueError('Invalid inputs')
    peq=kf/(kf+kr)
    p=peq+(p0-peq)*math.exp(-(kf+kr)*factor*t)
    return 1-p,p

def arrhenius(t,ea=50000,kref=1e-3,tref=T0):
    if min(t,kref,tref)<=0:raise ValueError('Positive T and rate required')
    return kref*math.exp(-ea/R*(1/t-1/tref))

def speedup(delta_g_lowered=10000,t=T0):
    if t<=0:raise ValueError('Positive temperature required')
    return math.exp(delta_g_lowered/(R*t))

def eyring_first_order(dg,t=T0,kappa=1):
    if t<=0 or not 0<kappa<=1:raise ValueError('Invalid T or transmission coefficient')
    return kappa*KB*t/PLANCK*math.exp(-dg/(R*t))

def ph_channels(p,k0=1e-5,kh=10,koh=100,kw=KW):
    h=10**(-p);acid=kh*h;base=koh*kw/h
    return k0,acid,base,k0+acid+base

def buffer_rate(c,p=5,pka=5,kha=.02,ka=0):
    if c<0 or min(kha,ka)<0:raise ValueError('Nonnegative concentration/coefficients required')
    ha=c/(1+10**(p-pka));a=c-ha
    specific=ph_channels(p)[3]
    return ha,a,specific,specific+kha*ha+ka*a

def profile(x,catalyzed=False):
    if not 0<=x<=1:raise ValueError('Coordinate outside [0,1]')
    knots=[(0,0),(.28,55),(.48,10),(.72,45),(1,-20)] if catalyzed else [(0,0),(.5,80),(1,-20)]
    for (xa,ya),(xb,yb) in zip(knots,knots[1:]):
        if xa<=x<=xb:
            z=(x-xa)/(xb-xa)
            return ya+(yb-ya)*(1-math.cos(math.pi*z))/2
    raise AssertionError('Unreachable')

if __name__=='__main__':
    print('DG eq kJ/mol',-R*T0*math.log(4)/1000)
    print('relax half-times',math.log(2)/.025,math.log(2)/.25)
    print('10kJ speedup',speedup())
    for t in [288.15,298.15,308.15]:print('Arrhenius',t,arrhenius(t))
    for p in [3,5,6.5,9,11]:print('pH',p,ph_channels(p))
    for c in [0,.01,.1]:print('buffer',c,buffer_rate(c))
