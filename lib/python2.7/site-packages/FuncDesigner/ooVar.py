# created by Dmitrey
#PythonAll = all
from numpy import asarray, empty, inf, any, array, \
asfarray, isscalar, ndarray, int16, int32, int64, float64, tile, vstack, searchsorted, \
logical_or, where, asanyarray, arange, log2, logical_and, ceil, string_, atleast_1d
import numpy as np

from FDmisc import FuncDesignerException, isPyPy
from ooFun import oofun
from logic import AND, OR, NOT, EQUIVALENT
from BooleanOOFun import BooleanOOFun
#from FuncDesigner import IMPLICATION
from ooarray import ooarray
from baseClasses import Stochastic

from boundsurf import boundsurf, surf

f_none = lambda *args, **kw: None
One = array(1.0)
Zero = array(0.0) ## TODO: mb use 1-d array to improve indexation
class oovar(oofun):
    is_oovar = True
    domain = None
    lb = -inf
    ub = inf
    #shape = nan
    #fixed = False
    #initialized = False
    _unnamedVarNumber = 1#static variable for oovar class
    __hash__ = oofun.__hash__

    def __init__(self, name=None, *args, **kwargs):
        if len(args) > 0: raise FuncDesignerException('incorrect args number for oovar constructor')
        if name is None:
            self.name = 'unnamed_oovar_with_oofun_id_%d' % oofun._id
#            oovar._unnamedVarNumber += 1
#            self.name = 'unnamed_' + str(oovar._unnamedVarNumber)
        else:
            kwargs['name'] = name
        oofun.__init__(self, f_none, *args, **kwargs)
    
    expression = lambda self, *args, **kw: self.name
    
    def _interval_(self, domain, dtype = float64):
        if self in domain.resolveSchedule:
            tmp = domain.get(self, None)
            if tmp is None: 
                Tmp = getattr(domain, '_dictOfStochVars', {})
                tmp = Tmp.get(self, None)
                return None if tmp is None else (tile(yield_stochastic(tmp, domain, self), (2, 1)), True)
                    
            if isinstance(tmp, ndarray) or isscalar(tmp): # thus variable value is fixed for this calculation
                tmp = asarray(tmp, dtype)
                return tile(tmp, (2, 1)), True
            infinum, supremum = tmp
            
            #prev
            #return asarray(vstack((infinum, supremum)), dtype), True
            #new, works faster in CPython
            r = empty((2, asarray(infinum).size), dtype)
            r[0] = infinum
            r[1] = supremum
            return r, True
        else:
            S = surf({self: One}, Zero)
            return boundsurf(S, S, True, domain), True
    
    def _getFuncCalcEngine(self, x, **kwargs):
        if hasattr(x, 'xf'):
            #return x.xf[self]
            if x.probType == 'MOP':
                s = 'evaluation of MOP result on arguments is unimplemented yet, use r.solutions'
                raise FuncDesignerException(s)
            return self._getFuncCalcEngine(x.xf, **kwargs) # essential for SP
        r = x.get(self, None)
        if r is not None: 
            if isinstance(r, Stochastic):
                r = yield_stochastic(r, x, self)
            return r
        r = x.get(self.name, None)
        if r is not None: 
            return r
        Tmp = getattr(x, '_dictOfStochVars', {})
        r = Tmp.get(self, None)
        if r is not None:
            r = yield_stochastic(r, x, self)
            return r
            
        # check for fixed oovars
        dictOfFixedFuncs = getattr(x, 'dictOfFixedFuncs', {})
        r = dictOfFixedFuncs.get(self, None)
        if r is not None:
            return r
        
        s = '''for oovar %s the point involved doesn't contain 
        neither name nor the oovar instance. 
        Maybe you try to get function value or derivative 
        in a point where value for an oovar is missing
        or run optimization problem 
        without setting initial value for this variable in start point
        ''' % self.name
        raise FuncDesignerException(s)
        
        
    def nlh(self, Lx, Ux, p, dataType, other=None):
        T0, res, DefiniteRange = get_P(self, Lx, Ux, p, dataType, other, goal_is_nlh = True)
        if type(T0) == bool:
            assert len(res) == 0
            return T0, {}, DefiniteRange
        else:
            return T0, {self: res}, DefiniteRange

    def lh(self, Lx, Ux, p, dataType, other=None):
        #print('lh')
        T0, res, DefiniteRange = get_P(self, Lx, Ux, p, dataType, other, goal_is_nlh = False)
        if type(T0) == bool:
            assert len(res) == 0
            return T0, {}, DefiniteRange
        else:
            return T0, {self: res}, DefiniteRange        

    __and__ = AND
    __or__ = OR
    #implication = IMPLICATION
    __invert__ = NOT
    __ne__ = lambda self, arg: NOT(self==arg)
    def __eq__(self, other): 
        if type(other) == str and other =='__builtins__': return False  
        if (self.domain is bool or self.domain is 'bool') and isinstance(other, (oovar, BooleanOOFun)):
            return EQUIVALENT(self, other)
        else:
            return oofun.__eq__(self, other)
    
    def formAuxDomain(self, sort = True):
        if 'aux_domain' in self.__dict__: return
        d = self.domain
