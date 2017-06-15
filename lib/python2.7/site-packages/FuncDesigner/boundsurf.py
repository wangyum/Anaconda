PythonSum = sum
PythonAll = all
import numpy as np
from numpy import all, any, logical_and, logical_not, isscalar, inf, logical_or, logical_xor, isnan#where
from operator import gt as Greater, lt as Less, truediv as td
from FDmisc import update_mul_inf_zero, update_div_zero, where
#from multiarray import multiarray

import operator

try:
    from bottleneck import nanmin, nanmax
except ImportError:
    from numpy import nanmin, nanmax
arrZero = np.array(0.0)

class surf(object):
    isRendered = False
    __array_priority__ = 15
    def __init__(self, d, c):
        self.d = d # dict of variables and linear coefficients on them (probably as multiarrays)
        self.c = np.asarray(c) # (multiarray of) constant(s)

    value = lambda self, point: self.c + PythonSum(point[k] * v for k, v in self.d.items())
    
#    def invert(self, ind=None):
#        ind_is_None = ind is None
#        C = -self.c if ind_is_None else where(ind, -self.c, self.c)
#        D = dict((k, 
#                  (-v if ind_is_None else where(ind, -v, v))) \
#                  for k, v in self.d.items())
#        if 'd2' not in self.__dict__:
#            return surf(D, C)
#        from boundsurf2 import surf2
#        D2 = dict((k, 
#                  (-v if ind_is_None else where(ind, -v, v))) \
#                  for k, v in self.d2.items())
#        return surf2(D2, D, C)
        
#    resolve = lambda self, domain, cmp: \
#    self.c + PythonSum(where(cmp(v, 0), domain[k][0], domain[k][1])*v for k, v in self.d.items())
    
    def exclude(self, domain, oovars, cmp):
        C = []
        d = self.d.copy()
        for v in oovars:
            tmp = d.pop(v, 0.0)
            if any(tmp):
                D = domain[v]
                C.append(where(cmp(tmp, 0), D[0], D[1])*tmp)
        c = self.c + PythonSum(C)
        return surf(d, c)
    
#    split = lambda self, inds: [extract(self, ind) for ind in inds]
    
    #self.resolve(domain, GREATER)
    minimum = lambda self, domain, domain_ind = None: \
    self.c +\
    (PythonSum(where(v > 0, 
    domain[k][0], domain[k][1])*v for k, v in self.d.items()) if domain_ind is None else
    PythonSum(where(v > 0, 
    domain[k][0][domain_ind], domain[k][1][domain_ind])*v for k, v in self.d.items()))
    
    #self.resolve(domain, LESS)
    maximum = lambda self, domain, domain_ind = None: \
    self.c +\
    (PythonSum(where(v < 0, 
    domain[k][0], domain[k][1])*v for k, v in self.d.items()) if domain_ind is None else
    PythonSum(where(v < 0, 
    domain[k][0][domain_ind], domain[k][1][domain_ind])*v for k, v in self.d.items()))
    
    def render(self, domain, cmp):
        self.rendered = dict((k, where(cmp(v, 0), domain[k][0], domain[k][1])*v) for k, v in self.d.items())
        self.resolved = PythonSum(self.rendered) + self.c
        self.isRendered = True
    
    def extract(self, ind): 
#        if ind.dtype == bool:
#            ind = where(ind)[0]
        d = dict((k, v if v.size == 1 else v[ind]) for k, v in self.d.items()) 
        C = self.c 
        c = C if C.size == 1 else C[ind] #if not isinstance(C, multiarray) else C[:, ind]
        return surf(d, c) 
    
    def __add__(self, other):
        if type(other) == surf:
#            if other.isRendered and not self.isRendered:
#                self, other = other, self
            S, O = self.d, other.d
            d = S.copy()
            d.update(O)
            for key in set(S.keys()) & set(O.keys()):
                d[key] = S[key]  + O[key]
            return surf(d, self.c+other.c)
        elif isscalar(other) or type(other) == np.ndarray:
            return surf(self.d, self.c + other)
        elif isinstance(other, surf):# surf2 class instance
            return other + self
        else:
            assert 0, 'unimplemented yet'
    
    __sub__ = lambda self, other: self.__add__(-other)
    
    __neg__ = lambda self: surf(dict((k, -v) for k, v in self.d.items()), -self.c)
    
    def __mul__(self, other):
        isArray = type(other) == np.ndarray
        if isscalar(other) or isArray:
            return surf(dict((k, v*other) for k, v in self.d.items()), self.c * other)
        else:
            assert 0, 'unimplemented yet'
            
    __rmul__ = __mul__
    
#    def koeffs_mul(self, other):
#        assert type(other) == surf
#        S, O = self.d, other.d
#        d = dict((key, S.get(key, 0.0)  * O.get(key, 0.0)) for key in set(S.keys()) | set(O.keys()))
#        return surf(d, 0.0)
            
#    def __getattr__(self, attr):
#        if attr == 'resolve_index':
#            assert 0, 'resolve_index must be used from surf derived classes only'
#        else:
#            raise AttributeError('error in FD engine (class surf)')
            

class boundsurf(object):#object is added for Python2 compatibility
    __array_priority__ = 15
    isRendered = False
    resolved = False
    level = 1
    def __init__(self, lowersurf, uppersurf, definiteRange, domain, checkType = True):
        if checkType:
            assert type(lowersurf) == type(uppersurf) == surf # not surf2
        self.l = lowersurf
        self.u = uppersurf
        self.definiteRange = definiteRange
        self.domain = domain
#        print lowersurf.d, lowersurf.c
#        print uppersurf.d, uppersurf.c
        
    Size = lambda self: max((len(self.l.d), len(self.u.d), 1))
    
    def _dep(self):
        r = set.union(set(self.l.d.keys()), set(self.u.d.keys()))
        tmp = getattr(self.l, 'd2', None)
        if tmp is not None:
            r |= set(tmp.keys())
        tmp = getattr(self.u, 'd2', None)
        if tmp is not None:
            r |= set(tmp.keys())
        return r
    
    def __getattr__(self, attr):
        if attr == 'dep':
            self.dep =self._dep()
            return self.dep # dependence oovars
        else:
            raise AttributeError('incorrect attribute %s for boundsurf / boundsurf2 instance' % attr)
            
    
    def exclude(self, oovars):
        L = self.l.exclude(self.domain, oovars, Greater)
        U = self.u.exclude(self.domain, oovars, Less)
        if len(L.d) != 0 or len(U.d) != 0:
            return boundsurf(L, U, self.definiteRange, self.domain)
        else:
            return np.vstack((L.c, U.c))
    
    def extract(self, ind): 
        Ind = ind if ind.dtype != bool else where(ind)[0]
        definiteRange = self.definiteRange if type(self.definiteRange) == bool \
        or self.definiteRange.size == 1 else self.definiteRange[ind]
        return boundsurf(self.l.extract(Ind), self.u.extract(Ind), definiteRange, self.domain)

    def resolve(self):
        if not self.resolved:
            self._resolved = np.vstack((self.l.minimum(self.domain), self.u.maximum(self.domain)))
            self.resolved = True
        assert self._resolved.shape[0] == 2, 'bug in FD kernel'
        return self._resolved, self.definiteRange
    
    def invert(self, ind=None):
        B = self.__class__
        if ind is None:
            return B(-self.u, -self.l, self.definiteRange, self.domain)
