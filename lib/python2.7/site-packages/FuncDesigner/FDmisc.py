PythonSum = sum
PythonAny = any
from numpy import asscalar, isscalar, asfarray, ndarray, prod, logical_and, logical_or, inf, atleast_1d, any, \
where, hstack, atleast_2d, vstack, isinf
import numpy as np
from baseClasses import MultiArray, Stochastic

try:
    import scipy.sparse as SP
    from scipy.sparse import hstack as HstackSP, vstack as VstackSP, eye as SP_eye, \
    lil_matrix as SparseMatrixConstructor, isspmatrix, find as Find
    def Hstack(Tuple):
        ind = where([isscalar(elem) or prod(elem.shape)!=0 for elem in Tuple])[0].tolist()
        elems = [Tuple[i] for i in ind]
        if PythonAny(isspmatrix(elem) for elem in elems):
            return HstackSP(elems)
        
        s = set([(0 if isscalar(elem) else elem.ndim) for elem in elems])
        ndim = max(s)
        if ndim <= 1:  return hstack(elems)
        assert ndim <= 2 and 1 not in s, 'bug in FuncDesigner kernel, inform developers'
        return hstack(elems) if 0 not in s else hstack([atleast_2d(elem) for elem in elems])
    def Vstack(Tuple):
        ind = where([isscalar(elem) or prod(elem.shape)!=0 for elem in Tuple])[0].tolist()
        elems = [Tuple[i] for i in ind]
        if PythonAny(isspmatrix(elem) for elem in elems):
            return VstackSP(elems)
        else:
            return vstack(elems)
#        s = set([(0 if isscalar(elem) else elem.ndim) for elem in elems])
#        ndim = max(s)
#        if ndim <= 1:  return hstack(elems)
#        assert ndim <= 2 and 1 not in s, 'bug in FuncDesigner kernel, inform developers'
#        return hstack(elems) if 0 not in s else hstack([atleast_2d(elem) for elem in elems])        
    scipyInstalled = True
except:
    isspmatrix = lambda *args,  **kwargs:  False
    Hstack = hstack
    Vstack = vstack
    SparseMatrixConstructor = None
    SP_eye = None
    scipyInstalled = False
    def Find(*args, **kwargs): 
        raise FuncDesignerException('error in FuncDesigner kernel, inform developers')

