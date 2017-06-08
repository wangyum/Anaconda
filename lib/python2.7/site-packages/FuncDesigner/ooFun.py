# created by Dmitrey
PythonSum = sum
PythonAny = any
PythonMax = max
PythonAll = all

import operator, functools, numpy as np
PythonProd = lambda arg: functools.reduce(operator.mul, arg, 1)
#def PythonProd(arg):
#    print('asdf')
#    return functools.reduce(operator.mul, arg, 1)
from numpy import inf, asfarray, all, any, atleast_2d, zeros, dot, asarray, atleast_1d, \
ones, ndarray, array, nan, vstack, eye, array_equal, isscalar, log, hstack, sum as npSum, prod, \
nonzero, asscalar, zeros_like, \
tile, int8, int16, int32, int64, string_, asanyarray#where

# for PyPy
from FDmisc import where

#from traceback import extract_stack 

try:
    from bottleneck import nanmin, nanmax
except ImportError:
    from numpy import nanmin, nanmax

from expression import getitem_expression, add_expression, mul_expression, neg_expression, div_expression, \
rdiv_expression, pow_expression, rpow_expression
from iqg import iqg

from boundsurf import boundsurf
from boundsurf2 import boundsurf2
    
from FDmisc import FuncDesignerException, Diag, Eye, pWarn, scipyAbsentMsg, scipyInstalled, \
raise_except, DiagonalType, isPyPy, formResolveSchedule, Len, SP_eye, SparseMatrixConstructor, \
isspmatrix, Hstack

from ooPoint import ooPoint
from FuncDesigner.multiarray import multiarray
from derivativeMisc import getDerivativeSelf, mul_aux_d, _D
from Interval import Interval, mul_interval, pow_const_interval, pow_oofun_interval, div_interval, \
add_interval, add_const_interval, neg_interval, defaultIntervalEngine#, rdiv_interval
#import inspect
from baseClasses import OOArray, Stochastic, OOFun
from debugMisc import print_info, fd_trace_id

try:
    from DerApproximator import check_d1
    DerApproximatorIsInstalled = True
except:
    DerApproximatorIsInstalled = False



class oofun(OOFun):
    #TODO:
    #is_oovarSlice = False
    tol = 0.0
    d = None # derivative
    input = None#[] 
    #usedIn =  set()
    is_oovar = False
    #is_stoch = False
    isConstraint = False
    #isDifferentiable = True
    discrete = False
    fixed = False
    _isSum = False
    _isProd = False
    
    stencil = 3 # used for DerApproximator
    
    #TODO: modify for cases where output can be partial
    evals = 0
    same = 0
    same_d = 0
    evals_d  = 0
    
    engine = 'unspecified'
    engine_convexity = nan # nan for undefined, 0 for linear, +1 for convex, -1 for concave
    engine_monotonity = nan
    monotonities = None

    # finite-difference aproximation step
    diffInt = 1.5e-8
    maxViolation = 1e-2
    _unnamedFunNumber = 1
    _lastDiffVarsID = 0
    _lastFuncVarsID = 0
    _lastOrderVarsID = 0
    criticalPoints = lambda *args, **kw: raise_except('bug in FD kernel')
    vectorized = False
#    getDefiniteRange = None
    _neg_elem = None # used in render into quadratic 
    
    ia_surf_level = 0 # 0 or 1 or 2

    _usedIn = 0
    _level = 0
    #_directlyDwasInwolved = False
    _id = 1
    _BroadCastID = 0
    _broadcast_id = 0
    _point_id = 0
    _point_id1 = 0
    _f_key_prev = None
    _f_val_prev = None
    _d_key_prev = None
    _d_val_prev = None
    __array_priority__ = 15# set it greater than 1 to prevent invoking numpy array __mul__ etc
    
    # used in ufuncs
    _lower_domain_bound = -inf
    _upper_domain_bound = inf

    
    pWarn = lambda self, msg: pWarn(msg)
    
    def disp(self, msg): 
        print(msg)
    
    nlh = lambda self, *args, **kw: raise_except("probably you have involved boolean operation on continuous function, that is error")
    lh = lambda self, *args, **kw: raise_except("probably you have involved boolean operation on continuous function, that is error")
    
    # TODO: mb rework it
#    _hasStochasticVariables = lambda self: PythonAny(v.distribution is not None for v in self.Dep)
    
    def __getattr__(self, attr):
        if attr == '__len__':
            # TODO: fix it
            if isPyPy:
                return 1
            else:
                raise AttributeError('using len(oofun) is not possible yet, try using oofun.size instead')
        elif attr == 'dep':
            self.dep = self._getDep()
            return self.dep # dependence oovars
        elif attr == 'Dep':
            self.Dep = set([self]) if self.is_oovar else self.dep
            return self.Dep
        elif attr == 'isUncycled':# TODO: rework it, mb change the word
            self._getDep()
            return self.isUncycled
#        elif attr == 'hasStochasticVariables':
#            self.hasStochasticVariables = self._hasStochasticVariables()
#            return self.hasStochasticVariables
        elif attr == 'isCostly':
            self.isCostly = self.d is None and not self._isSum
            return self.isCostly
        elif attr == 'resolveSchedule':
            formResolveSchedule(self)
            return self.resolveSchedule
        elif attr == 'expr':
            return self.expression()
        elif attr in self.fields:
            from categorical import categoricalAttribute
            return categoricalAttribute(self, attr)
        elif attr != 'size': 
            raise AttributeError('you are trying to obtain incorrect attribute "%s" for FuncDesigner oofun "%s"' %(attr, self.name))
        
        # to prevent creating of several oofuns binded to same oofun.size
        r = oofun(lambda x: asarray(x).size, self, discrete = True, fixed = True, getOrder = lambda *args, **kwargs: 0)
        self.size = r 

        return r

    """                                         Class constructor                                   """

    def __init__(self, fun, input=None, *args, **kwargs):
    #def __init__(self, fun, input=[], *args, **kwargs):
        assert len(args) == 0 #and input is not None
        self.fun = fun
        self.attachedConstraints = set()
        self.args = ()
        self.fields = () # for categorical veriables
        
        
        if 'name' not in kwargs.keys():
            self.name = 'unnamed_oofun_id_%d' % oofun._id
#            oofun._unnamedFunNumber += 1

        #self._broadcast_id = 0

        
        for key, item in kwargs.items():
            #assert key in self.__allowedFields__ # TODO: make set comparison
            setattr(self, key, item)
            
        if isinstance(input, (tuple, list)): 
            self.input = [(elem if isinstance(elem, (oofun, OOArray)) else array(elem, 'float')) for elem in input]
        elif input is not None: 
            self.input = [input]
        else: 
            self.input = [None] # TODO: get rid of None, use input = [] instead

        # TODO: fix it for ooarray!
        if input is not None:
            #levels = [0]
            for elem in self.input: 
                if isinstance(elem, oofun):
                    elem._usedIn += 1
                elif isinstance(elem, OOArray):
                    for Elem in elem.view(ndarray):
                        if isinstance(Elem, oofun):
                            Elem._usedIn += 1
#                    levels.append(elem._level)
#            self._level = max(levels)+1
    
        self._id = oofun._id
        if fd_trace_id.traces(self._id):
            print_info(self)
        fd_trace_id.object[self._id] = self
