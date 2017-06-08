from FuncDesigner import *
from openopt import QP
from numpy import zeros, arange

n = 15
a = oovar('a')
b = oovars(n, domain = int)('b')
c = oovar('c')
d = oovar('d', domain = bool)

B = 10*sin(arange(n)) # arange(n) = [0, 1, 2, ..., n-1]

objective = (a-1)**2 + 10*sum((b-B)**2) + 3*(1+10*(1+100*c**2)) + 100*(d-5)**2 + (0.1*a+1)*(c+d)
constraints = [a>0, a<1.03, b>0, b<10, c>0,  c<10.1, c**2 < 5, a+b<7]

startpoint = {a: 10, b: zeros(n), c:10, d:0}
p = QP(objective, startpoint, constraints = constraints)
solver = 'cplex'

r = p.solve(solver)
'''
istop: 1000 (Cplex status: "integer optimal, tolerance"; exit code: 102)
Solver:   Time Elapsed = 0.18 	CPU Time Elapsed = 0.15
objFunValue: 5025.3035 (feasible, MaxResidual = 0)
'''
print(a(r)) # 0.0
print(b(r)) # array([ 0.,  7.,  7.,  1.,  0.,  0.,  0.,  7.,  7.,  4.,  0.,  0.,  0., 4.,  7.])
print(r(c,d)) # [0.0, 1.0]

