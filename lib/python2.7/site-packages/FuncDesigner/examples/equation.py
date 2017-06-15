from FuncDesigner import *
from openopt import *

x = oovar(tol=1e-3) # solutions x1 and x2 with |x1-x2| < tol will be considered as equivalent
y = (1 + 1e-10 + sin(150*x)) * cos(10*x) ** 2
equation = y == 0

# we will search equation roots in the line segment [0,15]
constraints = (x>0,  x<1.5) 

startPoint = {x:0} # doesn't matter essentially for the solver "interalg" 
p = SNLE(equation, startPoint, constraints = constraints, ftol = 1e-10) # required tolerance for solutions
solver = oosolver('interalg', maxSolutions = 10000)
r = p.solve(solver)
'''
------------------------- OpenOpt 0.34 -------------------------
solver: interalg_0.21   problem: unnamed    type: NLSP
 iter   objFunVal   nSolutions   
    0  1.000e+00          0 
   10  7.367e-12          4 
OpenOpt info: Solution with required tolerance 1.0e-10 
 is guarantied (obtained precision: 5.1e-11)
   12  5.118e-11          5 
istop: 1001 (solutions are obtained)
Solver:   Time Elapsed = 0.07 	CPU Time Elapsed = 0.05
5 solutions have been obtained
'''
from pylab import plot, scatter, show, ylim, grid
from numpy import arange
xx = arange(0, 1.5, 0.001)
plot(xx, y({x:xx}))
X = [x(s) for s in r.solutions]
scatter(X, [0]*len(X), marker = (5, 1, 0), s=75)
ylim(-0.1, 2.1)
grid();show()