#        print('oofun id %d' % oofun._id)
        oofun._id += 1 # CHECK: it should be int32! Other types cannot be hash keys!
    
    __hash__ = lambda self: self._id
    
    def expression(self, *args, **kw):
        name = self.name if self.engine == 'unspecified' else self.engine
        Args = [inp.expression() + ', ' if isinstance (inp, oofun) else str(inp) for inp in self.input]
        Args_repr = '(' + ''.join(Args)[:-2] + ')'
        return name + Args_repr

    def attach(self, *args,  **kwargs):
        from constraints import BaseFDConstraint
        if len(kwargs) != 0:
            raise FuncDesignerException('keyword arguments are not implemented for FuncDesigner function "attach"')
        assert len(args) != 0
        Args = args[0] if len(args) == 1 and type(args[0]) in (tuple, list, set) else args
        for arg in Args:
            if not isinstance(arg, BaseFDConstraint):
                raise FuncDesignerException('the FD function "attach" currently expects only constraints')
        self.attachedConstraints.update(Args)
        return self
        
    def removeAttachedConstraints(self):
        self.attachedConstraints = set()    
        
    __repr__ = lambda self: self.name
    
    def _interval_(self, domain, dtype, inputData = None):
        if inputData is None:
            INP = self.input[0] 
            ia_surf_level = 2 #if self.engine_convexity in (-1, 1) else 1
            arg_lb_ub, definiteRange = INP._interval(domain, dtype, ia_surf_level = ia_surf_level)
        else:
            arg_lb_ub, definiteRange = inputData
        
#        INP = self.input[0] 
#        arg_lb_ub, definiteRange = INP._interval(domain, dtype, ia_surf_level = 1)
        
        isBoundsurf = type(arg_lb_ub) in (boundsurf, boundsurf2)
        
        if isBoundsurf and self.engine_convexity is not nan:# and all(isfinite(arg_lb_ub_resolved)):
            return defaultIntervalEngine(arg_lb_ub, self.fun, self.d, 
                                         self.engine_monotonity, self.engine_convexity, 
                                         feasLB = self._lower_domain_bound, feasUB = self._upper_domain_bound)
                                         
        arg_lb_ub_resolved = arg_lb_ub.resolve()[0] if isBoundsurf else arg_lb_ub
        
        
        
        if self.engine_monotonity is not nan:# or self.monotonities is not None:
#            if self.engine_monotonity is nan:
#                assert len(self.monotonities) == 2, 'unimplemented'
            arg_infinum, arg_supremum = arg_lb_ub_resolved#[0], arg_lb_ub_resolved[1]
            if (not isscalar(arg_infinum) and arg_infinum.size > 1) and not self.vectorized:
                raise FuncDesignerException('not implemented for vectorized oovars yet')
            Tmp = self.fun(arg_lb_ub_resolved)
            if isinstance(Tmp, multiarray):
                Tmp = Tmp.view(ndarray)
            if self.engine_monotonity == -1:
                Tmp = Tmp[::-1]
#            elif self.engine_monotonity is nan:
#                # TODO: mb improve it
#                assert not any(logical_and(arg_infinum<0, arg_supremum>0))
#                Tmp = Tmp.sort(axis=0)
            else:
                # func has to be monotonically growing
                assert self.engine_monotonity in (0, 1), \
                'interval computations are unimplemented for the oofun yet'
        else:
            tmp = [arg_lb_ub_resolved] + self.criticalPoints(arg_lb_ub_resolved) 
            Tmp = self.fun(vstack(tmp)) 
            Tmp = vstack((nanmin(Tmp, 0), nanmax(Tmp, 0)))

#        if self.getDefiniteRange is not None:
#            definiteRange = logical_and(definiteRange, self.getDefiniteRange(arg_infinum, arg_supremum))
            
        return Tmp, definiteRange
        
    
    def interval(self, domain, dtype = float, resetStoredIntervals = True, ia_surf_level = 0):
        if type(domain) != ooPoint:
            domain = ooPoint(domain)#, skipArrayCast = True)

        domain.resolveSchedule = {} if domain.surf_preference else self.resolveSchedule
        
        lb_ub, definiteRange = self._interval(domain, dtype, ia_surf_level = 2) 
        if ia_surf_level == 0 and type(lb_ub) in (boundsurf, boundsurf2):
            lb_ub = lb_ub.resolve()[0]
        if ia_surf_level == 1 and type(lb_ub) == boundsurf2:
            lb_ub = lb_ub.to_linear()
        
        # TODO: MB GET RID OF IT?
        if resetStoredIntervals:
            domain.storedIntervals = {}
        if type(lb_ub) == ndarray:
            return Interval(lb_ub[0], lb_ub[1], definiteRange)
        else: # boundsurf
            return lb_ub
    
    def _interval(self, domain, dtype, ia_surf_level = 0):
        tmp = domain.dictOfFixedFuncs.get(self, None)
        if tmp is not None:
            return tile(tmp, (2, 1)), True
        
        tmp = domain._dictOfRedirectedFuncs.get(self, None)
        if tmp is not None:
            return tmp._interval(domain, dtype, ia_surf_level) #if isinstance(tmp, oofun) \
#            else (tile(tmp, (2, 1)), True) if not isinstance(tmp, OOArray)\
#            else raise_except('unimplemented for ooarray yet')
            
        v = domain.modificationVar
        
        r = None
        if v is None or ((v not in self._getDep() or self.is_oovar) and self is not v): 
            r = domain.storedIntervals.get(self, None)

        if r is None and v is not None:
            r = domain.localStoredIntervals.get(self, None)
            
        newComputation = r is None
        if newComputation:
            # TODO: rework it
            r = self._interval_(domain, dtype)                
            if domain.useSave:
                domain.storedIntervals[self] = r 
            if v is not None and self._usedIn > 1:
                domain.localStoredIntervals[self] = r
        if type(r[0]) in (boundsurf, boundsurf2): 
            R, definiteRange = r
            if newComputation:
                Tmp = domain.resolveSchedule.get(self, ())
                if len(Tmp):
                    R = R.exclude(Tmp)
                    if domain.useSave:
                        domain.storedIntervals[self] = (R, definiteRange)#R if type(R) in (boundsurf, boundsurf2) else (R, definiteRange)
                    if v is not None and self._usedIn > 1:
                        domain.localStoredIntervals[self] =  (R, definiteRange)#R if type(R) in (boundsurf, boundsurf2) else (R, definiteRange)
            
            if type(R) in (boundsurf, boundsurf2):
                if ia_surf_level == 1 and R.level == 2:
                    R = R.to_linear()
                elif ia_surf_level == 0:
                    R = R.resolve()[0]
            return R, definiteRange

        return r            
    
    iqg = iqg

    __pos__ = lambda self: self

    # overload "a+b"
    # @checkSizes
    def __add__(self, other):
        if isinstance(other, ndarray) and other.dtype == object:
            from ooarray import ooarray
            return other.view(ooarray)+self
#        if isinstance(other, Stochastic):
#            return other.__add__(self)
        
#        for frame_tuple in inspect.stack():
#            frame = frame_tuple[0]
#            if 'func_code' in dir(frame) and 'func_code' in dir(npSum) and frame.f_code is npSum.func_code:
#                pWarn('''
#                seems like you use numpy.sum() on FuncDesigner object(s), 
#                using FuncDesigner.sum() instead is highly recommended''')              
        
        if not isinstance(other, (oofun, list, ndarray, tuple)) and not isscalar(other):
            raise FuncDesignerException('operation oofun_add is not implemented for the type ' + str(type(other)))
        
        other_is_sum = isinstance(other, oofun) and other._isSum
        
        from overloads import sum
        if self._isSum and other_is_sum:
            return sum(self._summation_elements + other._summation_elements)
        elif self._isSum:
            return sum(self._summation_elements + [other])
        elif other_is_sum:
            return sum(other._summation_elements + [self])
            
        # TODO: check for correct sizes during f, not only f.d 
    
        def aux_d(x, y):
            Xsize, Ysize = Len(x), Len(y)
            if Xsize == 1:
                return ones(Ysize)
            elif Ysize == 1:
                return Eye(Xsize)
            elif Xsize == Ysize:
                return Eye(Ysize) if not isinstance(x, multiarray) else ones(Ysize).view(multiarray)
            else:
                raise FuncDesignerException('for oofun summation a+b should be size(a)=size(b) or size(a)=1 or size(b)=1')        

        if isinstance(other, oofun):
            r = oofun(operator.add, [self, other], d = (lambda x, y: aux_d(x, y), lambda x, y: aux_d(y, x)), _isSum = True)
            r._summation_elements = [self, other]
            r.discrete = self.discrete and other.discrete
            r.getOrder = lambda *args, **kwargs: max((self.getOrder(*args, **kwargs), other.getOrder(*args, **kwargs)))
            r._interval_ = lambda *args, **kw: add_interval(self, other, *args, **kw)
        else:
            # TODO: mb rework it?
            if isscalar(other) and other == 0: return self # sometimes triggers from other parts of FD engine 
            if isinstance(other,  OOArray): return other + self
            if isinstance(other,  ndarray): other = other.copy() 

            r = oofun(lambda a: a+other, self, _isSum=True)
            r._summation_elements = [self, other]
            r.d = lambda x: aux_d(x, other)
            r._getFuncCalcEngine = lambda *args,  **kwargs: self._getFuncCalcEngine(*args,  **kwargs) + other
            r.discrete = self.discrete
            r.getOrder = self.getOrder
            
            Other2 = other if isscalar(other) \
            else other.item if type(other)==ndarray and other.size==1 \
            else tile(other, (2, 1))
