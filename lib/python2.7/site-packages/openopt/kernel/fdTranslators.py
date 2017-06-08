from numpy import hstack, vstack, atleast_1d, cumsum, asarray, zeros,  ndarray,\
prod, ones, copy, nan, flatnonzero, array_equal, asanyarray#, int64
from nonOptMisc import scipyInstalled, Hstack, Vstack, Find, \
isspmatrix, SparseMatrixConstructor, DenseMatrixConstructor
import numpy as np
#from oologfcn import OpenOptException


try:
    # available since numpy 1.6.x
    from numpy import count_nonzero
except:
    count_nonzero = lambda elem: len(flatnonzero(asarray(elem)))

def setStartVectorAndTranslators(p):
    from FuncDesigner import _Stochastic, ooarray
    startPoint = p.x0
    #assert all(asarray([atleast_1d(val).ndim for val in startPoint.values()]) == 1)
    
    fixedVars, freeVars = None, None
    
    allVarsAreFree = p.freeVars is None
    
    if not allVarsAreFree:
        if not isinstance(p.freeVars,  (list, tuple, ndarray, set)):
            assert hasattr(p.freeVars, 'is_oovar')
            p.freeVars = [p.freeVars]
            freeVars = p.freeVars
        else:
            freeVars = list(p.freeVars)
        freeVars = getVars(freeVars)
        fixedVars = list(set(startPoint.keys()).difference(set(freeVars)))
        p.fixedVars = fixedVars
    elif p.fixedVars is not None:
        p.fixedVars.update(p._aux_fixedVars)
        if not isinstance(p.fixedVars,  (list, tuple, ndarray, set)):
            assert hasattr(p.fixedVars, 'is_oovar')
            p.fixedVars = [p.fixedVars]
            fixedVars = p.fixedVars
        else:
            fixedVars = list(p.fixedVars)
            p.fixedVars = fixedVars
        for elem in fixedVars:
            if type(elem) == ooarray:
                p._init_fixed_ooarrays.add(elem)
        fixedVars = getVars(fixedVars)
        freeVars = list(set(startPoint.keys()).difference(set(fixedVars)))
        p.freeVars = freeVars
    else:
        freeVars = list(startPoint.keys())
    
    if len(p._aux_fixedVars):
        p.freeVars = freeVars = [elem for elem in freeVars if elem not in p._aux_fixedVars]
        if fixedVars is not None:
            fixedVars = list(set(p._aux_fixedVars.keys()) | set(fixedVars))
        else:
            fixedVars = list(p._aux_fixedVars.keys())
        p.fixedVars = fixedVars
    
    nn = len(freeVars)
    for i in range(nn):
        v = freeVars[nn-1-i]
        if isinstance(startPoint[v], _Stochastic):# TODO: is _Stochastic reachable here in freeVars? exclude if not
            if fixedVars is None:
                p.fixedVars = fixedVars = [v]
            else:
                fixedVars.append(v)
            if freeVars is None:
                freeVars = p.freeVars = startPoint.keys()
            del freeVars[nn-1-i]

    # TODO: use ordered set instead
    freeVars.sort(key=lambda elem: elem._id)
#    fixedVars.sort()
    p._freeVarsList = freeVars 
    p._discreteVarsNumList = []
    p._discreteVarsList = []
    for i, v in enumerate(p._freeVarsList):
        if v.domain is not None:
            p._discreteVarsNumList.append(i)
            p._discreteVarsList.append(v)
    
    p._fixedVars = p.fixedVarsSet = set(fixedVars) if fixedVars is not None else set()
    p._freeVars = p.freeVarsSet = set(freeVars) if freeVars is not None else set()
        
    # point should be FuncDesigner point that currently is Python dict        
    # point2vector = lambda point: atleast_1d(hstack([asfarray(point[oov]) for oov in freeVars]))
    
    tmp = {}
    for oov in freeVars:
        val = startPoint[oov]
        # TODO: is _Stochastic reachable here in freeVars? exclude if not
        tmp[oov] = 1 if isinstance(val, _Stochastic) else asanyarray(val).size
    
    p._optVarSizes = tmp#dict([(oov, asarray(startPoint[oov]).size) for oov in freeVars])
    sizes_items = list(p._optVarSizes.items())
    sizes_items.sort(key=lambda elem:elem[0]._id)
    point2vector = lambda point: atleast_1d(hstack([(point[oov] if oov in point else zeros(sz)) for oov, sz in sizes_items]))
    # 2nd case can trigger from objective/constraints defined over some of opt oovars only
        
    vector_x0 = point2vector(startPoint)
    n = vector_x0.size
    p.n = n
    
    #oovar_sizes = [asarray(startPoint[elem]).size for elem in freeVars]
    # temporary walkaround for pypy
    oovar_sizes = [len(atleast_1d(startPoint[elem]).flatten()) for elem in freeVars]

