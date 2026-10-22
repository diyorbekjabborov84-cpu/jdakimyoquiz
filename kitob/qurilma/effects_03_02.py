"""Illustrative models; not fitted acid or solvent measurements."""
import math
R=8.314462618
T0=298.15
PKA0=5.0

def born_factor(rho,epsilon):
    """Dimensionless positive stabilization factor for fixed z=1."""
    if rho<=0 or epsilon<1:raise ValueError('rho>0 and epsilon>=1 required')
    return (1-1/epsilon)/rho

def pka_temperature(t,dh,pka0=PKA0,t0=T0):
    """Constant dissociation enthalpy dh in J/mol; absolute T in kelvin."""
    if t<=0 or t0<=0:raise ValueError('Positive absolute temperature required')
    return pka0+dh/(R*math.log(10))*(1/t-1/t0)
