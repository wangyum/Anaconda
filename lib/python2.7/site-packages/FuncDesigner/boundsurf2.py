PythonSum = sum
import numpy as np
from numpy import logical_and, isscalar, any#, where

# for PyPy
from FDmisc import where

from boundsurf import surf, boundsurf, mul_fixed_interval, mul_handle_nan
#from multiarray import multiarray

from operator import gt as Greater, lt as Less

    
class surf2(surf):
    def __init__(self, d2, d, c):
        self.d2 = d2 # dict of variables and quadratic coefficients on them (probably as multiarrays)
        self.d = d # dict of variables and linear coefficients on them (probably as multiarrays)
        self.c = np.asarray(c) # (multiarray of) constant(s)
        
    value = lambda self, point: \
    self.c + \
    PythonSum(point[k] * v for k, v in self.d.items()) +\
    PythonSum(point[k]**2 * v for k, v in self.d2.items())
    
    def to_linear(self, domain, cmp):
        C = []
        D, D2 = self.d, self.d2
        new_D = D.copy()
        for k, d2 in D2.items():
            l, u = domain[k]#[0], domain[k][1]
            
            #d1 = D.pop(k, 0.0)
            d1 = D.get(k, 0.0)

            vals1, vals2 = (d2 * l + d1)*l, (d2*u + d1)*u

            ind = cmp(vals2, vals1)
            _r = where(ind, vals1, vals2)
            _argextr = where(ind, l, u)

            tops = -d1 / (2.0 * d2)
            ind_inside = logical_and(l < tops,  tops < u)
            #TODO: rework it as it was done in min/max
            if any(ind_inside):
                #assert 0, 'unimplemented'
                #print('asdf')
                top_vals = (d2*tops + d1) * tops
                ind_m = logical_and(ind_inside, cmp(_r, top_vals))
                _r = where(ind_m, top_vals, _r)
                _argextr = where(ind_m, tops, _argextr)
                
            extr_val = (d2 * _argextr + d1) * _argextr            
            tmp = d2*(u+l) + d1
            new_d1 = where(cmp(d2,0), d1 + 2 * d2 * _argextr, tmp)
            new_extr_val = where(cmp(new_d1, 0), l, u) * new_d1
            _r = extr_val - new_extr_val
            C.append(_r)
            new_D[k] = new_d1
                
        c = self.c + PythonSum(C)
#        print '----'
#        print _argextr
#        print D2, D, self.c
#        print new_D, c
        return surf(new_D, c)
    
    def exclude(self, domain, oovars, cmp):
        C = []
        D, D2 = self.d.copy(), self.d2.copy()
        for k in oovars:
            l, u = domain.get(k, (None, None))
            if l is None:
                continue # may be for fixed oovars
            d1, d2 = D.pop(k, 0.0), D2.pop(k, None)
            if d2 is None:
                C.append(where(cmp(d1, 0), l, u) * d1)
                continue
            #TODO: rework it as it was done in min/max
            rr = np.vstack(((d2 * l + d1)*l, (d2*u + d1)*u))
            rr.sort(axis=0)
            r_min, r_max = rr
            
            # check it
            _r = r_min if cmp == Greater else r_max
            
            #r_min = nanmin(rr, axis=0)
            tops = -d1 / (2.0 * d2)
            ind_inside = logical_and(l < tops,  tops < u)
            if any(ind_inside):
                top_vals = (d2*tops + d1) * tops
                ind_m = logical_and(ind_inside, cmp(_r, top_vals))
                _r = where(ind_m, top_vals, _r)
            C.append(_r)
        c = self.c + PythonSum(C)
        return surf2(D2, D, c)
        
        '''

        for v in oovars:
            tmp = d.pop(v, 0.0)
            if any(tmp):
                D = domain[v]
                C.append(where(cmp(tmp, 0), D[0], D[1])*tmp)
        c = self.c + PythonSum(C)
        return surf(d, c)
        '''
        
#    minimum = lambda self, domain, domain_ind = slice(None): \
#    self.c +\
#    PythonSum(where(v > 0, 
#    domain[k][0][domain_ind], domain[k][1][domain_ind])*v for k, v in self.d.items())
    def minimum(self, domain, domain_ind = slice(None)):#, reduceOnlyDomain = False):
        c = self.c
        oovars = set(self.d.keys()) | set(self.d2.keys())
        n = getattr(domain, 'nPoints',0)
        if n == 0:
            Vals = domain.values()
            n = np.asarray(Vals[0][0] if type(Vals) == list else next(iter(Vals))[0]).size
        active_domain_ind = type(domain_ind)==np.ndarray
        r = np.zeros(domain_ind.size if active_domain_ind else n) + c
        for k in oovars:
            l, u = domain[k][0][domain_ind], domain[k][1][domain_ind]
            d1, d2 = self.d.get(k, 0.0), self.d2.get(k, None)
