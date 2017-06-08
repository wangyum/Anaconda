"""
FuncDesigner SOCP example with nVariables = 91
"""

from numpy import arange
from FuncDesigner import *
from openopt import SOCP

x, y, z = oovars('x y z', lb = -1, ub = 1)

n = 30

startPoint = {x:0, # thus for our SOCP x will be from R
              y:[0]*n, # y from R^n
              z:[0]*2*n # and z from R^(2*n)
              }

linear_func1 = 5*x + 3*sum(2*y+0.5) + 4*sum(1-z)
linear_func2 = 2*linear_func1 + 100*x
f = 0.5*linear_func2 + 4*linear_func1 + x + 4*sum(3*z+x+1)

constraint1 = norm(x + z - 1) < -12 * x + 5 * sum(z) - 10 + linear_func1

constraint2 = norm(5*x + 0.2*y - arange(n)) < -3 * x + 6*sum(y/2+0.1) + 27


p = SOCP(f, startPoint, constraints = [constraint1('c1'), constraint2('c2')]) 
# you could add lb <= x <= ub, Ax <= b, Aeq x = beq constraints 
# via p = SOCP(f,  ..., A=A, b=b, Aeq=Aeq, beq=beq,lb=lb, ub=ub)
r = p.solve('cvxopt_socp')
x_opt, y_opt, z_opt = r(x,y,z)
'''
...
Solver:   Time Elapsed = 1.27   CPU Time Elapsed = 1.17
objFunValue: -576.03633 (feasible, MaxResidual = 1.98994e-09)
'''