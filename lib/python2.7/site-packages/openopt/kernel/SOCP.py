from baseProblem import MatrixProblem
from numpy import  dot, asfarray, zeros, asscalar
import numpy as np


class SOCP(MatrixProblem):
    probType = 'SOCP'
    _optionalData = ['d', 'A', 'Aeq', 'b', 'beq', 'lb', 'ub']
    goal = 'minimum'
    allowedGoals = ['minimum', 'min']
    #TODO: add goal=max, maximum
    showGoal = True
    #contol = 1e-6
    
    expectedArgs = ['f', 'C']
    # required are f, C, d for OO and f for FD
    
    FuncDesignerSign = 'f'
    
    def __init__(self, *args, **kwargs):
        MatrixProblem.__init__(self, *args, **kwargs)
        if self._isFDmodel():
            self.x0 = self.C
            return
        self.f = asfarray(self.f)
        self.n = self.f.size # for p.n to be available immediately after assigning prob
        if self.x0 is None: self.x0 = zeros(self.n)
    
    def _Prepare(self):
        MatrixProblem._Prepare(self)
        if self._isFDmodel():
            C, d, q, s = renderFDmodel(self)        
            self.C, self.d, self.q, self.s = C, d, q, s
            D = self.f.D(self._x0, fixedVars = self.fixedVars)
            _f = self._point2vector(D).flatten()
            self.f, self._f = _f, self.f

    def __finalize__(self):
        MatrixProblem.__finalize__(self)
        if self.goal in ['max', 'maximum']:
            self.f = -self.f
            for fn in ['fk', ]:#not ff - it's handled in other place in RunProbSolver.py
                if hasattr(self, fn):
                    setattr(self, fn, -getattr(self, fn))
        if hasattr(self, '_f'):
            self.f = self._f
            
    def objFunc(self, x):
        return asscalar(dot(self.f, x))

def renderFDmodel(p):
    from FuncDesigner import hstack, ooarray
    C, d, q, s = [], [], [], []
    D_kwargs = p._D_kwargs
    Z = p._Z
    D_kwargs_y  = D_kwargs.copy()
    D_kwargs_y['useSparse'] = False
    D_kwargs_y['exactShape'] = False
    for c in p.constraints:
        order = c.oofun.getOrder(p.freeVarsSet, p.fixedVarsSet, fixedVarsScheduleID = p._FDVarsID)
        if order < 2:
            continue # linear or box-bound constraint
        if c.descriptor is None:
            p.err('incorrect constraint for SOCP')
        x, op, y = c.descriptor
        if op == '>':
            x, y = y, x
        y_order = 0 if np.isscalar(y) or type(y) == np.ndarray else y.getOrder(p.freeVarsSet, p.fixedVarsSet, fixedVarsScheduleID = p._FDVarsID)
        if y_order > 1 or x.engine != 'norm2':
            p.err('incorrect constraint for SOCP')
        assert len(x.input) == 1, 'incorrect constraint for SOCP'
        z = x._norm_arg
        if isinstance(z, ooarray):
            z = hstack(z)
        
        d.append(z(Z))
        D = z.D(Z, **D_kwargs)
        C.append(p._pointDerivative2array(D))      
        
        S = y if y_order == 0 else y(Z)
        s.append(S)
        if y_order > 0:
            D = y.D(Z, **D_kwargs_y)
            rr = p._pointDerivative2array(D,useSparse = False).flatten()
        else:
            rr = np.zeros(p.n)
        q.append(rr)
    return C, d, q, s










