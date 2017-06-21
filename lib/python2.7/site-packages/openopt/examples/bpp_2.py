#!/usr/bin/python
'''
An OpenOpt BPP (Bin Packing Problem) example;
requires FuncDesigner installed.
For some solvers limitations on time, cputime, "enough" value, basic GUI features are available.
See http://openopt.org/BPP for more details
'''
from openopt import *
from numpy import sin, cos

N = 15

items = [
         {
         'name': 'item %d' % i, # name of item or item type
         'weight': 1.5*(cos(i)+1)**2, 
         'volume': 2*sin(i) + 3, 
         'n':  1 if i < N/3 else 2 if i < 2*N/3 else 3 # optional: number of items of the type, "1" by default
         } 
         for i in range(N)
         ]
bins = {
'volume': 35, # max volume the bin can store
'weight': 30,  # max weight the bin can handle

# Optional: number of available bins or a good estimation of opt value (no less than the value), 
# it can ESSENTIALLY speedup computations
'n': 5
}
# optional:
# we can add some constraints, each one will affect each bin
constraints = lambda values: 2*values['volume']+0.5*values['weight'] <70
# to add several constraints use constraints = [list_of_constraints],
# e.g. constraints = [lambda v: 2*v['volume']+0.5*v['weight'] <70, lambda v: 4*v['volume']+0.25*v['weight'] >7]
p = BPP(items, bins, constraints = constraints) 
r = p.solve('glpk', iprint = 0) # requires cvxopt and glpk installed, see http://openopt.org/BPP for other solvers
'''------------------------- OpenOpt 0.50 -------------------------
solver: glpk   problem: unnamed    type: MILP   goal: min
 iter   objFunVal   log10(maxResidual)   
    0  0.000e+00               0.48 
    1  4.000e+00            -100.00 
istop: 1000 (optimal)
Solver:   Time Elapsed = 0.11 	CPU Time Elapsed = 0.09
objFunValue: 4 (feasible, MaxResidual = 0)'''

print(r.xf) 
'''[{'item 13': 2, 'item 1': 1, 'item 6': 2}, 
{'item 3': 1, 'item 2': 1, 'item 13': 1, 'item 5': 2, 'item 12': 3}, 
{'item 10': 2, 'item 7': 2, 'item 14': 3}, 
{'item 9': 2, 'item 8': 2, 'item 0': 1, 'item 4': 1, 'item 11': 3, 'item 10': 1}]'''
# pay attention that Python indexation starts from zero: item 0, item 1 ...
# if fields 'name' are absent, you'll have list of numbers instead of Python dict

print(r.values) # per each bin
'''{'volume': (17.245948124126656, 19.886034336769214, 27.3955060854869, 27.004318475761739), 
'weight': (26.000659120389134, 26.211461050259725, 15.120985036297931, 12.972914561409214)}'''
