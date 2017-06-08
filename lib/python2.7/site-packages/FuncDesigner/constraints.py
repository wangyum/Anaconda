from ooFun import oofun
from BooleanOOFun import BooleanOOFun
from FDmisc import FuncDesignerException
from ooPoint import ooPoint
from numpy import atleast_1d, isnan, logical_and, inf, asfarray, tile, vstack, prod, int8, int16, int32, int64, \
isinf, logical_or, logical_not, isfinite, log2, any, ndarray

class BaseFDConstraint(BooleanOOFun):
    isConstraint = True
    tol = 0.0 
    expected_kwargs = set(['tol', 'name'])
    __hash__ = oofun.__hash__
    descriptor = None
    #def __getitem__(self, point):

    def __call__(self, *args,  **kwargs):
        expected_kwargs = self.expected_kwargs
        if not set(kwargs.keys()).issubset(expected_kwargs):
            raise FuncDesignerException('Unexpected kwargs: should be in '+str(expected_kwargs)+' got: '+str(kwargs.keys()))
            
        for elem in expected_kwargs:
            if elem in kwargs:
                setattr(self, elem, kwargs[elem])
        
        if len(args) > 1: raise FuncDesignerException('No more than single argument is expected')
        
        if len(args) == 0:
           if len(kwargs) == 0: raise FuncDesignerException('You should provide at least one argument')
           return self
           
        if isinstance(args[0], str):
            self.name = args[0]
            return self
        elif hasattr(args[0], 'xf'):
            return self(args[0].xf)
            
        return self._getFuncCalcEngine(*args,  **kwargs)
        
    def _getFuncCalcEngine(self, *args,  **kwargs):
        
        if not isinstance(args[0], dict): 
            raise FuncDesignerException('unexpected type: %s' % type(args[0]))
            
        isMultiPoint = isinstance(args[0], ooPoint) and args[0].isMultiPoint == True
        
        val = self.oofun(args[0])
        Tol = max((0.0, self.tol))
        
        from FuncDesigner import _Stochastic
        if isinstance(val, _Stochastic) or (isinstance(val, ndarray) and isinstance(val.flat[0], _Stochastic)):
            raise FuncDesignerException('''
                error in evaluation of %s (%s):
                objective and constraints cannot be directly applied on stochastic variables,
                you should use functions like mean, std, var, P.''' % (self.name, self.expr)
                )
        
        if isMultiPoint:
            return logical_and(self.lb-Tol<= val, val <= self.ub + Tol)
        elif any(isnan(val)):
            return False
        if any(atleast_1d(self.lb-val)>Tol):
            return False
        elif any(atleast_1d(val-self.ub)>Tol):
            return False
        return True
            

    def __init__(self, oofun_Involved, *args, **kwargs):
        BooleanOOFun.__init__(self, oofun_Involved._getFuncCalcEngine, (oofun_Involved.input if not oofun_Involved.is_oovar else oofun_Involved), *args, **kwargs)
        #oofun.__init__(self, lambda x: oofun_Involved(x), input = oofun_Involved)
        if len(args) != 0:
            raise FuncDesignerException('No args are allowed for FuncDesigner constraint constructor, only some kwargs')
            
        # TODO: replace self.oofun by self.engine
        self.oofun = oofun_Involved
    
#    def __ge__(self, other):
#        from overloads import hstack
#        x, op, y = self.descriptor
#        if op == '<':
#            x, y = y, x
#        return hstack((self, y>other))
#        
#    __gt__ = __ge__
#    
#    def __le__(self, other):
#        from overloads import hstack
#        x, op, y = self.descriptor
#        if op == '>':
#            x, y = y, x
#        return hstack((self, other<x))
#    __lt__ = __le__

