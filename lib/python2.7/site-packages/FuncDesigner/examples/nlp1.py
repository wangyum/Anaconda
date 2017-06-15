from FuncDesigner import *
from openopt import NLP

a, b, c = oovars('a', 'b', 'c')
f = sum(a*[1, 2])**2+b**2+c**2
startPoint = {a:[100, 12], b:2, c:40} # however, you'd better use numpy arrays instead of Python lists
p = NLP(f, startPoint)
p.constraints = [(2*c+a-10)**2 < 1.5 + 0.1*b, (a-10)**2<1.5, a[0]>8.9, (a+b > [ 7.97999836, 7.8552538 ])('sum_a_b', tol=1.00000e-12), \
a < 9, ((c-2)**2 < 1), (b < -1.02), c > 1.01, ((b + c * log10(a).sum() - 1) ** 2==0)(tol=1e-6)]
r = p.minimize('ralg', plot=0, xtol=1e-7)
#r = p.solve('ralg') # for NLPs old-style (openopt 0.25 and below) p.solve() is same to p.minimize()
#r = p.maximize('ralg')
print(r.xf)
print(a(r.xf))
a_opt,  b_opt, c_opt = r(a, b, c)
# or any of the following: 
# a_opt,  b_opt, c_opt = r(a), r(b), r(c)
# r('a'), r('b'), r('c') (provided you have assigned the names to oovars as above)
# r('a', 'b', 'c')
# a(r), b(r), c(r)

"""
Expected output:
...
objFunValue: 717.75631 (feasible, max constraint =  7.44605e-07)
{a: array([ 8.99999792,  8.87525277]), b: array([-1.01999971]), c: array([ 1.0613562])}
"""
