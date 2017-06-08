"""
Example: solving system of equations:
x + y - 9 = 0
x - 0.5 * y + z * sinh(t) = 0
z + x = 1.5
with a fixed variable, using oosystem
"""
from FuncDesigner import *
x, y, z, t = oovars(4)
S = oosystem()

# if no tol is assigned for an equation, p.ftol (default 10^-6) will be used for that one
S &= (x + y - 9==0, (x - 0.5*y + (z+4)*sinh(t)+t==0)(tol=1e-9), (z + x == 1.5)(tol=1e-9))
startPoint = {x:8, y:15, z:80, t:-0.5} 
# for general linear/nonlinear systems start point can include arrays, e.g. {x:[1, 10, 100], y:15, z:[80,800], t:ones(1000)} 
# and equations can have vector form (R^n_i - >R^m_i)
# No underdetermined or overdetermined linear/nonlinear systems are implemented in FD oosystem solve() yet, i.e. 
# (at least currently) total number of unknown variables have to match total number of equations m_1 + ... + m+k

# fixedVars and freeVars are optional parameters and can be omitted (that means all variables are unknown)
# if we set fixedVars=t then FuncDesigner will solve the system as linear 
# (sometimes autoselect involve as sparse matrices, you can overwrite it via useSparse = True/False),
# if we set fixedVars=(other variable) then FuncDesigner will solve the system as nonlinear
fixedVars=x

r = S.solve(startPoint, fixedVars=fixedVars)
# or
# r = S.solve(startPoint, fixedVars=fixedVars, nlpSolver = 'nssolve', iprint = 0)
# nlpSolver will be used if and only if the problem (wrt given set of fixed/free variables) is nonlinear

xs, ys, zs, ts = r(x, y, z, t)
print('Solution: x = %f   y = %f  z = %f t = %f' % (xs, ys, zs, ts))
"""
for fixedVars=t:
--------------------------------------------------
solver: defaultSLEsolver   problem: unnamed    type: SLE
 iter    objFunVal    log10(MaxResidual/ConTol)   
    0  2.584e+01                      9.51 
    1  1.066e-14                     -5.85 
istop: 10 (solved)
Solver:   Time Elapsed = 0.01 	CPU Time Elapsed = 0.0
objFunValue: 1.0658141e-14 (feasible, max(residuals/requiredTolerances) = 1.42109e-06)
Solution: x = 3.891961   y = 5.108039  z = -2.391961 t = -0.500000

for fixedVars=x:
--------------------------------------------------
solver: nssolve   problem: unnamed    type: NLSP
 iter    objFunVal   
    0  8.650e+04 
  813  7.911e-07 
istop: 10
Solver:   Time Elapsed = 3.8 	CPU Time Elapsed = 3.77
objFunValue: 7.9110148e-07
Solution: x = 8.000000   y = 0.999999  z = -6.500000 t = 2.050118
"""
