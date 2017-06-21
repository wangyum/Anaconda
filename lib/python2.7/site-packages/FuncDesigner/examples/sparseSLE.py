"""
FuncDesigner sparse SLE example
"""

from FuncDesigner import *
from numpy import arange
from time import time
t = time()
N = 15000

a, b, c = oovar(), oovar(size=N), oovar(size=2*N)

f1 = a + sum(b*arange(5, N+5))
f2 = a + 2*b + c.sum() 
f3 = a + a.size + 2*c.size 
f4 = c + arange(4, 2*N+4) + 4*f3

f = [a+f4+5, 2*a+b*arange(10, N+10)+15, a+4*b.sum()+2*c.sum()-45]
# alternatively, you could pass equations:
#f = [a+f4==-5, 2*a+b==-15, a==-4*b.sum()-2*c.sum()+45]
linSys = sle(f)
print('Number of equations: ' + str(linSys.n)) # should print 3*N+1

r = linSys.solve() # i.e. using autoselect - solver numpy.linalg.solve for dense (for current numpy 1.4 it's LAPACK dgesv)
# and scipy.sparse.linalg.spsolve for sparse SLEs (for current scipy 0.8 it's LAPACK dgessv)
A, B, C =  a(r), b(r), c(r) # or A, B, C = r[a], r[b], r[c]
print('A=%f B[4]=%f B[first]=%f C[last]=%f' % (A, B[4], B[0], C[-1]))
maxResidual = r.ff

# Note - time may differ due to different matrices obtained from SLE rendering
# because Python 2.6 doesn't has ordered sets (they are present in Python 3.x)
# maybe I'll implement fixed rendering in future for 3.x, I don't want to deal 
# with quite difficult walkaround for 2.6 
print('time elapsed: %f' % (time()-t))

#A=-50992.657068 B[4]=7283.593867 B[first]=10197.031414 C[last]=-15048.714662
#time elapsed: 2.829374

