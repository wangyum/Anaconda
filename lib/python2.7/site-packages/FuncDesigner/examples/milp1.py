# Example of creating MILP in FuncDesigner
# and solving it via OpenOpt

from FuncDesigner import *
from openopt import MILP

# Define some oovars
# old-style:
#x, y, z = oovars('x y z')
# new (OpenOpt v 0.37+): 
x = oovar('x')
y, z = oovars('y z', domain = int)# also you may use domain = bool

# Let's define some linear functions
f1 = 4*x+5*y + 3*z + 5
f2 = f1.sum() + 2*x + 4*y + 15
f3 = 5*f1 + 4*f2 + 20

# Define objective; sum(a) and a.sum() are same as well as for numpy arrays
obj = x.sum() + y + 50*z + sum(f3) + 2*f2.sum() + 4064.6

# Start point - currently matters only size of variables
startPoint = {x:[8, 15], y:25, z:80} # however, using numpy.arrays is more recommended than Python lists

# Define some constraints
cons = [x+5*y<15, x[0]<-5, f1<[25, 35], f1>-100, 2*f1+4*z<[80, 800], 5*f2+4*z<100, [-5.5, -4.5]<x,  x<1, -17<y,  y<20, -4000<z, z<4]

# Create prob
# old-style:
#p = MILP(obj, startPoint, intVars = [y, z], constraints=cons)
# new (OpenOpt v 0.37+): 
p = MILP(obj, startPoint, constraints=cons)

# Solve
r = p.minimize('lpSolve', iprint=-1) # glpk is name of the solver involved, see OOF doc for more arguments

# Decode solution
s = r.xf
print('Solution: x = %s   y = %f  z = %f' % (str(s[x]), s[y], s[z]))
# Solution: x = [-5.25 -4.5 ]   y = 3.000000  z = -33.000000

# OPTIONAL: you can export the problem into MPS format file
# (lpsolve and its Python binding should be properly installed,
# you may take a look at the instructions from openopt.org/LP)
# if file name not ends with '.MPS' or '.mps'
# then '.mps' will be appended
success = p.exportToMPS('milp_1')
# success is False if a error occurred (read-only file system, no write access, etc)
# elseware success is True
# You can solve problems defined in MPS files 
# with a variety of solvers at NEOS server for free
# http://neos.mcs.anl.gov/
# BTW they have Python API along with web API and other