#    for elem in freeVars:
#        print startPoint[elem]
#        if type(startPoint[elem]) == ndarray: 
#            print '----'
#            print type(startPoint[elem])
#            print startPoint[elem].size 
#            print len(startPoint[elem])

    oovar_indexes = cumsum([0] + oovar_sizes)
    
    # TODO: mb use oovarsIndDict here as well (as for derivatives?)
    from FuncDesigner import oopoint
    startDictData = []
    if fixedVars is not None:
        for v in p.probDep & p._fixedVars:
            val = startPoint.get(v, 'absent')
            if type(val) == str and val == 'absent':
                p.err('value for fixed variable %s is absent in start point' % v.name)
            startDictData.append((v, val))

    #vector2point = lambda x: oopoint(startDictData + [(oov, x[oovar_indexes[i]:oovar_indexes[i+1]]) for i, oov in enumerate(freeVars)])
    p._FDtranslator = {'prevX':nan}
    def vector2point(x): 
#        x = asarray(x)
#        if not str(x.dtype).startswith('float'):
#            x = asfarray(x)
        x = atleast_1d(x).copy()
        if array_equal(x, p._FDtranslator['prevX']):
            return p._FDtranslator['prevVal']
            
        # without copy() ipopt and probably others can replace it by noise after closing
#        r = oopoint(startDictData + \
#                    [(oov, x[oovar_indexes[i]:oovar_indexes[i+1]]) for i, oov in enumerate(freeVars)])
        r = startDictData
        tmp = [(oov, x[oovar_indexes[i]:oovar_indexes[i+1]] if oovar_indexes[i+1]-oovar_indexes[i]>1 else x[oovar_indexes[i]]) for i, oov in enumerate(freeVars)]
#        for i, oov in enumerate(freeVars):
#            #I, J = oovar_indexes[i], oovar_indexes[i+1]
#            #r.append((oov, x[I] if J - I == 1 else x[I:J]))
#            r.append((oov, x[oovar_indexes[i]:oovar_indexes[i+1]]))
        r = oopoint(r+tmp, skipArrayCast = True)
        r.maxDistributionSize = p.maxDistributionSize
        p._FDtranslator['prevVal'] = r 
        p._FDtranslator['prevX'] = copy(x)
        return r

    oovarsIndDict = dict([(oov, (oovar_indexes[i], oovar_indexes[i+1])) for i, oov in enumerate(freeVars)])

    def pointDerivative2array(pointDerivative, useSparse = 'auto',  func=None, point=None): 
        
        # useSparse can be True, False, 'auto'
        if not scipyInstalled and useSparse == 'auto':
            useSparse = False
        if useSparse is True and not scipyInstalled:
            p.err('to handle sparse matrices you should have module scipy installed') 

        if len(pointDerivative) == 0: 
            if func is not None:
                funcLen = func(point).size
                if useSparse is not False:
                    return SparseMatrixConstructor((funcLen, n))
                else:
                    return DenseMatrixConstructor((funcLen, n))
            else:
                p.err('unclear error, maybe you have constraint independend on any optimization variables') 

        Items = pointDerivative.items()
        key, val = Items[0] if type(Items) == list else next(iter(Items))
        
        if isinstance(val, float) or (isinstance(val, ndarray) and val.shape == ()):
            val = atleast_1d(val)
        var_inds = oovarsIndDict[key]
        # val.size works in other way (as nnz) for scipy.sparse matrices
        funcLen, _rest = divmod(prod(val.shape), var_inds[1] - var_inds[0])
        assert _rest == 0, 'bug in openopt kernel'
        
        # CHANGES
        
        # 1. Calculate number of zero/nonzero elements
        involveSparse = useSparse
        if useSparse == 'auto':
            nTotal = n * funcLen#sum([prod(elem.shape) for elem in pointDerivative.values()])
            nNonZero = sum((elem.size if isspmatrix(elem) else count_nonzero(elem)) for elem in pointDerivative.values())
            involveSparse = 4*nNonZero < nTotal and nTotal > 1000
        if involveSparse:
            r2 = []
            if funcLen == 1:
                inds = []
                for oov, val in pointDerivative.items():
                    ind_start, ind_end = oovarsIndDict[oov]
                    
                    # works faster than isscalar()
                    if type(val) in (float, np.float64)\
                    or np.isscalar(val):
                        r2.append(val)
                        inds.append(ind_start)
                    elif type(val) in (np.ndarray, np.matrix):
                        Val = (val if type(val) == ndarray else val.A).flatten()
#                        if Val.size == 1:
#                            r2.append(Val.item())
#                            inds.append(ind_start)
#                        else:
                        Ind = np.where(Val)[0]
                        r2 += Val[Ind].tolist()
                        inds += (ind_start+Ind).tolist()
                    elif isspmatrix(val):
                        I, J, vals = Find(val)
