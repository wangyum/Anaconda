'''
visualization of FuncDesigner oofun expressions
since FuncDesigner v.0.5107

you could use SymPy or other software from or beyond Python language 
for better expression visualization or for to rewrite your function with better computational performance.

For most of solvers usually you'll hardly get more than several percents speedup, 
but for interalg sometimes (quite rare, although) speedup may be several times 
or orders due to changing of interval analysis quality, e.g. for const1 / (const2 / oofun). 
'''

from FuncDesigner import *

a, b, c= oovars('a b c')

F = 3 + 2*a*10*b/5 - 2 
print(F.expr) 
# 4.0*b*a + 1.0

FF = F + sin(a+b[0]+c[1:5]) + hstack((min((a, b)), 0))
print(FF.expr)
# 4.0*b*a + sin(a + b[0] + c[1:5]) + hstack(min(a, b), 0) + 1.0

f = sin(a) + cos(a*b) + tan(2*b*3*c*4) + arctan(4/a**2) + sinh(sin(a))
print(f.expr) # sin(a) + cos(a*b) + tan(24*c*b) + arctan(4.0/a^2) + sinh(sin(a))

# For some cases pow operator representation via '**' is prefered, use oofun.expression(pow='**'):
f1 = (a+b+1)**c
print(f1.expr)
# (a + b + 1.0)^c
print(f1.expression(pow='**'))
# (a + b + 1.0)**c

d = oovars(2)('d') # array with 2 oovars

f2 = (a+b+1)**(c+d)
print(f2.expr)
# since d is ooarray of length 2 we have ooarray shown here, maybe it will be reworked in future
# ['(a + b + 1.0)^(d_0 + c)', '(a + b + 1.0)^(d_1 + c)']

f3 = 5 + a +3*b/c**2
f4 = 5*f3 + a+c/b + 10
print(f4.expr) # 5*(a + 3*b/c^2 + 5.0) + a + c/b + 10.0

# For custom oofuns name them to provide better view than something like "unnamed_oofun_134(...)"
from scipy import fft
f5 = oofun(lambda *args: abs(fft(hstack(args))), input=[a, sin(a+b), c])('my_fft')
ff = 2*f5 + a+3*b
print(ff.expr)
# 2*(my_fft(a, sin(a + b), c)) + a + 3*b
