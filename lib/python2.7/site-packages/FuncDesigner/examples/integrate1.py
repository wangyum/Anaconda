from numpy import pi, sqrt

sigma = 1e-4
ff = lambda x:  exp(-x**2/(2*sigma)) / sqrt(2*pi*sigma)
bounds_x = (-20, 10) # integral over whole (-inf, inf) is 1.0

from FuncDesigner import *
from openopt import IP
x = oovar('x') 
# f = ff(x) 
# or mere 
f = exp(-x**2/(2*sigma)) / sqrt(2*pi*sigma)

domain = {x: bounds_x}
p = IP(f, domain, ftol = 0.0001)
r = p.solve('interalg', maxIter = 5000, maxActiveNodes = 150)
print('interalg result: %f' % r.ff)
'''Solver:   Time Elapsed = 0.2 	CPU Time Elapsed = 0.2
objFunValue: 1.0000052 (feasible, MaxResidual = 1.31579e-05)
interalg result: 1.000005 (usually solution, obtained by interalg, has real residual 10-100 times less 
than required tolerance, because interalg works with "most worst case" that extremely rarely occurs. 
Unfortunately, real obtained residual cannot be revealed).
Now let's ensure scipy.integrate quad fails to solve the problem and mere lies about obtained residual: '''

from scipy.integrate import quad
val, abserr = quad(ff, bounds_x[0], bounds_x[1])
print('scipy.integrate quad value: %f   declared residual: %f' % (val, abserr)) 
'''scipy.integrate quad value: 0.000000   declared residual: 0.000000
While scipy quad fails already for sigma = 10^-4, interalg works perfectly even for sigma  = 10^-30:
Solver:   Time Elapsed = 0.2 	CPU Time Elapsed = 0.17
interalg result: 1.000008
'''
