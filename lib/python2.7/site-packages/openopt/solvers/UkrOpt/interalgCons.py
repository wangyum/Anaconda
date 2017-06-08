from numpy import empty, logical_and, logical_not, take, zeros, isfinite, any, \
asarray, ndarray, bool_#where
from interalgT import truncateByPlane, getTruncatedArrays, splitDomainForDiscreteVariable#adjustDiscreteVarBounds
import numpy as np

# for PyPy
from openopt.kernel.nonOptMisc import where

hasPoint = lambda y, e, point:\
    True if y.size != 0 and any([(np.all(y[i]<=point) and np.all(e[i]>=point)) for i in range(y.shape[0])]) else False
pointInd = lambda y, e, point:\
    where([(np.all(y[i]<=point) and np.all(e[i]>=point)) for i in range(y.shape[0])])[0].tolist()
    
def processConstraints(C0, y, e, _s, p, dataType):
    #P = np.array([  7.64673334e-01,    4.35551807e-01,    5.93869991e+02,   5.00000000e+00])
#    P = np.array([-0.63521194458007812, -0.3106536865234375, 0.0905609130859375, 0.001522064208984375, -0.69999999999999996, -0.99993896484375, 0.90000152587890625, 1.0, 4.0])

#    print('c-1', p.iter, hasPoint(y, e, P), pointInd(y, e, P))
    n = p.n
    m = y.shape[0]
    indT = empty(m, bool)
    indT.fill(False)
#    isSNLE = p.probType in ('NLSP', 'SNLE')
    
    for i in range(p.nb):
        y, e, indT, ind_trunc = truncateByPlane(y, e, indT, p.A[i], p.b[i]+p.contol)
        if ind_trunc is not True:
            _s = _s[ind_trunc]
    for i in range(p.nbeq):
        # TODO: handle it via one func
        y, e, indT, ind_trunc = truncateByPlane(y, e, indT, p.Aeq[i], p.beq[i]+p.contol)
        if ind_trunc is not True:
            _s = _s[ind_trunc]
        y, e, indT, ind_trunc = truncateByPlane(y, e, indT, -p.Aeq[i], -p.beq[i]+p.contol)
        if ind_trunc is not True:
            _s = _s[ind_trunc]
   
    DefiniteRange = True
    m = y.shape[0]
    nlh = zeros((m, 2*n))
    nlh_0 = zeros(m)
#    if len(p._discreteVarsNumList):
#        y, e, _s, indT = adjustDiscreteVarBounds(y, e, _s, indT, p)
#        y, e = adjustDiscreteVarBounds(y, e, p)
        #y, e, trunc_ind = adjustDiscreteVarBounds(y, e, p)
#        y, e, indT, _s, nlh, nlh_0 = \
#        getTruncatedArrays2(trunc_ind, y, e, indT, _s, nlh, nlh_0)

    m = y.shape[0]
    
    # TODO: probably remove it
    fullOutput = False#isSNLE and not p.hasLogicalConstraints
    
    residual = zeros((m, 2*n)) if fullOutput else None
    residual_0 = zeros(m) if fullOutput else None
    
    for itn, (c, f, lb, ub, tol) in enumerate(C0):
