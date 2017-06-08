"""
Solving system of equations:
x**3 + y**3 - 9 = 0
x - 0.5*y = 0
cos(z) + x - 1.5 = 0
"""
from FuncDesigner import *
from openopt import NLSP

x, y, z = oovars(3)

equations = (x**3 + y**3 - 9, x - 0.5*y, cos(z) + x - 1.5)
# alternatively, since FD 0.32: you can use equations and require custom tolerances
equations = (x**3 + y**3 - 9==0, (x - 0.5*y==0)(tol=1e-9), (cos(z) + x == 1.5) (tol=1e-9))
# if no tol is assigned for an equation, p.ftol (default 10^-6) will be used for that one

startPoint = {x:8, y:15, z:80}

p = NLSP(equations, startPoint)

# optional: we could set some constraints
p.constraints = [z<70,  z>50,  z + sin(x) < 60]

r = p.solve('nssolve') # nssolve is name of solver involved, see OOF doc for more arguments
xs, ys, zs = r(x, y, z)
print('Solution: x = %f   y = %f  z = %f' % (xs, ys, zs))
#Solution: x = 0.999999   y = 2.000000  z = 57.595865