#        if d.dtype.type not in [string_, unicode, str]:
#            raise FuncDesignerException('to compare string with oovar latter should have domain of string type')
        if type(d[0]) in (str, string_):
            d = dict((elem, i) for i, elem in enumerate(d))
            D = int(2 ** ceil(log2(len(d))))
            self.reverse_aux_domain = dict((i, elem) for i, elem in enumerate(self.domain))
        elif sort:    
            d = asanyarray(d)
            if any(d[1:] > d[:-1]):
#                if type(d) == tuple:
#                    d = list(d)
                d.sort()
            #self.ub = d.size - 1
            
            D = int(2 ** ceil(log2(len(atleast_1d(d)))))
        else:
            d = asanyarray(d)
        # atleast_1d - for domain from 1 element if it will be somewhere generated and obtained here
        
        self.domain, self.aux_domain = arange(D), d    
#        self.domainSortOrder = \
#        1 if PythonAll(d[i] <= d[i+1] for i in range(D-1)) else \
#        -1 if PythonAll(d[i] >= d[i+1] for i in range(D-1)) else\
#        0

#        if isinstance(x, dict):
#            tmp = x.get(self, None)
#            if tmp is not None:
#                return tmp #if type(tmp)==ndarray else asfarray(tmp)
#            elif self.name in x:
#                return asfarray(x[self.name])
#            else:
#                s = 'for oovar ' + self.name + \
#                " the point involved doesn't contain niether name nor the oovar instance. Maybe you try to get function value or derivative in a point where value for an oovar is missing"
#                raise FuncDesignerException(s)
#        elif hasattr(x, 'xf'):
#            # TODO: possibility of squeezing
#            return x.xf[self]
#        else:
#            raise FuncDesignerException('Incorrect data type (%s) while obtaining oovar %s value' %(type(x), self.name))
        
        
#    def _initialize(self, p):
#
#        """                                               Handling size and shape                                               """
#        sizes = set()
#        shapes = set()
#        for fn in ['v0', 'lb', 'ub']:
#            if hasattr(self, fn):
#                setattr(self, fn, asarray(getattr(self, fn)))
#                shapes.add(getattr(self, fn).shape)
#                sizes.add(getattr(self, fn).size)
#        if self.shape is not nan: 
#            shapes.add(self.shape)
#            sizes.add(prod(self.shape))
#        if self.size is not nan: sizes.add(self.size)
#        #if len(shapes) > 1: p.err('for oovar fields (if present) lb, ub, v0 should have same shape')
#        #elif len(shapes) == 1: self.shape = shapes.pop()
#        if len(shapes) >= 1: self.shape = prod(shapes.pop())
#        
#        if len(sizes) > 1: p.err('for oovar fields (if present) lb, ub, v0 should have same size')
#        elif len(sizes)==1 : self.size = sizes.pop()
#
#        if self.size is nan: self.size = asarray(self.shape).prod()
#        if self.shape is nan:
#            assert isfinite(self.size)
#            self.shape = (self.size, )
#        
#
#        """                                                     Handling init value                                                   """
##        if not hasattr(self, 'lb'):
##            self.lb = empty(self.shape)
##            self.lb.fill(-inf)
##        if not hasattr(self, 'ub'):
##            self.ub = empty(self.shape)
##            self.ub.fill(inf)
##        if any(self.lb > self.ub):
##            p.err('lower bound exceeds upper bound, solving impossible')
#        if not hasattr(self, 'v0'):
#            #p.warn('got oovar w/o init value')
#            v0 = zeros(self.shape)
#
#            ind = isfinite(self.lb) & isfinite(self.ub)
#            v0[ind] = 0.5*(self.lb[ind] + self.ub[ind])
#
#            ind = isfinite(self.lb) & ~isfinite(self.ub)
#            v0[ind] = self.lb[ind]
#
#            ind = ~isfinite(self.lb) & isfinite(self.ub)
#            v0[ind] = self.ub[ind]
#
#            self.v0 = v0
#            
#        self.initialized = True
        
        
def oovars(*args, **kw):
    if isPyPy:
        raise FuncDesignerException('''
        for PyPy using oovars() is impossible yet. 
        You could use oovar(size=n), also 
        you can create list or tuple of oovars in a cycle, e.g.
        a = [oovar('a'+str(i)) for i in range(100)]
        but you should ensure you haven't operations like k*a or a+val in your code, 
        it may work in completely different way (e.g. k*a will produce Python list of k a instances)
        ''')
    lb = kw.pop('lb', None)
    ub = kw.pop('ub', None)
    
    if len(args) == 1:
        if type(args[0]) in (int, int16, int32, int64):
            r = ooarray([oovar(**kw) for i in range(args[0])])
        elif type(args[0]) in [list, tuple]:
            r = ooarray([oovar(name=args[0][i], **kw) for i in range(len(args[0]))])
        elif type(args[0]) == str:
            r = ooarray([oovar(name=s, **kw) for s in args[0].split()])
        else:
            raise FuncDesignerException('incorrect args number for oovars constructor')
    else:
        r = ooarray([oovar(name=args[i], **kw) for i in range(len(args))])
        
    if lb is not None:
        if np.isscalar(lb) or (isinstance(lb, np.ndarray) and lb.size == 1):
            for v in r.view(np.ndarray):
               v.lb = lb
        else:
            assert type(lb) in (list, tuple, ndarray)
            for i, v in enumerate(r):
               v.lb = lb[i]

    if ub is not None:
        if np.isscalar(ub) or (isinstance(ub, np.ndarray) and ub.size == 1):
            for v in r.view(np.ndarray):
               v.ub = ub
        else:
            assert type(ub) in (list, tuple, ndarray)
            for i, v in enumerate(r):
               v.ub = ub[i]
               
    r._is_array_of_oovars = True
    
    return r



