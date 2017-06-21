# An example of FuncDesigner eigenvalues/eigenvectors for a linear equations system,
# see http://openopt.org/EIG for more examples and details
from FuncDesigner import *
from numpy import arange
n = 100
# create some variables
a, b, c = oovar('a'), oovar('b', size=n), oovar('c', size=2*n)

# let's construct some linear functions R^i -> R^j
# in Python range(m, k) is [m, m+1, ..., m+k-1]
f1 = a + sum(b*arange(5, n+5)) # R^(n+1) -> R
f2 = a + 2*b + c.sum() # R^(2n+1) -> R^n

# you could use size of oovars
f3 = a + a.size + 2*c.size # R^(2n+1) -> R; a.size and c.size will be resolved into 1 and 2*n

f4 = c + arange(4, 2*n+4) + f1 + 0.5*f2.sum() + 4*f3

# We can use "for" cycle:
for i in range(4):
    f4 = 0.5*f4 + a + f1 + 1

# Also, we could use matrix multiplication, eg f5 = dot(someMatrix, f4):
rng = 1.5 + cos(range(2*n)).reshape(-1, 1) # define 2n x 1 vector
R = dot(rng, rng.T) # create a matrix of shape 2n x 2n
f4 = dot(R, f4) # involve matrix multiplication

# Create Python list of linear equations 
f = [a+f4+5, 2*a+b*arange(10, n+10)+15, a+4*b.sum()+2*c.sum()-45]
# alternatively, you could pass equations:
f = [a+f4==-5, 2*a+b==-15, a==-4*b.sum()-2*c.sum()+45]

linSys = sle(f)
print('dimension of the SLE: %d' % linSys.n) # dimension of the SLE: 301
# let's search for 4 largest magnitude eigenvalues
r = linSys.eig(goal={'lm':4}, solver='arpack') # requires SciPy installed
# or goal={'largest magnitude':4}, with or without space inside, case-insensitive
# for whole list of available goals see http://openopt.org/EIG

# or use numpy_eig solver instead to search all eigenvalues / eigenvectors:
#r = linSys.eig(solver='numpy_eig') # requires only NumPy installed

print(r.eigenvalues)
#[ -1.35516602e-05 -1.71948079e-05j  -6.93570858e-01 +0.00000000e+00j
#   1.73033511e+00 +0.00000000e+00j   4.88614250e+06 +0.00000000e+00j]
# let's print eigenvector for 1st of the obtained eigenvalues with largest magnitude:
print(r.eigenvectors[0])
#{a: (1.5254915493391314e-11-6.5463605815307811e-11j), b: array([  5.44424793e-07 -7.86615045e-07j, 2.49866501e-07 +1.42239402e-06j,...
# c: array([ -1.41371978e-06 -1.14259649e-06j,1.62417813e-07 -8.00444176e-07j, ..., 5.24756666e-01 -4.13335624e-01j]}
print(r.eigenvectors[-1][a])
#(-0.10673471576669166+0j)
print(type(r.eigenvectors[-1][a]))
#<type 'numpy.complex128'>
