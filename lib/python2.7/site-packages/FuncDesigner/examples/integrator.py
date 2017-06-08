"""
Example of FuncDesigner functions integration
Currently scipy.intergate.quad is used (Fortan library QUADPACK, (R^n->R^1 only),
maybe in future higher order solvers will be connected,
e.g. scipy.intergate dblquad, tplquad, quadrature, fixed_quad, trapz etc
"""
from FuncDesigner import *
a, b, c = oovars('a', 'b', 'c') 
f1,  f2 = sin(a)+cosh(b), 2*b+3*sum(c)
f3 = 2*a*b*prod(c) + f1*cos(f2)

point1 = {a:1, b:2, c:[3, 4, 5]}
point2 = {a: -10.4, b: 2.5,  c:[3.2, 4.8]}

# Usage:
# myOOFun = integrator(integration_oofun, domain) 
# where domain is tuple (integration_oovar, lower_bound,  upper_bound)

domain = (b, -1, 1)
f4 = integrator(f1+2*f2+3*f3, domain)
print(f4(point1), f4(point2)) # Expected output: 147.383792876, 102.143425528

#                               integral bounds can be oofuns as well:

f5 = integrator(f1+2*f2+3*f3, (a, 10.4, f2+5*sin(f1)))
print(f5(point1), f5(point2)) # Expected output: 404683.969794 107576.397664

from numpy import inf
f6 = integrator(1/(1+a**2+b**2+sum(c**2)), (a, 10+cos(f2+2*f3), inf))
print(f6(point1), f6(point2)) # Expected output: 0.0847234400308 0.0905041349188

f7 = integrator(f1+2*f2+3*sqrt(abs(f3)), (a, cos(f2+2*f3), f2+5*sin(f1)) )
print(f7(point1), f7(point2)) # Expected output: 9336.70442146 5259.53130904


