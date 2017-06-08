''' A simple FuncDesigner stochastic optimization example '''
from FuncDesigner import *
from openopt import GLP

A = distribution.gauss(4, 0.5) # gauss distribution with mean = 4, std = 0.5
# this is same to
#from scipy import stats
#_a = distribution.continuous(ppf=stats.norm(4, 5).ppf)
# along with "gauss" you can use "norm" (for scipy.stats compatibility, yet I dislike it due to ambiguity with linalg.norm)
# or "normal"

B = distribution.exponential(3, 0.7) # location = 3, scale = 0.7
# for compatibility with scipy.stats you can use "expon" as well

C = distribution.uniform(-1.5, 1.5) # uniform distribution from -1.5 to 1.5

a, b, c = oovars('a b c')

x, y, z = oovars('x y z', lb=-1, ub=1)

f = sin(b) + cos(b) + arcsin(b/100) + arccos(b/100) + arctan(b) +\
     (1.5+x + 3*y*z)*cosh(b/ (20+x+y)) + sinh(b/30) + tanh(b) + arctanh(b/100) + arccosh(200+b) +\
     arcsinh(3+b) + (x+y+0.4)*exp(b/ (15+x+z)) + sqrt(b+100) + abs(b-2) + log(b+50) + log10(b+100) +\
     log2(b+100) + tan(c/50) + x + 2**(a/4 + x + y + z)

objective = 0.15 * mean(f+2*x) + x*cos(y+2*z) + z * var(b) * std(c) + y * P(a - z + b*sin(c)   > 5) 

constraints = [
               P(a**2 - z + b*c   < 4.7) < 0.03, # by default constraint tolerance is 10^-6
               (P(c/b + z > sin(x)) > 0.02)(tol = 1e-10), # use tol 10^-10 instead; especially useful for equality constraints  
               mean(b+y) <= 3.5
               ]

startPoint = {x: 0, y: 0, z: 0,  a: A, b: B, c: C}

''' This is multiextremum problem (due to sin, cos etc),
thus we have to use global nonlinear solver capable of handling nonlinear constraints
(BTW having probability functions P() make it even discontinuous for discrete distribution(s) involved)
'''

p = GLP(objective, startPoint, constraints = constraints)
solver = 'de' # named after "differential evolution", check http://openopt.org/GLP for other available global solvers
r = p.maximize(solver, maxTime = 150, maxDistributionSize=100, iprint = 50)
'''
------------------------- OpenOpt 0.45 -------------------------
solver: de   problem: unnamed    type: GLP
 iter   objFunVal   log10(MaxResidual/ConTol)   
    0  6.008e+00                      8.40 
   50  7.436e+00                   -100.00 
   93  7.517e+00                   -100.00 
istop: 11 (Non-Success Number > maxNonSuccess = 15)
Solver:   Time Elapsed = 31.58 	CPU Time Elapsed = 30.07
objFunValue: 7.516546 (feasible, max(residuals/requiredTolerances) = 0)
'''
print(r(x, y, z)) # [0.99771171590186, -0.15952854483416395, 0.8584877921129496]
# let's check constraint values
# below we could use c(r.xf) but c(r) is less-to-type and looks better
print(P(a**2 - z + b*c   < 4.7)(r)) # should be less than 0.03
print(P(c/b + z > sin(x))(r)) # should be greater than 0.02
print(mean(b+y)(r)) # should be less than 3.5
#0.0200595929361
#0.029969536767
#[ 3.49947095]
# we could plot cdf (and pdf for continuous) for any stochastic function wrt the optimal parameters point, e.g.
f(r).cdf.plot()
# or, for example, (f + sin(x) + 2*f*cos(y+f) + z * P(f<x))(r).cdf.plot()

