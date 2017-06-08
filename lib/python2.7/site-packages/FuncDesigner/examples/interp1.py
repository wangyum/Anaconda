"""
Example of using scipy.interpolate.UnivariateSpline 
this one has been wrapped by a routine from FuncDesigner
and yielded the oofun interpolate.scipy_UnivariateSpline with exactly same args/kwargs
see http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.UnivariateSpline.html
for whole list of possible parameters
"""

from FuncDesigner import *
a, b, c = oovars('a', 'b', 'c') 
point1 = {a:1, b: 0, c:[1, 2, 3]}

mySpline = interpolator([1, 2, 3, 4], [1.001, 4, 9, 16.01])
# Let's check our spline - they are implemented quite prematurely in scipy
print('max residual in spline definition points: %e' % mySpline.residual())
mySpline.plot()

f = mySpline(a)

print(f(point1))
print(f.D(point1))

f2 = a + sin(b) + c[0] + arctan(1.5*f)
F = mySpline(a + f2 + 2*b + (c**2).sum())

print(F(point1))
print(F.D(point1))


"""
Expected output:
max residual in spline definition points: 2.220446e-16
[ 1.001]
{a: 2.0015000000000001}
[ 329.61795391]
{a: 108.51234473582626, b: 111.39024933951316, c: array([ 111.39024934,  148.52033245,  222.78049868])}
"""
