# The example illustrates using "for" cycle in FD code
from FuncDesigner import *
a, b, c = oovars('a', 'b', 'c')
f1, f2 = sin(a) + cos(b) - log2(c) + sqrt(b), sum(c) + c * cosh(b) / arctan(a) + c[0] * c[1] + c[-1] / (a * c.size)
f3 = f1*f2 + 2*a + sin(b) * (1+2*c.size + 3*f2.size) 
F = sin(f2)*f3 + 1
M = 15
for i in range(M):  F = 0.5*F + 0.4*f3*cos(f1+2*f2)
point = {a:1, b:2, c:[3, 4, 5]} # however, you'd better use numpy arrays instead of Python lists
print(F(point))
print(F.D(point))
print(F.D(point, a))
print(F.D(point, [b]))
print(F.D(point, fixedVars = [a, c])) 
"""
[ 4.63468686  0.30782902  1.21725266]
{a: array([-436.83015952,  204.25331181,  186.38788436]), b: array([ 562.63390316, -273.23484496, -256.32464645]), c: array([[ 395.96975635,  167.24928464,   55.74976155],
       [ -74.80518167, -129.34496329,  -19.94804845],
       [ -57.42472654,  -45.93978123,  -66.30049589]])}
[-436.83015952  204.25331181  186.38788436]
{b: array([ 562.63390316, -273.23484496, -256.32464645])}
{b: array([ 562.63390316, -273.23484496, -256.32464645])}
"""