#            if ind.dtype != bool:
#                bool_ind = np.zeros()
        assert ind.dtype == bool, 'unimplemented yet'
        ind_same, ind_invert = where(logical_not(ind))[0], where(ind)[0]
        l1, u1 = self.l.extract(ind_same), self.u.extract(ind_same)
        l2, u2 = self.l.extract(ind_invert), self.u.extract(ind_invert)
        b1 = B(l1, u1, False, self.domain)
        b2 = B(-u2, -l2, False, self.domain)
        b = boundsurf_join((ind_same, ind_invert), (b1, b2))
        b.definiteRange = self.definiteRange
#        l, u = self.u.invert(ind), self.l.invert(ind)
#        if ind is None:
        return b
#        l_unchanged, u_unchanged = self.l.extract()
    
    def render(self):
        if self.isRendered:
            return
#        self.l.render(self, self.domain, GREATER)
#        self.u.render(self, self.domain, LESS)
        self.isRendered = True
    
    values = lambda self, point: (self.l.value(point), self.u.value(point))
    
    isfinite = lambda self: all(np.isfinite(self.l.c)) and all(np.isfinite(self.u.c))
    
    # TODO: handling fd.sum()
    def __add__(self, other):
        if isscalar(other) or (type(other) == np.ndarray and other.size == 1):
            if self.l is self.u:
                # TODO: mb use id() instead of "is"
                tmp = self.l+other
                rr = (tmp, tmp)
            else:
                rr = (self.l+other, self.u+other)
            return boundsurf(rr[0], rr[1], self.definiteRange, self.domain)
        elif type(other) == boundsurf:# TODO: replace it by type(r[0]) after dropping Python2 support
            if self.l is self.u and other.l is other.u:
                # TODO: mb use id() instead of "is"
                tmp = self.l+other.l
                rr = (tmp, tmp)
            else:
                rr = (self.l+other.l, self.u+other.u)
            return boundsurf(rr[0], rr[1], self.definiteRange & other.definiteRange, self.domain)
        elif type(other) == np.ndarray:
            assert other.shape[0] == 2, 'unimplemented yet'
            L = self.l + other[0]
            if self.l is self.u and np.array_equal(other[0], other[1]):
                # may be from fixed variables
                U = L
            else:
                U = self.u+other[1]
            return boundsurf(L, U, self.definiteRange, self.domain)
        elif isinstance(other, boundsurf): # boundsurf2
            return other + self
        else:
            assert 0, 'unimplemented yet'
            
    __radd__ = __add__
    
    def __neg__(self):
        l, u = self.l, self.u
        if l is u:
            tmp = surf(dict((k, -v) for k, v in u.d.items()), -u.c)
            L, U = tmp, tmp
        else: 
            L = surf(dict((k, -v) for k, v in u.d.items()), -u.c)
            U = surf(dict((k, -v) for k, v in l.d.items()), -l.c)
        return boundsurf(L, U, self.definiteRange, self.domain)
    
    # TODO: mb rework it
    __sub__ = lambda self, other: self.__add__(-other)
    __rsub__ = lambda self, other: (-self).__add__(other)
    
    def direct_sub(self, other):
        self_lvl = self.level
        if isinstance(other, boundsurf):
            other_lvl = other.level
            if self_lvl == 2 or other_lvl == 2:
                from boundsurf2 import boundsurf2
                B = boundsurf2
            else:
                B = boundsurf
            L, U = other.l, other.u
            return B(self.l - L, self.u - U, logical_and(self.definiteRange, other.definiteRange), self.domain)
        elif type(other) == np.ndarray:
            assert other.shape[0] == 2, 'probably bug'
            L, U = other
            B = type(self)
            # definiteRange must be computed in higher level
            return B(self.l - L, self.u - U, self.definiteRange, self.domain)
        else:
            assert 0, 'probably bug'
            
        
    def __mul__(self, other, resolveSchedule = ()):
        from boundsurf2 import boundsurf2
        
        domain = self.domain
        definiteRange = self.definiteRange
        
        isArray = type(other) == np.ndarray
        isBoundSurf = type(other) == boundsurf
        isBoundSurf2 = type(other) == boundsurf2
        
        if isBoundSurf:
            definiteRange = logical_and(definiteRange, other.definiteRange)
        R2 = other.resolve()[0] if isBoundSurf or isBoundSurf2 else other
        R2_is_scalar = isscalar(R2)
        
        if not R2_is_scalar and R2.size != 1:
            assert R2.shape[0] == 2, 'bug or unimplemented yet'
            R2Positive = all(R2 >= 0)
            R2Negative = all(R2 <= 0)
#            if not selfPositive and not selfNegative:
#                assert R2Positive or R2Negative, 'bug or unimplemented yet'
            
        if R2_is_scalar or (isArray and R2.size == 1):
            if self.l is self.u:
                tmp = self.l * R2
                rr = (tmp, tmp)
            else:
                rr = (self.l * R2, self.u * R2) if R2 >= 0 else (self.u * R2, self.l * R2)
            return boundsurf(rr[0], rr[1], definiteRange, domain)
        R1 = self.resolve()[0]
        selfPositive = all(R1 >= 0)
        selfNegative = all(R1 <= 0)
        
        if isArray:
