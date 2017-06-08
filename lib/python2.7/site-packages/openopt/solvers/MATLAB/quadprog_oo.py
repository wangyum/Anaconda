from MATLAB_BASE import MATLAB_BASE

class quadprog(MATLAB_BASE):
    __name__ = 'quadprog'
    __alg__ = ''
    __authors__ = ''
#    __isIterPointAlwaysFeasible__ = True
    
    __optionalDataThatCanBeHandled__ = ['lb', 'ub', 'A', 'Aeq', 'b', 'beq']
#    properTextOutput = True
    _canHandleScipySparse = True
    opts = ('Display', 'TolFun', 'TolX','MaxIter')
    
    def __init__(self): pass
    def __solver__(self, p):
        x = MATLAB_BASE._Solve(self, p, p.H, p.f, p.A, p.b, p.Aeq, p.beq, p.lb, p.ub, p.x0)
        p.xk = p.xf = x.flatten()
