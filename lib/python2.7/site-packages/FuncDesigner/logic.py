PythonSum = sum
from numpy import array, inf, logical_and, all, isnan, ndarray, where, atleast_1d, isfinite, log2, logical_not
#from ooFun import oofun, BooleanOOFun
from FDmisc import FuncDesignerException, raise_except
from baseClasses import OOFun

#def discreteNLH(_input_bool_oofun, Lx, Ux, p, dataType):
#    
#    T0, res, DefiniteRange = _input_bool_oofun.nlh(Lx, Ux, p, dataType)
#    #T = 1.0 - T0
#    #R = dict([(v, 1.0-val) for v, val in res.items()])
#    return T.flatten(), R, DefiniteRange

def nlh_and(_input, dep, Lx, Ux, p, dataType):
    nlh_0 = array(0.0)
    R = {}
    DefiniteRange = True
    
    elems_nlh = [(elem.nlh(Lx, Ux, p, dataType) if isinstance(elem, OOFun) \
                  else (0, {}, None) if elem is True 
                  else (inf, {}, None) if elem is False 
                  else raise_except()) for elem in _input]
                  
    for T0, res, DefiniteRange2 in elems_nlh:
        DefiniteRange = logical_and(DefiniteRange, DefiniteRange2)
        
    for T0, res, DefiniteRange2 in elems_nlh:
        if T0 is None or T0 is True: continue
        if T0 is False or all(T0 == inf):
            return inf, {}, DefiniteRange
        if all(isnan(T0)):
            raise FuncDesignerException('unimplemented for non-oofun or fixed oofun input yet')
        
        if type(T0) == ndarray:
            if nlh_0.shape == T0.shape:
                nlh_0 += T0
            elif nlh_0.size == T0.size:
                nlh_0 += T0.reshape(nlh_0.shape)
            else:
                nlh_0 = nlh_0 + T0
        else:
            nlh_0 += T0
        
        # debug 
#    if not any(isfinite(nlh_0)):
#        return inf, {}, DefiniteRange
#    for T0, res, DefiniteRange2 in elems_nlh:
        #debug end
        
        T_0_vect = T0.reshape(-1, 1) if type(T0) == ndarray else T0
        
        for v, val in res.items():
            r = R.get(v, None)
            if r is None:
                R[v] = val - T_0_vect
            else:
                r += (val if r.shape == val.shape else val.reshape(r.shape)) - T_0_vect
        
    nlh_0_shape = nlh_0.shape
    nlh_0 = nlh_0.reshape(-1, 1)
    for v, val in R.items():
        # TODO: check it
        #assert all(isfinite(val))
        tmp =  val + nlh_0
        tmp[isnan(tmp)] = inf # when val = -inf summation with nlh_0 == inf
        R[v] = tmp

    return nlh_0.reshape(nlh_0_shape), R, DefiniteRange