#            Other2 = tile(other, (2, 1))
            r._interval_ = lambda *args, **kw: add_const_interval(self, Other2, *args, **kw)
            
            if isscalar(other) or asarray(other).size == 1 or ('size' in self.__dict__ and self.size is asarray(other).size):
                r._D = lambda *args,  **kwargs: self._D(*args,  **kwargs) 
        r.vectorized = True
        r.expression = lambda *args, **kw: add_expression(self, other, *args, **kw)
        return r
    
    __radd__ = __add__
    
    # overload "-a"
    def __neg__(self): 
        if self._neg_elem is not None:
            return self._neg_elem
        if self._isProd:
            # TODO: rework it after bug in numpy prod ([obj,obj]) w|w/o dtype = object will be fixed
            #from overloads import prod as fd_prod
            tmp = -self._prod_elements[-1]
            for elem in self._prod_elements[:-1]:
                tmp = tmp * elem
            return tmp
#            return fd_prod(self._prod_elements[:-1]+[-self._prod_elements[-1]])
        if self._isSum:
            from overloads import sum as FDsum
            # TODO: improve it
            return FDsum([-elem for elem in self._summation_elements])
        r = oofun(operator.neg, self, d = lambda a: -Eye(Len(a)))
        r._neg_elem = self
        r._getFuncCalcEngine = lambda *args,  **kwargs: -self._getFuncCalcEngine(*args,  **kwargs)
        r.getOrder = self.getOrder
        r._D = lambda *args, **kwargs: dict((key, -value) for key, value in self._D(*args, **kwargs).items())
        r.d = raise_except
        r.vectorized = True
        r._interval_ = lambda *args, **kw: neg_interval(self, *args, **kw)
        r.expression =  lambda *args, **kw: neg_expression(self, *args, **kw)
        return r
        
    # overload "a-b"
    __sub__ = lambda self, other: self + (-asfarray(other).copy() if type(other) in (list, tuple, ndarray) else -other)
    __rsub__ = lambda self, other: (asfarray(other).copy() if type(other) in (list, tuple, ndarray) else other) + (-self)

    # overload "a/b"
    def __div__(self, other):
        if isinstance(other, ndarray) and other.dtype == object:
            from ooarray import ooarray
            return other.view(ooarray).__rdiv__(self)
        if isinstance(other, OOArray):
            return other.__rdiv__(self)
        if isinstance(other, list): other = asarray(other)
        if isscalar(other) or type(other) == ndarray:
            return self * (1.0 / other) # to make available using _prod_elements
        if isinstance(other, oofun):
#            return self * (1.0/other)
            r = oofun(operator.truediv, [self, other])
            def aux_dx(x, y):
                # TODO: handle float128
                y = asfarray(y) 
                Xsize, Ysize = x.size, y.size
                if Xsize != 1:
                    assert Xsize == Ysize or Ysize == 1, 'incorrect size for oofun devision'
                if Xsize != 1:
                    if Ysize == 1: 
                        r = Diag(None, size=Xsize, scalarMultiplier = 1.0/y)
                    else:
                        r = Diag(1.0/y)
                else:
                    r = 1.0 / y
                return r                
            def aux_dy(x, y):
                # TODO: handle float128
                x = asfarray(x)
                Xsize, Ysize = Len(x), Len(y)
                r = operator.truediv(-x, y**2)
                if Ysize != 1:
                    assert Xsize == Ysize or Xsize == 1, 'incorrect size for oofun devision'
                    r = Diag(r)
                return r
            r.d = (aux_dx, aux_dy)
            def getOrder(*args, **kwargs):
                order1, order2 = self.getOrder(*args, **kwargs), other.getOrder(*args, **kwargs)
                return order1 if order2 == 0 else inf
            r.getOrder = getOrder
            r._interval_ = lambda *args, **kw: div_interval(self, other, r, *args, **kw)
        else:
            # TODO: mb remove it?
            other = array(other,'float')# TODO: handle float128
            r = oofun(lambda a: operator.truediv(a, other), self, discrete = self.discrete)# TODO: involve sparsity if possible!
            r.getOrder = self.getOrder
            r._getFuncCalcEngine = lambda *args,  **kwargs: self._getFuncCalcEngine(*args,  **kwargs) / other
            #r.d = lambda x: 1.0/other if (isscalar(x) or x.size == 1) else Diag(ones(x.size)/other) if other.size > 1 \
            #else Diag(None, size=x.size, scalarMultiplier=1.0/other)
            r.d = lambda x: 1.0/other if (isscalar(x) or x.size == 1) else Diag(ones(x.size)/other) #if other.size > 1 \
            #else Diag(None, size=x.size, scalarMultiplier=1.0/other)
            # commented code is unreacheble, see r._D definition below for other.size == 1

#            if other.size == 1 or 'size' in self.__dict__ and self.size in (1, other.size):
            if other.size == 1:
                r._D = lambda *args, **kwargs: dict((key, value/other) for key, value in self._D(*args, **kwargs).items())
                r.d = raise_except
            
        # r.discrete = self.discrete and (?)
        #r.isCostly = True
        r.vectorized = True
        r.expression = lambda *args, **kw: div_expression(self, other, *args, **kw)
        return r

    def __rdiv__(self, other):
        
        # without the code it somehow doesn't fork in either Python3 or latest numpy
        #if isinstance(other,  Stochastic) or (isinstance(other, OOArray) and any([isinstance(elem, oofun) for elem in atleast_1d(other)])):
        if isinstance(other, OOArray) and PythonAny(isinstance(elem, oofun) for elem in atleast_1d(other)):
            return other.__div__(self)
        
        other = array(other, 'float') # TODO: sparse matrices handling!
        if other.size == 1:
            other = other.item()
        r = oofun(lambda x: operator.truediv(other, x), self, discrete = self.discrete)
        r.d = lambda x: Diag(operator.truediv(- other, x**2))
        r.monotonities = (-1, -1)
        r.convexities = (-1, 1)
        
        aux_interval_oofun = other * self**-1
        r._interval_ = aux_interval_oofun._interval_
        #r._interval_ = lambda *args, **kw: rdiv_interval(self, r, other, *args, **kw)
        #r.isCostly = True
        def getOrder(*args, **kwargs):
            order = self.getOrder(*args, **kwargs)
            return 0 if order == 0 else inf
        r.getOrder = getOrder
        r.vectorized = True

        r.expression = lambda *args, **kw: rdiv_expression(self, other, *args, **kw)
        return r

    # overload "a*b"
    def __mul__(self, other):
        # TODO: handle case of mul x 1 as copy creation
        if (isscalar(other) or (isinstance(other, ndarray) and other.size == 1 and not isinstance(other,  OOArray))) \
        and other == 1:
            return self

        if isinstance(other, ndarray) and other.dtype == object:
            from ooarray import ooarray
            other = other.view(ooarray)
        if isinstance(other, OOArray):#if isinstance(other, (OOArray, Stochastic)):
            return other.__mul__(self)
        
        isOtherOOFun = isinstance(other, oofun)
        if isOtherOOFun and other._isProd and not self._isProd:
            return other * self
            
        if isinstance(other, list): other = asarray(other)
        
        if self._isProd:
            if isOtherOOFun and other._isProd and not isinstance(other._prod_elements[-1], (oofun, OOArray))\
            and isinstance(self._prod_elements[-1], (oofun, OOArray)):
                return other * self
            
            P1, rest1 = (self._prod_elements, None) \
            if isinstance(self._prod_elements[-1], (oofun, OOArray))\
            else (self._prod_elements[:-1], self._prod_elements[-1])
            P2, rest2 = ([], other) if not isOtherOOFun\
            else ([other], None) if not other._isProd\
            else (other._prod_elements, None) \
            if other._isProd and isinstance(other._prod_elements[-1], (oofun, OOArray))\
            else (other._prod_elements[:-1], other._prod_elements[-1])
            rest = rest1 *  rest2 if rest1 is not None and rest2 is not None\
            else rest1 if rest1 is not None\
            else rest2 if rest2 is not None\
            else None
