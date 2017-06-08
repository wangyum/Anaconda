"""
Sparse OpenOpt NLP example with knitro
"""

from openopt import *
from numpy import arange
from FuncDesigner import *
N = 50000 
x, y, z = oovars(3)

startPoint = {x:0, y:[0]*N, z:[0]*(2*N)} 
# thus x from R, y from R^N, z from R^2N
# hence for N = 50000 nVars = 150001

objective = x**2 + 2*sum(y**2) + 3*sum(z)

cons = [
        x<150, x + 1e-3*abs(x)**2.05<100,  x>-100, y<arange(N), 
        y>-10-arange(N), z<arange(2*N), z>-100-arange(2*N), 
        x + y > 2-3*arange(N), # N linear constraints
        x**4 + sum(y) + sum(z**2) < 100, 
        x+sum(z)>4 
        ]

p = NLP(objective, startPoint, constraints = cons, iprint=50)
solver = 'knitro'
r = p.minimize(solver)
''' Intel Pentium 2.8 GHz, 32-bit Ubuntu Linux:
------------------------- OpenOpt 0.50 -------------------------
solver: knitro   problem: unnamed    type: NLP   goal: minimum
 iter   objFunVal   log10(maxResidual)   
    0  0.000e+00               0.60 
   50  9.896e+00              -0.39 
  100  1.033e+01            -100.00 
  150  1.006e+01            -100.00 
  200  1.000e+01            -100.00 
  232  1.000e+01            -100.00 
istop: 1000
Solver:   Time Elapsed = 270.07 	CPU Time Elapsed = 270.0
objFunValue: 10.000001 (feasible, MaxResidual = 0)
# Peak memory consumption ~ 400 MB
'''