#            assert R2Positive or R2Negative, 'bug or unimplemented yet'
            rr = mul_fixed_interval(self, other)

        elif isBoundSurf or isBoundSurf2:
            sameBounds_1 = self.l is self.u
            sameBounds_2 = other.l is other.u
            if self.level == other.level == 1 and sameBounds_1 and sameBounds_2 and self.b2equiv(other):
                rr = b2mult_direct(self, other)
            elif (((selfPositive or selfNegative) and sameBounds_1) or ((R2Positive or R2Negative) and sameBounds_2))\
            and self.level == other.level == 1 and self.b2equiv(other):
                Self = self if selfPositive else -self
                Other = other if R2Positive else -other
                r = b2mult(Self, Other)
                rr = r if selfPositive == R2Positive else -r
            elif (selfPositive or selfNegative) and (R2Positive or R2Negative):
                Self = self if selfPositive else -self
                Other = other if R2Positive else -other
                
                if self.level == other.level == 1 and self.b2equiv(other):
                    r = b2mult(Self, Other)
                else:
                    _r = Self.log() + Other.log()
                    if len(resolveSchedule):
                        _r = _r.exclude(resolveSchedule)
                    if type(_r) == np.ndarray:
                        r = np.exp(_r)
                        return r if selfPositive == R2Positive else -r[::-1]#, definiteRange
                    r = _r.exp()
                    # is definiteRange required here?
                    r.definiteRange = definiteRange
                    
                rr = r if selfPositive == R2Positive else -r
            else:
                Elems = (self, other)
                rr = aux_mul_div_boundsurf(Elems, operator.mul, resolveSchedule)

#            else:
#                RR = R1*R2 if selfPositive and R2Positive \
#                else (R1*R2)[::-1] if not selfPositive and not R2Positive\
#                else R1[::-1]*R2 if not selfPositive and R2Positive\
#                else R1*R2[::-1] #if selfPositive and not R2Positive
#                new_l_resolved, new_u_resolved = RR
#                
#                l1, u1, l2, u2 = self.l, self.u, other.l, other.u
#                l, u = l1.koeffs_mul(l2), u1.koeffs_mul(u2)
#                l.c = new_l_resolved - l.minimum(domain)
#                u.c = new_u_resolved - u.maximum(domain)
#                rr = (l, u)

#            return R1*other# if nanmax(R2[0])
            #return 0.5 * (R1*other + R2*self)
            
        else:
            assert 0, 'bug or unimplemented yet (incorrect boundsurf.__mul__ type: %s)' % type(other)
#            assert isBoundSurf2, 'bug or unimplemented yet (incorrect boundsurf.__mul__ type: %s)' % type(other)
#            return other * self
            
        R = rr if type(rr) in (boundsurf, boundsurf2) else boundsurf(surf({}, rr[0]), surf({}, rr[1]), definiteRange, domain)
        R = mul_handle_nan(R, R1, R2, domain)
        return R
    
    __rmul__ = __mul__
    
    def __div__(self, other, resolveSchedule=()):
        isBoundSurf = isinstance(other, boundsurf)
        assert isBoundSurf
        
        r = aux_mul_div_boundsurf((self, other), operator.truediv, resolveSchedule)
        
#        return r 
#        ind_inf_z = logical_or(logical_or(R2[0]==0, R2[1]==0), logical_or(isinf(R1[0]), isinf(R1[1])))
        #(R2[0]==0) | (R2[1]==0) | (isinf(R2[0])) | (isinf(R2[1])) | (isinf(R1[0])) | isinf(R1[1])
        
        isBoundsurf = isinstance(r, boundsurf)
        rr = r.resolve()[0] if isBoundsurf else r#[0]
        
#        import pylab, numpy
#        xx = numpy.linspace(-1, 0, 1000)
#        t=r.l.d.keys()[0]
#        tmp=r
#        pylab.plot(xx, tmp.l.d2.get(t, 0.0)*xx**2+ tmp.l.d.get(t, 0.0)*xx+ tmp.l.c, 'r')
#        pylab.plot(xx, tmp.u.d2.get(t, 0.0)*xx**2+ tmp.u.d.get(t, 0.0)*xx+ tmp.u.c, 'b')
#        pylab.grid()
#        pylab.show()
        
        
        # nans may be from other computations from a level below, although
        ind_nan = logical_or(isnan(rr[0]), isnan(rr[1]))
        if not any(ind_nan) or not isBoundsurf:
            return r #if isBoundsurf else rr

        Ind_finite = where(logical_not(ind_nan))[0]
        r_finite = r.extract(Ind_finite)
        ind_nan = where(ind_nan)[0]
        R1 = self.resolve()[0]
        R2 = other.resolve()[0]
        lb1, ub1, lb2, ub2 = R1[0, ind_nan], R1[1, ind_nan], R2[0, ind_nan], R2[1, ind_nan]
        tmp = np.vstack((td(lb1, lb2), td(lb1, ub2), td(ub1, lb2), td(ub1, ub2)))
        R = np.vstack((nanmin(tmp, 0), nanmax(tmp, 0)))
        update_div_zero(lb1, ub1, lb2, ub2, R)
        b = boundsurf(surf({}, R[0]), surf({}, R[1]), False, self.domain)
        r = boundsurf_join((ind_nan, Ind_finite), (b, r_finite))
        definiteRange = logical_and(self.definiteRange, other.definiteRange)
        r.definiteRange = definiteRange
        return r 
    
    __truediv__ = __div__
    
#    __rdiv__ = lambda self, other: other * self ** -1
    
#    __rtruediv__ = __rdiv__

    def log(self):#, domain_ind = slice(None)):
        from Interval import defaultIntervalEngine
#        from ooFun import oofun
#        return oofun._interval_(self, domain, dtype)
#        from overloads import log_interval
#        return log_interval(self, self.domain, float)

        ia_lvl_2_unavailable = len(self.l.d) != 1 or len(self.u.d) != 1 \
        or (self.level == 2 and (len(self.l.d2) != 1 or len(self.u.d2) != 1))
        
        is_b2 = self.level == 2
        
        if ia_lvl_2_unavailable or is_b2:
            r1 = defaultIntervalEngine(self, np.log, lambda x: 1.0/x, monotonity = 1, convexity = -1, feasLB = 0.0)[0]
        else:
            r1 = None
            
        if ia_lvl_2_unavailable:
            return r1
            
        from overloads import log_b_interval
        r = log_b_interval(self, r1)[0]
        return r
        
    def exp(self):#, domain_ind = slice(None)):
        from Interval import defaultIntervalEngine
        
        ia_lvl_2_unavailable = len(self.l.d) != 1 or len(self.u.d) != 1 \
        or (self.level == 2 and (len(self.l.d2) != 1 or len(self.u.d2) != 1))
        
        is_b2 = self.level == 2
        
        if ia_lvl_2_unavailable or is_b2:
            r1 = defaultIntervalEngine(self, np.exp, np.exp, 
                         monotonity = 1, convexity = 1)[0]
        else:
            r1 = None
            
        if ia_lvl_2_unavailable:
            return r1
            
        from overloads import exp_b_interval
        r = exp_b_interval(self, r1, self.definiteRange, self.domain)[0]
        return r

    # TODO: rework it if __iadd_, __imul__ etc will be created
    def copy(self):
        assert '__iadd__' not in self.__dict__
        assert '__imul__' not in self.__dict__
        assert '__idiv__' not in self.__dict__
        assert '__isub__' not in self.__dict__
        return self
    
    def b2equiv(self, other):
        if len(self.l.d) > 1 or len(other.l.d) > 1 or len(self.u.d) > 1 or len(other.u.d) > 1:
            return False
        if len(getattr(self.l, 'd2', {})) > 1 or len(getattr(other.l, 'd2', {})) > 1 \
        or len(getattr(self.u, 'd2', {})) > 1 or len(getattr(other.u, 'd2', {})) > 1:
            return False
        if not (set(self.l.d.keys()) == set(other.l.d.keys()) == set(self.u.d.keys()) == set(other.u.d.keys())):
            return False
        return True
    
    abs = lambda self: boundsurf_abs(self)
    
    
