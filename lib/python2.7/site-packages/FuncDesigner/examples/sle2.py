"""
Another one, more advanced example
for solving SLE (system of linear equations)
"""
from FuncDesigner import *
from numpy import arange
n = 100
# create some variables
a, b, c = oovar(), oovar(size=n), oovar(size=2*n)

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
r = linSys.solve()

# get result
A, B, C =  a(r), b(r), c(r)
# or 
# A, B, C =  r[a], r[b], r[c]
# A, B, C will be numpy arrays of sizes 1,  n,  2*n
# if failed to solve - A, B, C will contain numpy.nan(s)

print('A=%f B[0]=%f C[15]=%f' % (A, B[0], C[15]))
# for n=100 it prints A=-5.000000 B[0]=-5.00000 C[15]=-1883724.947909

# you could get residuals
# here it will be Python list of length 3 
# that is number of (vectorized) equations
# with elements of type numpy.array
residuals = [F(r) for F in f]
maxResidual = r.ff