#            INP = P1+P2
#            if rest is not None: 
#                INP.append(rest)
#            r = oofun(np.prod, INP, vectorized=True)

            if rest1 is not None and rest2 is not None and isOtherOOFun:
                self._fixed_part = rest
                self._unfixed_part = PythonProd(P1+P2)
                r = self._unfixed_part * self._fixed_part
                r._prod_elements = P1+P2+[rest]
                return r
            
            if rest1 is not None:
                # TODO: replace np.prod by fd.prod
                return \
                (other*(PythonProd(self._prod_elements[:-1]) if len(self._prod_elements) > 2 else self._prod_elements[0]))\
                * rest1 \
                if isOtherOOFun else \
                (PythonProd(self._prod_elements[:-1]) if len(self._prod_elements) > 2 else self._prod_elements[0])\
                * (other * rest1)
        
        if isOtherOOFun:
            r = oofun(operator.mul, [self, other])
            r.d = (lambda x, y: mul_aux_d(x, y), lambda x, y: mul_aux_d(y, x))
            r.getOrder = lambda *args, **kw: self.getOrder(*args, **kw) + other.getOrder(*args, **kw)
        else:
            other = other.copy() if isinstance(other,  ndarray) else asarray(other)
            r = oofun(lambda x: x*other, self, discrete = self.discrete)
            r.getOrder = self.getOrder
            r._getFuncCalcEngine = lambda *args,  **kw: other * self._getFuncCalcEngine(*args,  **kw)

            if isscalar(other) or asarray(other).size == 1:  # other may be array-like
                r._D = lambda *args, **kw: \
                dict((key, value * other) for key, value in self._D(*args, **kw).items())
                r.d = raise_except
            else:
                r.d = lambda x: mul_aux_d(x, other)
        
        r._interval_ = lambda *args, **kw: mul_interval(self, other, isOtherOOFun, r, *args, **kw)
        r.vectorized = True
        #r.isCostly = True
        r._isProd = True
        elems1 = [self] if not self._isProd else self._prod_elements
        # TODO: handle ooarray here
        #elems2 = [other] if not isinstance(other, (oofun, OOArray)) or not other._isProd else other._prod_elements
        elems2 = [other] if not isOtherOOFun or not other._isProd else other._prod_elements
        r._prod_elements = elems1 + elems2#[self, other]
        r.expression = lambda *args, **kw:  mul_expression(self, other, *args, **kw)
        if PythonAny(isscalar(elem) for elem in r._prod_elements[:-1]):
            print('got FuncDesigner SP issue, inform developers')
        if np.isscalar(r._prod_elements[-1]) \
        or (type(r._prod_elements[-1]) == ndarray and not isinstance(r._prod_elements[-1], OOArray)):
            r._fixed_part, r._unfixed_part = r._prod_elements[-1], PythonProd(r._prod_elements[:-1])
        else:
            r._fixed_part, r._unfixed_part = None, r
        return r

    __rmul__ = __mul__

    def __pow__(self, other):
        if isinstance(other, ndarray) and other.dtype == object:
            from ooarray import ooarray
            return other.view(ooarray).__rpow__(self)
        if isinstance(other, OOArray):
            return other.__rpow__(self)

        d_x = lambda x, y: \
            (y * x ** (y - 1) if (isscalar(x) or x.size == 1 or isinstance(x, multiarray)) else Diag(y * x ** (y - 1))) if y is not 2 else Diag(2 * x)

        d_y = lambda x, y: x ** y * log(x) if (isscalar(y) or y.size == 1) and not isinstance(x, multiarray) else Diag(x ** y * log(x))
        
        other_is_oofun = isinstance(other, oofun)
        if type(other) == ndarray and other.size == 1:
            other = other.item()
        isInt = isscalar(other) and int(other) == other
        isIntArray = type(other) == ndarray and other.dtype in (int, int8, int16, int32, int64)
        if not other_is_oofun:
            if isscalar(other):
                if type(other) == int: # TODO: handle numpy integer types
                    pass
                    #other = asarray(other, dtype='float')
                else:
                    other = asarray(other, dtype= type(other))# with same type, mb float128
            elif not isinstance(other, ndarray): 
                other = asarray(other, dtype='float' if type(other) in (int, int8, int16, int32, int64) else type(other)).copy()
            
            f = lambda x: asanyarray(x) ** other
            d = lambda x: d_x(x, other)
            input = self
        else:
            f = lambda x, y: asanyarray(x) ** y
            d = (d_x, d_y)
            input = [self, other]
            
        r = oofun(f, input, d = d)
        if not other_is_oofun:
            if not isInt:
                r._lower_domain_bound = 0.0
                r.engine_convexity = -1 if 0 < other < 1 else 1
                
            r.getOrder = lambda *args, **kw: \
            other * self.getOrder(*args, **kw) if isInt and other >= 0 \
            else inf
            r._interval_ = lambda *args, **kw: pow_const_interval(self, r, other, *args, **kw)
            if isscalar(other) or other.size == 1:
                if other > 0 or (isInt and other%2 == 1): 
                    
                    if not isInt:
                        r.engine_monotonity = 1 if other > 0 else -1
                        
                    # is int
                    elif other < 0: 
                        r.monotonities = (-1 if other%2 == 1 else 1, -1)
                    else: # other is int, other > 0
#                        r.monotonities = (-1 if other%2 == 0 else 1, 1)
                        if other % 2 == 0:
                            r.monotonities = (-1, 1)
                        else:
                            r.engine_monotonity = 1
                        
                    r.convexities = ((-1 if isInt and other%2 == 1 else 1 if other > 1 else -1), 
                                     (1 if other > 1 or other < 0 else -1))
                elif isInt and other%2 == 0: #int, other = 2k < 0
                    r.monotonities = (1, -1)
                    r.engine_convexity = -1
                else: # not int,other < 0
                    r.engine_monotonity = -1
                    r.engine_convexity  = -1
        else:
            r._interval_ = lambda *args, **kw: pow_oofun_interval(self, other, *args, **kw)
            
        if other_is_oofun or (not isInt and not isIntArray): 
            r.attach((self>0)('pow_domain_%d'%r._id, tol=-1e-7)) # TODO: if "other" is fixed oofun with integer value - omit this
