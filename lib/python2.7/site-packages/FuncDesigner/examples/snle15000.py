"""
Solving system of 15000 nonlinear equations with 15000 variables
"""
from FuncDesigner import *
from openopt import SNLE
from numpy import arange

x, y, z = oovars(3)

n = 5000

equations = (
             x + 2* y + 1 == 3*z,  # n equations
             
             #x[i] + x[i+1] + y[i] + log(z[i]^2+15) = i+1, i = 0, 1, ..., n-1
             x+hstack((x[1:n], x[0])) + y + log(z**2 + 15) == arange(1, n+1), # n equations
             
             z + 2*x + 5*y == 100 # n equations
             )
# you can use equations with custom tolerances
# equations = (x**3 + y**3 - 9==0, (x - 0.5*y==0)(tol=1e-9), (cos(z) + x == 1.5) (tol=1e-9))
# if no tol is assigned for an equation, p.ftol (default 10^-6) will be used for that one

startPoint = {x:[0]*n, y:[0]*n, z:[0]*n}

p = SNLE(equations, startPoint)

# for some OpenOpt SNLE solvers we can set some constraints
# p.constraints = [z<70,  z>50,  z + sin(x) < 60]

r = p.solve('matlab_fsolve', matlab='/usr/local/MATLAB/R2012a/bin/matlab')
# Notebook Intel Atom 1.6 GHz:
# Solver:   Time Elapsed = 189.23 	(MATLAB preload time ~ 30 sec)
# peak memory consumption for n = 5000 (thus 15000 variables) 160 MB