class SmoothFDConstraint(BaseFDConstraint):
    __getitem__ = lambda self, point: self.__call__(point)
    __hash__ = oofun.__hash__

    def __init__(self, *args, **kwargs):
        BaseFDConstraint.__init__(self, *args, **kwargs)
        self.lb, self.ub = -inf, inf
        for key, val in kwargs.items():
            if key in ['lb', 'ub', 'tol']:
                setattr(self, key, asfarray(val))
            else:
                raise FuncDesignerException('Unexpected key in FuncDesigner constraint constructor kwargs')
    
    def lh(self, *args, **kw): # overwritten in ooVar, mb something else
        if '_invert' not in self.__dict__:
            from logic import NOT
            self._invert = NOT(self)
        return self._invert.nlh(*args, **kw)
    
#    def nlh(self, Lx, Ux, p, dataType):
    
    def nlh(self, Lx, Ux, p, dataType, fullOutput = False):
        m = Lx.shape[0] # is changed in the cycle
        assert m != 0, 'bug in FuncDesigner'
        #return None, None, None
        
        tol = self.tol if self.tol > 0.0 else p.contol if self.tol == 0 else 0.0 # 0 for negative tolerances
        # TODO: check it
        if p.solver.dataHandling == 'sorted': tol = 0
        selfDep = (self.oofun._getDep() if not self.oofun.is_oovar else set([self.oofun]))
        
        # TODO: improve it
        domainData = [(v, (Lx[:, k], Ux[:, k])) for k, v in enumerate(p._freeVarsList) if v in selfDep]

        domain = ooPoint(domainData, skipArrayCast=True)
        domain.isMultiPoint = True
        domain.nPoints = m
        domain.dictOfFixedFuncs = p.dictOfFixedFuncs
        domain._dictOfRedirectedFuncs = p._dictOfRedirectedFuncs
        domain.maxDistributionSize = p.maxDistributionSize
        domain._dictOfStochVars = p._dictOfStochVars
        domain._p = p
        
        # TODO: rework it 
        r, r0 = self.oofun.iqg(domain, dataType, self.lb, self.ub, None)#, Lx, Ux)
        
        Lf, Uf = r0.lb, r0.ub
        tmp = getSmoothNLH(tile(Lf, (2, 1)), tile(Uf, (2, 1)), self.lb, self.ub, tol, m, dataType)
        T02 = tmp
        T0 = T02[:, tmp.shape[1]/2:].flatten()
        if fullOutput:
            Uf[Uf==inf] = 1e300
            Lf[Lf==-inf] = -1e300
            Uf_Lf = Uf - Lf
            Uf_Lf[Uf_Lf<1e-300] = 1e-300
            #T_ = (T0, log2(Uf_Lf))
            T_ = (T0, Uf_Lf.T)# * tol)
        else:
            T_ = T0
        
        res, uflf_res = {}, {}
        if len(r):
            dep = selfDep.intersection(domain.keys()) # TODO: Improve it
            for v in dep:
                Lf, Uf = vstack((r[v][0].lb, r[v][1].lb)), vstack((r[v][0].ub, r[v][1].ub))

                # TODO: 1) FIX IT it for matrix definiteRange
                # 2) seems like DefiniteRange = (True, True) for any variable is enough for whole range to be defined in the involved node
#                DefiniteRange = logical_and(DefiniteRange, r[v][0].definiteRange)
#                DefiniteRange = logical_and(DefiniteRange, r[v][1].definiteRange)
                
                tmp = getSmoothNLH(Lf, Uf, self.lb, self.ub, tol, m, dataType) #- T02
                #tmp[isnan(tmp)] = inf
                res[v] = tmp 
                if fullOutput:
                    Uf[Uf==inf] = 1e300
                    Lf[Lf==-inf] = -1e300
                    Uf_Lf = Uf - Lf
                    Uf_Lf[Uf_Lf<1e-300] = 1e-300
                    #uflf_res[v] = log2(Uf_Lf)
                    uflf_res[v] = Uf_Lf.T#*tol
        res_ = (res, uflf_res) if fullOutput else res
        #return T0, res, r0.definiteRange
        return T_, res_, r0.definiteRange
        
def getSmoothNLH(Lf, Uf, lb, ub, tol, m, dataType):

    M = prod(Lf.shape) / (2*m)

    Lf, Uf  = Lf.reshape(2*M, m).T, Uf.reshape(2*M, m).T
    
