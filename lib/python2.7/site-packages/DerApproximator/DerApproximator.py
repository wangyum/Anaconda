"""
finite-difference derivatives approximation
made by Dmitrey
"""

try:
    import numpypy as numpy
except:
    pass

from numpy import isfinite, empty, ndarray, abs, asarray, isnan, array, all
from numpy import float32, float64
floatTypes = [float32, float64, float]
try:
    from numpy import float128
    floatTypes.append(float128)
except ImportError:
    pass
try:
    from numpy import float16
    floatTypes.append(float16)
except ImportError:
    pass

# asfarray
try:
    from numpy import asfarray
except ImportError:
    asfarray = lambda elem: elem if type(elem) == ndarray and elem.dtype in floatTypes else array(elem, float)

# isscalar
try:
    from numpy import isscalar
except ImportError:
    from numpy import int32, int64 
    scalarTypes = [int, int32, int64] + floatTypes

    isscalar = lambda elem: type(elem) in scalarTypes

# asscalar
try:
    from numpy import asscalar
except ImportError:
    asscalar = lambda elem: elem if isscalar(elem) else elem.item()
    
# atleast_1d
try:
    from numpy import atleast_1d
except ImportError:
    def atleast_1d(X):
        x = X if type(X) == ndarray else asarray(X)
        return x if x.ndim >= 1 else reshape(x,(1,))

# atleast_2d
try:
    from numpy import atleast_2d
except ImportError:
    from numpy import reshape
    def atleast_2d(X):
        x = X if type(X) == ndarray else asarray(X)
        return x if x.ndim >= 2 else reshape(x,(1, x.size))

# hstack
try:
    from numpy import hstack
except ImportError:
    from numpy import concatenate
    hstack = lambda arg: concatenate(arg, 1)

