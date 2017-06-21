from FuncDesigner import *

a, b, c = oovars('a', 'b', 'c')
f = sum(a*[1, 2])+2*b+4*c
another_func = 2*f + 100 # doesn't matter in the example

startPoint = {a:[100, 12], b:2, c:40} # for to ajust sizes of the variables
S = oosystem(f, another_func)
# add some constraints
S &= [2*c+a-10 < 1500+0.1*b, a-10<150, c<300, a[0]>8.9, c>-100, 
      (a+2*b > [ 7.9, 7.8 ])('sum_a_b', tol=1.00000e-12), a > -10, b > -10, b<10]

for i in range(1000):
    S &= b+i*c > 10*i + sum(a)

w = oovar()
S &= a+sin(w) < 100
startPoint[w] = 1

r = S.minimize(f+cos(w), startPoint, fixedVars=w, solver = 'cvxopt_lp') 
# You could use S.maximize as well. 
# To change solver you could parameter solver='lpSolve', solver='cplex' etc

# default LP solvers are (sequentially, if installed): lpSolve, glpk, cvxopt_lp, lp:ipopt, lp:algencan, lp:scipy_slsqp, lp:ralg
# to change solver you can use kwarg "solver", e.g.
# r = S.minimize(f, startPoint, solver = 'cvxopt_lp')
# also you can provide any openopt kwargs:
# r = S.minimize(f, startPoint, iprint=-1, ...)

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
Solver:   Time Elapsed = 0.02 	CPU Time Elapsed = 0.02
objFunValue: 47.200262 (feasible, max(residuals/requiredTolerances) = 0)
{a: array([  8.9, -10. ]), b: array([ 8.9]), c: array([ 9.98998999])}
"""
