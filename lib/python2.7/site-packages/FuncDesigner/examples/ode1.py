""" Basic FuncDesigner example for solving ODE with automatic differentiation """

from FuncDesigner import *
from numpy import linspace

# create some variables
x, y, z, t = oovars('x y z t')
# or just x, y, z, t = oovars(4)

S = 15
# Python dict of ODEs
equations = {
             x: 2*x + S*sin(S*t), # dx/dt
             y: y + S*cos(2*S*t + 1), # dy/dt
             z: x + 4*y + S*sin(t+4)# dz/dt
             }

startPoint = {x: 3, y: 4, z: 5}

timeArray = linspace(0, 1, 101) # 0, 0.01, 0.02, 0.03, ..., 0.99, 1.0

# assign ODE. 3rd argument (here "t") is time variable that is involved in differentiation.
myODE = ode(equations, startPoint, {t: timeArray})
# if your equations are time-independend you can use just 
#myODE = ode(equations, startPoint, timeArray)

# Choose solver: 
#solver = 'ode15s'
#solver = 'ode23'
#solver = 'ode113'
#solver = 'ode23t'
#solver = 'ode23tb'
#solver = 'ode45'
solver = 'ode23s'
#solver = 'vode'
#solver = 'zvode'
#solver = 'lsoda'
#solver =  'dopri5'
#solver =  'dop853'
#solver = 'scipy_lsoda' # that is Python wrapper for Fortran package lsoda


r = myODE.solve(solver, 
                abstol = 0.00015, # OpenOpt default: 1.49012e-8
                reltol = 0.00015, # OpenOpt default: 1.49012e-8
                # if "matlab" from command prompt doesn't work
                # set path to matlab executable
                matlab = '/usr/local/MATLAB/R2012a/bin/matlab' 
                )

# FuncDesigner automatic differentiation will be involved
# although it is not used in some solvers
# and seems like essentially matters for ode23s only

X,  Y,  Z = r(x, y, z)
print(X[0:5], Y[50:55], Z[-5:])

"""
(array([ 3.        ,  3.07193008,  3.16782576,  3.28733903,  3.42969264]), 
array([ 5.78536885,  5.70732574,  5.65359904,  5.63434194,  5.65678894]), 
array([ 26.20644978,  26.69463043,  27.19504442,  27.70965187,  28.23994139]))
"""
