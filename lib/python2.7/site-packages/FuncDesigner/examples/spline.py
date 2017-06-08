from FuncDesigner import *
a, b, c = oovars('a', 'b', 'c') 
point1 = {a:1, b: 0, c:[1, 2, 3]}
 
mySpline = interpolate.scipy_UnivariateSpline([1, 2, 3, 4], [1.001, 4, 9, 16.01])
# see http://www.scipy.org/doc/api_docs/SciPy.interpolate.fitpack2.UnivariateSpline.html#__init__ for other available arguments
 
f = mySpline(a)
 
print(f(point1))
print(f.D(point1))
 
f2 = a + sin(b) + c[0] + arctan(1.5*f)
F = mySpline(a + f2 + 2*b + (c**2).sum())
 
print(F(point1))
print(F.D(point1))
 
"""
Expected output:
 [ 1.001]
 {a: 2.0015000000000001}
[ 329.61795391]
{a: 108.51234473582626, b: 111.39024933951316, c: array([ 111.39024934,  148.52033245,  222.78049868])}
"""