#        r.isCostly = True
        r.vectorized = True
        if other_is_oofun or not isInt:
            r._lower_domain_bound = 0.0
            
        r.expression = lambda *args, **kw: pow_expression(self, other, *args, **kw)
        return r

    def __rpow__(self, other):
        assert not isinstance(other, oofun)# if failed - check __pow__implementation
        other_is_scalar = isscalar(other)
        if other_is_scalar:
            if type(other) == int: # TODO: handle numpy integer types
                other = float(other)
        elif not isinstance(other, ndarray): 
            other = asarray(other, 'float' if type(other) in (int, int32, int64, int16, int8) else type(other))
        
        f = lambda x: other ** x
        d = lambda x: Diag(other ** x * log(other)) 
        r = oofun(f, self, d=d, vectorized = True)
        if other_is_scalar:
            r.engine_convexity = 1
            r.engine_monotonity = 1 if other > 1 else -1 if other >= 0 else nan
            
        def rpow_interval(r, other, domain, dtype):
            lb_ub, definiteRange = self._interval(domain, dtype, ia_surf_level = 2)
            
            #!!!!! Temporary !!!!

            r1, definiteRange = oofun._interval_(r, domain, dtype)
            if type(lb_ub) == np.ndarray or len(lb_ub.l.d) > 1 or len(lb_ub.u.d) > 1 or len(lb_ub.dep) != 1:
                return r1, definiteRange
            from overloads import exp_b_interval
            return exp_b_interval(log(other) * lb_ub, r1, definiteRange, domain)
            
        r._interval_ = lambda *args, **kw: rpow_interval(r, other, *args, **kw)

        r.expression = lambda *args, **kw: rpow_expression(self, other, *args, **kw)
        return r

    def __xor__(self, other): raise FuncDesignerException('For power of oofuns use a**b, not a^b')
        
    def __rxor__(self, other): raise FuncDesignerException('For power of oofuns use a**b, not a^b')
        
    def __getitem__(self, ind): # overload for oofun[ind]
#        print '1>', ind
        if isinstance(ind, oofun):# NOT IMPLEMENTED PROPERLY YET
            self.pWarn('Slicing oofun by oofun IS NOT IMPLEMENTED PROPERLY YET')
            f = lambda x, _ind: x[_ind]
            def d(x, _ind):
                r = zeros(x.shape)
                r[_ind] = 1
                return r
        elif type(ind) not in (int, int32, int64, int16, int8):
            # Python 3 slice
            return self.__getslice__(ind.start, ind.stop)
        else:
            if not hasattr(self, '_slicesIndexDict'):
                self._slicesIndexDict = {}
            if ind in self._slicesIndexDict:
                return self._slicesIndexDict[ind]
                
            f = lambda x: x[ind] 
            def d(x):
                Xsize = Len(x)
                condBigMatrix = Xsize > 100 
                if condBigMatrix and scipyInstalled:
                    r = SparseMatrixConstructor((1, x.shape[0]))
                    r[0, ind] = 1.0
                else: 
                    if condBigMatrix and not scipyInstalled: 
                        self.pWarn(scipyAbsentMsg)
                    r = zeros_like(x)
                    r[ind] = 1
                return r
        expression = lambda *args, **kw: getitem_expression(self, ind, *args, **kw)
        r = oofun(f, self, d = d, size = 1, getOrder = self.getOrder, expression = expression)
        # TODO: check me!
        # what about a[a.size/2:]?
            
        # TODO: edit me!
#        if self.is_oovar:
#            r.is_oovarSlice = True
        self._slicesIndexDict[ind] = r
        return r
    
    def __getslice__(self, ind1, ind2):# overload for oofun[ind1:ind2]
#        print '>', ind1, ind2
        #TODO: mb check if size is known then use it instead of None?
        if ind1 is None: 
            ind1 = 0
        if ind2 is  None: 
            if 'size' in self.__dict__ and type(self.size) in (int, int8, int16, int32, int64):
                ind2 = self.size
            else:
                raise FuncDesignerException('if oofun.size is not provided then you should provide full slice coords, e.g. x[3:10], not x[3:]')
        assert not isinstance(ind1, oofun) and not isinstance(ind2, oofun), 'slicing by oofuns is unimplemented yet'
        f = lambda x: x[ind1:ind2]
        def d(x):
            condBigMatrix = Len(x) > 100 #and (ind2-ind1) > 0.25*x.size
            if condBigMatrix and not scipyInstalled:
                self.pWarn(scipyAbsentMsg)
            
            if condBigMatrix and scipyInstalled:
                r = SP_eye(ind2-ind1, ind2-ind1)
                if ind1 != 0:
                    m1 = SparseMatrixConstructor((ind2-ind1, ind1))
                    r = Hstack((SparseMatrixConstructor((ind2-ind1, ind1)), r))
                if ind2 != x.size:
                   r = Hstack((r, SparseMatrixConstructor((ind2-ind1, x.size - ind2))))
            else:
                m1 = zeros((ind2-ind1, ind1))
                m2 = eye(ind2-ind1)
                m3 = zeros((ind2-ind1, x.size - ind2))
                r = hstack((m1, m2, m3))
            return r
        expression = lambda *args, **kw: getitem_expression(self, slice(ind1, ind2), *args, **kw)
        r = oofun(f, self, d = d, getOrder = self.getOrder, expression = expression)

        return r
   
    #def __len__(self):
        #return self.size
        #raise FuncDesignerException('using len(obj) (where obj is oovar or oofun) is not possible (at least yet), use obj.size instead')

    def sum(self):
        def d(x):
            #if type(x) == ndarray and x.ndim > 1: raise FuncDesignerException('sum(x) is not implemented yet for arrays with ndim > 1')
            
            #r = ones_like(x) sometimes yields ooarray with dtype object
