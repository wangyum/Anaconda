'''
interalg example for global MINLP with 100 variables and some constraints
'''
from FuncDesigner import *
from openopt import *
 
n = 98
x = oovars(n)
x[4].domain = [0.9, -0.7, 0.4] # let's set one of x coords as  discrete variable
y = oovar(domain = bool) # the same to domain = [0,1], but has some optimizations
z = oovar(domain = [1, 1.5, 2, 4, 6, -4, 5]) 

F = sum(x) / n  + y*sin(z)  

constraints = [
               x>-1, x<1, 
               (x[0]**2 + x[1]**2 == 0.5)(tol=1.0e-3), 
                z**2 - y**2 > 0.1, 
               (x[1]**2 + (x[2]-0.02)**2 <= 0.17)(tol=1e-4), 
               (x[2]-0.1)**2 + (x[3]-0.03)**2 <= 0.1,  # default constraint tol is 10^-6
               cos(y) + x[5] <= 0.4, 
               z**2 +arctan(x[1]) < 16, 
               ]

startPoint = {x:[0]*n, y:0, z:3} # [0]*n means Python list [0,0,...,0] with n zeros

# interalg solves problems with specifiable accuracy fTol: 
# | f - f*|< fTol , where f* is  theoretical optimal value

p = GLP(F, startPoint, fTol = 0.05, constraints = constraints)
# interalg requires all finite box bounds, but they can be very huge, e.g. +/- 10^15
# you may found useful arg implicitBounds, for example p.implicitBounds = [-1, 1], 
# for those variables that haven't assigned bounds, 
# it affects only solvers that demand finite box bounds on variables

r = p.solve('interalg', iprint = 100)
print(r(x, y, z))
'''
on slow notebook Intel Atom 2 GHz, peak RAM consumption 130 MB
------------------------- OpenOpt 0.38 -------------------------
solver: interalg   problem: unnamed    type: GLP
 iter   objFunVal   log10(MaxResidual/ConTol)   
    0  0.000e+00                      5.78 
  100  -1.128e+00                     -0.77 
  200  -1.444e+00                     -0.77 
  300  -1.592e+00                     -0.77 
  400  -1.662e+00                     -0.77 
OpenOpt info: Solution with required tolerance 5.0e-02 
 is guarantied (obtained precision: 2.1e-02)
  427  -1.722e+00                     -0.76 
istop: 1000 (solution has been obtained)
Solver:   Time Elapsed = 190.9 	CPU Time Elapsed = 189.13
objFunValue: -1.7220354 (feasible, max(residuals/requiredTolerances) = 0.171915)
'''