def nlh_xor(_input, dep, Lx, Ux, p, dataType):
    nlh_0 = array(0.0)
    nlh_list = []
    nlh_list_m = {}
    num_inf_m = {}
    S_finite = array(0.0)
    num_inf_0 = atleast_1d(0)
    num_inf_elems = []
    R_diff = {}
    R_inf = {}
    #S_finite_diff = {}
    
    DefiniteRange = True

    elems_lh = [(elem.lh(Lx, Ux, p, dataType) if isinstance(elem, OOFun) \
                  else (inf, {}, None) if elem is True 
                  else (0, {}, None) if elem is False 
                  else raise_except()) for elem in _input]


    for T0, res, DefiniteRange2 in elems_lh:
        DefiniteRange = logical_and(DefiniteRange, DefiniteRange2)

    for j, (T0, res, DefiniteRange2) in enumerate(elems_lh):
        if T0 is None: 
            raise FuncDesignerException('probably bug in FD kernel')
            # !!!!!!!!!!!!!!!!! check "len(elems_lh)" below while calculating P_t
            #continue
        if all(isnan(T0)):
            raise FuncDesignerException('unimplemented for non-oofun or fixed oofun input yet')

        #T_0_vect = T0.reshape(-1, 1) if type(T0) == ndarray else T0
        
        T_inf = where(isfinite(T0), 0, 1)
        num_inf_elems.append(T_inf)
        T0 = where(isfinite(T0), T0, 0.0)
        two_pow_t0 = 2.0 ** T0
        if type(T0) == ndarray:
            if nlh_0.shape == T0.shape:
                nlh_0 += T0
                num_inf_0 += T_inf
                S_finite += two_pow_t0
            elif nlh_0.size == T0.size:
                nlh_0 += T0.reshape(nlh_0.shape)
                num_inf_0 += T_inf.reshape(nlh_0.shape)
                S_finite += two_pow_t0.reshape(nlh_0.shape)
            else:
                nlh_0 = nlh_0 + T0
                num_inf_0 = num_inf_0 + T_inf
                S_finite = S_finite + two_pow_t0.reshape(nlh_0.shape)
        else:
            nlh_0 += T0
            num_inf_0 += T_inf
            S_finite += two_pow_t0
            
        nlh_list.append(T0)
        
        for v, val in res.items():
            T_inf_v = where(isfinite(val), 0, 1)
            val_noninf = where(isfinite(val), val, 0)
            T0v = val_noninf - T0.reshape(-1, 1)
            
            r = nlh_list_m.get(v, None)
            if r is None:
                nlh_list_m[v] = [(j, T0v)]
                num_inf_m[v] = [(j, T_inf_v.copy())]
                #num_inf_m[v] = T_inf_v.copy()
            else:
                r.append((j, T0v))
                num_inf_m[v].append((j, T_inf_v.copy()))
                #num_inf_m[v] +=T_inf_v
                
            r = R_inf.get(v, None)
            T_inf = T_inf.reshape(-1, 1)
            if r is None:
                R_inf[v] = T_inf_v - T_inf#.reshape(-1, 1)
                R_diff[v] = T0v.copy()
            else:
                # TODO: check for 1st elem of size 1
                r += (T_inf_v if r.shape == T_inf_v.shape else T_inf_v.reshape(r.shape))  - T_inf#.reshape(-1, 1)
                R_diff[v] += T0v
                
        
    nlh_1 = [nlh_0 - elem for elem in nlh_list]
    # !!! TODO: speedup it via matrix insted of sequence of vectors
    num_infs = [num_inf_0 - t for t in num_inf_elems]

    S1 = PythonSum([2.0 ** where(num_infs[j] == 0, -t, -inf) for j, t in enumerate(nlh_1)])
    S2 = atleast_1d(len(elems_lh)  * 2.0 ** (-nlh_0))
    S2[num_inf_0 != 0] = 0
    #nlh_t = -log(S2 - S1 + 1.0)
    #nlh_t = -log1p(S2 - S1) * 1.4426950408889634
    nlh_t = -log2(S1-S2)
#    assert not any(isnan(nlh_t))
#    if not all(isfinite(nlh_t)):
#        print('='*10)
#        print(nlh_t)
#        print(elems_lh)
#        raise 0
    #print(elems_lh)
#    print(R_inf)
    #raise 0
    R = {}
    nlh_0 = nlh_0.reshape(-1, 1)
    num_inf_0 = num_inf_0.reshape(-1, 1)

    for v, nlh_diff in R_diff.items():
        nlh = nlh_0 + nlh_diff
        nlh_1 = [nlh - elem.reshape(-1, 1) for elem in nlh_list]
        
        for j, val in nlh_list_m[v]:
            nlh_1[j] -= val
        Tmp = R_inf[v] + num_inf_0
        num_infs = [Tmp] * len(nlh_1)
        for j, num_inf in num_inf_m[v]:
            num_infs[j] = num_inf
        
        num_infs2 = [Tmp - elem for elem in num_infs]
        #num_infs = num_inf - num_inf_m[v]
        S1 = PythonSum([2.0 ** where(num_infs2[j] == 0, -elem, -inf) for j, elem in enumerate(nlh_1)])
        S2 = atleast_1d(len(elems_lh)  * 2.0 ** (-nlh))
        S2[Tmp.reshape(S2.shape) != 0] = 0
        R[v] = -log2(S1 - S2)
        #R[v] = -log1p(S2 - S1) * 1.4426950408889634
        
    for v, val in R.items():
        val[isnan(val)] = inf
        val[val < 0.0] = 0.0
#    print('-'*10)
#    #print(Lx, Ux)
#    print('elems_lh:', elems_lh)
#    print(nlh_t, R, DefiniteRange)
    #raw_input()
#    if nlh_t.size > 2:
#        raise 0
    return nlh_t, R, DefiniteRange


def nlh_not(_input_bool_oofun, dep, Lx, Ux, p, dataType):
    if _input_bool_oofun is True or _input_bool_oofun is False:
        raise 'unimplemented for non-oofun input yet'
       
    T0, res, DefiniteRange = _input_bool_oofun.nlh(Lx, Ux, p, dataType)
    T = reverse_l2P(T0)
    R = dict([(v, reverse_l2P(val)) for v, val in res.items()])
    return T, R, DefiniteRange