class DerApproximatorException:
    def __init__(self,  msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def get_d1(fun, vars, diffInt=1.5e-8, pointVal = None, args=(), stencil = 3, varForDifferentiation = None, exactShape = False):
    """
    Usage: get_d1(fun, x, diffInt=1.5e-8, pointVal = None, args=(), stencil = 3, varForDifferentiation = None, exactShape = False)
    fun: R^n -> R^m, x: Python list (not tuple!) or numpy array from R^n: function and point where derivatives should be obtained 
    diffInt - step for stencil
    pointVal - fun(x) if known (it is used from OpenOpt and FuncDesigner)
    args - additional args for fun, if not equalk to () then fun(x, *args) will be involved 
    stencil = 1: (f(x+diffInt) - f(x)) / diffInt
    stencil = 2: (f(x+diffInt) - f(x-diffInt)) / (2*diffInt)
    stencil = 3: (-f(x+2*diffInt) + 8*f(x+diffInt) - 8*f(x-diffInt) + f(x-2*diffInt)) / (12*diffInt)
    varForDifferentiation - the parameter is used from FuncDesigner
    exactShape - set True to forbid possible flattering for 1D arrays
    """
    assert type(vars) in [tuple,  list,  ndarray, float, dict]
    #assert asarray(diffInt).size == 1,  'vector diffInt are not implemented for oofuns yet'      
    diffInt = atleast_1d(diffInt)
    if atleast_1d(diffInt).size > 1: assert type(vars) == ndarray, 'not implemented yet'
    
    if type(vars) == tuple:
        Vars = [asfarray(var) for var in vars]
    elif type(vars) not in [list, tuple] or isscalar(vars[0]):
        Vars = [vars, ]
    else: 
        Vars = list(vars)
        # TODO: IMPLEMENT CHECK FOR SAME VARIABLES IN INPUT
        #if len(set(tuple(Vars))) != len(Vars):
            #raise DerApproximatorException('currently DerApproximator can handle only different input variables')
    
    if type(args) != tuple:
        args = (args, )
    Args = list(tuple(asfarray(v) for v in Vars) + args)

    if pointVal is None:
        v_0 = atleast_1d(fun(*Args))
    else:
        v_0 = pointVal
    if v_0.ndim >= 2: 
        raise DerApproximatorException('Currently DerApproximatorx cannot handle functions with (ndim of output) > 1 , only vectors are allowed')
    M = v_0.size
    r = []
    
    for i in range(len(Vars)):
        if varForDifferentiation is not None and i != varForDifferentiation: continue
        if not isscalar(Args[i]):
            Args[i] = asfarray(Args[i])
            S = Args[i]
        else:
            S = asfarray([Args[i]])
        S = atleast_1d(S)
        agregate_counter = 0
        assert asarray(Args[i]).ndim <= 1, 'derivatives for more than single dimension variables are not implemented yet'
        
        if diffInt.size == 1: diff_int = asarray([diffInt[0]]*S.size)# i.e. python list of length inp.size
        else: diff_int = diffInt
   
        cmp = atleast_1d(1e-10 * abs(S))
        ind = diff_int<cmp
        diff_int[ind] = cmp[ind]
        
        d1 = empty((M, S.size))

        for j in range(S.size):
            di = float(asscalar(diff_int[j]))
            tmp = S[j] #if S.ndim > 0 else asscalar(S)
            di = diff_int[j]
            di2 = di / 2.0
            S[j] += di
            TMP = fun(*Args)
            #if not isscalar(TMP): TMP = hstack(TMP)
            v_right = atleast_1d(TMP)# TODO: fix it for matrices with ndims>1
            S[j] = tmp 
            # not Args[i][j] -= di, because it can change primeval Args[i][j] value 
            # and check for key == same value will be failed
            
            has_nonfinite_right = not all(isfinite(v_right))
            if stencil >= 2 or has_nonfinite_right:
                S[j] -= di
                v_left = atleast_1d(fun(*Args))
                S[j] = tmp
                has_nonfinite_left = not all(isfinite(v_left))
                
                if has_nonfinite_right:
                    if stencil == 1:
                        d1[:, agregate_counter] = (v_0-v_left) / di
                    else:
                        S[j] -= di2
                        v_subleft = atleast_1d(fun(*Args))
                        S[j] = tmp
                        d1[:, agregate_counter] = (3*v_0+v_left-4*v_subleft) / di
                elif has_nonfinite_left:
                    if stencil == 1:
                        d1[:, agregate_counter] = (v_right - v_0) / di
                    else:
                        S[j] += di2
                        v_subright = atleast_1d(fun(*Args))
                        S[j] = tmp
                        d1[:, agregate_counter] = (4*v_subright-3*v_0-v_right) / di
                    
                elif stencil == 2:
                    d1[:, agregate_counter] = (v_right-v_left) / (2.0 * di)
                else:
                    assert stencil == 3
                    S[j] -= di2
                    v_subleft = atleast_1d(fun(*Args))
                    S[j] = tmp
                    
                    S[j] += di2
                    v_subright = atleast_1d(fun(*Args))
                    S[j] = tmp
                    
                    d1[:, agregate_counter] = (v_left - v_right + 8.0 * (v_subright-v_subleft)) / (6.0 * di)
            else:
                d1[:, agregate_counter] = (v_right-v_0) / di
                
            agregate_counter += 1 # TODO: probably other values for n-dim arrays
            
        # TODO: fix it for arrays with ndim > 2
        if not exactShape and min(d1.shape)==1: d1 = d1.flatten()
        
        r.append(asfarray(d1))

    if varForDifferentiation is not None or isscalar(vars) or isinstance(vars, ndarray) or isinstance(vars, list): r = d1
    else: r = tuple(r)
    return r

def check_d1(fun, fun_d, vars, func_name='func', diffInt=1.5e-8, pointVal = None, args=(), stencil = 3, maxViolation=0.01, varForCheck = None):
    """
    Usage: check_d1(fun, fun_d, x, func_name='func', diffInt=1.5e-8, pointVal = None, args=(), stencil = 3, maxViolation=0.01, varForCheck = None)
    fun: R^n -> R^m, x0 from R^n: function and point where derivatives should be obtained 
    fun_d - user-provided routine for derivatives evaluation to be checked 
    diffInt - step for stencil
    pointVal - fun(x) if known (it is used from OpenOpt and FuncDesigner)
    args - additional args for fun, if not equalk to () then fun(x, *args) will be involved 
    stencil = 1: (f(x+diffInt) - f(x)) / diffInt
    stencil = 2: (f(x+diffInt) - f(x-diffInt)) / (2*diffInt)
    stencil = 3: (-f(x+2*diffInt) + 8*f(x+diffInt) - 8*f(x-diffInt) + f(x-2*diffInt)) / (12*diffInt)
    maxViolation - threshold for reporting of incorrect derivatives
    varForCheck - the parameter is used from FuncDesigner
    
    Note that one of output values RD (relative difference) is defined as
    int(ceil(log10(abs(Diff) / maxViolation + 1e-150)))
    where
    Diff = 1 - (info_user+1e-8)/(info_numerical + 1e-8) 
    """
    
    from numpy import ceil, log10, argmax
    
    info_numerical = get_d1(fun, vars, diffInt=diffInt, pointVal = pointVal, args=args, stencil = stencil, varForDifferentiation = varForCheck)
    
    if type(vars) not in [list, tuple]:
        Vars = [vars, ]
    else: Vars = list(vars)
    
    if type(args) != tuple:
        args = (args, )
    Args = list(tuple(Vars) + args)
    
    if isinstance(fun_d, ndarray):
        info_user = fun_d
    elif hasattr(fun_d, 'scalarMultiplier'):# is FD "diagonal" matrix type
        info_user = fun_d.resolve(False)
    else:
        info_user = asfarray(fun_d(*Args))
    
    if min(info_numerical.shape) == 1: info_numerical = info_numerical.flatten()
    if min(info_user.shape) == 1: info_user = info_user.flatten()
    
    if atleast_2d(info_numerical).shape != atleast_2d(info_user).shape:
        raise DerApproximatorException('user-supplied gradient for ' + func_name + ' has other size than the one, obtained numerically: '+ \
        str(info_numerical.shape) + ' expected, ' + str(info_user.shape) + ' obtained')
    
    Diff = 1 - (info_user+1e-8)/(info_numerical + 1e-8) # 1e-8 to suppress zeros
    log10_RD = log10(abs(Diff)/maxViolation+1e-150)

    #TODO: omit flattering
    d = hstack((info_user.reshape(-1,1), info_numerical.reshape(-1,1), Diff.reshape(-1,1)))
    
    if info_numerical.ndim > 1: useDoubleColumn = True
    else: useDoubleColumn = False

    cond_same = all(abs(Diff) <= maxViolation)
    if not cond_same:
        ss = '    '
            
        if useDoubleColumn:
            ss = ' i,j: d' + func_name + '[i]/dx[j]'

        s = func_name + ' num  ' + ss + '   user-supplied     numerical               RD'
        print(s)

    #ns = ceil(log10(d.shape[0]))
    counter = 0
    fl_info_user = info_user.flatten()
    fl_info_numerical = info_numerical.flatten()
    if len(Diff.shape) == 1:
        Diff = Diff.reshape(-1,1)
        log10_RD = log10_RD.reshape(-1,1)
    for i in range(Diff.shape[0]):
        for j in range(Diff.shape[1]):
            if abs(Diff[i,j]) < maxViolation: continue
            counter += 1
            k = Diff.shape[1]*i+j
            if useDoubleColumn:  ss = str(i) + ' / ' + str(j)
            else: ss = ''

            if len(Diff.shape) == 1 or Diff.shape[1] == 1: n2 = 0
            else: n2 = 15
            RDnumOrNan = 'NaN' if isnan(log10_RD[i,j]) else ('%d' % int(ceil(log10_RD[i,j])))
            s = '    ' + ('%d' % k).ljust(5) + ss.rjust(n2) + ('%+0.3e' % fl_info_user[k]).rjust(19) + ('%+0.3e' % fl_info_numerical[k]).rjust(15) + RDnumOrNan.rjust(15)
            print(s)

    diff_d = abs(d[:,0]-d[:,1])
    ind_max = argmax(diff_d)
    val_max = diff_d[ind_max]
    if not cond_same:
        print('max(abs(d_user - d_numerical)) = ' + str(val_max))
        print('(is registered in func number ' + str(ind_max) + ')')
    else:
        print('derivatives are equal')
    print(75 * '*')
    
    
def get_d2(fun, vars, fun_d = None, diffInt = 1.5e-4, pointVal = None, args=(), stencil = 3, varForDifferentiation = None, exactShape = True, pointD1 = None):
    """
    Usage: get_d2(fun, x, fun_d = None, diffInt = 1.5e-4, pointVal = None, args=(), stencil = 3, varForDifferentiation = None, exactShape = True)
    
    fun: R^n -> R^m, x0 from R^n: function and point where derivatives should be obtained 
    currently implemented for m=1 only!
    
    diffInt - step for stencil
    pointVal - fun(x) if known (it is used from OpenOpt and FuncDesigner)
    args - additional args for fun, if not equalk to () then fun(x, *args) will be involved 
    
    stencil - parameter for lower-level routine get_d1 used in get_d2, default 3
    stencil = 1: (f(x+diffInt) - f(x)) / diffInt
    stencil = 2: (f(x+diffInt) - f(x-diffInt)) / (2*diffInt)
    stencil = 3: (-f(x+2*diffInt) + 8*f(x+diffInt) - 8*f(x-diffInt) + f(x-2*diffInt)) / (12*diffInt)
    
    varForDifferentiation - the parameter is used from FuncDesigner
    exactShape - set True to forbid possible flattering for 1D arrays
    """
    
    # TODO: reduce number of func evals via (j,i) -> (i,j)
    
    if fun_d is None: 
        fun_d = lambda x: get_d1(fun, x, diffInt=diffInt, pointVal = pointVal, args=args, stencil = stencil, \
                                 varForDifferentiation = varForDifferentiation, exactShape = exactShape)
                                 
    # TODO: get rid of it when m could be greater than 1
#    if pointVal is None:
#        pointVal = fun(vars)

    # TODO: involve start value of 1st derivative,  if known
    point_D1_Val = (fun_d(vars) if pointD1 is None else array(pointD1, float)).flatten()
    

    return get_d1(fun_d, vars, diffInt=diffInt, pointVal = point_D1_Val, args=args, stencil = stencil, \
                  varForDifferentiation = varForDifferentiation, exactShape = exactShape)
    