#                        if vals.size == 1:
#                            r2.append(vals.item())
#                            inds.append(ind_start+J.item())
#                        else:
                        r2 += vals.tolist()
                        inds += (ind_start+J).tolist()

                from scipy.sparse import coo_matrix
                r3 = coo_matrix((r2, ([0]*len(r2), inds)), shape=(funcLen, n))
            else:
                # USE STACK
                ind_Z = 0
                derivative_items = list(pointDerivative.items())
                derivative_items.sort(key=lambda elem: elem[0]._id)
                for oov, val in derivative_items:#pointDerivative.items():
                    ind_start, ind_end = oovarsIndDict[oov]
                    if ind_start != ind_Z:
                        r2.append(SparseMatrixConstructor((funcLen, ind_start - ind_Z)))
                    if not isspmatrix(val): 
                        val = asarray(val) # else bug with scipy sparse hstack
                    r2.append(val)
                    ind_Z = ind_end
                if ind_Z != n:
                    # assert ind_Z < n
                    r2.append(SparseMatrixConstructor((funcLen, n - ind_Z)))
                r3 = Hstack(r2) 
                #if isspmatrix(r3) and 4 * r3.nnz > asarray(r3.shape, int64).prod(): r3 = r3.A
            return r3
        else:
            # USE INSERT
            if funcLen == 1:
                r = DenseMatrixConstructor(n)
            else:
                r = SparseMatrixConstructor((funcLen, n)) if involveSparse else DenseMatrixConstructor((funcLen, n)) 
            
            for key, val in pointDerivative.items():
                indexes = oovarsIndDict[key]
                if not involveSparse and isspmatrix(val): val = val.A
#                if isscalar(val) or prod(val.shape)==1:
#                    r[indexes[0]] = val.flatten() if type(val) == ndarray else val
#                el
                if r.ndim == 1:
                    r[indexes[0]:indexes[1]] = val.flatten() if type(val) == ndarray else val
                else:
                    r[:, indexes[0]:indexes[1]] = val if val.shape == r.shape else val.reshape((funcLen, prod(val.shape)/funcLen))
            # TODO: mb remove it
            if useSparse is True and funcLen == 1: 
                return SparseMatrixConstructor(r)
            elif r.ndim <= 1:
                r = r.reshape(1, -1)
            if useSparse is False and hasattr(r, 'toarray'):
                r = r.toarray()
            return r
                

    def getPattern(oofuns):
        # oofuns is Python list of oofuns
        assert isinstance(oofuns, list), 'oofuns should be Python list, inform developers of the bug'
        R = []
        for oof in oofuns:
            SIZE = asarray(oof(startPoint)).size
            r = []
            dep = oof._getDep()
            if len(p._fixedVars) != 0:
                dep = dep & p._freeVars if len(p._freeVars) < len(p._fixedVars) else dep.difference(p._fixedVars)
            
            # NEW
            ind_Z = 0
            vars = list(dep)
            vars.sort(key=lambda elem: elem._id)
            for oov in vars:
                ind_start, ind_end = oovarsIndDict[oov]
                if ind_start != ind_Z:
                    r.append(SparseMatrixConstructor((SIZE, ind_start - ind_Z)))
                r.append(ones((SIZE, ind_end - ind_start)))
                ind_Z = ind_end
            if ind_Z != n:
                # assert ind_Z < n
                r.append(SparseMatrixConstructor((SIZE, n - ind_Z)))
            if any([isspmatrix(elem) for elem in r]):
                rr = Hstack(r) if len(r) > 1 else r[0]
            elif len(r)>1:
                rr = hstack(r)
            else:
                rr = r[0]
            R.append(rr)
        result = Vstack(R) if any([isspmatrix(_r) for _r in R]) else vstack(R)
        
        return result
        
    p._getPattern = getPattern
    p.freeVars, p.fixedVars = freeVars, fixedVars
    p._point2vector, p._vector2point = point2vector, vector2point
    p._pointDerivative2array = pointDerivative2array
    p._oovarsIndDict = oovarsIndDict
    
    # TODO: replave p.x0 in RunProbSolver finish  
    p._x0, p.x0 = p.x0, vector_x0 
    
    def linearOOFunsToMatrices(oofuns): #, useSparse = 'auto'
        # oofuns should be linear
        C, d = [], []
        Z = p._vector2point(zeros(p.n))
        for elem in oofuns:
            if elem.isConstraint:
                lin_oofun = elem.oofun
            else:
                lin_oofun = elem
            if lin_oofun.getOrder(p.freeVars, p.fixedVars) > 1:
                from oologfcn import OpenOptException
                raise OpenOptException("this function hasn't been intended to work with nonlinear FuncDesigner oofuns")
            C.append(p._pointDerivative2array(lin_oofun.D(Z, **p._D_kwargs), useSparse = p.useSparse))
            d.append(-lin_oofun(Z))

        C, d = Vstack(C), hstack(d).flatten()

        return C, d    
    p._linearOOFunsToMatrices = linearOOFunsToMatrices





def getVars(t):
    from FuncDesigner import ooarray
    vars1 = [v for v in (t if t is not None else []) if type(v) != ooarray]
    vars2 = [v for v in (t if t is not None else []) if type(v) == ooarray]
    t = vars1 
    for elem in vars2:
        t += elem.tolist()
    return t