def reverse_l2P(l2P):
    l2P = atleast_1d(l2P)# elseware bug "0-d arrays cannot be indexed"
    #l2P[l2P<0]=0
    r = 1.0 / l2P
    ind = l2P < 15
    r[ind] = -log2(1-2**(-l2P[ind]))
    #r[r<0] = 0
    return r
    

def AND(*args):
    from BooleanOOFun import BooleanOOFun
    Args = args[0] if len(args) == 1 and isinstance(args[0], (ndarray, tuple, list, set)) else args
    assert not isinstance(args[0], ndarray), 'unimplemented yet' 
    Args2 = []
    for arg in Args:
        if not isinstance(arg, OOFun):
            if arg is False:
                return False
            elif arg is True:
                continue
            raise FuncDesignerException('FuncDesigner logical AND currently is implemented for oofun instances only')
        Args2.append(arg)
    if len(Args2) == 0:
        return True
    elif len(Args2) == 1:
        return Args2[0]
        
    f  = logical_and if len(Args2) == 2 else alt_AND_engine
    r = BooleanOOFun(f, Args2, vectorized = True)
    r.nlh = lambda *arguments: nlh_and(Args2, r._getDep(), *arguments)
    r.oofun = r
    return r
    
def alt_AND_engine(*input):
    tmp = input[0]
    for i in range(1, len(input)):
        tmp = logical_and(tmp, input[i])
    return tmp

# TODO: multiple args
XOR_prev = lambda arg1, arg2: (arg1 & ~arg2) | (~arg1 & arg2)

def XOR(*args):
    from BooleanOOFun import BooleanOOFun
    Args = args[0] if len(args) == 1 and isinstance(args[0], (ndarray, tuple, list, set)) else args
    assert not isinstance(args[0], ndarray), 'unimplemented yet' 
    for arg in Args:
        if not isinstance(arg, OOFun):
            raise FuncDesignerException('FuncDesigner logical XOR currently is implemented for oofun instances only')    
    #f = lambda *args: logical_xor(hstack([asarray(elem).reshape(-1, 1) for elem in args]))
    r = BooleanOOFun(f_xor, Args, vectorized = True)
    r.nlh = lambda *arguments: nlh_xor(Args, r._getDep(), *arguments)
    r.oofun = r # is it required?
    return r
def f_xor(*args):
    r = sum(array(args), 0)
    return r == 1


EQUIVALENT = lambda arg1, arg2: ((arg1 & arg2) | (~arg1 & ~arg2))
    
def NOT(_bool_oofun):
    if _bool_oofun is False:
        return True
    elif _bool_oofun is True:
        return False
    from BooleanOOFun import BooleanOOFun
    assert not isinstance(_bool_oofun, (ndarray, list, tuple, set)), 'disjunctive and other logical constraint are not implemented for ooarrays/ndarrays/lists/tuples yet' 
    if not isinstance(_bool_oofun, OOFun):
        raise FuncDesignerException('FuncDesigner logical NOT currently is implemented for oofun instances only')
    r = BooleanOOFun(logical_not, [_bool_oofun], vectorized = True)
    r.oofun = r

    if _bool_oofun.is_oovar:
        r.lh = lambda *arguments: nlh_not(_bool_oofun, r._getDep(), *arguments)
        r.nlh = _bool_oofun.lh
    else:
        r.nlh = lambda *arguments: nlh_not(_bool_oofun, r._getDep(), *arguments)
    return r

NAND = lambda *args, **kw: NOT(AND(*args, **kw))
NOR = lambda *args, **kw: NOT(OR(*args, **kw))


def OR(*args):
    Args = args[0] if len(args) == 1 and isinstance(args[0], (ndarray, list, tuple, set)) else args
    assert not isinstance(args[0], ndarray), 'unimplemented yet' 
    Args2 = []
    for arg in Args:
        if not isinstance(arg, OOFun):
            if arg is True:
                return True
            elif arg is False:
                continue
            raise FuncDesignerException('''
            FuncDesigner logical OR currently is implemented 
            for oofun instances or list/tuple/set on them only''')
        Args2.append(arg)
        
    if len(Args2) == 0:
        return False
    elif len(Args2) == 1:
        return Args2[0]
        
    r = ~ AND([~elem for elem in Args2])
    #r.fun = np.logical_or
    r.oofun = r
    return r