#            if not reduceOnlyDomain and active_domain_ind:
#                if type(d1) == np.ndarray and d1.size != 1:
#                    d1 = d1[domain_ind]
#                if type(d2) == np.ndarray and d2.size != 1:
#                    d2 = d2[domain_ind]
            if d2 is None:
                r += where(d1 > 0, l, u) * d1
                continue
            
            t1, t2 = (d2 * l + d1)*l, (d2*u + d1)*u
            r_min = where(t1<t2, t1, t2)
            tops = -d1 / (2.0 * d2)
            
            ind_inside = logical_and(l < tops, tops < u)
            ind_inside = logical_and(ind_inside, d2 > 0)# d2 may be a scalar
            if any(ind_inside):
                top_vals = (d2*tops + d1) * tops
                # top_vals may be a scalar
                r_min = where(ind_inside, top_vals, r_min)
            r += r_min
        return r

    def maximum(self, domain, domain_ind = slice(None)):#, reduceOnlyDomain = False):
        c = self.c
        oovars = set(self.d.keys()) | set(self.d2.keys())
        n = getattr(domain, 'nPoints',0)
        if n == 0:
            Vals = domain.values()
            n = np.asarray(Vals[0][0] if type(Vals) == list else next(iter(Vals))[0]).size
        active_domain_ind = type(domain_ind)==np.ndarray
        r = np.zeros(domain_ind.size if active_domain_ind else n) + c
        for k in oovars:
            l, u = domain[k][0][domain_ind], domain[k][1][domain_ind]
            d1, d2 = self.d.get(k, 0.0), self.d2.get(k, None)
#            if not reduceOnlyDomain and active_domain_ind:
#                if type(d1) == np.ndarray and d1.size != 1:
#                    d1 = d1[domain_ind]
#                if type(d2) == np.ndarray and d2.size != 1:
#                    d2 = d2[domain_ind]
            if d2 is None:
                r += where(d1 < 0, l, u) * d1
                continue

            t1, t2 = (d2 * l + d1)*l, (d2*u + d1)*u
            r_max = where(t1 > t2, t1, t2)
                
            tops = -d1 / (2.0 * d2)
            ind_inside = logical_and(l < tops, tops < u)
            ind_inside = logical_and(ind_inside, d2 < 0) # d2 may be a scalar

            if any(ind_inside):
                top_vals = (d2*tops + d1) * tops
                # top_vals may be a scalar
                r_max = where(ind_inside, top_vals, r_max)
            r += r_max
        return r
        
    def extract(self, ind): 
#        if ind.dtype == bool:
#            ind = where(ind)[0]
        d = dict((k, v if v.size == 1 else v[ind]) for k, v in self.d.items()) 
        d2 = dict((k, v if v.size == 1 else v[ind]) for k, v in self.d2.items()) 
        C = self.c 
        c = C if C.size == 1 else C[ind]# if not isinstance(C, multiarray) else C[:, ind]
        return surf2(d2, d, c) 


    __neg__ = lambda self: surf2(dict((k, -v) for k, v in self.d2.items()), dict((k, -v) for k, v in self.d.items()), -self.c)
    
    def __add__(self, other):
        if type(other) in (surf, surf2):
#            if other.isRendered and not self.isRendered:
#                self, other = other, self
            S, O = self.d, other.d
            d = S.copy()
            d.update(O)
            for key in set(S.keys()) & set(O.keys()):
                d[key] = S[key]  + O[key]
            
            if type(other) == surf2:
                S, O = self.d2, other.d2
                d2 = S.copy()
                d2.update(O)
                for key in set(S.keys()) & set(O.keys()):
                    d2[key] = S[key]  + O[key]
            else:
                d2 = self.d2.copy()
            return surf2(d2, d, self.c+other.c)
        elif isscalar(other) or type(other) == np.ndarray:
            return surf2(self.d2, self.d, self.c + other)
        else:
            assert 0, 'unimplemented yet'
    
    def __mul__(self, other):
        isArray = type(other) == np.ndarray
        if isscalar(other) or isArray:
            return surf2(dict((k, v*other) for k, v in self.d2.items()), 
            dict((k, v*other) for k, v in self.d.items()), self.c * other)
#        elif type(other) == boundsurf:
#            return other * self.to_linear()
#        elif type(other) == boundsurf2:
#            return other.to_linear() * self.to_linear()
        else:
            assert 0, 'unimplemented yet'
            
    __rmul__ = __mul__
    
class boundsurf2(boundsurf):
    level = 2
#    def __init__(self, lowersurf, uppersurf, definiteRange, domain):
#        self.l = lowersurf
#        self.u = uppersurf
#        self.definiteRange = definiteRange
#        self.domain = domain
    def __init__(self, lowersurf, uppersurf, definiteRange, domain):
        boundsurf.__init__(self, lowersurf, uppersurf, definiteRange, domain, checkType = False)
