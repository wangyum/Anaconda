PythonSum = sum
PythonMax = max
PythonAny = any
PythonAll = all
import numpy as np
from FDmisc import FuncDesignerException, Diag, Eye, raise_except, \
diagonal, DiagonalType, dictSum, Vstack, Copy
from ooFun import atleast_oofun, oofun
from ooarray import ooarray
from Interval import nonnegative_interval, ZeroCriticalPointsInterval, \
box_1_interval, defaultIntervalEngine
from numpy import atleast_1d, logical_and
from FuncDesigner.multiarray import multiarray
from boundsurf import boundsurf, surf, devided_interval, boundsurf_join, split, merge_boundsurfs
from boundsurf2 import boundsurf2, surf2
from baseClasses import OOArray
    
try:
    from scipy.sparse import isspmatrix, lil_matrix as Zeros
    scipyInstalled = True
except ImportError:
    scipyInstalled = False
    isspmatrix = lambda *args, **kw: False
    Zeros = np.zeros 
    
__all__ = []

#class unary_oofun_overload:
#    def __init__(self, *args, **kwargs):
#        assert len(args) == 1 and len(kwargs) == 0
#        self.altFunc = args[0]
#
#    def __call__(self, *args, **kwargs):
#        assert len(args) == 1 and len(kwargs) == 0
#        if not isinstance(args[0], oofun):
#            return self.altFunc(*args)
#        return self.fun(*args, **kwargs)

#@unary_oofun_overload(np.sin)
#def sin(inp):
#    #if not isinstance(inp, oofun): return np.sin(inp)
#    def d(x):
#        return np.cos(x)
#    return oofun(lambda x: np.sin(x), inp, d = d)

try:
    import distribution
    hasStochastic = True
except:
    hasStochastic = False

#hasStochastic = False

def sin_cos_interval(r, inp, domain, dtype):
    is_cos = r.fun == st_cos
#    print('is_cos', is_cos)
    lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 1)
    
    if is_cos:
        # not inplace!
        lb_ub = lb_ub + np.pi / 2
        
    isBoundsurf = type(lb_ub) == boundsurf
    lb_ub_resolved = lb_ub.resolve()[0] if isBoundsurf else lb_ub
    lb, ub = lb_ub_resolved
    res = lb % (2 * np.pi)
    shift = lb - res
    lb, ub = res, ub - shift
    R0 = np.vstack((lb, ub))
    
    if isBoundsurf:
        c1 = ub <= np.pi
        c2 = logical_and(lb >= np.pi, ub <= 2*np.pi)# logical_and() is REQUIRED here
        c3 = logical_and(lb >= 1.5*np.pi, ub <= 2.5*np.pi)
        c4 = logical_and(lb >= 0.5*np.pi, ub <= 1.5*np.pi)
        Inds = split(c1, c2, c3, c4) 
        
        m = PythonSum(ind_.size for ind_ in Inds)
        inds, rr = [], []
        ind = Inds[0]
        if ind.size != 0:
            tmp = defaultIntervalEngine(lb_ub, np.sin, np.cos, np.nan, convexity = -1, 
                                        criticalPoint = np.pi/2, 
                                        criticalPointValue = 1, 
                                        domain_ind = ind, R0 = R0)[0]
            if ind.size == m:
                return tmp, tmp.definiteRange
            rr.append(tmp)
            inds.append(ind)
            
        ind = Inds[1]
        if ind.size != 0:
            tmp = defaultIntervalEngine(lb_ub, np.sin, np.cos, np.nan, convexity = 1, 
                                        criticalPoint = 3*np.pi/2, 
                                        criticalPointValue = -1, 
                                        domain_ind = ind, R0 = R0)[0]
            if ind.size == m:
                return tmp, tmp.definiteRange
            rr.append(tmp)
            inds.append(ind)
        
        ind = Inds[2]
        if ind.size != 0:
            tmp = defaultIntervalEngine(lb_ub, np.sin, np.cos, monotonity=1, convexity = 9, #10-1
                                        domain_ind = ind, R0 = R0)[0]
            if ind.size == m:
                return tmp, tmp.definiteRange
            rr.append(tmp)
            inds.append(ind)

        ind = Inds[3]
        if ind.size != 0:
            tmp = defaultIntervalEngine(lb_ub, np.sin, np.cos, monotonity=-1, convexity = -101, 
                                        domain_ind = ind, R0 = R0)[0]
            if ind.size == m:
                return tmp, tmp.definiteRange
            rr.append(tmp)
            inds.append(ind)

    ind = Inds[-1] if isBoundsurf else slice(None)
    R0 = R0[:, ind]
    lb, ub = R0
    #R = r.fun(R0)
    R = np.sin(R0)
    R.sort(axis=0)
    ind_minus_1 = logical_and(lb < 3*np.pi/2, ub > 3*np.pi/2)
    R[0][ind_minus_1] = -1.0
    ind_plus_1 = np.logical_or(
                            logical_and(lb < np.pi/2, ub > np.pi/2), 
                            logical_and(lb < 5*np.pi/2, ub > 5*np.pi/2)
                            )
    R[1][ind_plus_1] = 1.0
    
    if not isBoundsurf or ind.size == m:
        return R, definiteRange
    else:
        definiteRange_ = definiteRange if type(definiteRange) == bool or definiteRange.size == 1 \
        else definiteRange[ind]
        tmp = boundsurf(surf({}, R[0]), surf({}, R[1]), definiteRange_, domain)
        rr.append(tmp)
        inds.append(ind)
        b = boundsurf_join(inds, rr)
        return b, b.definiteRange
#    return oofun._interval_(r, domain, dtype)