#        assert np.all(y == np.floor(y))
#        assert np.all(e == np.floor(e))
#        print ('c_1', itn, c.dep, hasPoint(y, e, P))
        m = y.shape[0] # is changed in the cycle
        if m == 0: 
            return y.reshape(0, n), e.reshape(0, n), nlh.reshape(0, 2*n), residual, True, False, _s
            #return y.reshape(0, n), e.reshape(0, n), nlh.reshape(0, 2*n), residual.reshape(0, 2*n), True, False, _s
        assert nlh.shape[0] == y.shape[0]
        
        if fullOutput:
            (T0, Res0), (res, R_res), DefiniteRange2 = c.nlh(y, e, p, dataType, fullOutput = True)
            residual_0 += Res0
        else:
            # may be logical constraint and doesn't have kw fullOutput at all
            T0, res, DefiniteRange2 = c.nlh(y, e, p, dataType)
        DefiniteRange = logical_and(DefiniteRange, DefiniteRange2)
        
        assert T0.ndim <= 1, 'unimplemented yet'

        nlh_0 += T0
        assert nlh.shape[0] == m
        # TODO: rework it for case len(p._freeVarsList) >> 1

        for v, tmp in res.items():
            j = p._freeVarsDict.get(v)
            nlh[:, n+j] += tmp[:, tmp.shape[1]/2:].flatten() - T0
            nlh[:, j] += tmp[:, :tmp.shape[1]/2].flatten() - T0
            if fullOutput:
                Tmp = R_res[v]
                residual[:, n+j] += Tmp[:, Tmp.shape[1]/2:].flatten() - Res0
                residual[:, j] += Tmp[:, :Tmp.shape[1]/2].flatten() - Res0
                    
        assert nlh.shape[0] == m
        ind = where(logical_and(any(isfinite(nlh), 1), isfinite(nlh_0)))[0]
        lj = ind.size
        if lj != m:
            assert nlh.shape[0] == y.shape[0]
            y = take(y, ind, axis=0, out=y[:lj])
            e = take(e, ind, axis=0, out=e[:lj])
            nlh = take(nlh, ind, axis=0, out=nlh[:lj])
            nlh_0 = nlh_0[ind]
            assert nlh.shape[0] == y.shape[0]
#            residual = take(residual, ind, axis=0, out=residual[:lj])
            indT = indT[ind]
            _s = _s[ind]
            if fullOutput:
                residual_0 = residual_0[ind]
                residual = take(residual, ind, axis=0, out=residual[:lj])
            if asarray(DefiniteRange).size != 1: 
                DefiniteRange = take(DefiniteRange, ind, axis=0, out=DefiniteRange[:lj])
#            print ('c_2', itn, c.dep, hasPoint(y, e, P))
        assert nlh.shape[0] == y.shape[0]


        ind = logical_not(isfinite(nlh)) #& False
        if any(ind):
            indT[any(ind, 1)] = True
            
            ind_l,  ind_u = ind[:, :ind.shape[1]/2], ind[:, ind.shape[1]/2:]
#            ind_ = logical_or(logical_not(ind_l), logical_not(ind_u))
            tmp_l, tmp_u = 0.5 * (y[ind_l] + e[ind_l]), 0.5 * (y[ind_u] + e[ind_u])
            
            # TODO: improve it, don't copy for continuous variables
            if len(p._discreteVarsNumList):
                r10 = np.array(p._discreteVarsNumList, int)
                L, U = y[:, r10].copy(), e[:, r10].copy()
                
            y[ind_l], e[ind_u] = tmp_l, tmp_u
            
            if len(p._discreteVarsNumList):
                y[:, r10], e[:, r10] = L, U
            
            for i in p._discreteVarsNumList:
                v = p._freeVarsList[i]
                
                ind_l1 = where(ind_l[:, i])[0]
                if ind_l1.size:
                    mid1, mid2 = splitDomainForDiscreteVariable(y[ind_l1, i], e[ind_l1, i], v)
#                    y[ind_l1, i] = L[ind_l1, n+i]
                    y[ind_l1, i] = mid2
#                    y[ind_l1, n+i] = mid2
                    
                ind_u1 = where(ind_u[:, i])[0]
                if ind_u1.size:
                    mid1, mid2 = splitDomainForDiscreteVariable(y[ind_u1, i], e[ind_u1, i], v)
                    e[ind_u1, i] = mid1
#                    e[ind_u1, n+i] = U[ind_u1, i]
#                    e[ind_u1, i] = mid1

            # TODO: mb lock is required for parallel computations
            
            nlh_l, nlh_u = nlh[:, nlh.shape[1]/2:], nlh[:, :nlh.shape[1]/2]
            
            # inplace operations are performed in the cycle
            if 1:
                nlh_l[ind_u], nlh_u[ind_l] = nlh_u[ind_u].copy(), nlh_l[ind_l].copy()   
            else:
                ind_Tmp = logical_and(ind_u, logical_not(ind_l))
                nlh_l[ind_Tmp] = nlh_u[ind_Tmp].copy()
                ind_Tmp = logical_and(ind_l, logical_not(ind_u))
                nlh_u[ind_Tmp] = nlh_l[ind_Tmp].copy()
            
            
            if fullOutput:
                residual_l, residual_u = residual[:, residual.shape[1]/2:], residual[:, :residual.shape[1]/2]
                residual_l[ind_u], residual_u[ind_l] = residual_u[ind_u].copy(), residual_l[ind_l].copy()   
