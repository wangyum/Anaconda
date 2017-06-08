from FuncDesigner import *
from numpy import ones
a, b = oovars('a', 'b')
a_infsup = (-ones(3), [1, 2, 3]) # Python list or tuple with 2 elements LowerBound, UpperBound
b_infsup = (2, 50.5)
f1 = 2 * a
f2 = b + 15
f = f1 + f2

f_interval = f.interval({a: a_infsup, b: b_infsup})
print(f_interval.lb, f_interval.ub) # (array([ 15.,  15.,  15.]), array([ 67.5,  69.5,  71.5]))

# for some fixed coords (b) and some interval coords (a):
f_interval = f.interval({a: a_infsup, b: -15})
print(f_interval.lb, f_interval.ub) # (array([-2., -2., -2.]), array([ 2.,  4.,  6.]))
print(f_interval) # "FuncDesigner interval with lower bound [-2. -2. -2.] and upper bound [ 2.  4.  6.]"

f = sin(b) + cos(b+0.15) + a/100
f_interval = f.interval({a: 1000, b: (0.1, 3.14/2)}) # fixed a = 1000, b from -0.1 to 3.14/2
print(f_interval.lb, f_interval.ub) # (9.951182716375465, 11.96891210464248)