def get_P(v, Lx, Ux, p, dataType, other=None, goal_is_nlh = True):
    DefiniteRange = True
    d = v.domain
    if d is None:
        raise FuncDesignerException('probably you are invoking boolean operation on continuous oovar')
    if d is int or d is 'int':
        raise FuncDesignerException('probably you are invoking boolean operation on non-boolean oovar')
    inds = p._oovarsIndDict.get(v, None)
    m = Lx.shape[0]
    if inds is None:
        # this oovar is fixed
        res = {}
        if v.domain is bool or v.domain is 'bool':
            if goal_is_nlh:
                T0 = True if p._x0[v] == 1 else False # 0 or 1
            else:
                T0 = False if p._x0[v] == 1 else True # 0 or 1
        else:
            assert other is not None, 'bug in FD kernel: called nlh with incorrect domain type'
            if goal_is_nlh:
                T0 = False if p._x0[v] != other else True
            else:
                T0 = False if p._x0[v] == other else True
        return T0, res, DefiniteRange
        #raise FuncDesignerException('probably you are trying to get nlh of fixed oovar, this is unimplemented in FD yet')
    ind1, ind2 = inds
    assert ind2-ind1 == 1, 'unimplemented for oovars of size > 1 yet'
    lx, ux = Lx[:, ind1], Ux[:, ind1]
    
    if d is bool or d is 'bool':
        T0 = empty(m)
        if goal_is_nlh:
            T0.fill(inf)
            T0[ux != lx] = 1.0 # lx = 0, ux = 1 => -log2(0.5) = 1
            T0[lx == 1.0] = 0.0 # lx = 1 => ux = 1 => -log2(1) = 0

            T2 = vstack((where(lx == 1, 0, inf), where(ux == 1, 0, inf))).T
        else:
            T0.fill(0)
            T0[ux != lx] = 1.0
            T0[lx == 1.0] = inf
            
            T2 = vstack((where(lx == 1, inf, 0), where(ux == 1, inf, 0))).T
    else:
        assert other is not None, 'bug in FD kernel: called nlh with incorrect domain type'
        mx = 0.5 * (lx + ux) 

       
        prev = 0
        if prev:
            ind = logical_and(mx==other, lx != ux)
            if any(ind):
                p.pWarn('seems like a categorical variables bug in FuncDesigner kernel, inform developers')
                
