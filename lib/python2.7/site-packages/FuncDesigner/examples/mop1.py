'''
Simplest MOP example for interalg 
similar to MATLAB gamultiobj example from 
http://www.mathworks.com/products/global-optimization/demos.html?file=/products/demos/shipping/globaloptim/gamultiobjfitness.html
'''
from FuncDesigner import *
from openopt import *
 
x = oovar('x')


f1 = (x + 2) ** 2 - 10
f2 = (x - 2) ** 2 + 20

# let's assing names for objectives
f1('func 1')
f2('func 2')

objectives = [
     # triplets (objective, tolerance, goal)
     f1, 0.1, 'min', 
     f2, 0.1, 'min', 
     ]
     
constraints = [x>-1.5, x<0]

startPoint = {x:-10} # we could use any start point

p = MOP(objectives, startPoint, constraints = constraints)
r = p.solve('interalg')
r.export('/home/dmitrey/asdf.xls')
# for solution coordinates and related values of objective functions
# see r.solutions (list of points and related objective values); 

# expected output
# [...]
# istop: 1001 (all solutions have been obtained)
# Solver:   Time Elapsed = 0.11 	CPU Time Elapsed = 0.11
# 71 solutions have been obtained
# (solutions number may differ)

# optional: graphical visualization (for MOPs with 2 objectives only)
# requires matplotlib installed
r.plot()


