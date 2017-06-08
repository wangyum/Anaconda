from numpy import pi

sigma = 1e-4
# here lambda y, x is used to keep it in accordance with scipy.integrate.dblquad API
# for FuncDesigner models you shouldn't keep the order in mind
ff = lambda y, x:  (exp(-(x-0.1)**2/(2*sigma)) * exp(-(y+0.2)**2/(2*sigma))) / (2*pi*sigma) 
#ff = lambda y, x:  (exp(-(x-0.1)**2/(2*sigma)) * exp(-(y+0.2)**2/(2*sigma))) / (2*pi*sigma) 


bounds_x = (-15, 5)
bounds_y = (-15, 5)

from FuncDesigner import *
from openopt import IP
x, y = oovars('x y') 
f = ff(y, x) 
# or 00
#f = (exp(-(x-0.1)**2/(2*sigma)) * exp(-(y+0.2)**2/(2*sigma))) / (2*pi*sigma) 

domain = {x: bounds_x, y: bounds_y}
p = IP(f, domain, ftol = 0.05)
r = p.solve('interalg', maxIter = 50, maxNodes = 500000, maxActiveNodes = 150, iprint = 100)
print('interalg result: %f' % r.ff)
'''
OpenOpt Suite 0.45+ on Intal Atom 1.7 GHz:
Solver:   Time Elapsed = 1.34 	CPU Time Elapsed = 1.34
objFunValue: 1.001662 (feasible, MaxResidual = 0.0369961)
(usually solution, obtained by interalg, has real residual 10-100 times less 
than required tolerance, because interalg works with "most worst case" that extremely rarely occurs. 
Unfortunately, real obtained residual cannot be revealed).
Now let's ensure scipy.integrate dblquad fails to solve the problem and mere lies about obtained residual:'''

from scipy.integrate import dblquad
val, abserr = dblquad(ff, bounds_x[0], bounds_x[1], lambda y: bounds_y[0], lambda y: bounds_y[1])

print('scipy.integrate dblquad value: %f   declared residual: %f' % (val, abserr)) 
''' scipy.integrate dblquad value: 0.000000   declared residual: 0.000000
'''