def boundsurf_abs(b):
    r, definiteRange = b.resolve()
    lf, uf = r

    assert lf.ndim <= 1, 'unimplemented yet'
    
    ind_l = lf >= 0
    if all(ind_l):
        return b, b.definiteRange
    
    ind_u = uf <= 0
    if all(ind_u):
        return -b, b.definiteRange
    
    from Interval import defaultIntervalEngine
        
    return defaultIntervalEngine(b, np.abs, np.sign, 
                         monotonity = np.nan, convexity = 1, 
                         criticalPoint = 0.0, criticalPointValue = 0.0)


def Join(inds, arrays):
#    print(type(inds), type(arrays), len(inds), len(arrays))
#    print(PythonSum(ind.size for ind in inds), arrays[0].dtype)
    r = np.empty(PythonSum(ind.size for ind in inds), arrays[0].dtype)
#    print(r.shape, r.dtype)
    for ind, arr in zip(inds, arrays):
        if ind.size == 0: 
            continue
#        print (ind.shape, arr.shape)
        r[ind] = arr
    return r

def surf_join(inds, S):
    c = Join(inds, [s.c for s in S]) # list, not iterator!
    
    keys = set.union(*[set(s.d.keys()) for s in S])
    d = dict((k, Join(inds, [s.d.get(k, arrZero) for s in S])) for k in keys)
    
    keys = set.union(*[set(getattr(s,'d2', {}).keys()) for s in S])
    if len(keys) == 0:
        return surf(d, c)
        
    d2 = dict((k, Join(inds, [getattr(s, 'd2', {}).get(k, arrZero) for s in S])) for k in keys)
    from boundsurf2 import surf2
    return surf2(d2, d, c)

def boundsurf_join(inds, B):
    inds = [(ind if ind.dtype != bool else where(ind)[0]) for ind in inds]
#    B = [b for b in B if b is not None]
    L = surf_join(inds, [b.l for b in B])
    U = surf_join(inds, [b.u for b in B]) #if self.l is not self.u else L
    definiteRange = True \
    if PythonAll(np.array_equiv(True, b.definiteRange) for b in B)\
    else Join(inds, [np.asarray(b.definiteRange) for b in B])
    from boundsurf2 import boundsurf2
    b = boundsurf if type(L) == type(U) == surf else boundsurf2
    return b(L, U, definiteRange, B[0].domain)

#split = lambda condition1, condition2: \
#    (
#    where(condition1)[0], 
#    where(logical_and(condition2, logical_not(condition1)))[0], 
#    where(logical_and(logical_not(condition1), logical_not(condition2)))[0]
#    )

def split(*conditions):
    #Rest = np.ones_like(conditions[0]) # dtype bool
    #Temporary for PyPy:
    Rest = np.ones(conditions[0].shape, conditions[0].dtype) 
    r = []
    for c in conditions:
        tmp = logical_and(c, Rest)
        r.append(where(tmp)[0])
        Rest &= logical_not(c)
    r.append(where(Rest)[0])
    return r

    
Split = lambda condition1, condition2: \
    (
    condition1, 
    logical_and(condition2, logical_not(condition1)), 
    logical_and(logical_not(condition1), logical_not(condition2))
    )



def devided_interval(inp, r, domain, dtype, feasLB = -inf, feasUB = inf):
    import ooFun

    lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 2)
    isBoundSurf = isinstance(lb_ub, boundsurf)
    if not isBoundSurf:
        return ooFun.oofun._interval_(r, domain, dtype)
    
    lb_ub_resolved = lb_ub.resolve()[0]
    
    if feasLB != -inf or feasUB != inf:
        from Interval import adjustBounds
        lb_ub_resolved, definiteRange = adjustBounds(lb_ub_resolved, definiteRange, feasLB, feasUB)
        lb_ub.definiteRange = definiteRange
        
    lb, ub = lb_ub_resolved
    Inds = split(ub <= -0.0, lb >= 0.0)
    assert len(Inds) == 3
    
    monotonities = [r.engine_monotonity] * (len(Inds)-1) if r.engine_monotonity is not np.nan \
    else r.monotonities
    
    convexities = [r.engine_convexity] * (len(Inds)-1) if r.engine_convexity is not np.nan else r.convexities
    
    m = PythonSum(ind_.size for ind_ in Inds)
    inds, rr = [], []
    
    from Interval import defaultIntervalEngine
    
    for j, ind in enumerate(Inds[:-1]):
        if ind.size != 0:
            assert ind.dtype != bool, 'error in FD kernel'
            tmp = defaultIntervalEngine(lb_ub, r.fun, r.d, monotonity=monotonities[j], convexity=convexities[j], 
                                        feasLB = feasLB, feasUB = feasUB, domain_ind = ind if ind.size != m else slice(None))[0]
            if ind.size == m:
                return tmp, tmp.definiteRange
            rr.append(tmp)
            inds.append(ind)
    
    _ind = Inds[-1]
    if _ind.size:
        if convexities == (-1, 1) and r.engine_monotonity == 1:
            tmp = defaultIntervalEngine(lb_ub, r.fun, r.d, monotonity = r.engine_monotonity, convexity=-101, 
                                        feasLB = feasLB, feasUB = feasUB, domain_ind = _ind if _ind.size != m else slice(None))[0]
            if _ind.size == m:
                return tmp, tmp.definiteRange
        elif convexities == (1, -1) and r.engine_monotonity is not np.nan:
            tmp = defaultIntervalEngine(lb_ub, r.fun, r.d, monotonity = r.engine_monotonity, convexity= 9, # 10-1 
                                        feasLB = feasLB, feasUB = feasUB, domain_ind = _ind if _ind.size != m else slice(None))[0]
            if _ind.size == m:
                return tmp, tmp.definiteRange
        else:
            DefiniteRange = definiteRange if type(definiteRange) == bool or definiteRange.size == 1 \
            else definiteRange[_ind]
            
            Tmp, definiteRange3 = \
            ooFun.oofun._interval_(r, domain, dtype, inputData = (lb_ub_resolved[:, _ind], DefiniteRange))
            
            if _ind.size == m:
                return Tmp, definiteRange3
            tmp = boundsurf(surf({}, Tmp[0]), surf({}, Tmp[1]), definiteRange3, domain)
            
        rr.append(tmp)
        inds.append(_ind)

    b = boundsurf_join(inds, rr)
    return b, b.definiteRange