#            print x.shape
            x = asanyarray(x)
            r = np.ones_like(x) if isPyPy else ones(x.shape, x.dtype if x.dtype != object else int)
            return r
            
        def interval(domain, dtype):
            if type(domain) == ooPoint and domain.isMultiPoint:
                raise FuncDesignerException('interval calculations are unimplemented for sum(oofun) yet')
            lb_ub, definiteRange = self._interval(domain, dtype)
            lb, ub = lb_ub[0], lb_ub[1]
            return vstack((npSum(lb, 0), npSum(ub, 0))), definiteRange
        r = oofun(npSum, self, getOrder = self.getOrder, _interval_ = interval, d=d)
        r.expression = lambda *args, **kw: 'sum(' + self.expression(**kw) + ')'
        return r
    
    def prod(self):
        # TODO: consider using r.isCostly = True
        r = oofun(prod, self)
        # TODO: IMPLEMENT IT 
        #r.getOrder = lambda *args, **kwargs: self.getOrder(*args, **kwargs)*self.size
        def d(x):
            x = asfarray(x) 
            if x.ndim > 1: 
                raise FuncDesignerException('prod(x) is not implemented yet for arrays with ndim > 1')
            ind_zero = where(x==0)[0].tolist()
            ind_nonzero = nonzero(x)[0].tolist()
            numOfZeros = len(ind_zero)
            r = prod(x) / x
            
            if numOfZeros >= 2: 
                r[ind_zero] = 0
            elif numOfZeros == 1:
                r[ind_zero] = prod(x[ind_nonzero])

            return r 
        r.d = d
        r.expression = lambda *args, **kw: 'prod(' + self.expression(**kw) + ')'
        return r


    """                                     Handling constraints                                  """
    
    # TODO: optimize for lb-ub imposed on oovars
    
    # TODO: fix it for discrete problems like MILP, MINLP
    def __gt__(self, other): # overload for >
        from constraints import BoxBoundConstraint, Constraint
        if self.is_oovar and not isinstance(other, (oofun, OOArray)) \
        and not (isinstance(other, ndarray) and str(other.dtype) =='object'):
            r = BoxBoundConstraint(self, lb = other)
        elif isinstance(other, OOArray) or (isinstance(other, ndarray) and str(other.dtype) =='object'):
            r = other.__le__(self)
        else:
            r = Constraint(self - other, lb=0.0) 
            # do not perform check for other == 0, copy should be returned, not self!
        r.descriptor = (self, '>', other)
        Other = str(other) if not isinstance(other, ndarray) or other.size < 5\
        else '[%s %s ... %s %s]' % (other[0], other[1], other[-2], other[-1])
        r.name = self.name + ' >= ' + Other
        def expression(*args, **kw):
            r1 = self.expression(**kw)
            r2 = other.expression(**kw) if isinstance(other, oofun) else Other if kw.get('truncation', False) else str(other)
            return r1 + ' >= '  + r2
        r.expression = expression
        return r

    # overload for >=
    __ge__ = __gt__

    # TODO: fix it for discrete problems like MILP
    def __lt__(self, other): # overload for <
        # TODO:
        #(self.is_oovar or self.is_oovarSlice)
        from constraints import BoxBoundConstraint, Constraint
        if self.is_oovar and not isinstance(other, (oofun, OOArray))\
        and not(isinstance(other, ndarray) and str(other.dtype) =='object'):
            r = BoxBoundConstraint(self, ub = other)
        elif isinstance(other, OOArray) or (isinstance(other, ndarray) and str(other.dtype) =='object'):
            r = other.__ge__(self)
        else:
            r = Constraint(self - other, ub = 0.0) 
            # do not perform check for other == 0, copy should be returned, not self!
        r.descriptor = (self, '<', other)
        Other = str(other) if not isinstance(other, ndarray) or other.size < 5\
        else '[%s %s ... %s %s]' % (other[0], other[1], other[-2], other[-1])
        r.name = self.name + ' <= ' + Other
        def expression(*args, **kw):
            r1 = self.expression(**kw)
            r2 = other.expression(**kw) if isinstance(other, oofun) else Other if kw.get('truncation', False) else str(other)
            return r1 + ' <= ' + r2
        r.expression = expression
        return r            

    # overload for <=
    __le__ = __lt__
  
    def eq(self, other):
        #if type(other) == str and other == '__builtins__': return False
        from constraints import Constraint
        if other is None or other is () or (type(other) == list and len(other) == 0): return False
        if type(other) in (str, string_): 
        #if self.domain is not None and self.domain is not bool and self.domain is not 'bool':
            if 'aux_domain' not in self.__dict__:
                if not self.is_oovar:
                    raise FuncDesignerException('comparing with non-numeric data is allowed for string oovars, not for oofuns')
                self.formAuxDomain()
#            if len(self.domain) != len(self.aux_domain):
#                raise FuncDesignerException('probably you have changed domain of categorical oovar, that is not allowed')

            ind = self.aux_domain.get(other, -1)
            if ind == -1:
                raise FuncDesignerException('compared value %s is absent in oovar %s domain' %(other, self.name))
            
            r = Constraint(self - ind, ub = 0.0, lb = 0.0, tol=0.5)
            if self.is_oovar: r.nlh = lambda Lx, Ux, p, dataType: self.nlh(Lx, Ux, p, dataType, ind)
            Other = other
            
        elif 'startswith' in dir(other): 
            return False # TODO: check it - is it required yet?
        else:
            r = Constraint(self - other, ub = 0.0, lb = 0.0) # do not perform check for other == 0, copy should be returned, not self!
            if self.is_oovar and isscalar(other) and self.domain is not None:
                if self.domain is bool or self.domain is 'bool':
                    if other not in [0, 1]:# and type(other) not in (int, int16, int32, int64):
                        raise FuncDesignerException('bool oovar can be compared with [0,1] only')
                    r.nlh = self.nlh if other == 1.0 else (~self).nlh
                elif self.domain is not int and self.domain is not 'int':# and type(other) in (str, string_):
                    pass
            Other = str(other) if not isinstance(other, ndarray) or other.size < 5\
            else '[%s %s ... %s %s]' %(other[0], other[1], other[-2], other[-1])
        
        r.name = self.name + ' == ' + Other
            
        def expression(*args, **kw):
            r1 = self.expression(**kw)
            r2 = other.expression(**kw) if isinstance(other, oofun) else Other if kw.get('truncation', False) else str(other)
            return r1 + ' == ' + r2
        r.expression = expression
        
        return r  
    
    __eq__ = eq

    """                                             getInput                                              """
    def _getInput(self, *args, **kw):
#        self.inputOOVarTotalLength = 0
        r = []
        for item in self.input:
            tmp = \
            item._getFuncCalcEngine(*args, **kw) if isinstance(item, oofun) \
            else item(*args, **kw) if isinstance(item, OOArray) \
            else item
            
            r.append(asarray(tmp) if type(tmp) in (list, tuple) else tmp)
            
        return tuple(r)

    """                                                getDep                                             """
    def _getDep(self):
        # returns Python set of oovars it depends on
        if 'dep' in self.__dict__:
            return self.dep
        elif self.input is None:
            self.dep = None
        else:
            if type(self.input) not in (list, tuple) and not isinstance(self.input, OOArray):
                self.input = [self.input]
            
            r_oovars = []
            r_oofuns = []
            isUncycled = True
            Tmp = set()
            for Elem in self.input:
                if isinstance(Elem, OOArray):
                    for _elem in Elem:
                        if isinstance(_elem, oofun):
                            Tmp.add(_elem)
                            
            for Elem in (list(Tmp) + self.input):
                if not isinstance(Elem, oofun): continue
                if Elem.is_oovar:
                    r_oovars.append(Elem)
                    continue
                
                tmp = Elem._getDep()
                if not Elem.isUncycled: isUncycled = False
                if tmp is None or len(tmp)==0: continue # TODO: remove None, use [] instead
                r_oofuns.append(tmp)
            r = set(r_oovars)

            # Python 2.5 set.update fails on empty input
            if len(r_oofuns)!=0: r.update(*r_oofuns)
            if len(r_oovars) + sum([len(elem) for elem in r_oofuns]) != len(r):
                isUncycled = False
            self.isUncycled = isUncycled            
            
            self.dep = r    
            
        return self.dep


    """                                                getFunc                                             """
    def _getFunc(self, *args, **kwargs):
        Args = args
        if len(args) == 0 and len(kwargs) == 0:
            raise FuncDesignerException('at least one argument is required')
        if len(args) != 0:
            if type(args[0]) != str:
                assert not isinstance(args[0], oofun), "you can't invoke oofun on another one oofun"
                x = args[0]
                if type(x) == dict: 
                    x = ooPoint(x)
                    Args = (x,) + args[1:]
                if self.is_oovar:
                    return self._getFuncCalcEngine(*Args, **kwargs)
            else:
                self.name = args[0]
                return self
        else:
            for fn in ['name', 'size', 'tol']:
                if fn in kwargs:
                    setattr(self, fn, kwargs[fn])
            return self
        
        if hasattr(x, 'probType') and x.probType == 'MOP':# x is MOP result struct
            s = 'evaluation of MOP result on arguments is unimplemented yet, use r.solutions'
            raise FuncDesignerException(s)

        
        return self._getFuncCalcEngine(*Args, **kwargs)


    def _getFuncCalcEngine(self, *args, **kwargs):
        x = args[0]
        
        # chenges
        tmp = getattr(x, 'dictOfFixedFuncs', {})
        Tmp = tmp.get(self, None)
        if Tmp is not None:
            return Tmp
        tmp = getattr(x, '_dictOfRedirectedFuncs', {})
        Tmp = tmp.get(self, None)
        if Tmp is not None:
            return Tmp._getFuncCalcEngine(*args, **kwargs)
        #changes end
        
        dep = self._getDep()
        
        CondSamePointByID = True if type(x) == ooPoint and not x.isMultiPoint and self._point_id == x._id else False

        fixedVarsScheduleID = kwargs.get('fixedVarsScheduleID', -1)
        fixedVars = kwargs.get('fixedVars', None)
        Vars = kwargs.get('Vars', None) 
        
        sameVarsScheduleID = fixedVarsScheduleID == self._lastFuncVarsID 
        rebuildFixedCheck = not sameVarsScheduleID
        if fixedVarsScheduleID != -1: self._lastFuncVarsID = fixedVarsScheduleID
        
        if rebuildFixedCheck:
            self._isFixed = (fixedVars is not None and dep.issubset(fixedVars)) or (Vars is not None and dep.isdisjoint(Vars))
        
        if isinstance(x, ooPoint) and x.isMultiPoint:
            cond_same_point = False
        else:
            cond_same_point = CondSamePointByID or \
            (self._f_val_prev is not None and \
            (self._isFixed or 
            (self.isCostly and  
            PythonAll(array_equal((x if isinstance(x, dict) else x.xf)[elem], self._f_key_prev[elem]) for elem in (dep & set((x if isinstance(x, dict) else x.xf).keys()))))))
            
        if cond_same_point:
            self.same += 1
            tmp =  self._f_val_prev
            return tmp.copy() if isinstance(tmp, (ndarray, Stochastic)) else tmp 
            
        self.evals += 1
        
        #TODO: add condition "and self in x._p.dictOfLinearFuncs" instead of self._order == 1
        #use_line_points = hasattr(x,'_p') and x._p.solver.useLinePoints and self._order == 1