#            print ('c_3', itn, c.dep, hasPoint(y, e, P))

    if nlh.size != 0:
        if DefiniteRange is False:
            nlh_0 += 1e-300
        elif type(DefiniteRange) == ndarray and not all(DefiniteRange):
            nlh_0[logical_not(DefiniteRange)] += 1e-300
        else:
            assert type(DefiniteRange) in (bool, bool_, ndarray)
    # !! matrix - vector
    nlh += nlh_0.reshape(-1, 1)
    
    if fullOutput:
        # !! matrix - vector
        residual += residual_0.reshape(-1, 1)
        residual[residual_0>=1e300] = 1e300
    
    #print('c2', p.iter, hasPoint(y, e, P), pointInd(y, e, P))
    return y, e, nlh, residual, DefiniteRange, indT, _s

hasPoint = lambda y, e, point:\
    True if y.size != 0 and any([(all(y[i]<=point) and all(e[i]>=point)) for i in range(y.shape[0])]) else False
pointInd = lambda y, e, point:\
    where([(all(y[i]<=point) and all(e[i]>=point)) for i in range(y.shape[0])])[0].tolist()
    

def getTruncatedArrays2(ind, y, e, indT, _s, nlh, nlh_0, ind_l = None, ind_u = None):
    # TODO: rework it when numpy will have appropriate inplace function
    y, e, indT, _s = getTruncatedArrays(ind, y, e, indT, _s)
    s = ind.size
    nlh_0 = nlh_0[ind]
    nlh = take(nlh, ind, axis=0, out=nlh[:s])
    
    if ind_l is None:
        return y, e, indT, _s, nlh, nlh_0

    ind_l = take(ind_l, ind, axis=0, out=ind_l[:s])
    ind_u = take(ind_u, ind, axis=0, out=ind_u[:s])
    return y, e, indT, _s, nlh, nlh_0, ind_l, ind_u
    

'''
            if len(p._discreteVarsNumList):
                tmp_l, tmp_u = adjustDiscreteVarBounds(tmp_l, tmp_u, p)
                if tmp_l.ndim > 1:
                    # shouldn't reduce y,e shape here, so output values doesn't matter
#                    l1 = len(_s)
                    assert nlh.shape[0] == y.shape[0]
#                    tmp_l, tmp_u, _s2, indT2 = \
#                    adjustDiscreteVarBounds(tmp_l, tmp_u, _s, indT, p)
                    #adjustDiscreteVarBounds(tmp_l, tmp_u, p, (indT, _s, nlh, nlh_0))
                    
                    
#                    tmp_l, tmp_u = adjustDiscreteVarBounds(tmp_l, tmp_u, p)
                    
                    
                    #tmp_l, tmp_u, trunc_ind = adjustDiscreteVarBounds(tmp_l, tmp_u, p)
#                    tmp_l, tmp_u, indT, _s, nlh, nlh_0, ind_l, ind_u  = \
#                    getTruncatedArrays2(trunc_ind, tmp_l, tmp_u, indT, _s, nlh, nlh_0)
#                    y[ind_l], e[ind_u] = tmp_l, tmp_u
                    
                    assert nlh.shape[0] == y.shape[0]
#                    l2 = len(trunc_ind)
#                    if l2 != 0:
#                        print('Warning: possible bug in interalg constraints processing, inform developers')
                else:
                    pass
#                    y, e = adjustDiscreteVarBounds(y, e, p)
                    #y, e, trunc_ind = adjustDiscreteVarBounds(y, e, p)
#                    y, e, indT, _s, nlh, nlh_0, ind_l, ind_u = \
#                    getTruncatedArrays2(trunc_ind, y, e, indT, _s, nlh, nlh_0, ind_l, ind_u)
                    #y, e, _s, indT = adjustDiscreteVarBounds(y, e, _s, indT, p)
'''