def aux_mul_div_boundsurf(Elems, op, resolveSchedule=()):
    _r = []
    _resolved = []
    changeSign = False
    indZ = False
    
    definiteRange = np.array(True)
    for elem in Elems:
        _R = elem.resolve()[0]
        lb, ub = _R
        
        ind_positive, ind_negative, ind_z = \
        Split(lb >= 0, ub <= 0) if op == operator.mul else Split(lb > 0, ub < 0)# TODO: improve for div
        
        not_ind_negative = logical_not(ind_negative)
        changeSign = logical_xor(changeSign, ind_negative)
        indZ = logical_or(indZ, ind_z)

        tmp1 = elem.extract(not_ind_negative)
        tmp2 = -elem.extract(ind_negative)
        Tmp = boundsurf_join((not_ind_negative, ind_negative), (tmp1, tmp2))#.log()
        
        _r.append(Tmp)
        _resolved.append(_R)
        definiteRange = logical_and(definiteRange, elem.definiteRange)
        
    use_exp = True
    if op == operator.mul:
        if len(_r) == 2 and _r[0].level == _r[1].level == 1 and _r[0].b2equiv(_r[1]):
            rr = b2mult(_r[0], _r[1])
            use_exp = False
        else:
            rr = PythonSum(elem.log() for elem in _r)#.exp()
    else:
        assert op == operator.truediv and len(Elems) == 2
        if _r[1].level == 1 and _r[0].b2equiv(_r[1]):
            rr = b2div(_r[0], _r[1])
            use_exp = False
        else:#if not any(all(_r[0].resolve()[0], 0)==0):# TODO: mb rework it
            #print _r[0].resolve(), _r[1].resolve()
            rr = (_r[0].log() - _r[1].log())#.exp()
#        else:
#            from Interval import direct_div
#            rr = direct_div( _r[0], _r[1])
#            use_exp = False
    

    changeSign = logical_and(changeSign, logical_not(indZ))
    keepSign = logical_and(logical_not(changeSign), logical_not(indZ))

    if use_exp:
        if len(resolveSchedule):
            rr = rr.exclude(resolveSchedule)
            
            if type(rr) == np.ndarray:
                #print('asdf')
                r = np.exp(rr)
                r[:, changeSign] = -r[:, changeSign][::-1]
                return r#, definiteRange
#        print len(rr.dep)
        rr = rr.exp()
#        print type(rr)
#        if type(rr) != boundsurf:
#            print(rr.l.d2, rr.l.d, rr.l.c, '----', rr.u.d2, rr.u.d, rr.u.c)
    
    _rr, _inds = [], []
    if any(keepSign):
        _rr.append(rr.extract(keepSign))
        _inds.append(keepSign)
    if any(changeSign):
        _rr.append(-rr.extract(changeSign))
        _inds.append(changeSign)
    if any(indZ):
        assert len(Elems) == 2, 'unimplemented yet'
        if op == operator.mul:
            lb1, ub1 = Elems[0].resolve()[0] # R1
            other_lb, other_ub = Elems[1].resolve()[0] # R2
           
            IndZ = where(indZ)[0]
            tmp_z = np.vstack((
                               op(lb1[IndZ], other_lb[IndZ]), 
                               op(ub1[IndZ], other_lb[IndZ]), 
                               op(lb1[IndZ], other_ub[IndZ]), 
                              op(ub1[IndZ], other_ub[IndZ])
                              ))
            l_z, u_z = nanmin(tmp_z, 0), nanmax(tmp_z, 0)
        else:
            assert op == operator.truediv
            from Interval import direct_div
            tmp_z = direct_div(Elems[0].resolve()[0][:, indZ], Elems[1].resolve()[0][:, indZ])
            l_z, u_z = tmp_z

        rr_z = boundsurf(surf({}, l_z), surf({}, u_z), True, Elems[0].domain)
        _rr.append(rr_z)
        _inds.append(indZ)

    rr = boundsurf_join(_inds, _rr)

    rr.definiteRange = definiteRange
    return rr


def mul_fixed_interval(self, R2):
    
    if type(self) == boundsurf:
        Boundsurf = boundsurf
    else:
        from boundsurf2 import boundsurf2
        Boundsurf = boundsurf2
    domain = self.domain
    definiteRange = self.definiteRange

    assert R2.shape[0] == 2, 'bug or unimplemented yet'
    R2Positive = all(R2 >= 0)
    R2Negative = all(R2 <= 0)
    
    R1 = self.resolve()[0]
    selfPositive = all(R1 >= 0)
    selfNegative = all(R1 <= 0)
    
    # Temporary, TODO: rework
    R2_0 = R2
    if R2.shape[1] < R1.shape[1]:
        assert R2.shape[1] == 1
        R2  = np.tile(R2, (1, R1.shape[1]))
    
    SelfSameBounds = self.l is self.u
#    print('0', SelfSameBounds, selfPositive, selfNegative)
    if 1 and SelfSameBounds and (selfPositive or selfNegative):
        bound = self.l # equal to self.u
#        if selfPositive or selfNegative:
        rr = (bound * R2_0[0], bound * R2_0[1]) if selfPositive else (bound * R2_0[1], bound * R2_0[0])

    elif selfPositive and R2Positive:
        rr = (self.l * R2_0[0], self.u * R2_0[1]) 
    elif selfPositive and R2Negative:
        rr = (self.u * R2_0[0], self.l * R2_0[1])
    elif selfNegative and R2Negative:
        rr = (self.u * R2_0[1], self.l * R2_0[0]) 
    elif selfNegative and R2Positive:
        rr = (self.l * R2_0[1], self.u * R2_0[0])
    elif R2Positive or R2Negative:
        lb1, ub1 = R1
        ind_positive, ind_negative, ind_z = split(lb1 >= 0, ub1 <= 0)
        other_lb, other_ub = R2 if R2Positive else (-R2[1], -R2[0])
        l, u = self.l, self.u
        
        tmp_l1 = other_lb[ind_positive] * l.extract(ind_positive)
        tmp_l2 = other_ub[ind_negative] * l.extract(ind_negative)
        tmp_u1 = other_ub[ind_positive] * u.extract(ind_positive)
        tmp_u2 = other_lb[ind_negative] * u.extract(ind_negative)
        
