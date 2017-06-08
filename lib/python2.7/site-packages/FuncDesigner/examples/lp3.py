"""
Sparse LP example
for Nvariables = 25000 
(hence Nconstraints = 75000)
glpk peak memory ~70 Mb, 
time elapsed = 35.79, CPU time elapsed = 35.0
"""

from openopt import LP
from numpy import arange
from FuncDesigner import *
N = 25000 
x, y, z = oovars(3)
startPoint = {x:0, y:[0]*N, z:[0]*(2*N)} # thus x from R, y from R^N, z from R^2N

objective = sum(x) + 2*sum(y) + 3*sum(z)

cons = [x<100,  x>-100, y<arange(N), y>-10-arange(N), z<arange(2*N), z>-100-arange(2*N), x+y>2-3*arange(N), x+z>4-5*arange(2*N)]

p = LP(objective, startPoint, constraints = cons)

solver = 'glpk' # CVXOPT & glpk must be installed
r = p.minimize(solver)

print('objFunValue:%f' % r.ff)
