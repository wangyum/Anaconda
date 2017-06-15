from baseProblem import MatrixProblem
from STAB import set_routine

class DSP(MatrixProblem):
    _optionalData = []
    probType = 'DSP'
    expectedArgs = ['graph']
    allowedGoals = ['minimum dominating set']
    showGoal = False

    _immutable = False
    
    def __setattr__(self, attr, val): 
        if self._immutable: self.err('openopt DSP instances are immutable, arguments should pass to constructor or solve()')
        self.__dict__[attr] = val

    def __init__(self, *args, **kw):
        MatrixProblem.__init__(self, *args, **kw)
        self._init_kwargs = kw
        self._immutable = True
    
    def manage(self, *args, **kw):
        kw['routine'] = 'manage'
        r = self.solve(*args, **kw)
        return r
    
    def solve(self, *args, **kw):
        return set_routine(self, *args, **kw)
#        from openopt import STAB
#        KW = self._init_kwargs
#        KW.update(kw)
#        P = STAB(graph, **KW)
#        r = P.solve(*args)
#        return r
        
