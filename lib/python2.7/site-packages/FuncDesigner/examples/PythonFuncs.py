# The example illustrates how oovars can pass through ordinary Python functions 
# provided FuncDesigner has appropriate overloads for all functions/operators used inside those ones 

from FuncDesigner import *
a, b, c = oovars('a', 'b', 'c')

def func1(x, y):
    return x+4*y
    
func2 = lambda x, y, z: sin(x)+4*y+3*cos(z) + func1(x, z)
    
def func3(x, y, z):
    return x+2*y+5*sin(z) +func2(x, z, y) + func1(z, y)

print(func3(2, 3, 4))

# Note that func3, func2, func1 could be imported from another file instead of been defined here

myFunc = func3(a, b, c) # now myFunc is instance of FuncDesigner class oofun
point = {a:2, b:3, c:4} 

print(myFunc(point))
print('difference: %f'% (func3(2, 3, 4) - myFunc(point)))
print('Derivative obtained via Automatic differentiation:')
print(myFunc.D(point))

# Expected output:
# 48.1553074605
# [ 48.15530746]
# difference: 0.000000
# Derivative obtained via Automatic differentiation:
# {a: array([ 1.58385316]), b: array([ 9.57663998]), c: array([ 1.7317819])}
