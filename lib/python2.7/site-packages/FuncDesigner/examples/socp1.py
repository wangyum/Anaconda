
"""
FuncDesigner SOCP example
for the problem http://openopt.org/images/2/28/SOCP.png
"""

from numpy import *
from FuncDesigner import *
from openopt import SOCP

x, y, z = oovars('x y z')

f = -2*x + y + 5*z

# since all our oovar instances have size=1 in the example
# to define dot(A, x) we could use either standalone oovar operations:
constraint1 = norm([-13,-12]*x + [3, 12]*y + [5,-6]*z - [3, 2]) < -12 * x - 6 * y + 5 * z - 12

# or matrix multiplication:
C = mat('-3 6 2; 1 9 2; -1 -19 3')
constraint2 = norm(dot(C, hstack((x, y, z))) + [0, 3, -42]) < -3 * x + 6*y -10*z + 27

startPoint = {x:0, y:0, z:0}
p = SOCP(f, startPoint, constraints = [constraint1, constraint2]) 
# you could add lb <= x <= ub, Ax <= b, Aeq x = beq constraints 
# via p = SOCP(f,  ..., A=A, b=b, Aeq=Aeq, beq=beq,lb=lb, ub=ub)
r = p.solve('cvxopt_socp')
x_opt, f_opt = r.xf,  r.ff
print(' f_opt: %f  opt_point: %s' % (f_opt, x_opt))
# f_opt: -38.346368  opt_point: {x: -5.014699121387137, y: -5.7669074876955024, z: -8.5217718312083015}
