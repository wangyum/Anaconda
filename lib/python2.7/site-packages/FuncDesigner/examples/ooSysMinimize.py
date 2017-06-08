from FuncDesigner import *

a, b, c = oovars('a', 'b', 'c')
f = (sum(a*[1, 2])**2+b**2+c**2)('f')
another_func = 2*f + 100 + log(c-1.075) # this func has attached constraint c > 1.075 with a negative tol ~ -1e-7

startPoint = {a:[100, 12], b:2, c:40} # however, you'd better use numpy arrays instead of Python lists
S = oosystem(f, another_func)
# add some constraints
S &= [(2*c+a-10)**2 < 1.5 + 0.1*b, (a-10)**2<1.5, c**c<3, a[0]>8.9, 
      (a+b > [ 7.97999836, 7.8552538 ])('sum_a_b', tol=1.00000e-12), a < 9, b < -1.02]

r = S.minimize(f, startPoint) 
# you could use S.maximize as well

# default NLP solver is ralg;
# to change solver you can use kwarg "solver", e.g.
# r = S.minimize(f, startPoint, solver = 'ipopt')
# also you can provide any openopt kwargs:
# r = S.minimize(f, startPoint, xtol=1e-7, ftol = 1e-7, maxTime = 1e3, ...)

print(r.xf)
a_opt,  b_opt, c_opt = r(a, b, c)
# or any of the following: 
# a_opt,  b_opt, c_opt = r(a), r(b), r(c)
# r('a'), r('b'), r('c') (provided you have assigned the names to oovars as above)
# r('a', 'b', 'c')
# a(r), b(r), c(r)

"""
Expected output:
...
objFunValue: 717.78622 (feasible, max(residuals/requiredTolerances) = 0.786102)
{a: array([ 8.99999758,  8.87525302]), b: array([-1.01999921]), c: array([ 1.07534812])}
"""
