from FuncDesigner import *
from openopt import MINLP

a, b, c = oovars('a', 'b', 'c')
d = oovar('d', domain = [1, 2, 3, 3.5, -0.5,  -4]) # domain should be Python list/set/tuple of allowed values
e = oovar('e', domain = [1, 2, 3, 3.5, -0.5,  -4])
a=oovars(2)('a')
startPoint = {a:[100, 12], b:2, c:40, d:1, e:2} # however, you'd better use numpy arrays instead of Python lists
f = sum(a*[1, 2])**2 + b**2 + c**2 + d**2+e**2
constraints = [(2*c+a-10)**2 < 1.5 + 0.1*b, (a-10)**2<1.5, a[0]>8.9, (a+b > [ 7.97999836, 7.8552538 ])('sum_a_b', tol=1.00000e-12), \
a < 9, b < -1.02, c > 1.01, ((b + c * log10(a).sum() - 1) ** 2==0)(tol=1e-6), b+d**2 < 100]

p = MINLP(f, startPoint, constraints = constraints)
r = p.minimize('interalg', iprint=10, fTol = 1e-8, implicitBounds=1000)
print(r.xf)
a_opt,  b_opt, c_opt, d_opt = r(a, b, c, d)
# or any of the following: 
# a_opt,  b_opt, c_opt,d_opt = r(a), r(b), r(c),r(d)
# r('a'), r('b'), r('c'), r('d') (provided you have assigned the names to oovars as above)
# r('a', 'b', 'c', 'd')
# a(r), b(r), c(r), d(r)

"""
Expected output:
...
OpenOpt info: Solution with required tolerance 1.0e-08 is guarantied
Solver:   Time Elapsed = 4.72 	CPU Time Elapsed = 4.48
objFunValue: 718.2574 (feasible, max(residuals/requiredTolerances) = 0.00144128)
{b: -1.0200000004647196, c: 1.0618036990619659, d: -0.5, e: -0.5, a_0: 8.9999983590234365, a_1: 8.8752537991469964}
"""