#                tmp_l3 = other_ub[ind_z] * l.extract(ind_z)
#                tmp_u3 = other_ub[ind_z] * u.extract(ind_z)

        # TODO: check for similar cases in other code lines
        l2, u2 = (other_lb[ind_z], other_ub[ind_z]) #if R2.size > 2 else (other_lb, other_ub)
        
        l1, u1 = lb1[ind_z], ub1[ind_z]
        Tmp = np.vstack((l1*l2, l1*u2, l2*u1, u1*u2))
        tmp_l3 = surf({}, nanmin(Tmp, axis=0))
        tmp_u3 = surf({}, nanmax(Tmp, axis=0))

        tmp_l = surf_join((ind_positive, ind_negative, ind_z), (tmp_l1, tmp_l2, tmp_l3))
        tmp_u = surf_join((ind_positive, ind_negative, ind_z), (tmp_u1, tmp_u2, tmp_u3))

#        Inds, L, U = [], [], []
#        if ind_positive.size:
#            tmp_l1 = other_lb[ind_positive] * l.extract(ind_positive)
#            tmp_u1 = other_ub[ind_positive] * u.extract(ind_positive)
#            Inds.append(ind_positive)
#            L.append(tmp_l1)
#            U.append(tmp_u1)
#        if ind_negative.size:
#            tmp_l2 = other_ub[ind_negative] * l.extract(ind_negative)
#            tmp_u2 = other_lb[ind_negative] * u.extract(ind_negative)
#            Inds.append(ind_negative)
#            L.append(tmp_l2)
#            U.append(tmp_u2)
#        if ind_z.size:
#            l2, u2 = other_lb[ind_z], other_ub[ind_z]
#            l1, u1 = lb1[ind_z], ub1[ind_z]
#            Tmp = np.vstack((l1*l2, l1*u2, l2*u1, u1*u2))
#            tmp_l3 = surf({}, nanmin(Tmp, axis=0))
#            tmp_u3 = surf({}, nanmax(Tmp, axis=0))
#            Inds.append(ind_z)
#            L.append(tmp_l3)
#            U.append(tmp_u3)

        rr = (tmp_l, tmp_u) if R2Positive else (-tmp_u, -tmp_l)
    elif selfPositive or selfNegative:
        l, u = (self.l, self.u) if selfPositive else (-self.u, -self.l)
        lb1, ub1 = R1
        other_lb, other_ub = R2
        ind_other_positive, ind_other_negative, ind_z2 = split(other_lb >= 0, other_ub <= 0)
        Ind, Tmp_l, Tmp_u = [], [], []
        if ind_other_positive.size:
            Ind.append(ind_other_positive)
            Tmp_l.append(other_lb[ind_other_positive] * l.extract(ind_other_positive))
            Tmp_u.append(other_ub[ind_other_positive] * u.extract(ind_other_positive))
        if ind_other_negative.size:
            Ind.append(ind_other_negative)
            Tmp_l.append(other_lb[ind_other_negative] * u.extract(ind_other_negative))
            Tmp_u.append(other_ub[ind_other_negative] * l.extract(ind_other_negative))
            
#        if 1:
        if ind_z2.size:
            uu = u.extract(ind_z2)
            Ind.append(ind_z2)
            Tmp_l.append(other_lb[ind_z2] * uu)
            Tmp_u.append(other_ub[ind_z2] * uu)
#        else:
#            l2, u2 = other_lb[ind_z2], other_ub[ind_z2]
#            l1, u1 = lb1[ind_z2], ub1[ind_z2]
#            Tmp = np.vstack((l1*l2, l1*u2, l2*u1, u1*u2))
#            tmp_l3 = surf({}, nanmin(Tmp, axis=0))
#            tmp_u3 = surf({}, nanmax(Tmp, axis=0))
        
        tmp_l = surf_join(Ind, Tmp_l)
        tmp_u = surf_join(Ind, Tmp_u)
        rr = (tmp_l, tmp_u) if selfPositive else (-tmp_u, -tmp_l)
    else:
        # TODO: mb improve it
        lb1, ub1 = R1
        lb2, ub2 = R2
        l, u = self.l, self.u
        ind_other_positive, ind_other_negative, ind_z2 = Split(lb2 >= 0, ub2 <= 0)
        ind_positive, ind_negative, ind_z1 = Split(lb1 >= 0, ub1 <= 0)
        inds, lu = [], []

        ind_Z = where(ind_z1)[0]
        if ind_Z.size:
            inds.append(ind_Z)
            l2, u2 = lb2[ind_Z], ub2[ind_Z]
            l1, u1 = lb1[ind_Z], ub1[ind_Z]
            Tmp = np.vstack((l1*l2, l1*u2, l2*u1, u1*u2))
            tmp_l3 = surf({}, nanmin(Tmp, axis=0))
            tmp_u3 = surf({}, nanmax(Tmp, axis=0))
            lu.append((tmp_l3, tmp_u3))
            
        ind_positive_all = logical_and(ind_positive, ind_other_positive)
        ind_Positive = where(ind_positive_all)[0]
        if ind_Positive.size:
            inds.append(ind_Positive)
            L = l.extract(ind_Positive) * lb2[ind_Positive]
            U = u.extract(ind_Positive) * ub2[ind_Positive]
            lu.append((L, U))
        
        ind_negative_all = logical_and(ind_negative, ind_other_negative)
        ind_Negative =  where(ind_negative_all)[0]
        if ind_Negative.size:
            inds.append(ind_Negative)
            U = l.extract(ind_Negative) * lb2[ind_Negative]
            L = u.extract(ind_Negative) * ub2[ind_Negative]
            lu.append((L, U))
            
        ind = logical_and(ind_positive, ind_other_negative)
        Ind = where(ind)[0]
        if Ind.size:
            inds.append(Ind)
            L = u.extract(Ind) * lb2[Ind]
            U = l.extract(Ind) * ub2[Ind]
            lu.append((L, U))

        ind = logical_and(ind_negative, ind_other_positive)
        Ind = where(ind)[0]
        if Ind.size:
            inds.append(Ind)
            L = l.extract(Ind) * ub2[Ind]
            U = u.extract(Ind) * lb2[Ind]
            lu.append((L, U))

        ind = logical_and(ind_positive, ind_z2)
        Ind = where(ind)[0]
        if Ind.size:
            inds.append(Ind)
            uu = u.extract(Ind)
            L = uu * lb2[Ind]
            U = uu * ub2[Ind]
            lu.append((L, U))
        
        ind = logical_and(ind_negative, ind_z2)
        Ind = where(ind)[0]
        if Ind.size:
            inds.append(Ind)
            ll = l.extract(Ind)
            L = ll * ub2[Ind]
            U = ll * lb2[Ind]
            lu.append((L, U))