st_sin = (lambda x: \
distribution.stochasticDistribution(sin(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([sin(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.sin(x))\
if hasStochastic\
else np.sin

def sin(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([sin(elem) for elem in inp])
    elif hasStochastic and isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(sin(inp.values), inp.probabilities.copy())._update(inp)
    elif not isinstance(inp, oofun): return np.sin(inp)
    r = oofun(st_sin, inp, engine = 'sin', 
                 d = lambda x: Diag(np.cos(x)), 
                 vectorized = True)
    r._interval_ = lambda domain, dtype: sin_cos_interval(r, inp, domain, dtype)
    return r

st_cos = (lambda x: \
distribution.stochasticDistribution(cos(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([cos(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.cos(x))\
if hasStochastic\
else np.cos

def cos(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([cos(elem) for elem in inp])
    elif hasStochastic and isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(cos(inp.values), inp.probabilities.copy())._update(inp)
    elif not isinstance(inp, oofun): return np.cos(inp)
    r = oofun(st_cos, inp, engine = 'cos', 
                 d = lambda x: Diag(-np.sin(x)), 
                 vectorized = True)
    r._interval_ = lambda domain, dtype: sin_cos_interval(r, inp, domain, dtype)
    return r
#cos = lambda inp: sin(inp+np.pi/2)

st_tan = (lambda x: \
distribution.stochasticDistribution(tan(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([tan(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.tan(x))\
if hasStochastic\
else np.tan

def tan_interval(inp, r, domain, dtype):
    lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 1)
    isBoundSurf = type(lb_ub) == boundsurf
    lb, ub = lb_ub.resolve()[0] if isBoundSurf else lb_ub
    if np.any(lb < -np.pi/2) or np.any(ub > np.pi/2):
        raise FuncDesignerException('interval for tan() is unimplemented for range beyond (-pi/2, pi/2) yet')        
    return devided_interval(inp, r, domain, dtype)
    
def tan(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([tan(elem) for elem in inp])
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(tan(inp.values), inp.probabilities.copy())._update(inp)       
    if not isinstance(inp, oofun): return np.tan(inp)
    # TODO: move it outside of tan definition
    r = oofun(st_tan, inp, d = lambda x: Diag(1.0 / np.cos(x) ** 2), vectorized = True, \
    engine_monotonity = 1, convexities = (-1, 1), engine = 'tan')
    r._interval_ = lambda domain, dtype: tan_interval(inp, r, domain, dtype)
    return r
    
__all__ += ['sin', 'cos', 'tan']

# TODO: cotan?

# TODO: rework it with matrix ops
#get_box1_DefiniteRange = lambda lb, ub: logical_and(np.all(lb >= -1.0), np.all(ub <= 1.0))

st_arcsin = (lambda x: \
distribution.stochasticDistribution(arcsin(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([arcsin(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.arcsin(x))\
if hasStochastic\
else np.arcsin

def arcsin(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([arcsin(elem) for elem in inp])
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(arcsin(inp.values), inp.probabilities.copy())._update(inp)       
    if not isinstance(inp, oofun): 
        return np.arcsin(inp)
    r = oofun(st_arcsin, inp, d = lambda x: Diag(1.0 / np.sqrt(1.0 - x**2)), vectorized = True, 
    engine_monotonity = 1, convexities = (-1, 1), engine = 'arcsin')
#    r.getDefiniteRange = get_box1_DefiniteRange
    r._interval_ = lambda domain, dtype: box_1_interval(inp, r, np.arcsin, domain, dtype)
    r.attach((inp>-1)('arcsin_domain_lower_bound_%d' % r._id, tol=-1e-7), (inp<1)('arcsin_domain_upper_bound_%d' % r._id, tol=-1e-7))
    return r

st_arccos = (lambda x: \
distribution.stochasticDistribution(arccos(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([arccos(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.arccos(x))\
if hasStochastic\
else np.arccos


def arccos(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([arccos(elem) for elem in inp])
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(arccos(inp.values), inp.probabilities.copy())._update(inp)     
    if not isinstance(inp, oofun): return np.arccos(inp)
    r = oofun(st_arccos, inp, d = lambda x: Diag(-1.0 / np.sqrt(1.0 - x**2)), vectorized = True, 
    engine_monotonity = -1, convexities = (1, -1), engine = 'arccos')
#    r.getDefiniteRange = get_box1_DefiniteRange
    r._interval_ = lambda domain, dtype: box_1_interval(inp, r, np.arccos, domain, dtype)
    r.attach((inp>-1)('arccos_domain_lower_bound_%d' % r._id, tol=-1e-7), (inp<1)('arccos_domain_upper_bound_%d' % r._id, tol=-1e-7))
    return r

st_arctan = (lambda x: \
distribution.stochasticDistribution(arctan(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([arctan(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.arctan(x))\
if hasStochastic\
else np.arctan

def arctan(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([arctan(elem) for elem in inp])    
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(arctan(inp.values), inp.probabilities.copy())._update(inp)             
    if not isinstance(inp, oofun): return np.arctan(inp)
    r = oofun(st_arctan, inp, d = lambda x: Diag(1.0 / (1.0 + x**2)), 
                 vectorized = True, engine_monotonity = 1, convexities = (1, -1), engine = 'arctan')
    r._interval_ = lambda domain, dtype: devided_interval(inp, r, domain, dtype)
    return r

__all__ += ['arcsin', 'arccos', 'arctan']

st_sinh = (lambda x: \
distribution.stochasticDistribution(sinh(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([sinh(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.sinh(x))\
if hasStochastic\
else np.sinh

def sinh(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([sinh(elem) for elem in inp])        
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(sinh(inp.values), inp.probabilities.copy())._update(inp)        
    if not isinstance(inp, oofun): return np.sinh(inp)
    r = oofun(st_sinh, inp, d = lambda x: Diag(np.cosh(x)), vectorized = True, 
    engine_monotonity = 1, convexities = (-1, 1), engine = 'sinh')
    r._interval_ = lambda domain, dtype: devided_interval(inp, r, domain, dtype)
    return r

#def asdf(x):
##    print (1, type(x))
##    if isinstance(x, np.ndarray):
##        print('1>', x.shape)
##        print(x)
##        if isinstance(x[0], np.ndarray):
##            print(2, type(x[0]), x[0].shape)
##    if isinstance(x, multiarray):
##        print('-----')
##        print (x.shape, x.view(np.ndarray).shape)
##        print([type(elem) for elem in x.flat])
##        print '===='
#    r = distribution.stochasticDistribution(cosh(x.values), x.probabilities.copy())._update(x) \
#        if isinstance(x, distribution.stochasticDistribution)\
#        else np.array([cosh(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray)\
#        else np.cosh(x)
#    return r
#
#st_cosh = (asdf)\
#if hasStochastic\
#else np.cosh


st_cosh = \
(lambda x: \
distribution.stochasticDistribution(cosh(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([cosh(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.cosh(x))\
if hasStochastic\
else np.cosh

def cosh(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([cosh(elem) for elem in inp])        
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(cosh(inp.values), inp.probabilities.copy())._update(inp)                
    if not isinstance(inp, oofun): 
        return np.cosh(inp)
    r =oofun(st_cosh, inp, d = lambda x: Diag(np.sinh(x)), engine_convexity = 1, vectorized = True, \
    _interval_=ZeroCriticalPointsInterval(inp, np.cosh), engine = 'cosh')
    return r
    
__all__ += ['sinh', 'cosh']

st_tanh = (lambda x: \
distribution.stochasticDistribution(tanh(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([tanh(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.tanh(x))\
if hasStochastic\
else np.tanh

def tanh(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([tanh(elem) for elem in inp])       
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(tanh(inp.values), inp.probabilities.copy())._update(inp)              
    if not isinstance(inp, oofun): return np.tanh(inp)
    r = oofun(st_tanh, inp, d = lambda x: Diag(1.0/np.cosh(x)**2), vectorized = True, 
    engine_monotonity = 1, convexities = (1, -1), engine = 'tanh')
    r._interval_ = lambda domain, dtype: devided_interval(inp, r, domain, dtype)
    return r
    
st_arctanh = (lambda x: \
distribution.stochasticDistribution(arctanh(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([arctanh(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.arctanh(x))\
if hasStochastic\
else np.arctanh

def arctanh(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([arctanh(elem) for elem in inp])        
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(arctanh(inp.values), inp.probabilities.copy())._update(inp)          
    if not isinstance(inp, oofun): return np.arctanh(inp)
    r = oofun(st_arctanh, inp, d = lambda x: Diag(1.0/(1.0-x**2)), vectorized = True, 
    engine_monotonity = 1, convexities = (-1, 1), engine = 'arctanh')
#    r.getDefiniteRange = get_box1_DefiniteRange
    r._interval_ = lambda domain, dtype: box_1_interval(inp, r, np.arctanh, domain, dtype)
    return r

__all__ += ['tanh', 'arctanh']

st_arcsinh = (lambda x: \
distribution.stochasticDistribution(arcsinh(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([arcsinh(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.arcsinh(x))\
if hasStochastic\
else np.arcsinh

def arcsinh(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([arcsinh(elem) for elem in inp])        
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(arcsinh(inp.values), inp.probabilities.copy())._update(inp)      
    if not isinstance(inp, oofun): return np.arcsinh(inp)
    r = oofun(st_arcsinh, inp, d = lambda x: Diag(1.0/np.sqrt(1+x**2)), 
    vectorized = True, engine_monotonity = 1, convexities = (1, -1), engine = 'arcsinh')
    r._interval_ = lambda domain, dtype: devided_interval(inp, r, domain, dtype)
    return r

st_arccosh = (lambda x: \
distribution.stochasticDistribution(arccosh(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([arccosh(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.arccosh(x))\
if hasStochastic\
else np.arccosh

def arccosh(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([arccosh(elem) for elem in inp])        
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(arccosh(inp.values), inp.probabilities.copy())._update(inp)      
    if not isinstance(inp, oofun): return np.arccosh(inp)
    r = oofun(st_arccosh, inp, d = lambda x: Diag(1.0/np.sqrt(x**2-1.0)), vectorized = True, 
    engine_monotonity = 1, engine_convexity = -1, engine = 'arccosh')
    F0, shift = 0.0, 1.0
    r._interval_ = lambda domain, dtype: nonnegative_interval(inp, np.arccosh, r.d, domain, dtype, F0, shift)
    return r

__all__ += ['arcsinh', 'arccosh']

def angle(inp1, inp2):
    # returns angle between 2 vectors
    # TODO: 
    # 1) handle zero vector(s)
    # 2) handle small numerical errors more properly
    #     (currently they are handled via constraint attached to arccos)
    return arccos(PythonSum(inp1*inp2)/sqrt(sum(inp1**2)*sum(inp2**2)))

st_exp = (lambda x: \
distribution.stochasticDistribution(exp(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([exp(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.exp(x))\
if hasStochastic\
else np.exp

def get_exp_b2_coeffs(ll, uu, dll, duu, c_l, c_u):
    ind_z =  np.logical_or(uu == ll, c_u == np.inf)
    
    #L
    #L2, U2 = dll * ll + c_l, dll * uu + c_l
    #ind = L2<U2
    #l2 = np.where(ind, L2, U2)
    d = dll#np.where(ind, dll, duu)
    ind = d > 0
    l = np.where(ind, ll, uu)
    
    l2 = l * d + c_l
    
    exp_l2 = exp(l2)

    a = d**2 * exp_l2 * 0.5 
    b = d * exp_l2 * (1.0 - d * l)
    a[ind_z] = b[ind_z] = 0.0
    c = exp_l2 - (a * l + b) * l
    koeffs_l = (a, b, c)
    
    
    #U
#    L2, U2 = duu * ll + c_u, duu * uu + c_u
#    ind = L2<U2
#    l2, u2 = np.where(ind, L2, U2), np.where(ind, U2, L2)
    d = duu#np.where(ind, dll, duu)
    ind = d > 0
    l, u = np.where(ind, ll, uu), np.where(ind, uu, ll)
    
    l2, u2 = l * d + c_u, u * d + c_u
    
    exp_u2, exp_l2 = exp(u2), exp(l2)
    
    a = (exp_u2 - exp_l2 + (l-u) * d * exp_l2) * (u-l) ** -2.0
    b = d * exp_l2 - 2 * a * l
    ind_z = np.logical_or(ind_z, np.isinf(a))
    a[ind_z] = b[ind_z] = 0.0
    c = exp_u2 - (a * u + b) * u
    koeffs_u = (a, b, c)
    
    return koeffs_l, koeffs_u
    
def exp_interval(r, inp, domain, dtype):
    lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 2)
    
    #!!!!! Temporary !!!!
    ia_lvl_2_unavailable = type(lb_ub) == np.ndarray or len(lb_ub.dep) != 1
    is_b2 = type(lb_ub) == boundsurf2
    
    if ia_lvl_2_unavailable or is_b2:
        r1, definiteRange = oofun._interval_(r, domain, dtype)
    else:
        r1 = None
        
    if ia_lvl_2_unavailable:
        return r1, definiteRange
        
    return exp_b_interval(lb_ub, r1, definiteRange, domain)

def exp_b_interval(lb_ub, r1, definiteRange, domain):
    if type(lb_ub) == boundsurf2:
        lb_ub = lb_ub.to_linear()
        
    k = list(lb_ub.dep)[0]
    l, u = domain[k]
    d_l, d_u = lb_ub.l.d[k], lb_ub.u.d[k]
    c_l, c_u = lb_ub.l.c, lb_ub.u.c 
    
    koeffs_l, koeffs_u = get_exp_b2_coeffs(l, u, d_l, d_u, c_l, c_u)
    
    # L
    a, b, c = koeffs_l
    L = surf2({k:a}, {k:b}, c)
#    D, C = lb_ub.l.d[k], lb_ub.l.c
#    A, B, C = a * D**2, (2*a*C + b) * D, (a * C + b) * C + c
#    L = surf2({k:A}, {k:B}, C)

    
    # U
    a, b, c = koeffs_u
    U = surf2({k:a}, {k:b}, c)
#    from numpy import linspace
#    x = linspace(l, u, 1000)
#    import pylab
#    pylab.plot(x, exp(d_l*x+c_l), 'b')
#    pylab.plot(x, exp(d_u*x+c_u), 'g')
#    pylab.plot(x, koeffs_l[0]*x**2+koeffs_l[1]*x+koeffs_l[2], 'r')
#    pylab.plot(x, koeffs_u[0]*x**2+koeffs_u[1]*x+koeffs_u[2], 'k')
#    pylab.show()
#    pass
    
#    D, C = lb_ub.u.d[k], lb_ub.u.c
#    A, B, C = a * D**2, (2*a*C + b) * D, (a * C + b) * C + c
#    U = surf2({k:A}, {k:B}, C)
#    U = surf2({k:0}, r1.u.d, r1.u.c)
    
    r2 = boundsurf2(L, U, definiteRange, domain)
    R = merge_boundsurfs(r1, r2)
    return R, definiteRange

def exp(inp):
    if isinstance(inp, ooarray):
        return ooarray([exp(elem) for elem in inp])         
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(exp(inp.values), inp.probabilities.copy())._update(inp)      
    if not isinstance(inp, oofun): return np.exp(inp)
    r = oofun(st_exp, inp, d = lambda x: Diag(np.exp(x)), vectorized = True, 
    engine_convexity = 1, engine_monotonity = 1, engine = 'exp')
    r._interval_ = lambda domain, dtype: exp_interval(r, inp, domain, dtype)
    return r

#st_sqrt = (lambda x: \
#distribution.stochasticDistribution(sqrt(x.values), x.probabilities.copy())._update(x) \
#if isinstance(x, distribution.stochasticDistribution)\
#else np.array([sqrt(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
#else np.sqrt(x))\
#if hasStochastic\
#else np.sqrt

def sqrt(inp, attachConstraints = True):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([elem ** 0.5 for elem in inp])
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(sqrt(inp.values), inp.probabilities.copy())._update(inp)      
    if not isinstance(inp, oofun): 
        return np.sqrt(inp)
#    r = oofun(st_sqrt, inp, d = lambda x: Diag(0.5 / np.sqrt(x)), vectorized = True, 
#    engine_monotonity = 1, engine_convexity = -1)
#    r._interval_ = lambda domain, dtype: nonnegative_interval(inp, np.sqrt, r.d, domain, dtype, 0.0)
    r = inp ** 0.5
    r.engine = 'sqrt'
    if attachConstraints: r.attach((inp>0)('sqrt_domain_zero_bound_%d' % r._id, tol=-1e-7))
    return r

__all__ += ['angle', 'exp', 'sqrt']

st_abs = (lambda x: \
distribution.stochasticDistribution(abs(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([abs(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.abs(x))\
if hasStochastic\
else np.abs

def abs(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([abs(elem) for elem in inp])
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(abs(inp.values), inp.probabilities.copy())._update(inp)      
    if not isinstance(inp, oofun): return np.abs(inp)
    
    r = oofun(st_abs, inp, d = lambda x: Diag(np.sign(x)), vectorized = True, 
    _interval_ = ZeroCriticalPointsInterval(inp, np.abs), engine = 'abs')
    return r
    
__all__ += ['abs']

def get_log_b2_coeffs(L, U, d_l, d_u, c_l, c_u):
    # L
    d = d_l
    ind = d > 0
    l, u = np.where(ind, L, U), np.where(ind, U, L)
    
    koeffs_l = get_inner_coeffs(np.log, lambda x: 1.0/x, d, l, u, d_l, d_u, c_l, c_u, 
                                pointCase='u', lineCase='l', feasLB = 0.0)

    # U
    d = d_u
    ind = d > 0
    l, u = np.where(ind, L, U), np.where(ind, U, L)
    
    point = d*u + c_u
    f = log(point)
    df = d / point
    d2f = - df**2
    koeffs_u = get_outer_coeffs(u, f, df, d2f)
    
    return koeffs_l, koeffs_u
    
def log_b_interval(lb_ub, r1):
    definiteRange, domain = lb_ub.definiteRange, lb_ub.domain
    if type(lb_ub) == boundsurf2:
        lb_ub = lb_ub.to_linear()
    
    k = list(lb_ub.dep)[0]
    l, u = domain[k]
    d_l, d_u = lb_ub.l.d[k], lb_ub.u.d[k]
    c_l, c_u = lb_ub.l.c, lb_ub.u.c 
    
    koeffs_l, koeffs_u = get_log_b2_coeffs(l, u, d_l, d_u, c_l, c_u)
    
    # L
    a, b, c = koeffs_l
    L = surf2({k:a}, {k:b}, c)
    
    # U
    a, b, c = koeffs_u
    U = surf2({k:a}, {k:b}, c)
#########################
#    from numpy import linspace
#    x = linspace(l, u, 10000)
#    import pylab
#    pylab.plot(x, log(d_l*x+c_l), 'b', linewidth = 2)
#    pylab.plot(x, log(d_u*x+c_u), 'r', linewidth = 2)
#    pylab.plot(x, koeffs_l[0]*x**2+koeffs_l[1]*x+koeffs_l[2], 'b', linewidth = 1)
#    pylab.plot(x, koeffs_u[0]*x**2+koeffs_u[1]*x+koeffs_u[2], 'r', linewidth = 1)
#    pylab.show()
#########################
    definiteRange = logical_and(definiteRange, c_l+d_l*np.where(d_l>0, l, u)>=0)
    r2 = boundsurf2(L, U, definiteRange, domain)
    R = merge_boundsurfs(r1, r2)
    
    return R, definiteRange
    
def log_interval(inp, domain, dtype):
    lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 2)
    
    #!!!!! Temporary !!!!
    ia_lvl_2_unavailable =  type(lb_ub) == np.ndarray or len(lb_ub.l.d) > 1 or len(lb_ub.u.d) > 1 or len(lb_ub.dep) != 1
    is_b2 = type(lb_ub) == boundsurf2
    
    if ia_lvl_2_unavailable or is_b2:
        r1, definiteRange = nonnegative_interval(inp, np.log, lambda x: 1.0 / x, domain, dtype, 0.0)
    else:
        r1 = None
    
    if ia_lvl_2_unavailable:
        return r1, definiteRange

    return log_b_interval(lb_ub, r1)

st_log = (lambda x: \
distribution.stochasticDistribution(log(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([log(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.log(x))\
if hasStochastic\
else np.log

def log(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([log(elem) for elem in inp])    
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(log(inp.values), inp.probabilities.copy())._update(inp)      
    if not isinstance(inp, oofun): return np.log(inp)
    d = lambda x: Diag(1.0/x)
    r = oofun(st_log, inp, d = d, vectorized = True, engine_monotonity = 1, engine_convexity = -1, 
              engine = 'log')
    #r._interval_ = lambda domain, dtype: nonnegative_interval(inp, np.log, r.d, domain, dtype, 0.0)
    r._interval_ = lambda domain, dtype: log_interval(inp, domain, dtype)
    r.attach((inp>1e-300)('log_domain_zero_bound_%d' % r._id, tol=-1e-7))
    return r

st_log10 = (lambda x: \
distribution.stochasticDistribution(log10(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([log10(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.log10(x))\
if hasStochastic\
else np.log10

INV_LOG_10 = 1.0 / np.log(10)
def log10_interval(inp, domain, dtype):
    r, definiteRange = log_interval(inp, domain, dtype)
    r *= INV_LOG_10
    return r, definiteRange
    
def log10(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([log10(elem) for elem in inp])    
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(log10(inp.values), inp.probabilities.copy())._update(inp)              
    if not isinstance(inp, oofun): return np.log10(inp)
    d = lambda x: Diag(INV_LOG_10 / x)
    r = oofun(st_log10, inp, d = d, vectorized = True, engine_monotonity = 1, engine_convexity = -1, 
              engine = 'log10')
    #r._interval_ = lambda domain, dtype: nonnegative_interval(inp, np.log10, r.d, domain, dtype, 0.0)
    r._interval_ = lambda domain, dtype: log10_interval(inp, domain, dtype)
    r.attach((inp>1e-300)('log10_domain_zero_bound_%d' % r._id, tol=-1e-7))
    return r

st_log2 = (lambda x: \
distribution.stochasticDistribution(log2(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([log2(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.log2(x))\
if hasStochastic\
else np.log2

INV_LOG_2 = 1.0 / np.log(2)
def log2_interval(inp, domain, dtype):
    r, definiteRange = log_interval(inp, domain, dtype)
    r *= INV_LOG_2
    return r, definiteRange
    
def log2(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([log2(elem) for elem in inp])    
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(log2(inp.values), inp.probabilities.copy())._update(inp)       
    if not isinstance(inp, oofun): return np.log2(inp)
    d = lambda x: Diag(INV_LOG_2/x)
    r = oofun(st_log2, inp, d = d, vectorized = True, engine_monotonity = 1, engine_convexity = -1, 
              engine = 'log2')
#    r._interval_ = lambda domain, dtype: nonnegative_interval(inp, np.log2, r.d, domain, dtype, 0.0)
    r._interval_ = lambda domain, dtype: log2_interval(inp, domain, dtype)
    r.attach((inp>1e-300)('log2_domain_zero_bound_%d' % r._id, tol=-1e-7))
    return r

__all__ += ['log', 'log2', 'log10']


def f_dot(x, y):
    if x.size == 1 or y.size == 1:
        return x*y
    if isinstance(y, multiarray) and not isinstance(x, multiarray):
        return dot(x, y.T).T
    return np.dot(x, y)

def d_dot(x, y):
    if y.size == 1: 
        r = np.empty_like(x)
        r.fill(y)
        return Diag(r)
    else:
        return y

def dot(inp1, inp2):
    if not isinstance(inp1, oofun) and not isinstance(inp2, oofun): return np.dot(inp1, inp2)
    r = oofun(f_dot, [inp1, inp2], d=(lambda x, y: d_dot(x, y), lambda x, y: d_dot(y, x)), engine = 'dot')
    r.getOrder = lambda *args, **kwargs: (inp1.getOrder(*args, **kwargs) if isinstance(inp1, oofun) else 0) + (inp2.getOrder(*args, **kwargs) if isinstance(inp2, oofun) else 0)
    #r.isCostly = True
    return r

def cross_d(x, y):
    assert x.size == 3 and y.size == 3, 'currently FuncDesigner cross(x,y) is implemented for arrays of length 3 only'
    return np.array([[0, -y[2], y[1]], [y[2], 0, -y[0]], [-y[1], y[0], 0]])
    
def cross(a, b):
    if not isinstance(a, oofun) and not isinstance(b, oofun): return np.cross(a, b)
   
    r = oofun(np.cross, [a, b], d=(lambda x, y: -cross_d(x, y), lambda x, y: cross_d(y, x)), engine = 'cross')
    r.getOrder = lambda *args, **kwargs: \
    (a.getOrder(*args, **kwargs) if isinstance(a, oofun) else 0)\
    + (b.getOrder(*args, **kwargs) if isinstance(b, oofun) else 0)
    return r

__all__ += ['dot', 'cross']

def ceil(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([ceil(elem) for elem in inp])        
    if not isinstance(inp, oofun): return np.ceil(inp)
    r = oofun(lambda x: np.ceil(x), inp, vectorized = True, engine_monotonity = 1, engine = 'ceil')
    r._D = lambda *args, **kwargs: raise_except('derivative for FD ceil is unimplemented yet')
    return r

def floor(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([floor(elem) for elem in inp])        
    if not isinstance(inp, oofun): return np.floor(inp)
    r = oofun(lambda x: np.floor(x), inp, vectorized = True, engine_monotonity = 1, engine = 'floor')
    r._D = lambda *args, **kwargs: raise_except('derivative for FD floor is unimplemented yet')
    return r

st_sign = (lambda x: \
distribution.stochasticDistribution(sign(x.values), x.probabilities.copy())._update(x) \
if isinstance(x, distribution.stochasticDistribution)\
else np.array([sign(elem) for elem in x.flat]).view(multiarray) if isinstance(x, multiarray) and isinstance(x.flat[0], distribution.stochasticDistribution)
else np.sign(x))\
if hasStochastic\
else np.sign

def sign(inp):
    if isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp)):
        return ooarray([sign(elem) for elem in inp])
    if hasStochastic and  isinstance(inp, distribution.stochasticDistribution):
        return distribution.stochasticDistribution(sign(inp.values), inp.probabilities.copy())._update(inp)      
    if not isinstance(inp, oofun): 
        return np.sign(inp)
    r = oofun(st_sign, inp, vectorized = True, d = lambda x: 0.0, engine_monotonity = 1, engine = 'sign')
    return r

__all__ += ['ceil', 'floor', 'sign']


def sum_engine(r0, *args):
    if not hasStochastic:
        return PythonSum(args) + r0
    Args, Args_st = [], {}
    for elem in args:
        if isinstance(elem, distribution.stochasticDistribution):
            stDep = frozenset(elem.stochDep.keys())
            tmp = Args_st.get(stDep, None)
            if tmp is None:
                Args_st[stDep] = [elem]
            else:
                Args_st[stDep].append(elem)
        else:
            Args.append(elem)
    r = PythonSum(Args) + r0
    if len(Args_st) == 0:
        return r
    
    # temporary
    for key, val in Args_st.items():
        maxDistributionSize = val[0].maxDistributionSize
        break
    stValues = Args_st.values()
#            stValues = Args_st.values()
#            T = list(set(stValues))[0]
#            maxDistributionSize = next(iter(T)).maxDistributionSize
    r1 = 0.0
    for elem in stValues:
        tmp = PythonSum(elem)
        r1 = tmp + r1 
        r1.reduce(maxDistributionSize)
    r1 = r1 + r
    r1.maxDistributionSize = maxDistributionSize
    return r1 

def sum_interval(R0, r, INP, domain, dtype):
#    if len(INP) <= 10:
#        B = []
#        _r = [R0]
#        DefiniteRange = True
#        for inp in INP:
#            arg_lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 2)
#            DefiniteRange = np.logical_and(DefiniteRange, definiteRange)
#            if type(arg_lb_ub) in (boundsurf, boundsurf2):
#                B.append(arg_lb_ub)
#            else:
#                _r.append(arg_lb_ub)
#        _r = PythonSum(_r)
#        R = _r if len(B) == 0 else boundsurf_sum(B, _r, DefiniteRange, domain)
#        return R, DefiniteRange
        
    v = domain.modificationVar
    if v is not None:
        
        # self already must be in domain.storedSums
        R, DefiniteRange = domain.storedSums[r][-1]
        
        if isinstance(R, np.ndarray) and R.dtype == object:#array of stochasticDistribution

            has_infs = not np.all(np.hstack([np.isfinite(R[0, i].values) for i in range(R.shape[1])])) \
            or not np.all(np.hstack([np.isfinite(R[1, i].values) for i in range(R.shape[1])]))
        else:
            has_infs = not (np.all(np.isfinite(R)) if type(R) not in (boundsurf, boundsurf2) else R.isfinite())
        
        if has_infs:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!   TODO: implement ia_surf_level = 1 here
            R = np.asarray(R0, dtype).copy()
            if domain.isMultiPoint:
                R = np.tile(R, (1, len(list(domain.values())[0][0])))
                #R = np.tile(R, (1, len(domain.values()[0][0])))
            #DefiniteRange = True
            #####################
            # !!! don't use sum([inp._interval(domain, dtype) for ...]) here
            # to reduce memory consumption
            for inp in INP:
                arg_lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 2)
#                DefiniteRange = logical_and(DefiniteRange, definiteRange)
                if type(R)==type(arg_lb_ub)==np.ndarray and R.shape == arg_lb_ub.shape and R.dtype == arg_lb_ub.dtype:
                    R += arg_lb_ub
                else:
                    R = R + arg_lb_ub
            #####################
            return R, DefiniteRange

        #R = R.copy() - domain.storedSums[r][v]
        if type(R) == np.ndarray:
            assert type(domain.storedSums[r][v]) == np.ndarray
            R = (R - domain.storedSums[r][v])# not inplace!
        else:
            # boundsurf
            R = R.direct_sub(domain.storedSums[r][v])
            
#        if R.__class__ == boundsurf:
#            R = R.resolve()[0] 
        R2 = np.zeros((2, 1))
        B = []
        for inp in r.storedSumsFuncs[v]:
            # TODO: mb rework definiteRange processing ?
            arg_lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 2)
            DefiniteRange = logical_and(DefiniteRange, definiteRange)

            if type(arg_lb_ub) == np.ndarray:
                if R2.shape == arg_lb_ub.shape and R2.dtype == arg_lb_ub.dtype:
                    R2 += arg_lb_ub
                else:
                    R2 = R2  + arg_lb_ub
            else:
                B.append(arg_lb_ub)

        if type(R) in (boundsurf, boundsurf2):
            B.append(R)
            R = boundsurf_sum(B, R2, DefiniteRange, domain)
            R.definiteRange = logical_and(R.definiteRange, DefiniteRange)
        elif len(B):
            R = boundsurf_sum(B, R+R2, DefiniteRange, domain)#.resolve()[0]
        else:
            R = R + R2
#        if type(R) == boundsurf and not domain.surf_preference:# and R.Size() > 5:
#            R = R.resolve()[0]

        #R -= domain.storedSums[r][v]
        
#        # To supress inf-inf=nan, however, it doesn't work properly yet, other code is used
#        if np.any(np.isinf(arg_lb_ub)):
#            R[arg_lb_ub == np.inf] = np.inf
#            R[arg_lb_ub == -np.inf] = -np.inf
        
        return R, DefiniteRange
    
    D = {}

    #assert np.asarray(r0).ndim <= 1
    #R = np.asarray(R0, dtype).copy()
    R = np.asarray(R0).copy()
    if domain.isMultiPoint:
        R = np.tile(R, (1, domain.nPoints))
        #R = np.tile(R, (1, len(list(domain.values())[0][0])))

    #####################
    # !!! don't use sum([inp._interval(domain, dtype) for ...]) here
    # to reduce memory consumption
    DefiniteRange = True
    B = []
    for inp in INP:
        arg_lb_ub, definiteRange = inp._interval(domain, dtype, ia_surf_level = 2)
        Tmp = inp._getDep() if not inp.is_oovar else [inp]
        for oov in Tmp:
            tmp = D.get(oov, None)
            if tmp is None:
                D[oov] = arg_lb_ub.copy()
            else:
                if type(tmp)==type(arg_lb_ub)==np.ndarray and  tmp.shape == arg_lb_ub.shape and tmp.dtype == arg_lb_ub.dtype:
                    D[oov] += arg_lb_ub
                    # tmp += arg_lb_ub is not used here because tmp can be boundsurf 
                    # and inplace operations are unimplemented yet
                else:
                    # may be of different shape, e.g. for a fixed variable
                    D[oov] = tmp + arg_lb_ub
        
        DefiniteRange = logical_and(DefiniteRange, definiteRange)
        if type(arg_lb_ub) in (boundsurf, boundsurf2):
            B.append(arg_lb_ub)
        elif type(R) == np.ndarray == type(arg_lb_ub) and R.shape == arg_lb_ub.shape and R.dtype == arg_lb_ub.dtype:
            R += arg_lb_ub
        else:
            R = R + arg_lb_ub
            
    #####################
    if len(B):
        R = boundsurf_sum(B, R, DefiniteRange, domain)

#        if 1 or R.Size() > 5:
#            R = R.resolve()[0]
#        D = dict((k, v.resolve()[0] if type(v) in (boundsurf, boundsurf2) else v) for k, v in D.items())

#    if R.__class__ == boundsurf and R.Size() > 15:
#        R.render(domain)
        
    if v is None: 
        D[-1] = R, DefiniteRange
        
    domain.storedSums[r] = D
    
    return R, DefiniteRange

    
def boundsurf_sum(B, s, DefiniteRange, domain):
    
    sameBounds = np.array_equal(s[0], s[1]) and PythonAll(b.l is b.u for b in B)
    L = PythonSum(b.l.c for b in B) + s[0]
    U = L if sameBounds else PythonSum(b.u.c for b in B) + s[1]
    
    ##############################
    # dictSum works with Python lists, not iterables!
    Ld = dictSum([b.l.d for b in B])
    Ud = Ld if sameBounds else dictSum([b.u.d for b in B])
    ##############################
    
    l2 = [elem for elem in (getattr(b.l, 'd2', None) for b in B) if elem is not None]
    u2 = l2 if sameBounds else [elem for elem in (getattr(b.u, 'd2', None) for b in B) if elem is not None]

    if len(l2) == len(u2) == 0:
        if sameBounds:
            s1 = s2 = surf(Ld, L)
        else:
            s1, s2 = surf(Ld, L), surf(Ud, U)
        return boundsurf(s1, s2, DefiniteRange, domain)
    else:
        Ld2 = dictSum(l2)
        Ud2 = Ld2 if sameBounds else dictSum(u2)
        if sameBounds:
            s1 = s2 = surf2(Ld2, Ld, L)
        else:
            s1, s2 = surf2(Ld2, Ld, L), surf2(Ud2, Ud, U)
        return boundsurf2(s1, s2, DefiniteRange, domain)

def sum_derivative(r_, r0, INP, dep, point, fixedVarsScheduleID, Vars=None, fixedVars = None, useSparse = 'auto'):
    # TODO: handle involvePrevData
    # TODO: handle fixed vars
    
    r = {}
   
    isSP = hasattr(point, 'maxDistributionSize') and point.maxDistributionSize != 0
    
    for elem in INP:
        if isinstance(elem, ooarray):
            elem = hstack(elem)
        if not elem.is_oovar and (elem.input is None or len(elem.input)==0 or elem.input[0] is None): 
            continue # TODO: get rid if None, use [] instead
        if elem.discrete: continue
        
        # TODO: code cleanup 
        if elem.is_oovar:
            if (fixedVars is not None and elem in fixedVars) or (Vars is not None and elem not in Vars): continue
            sz = np.asarray(point[elem]).size
            tmpres = Eye(sz) if not isinstance(point[elem], multiarray) else np.ones(sz).view(multiarray)
            r_val = r.get(elem, None)
            if isSP:
                if r_val is not None:
                    r_val.append(tmpres)
                else:
                    r[elem] = [tmpres]
            else:
                if r_val is not None:
                    if sz != 1 and isinstance(r_val, np.ndarray) and not isinstance(tmpres, np.ndarray): # i.e. tmpres is sparse matrix
                        tmpres = tmpres.toarray()
                    elif not np.isscalar(r_val) and not isinstance(r_val, np.ndarray) and isinstance(tmpres, np.ndarray):
                        r[elem] = r_val.toarray()
                    Tmp = tmpres.resolve(True) if isspmatrix(r[elem]) and type(tmpres) == DiagonalType else tmpres
                    try:
                        r[elem] += Tmp
                    except:
                        r[elem] = r[elem] + Tmp
                else:
                    # TODO: check it for oovars with size > 1
                    r[elem] = tmpres
        else:
            tmp = elem._D(point, fixedVarsScheduleID, Vars, fixedVars, useSparse = useSparse)
            for key, val in tmp.items():
                r_val = r.get(key, None)
                if isSP:
                    if r_val is not None:
                        r_val.append(val)
                    else:
                        r[key] = [val]
                else:
                    if r_val is not None:
                        if not np.isscalar(val) and isinstance(r_val, np.ndarray) and not isinstance(val, np.ndarray): # i.e. tmpres is sparse matrix
                            val = val.toarray()
                        elif not np.isscalar(r_val) and not isinstance(r_val, np.ndarray) and isinstance(val, np.ndarray):
                            r[key] = r_val.toarray()
                        
                        if isspmatrix(r_val) and type(val) == DiagonalType:
                            val = val.resolve(True)
                        elif isspmatrix(val) and type(r_val) == DiagonalType:
                            r[key] = r_val.resolve(True)
                        
                        # TODO: rework it
                        try:
                            r[key] += val
                        except:
                            r[key] = r_val + val
                    else:
                        r[key] = Copy(val)
    
    if isSP:
        for key, val in r.items():
            r[key] = sum_engine(0.0, *val)
            
    
    if useSparse is False:
        for key, val in r.items():
            #if np.isscalar(val): val = np.asfarray(val)
            if hasattr(val, 'toarray'):# and not isinstance(val, multiarray): # i.e. sparse matrix
                r[key] = val.toarray()

    if not isSP:
        # TODO: rework it, don't recalculate each time
        Size = np.asarray(r0).size
        if Size == 1 and not point.isMultiPoint:
            if r_._lastFuncVarsID == fixedVarsScheduleID:
                if not np.isscalar(r_._f_val_prev):
                    Size = r_._f_val_prev.size
            else:
                Size = np.asarray(r_._getFuncCalcEngine(point, Vars = Vars, fixedVars = fixedVars, fixedVarsScheduleID = fixedVarsScheduleID)).size

        if Size != 1 and not point.isMultiPoint:
            for key, val in r.items():
                if not isinstance(val, diagonal):
                    if np.isscalar(val) or np.prod(val.shape) <= 1:
                        tmp = np.empty((Size, 1))
                        tmp.fill(val if np.isscalar(val) else val.item())
                        r[key] = tmp
                    elif val.shape[0] != Size:
                        tmp = np.tile(val, (Size, 1))
                        r[key] = tmp
    #                    elif np.asarray(val).size !=1:
    #                        raise_except('incorrect size in FD sum kernel')
    
    return r

def sum_getOrder(INP, *args, **kwargs):
    orders = [0]+[inp.getOrder(*args, **kwargs) for inp in INP]
    return PythonMax(orders)


def sum(inp, *args, **kwargs):
    if type(inp) == np.ndarray and inp.dtype != object:
        return np.sum(inp, *args, **kwargs)
        
    if isinstance(inp, ooarray) and inp.dtype != object:
        inp = inp.view(np.ndarray)
        
    cond_ooarray = isinstance(inp, ooarray) and any(isinstance(elem, oofun) for elem in atleast_1d(inp))
    if cond_ooarray and inp.size == 1: 
        return np.asscalar(inp).sum()
    condIterableOfOOFuns = type(inp) in (list, tuple) or cond_ooarray
    
    if not isinstance(inp, oofun) and not condIterableOfOOFuns: 
        return np.sum(inp, *args, **kwargs)

    if isinstance(inp, ooarray) and PythonAny(isinstance(elem, oofun) for elem in atleast_1d(inp)): 
        inp = inp.tolist()

    if condIterableOfOOFuns:
        INP, r0 = [], 0.0
        for elem in inp: # TODO: mb use reduce() or something like that
            if not isinstance(elem, (oofun, ooarray)): 
                # not '+=' because size can be changed from 1 to another value
                r0 = r0 + np.asanyarray(elem) # so it doesn't work for different sizes
                continue
            INP.append(elem)
        if len(INP) == 0:
            return r0
        
        r = oofun(lambda *args: sum_engine(r0, *args), INP, _isSum = True)
        r._summation_elements = INP if np.isscalar(r0) and r0 == 0.0 else INP + [r0]

        r.storedSumsFuncs = {}
        for inp in INP:
            Dep = [inp] if isinstance(inp, oofun) and inp.is_oovar else inp.dep
            for v in Dep:
                if v not in r.storedSumsFuncs:
                    r.storedSumsFuncs[v] = set()
                r.storedSumsFuncs[v].add(inp)
                                
        # TODO:  check for fixed inputs
        
        r.getOrder = lambda *args, **kw: sum_getOrder(INP, *args, **kw)
        
        R0 = np.tile(r0, (2, 1))

        r._interval_ = lambda *args, **kw: sum_interval(R0, r, INP, *args, **kw)
        r.vectorized = True
        r_dep = r._getDep()
        r._D = lambda *args, **kw: sum_derivative(r, r0, INP, r_dep, *args, **kw)
        r.isCostly = True
        
        def expression(*args, **kw):
            Elems = [elem.expression(**kw) if isinstance(elem, oofun) else str(elem) for elem in INP]
            r = []
            for i in range(len(Elems)):
                r.append(Elems[i] +  (' + ' if i != len(Elems)-1 and Elems[i+1][0] != '-' else ' '))
            rr = ''.join(r)[:-1]
            if not np.array_equal(r0, 0.0):
                str_r0 = str(r0)
                rr += ' + ' + str_r0 if str_r0[0] != '-' else ' - ' + str_r0[1:]
            return rr
        r.expression = expression
        
        return r
    else: 
        return inp.sum(*args, **kwargs)#np.sum(inp, *args, **kwargs)
    
    
def prod(inp, *args, **kwargs):
    if not isinstance(inp, oofun): 
        if isinstance(inp, np.ndarray) and not isinstance(inp, OOArray):
            return np.prod(inp, *args, **kwargs)
        from ooFun import PythonProd
        return PythonProd(inp, *args, **kwargs)#could be improved for big ooarrays 
    if len(args) != 0 or len(kwargs) != 0:
        raise FuncDesignerException('oofun for prod(x, *args,**kwargs) is not implemented yet')
    #r.getOrder = lambda *args, **kwargs: prod([(1 if not isinstance(inp, oofun) else inp.getOrder(*args, **kwargs)) for inp in self.input])
    return inp.prod()

# Todo: implement norm_1, norm_inf etc
def norm(*args, **kwargs):
    if len(kwargs) or len(args) > 1:
        return np.linalg.norm(*args, **kwargs)
        
    r = sqrt(sum(args[0]**2),  attachConstraints=False)

    if isinstance(r, oofun) and len(kwargs) == 0:
        assert len(args) == 1 or args[1] == 2, 'FuncDesigner norm() is implemented for n = 2 only'
        r.engine = 'norm2'
        r._norm_arg = args[0]#used in SOCP
    else:
        assert 0, 'FuncDesigner norm() is implemented for n = 2 only'
    return r
 
__all__ += ['sum', 'prod', 'norm']

#def stack(*args, **kwargs):
#    assert len(kwargs) == 0 and len(args) != 0
#    if len(args) == 1:
#        assert type(args[0]) in (list, tuple)
#        if not any([isinstance(arg, oofun) for arg in args[0]]): return np.hstack(args)
#        #f = lambda *Args: np.hstack([arg(Args) if isinstance(arg, oofun) else arg for arg in args[0]])
#        def f(*Args): 
#            r = np.hstack([arg.fun(Args) if isinstance(arg, oofun) else arg for arg in args[0]])
#            print '1:', r
#            raise 0
#            return r
#        #d = lambda *Args: np.hstack([arg.d(Args).reshape(-1, 1) if isinstance(arg, oofun) else np.zeros((len(arg))) for arg in args[0]])
#        def d(*Args):
#            r = np.hstack([arg.d(Args).reshape(-1, 1) if isinstance(arg, oofun) else np.zeros((len(arg))) for arg in args[0]])
#            print '2:', r
#            return r
#        print 'asdf', args[0]
#        return oofun(f, args[0], d=d)
#    else:
#        raise FuncDesignerException('unimplemented yet')
#        #assert isinstance(args[0], oofun) 
        
    

#def norm(inp, *args, **kwargs):
#    if len(args) != 0 or len(kwargs) != 0:
#        raise FuncDesignerException('oofun for norm(x, *args,**kwargs) is not implemented yet')
#    
#    #np.linalg.norm
#    f = lambda x: np.sqrt(np.sum(x**2))
#    
#    r = oofun(f, inp, isCostly = True)
#    
#    def d(x):
#        
#    
#    #r.d = lambda *args, **kwargs: 
#        
#        #s = r(x)
#        #return Diag(x /  s if s != 0 else np.zeros(x.size)) # however, dirivative doesn't exist in (0,0,..., 0)
#    r.d = d
#    
#    return r
    

def size(inp, *args, **kwargs):
    if not isinstance(inp, oofun): return np.size(inp, *args, **kwargs)
    return inp.size
    
def ifThenElse(condition, val1, val2, *args, **kwargs):
    
    # for future implementation
    assert len(args) == 0 and len(kwargs) == 0 
    Val1 = atleast_oofun(val1)#fixed_oofun(val1) if not isinstance(val1, oofun) else val1
    #if np.isscalar(val1): raise 0
    Val2 = atleast_oofun(val2)#fixed_oofun(val2) if not isinstance(val2, oofun) else val2
    if isinstance(condition, bool): 
        return Val1 if condition else Val2
    elif isinstance(condition, oofun):
        f = lambda conditionResult, value1Result, value2Result: value1Result if conditionResult else value2Result
        # !!! Don't modify it elseware function will evaluate both expressions despite of condition value 
        r = oofun(f, [condition, val1, val2], engine = 'ifThenElse')
        r.D = lambda point, *args, **kwargs: (Val1.D(point, *args, **kwargs) if isinstance(Val1, oofun) else {}) if condition(point) else \
        (Val2.D(point, *args, **kwargs) if isinstance(Val2, oofun) else {})
        r._D = lambda point, *args, **kwargs: (Val1._D(point, *args, **kwargs) if isinstance(Val1, oofun) else {}) if condition(point) else \
        (Val2._D(point, *args, **kwargs) if isinstance(Val2, oofun) else {})
        r.d = errFunc
        
        # TODO: try to set correct value from val1, val2 if condition is fixed
#        def getOrder(Vars=None, fixedVars=None, *args, **kwargs):
#            dep = condition.getDep()
#            if Vars is not None and dep.is

        return r
    else:
        raise FuncDesignerException('ifThenElse requires 1st argument (condition) to be either boolean or oofun, got %s instead' % type(condition))

__all__ += ['size', 'ifThenElse']

def decision(*args, **kwargs):
    pass
        
def max(inp,  *args,  **kwargs): 
    if type(inp) in (list, tuple, np.ndarray) \
    and (len(args) == 0 or len(args) == 1 and not isinstance(args[0], oofun)) \
    and not any(isinstance(elem, oofun) for elem in (inp if type(inp) in (list, tuple) else np.atleast_1d(inp))):
        return np.max(inp, *args, **kwargs)
        
    assert len(args) == len(kwargs) == 0, 'incorrect data type in FuncDesigner max or not implemented yet'
    
    if isinstance(inp, oofun):
        f = lambda x: np.max(x)
#        def f(x):
#            print np.max(x)
#            return np.max(x)
        def d(x):
            df = inp.d(x)
            ind = np.argmax(x)
            return df[ind, :]
        def interval(domain, dtype):
            lb_ub, definiteRange = inp._interval(domain, dtype)
            tmp1, tmp2 = lb_ub[0], lb_ub[1]
            return np.vstack((np.max(np.vstack(tmp1), 0), np.max(np.vstack(tmp2), 0))), np.all(definiteRange, 0)
        r = oofun(f, inp, d = d, size = 1, _interval_ = interval)
    elif type(inp) in (list, tuple, ooarray):
        f = lambda *args: np.max([arg for arg in args])
        def interval(domain, dtype):
            arg_inf, arg_sup, tmp, DefiniteRange = [], [], -np.inf, True
            for _inp in inp:
                if isinstance(_inp, oofun):
                    #tmp1, tmp2 = _inp._interval(domain, dtype)
                    lb_ub, definiteRange = _inp._interval(domain, dtype)
                    tmp1, tmp2 = lb_ub[0], lb_ub[1]
                    arg_inf.append(tmp1)
                    arg_sup.append(tmp2)
                    DefiniteRange = logical_and(DefiniteRange, definiteRange)
                elif tmp < _inp:
                    tmp = _inp
            r1, r2 = np.max(np.vstack(arg_inf), 0), np.max(np.vstack(arg_sup), 0)
            r1[r1<tmp] = tmp
            r2[r2<tmp] = tmp
            return np.vstack((r1, r2)), DefiniteRange
        r = oofun(f, inp, size = 1, _interval_ = interval, engine = 'max')
        def _D(point, *args, **kwargs):
            ind = np.argmax([(s(point) if isinstance(s, oofun) else s) for s in r.input])
            return r.input[ind]._D(point, *args, **kwargs) if isinstance(r.input[ind], oofun) else {}
        r._D = _D
    else:
        return np.max(inp, *args, **kwargs)
    return r        
    
def min(inp,  *args,  **kwargs): 
    if type(inp) in (list, tuple, np.ndarray) \
    and (len(args) == 0 or len(args) == 1 and not isinstance(args[0], oofun))\
    and not any(isinstance(elem, oofun) for elem in (inp if type(inp) in (list, tuple) else np.atleast_1d(inp))):
        return np.min(inp, *args, **kwargs)
    
    assert len(args) == len(kwargs) == 0, 'incorrect data type in FuncDesigner min or not implemented yet'
    if isinstance(inp, oofun):
        f = lambda x: np.min(x)
        def d(x):
            df = inp.d(x)
            #df = inp.d(x) if type(inp.d) not in (list, tuple) else np.hstack([item(x) for item in inp.d])
            ind = np.argmin(x)
            return df[ind, :]
        def interval(domain, dtype):
            lb_ub, definiteRange = inp._interval(domain, dtype)
            tmp1, tmp2 = lb_ub[0], lb_ub[1]
            return np.vstack((np.min(np.vstack(tmp1), 0), np.min(np.vstack(tmp2), 0))), np.all(definiteRange, 0)
        r = oofun(f, inp, d = d, size = 1, _interval_ = interval)
    elif type(inp) in (list, tuple, ooarray):
        f = lambda *args: np.min([arg for arg in args])
        def interval(domain, dtype):
            arg_inf, arg_sup, tmp, DefiniteRange = [], [], np.inf, True
            for _inp in inp:
                if isinstance(_inp, oofun):
                    lb_ub, definiteRange = _inp._interval(domain, dtype)
                    tmp1, tmp2 = lb_ub[0], lb_ub[1]
                    arg_inf.append(tmp1)
                    arg_sup.append(tmp2)
                    DefiniteRange = logical_and(DefiniteRange, definiteRange)
                elif tmp > _inp:
                    tmp = _inp
            r1, r2 = np.min(np.vstack(arg_inf), 0), np.min(np.vstack(arg_sup), 0)
            if np.isfinite(tmp):
                r1[r1>tmp] = tmp
                r2[r2>tmp] = tmp
            return np.vstack((r1, r2)), DefiniteRange
            
        r = oofun(f, inp, size = 1, _interval_ = interval, engine = 'min')
        def _D(point, *args, **kwargs):
            ind = np.argmin([(s(point) if isinstance(s, oofun) else s) for s in r.input])
            return r.input[ind]._D(point, *args, **kwargs) if isinstance(r.input[ind], oofun) else {}
        r._D = _D
    else:
        return np.min(inp, *args, **kwargs)
    return r        


__all__ += ['min', 'max']

#def fixed_oofun(Val):
#    val = np.asfarray(Val)
#    f = lambda: Val
#    r = oofun(f, input=[])
#    r._D = lambda *args,  **kwargs: {}
#    r.D = lambda *args,  **kwargs: {}
#    r.discrete = True
#    return r

det3 = lambda a, b, c: a[0] * (b[1]*c[2] - b[2]*c[1]) - a[1] * (b[0]*c[2] - b[2]*c[0]) + a[2] * (b[0]*c[1] - b[1]*c[0]) 

__all__ += ['det3']


def hstack(tup): # overload for oofun[ind]
    c = [isinstance(t, (oofun, ooarray)) for t in tup]
    if any(isinstance(t, ooarray) for t in tup):
        return ooarray(np.hstack(tup))
    if not any(c):
        return np.hstack(tup)
    #an_oofun_ind = np.where(c)[0][0]
    f = lambda *x: np.hstack(x).flatten()
    
    
  
#    def d(*x): 
#
#        r = [elem.d(x[i]) if c[i] else None for i, elem in enumerate(tup)]
#        size = atleast_1d(r[an_oofun_ind]).shape[0]
#        r2 = [elem if c[i] else Zeros(size) for elem in r]
#        return r2
        
        #= lambda *x: np.hstack([elem.d(x) if c[i] else elem for elem in tup])
            
#        f = lambda x: x[ind] 
#        def d(x):
#            Xsize = Len(x)
#            condBigMatrix = Xsize > 100 
#            if condBigMatrix and scipyInstalled:
#                r = SparseMatrixConstructor((1, x.shape[0]))
#                r[0, ind] = 1.0
#            else: 
#                if condBigMatrix and not scipyInstalled: self.pWarn(scipyAbsentMsg)
#                r = zeros_like(x)
#                r[ind] = 1
#            return r
    def getOrder(*args, **kwargs):
        orders = [0]+[inp.getOrder(*args, **kwargs) for inp in tup]
        return np.max(orders)
    
            
    r = oofun(f, tup, getOrder = getOrder, engine = 'hstack')
    
    #!!!!!!!!!!!!!!!!! TODO: sparse 

    
    def _D(*args,  **kwargs): 
        # TODO: rework it, especially if sizes are fixed and known
        # TODO: get rid of fixedVarsScheduleID
        sizes = [(t(args[0], fixedVarsScheduleID = kwargs.get('fixedVarsScheduleID', -1)) if c[i] else np.asarray(t)).size for i, t in enumerate(tup)]
        
        tmp = [elem._D(*args,  **kwargs) if c[i] else None for i, elem in enumerate(tup)]
        res = {}
        for v in r._getDep():
            Temp = []
            for i, t in enumerate(tup):
                if c[i]:
                    temp = tmp[i].get(v, None)
                    if temp is not None:
                        Temp.append(temp if type(temp) != DiagonalType else temp.resolve(kwargs['useSparse']))
                    else:
#                        T = next(iter(tmp[i].values()))
#                        sz = T.shape[0] if type(T) == DiagonalType else np.atleast_1d(T).shape[0]
                        Temp.append((Zeros if sizes[i] * np.asarray(args[0][v]).size > 1000 else np.zeros)((sizes[i], np.asarray(args[0][v]).size)))
                else:
                    sz = np.atleast_1d(t).shape[0]
                    Temp.append(Zeros((sz, 1)) if sz > 100 else np.zeros(sz))
            rr = Vstack([elem for elem in Temp])
            #print type(rr)
            res[v] = rr if not isspmatrix(rr) or 0.3 * prod(rr.shape) > rr.size else rr.toarray()
            #print type(res[v])
        return res
    r._D = _D
    return r

__all__ += ['hstack']

# TODO: move the func into fdmisc.py
def errFunc(*args,  **kwargs): 
    # this function shouldn't be ever called, an FD kernel hack has been involved
    raise FuncDesignerException('error in FuncDesigner kernel, inform developers')

#for func in (sin, arctan):
#    i0 = func._interval
#    def f2(domain, dtype):
#        if type(domain) == dict:
#            return i0(domain, dtype)
#        r = domain.storedIntervals.get(self, None)
#        if r is None:
#            r = i0(domain, dtype)
#            domain.storedIntervals[self] = r
#        return r
#    func._interval = f2

def get_inner_coeffs(func, func_d, d, l, u, d_l, d_u, c_l, c_u, pointCase, lineCase, feasLB = -np.inf):
    if lineCase == 'u': # parabola must be upper the func
        ll, uu = d_u * l + c_u, d_u * u + c_u
    else: # parabola must be below the func
        ll, uu = d_l * l + c_l, d_l * u + c_l
    
    ind_infeas = False
    if feasLB != -np.inf:
        ind_infeas = logical_and(ll<feasLB, uu>feasLB)
        ll[ind_infeas] = feasLB
    f_l, f_u = func(ll), func(uu)

    if pointCase == 'u':
        df_u = func_d(uu)
        a = -(f_u - f_l - d * df_u * (u-l)) * (u-l)**-2
        b = d * df_u - 2 * a * u
    else:
        assert pointCase == 'l'
        df_l = func_d(ll)
        a = (f_u - f_l - d * df_l * (u-l)) * (u-l)**-2
        b = d * df_l - 2 * a * l
        
    ind_z = np.logical_or(l == u, np.logical_not(np.isfinite(b)))
    P = 1e10
    #ind_numericaly_unstable = P  < np.abs(a * l) + np.abs(b)
    ind_numericaly_unstable = np.logical_or(P  < np.abs(a * l), P < np.abs(b))
    
    ind_z = np.logical_or(ind_z, ind_numericaly_unstable)
    ind_z = np.logical_or(ind_z, ind_infeas)
    a[ind_z] = b[ind_z] = 0.0
    
    c = f_l - (a * l + b) * l
#    if np.all(np.isfinite(f_l)):
#        c = f_l - (a * l + b) * l
#    elif np.all(np.isfinite(f_u)):
#        c = f_u - (a * u + b) * u
#    else:
#        c = np.where(np.isfinite(f_l), f_l - (a * l + b) * l, f_u - (a * u + b) * u)
    return a, b, c

def get_outer_coeffs(point, f, df, d2f):
    return d2f / 2.0, df - point * d2f, f - point * df + point ** 2 * d2f / 2.0
    
