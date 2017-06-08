"""
example of rendering FuncDesigner SLE
(system of linear equations)
into ordinary SLE (Ax=b)
"""
from FuncDesigner import *

# Create some variables
a, b = oovars('a', 'b')
c = oovar('c', size=2)

# Python list of linear equations
f = [2*a + 3*b - 2*(c+[1, 2]) * [3, 4] + 5, # R^nVars - > R^2
     2*a+13*b+15, # R^nVars - > R
     a+4*b+2*c.sum()-45# R^nVars - > R
     ]  
# Alternatively, you could pass equations:
# f = [2*a + 3*b - 2*(c+[1, 2]) * [3, 4]==-5, 
#            2*a+15==-13*b, a==-4*b-2*c.sum()+45]

# Assign SLE
linSys = sle(f)

# Rendered matrices for Ax=b are linSys.A (numpy.array of shape 4 x 4) and linSys.b (numpy.array of length 4)
A, B = linSys.A, linSys.b # B instead b for to prevent overriding the oovar b defined above
# However, for large sparse problems they can have other type than numpy.ndarray, 
# e.g. scipy.sparse lil_matrix or coo_matrix (provided you have scipy installed);
# elseware sometimes they can be mere out of your computer RAM.
# You could cast it to ndarray for example via myArr = myMatrix.toarray()

"""
Now let's solve it, for this example I use numpy.linalg.solve 
(that is default dense solver for FD SLEs)
but you can use any other linear solver 
e.g. cvxopt, scipy.lapack or scipy.sparse solvers, PyAMG etc.
Also you can code it (via scipy.sparse or somehow else) into 
one of common sparse matrices formats,
save it into a file and solve it via C, Fortran etc
(BTW f2py or Cython could be useful here)
Current drawback: for huge sparse SLEs you should have enough memory 
to handle dense A before casting to sparse will be performed.
Maybe I'll fix it in future, currently for my purposes I have no deal with these situations
"""
from numpy import linalg
xf = linalg.solve(A, B)

# Decode solution
sol = linSys.decode(xf)
print(c(sol)[0])
print(sol)
# Expected output:
# 10.2
# {b: array([-7.72]), c: array([ 10.2,   6.4]), a: array([ 42.68])}