class FuncDesignerException(BaseException):
    def __init__(self,  msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def checkSizes(a, b):
    if a.size != 1 and b.size != 1 and a.size != b.size:
        raise FuncDesignerException('operation of oovar/oofun ' + a.name + \
        ' and object with inappropriate size:' + str(a.size) + ' vs ' + b.size)

scipyAbsentMsg = 'Probably scipy installation could speed up running the code involved'

pwSet = set()
def pWarn(msg):
    if msg in pwSet: return
    pwSet.add(msg)
    print('FuncDesigner warning: ' + msg)


class diagonal:
    isOnes = False
    __array_priority__ = 150000# set it greater than 1 to prevent invoking numpy array __mul__ etc
    
    def __init__(self, arr, scalarMultiplier=1.0, size=0):
        #assert arr is None or arr.ndim <= 1
        self.diag = arr.copy() if arr is not None else None # may be None, then n has to be provided
        self.scalarMultiplier = scalarMultiplier if isscalar(scalarMultiplier) \
        else asscalar(scalarMultiplier) if type(scalarMultiplier) == ndarray\
        else scalarMultiplier[0, 0] if scipyInstalled and SP.isspmatrix(scalarMultiplier)\
        else raise_except()
        self.size = arr.size if size == 0 else size
        if arr is None:
            self.isOnes = True
        
    copy = lambda self: diagonal(self.diag, scalarMultiplier = self.scalarMultiplier, size = self.size)
    
    def toarray(self):
        if self.isOnes:
            tmp = np.empty(self.size)
            
            # for PyPy compatibility
            scalarMultiplier = asscalar(self.scalarMultiplier) if type(self.scalarMultiplier) == ndarray else self.scalarMultiplier
            
            tmp.fill(scalarMultiplier)
            return np.diag(tmp)
        else:
            return np.diag(self.diag * self.scalarMultiplier)
    
    def resolve(self, useSparse):
        if useSparse in (True, 'auto') and scipyInstalled and self.size > 50:
            if self.isOnes:
                tmp = np.empty(self.size)
                tmp.fill(self.scalarMultiplier)
            else:
                tmp = self.diag*self.scalarMultiplier
            return SP.dia_matrix((tmp,0), shape=(self.size,self.size)) 
        else:
            return self.toarray()

    def __add__(self, item):
        if type(item) == DiagonalType:
            # TODO: mb use other.diag.copy(), self.diag.copy() for more safety, especially for parallel computations?
            if self.isOnes and item.isOnes:
                return diagonal(None, self.scalarMultiplier + item.scalarMultiplier, size=self.size)
            else:
                if self.isOnes:
                    d1 = np.empty(self.size) 
                    d1.fill(self.scalarMultiplier )
                else:
                    d1 = self.diag
                if item.isOnes:
                    d2 = np.empty(item.size) 
                    d2.fill(item.scalarMultiplier )
                else:
                    d2 = item.diag
                return diagonal(d1 * self.scalarMultiplier + d2 * item.scalarMultiplier)
        elif np.isscalar(item) or type(item) == np.ndarray:
            return self.resolve(False)+item
        else: # sparse matrix
            assert SP.isspmatrix(item)
            return self.resolve(True)+item
    
    def __radd__(self, item):
        return self.__add__(item)
    
    def __neg__(self):
        return diagonal(self.diag, -self.scalarMultiplier, size=self.size)
    
    def __mul__(self, item): 
        #!!! PERFORMS MATRIX MULTIPLICATION!!!
        if np.isscalar(item):
            return diagonal(self.diag, item*self.scalarMultiplier, size=self.size)
        if type(item) == DiagonalType:#diagonal:
            scalarMultiplier = item.scalarMultiplier * self.scalarMultiplier
            if self.isOnes:
                diag = item.diag
            elif item.isOnes:
                diag = self.diag
            else:
                diag = self.diag * item.diag
            return diagonal(diag, scalarMultiplier, size=self.size) 
        elif isinstance(item, np.ndarray):
            if item.size == 1:
                return diagonal(self.diag, scalarMultiplier = np.asscalar(item)*self.scalarMultiplier, size=self.size)
            elif min(item.shape) == 1:
                #TODO: assert item.ndim <= 2 
                r = self.scalarMultiplier*item.flatten()
                if self.diag is not None: r *= self.diag
                return r.reshape(item.shape)
            else:
                # new; TODO: improve it
                if self.isOnes:
                    D = np.empty(self.size)
                    D.fill(self.scalarMultiplier)
                else:
                    D = self.scalarMultiplier * self.diag if self.scalarMultiplier != 1.0 else self.diag
                return D.reshape(-1, 1) * item # ! different shapes !
                
                
#                    T = np.dot(self.resolve(False), item)
#                    from numpy import array_equal, all
#                    assert array_equal(T.shape,  T2.shape) and all(T==T2)
#                    print '!'
                #prev
                # !!!!!!!!!! TODO:  rework it!!!!!!!!!!!
#                if self.size < 100 or not scipyInstalled:
#                    return np.dot(self.resolve(False), item)
#                else:
#                    return self.resolve(True)._mul_sparse_matrix(item)
        else:
            #assert SP.isspmatrix(item)
            if prod(item.shape) == 1:
                return diagonal(self.diag, scalarMultiplier = self.scalarMultiplier*item[0, 0], size=self.size)
            else:
                tmp = self.resolve(True)
                if not SP.isspmatrix(tmp): # currently lil_matrix and K^ works very slow on sparse matrices
                    tmp = SP.lil_matrix(tmp) # r.resolve(True) can yield dense ndarray
                return tmp._mul_sparse_matrix(item)
        #return r
    
    def __getattr__(self, attr):
        if attr == 'T': return self # TODO: mb using copy will be more safe
        elif attr == 'shape': return self.size, self.size
        elif attr == 'ndim': return 2
        raise AttributeError('you are trying to obtain incorrect attribute "%s" for FuncDesigner diagonal' %attr)
    
    def __rmul__(self, item):
        return self.__mul__(item) if isscalar(item) else self.__mul__(item.T).T
    
    def __div__(self, other):
        #TODO: check it
        if isinstance(other, np.ndarray) and other.size == 1: other = np.asscalar(other)
        if np.isscalar(other) or prod(other.shape)==1: 
            return diagonal(self.diag, self.scalarMultiplier/other, size=self.size) 
        else: 
            # TODO: check it
            return diagonal(self.diag/other if self.diag is not None else 1.0/other, self.scalarMultiplier, size=self.size) 

DiagonalType = type(diagonal(np.array([0, 0])))

Eye = lambda n: 1.0 if n == 1 else diagonal(None, size=n)

def Diag(x, *args, **kw):
    if isscalar(x) or (type(x)==ndarray and x.size == 1) or isinstance(x, (Stochastic, MultiArray)): 
        return x
    else: 
        return diagonal(asfarray(x) if x is not None else x, *args,  **kw)

#def dictSum(dicts):
#    r = {}
#    K = set().union(*[set(d.keys()) for d in dicts])
#    for k in K:
#        elems = (d.get(k, None) for d in dicts)
#        r[k] = PythonSum(elem for elem in elems if elem is not None)
##        r[k] = PythonSum(d.get(k) for d in dicts if k in d)
#    return r

def dictSum(dicts):
    K = set.union(*[set(d.keys()) for d in dicts])
    R = dict((v, []) for v in K)
    for d in dicts:
        for k, val in d.items():
          R[k].append(val)
    r = dict((k, PythonSum(val)) for k, val in R.items())
    return r

class fixedVarsScheduleID:
    fixedVarsScheduleID = 0
    def _getDiffVarsID(*args):
        fixedVarsScheduleID.fixedVarsScheduleID += 1
        return fixedVarsScheduleID.fixedVarsScheduleID
DiffVarsID = fixedVarsScheduleID()
_getDiffVarsID = lambda *args: DiffVarsID._getDiffVarsID(*args)

try:
    import __pypy__
    isPyPy = True
except ImportError:
    isPyPy = False

def raise_except(*args, **kwargs):
    raise FuncDesignerException('bug in FuncDesigner engine, inform developers')
    
class Extras:
    pass

# TODO: make it work for ooSystem as well
def broadcast(func, oofuncs, useAttachedConstraints, *args, **kwargs):
    from ooFun import oofun
    if isinstance(oofuncs, oofun):
        oofuncs = [oofuncs]
    oofun._BroadCastID += 1
    for oof in (oofuncs if not isinstance(oofuncs, ndarray) else atleast_1d(oofuncs)):
        Iterator = oof if isinstance(oof, (list, tuple, ndarray)) else [oof] if oof is not None else []
        for elem in Iterator: 
            elem._broadcast(func, useAttachedConstraints, *args, **kwargs)

def _getAllAttachedConstraints(oofuns):
    from FuncDesigner import broadcast
    r = set()
    def F(oof):
        r.update(oof.attachedConstraints)
    broadcast(F, oofuns, useAttachedConstraints=True)
    return r

def formDepCounter(oofuns):
    # TODO: mb exclude fixed oovars/oofuncs?
    from FuncDesigner import broadcast, oofun
    R = {}
    def func(oof):
        if oof.is_oovar:
            R[oof] = {oof: 1}
            return
        dicts = [R.get(inp) for inp in oof.input if isinstance(inp, oofun)]
        R[oof] = dictSum(dicts)
    broadcast(func, oofuns, useAttachedConstraints=False)
    return R 

def formResolveSchedule(oof):
    depsNumber = formDepCounter(oof)
    def F(ff, depsNumberDict, baseFuncDepsNumber, R):
        tmp = depsNumberDict[ff]
        s = []
        for k, v in tmp.items():
            if baseFuncDepsNumber[k] == v:
                s.append(k)
                baseFuncDepsNumber[k] -= 1
        if len(s):
            R[ff] = s
    R = {}
    broadcast(F, oof, False, depsNumber, depsNumber[oof].copy(), R)
    R.pop(oof, None)
    oof.resolveSchedule = R

def update_mul_inf_zero(lb1_ub1, lb2_ub2, t):
    #TODO: handle Stochastic
    if not any(isinf(lb1_ub1)) and not any(isinf(lb2_ub2)):
        return
        
    t_min, t_max = t
    lb1, ub1 = lb1_ub1
    lb2, ub2 = lb2_ub2
    
    ind1_zero_minus = logical_and(lb1<0, ub1>=0)
    ind1_zero_plus = logical_and(lb1<=0, ub1>0)
    
    ind2_zero_minus = logical_and(lb2<0, ub2>=0)
    ind2_zero_plus = logical_and(lb2<=0, ub2>0)
    
    has_plus_inf_1 = logical_or(logical_and(ind1_zero_minus, lb2==-inf), logical_and(ind1_zero_plus, ub2==inf))
    has_plus_inf_2 = logical_or(logical_and(ind2_zero_minus, lb1==-inf), logical_and(ind2_zero_plus, ub1==inf))
    
    # !!!! lines with zero should be before lines with inf !!!!
    ind = logical_or(logical_and(lb1==-inf, ub2==0), logical_and(lb2==-inf, ub1==0))
    t_max[atleast_1d(logical_and(ind, t_max<0.0))] = 0.0
    
    t_max[atleast_1d(logical_or(has_plus_inf_1, has_plus_inf_2))] = inf
    t_max[atleast_1d(logical_or(logical_and(lb1==0, ub2==inf), logical_and(lb2==0, ub1==inf)))] = inf
    
    has_minus_inf_1 = logical_or(logical_and(ind1_zero_plus, lb2==-inf), logical_and(ind1_zero_minus, ub2==inf))
    has_minus_inf_2 = logical_or(logical_and(ind2_zero_plus, lb1==-inf), logical_and(ind2_zero_minus, ub1==inf))
    # !!!! lines with zero should be before lines with -inf !!!!
    t_min[atleast_1d(logical_or(logical_and(lb1==0, ub2==inf), logical_and(lb2==0, ub1==inf)))] = 0.0
    t_min[atleast_1d(logical_or(logical_and(lb1==-inf, ub2==0), logical_and(lb2==-inf, ub1==0)))] = 0.0
    
    t_min[atleast_1d(logical_or(has_minus_inf_1, has_minus_inf_2))] = -inf

def update_negative_int_pow_inf_zero(arg_infinum, arg_supremum, r, other):
    #TODO: handle Stochastic
    r1, r2 = r
    assert other < 0
    isOdd = other % 2 == 1
    ind_zero = logical_and(arg_infinum<0, arg_supremum>0)
    if isOdd:
        r1[ind_zero] = -inf
    r2[ind_zero] = inf
    ind_zero_minus = logical_and(arg_infinum<0, arg_supremum==0)
    if isOdd:
        r1[ind_zero_minus] = -inf
    r2[ind_zero_minus] = arg_infinum[ind_zero_minus]**other
    ind_zero_plus = logical_and(arg_infinum==0, arg_supremum>0)
    r1[ind_zero_plus] = arg_supremum[ind_zero_plus]**other
    r2[ind_zero_plus] = inf
        
def update_div_zero(lb1, ub1, lb2, ub2, r):
    #TODO: handle Stochastic
    r1, r2 = r
    ind = logical_or(lb1==0.0, ub1==0.0)
    if any(ind):
        r1[atleast_1d(logical_and(ind, r1>0.0))] = 0.0
        r2[atleast_1d(logical_and(ind, r2<0.0))] = 0.0

    # adjust inf
    ind2_zero_minus = logical_and(lb2<0, ub2>=0)
    ind2_zero_plus = logical_and(lb2<=0, ub2>0)
    if any(ind2_zero_minus) or any(ind2_zero_plus):
        r1[atleast_1d(logical_or(logical_and(ind2_zero_minus, ub1>0), logical_and(ind2_zero_plus, lb1<0)))] = -inf
        r2[atleast_1d(logical_or(logical_and(ind2_zero_minus, lb1<0), logical_and(ind2_zero_plus, ub1>0)))] = inf

Len = lambda x: 1 if isscalar(x) else x.size if type(x)==ndarray \
else x.values.size if isinstance(x, Stochastic) else len(x)

Copy = lambda arg: asscalar(arg) if type(arg)==ndarray and arg.size == 1 \
else arg.copy() if hasattr(arg, 'copy') else np.copy(arg)


# temporary, until normal pypy implementation
def PyPy_where(*args):
    if len(args) == 3:
        return np.where(*args)
    elif len(args) != 1:
        assert 0, 'number of arguments for numpy.where must be 1 or 3'
    A = np.asarray(args[0])
    if A.ndim > 2:
        assert 0, 'unimplemented yet'
    if A.ndim == 0:
        return (np.array([0]),) if A != 0 else (np.array([], dtype=np.int32),)
    if A.ndim == 1:
        r = (np.array([i for i, elem in enumerate(A) if elem != 0.0]),)
        return r
        
    # A.ndim == 2
    I, J = [], []
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if A[i, j] != 0.0:
                I.append(i)
                J.append(j)
    return (np.array(I), np.array(J))


where = PyPy_where if isPyPy else np.where