#    lf1, lf2, uf1, uf2 = Lf[:, 0:M], Lf[:, M:2*M], Uf[:, 0:M], Uf[:, M:2*M]

    UfLfDiff = Uf - Lf
    if UfLfDiff.dtype.type in [int8, int16, int32, int64, int]:
        UfLfDiff = asfarray(UfLfDiff)
    #UfLfDiff[UfLfDiff > 1e200] = 1e200
    if lb == ub:
        val = ub
        
#        ind1, ind2 = val - tol > Uf, val+tol < Lf
#        residual[ind1] += val - tol - Uf[ind1]
#        residual[ind2] += Lf[ind2] - (val + tol)
        
        Uf_t,  Lf_t = Uf.copy(), Lf.copy()
        if Uf.dtype.type in [int8, int16, int32, int64, int] or Lf.dtype.type in [int8, int16, int32, int64, int]:
            Uf_t,  Lf_t = asfarray(Uf_t), asfarray(Lf_t)
        
        Uf_t[Uf_t > val + tol] = val + tol
        Lf_t[Lf_t < val - tol] = val - tol
        allowedLineSegmentLength = Uf_t - Lf_t
        tmp = allowedLineSegmentLength / UfLfDiff
        tmp[logical_or(isinf(Lf), isinf(Uf))] = 1e-10 #  (to prevent inf/inf=nan); TODO: rework it
        
        tmp[allowedLineSegmentLength == 0.0] = 1.0 # may be encountered if Uf == Lf, especially for integer probs
        tmp[tmp<1e-300] = 1e-300 # TODO: improve it

        # TODO: for non-exact interval quality increase nlh while moving from 0.5*(Ux-Lx)
        tmp[val - tol > Uf] = 0
        tmp[val + tol < Lf] = 0

    elif isfinite(lb) and not isfinite(ub):
        tmp = (Uf - (lb - tol)) / UfLfDiff
        
        #ind = Lf < lb-tol
        #residual[ind] += lb-Lf[ind]
        
        tmp[logical_and(isinf(Lf), logical_not(isinf(Uf)))] = 1e-10 # (to prevent inf/inf=nan); TODO: rework it
        tmp[isinf(Uf)] = 1-1e-10 # (to prevent inf/inf=nan); TODO: rework it
        
        tmp[tmp<1e-300] = 1e-300 # TODO: improve it
        tmp[tmp>1.0] = 1.0
        
        tmp[lb-tol > Uf] = 0
        
        tmp[lb <= Lf] = 1
        
    elif isfinite(ub) and not isfinite(lb):
        tmp = (ub + tol - Lf ) / UfLfDiff
        
        #ind = Uf > ub+tol
        #residual[ind] += Uf[ind]-ub
        
        tmp[isinf(Lf)] = 1-1e-10 # (to prevent inf/inf=nan);TODO: rework it
        tmp[logical_and(isinf(Uf), logical_not(isinf(Lf)))] = 1e-10 # (to prevent inf/inf=nan); TODO: rework it
        
        tmp[tmp<1e-300] = 1e-300 # TODO: improve it
        tmp[tmp>1.0] = 1.0
        
        tmp[ub+tol < Lf] = 0
        #tmp[ub < Lf] = 0
        
        tmp[ub >= Uf] = 1

    else:
        raise FuncDesignerException('this part of interalg code is unimplemented for double-box-bound constraints yet')
    
    tmp = -log2(tmp)
    tmp[isnan(tmp)] = inf # to prevent some issues in disjunctive cons    
    return tmp

class Constraint(SmoothFDConstraint):
    __hash__ = oofun.__hash__
#    __init__ = SmoothFDConstraint.__init__
    def __init__(self, *args, **kwargs):
        SmoothFDConstraint.__init__(self, *args, **kwargs)
        
class BoxBoundConstraint(SmoothFDConstraint):
    def __init__(self, *args, **kwargs):
        SmoothFDConstraint.__init__(self, *args, **kwargs)
    __hash__ = oofun.__hash__
#    __init__ = SmoothFDConstraint.__init__