#        if use_line_points:
#            _linePointDescriptor = getattr(x, '_linePointDescriptor', None)
#            if _linePointDescriptor is not None:
#                #point1, alp, point2 = _linePointDescriptor
#                alp = _linePointDescriptor
#                r1, r2 = self._p._firstLinePointDict[self], self._p._secondLinePointDict[self]
#                #assert r1 is not None and r2 is not None
#                return r1 * (1-alp) + r2 * alp
        
        if type(self.args) != tuple:
            self.args = (self.args, )
            
        Input = self._getInput(*args, **kwargs) 
        
#        if not isinstance(x, ooPoint) or not x.isMultiPoint or (self.vectorized and not any([isinstance(inp, Stochastic) for inp in Input])):
        if not PythonAny(isinstance(inp, multiarray) for inp in Input) or self.vectorized:
            if self.args != ():
                Input += self.args
            Tmp = self.fun(*Input)
            if isinstance(Tmp, (list, tuple)):
                tmp = hstack(Tmp) if len(Tmp) > 1 else Tmp[0]
            else:
                tmp = Tmp
        else:
            if hasattr(x, 'N'):
                N = x.N
            else:
                # TODO: fix it for x.values() is Stochastic
                N = PythonMax([1] + [inp.size for inp in Input if type(inp) == ndarray])

            Temp = [inp.tolist() if isinstance(inp, multiarray) else [inp]*N for inp in Input]
            inputs = zip(*Temp)
            
            # Check it!
            Tmp = [self.fun(*inp) if self.args == () else self.fun(*(inp + self.args)) for inp in inputs]
            if len(Tmp) == 1:
                tmp = Tmp[0]
            else:
                tmp = array([elem for elem in Tmp]).view(multiarray)
        
        #if self._c != 0.0: tmp += self._c
        
        #self.outputTotalLength = ([asarray(elem).size for elem in self.fun(*Input)])#self.f_val_prev.size # TODO: omit reassigning
        
        #!! TODO: handle case tmp is multiarray of Stochastic
        if isinstance(tmp, Stochastic):
            if 'xf' in x.__dict__:
                maxDistributionSize = getattr(x.xf, 'maxDistributionSize', 0)
            else:
                maxDistributionSize = getattr(x, 'maxDistributionSize', 0)
            if maxDistributionSize == 0:
                s = '''
                    if one of function arguments is stochastic distribution 
                    without resolving into quantified value 
                    (e.g. uniform(-10,10) instead of uniform(-10,10, 100), 100 is number of point to emulate)
                    then you should evaluate the function 
                    onto oopoint with assigned parameter maxDistributionSize'''
                raise FuncDesignerException(s)
            if tmp.size > maxDistributionSize:
                tmp.reduce(maxDistributionSize)
            tmp.maxDistributionSize = maxDistributionSize
        
        
        if ((type(x) == ooPoint and not x.isMultiPoint) and not (isinstance(tmp, ndarray) and type(tmp) != ndarray))\
        or self._isFixed:# or self.isCostly:

            # TODO: rework it (for input with ooarays)
            try:
                t1 = dict((elem, (x if isinstance(x, dict) else x.xf)[elem]) for elem in dep) if self.isCostly else None
                #t1 = dict([(elem, copy((x if isinstance(x, dict) else x.xf)[elem])) for elem in dep]) if self.isCostly else None
                if t1 is not None:
                    t2 = tmp.copy() if isinstance(tmp, (ndarray, Stochastic)) else tmp
                    self._f_key_prev, self._f_val_prev = t1, t2
                    if type(x) == ooPoint: 
                        self._point_id = x._id                
            except:
                pass
            
        r = tmp
