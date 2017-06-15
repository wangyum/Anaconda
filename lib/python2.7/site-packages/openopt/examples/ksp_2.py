#!/usr/bin/python
'''
Simplest OpenOpt KSP example;
requires FuncDesigner installed.
For some solvers limitations on time, cputime, "enough" value, basic GUI features are available.
See http://openopt.org/KSP for more details
'''
from openopt import *
from numpy import sin, cos

N = 150

items = [
         {
             'name': 'item %d' % i, # pay attention that Python indexation starts from zero
             'cost': 1.5*(cos(i)+1)**2, 
             'volume': 2*sin(i) + 3, 
             'mass': 4*cos(i)+5,
             'n':  1 if i < N/3 else 2 if i < 2*N/3 else 3 # number of elements
         } 
         for i in range(N) # i = 0, ... , N-1
         ]
         
constraints = lambda values: (
                              values['volume'] < 10, 
                              values['mass'] < 100,
                              values['nItems'] <= 10, 
                              values['nItems'] >= 5
                              # we could use lambda-func, e,g.
                              # values['mass'] + 4*values['volume'] < 100
                              )
objective = 'cost'
# we could use lambda-func, e.g. 
# objective = lambda val: 5*value['cost'] - 2*value['volume'] - 5*value['mass'] + 3*val['nItems']
p = KSP(objective, items, goal = 'max', constraints = constraints) 
r = p.solve('glpk', iprint = 0) # requires cvxopt and glpk installed, see http://openopt.org/KSP for other solvers
''' Results for Intel Atom 1.6 GHz:
------------------------- OpenOpt 0.50 -------------------------
solver: glpk   problem: unnamed    type: MILP   goal: max
 iter   objFunVal   log10(maxResidual)   
    0  0.000e+00               0.70 
    1  2.739e+01            -100.00 
istop: 1000 (optimal)
Solver:   Time Elapsed = 0.82   CPU Time Elapsed = 0.82
objFunValue: 27.389749 (feasible, MaxResidual = 0)
'''
print(r.xf) # {'item 131': 2, 'item 18': 1, 'item 62': 2, 'item 87': 1, 'item 43': 1}
# pay attention that Python indexation starts from zero: item 0, item 1 ...
# if fields 'name' are absent in items, you'll have list of numbers instead of Python dict
