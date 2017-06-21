#!/usr/bin/python
'''
Simplest OpenOpt BPP (Bin Packing Problem) example;
requires FuncDesigner installed.
For some solvers limitations on time, cputime, "enough" value, basic GUI features are available.
See http://openopt.org/BPP for more details
'''
from openopt import *
from numpy import sin

N = 15 
# create N items: 
items = [{'volume': 2*sin(i) + 3} for i in range(N)] # i = 0, ..., N-1 (Python indexation starts from zero)
# bins (containers):
bins = {'volume': 13}
p = BPP(items, bins)
r = p.solve('glpk', iprint = 0) # requires cvxopt and glpk installed, see http://openopt.org/BPP for other solvers
'''
------------------------- OpenOpt 0.50 -------------------------
solver: glpk   problem: unnamed    type: MILP   goal: min
 iter   objFunVal   log10(maxResidual)   
    0  0.000e+00               0.00 
    1  4.000e+00            -100.00 
istop: 1000 (optimal)
Solver:   Time Elapsed = 0.3 	CPU Time Elapsed = 0.11
objFunValue: 4 (feasible, MaxResidual = 0)
'''
print(r.xf) # numbers of items in 1st, 2nd, 3rd, 4th bins
# [(2, 4, 9, 10), (0, 8, 14), (1, 3, 12), (5, 6, 7, 11, 13)]
# pay attention that Python indexation starts from zero: item 0, item 1 ...
