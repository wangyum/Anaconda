from FuncDesigner import *
a, b, c = oovars('a', 'b', 'c')
f1, f2 = sin(a) + cos(b) - log2(c) + sqrt(b), sum(c) + c * cosh(b) / arctan(a) + c[0] * c[1] + c[-1] / (a * c.size)
f3 = f1*f2 + 2*a + sin(b) * (1+2*c.size + 3*f2.size)
f = (2*a*b*c + f1*f2 + f3 + dot(a+c, b+c))


point = {a:1, b:2, c:[3, 4, 5]} # however, you'd better use numpy arrays instead of Python lists

print(f(point))
print(f.D(point))
print(f.D(point, a))
print(f.D(point, [b]))
print(f.D(point, fixedVars = [a, c]))

M = [[1, 2, 3], [2, 3, 4], [2, 5, 9]] # 2D matrix

_ff = f +  dot(M, sinh(a) + c + c.size + a.size) 
ff = 2*cos(_ff) + 3*sin(f)
print(ff.D(point))




""" Expected output: 
[ 140.9337138   110.16255336   80.67870244]
{a: array([  69.75779959,   88.89020412,  109.93551537]), b: array([-23.10565554, -39.41138045, -59.08378522]), c: array([[-20.52297003,  13.03660168,  13.67886723],
       [  7.39537711, -20.15709726,  12.57210056],
       [  4.17609616,   7.14087693, -17.54104071]])}
[  69.75779959   88.89020412  109.93551537]
{b: array([-23.10565554, -39.41138045, -59.08378522])}
{b: array([-23.10565554, -39.41138045, -59.08378522])}
{a: array([-179.32304408, -252.89529768,  -66.92700988]), b: array([  59.79244279,  112.61139818,   11.88339733]), c: array([[ 53.23808868, -33.47775198, -35.0107186 ],
       [-20.97356663,  57.83174031, -35.6077032 ],
       [ -4.47032227, -10.51221164, -12.80877519]])}
"""
