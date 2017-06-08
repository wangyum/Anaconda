from numpy import asanyarray, int8, logical_xor, logical_not
from ooFun import oofun
from logic import AND, EQUIVALENT, NOT, nlh_not
from FDmisc import FuncDesignerException

class BooleanOOFun(oofun):
    # an oofun that returns True/False
#    _unnamedBooleanOOFunNumber = 0
    discrete = True
    def __init__(self, func, _input, *args, **kwargs):
        oofun.__init__(self, func, _input, *args, **kwargs)
        #self.input = oofun_Involved.input
#        BooleanOOFun._unnamedBooleanOOFunNumber += 1
        #self.name = 'unnamed_boolean_oofun_id_' + str(BooleanOOFun._unnamedBooleanOOFunNumber)
        self.name = 'unnamed_boolean_oofun_id_' + str(oofun._id)
        self.oofun = oofun(lambda *args, **kw: asanyarray(func(*args, **kw), int8), _input, vectorized = True)
        # TODO: THIS SHOULD BE USED IN UP-LEVEL ONLY
        self.lb = self.ub = 1
    
    __hash__ = oofun.__hash__
        
    def size(self, *args, **kwargs): raise FuncDesignerException('currently BooleanOOFun.size() is disabled')
    def D(self, *args, **kwargs): raise FuncDesignerException('currently BooleanOOFun.D() is disabled')
    def _D(self, *args, **kwargs): raise FuncDesignerException('currently BooleanOOFun._D() is disabled')
    
    def nlh(self, *args, **kw):
        raise FuncDesignerException('This is virtual method to be overloaded in derived class instance')
    
    __and__ = AND
    
    #IMPLICATION = IMPLICATION
    __eq__ = EQUIVALENT
    __ne__ = lambda self, arg: NOT(self==arg)
    
    def __or__(self, other):
        if other is False: return self
        return ~((~self) & (~other))
        
#        print('__or__')
#        r = BooleanOOFun(logical_or, (self, other), vectorized = True)
#        r.nlh = lambda *args: nlh_or((self, other), r._getDep(), *args)
#        r.oofun = r
#        return r
        
    
    def __xor__(self, other):
        return BooleanOOFun(logical_xor, (self, other), vectorized = True)
    
    def __invert__(self):
        r = BooleanOOFun(logical_not, self, vectorized = True)
        r.nlh = lambda *args: nlh_not(self, r._getDep(), *args)
        r.oofun = r
        return r
