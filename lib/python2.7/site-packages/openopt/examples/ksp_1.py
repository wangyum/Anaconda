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

items = [{'name': 'item %d' % i,'weight': 1.5*(cos(i)+1)**2, 
'volume': 2*sin(i) + 3, 'n':  1 if i < N/3 else 2 if i < 2*N/3 else 3} for i in range(N)]
constraints = lambda values: values['volume'] < 10

p = KSP('weight', items, constraints = constraints) 
r = p.solve('glpk', iprint = 0) # requires cvxopt and glpk installed, see http://openopt.org/KSP for other solvers
#Solver:   Time Elapsed = 0.73 	CPU Time Elapsed = 0.55
#objFunValue: 27.389749 (feasible, MaxResidual = 0)
print(r.xf) # {'item 131': 2, 'item 18': 1, 'item 62': 2, 'item 87': 1, 'item 43': 1}
# pay attention that Python indexation starts from zero: item 0, item 1 ...
# if fields 'name' are absent, you'll have list of numbers instead of Python dict
