'''
Another one interalg example for global MOP
'''
from FuncDesigner import *
from openopt import *
 
x, y, z, t = oovars('x y z t')
n=5
u=oovars(n)
# let's assign names u0,u1,,, u_n-1 to variables from vector u
for i in range(n):
    u[i]('u'+str(i))

# let y and u[0] be discrete vars
y.domain = [0.1, 0.2, 0.3] 
u[0].domain = [-0.1, -0.2, 0.4]

f1 = (x**2 + y**2 + 2*z ** 2 + (t+0.2)**2)+4
f2 = (x-2)**2 + 2*(y-0.3)**2 + 3*(z-0.2) ** 2 + sum(u-0.1)**2
objectives = [
     # triplets (objective, tolerance, goal)
     f1('func 1'), 0.5, 'min', 
     f2('func 2'), 0.5, 'min', 
     # evaluation oofun on string set its name to the string
     ]

constraints = [
               x>-1, x<4, y>-1, y<5, z>-1, z<4, t>-1, t<3,u>-2, u<4,  
               (u[0]**2 + u[1]**2 == 0.5)(tol=1.0e-3), 
               (u[1]**2 + 0.01*u[1]*u[2] + (u[2]-0.02)**2 <= 0.47)(tol=1e-3), 
               (x-0.1)**2 - (y-0.03)**2 <= 10.01,  # default constraint tol is 10^-6
               cos(y) + x <= 1.7, 
               z**2 +arctan(t) < 16, 
               interpolator([1, 2.7, 3, 4.1], [1.001, 4, 9, 16.01])(3+y+2*z) < 20
               ]

startPoint = {x:-10, y:0.2, z:1.5, t:0.5, u:[0]*5} # [0]*n means Python list [0,0,...,0] with n zeros

p = MOP(objectives, startPoint, constraints = constraints)
'''
interalg requires all finite box bounds, but they can be very huge, e.g. +/- 10^15
you may found useful arg implicitBounds, for example p.implicitBounds = [-1, 1], 
for those variables that haven't assigned bounds, 
it affects only solvers that demand finite box bounds on variables

real-time graphical visualization (for MOPs with 2 objectives only)
is performed via setting p.plot = 1 (or p.plot = True);
it requires matplotlib installed
'''
r = p.solve('interalg', plot=True, nProc = 2)
# optional: export results to xls file:
#r.export('/home/dmitrey/asdf.xls')

'''
hints: 
1) if you haven't specified prob parameter plot = True or closed the figure
you can plot it via r.plot()
2) if you have tkinter installed, you can use r.export() and choose xls file path and name in GUI window

Expected output:
[...]
istop: 1001 (all solutions have been obtained)
Solver:   Time Elapsed = 20.54 	CPU Time Elapsed = 20.7
Plotting: Time Elapsed = 3.13 	CPU Time Elapsed = 2.13
9 solutions have been obtained

for solution coordinates and related values of objective functions
see r.solutions, that is list of points and related objective values with entries like
{x: 0.25, y: 0.20000000000000001, z: 0.14677934927586705, t: -0.019045371155551421, 
u0: 0.40000000000000002, u1: -0.58311809774478141, u2: -0.30460558721734537, 
u3: 1.3378469653475178, u4: 1.0, func 1: 4.178332932447926, func 2: 4.913830185229109}
'''


