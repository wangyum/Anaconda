from MATLAB_BASE import MATLAB_BASE
#import numpy as np

class bintprog(MATLAB_BASE):
    __name__ = 'bintprog'
    __alg__ = ''
    __authors__ = ''
#    __isIterPointAlwaysFeasible__ = True
    
    __optionalDataThatCanBeHandled__ = ['lb', 'ub', 'A', 'Aeq', 'b', 'beq', 'intVars']
#    properTextOutput = True
    _canHandleScipySparse = True
    opts = ('Display', 'TolFun', 'MaxIter', 'MaxTime', 'TolXInteger')
    
    def __init__(self): pass
    def __solver__(self, p):
        #assert np.array_equiv(p.lb, 0) and np.array_equiv(p.ub, 1), 'bintprog handles only binary variables'
        
        x = MATLAB_BASE._Solve(self, p, p.f, p.A, p.b, p.Aeq, p.beq, p.x0)
        p.xk = p.xf = x.flatten()