#                mx[ind] += 1e-15 + 1e-15*abs(mx[ind])            
            I = searchsorted(d, lx, 'right') -  1
            J = searchsorted(d, mx, 'right') - 1
            #assert np.all(searchsorted(d, mx, 'right') == searchsorted(d, mx, 'left'))
            K = searchsorted(d, ux, 'right') - 1
            
            D0, D1, D2 = d[I], d[J], d[K]
            
            d1, d2 = D0, D1
    #        if goal_is_nlh:
            tmp1 = asfarray(J-I+1+where(d2==other, 1, 0))
            tmp1[logical_or(other<d1, other>d2)] = inf
    #        else:
    #            tmp1 = asfarray(J-I+where(d2==other, 0, 1))
    #            tmp1[logical_or(other<d1, other>d2)] = 0
            
            d1, d2 = D1, D2
    #        if goal_is_nlh:
            tmp2 =  asfarray(K-J+1+where(d2==other, 1, 0))
            tmp2[logical_or(other<d1, other>d2)] = inf
    #        else:
    #            tmp2 =  asfarray(K-J+where(d2==other, 0, 1))
    #            tmp2[logical_or(other<d1, other>d2)] = 0
            if goal_is_nlh:
                T2 = log2(vstack((tmp1, tmp2)).T)
            else:
                T2 = log2(vstack((tmp1, tmp2)).T)
            
            d1, d2 = D0, D2
            tmp = asfarray(K-I+where(d2==other, 1, 0))
            tmp[logical_or(other<d1, other>d2)] = inf
            T0 = log2(tmp)
        else:
            assert np.all(d == array(d, int)) and len(d) == d[-1]-d[0]+1, 'bug in FD kernel'
            #assert np.all(1e-6 < np.abs(np.array(mx, int)-mx))
            assert goal_is_nlh, 'unimplemented yet'
            
            tmp = ux - lx
            tmp[other < lx] = inf
            tmp[other > ux] = inf
            tmp[logical_and(tmp==0, other == lx)] = 0.0
            T0 = log2(tmp+1)
            
            floor_mx = np.floor(mx)
            tmp1 = floor_mx - lx
            tmp1[other < lx] = inf
            tmp1[other > floor_mx] = inf
            tmp1[logical_and(tmp1==0, other == lx)] = 0.0
            
            ceil_mx = np.ceil(mx)
            tmp2 = ux - ceil_mx 
            tmp2[other > ux] = inf
            tmp2[other < ceil_mx] = inf
            tmp2[logical_and(tmp2==0, other == ux)] = 0.0
            if goal_is_nlh:
                T2 = log2(vstack((tmp1, tmp2)).T + 1.0)
            else:
                assert 0, 'unimplemented yet'
                #T2 = log2(vstack((tmp1, tmp2)).T)

    res = T2
    
    return T0, res, DefiniteRange


def yield_stochastic(r, point, v):
    sz = getattr(point, 'maxDistributionSize', 0)
    if sz == 0:
        s = '''
        if one of function arguments is stochastic distribution 
        without resolving into quantified value 
        (e.g. uniform(-10,10) instead of uniform(-10,10, 100), 100 is number of point to emulate)
        then you should evaluate the function 
        onto oopoint with assigned parameter maxDistributionSize'''
        raise FuncDesignerException(s)
    if not r.quantified:
        r = r._yield_quantified(sz)
    r = r.copy()
    r.stochDep = {v:1}
    r.maxDistributionSize = sz
    if r.size > sz:
        r.reduce(sz)
    tmp = getattr(point, '_p', None)
    if tmp is not None:
        r._p = tmp
    return r
