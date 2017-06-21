from FuncDesigner import *
from openopt import *

x, y, z, u, v, t = oovars('x y z u v t')
F =  [
      (log(x+5)+cos(y) == 1.0)(tol=1e-10), 
      (x**3 + z == -1.5)(tol=1e-5), 
      u**3 + sqrt(abs(v)) == 0.5,#unassigned tol will be taken from p.ftol, default 10^-6
      abs(t)**1.5 + abs(y)**0.1 == 10,
      sinh(v)+arctan(z) == 4,  
      z**15 == u + v
      ]

startPoint = {x:0.51, y:0.52, z:0.53, u:0.54, v:0.55, t:0.56} # doesn't matter for interalg, matters for other solvers

solver='interalg' # set it to scipy_fsolve to ensure that the solver cannot find any solution of the system
p = SNLE(F, startPoint, ftol = 1e-10)
# interalg requires finite box bounds on variables while scipy_fsolve cannot handle any constraints.
# To set box bounds you can do either 
#p.constraints = (x>-10, x<20, y>-20, y<10, z>-30, z<30, u>-32, u<32, v>-21, v<20, t>-10, t<10)
# or
p.implicitBounds=[-10, 10] # to affect all variables without assigned bounds

# you can add some constraints, e.g. p.constraints = t**2+y>10 or p.constraints = [sin(t)>0, y<0] or [sin(t+i) + y < 2*i for i in range(5)]

# without ALL positive tolerances on ALL variables number of solutions is infinite
x.tol = y.tol = z.tol = u.tol = v.tol = t.tol = 1e-5
# alternatively, you could use x, y, z, u, v, t = oovars('x y z u v t', tol = 1e-5)
# solutions s1 and s2 are equivalent if and only if |s1_variable[i]-s2_variable[i]| <= variable[i].tol for all variables
r = p.solve(solver, dataType='float64', maxSolutions = 1000, maxActiveNodes = 150, iprint = 10)# also you can use 'all' or 0, but sometimes it can be out of memory
'''
solver: interalg_0.21   problem: unnamed    type: NLSP
 iter   objFunVal   
    0  8.644e+00 
   10  3.943e+00 
   20  2.248e+00 
   30  8.349e-05 
   40  9.681e-08 
   50  4.327e-10 
OpenOpt info: Solution with required tolerance 1.0e-10 
 is guarantied (obtained precision: 3.9e-11)
   56  3.904e-11 
istop: 1001 (optimal solutions obtained)
Solver:   Time Elapsed = 0.42 	CPU Time Elapsed = 0.42
12 solutions have been obtained
'''
# r.solutions is Python dict with the obtained  solutions
# Let's perform some analysis on them:
from numpy import amin, amax
SolutionsCoords = [(v,  [v(s) for s in r.solutions]) for v in (x, y, z, u, v, t)]
SolutionsCoords.sort(key=lambda elem: amax(elem[1])-amin(elem[1]))
for v, coords in SolutionsCoords:
    print('variable %s is bounded in range of length %0.1e' % (v.name, amax(coords)-amin(coords)))
'''
variable v is bounded in range of length 0.0e+00
variable z is bounded in range of length 4.5e-12
variable u is bounded in range of length 9.1e-12
variable x is bounded in range of length 2.0e-07
variable t is bounded in range of length 8.6e+00
variable y is bounded in range of length 1.6e+01
'''
# So only t and y differ essentially.
# Let's plot them:
S = dict(SolutionsCoords)
from pylab import *
scatter(S[t], S[y], marker = (5, 1, 0), s=75)
xlabel('t'); ylabel('y')
grid(1)
show()

