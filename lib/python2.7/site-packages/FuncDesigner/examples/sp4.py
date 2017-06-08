from FuncDesigner import *
from openopt import NLP
 
values = [1, -1,  2, 3]
probabilities = [0.1, 0.3, 0.2, 0.4]
A = distribution.discrete(values, probabilities)
B = distribution.exponential(3, 0.7) # location = 3, scale = 0.7
C = distribution.uniform(-1.5, 1.5) # uniform distribution with location = -1.5, scale = 1.5

a = oovars(10)('a') # 10 variables
b = oovars(4) # 4 variables
c = oovar() # 1 variable
 
x = oovars(10, lb=5, ub=15)('x') # 10 unknowns
y = oovars(4, lb=10, ub=20) # 4 unknowns
z = oovar('z') # 1 unknown
 

f = 2*sum(x*a) + sum(y*b) + c**4 + sum(x-1)**2 + sum(y)**2 + sum(y**2) + (z-5)**2
objective = 0.15 * mean(f) + mean(z*c)+ 5*x[0]**4 + 10 * sum(x**2) + 3 * z**2

 
constraints = [
               P(sum(a)**2 + sum(b**2) + sum(x) > 7*(z + sum(y)), interpolate=True) < 0.5, # by default constraint tolerance is 10^-6
               mean(c + a[0] + b[1]+z) >= 15, 
               mean(z + a[0]) >= 15
               ]

startPoint = {
              x: [0]*10, # same to numpy.zeros(10); start point will have x[0]=0, x[1]=0, ..., x[9]=0
              y: [0]*4, z: 0,  
              a: [A]*10, b: [B]*4, c: C}

p = NLP(objective, startPoint, constraints = constraints)

#solver = 'scipy_cobyla' # ~ 20 sec
solver = 'algencan' # ~ 0.8 sec

r = p.minimize(solver, iprint = 1, maxDistributionSize=100, implicitBounds = 100, maxIter = 500)
#istop: 2 (|| gradient F(X[k]) || < gtol)
#Solver:   Time Elapsed = 0.82 	CPU Time Elapsed = 0.8
#objFunValue: 6764.5968 (feasible, MaxResidual = 1.71237e-09)
