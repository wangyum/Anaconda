from FuncDesigner import *
from openopt import LLSP
 
# create some variables
a, b, c = oovars('a', 'b', 'c')
# or just a, b, c = oovars(3)
 
# start point is unused by lapack_dgelss and lapack_dgelss
# but it is required to set dimensions of variables
# also, it is used for some converters e.g. r = p.solve('nlp:ralg')
startPoint = {a:0, b:0, c:0} 
# in general case variables can be arrays,
# e.g. startPoint = {a:zeros(100), b:[0, 2], c:ones(20000)} 
 
# overdetermined system of 4 linear equations with 3 variables
# you can use "for" cycle, operations of sum() eg 
# startPoint = {a:[0,10], b:0, c:0} 
# f = [sum(a) + i * b + 4 * sqrt(i) * c - 2 * i**2 for i in range(40)]
f = [2*a+3*b-4*c+5, 2*a+13*b+15, a+4*b+4*c-25, 20*a+30*b-4*c+50]
 
# alternatively, you can use the following vectorized form
measurements_a_koeff = [2, 2, 1, 20]
measurements_b_koeff = [3, 13, 4, 30]
measurements_c_koeff = [-4, 0, 4, -4]
d = [5, 15, -25, 50] 
f = a * measurements_a_koeff + b * measurements_b_koeff + c * measurements_c_koeff + d
# you can set several oofuns with different output sizes, 
# e.g. f = [myOOFun1, myOOFun2, ..., myOOfunN] 
 
# assign prob
p = LLSP(f, startPoint)
 
# solve
r = p.solve('lsqr')
a_sol,  b_sol,  c_sol = r(a, b, c)
# print result
print(r.xf)
 
# Expected output:
# {a: array([-0.3091145]), b: array([-0.86376906]), c: array([ 4.03827441])}

