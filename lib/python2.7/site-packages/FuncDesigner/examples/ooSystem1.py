"""
Basic example of using FuncDesigner ooSystem
"""
from FuncDesigner import *
a, b, c = oovars('a', 'b', 'c')
f = (sum(a*[1, 2])**2+b**2+c**2)('func 1')
f2 = (f+4*b+5)('func2')
f3 = ((c-50) ** 0.5)('func3')
S = oosystem(f, f2, f3)

point = {a:[100, 12], b:2, c:40} 
print(S(point)) # prints "func 1 = 16980 func2 = 16993 func3 = nan"
S += (2*a)('doubled a') # adds the oofun 2*a named 'doubled a' as another one element of the ooSystem

S &= (a<15)('constraint A1') # operation "&=" adds constraint
S &= (a>[3, 4])('constraint A2')
S &= (c<30)('c less than 30')
S &= (c<45)('c less than 45')

# with &= you may add tuple, list or set of several oofuns or constraints, as well as with += for oofuns
cons_B,  cons_C = b>1, (c < 39.9999995)('cons_C', tol=1e-4)
S &= (cons_B, cons_C) 

# don't forget about possibility of negative constraints, see FD doc for details
S &= (b>2.0000000000001)('constraint D',  tol=-0.0001)
print('-'*15)
print(S(point))

# we can involve objects of class ooSystemState:
ss = S(point) # object of class ooSystemState
print(ss.activeConstraints) # prints "[pow_domain_14, constraint A1, c less than 30, constraint D]", 
# constraint A1 is present since [100, 12] has element greater than 15
# here pow_domain_14 is an attached constraint (see FD doc) raised from f3 

print(ss(f)) # 16980.
print(ss(f,f2)) # [16980.0, 16993.0] - we may use several aguments to extract their values from ss
print(ss('doubled a')) # [ 200.   24.] - we may use names as well
print(ss.isFeasible) # One of system constraints or attached constraints is False, thus it prints "False"
