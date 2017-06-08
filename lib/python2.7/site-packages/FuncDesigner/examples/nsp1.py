from numpy import cos, arange
from FuncDesigner import *
from openopt import NSP

x, y = oovars('x y')

N = 75
koeffs = arange(1, N+1) ** 1.2 # 1, 1.2, 1.44, ..., 1.2^m, ..., 1.2^N

objective = sum(abs(x) * koeffs) + abs(y-15) + abs(y+15) + y**2
constraints = [(y-1)**2<1, abs(y) < 0.5, abs(x[0]) < 1e-5, abs(x[N-1]) < 1e-5]
constraints.append((x - 0.01*arange(N))**2 < 0.1*arange(1, N+1)) # (x_0-0)**2 < 0.1, (x_1-0.01)**2 < 0.2, (x_2-0.02)**2 < 0.2,...
startPoint = {x: cos(1+arange(N)), y:80}

p = NSP(objective, startPoint, maxIter = 1e5, constraints = constraints)

r = p.solve('ralg')
x_opt, y_opt = x(r), y(r)
print(max(abs(x_opt)), y_opt)

'''
expected output:
[...]
  876  3.004e+01            -100.00 
istop: 4 (|| F[k] - F[k-1] || < ftol)
Solver:   Time Elapsed = 7.98 	CPU Time Elapsed = 7.97
objFunValue: 30.042539 (feasible, MaxResidual = 0)
(6.6277698279489041e-06, 0.20306221768582972)
'''