#        assert all(all(val<1e5) for val in lowersurf.d2.values())
#        assert all(all(val>-1e5) for val in lowersurf.d2.values())
#        assert all(all(val<1e5) for val in uppersurf.d2.values())
#        assert all(all(val>-1e5) for val in uppersurf.d2.values())
#        print lowersurf.d2
#        print uppersurf.d2
    
    def exclude(self, oovars):
        L = self.l.exclude(self.domain, oovars, Greater)
        U = self.u.exclude(self.domain, oovars, Less)
        if len(L.d) != 0 or len(U.d) != 0 or len(L.d2) != 0 or len(U.d2) != 0:
            return boundsurf2(L, U, self.definiteRange, self.domain)
        else:
            return np.vstack((L.c, U.c))

    
    def extract(self, ind): 
        Ind = ind if ind.dtype != bool else where(ind)[0]
        definiteRange = self.definiteRange if type(self.definiteRange) == bool \
        or self.definiteRange.size == 1 else self.definiteRange[ind]
        return boundsurf2(self.l.extract(Ind), self.u.extract(Ind), definiteRange, self.domain)
    # TODO: handling fd.sum()
    
    def to_linear(self):
        L = self.l.to_linear(self.domain, Greater)
        U = self.u.to_linear(self.domain, Less)
        return boundsurf(L, U, self.definiteRange, self.domain)
    
    
    def __add__(self, other):
        if isscalar(other) or (type(other) == np.ndarray and other.size == 1):
            if self.l is self.u:
                # TODO: mb use id() instead of "is"
                tmp = self.l+other
                rr = (tmp, tmp)
            else:
                rr = (self.l+other, self.u+other)
            return boundsurf2(rr[0], rr[1], self.definiteRange, self.domain)
        elif type(other) in (boundsurf, boundsurf2):
            if self.l is self.u and other.l is other.u:
                # TODO: mb use id() instead of "is"
                tmp = self.l+other.l
                rr = (tmp, tmp)
            else:
                rr = (self.l+other.l, self.u+other.u)
            return boundsurf2(rr[0], rr[1], self.definiteRange & other.definiteRange, self.domain)
        elif type(other) == np.ndarray:
            assert other.shape[0] == 2, 'unimplemented yet'
            L = self.l + other[0]
            if self.l is self.u and np.array_equal(other[0], other[1]):
                # may be from fixed variables
                U = L
            else:
                U = self.u+other[1]
            return boundsurf2(L, U, self.definiteRange, self.domain)
        else:
            assert 0, 'unimplemented yet'
            
    __radd__ = __add__
    
    def __neg__(self):
        l, u = self.l, self.u
        if l is u:
            tmp = surf2(dict((k, -v) for k, v in u.d2.items()), dict((k, -v) for k, v in u.d.items()), -u.c)
            L, U = tmp, tmp
        else: 
            L = surf2(dict((k, -v) for k, v in u.d2.items()), dict((k, -v) for k, v in u.d.items()), -u.c)
            U = surf2(dict((k, -v) for k, v in l.d2.items()), dict((k, -v) for k, v in l.d.items()), -l.c)
        return boundsurf2(L, U, self.definiteRange, self.domain)
    
    def __mul__(self, other, resolveSchedule=()):
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
#            R2Positive = all(R2 >= 0)
#            R2Negative = all(R2 <= 0)
#            if not selfPositive and not selfNegative:
#                assert R2Positive or R2Negative, 'bug or unimplemented yet'
            
        if R2_is_scalar or (isArray and R2.size == 1):
            if self.l is self.u:
                tmp = self.l * R2
                rr = (tmp, tmp)
            else:
                rr = (self.l * R2, self.u * R2) if R2 >= 0 else (self.u * R2, self.l * R2)
            return boundsurf2(rr[0], rr[1], definiteRange, domain)
            
#        
#        selfPositive = all(R1 >= 0)
#        selfNegative = all(R1 <= 0)
        if isArray:
            r = mul_fixed_interval(self, R2)
            R1 = self.resolve()[0]
            R = mul_handle_nan(r, R1, R2, domain)
            return R
            
        # temporary
#        elif isBoundSurf:
#            return self.to_linear().__mul__(other, resolveSchedule)
#        elif isBoundSurf2:
#            return self.to_linear().__mul__(other.to_linear(), resolveSchedule)
        elif isBoundSurf or isBoundSurf2:
            return boundsurf.__mul__(self, other, resolveSchedule)
        else:
            assert 0, 'unimplemented yet'
        
        R = rr if type(rr) in (boundsurf, boundsurf2) else boundsurf2(rr[0], rr[1], definiteRange, domain)
        return R
        
    __rmul__ = __mul__

    
def apply_quad_lin(a, b, c, s):
    assert type(s) == surf
    D, C = s.d, s.c
    d2 = dict((k, a*v**2) for k, v in D.items())
    tmp = 2*a*C+b
    d = dict((k, v*tmp) for k, v in D.items())
    c_ = c + (a*C+b)*C
    return surf2(d2, d, c_)
