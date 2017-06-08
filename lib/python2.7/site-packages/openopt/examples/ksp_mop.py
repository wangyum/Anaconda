#!/usr/bin/python
'''
Simplest OpenOpt KSP example;
requires FuncDesigner installed.
For some solvers limitations on time, cputime, "enough" value, basic GUI features are available.
See http://openopt.org/KSP for more details
'''
from openopt import *
from numpy import sin, cos

N = 15

items = [{'name': 'item %d' % i,'weight': 1.5*(cos(i)+1)**2, 'volume': 2*sin(i) + 3, 'n': 2} for i in range(N)]
constraints = lambda values: (
                              values['volume'] < 10, 
                              values['volume'] > 5, 
                              values['nItems'] >= N/5, 
                              values['nItems'] <= 2*N/3
                              )

objective = [
              # name, tol, goal
              'volume', 1.0, 'min', 
              'weight', 0.5, 'max'
              # you could use custom funcs, e.g.
              #lambda v: 2*v['weight'] - 3*v['volume'] + 4 * v['nItems']
              # With interalg you could use nonlinear funcs, including FuncDesigner splines, e.g. 
              #lambda v: 2*v['weight'] - 3*v['volume']**2 + 4 * v['nItems'], 0.01, 'max'
              ]

p = KSP(objective, items, constraints = constraints, name = 'ksp_mop') 
r = p.solve('interalg', plot=1, iprint = 1) 
# see r.solutions, r.solutions.coords, r.solutions.values

