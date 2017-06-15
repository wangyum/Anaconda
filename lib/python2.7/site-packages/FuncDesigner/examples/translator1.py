"""
This example illustrates using FuncDesigner with routines that has input x (numpy array of size n), 
function fun: R^n -> R^m,
optionally with function Dfun: R^n -> R^(m x n) that provides derivatives.

Examples of the functions: routines from scipy.optimize, especially gradient-based;
scipy odr; scipy.interate ode; maybe some user-defined routines; etc.
Of course, some routines mentioned above are already connected to FuncDesigner but 
an awful lot of other is not yet and some of them (especially user-defined) will never be
"""

from FuncDesigner import *

#                                                         Creating translator:

# Way 1. You can define translator from a set (list, tuple) of oovars
a, b, c = oovar(size=3), oovar(size=10), oovar(size=100)
d = oovar() # for unsized oovars translator will consider it has size 1

T = ootranslator([a, b, c, d])

# Way 2. You can define translator from a point (Python dict of oovars and their values in the point)
a, b, c, d = oovars(4) # create 3 oovars
point = {a:[0, 1, 2], b:[1]*10, c:[0]*100, d:1} # size a is 3, size b is 10, size c is 100, size d is 1
# alternatively: 
# from numpy import *
# point = {a:arange(3), b:ones(10), c:zeros(100)}
T = ootranslator(point)

#                                                               Using translator:

# First of all let's concider using the routines point2vector and vector2point
x = T.point2vector(point) # x is numpy array of length ooT.n = 114
# we can perform some operations on x, e.g. pass to a routine
x += 1 + sin(x)
# and decode it backward:
newPoint = T.vector2point(x)

# Now let's involve automatic differentiation
# create a func
func1 = (sum(a)+2*sum(b)+sum(sin(c)*cosh(d)))**2 # R^ 114 -> R
pointDerivative1 = func1.D(point) # Python dict {a: df/da, b:df/db, c:df/dc, d:df/dd}
func1_d = T.pointDerivative2array(pointDerivative1) # numpy array of size 114

func2 = a+2*sum(b)+sum(sin(c)*cosh(d)) # R^ 114 -> R^3, because size(a) is 3 and other summation elements are of size 1
pointDerivative2 = func2.D(point) # Python dict {a: df/da, b:df/db, c:df/dc, d:df/dd}
func2_d = T.pointDerivative2array(pointDerivative2) # numpy 2d array of shape (3, 114)

# Now you could use translator in a routine that consumes function, it derivative and start point as numpy array
# e.g. for scipy optimize fmin_bfgs you could write
from scipy.optimize import fmin_bfgs
objective = lambda x: func1(T.vector2point(x))
x0 = T.point2vector(point)
derivative = lambda x: T.pointDerivative2array(func1.D(T.vector2point(x))).flatten() 
# without flatten it may be 2d array, e.g. 1 x 114 or 114 x 1

x_opt = fmin_bfgs(objective, x0, derivative)
optPoint = T.vector2point(x_opt) # Python dict {a:a_opt, b:b_opt, c:c_opt, d:d_opt}
a_opt,  b_opt,  c_opt,  d_opt = optPoint[a], optPoint[b], optPoint[c], optPoint[d] # numpy arrays of size 3, 10, 100, 1

# Using sparse matrices
ff = 4 * c**2 # R^100 -> R^100
# param useSparse can be True,  False,  'auto'
# default False; if not, you must check type(result) each time by yourself,
# it can be scalar, numpy.array, one of scipy.sparse matrix types (using isspmatrix() is recommended)
pointDerivative1 = ff.D(point, useSparse = True)

# way 1: use useSparse as pointDerivative2array argument
ff_d = T.pointDerivative2array(pointDerivative1, useSparse = True)
print(type(ff_d), ff_d.shape)
#with scipy installed: <class 'scipy.sparse.coo.coo_matrix'>, (100, 114)
#also you can check scipy.sparse.isspmatrix(ff_d)

# way 2: use useSparse as translator argument in ootranslator constructor
T = ootranslator([a, b, c, d], useSparse = 'auto') # or True
# or direct assignment
T = ootranslator([a, b, c, d])
T.useSparse = True # or 'auto'