#        if use_line_points:
#            self._p._currLinePointDict[self] = r
#        if fixedVarsScheduleID != -1: 
#            self._lastSize = tmp.size
        return r


    """                                                getFunc                                             """
    __call__ = _getFunc


    """                                              derivatives                                           """
    def D(self, x, Vars=None, fixedVars = None, resultKeysType = 'vars', useSparse = False, exactShape = False, fixedVarsScheduleID = -1):
        
        # resultKeysType doesn't matter for the case isinstance(Vars, oovar)
        if Vars is not None and fixedVars is not None:
            raise FuncDesignerException('No more than one argument from "Vars" and "fixedVars" is allowed for the function')
        #assert type(Vars) != ndarray and type(fixedVars) != ndarray
        if type(x) == dict: x = ooPoint(x)
        initialVars = Vars
        #TODO: remove cloned code
        if Vars is not None:
            if type(Vars) in [list, tuple]:
                Vars = set(Vars)
            elif isinstance(Vars, oofun):
                if not Vars.is_oovar:
                    raise FuncDesignerException('argument Vars is expected as oovar or python list/tuple of oovar instances')
                Vars = set([Vars])
        if fixedVars is not None:
            if type(fixedVars) in [list, tuple]:
                fixedVars = set(fixedVars)
            elif isinstance(fixedVars, oofun):
                if not fixedVars.is_oovar:
                    raise FuncDesignerException('argument fixedVars is expected as oovar or python list/tuple of oovar instances')
                fixedVars = set([fixedVars])
        r = self._D(x, fixedVarsScheduleID, Vars, fixedVars, useSparse = useSparse)
        r = dict((key, (val if type(val)!=DiagonalType else val.resolve(useSparse))) for key, val in r.items())
        is_oofun = isinstance(initialVars, oofun)
        if is_oofun and not initialVars.is_oovar:
            # TODO: handle it with input of type list/tuple/etc as well
            raise FuncDesignerException('Cannot perform differentiation by non-oovar input')

        if resultKeysType == 'names':
            raise FuncDesignerException("""This possibility is out of date, 
            if it is still present somewhere in FuncDesigner doc inform developers""")
        elif resultKeysType == 'vars':
            rr = {}
            #!!! TODO: mb remove the cycle!!!!
            for oov, tmp in r.items():
                if (fixedVars is not None and oov in fixedVars) or (Vars is not None and oov not in Vars):
                    continue
                if useSparse == False and hasattr(tmp, 'toarray'): tmp = tmp.toarray()
                if not isspmatrix(tmp) and not isscalar(tmp):
                    if tmp.size == 1: 
                        tmp = tmp.item()
                    elif not exactShape and min(tmp.shape) == 1: 
                        tmp = tmp.flatten()
                rr[oov] = tmp
            return rr if not is_oofun else rr[initialVars]
        else:
            raise FuncDesignerException('Incorrect argument resultKeysType, should be "vars" or "names"')

    _getDerivativeSelf = getDerivativeSelf
    
    ##########################
    # !! May be overloaded by some oofuns,
    # thus cannot be moved from here
    _D = _D
    ##########################

    def D2(self, x):
        raise FuncDesignerException('2nd derivatives for oofuns are not implemented yet')

    def check_d1(self, point):
        if self.d is None:
            self.disp('Error: no user-provided derivative(s) for oofun ' + self.name + ' are attached')
            return # TODO: return non-void result
        separator = 75 * '*'
        self.disp(separator)
        assert type(self.d) != list
        val = self(point)
        input = self._getInput(point)
        ds= self._getDerivativeSelf(point, fixedVarsScheduleID = -1, Vars=None,  fixedVars=None)
        self.disp(self.name + ': checking user-supplied gradient')
        self.disp('according to:')
        self.disp('    diffInt = ' + str(self.diffInt)) # TODO: ADD other parameters: allowed epsilon, maxDiffLines etc
        self.disp('    |1 - info_user/info_numerical| < maxViolation = '+ str(self.maxViolation))        
        j = -1
        for i in range(len(self.input)):
            if len(self.input) > 1: self.disp('by input variable number ' + str(i) + ':')
            if isinstance(self.d, tuple) and self.d[i] is None:
                self.disp('user-provided derivative for input number ' + str(i) + ' is absent, skipping the one;')
                self.disp(separator)
                continue
            if not isinstance(self.input[i], oofun):
                self.disp('input number ' + str(i) + ' is not oofun instance, skipping the one;')
                self.disp(separator)
                continue
            j += 1
            check_d1(lambda *args: self.fun(*args), ds[j], input, \
                 func_name=self.name, diffInt=self.diffInt, pointVal = val, args=self.args, \
                 stencil = max((3, self.stencil)), maxViolation=self.maxViolation, varForCheck = i)

    def getOrder(self, Vars=None, fixedVars=None, fixedVarsScheduleID=-1):
        #is overloaded by several functions like add, mul etc
        
        # TODO: improve it wrt fixedVarsScheduleID
        # returns polinomial order of the oofun
        if isinstance(Vars, oofun): Vars = set([Vars])
        elif Vars is not None and type(Vars) != set: Vars = set(Vars)
        
        if isinstance(fixedVars, oofun): fixedVars = set([fixedVars])
        elif fixedVars is not None and type(fixedVars) != set: fixedVars = set(fixedVars)
        
        sameVarsScheduleID = fixedVarsScheduleID == self._lastOrderVarsID 
        rebuildFixedCheck = not sameVarsScheduleID
        if fixedVarsScheduleID != -1: self._lastOrderVarsID = fixedVarsScheduleID
        
        if rebuildFixedCheck:
            # ajust new value of self._order wrt new free/fixed vars schedule
            if self.fixed: 
                self._order = 0
            elif self.is_oovar:
                if fixedVars is not None and Vars is not None:
                    isFixed = (self in fixedVars) if len(fixedVars) < len(Vars) else (self not in Vars)
                else:
                    isFixed = (fixedVars is not None and self in fixedVars) or (Vars is not None and self not in Vars)
                self._order = 0 if isFixed else 1
            else:
                self._order = 0
                for inp in self.input:
                    if isinstance(inp, oofun):
                        if inp.getOrder(Vars, fixedVars, fixedVarsScheduleID=fixedVarsScheduleID) != 0:
                            self._order = inf
                            break
                    elif isinstance(inp, OOArray):
                        for elem in inp.view(ndarray):
                            if isinstance(elem, oofun) and elem.getOrder(Vars, fixedVars, fixedVarsScheduleID=fixedVarsScheduleID) != 0:
                                self._order = inf
                                break
        return self._order
    
    # TODO: should broadcast return non-void result?
    def _broadcast(self, func, useAttachedConstraints, *args, **kwargs):
        if self._broadcast_id == oofun._BroadCastID: 
            return # already done for this one
            
        self._broadcast_id = oofun._BroadCastID
        
        #TODO: implement cond_skip to quit from a brench of the reqursive process 
        
        # TODO: possibility of reverse order?
        elems = self.input if not self._isSum else self._summation_elements
        if elems is not None:
            for inp in elems: 
                if not isinstance(inp, oofun): continue#TODO: check ooarray
                inp._broadcast(func, useAttachedConstraints, *args, **kwargs)
        if useAttachedConstraints:
            for c in self.attachedConstraints:
                if isinstance(c, OOArray):
                    for elem in c.view(ndarray):
                        if isinstance(elem, oofun): # TODO: handle case of ooarray
                            elem._broadcast(func, useAttachedConstraints, *args, **kwargs)
                elif isinstance(c, oofun):
                    c._broadcast(func, useAttachedConstraints, *args, **kwargs)
                else:
                    pass# TODO: mb another action(s)?
        func(self, *args, **kwargs)
        
    def uncertainty(self, point, deviations, actionOnAbsentDeviations='warning'):
        ''' 
        result = oofun.uncertainty(point, deviations, actionOnAbsentDeviations='warning')
        point and deviations should be Python dicts of pairs (oovar, value_for_oovar)
        actionOnAbsentDeviations = 
        'error' (raise FuncDesigner exception) | 
        'skip' (treat as fixed number with zero deviation) |
        'warning' (print warning, treat as fixed number) 
        
        Sparse large-scale examples haven't been tested,
        we could implement and test it properly on demand
        '''
        dep = self._getDep()
        dev_keys = set(deviations.keys())
        set_diff = dep.difference(dev_keys)
        nAbsent = len(set_diff)
        if actionOnAbsentDeviations != 'skip':
            if len(set_diff) != 0:
                if actionOnAbsentDeviations == 'warning':
                    pWarn('''
                    dict of deviations miss %d variables (oovars): %s;
                    they will be treated as fixed numbers with zero deviations
                    ''' % (nAbsent, list(set_diff)))
                else:
                    raise FuncDesignerException('dict of deviations miss %d variable(s) (oovars): %s' % (nAbsent, list(set_diff)))
        
        d = self.D(point, exactShape=True) if nAbsent == 0 else self.D(point, fixedVars = set_diff, exactShape=True)
        tmp = [dot(val, (deviations[key] if isscalar(deviations[key]) else asarray(deviations[key]).reshape(-1, 1)))**2 for key, val in d.items()]
        tmp = [asscalar(elem) if isinstance(elem, ndarray) and elem.size == 1 else elem for elem in tmp]
        r = atleast_2d(hstack(tmp)).sum(1)
        return r ** 0.5
        
    # For Python 3:
    __rtruediv__ = __rdiv__
    __truediv__ = __div__
    
    def IMPLICATION(*args, **kw): 
        raise FuncDesignerException('oofun.IMPLICATION is temporary disabled, use ifThen(...) or IMPLICATION(...) instead')
    
    """                                             End of class oofun                                             """


def atleast_oofun(arg):
    if isinstance(arg, oofun):
        return arg
    elif hasattr(arg, 'copy'):
        tmp = arg.copy()
        return oofun(lambda *args, **kwargs: tmp, input = None, getOrder = lambda *args,  **kwargs: 0, discrete=True)#, isConstraint = True)
    elif isscalar(arg):
        tmp = array(arg, 'float')
        return oofun(lambda *args, **kwargs: tmp, input = None, getOrder = lambda *args,  **kwargs: 0, discrete=True)#, isConstraint = True)
    else:
        #return oofun(lambda *args, **kwargs: arg(*args,  **kwargs), input=None, discrete=True)
        raise FuncDesignerException('incorrect type for the function _atleast_oofun')

