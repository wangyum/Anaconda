from FuncDesigner import *
N = 100
a = oovars(N) # create array of N oovars
b = oovars(N) # another array of N oovars 
some_lin_funcs = [i*a[i]+4*i + 5*b[i] for i in range(N)]
f = some_lin_funcs[15] + some_lin_funcs[80] - sum(a) + sum(b)
point = {}
for i in range(N):
    point[a[i]] = 1.5 * i**2
    point[b[i]] = 1.5 * i**3
# BTW we could use 1-dimensional arrays here, eg point[a[25]] = [2,3,4,5], point[a[27]] = [1,2,5] etc
print f(point) # prints 40899980.

from openopt import LP
# define prob
p = LP(f, point)

# add some box-bound constraints
aLBs = [a[i]>-10 for i in range(N)]
bLBs = [b[i]>-10 for i in range(N)]
aUBs = [a[i]<15 for i in range(N)]
bUBs = [b[i]<15 for i in range(N)]
p.constraints = aLBs + bLBs + aUBs + bUBs

# add some general linear constraints
p.constraints.append(a[4] + b[15] + a[20].size - f.size>-9) # array size, here a[20].size = f.size = 1
# or p.constraints += [a[4] + b[15] + a[20].size - f.size>-9]
for i in range(N):
    p.constraints.append(2 * some_lin_funcs[i] + a[i] < i / 2.0 + some_lin_funcs[N-i-1] + 1.5*b[i])
# or p.constraints += [2 * some_lin_funcs[i] + a[i] < i / 2.0 + some_lin_funcs[N-i-1] + 1.5*b[i] for i in range(N]

# solve
r = p.solve('cplex')
print('opt a[15]=%f'%a[15](r)) 
# opt a[15]=-10.000000