#
#                    ind = logical_and(ind_z1, ind_other_positive)
#                    Ind = where(ind)[0]
#                    if Ind.size:
#                        print('8')
#                        inds.append(Ind)
#                        L = l.extract(Ind) * ub2[Ind]
#                        U = u.extract(Ind) * ub2[Ind]
#                        lu.append((L, U))
#                    
#                    ind = logical_and(ind_z1, ind_other_negative)
#                    Ind = where(ind)[0]
#                    if Ind.size:
#                        print('9')
#                        inds.append(Ind)
#                        L = u.extract(Ind) * lb2[Ind]
#                        U = l.extract(Ind) * lb2[Ind]
#                        lu.append((L, U))
#                        
        B = [Boundsurf(_l, _u, False, domain) for _l, _u in lu]
        rr = boundsurf_join(inds, B)
        rr.definiteRange = definiteRange
    R = Boundsurf(rr[0], rr[1], definiteRange, domain) if type(rr) == tuple else rr 
    return R

def mul_handle_nan(R, R1, R2, domain):
    if all(np.isfinite(R1)) and all(np.isfinite(R2)):
        return R
    RR = R.resolve()[0]
    R2_is_scalar = isscalar(R2)
    ind = logical_or(np.isnan(RR[0]), np.isnan(RR[1]))
#        ind_z1 = logical_or(lb1 == 0, ub1 == 0)
#        ind_z2 = logical_or(lb2 == 0, ub2 == 0)
#        ind_i1 = logical_or(np.isinf(lb1), np.isinf(ub1))
#        ind_i2 = logical_or(np.isinf(lb2), np.isinf(ub2))
#        ind = logical_or(logical_and(ind_z1, ind_i2), logical_and(ind_z2, ind_i1))
    if any(ind):
        lb1, ub1 = R1
        lb2, ub2 = (R2, R2) if R2_is_scalar or R2.size == 1 else R2
        lb1, lb2, ub1, ub2 = lb1[ind], lb2[ind], ub1[ind], ub2[ind] 
        R1, R2 = R1[:, ind], R2[:, ind]
        t = np.vstack((lb1 * lb2, ub1 * lb2, lb1 * ub2, ub1 * ub2))
        t_min, t_max = np.atleast_1d(nanmin(t, 0)), np.atleast_1d(nanmax(t, 0))
        
        # !!!!!!!!!!!!!!!!1 TODO: check it
        t = np.vstack((t_min, t_max))
        update_mul_inf_zero(R1, R2, t)
        t_min, t_max = t
        
        definiteRange_Tmp = \
        R.definiteRange if type(R.definiteRange) == bool or R.definiteRange.size == 1\
        else R.definiteRange[ind]
        R_Tmp_nan = boundsurf(surf({}, t_min), surf({}, t_max), definiteRange_Tmp, domain)
        R = R_Tmp_nan if all(ind) \
        else boundsurf_join((ind, logical_not(ind)), (R_Tmp_nan, R.extract(logical_not(ind))))
    return R

def b2mult(Self, Other):
    assert Self.level == Other.level == 1 and Self.b2equiv(Other)
    lc = Self.l.c * Other.l.c
    uc = Self.u.c * Other.u.c
    if len(Self.dep):
        k = list(Self.dep)[0]
        ld = {k: Self.l.c*Other.l.d.get(k, 0.0) + Other.l.c*Self.l.d.get(k, 0.0)}
        ud = {k: Self.u.c*Other.u.d.get(k, 0.0) + Other.u.c*Self.u.d.get(k, 0.0)}
        ld2 = {k: Other.l.d.get(k, 0.0) * Self.l.d.get(k, 0.0)}
        ud2 = {k: Other.u.d.get(k, 0.0) * Self.u.d.get(k, 0.0)}
    else:
        assert len(Other.dep) == 0
        return boundsurf(surf({}, lc), surf({}, uc), Self.definiteRange & Other.definiteRange, Self.domain)
        
    from boundsurf2 import surf2, boundsurf2
    ls, us = surf2(ld2, ld, lc), surf2(ud2, ud, uc)
    r = boundsurf2(ls, us, Self.definiteRange & Other.definiteRange, Self.domain)
    return r

def b2mult_direct(Self, Other):
    assert Self.level == Other.level == 1 and Self.b2equiv(Other) and Self.l is Self.u and Other.l is Other.u
    k = list(Self.dep)[0]
    s, o = Self.l, Other.l # = Self.u, Other.u 
    ld = {k: s.c * o.d.get(k, 0.0) + o.c * s.d.get(k, 0.0)}
    ld2 = {k: o.d.get(k, 0.0) * s.d.get(k, 0.0)}
    lc = s.c * o.c
    from boundsurf2 import surf2, boundsurf2
    ls = surf2(ld2, ld, lc)
    r = boundsurf2(ls, ls, Self.definiteRange & Other.definiteRange, Self.domain)
    return r

