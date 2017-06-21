'''
interalg example for global MINLP with 9 variables and some constraints
'''
from FuncDesigner import *
from openopt import *
 
n = 7
x = oovars(n)
for i in range(n):
    x[i](str(i))
x[4].domain = [0.9, -0.7, 0.4] # let's set one of x coords as  discrete variable
y = oovar(domain = bool) # the same to domain = [0,1]
z = oovar(domain = {1, 1.5, 2, 4, 6, -4, 5}) # for obsolete Python versions use [] or () instead of {}

F = abs(x[0]-0.1) + abs(x[n-1]-0.9)  +0.55 * (x[0]-0.1) * (0.2-x[3]) +  1e-1*sum(x)  + y*sin(z) 

constraints = [
               x>-1, x<1, 
               (x[0]**2 + x[1]**2 == 0.5)(tol=1.0e-7), 
               (x[1]**2 + 0.71*x[1]**2 + (x[2]-0.02)**2 <= 0.17)(tol=1e-4), 
               (x[2]-0.1)**2 + (x[3]-0.03)**2 <= 0.0009,  # default constraint tol is 10^-6
               cos(y) + x[5] <= -0.1, 
               z**2 +arctan(x[1]) < 16, 
               interpolator([1, 2, 3, 4], [1.001, 4, 9, 16.01])(3+x[4]+x[5]) < 20
               ]

startPoint = {x:[0]*n, y:0, z:1.5} # [0]*n means Python list [0,0,...,0] with n zeros

# interalg solves problems with specifiable accuracy fTol: 
# | f - f*|< fTol , where f* is  theoretical optimal value

# Any of the following will work here in the same way - 
# NLP, NSP, GLP, MINLP , but word MINLP is more informative
p = MINLP(F, startPoint, fTol = 0.0005, constraints = constraints)
# interalg requires all finite box bounds, but they can be very huge, e.g. +/- 10^15
# you may found useful arg implicitBounds, for example p.implicitBounds = [-1, 1], 
# for those variables that haven't assigned bounds, 
# it affects only solvers that demand finite box bounds on variables

r = p.solve('interalg', dataHandling = 'sorted', iprint = 100)
print(r(x, y, z))
''' results for Intel Atom 1.6 GHz:
------------------------- OpenOpt 0.39 -------------------------
solver: interalg   problem: unnamed    type: MINLP   goal: minimum
 iter   objFunVal   log10(MaxResidual/ConTol)   
    0  1.079e+00                      6.70 
OpenOpt info: Solution with required tolerance 5.0e-04 
 is guarantied (obtained precision: 4.8e-05)
   70  -2.672e-01                     -0.14 
istop: 1000 (solution has been obtained)
Solver:   Time Elapsed = 14.81 	CPU Time Elapsed = 14.0
objFunValue: -0.26721888 (feasible, max(residuals/requiredTolerances) = 0.725122)
[[-0.63521194458007812, -0.3106536865234375, 0.0905609130859375, 0.001522064208984375, -0.69999999999999996, -0.99993896484375, 0.90000152587890625], 1.0, 4.0]
'''
