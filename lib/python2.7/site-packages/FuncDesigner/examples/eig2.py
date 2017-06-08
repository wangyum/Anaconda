# An example of FuncDesigner eigenvalues/eigenvectors for an automatic differentiation result,
# see http://openopt.org/EIG for more examples and details
from FuncDesigner import *
from openopt import EIG
from numpy import arange
n = 2
# create everal variables of size 1, n, 2*n
a, b, c = oovar('a'), oovar('b', size=n), oovar('c', size=2*n)

# define some funcs
f1 = 0.01*a + a.size + 2*c.size # R^(2n+1) -> R; a.size and c.size will be resolved into 1 and 2*n

f2 = sum(c) - 100 * a * b - cos(b) - 0.5*b.sum()  + sin(a) + f1

# We can use "for" cycle:
for i in range(4):
    f2 = 0.5*f2 + a + f1 + 1

f3 = sum(f2) / arctan(c) - c**2

# Also, we could use matrix multiplication, eg f5 = dot(someMatrix, f4):
# create a matrix
rng = 1.5 + cos(range(2*n)).reshape(-1, 1) # define 2n x 1 vector
R = dot(rng, rng.T) # create a matrix of shape 2n x 2n

# use matrix dot product
f3 = dot(R, f3) 

# choose a point
Point = {a:-1, b: [2, -3], c: [4, 5, 6, -7]}

# Create Python list of Automaic differentiation results:
C = [f.D(Point, exactShape = True) for f in (f1, f2, f3)]

# define a prob
p = EIG(C, goal={'lm':3})

# solve
r = p.solve('arpack') # requires SciPy installed

# or goal={'largest magnitude':3}, with or without space inside, case-insensitive
# for whole list of available goals see http://openopt.org/EIG

# or use numpy_eig solver instead to search all eigenvalues / eigenvectors:
# it requires only NumPy installed
#p = EIG(C)
#r = p.solve('numpy_eig')

print(r.eigenvalues) # [-221.93543679+0.j  627.10390438+0.j  625.02348702+0.j]

# let's print eigenvector for 1st of the obtained eigenvalues with largest magnitude:
print(r.eigenvectors[0])
'''{
    a: array([  2.49800181e-16+0.j]), 
    b: array([-0.00013151+0.j, -0.00013152+0.j]), 
    c: array([ 0.72631224+0.j,  0.59275862+0.j,  0.31488633+0.j,  0.14816988+0.j])
    }'''

print(r.eigenvectors[-1][a]) # [ -1.64985247e-16+0.j] 

print(type(r.eigenvectors[-1][a]))#<type 'numpy.ndarray'> (sometimes can be a scalar, real or complex)

