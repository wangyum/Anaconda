"""
GLP (GLobal Problem from OpenOpt set) example for FuncDesigner model:
searching for global minimum of the func 
(x-1.5)**2 + sin(0.8 * y ** 2 + 15)**4 + cos(0.8 * z ** 2 + 15)**4 + (t-7.5)**4
subjected to some constraints
See http://openopt.org/GLP for more info and examples.
"""
from openopt import GLP
from FuncDesigner import *

x, y, z, t = oovars(4)

# define objective
f = (x-1.5)**2 + sin(0.8 * y ** 2 + 15)**4 + cos(0.8 * z ** 2 + 15)**4 + (t-7.5)**4

# define some constraints
constraints = [x<1, x>-1, y<1, y>-1, z<1, z>-1, t<1, t>-1, x+2*y>-1.5,  sinh(x)+cosh(z)+sinh(t) <2.0]

# add some more constraints via Python "for" cycle
M = 10
for i in range(M):
    func = i*x+(M-i)*y+sinh(z)+cosh(t)
    constraints.append(func < i+1)

# define start point. You can use variables with length > 1 as well
startPoint = {x:0, y:0, z:0, t:0}

# assign prob
p = GLP(f, startPoint, constraints=constraints,  maxIter = 1e3,  maxFunEvals = 1e5,  maxTime = 5,  maxCPUTime = 5)

#optional: graphic output
#p.plot = 1 or p.solve(..., plot=1) or p = GLP(..., plot=1)

# solve
r = p.solve('de', plot=1) # try other solvers: galileo, pswarm

optPoint, optVal = r.xf, r.ff
x, y, z, t = optPoint[x], optPoint[y], optPoint[z], optPoint[t]
# or 
# x, y, z, t = x(optPoint), y(optPoint), z(optPoint), t(optPoint)