def b2div(Self, Other):
    # Self and Other must be nonnegative
    assert Other.level == 1 and Self.b2equiv(Other)
    DefiniteRange = Self.definiteRange & Other.definiteRange
    domain = Self.domain
    is_b2 = Self.level == 2
    
    k = list(Self.dep)[0]
    L, U = Self.domain[k]
    
    # L
    if is_b2:
        h = Self.l.d2.get(k, 0.0)
    d1, d2 = Self.l.d[k], Other.u.d[k]
    c1, c2 = Self.l.c, Other.u.c
    ind_Z_l = d2 == 0.0
    ind_z_l = where(ind_Z_l)[0]
    if ind_z_l.size:
        d_z_l = where(ind_Z_l, d1 / c2, 0.0)
        c_z_l = where(ind_Z_l, c1 / c2, 0.0)
        if is_b2:
            h_z_l = where(ind_Z_l, h / c2, 0.0)
    if is_b2:
        H1 = h / d2
        a1 = (d1 - h * c2 / d2) / d2
    else:
        a1 = d1 / d2
    b1 = c1 - a1 * c2

    ind_negative = b1<0
    ind_b_negative_l = where(ind_negative)[0]
    ind_b_positive_l = where(logical_not(ind_negative))[0]
    b1[ind_b_negative_l] = -b1[ind_b_negative_l]

    d = {k: d2}
    c = c2 
    s_l = surf(d, c)    
    
    # U
    if is_b2:
        h = Self.u.d2.get(k, 0.0)
    d1, d2 = Self.u.d[k], Other.l.d[k]
    c1, c2 = Self.u.c, Other.l.c
    ind_Z_u = d2 == 0.0
    ind_z_u = where(ind_Z_u)[0]
    if ind_z_u.size:
        d_z_u = where(ind_Z_u, d1 / c2, 0.0)
        c_z_u = where(ind_Z_u, c1 / c2, 0.0)
        if is_b2:
            h_z_u = where(ind_Z_u, h / c2, 0.0)
    if is_b2:
        H2 = h / d2
        a2 = (d1 - h * c2 / d2) / d2
    else:
        a2 = d1 / d2
    b2 = c1 - a2 * c2
    ind_negative = b2<0
    ind_b_negative_u = where(ind_negative)[0]
    ind_b_positive_u = where(logical_not(ind_negative))[0]
    b2[ind_b_negative_u] = -b2[ind_b_negative_u]

    d = {k: d2}
    c = c2 
    s_u = surf(d, c)
    
    tmp = boundsurf(s_l, s_u, DefiniteRange, domain)
    
    from Interval import inv_b_interval
    B = inv_b_interval(tmp, revert = False)[0]
    sl, su = B.l, B.u
    
    from boundsurf2 import boundsurf2, surf2
    P = 1e11
    sl2 = surf_join((ind_b_positive_l, ind_b_negative_l), \
    (sl.extract(ind_b_positive_l), -su.extract(ind_b_negative_l)))*b1 
    ind_numericaly_unstable_l = P * np.abs(sl2.c + a1) < np.abs(sl2.c) + np.abs(a1)
    sl2 += a1
    
    su2 = surf_join((ind_b_positive_u, ind_b_negative_u), \
    (su.extract(ind_b_positive_u), -sl.extract(ind_b_negative_u)))*b2 
    ind_numericaly_unstable_u = P * np.abs(su2.c + a2) < np.abs(su2.c) + np.abs(a2)
    su2 += a2
    
    if is_b2:
        ind_numericaly_unstable_l = logical_or(ind_numericaly_unstable_l, 
                                               P*np.abs(sl2.d.get(k, 0.0) + H1) < np.abs(sl2.d.get(k, 0.0)) + np.abs(H1))
        ind_numericaly_unstable_u = logical_or(ind_numericaly_unstable_u, 
                                               P*np.abs(su2.d.get(k, 0.0) + H2) < np.abs(su2.d.get(k, 0.0)) + np.abs(H2))
        sl2.d[k] = sl2.d.get(k, 0.0) + H1
        su2.d[k] = su2.d.get(k, 0.0) + H2
    
    if ind_z_l.size:
        ind_nz_l = where(logical_not(ind_Z_l))[0]
        sl2 = surf_join((ind_nz_l, ind_z_l), \
        (sl.extract(ind_nz_l), surf2({k:0}, {k:d_z_l}, c_z_l)))
        if is_b2:
            sl2.d2[k] = sl2.d2.get(k, 0.0) + h_z_l
    
    if ind_z_u.size:
        ind_nz_u = where(logical_not(ind_Z_u))[0]
        su2 = surf_join((ind_nz_u, ind_z_u), \
        (su.extract(ind_nz_u), surf2({k:0}, {k:d_z_u}, c_z_u)))
        if is_b2:
            su2.d2[k] = su2.d2.get(k, 0.0) + h_z_u

    r = boundsurf2(sl2, su2, DefiniteRange, domain)
    
    ind_numericaly_unstable = logical_or(ind_numericaly_unstable_l, ind_numericaly_unstable_u)
    if any(ind_numericaly_unstable):
        ind_numericaly_stable = logical_not(ind_numericaly_unstable)
#        print where(ind_numericaly_stable)[0].size, where(ind_numericaly_unstable)[0].size
        r2 = (Self.log() - Other.log()).exp()
        r = boundsurf_join((ind_numericaly_unstable, ind_numericaly_stable), \
        (r2.extract(ind_numericaly_unstable), r.extract(ind_numericaly_stable)))
    return r

def merge_boundsurfs(r1, r2):
    if r1 is None:
        return r2
    elif r2 is None:
        return r1
    if type(r1) == np.ndarray:
        r1 = boundsurf(surf({}, r1[0]), surf({}, r1[1]), r2.definiteRange, r2.domain)
    if type(r2) == np.ndarray:
        r2 = boundsurf(surf({}, r2[0]), surf({}, r2[1]), r1.definiteRange, r1.domain)
        
#    definiteRange = logical_or(r1.definiteRange, r2.definiteRange)
#    print all(isfinite(r1.resolve()[0])), all(isfinite(r2.resolve()[0]))

    domain = r1.domain
    k = list(r1.dep | r2.dep)[0]
    
    a1, b1, c1 = getattr(r1.l, 'd2', {k:0.0}).get(k, 0.0), r1.l.d.get(k, 0.0), r1.l.c
    a2, b2, c2 = getattr(r2.l,'d2', {k:0.0}).get(k, 0.0), r2.l.d.get(k, 0.0), r2.l.c
    lb, ub = domain[k]
    A, B = (lb**2 + lb*ub + ub**2) / 3.0, 0.5 * (lb + ub)
    
    diff_l = (a1-a2) * A + (b1-b2) * B + (c1-c2)
    # where r1.l better than r2.l
#        ind_l = diff_l  > 0.0
    
    a1, b1, c1 = getattr(r1.u,'d2', {k:0.0}).get(k, 0.0), r1.u.d.get(k, 0.0), r1.u.c
    a2, b2, c2 = getattr(r2.u,'d2', {k:0.0}).get(k, 0.0), r2.u.d.get(k, 0.0), r2.u.c
    lb, ub = domain[k]
    A, B = (lb**2 + lb*ub + ub**2) / 3.0, 0.5 * (lb + ub)
    
    diff_u = (a1-a2) * A + (b1-b2) * B + (c1-c2)
    # where r1.u better than r2.u
#        ind_u = diff_u  < 0.0
    
    
    # TODO: use ind_l, ind_u with surf processing
    
    ind = diff_l - diff_u > 0.0
        
    #debug
    #print int(np.log10(1e-300+np.max(np.abs(R1[1]-R1[0] - (R2[1]-R2[0])))))
    #debug end
    if all(ind):
        R = r1
    elif not any(ind):
        R = r2
    else:
        ind1, ind2 = ind, logical_not(ind)
        b1, b2 = r1.extract(ind1), r2.extract(ind2)
        R = boundsurf_join((ind1, ind2), (b1, b2))
    #R = r2
    
#    if not np.all(definiteRange):
#        ind1 = where(definiteRange)[0]
#        r1 = R.extract(ind1)
#        ind2 = where(logical_not(definiteRange))[0]
#        r2 = boundsurf(surf({}, new_l_resolved[ind2]), surf({}, new_u_resolved[ind2]), 
#        definiteRange[ind2] if type(definiteRange)==ndarray and definiteRange.size != 1 else definiteRange, 
#        domain)
#        R = boundsurf_join((ind1, ind2), (r1, r2))
    
    return R

