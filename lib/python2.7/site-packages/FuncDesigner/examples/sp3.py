''' A little bit vectorized FuncDesigner stochastic optimization example with 15 unknowns
(defined via oovars(n), not oovar(size=n), thus no any vectorization speedup) 

oovar(size=n) doesn't work with stochastic problems yet 
except of some cases where they doesn't interfere in objective or constraints
(sticking oovar(size=n) with std, mean, var of a stochastic var/func is ok)
'''

from FuncDesigner import *
from openopt import NLP

A = distribution.normal(4, 0.5) # gauss distribution with mean = 4, std = 0.5

B = distribution.exponential(3, 0.7) # location = 3, scale = 0.7

C = distribution.uniform(-1.5, 1.5) # uniform distribution from -1.5 to 1.5

a = oovars(10) # 10 variables
b = oovars(4) # 4 variables
c = oovar() # 1 variable

x = oovars(10, lb=5, ub=15) # 10 unknowns
y = oovars(4, lb=10, ub=20) # 4 unknowns
z = oovar() # 1 unknown

f = sum(x*a)**2 + sum(y*b) + c**4 + sum(x-1)**2 + sum(y)**2 + sum(y**2) + (z-5)**2
objective = 0.15 * mean(f+2*x) + sum(y) + sum(x) + z**2* std(c)  

constraints = [
               P(sum(a)**2 + sum(b**2) + sum(x) > 50*(z + sum(y))) < 0.5, # by default constraint tolerance is 10^-6
               mean(c + a[0] + b[1]+z) >= 15
               ]

startPoint = {
              x: [0]*10, # same to numpy.zeros(10); start point will have x[0]=0, x[1]=0, ..., x[9]=0
              y: [0]*4, z: 0,  
              a: [A]*10, b: [B]*4, c: C}

p = NLP(objective, startPoint, constraints = constraints)
solver = 'scipy_cobyla' 
r = p.minimize(solver, iprint = 5, maxDistributionSize=100)
''' output for Intel Atom 1.6 GHz:
------------------------- OpenOpt 0.39 -------------------------
solver: scipy_cobyla   problem: unnamed    type: NLP   goal: minimum
 iter   objFunVal   log10(maxResidual)   
    0  1.890e+01               1.00 
    5  6.791e+03              -1.65 
   10  6.790e+03              -4.46 
   15  6.790e+03              -6.07 
   17  6.790e+03             -14.75 
istop: 1000
Solver:   Time Elapsed = 45.84 	CPU Time Elapsed = 45.6
objFunValue: 6789.6809 (feasible, MaxResidual = 1.77636e-15)
'''
