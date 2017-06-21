PythonMin, PythonMax = min, max
from numpy import isnan, array, atleast_1d, all, searchsorted, logical_or, any, nan, \
vstack, inf, where, logical_not, min, abs, insert, logical_xor, argsort, zeros_like

# for PyPy
from openopt.kernel.nonOptMisc import isPyPy

try:
    from numpy import append
except ImportError:
    def append(*args, **kw):
        raise ImportError('function append() is absent in PyPy yet')
        
from interalgLLR import *

try:
    from bottleneck import nanmin, nanmax
except ImportError:
    from numpy import nanmin, nanmax

hasPoint = lambda y, e, point:\
    True if y.size != 0 and any([(all(y[i]<=point) and all(e[i]>=point)) for i in range(y.shape[0])]) else False
pointInd = lambda y, e, point:\
    where([(all(y[i]<=point) and all(e[i]>=point)) for i in range(y.shape[0])])[0].tolist()
    
def r14(p, nlhc, residual, definiteRange, y, e, vv, asdf1, C, 
                 r40, g, nNodes, 
                 r41, fTol, Solutions, varTols, _in, dataType,
                 maxNodes, _s, indTC, xRecord):

    isSNLE = p.probType in ('NLSP', 'SNLE')
    
#    print p.iter, y, e, hasPoint(y, e, [10.,  20.,  10.,  50])

    #maxSolutions, solutions, coords = Solutions.maxNum, Solutions.solutions, Solutions.coords
    maxSolutions, solutions = Solutions.maxNum, Solutions.solutions

    fo_prev = \
    float(0 if isSNLE else PythonMin((r41, r40 - (fTol if maxSolutions == 1 else 0))))
    fo_prev  =  PythonMin(1e300, fo_prev)

    if 0 and isSNLE:
        a = residual
        o = zeros_like(a)
        o2, a2, r41 = r45(y, e, vv, p, asdf1, dataType, r41, nlhc)
#        print p.iter,nanmax(a/a2) / nanmin(a/a2)
#        o, a = o2, a2
        a = a2
        o = zeros_like(a)
    else:
        y, e, o, a, r41, _s, indTC = \
        r45(y, e, vv, p, asdf1, dataType, r41, nlhc, _s, indTC)
        #assert _s.size == y.shape[0]
    
    if o is None:
        return _in, g, fo_prev, _s, Solutions, xRecord, r41, r40
    
#    print(o, a)
#    print 'LF:', o
#    print 'a:', a
#    if p.iter == 13:
#        print y[1]
#        print e[1]
#        print o[1]
#        print a[1]

#    if not isSNLE and isfinite(r40):
#        tmp1 = r40
#        tmp2 = PythonMin(nanmin(o), PythonMin([1e300]+[node.key for node in _in]))
#        rTol = p.rTol * (tmp1 - tmp2) / (1e-300+PythonMin(abs(tmp1), abs(tmp2)))
#        fTol = PythonMax(rTol, fTol)
#        print p.iter, fTol
    
    y, e, o, a, _s, indTC, nlhc, residual = \
    func7(y, e, o, a, _s, indTC, nlhc, residual)    

    if y.size == 0:
        return _in, g, fo_prev, _s, Solutions, xRecord, r41, r40
    
    nodes = func11(y, e, nlhc, indTC, residual, o, a, _s, p)
    #nodes, g = func9(nodes, fo_prev, g, p)
    #y, e = func4(y, e, o, a, fo)
    

    if p.solver.dataHandling == 'raw':
            
        if not isSNLE:
            tmp = o.copy()
            tmp[tmp > fo_prev] = -inf
            M = atleast_1d(nanmax(tmp, 1))
            for i, node in enumerate(nodes):
                node.th_key = M[i]
                node.fo = fo_prev       
                
        if 0 or p.__isNoMoreThanBoxBounded__():#nlhc is not None and not isSNLE:
            for node in nodes: node.tnlhf = node.nlhf 
        else:
            for node in nodes: node.tnlhf = node.nlhc + node.nlhf 
            
        an = nodes + _in#hstack((nodes, _in))
        
        #tnlh_fixed = vstack([node.tnlhf for node in an])
        tnlh_fixed_local = vstack([node.nlhf for node in nodes])#tnlh_fixed[:len(nodes)]
#        if isSNLE:
#            tnlh_curr = tnlh_fixed_local#vstack([node.nlhc for node in nodes])
        if 1:
            tmp_u = where(a>fo_prev, fo_prev, a)#a.copy()
            tmp_l = where(o==-inf, -1e300, o)
#            tmp[tmp>fo_prev] = fo_prev
            tmp2 = tmp_u - tmp_l
#            ind_inf = tmp2==inf
            tmp2[tmp2<1e-300] = 1e-300
            o_exclude_ind = o > fo_prev
            if any(o_exclude_ind):
                tmp2[o_exclude_ind] = nan
                if not isSNLE:
                    g = PythonMin(g, min(o[o_exclude_ind]))
            tnlh_curr = tnlh_fixed_local - log2(tmp2)
#            tnlh_curr[ind_inf] = 1e300
        else:
            if isSNLE:
                tnlh_curr = tnlh_fixed_local
            else:
                tmp = a.copy()
                tmp[tmp>fo_prev] = fo_prev
                tmp2 = tmp - o
                tmp2[tmp2<1e-300] = 1e-300
                tmp2[o > fo_prev] = nan
                tnlh_curr = tnlh_fixed_local - log2(tmp2)
        tnlh_curr_best = nanmin(tnlh_curr, 1)
        for i, node in enumerate(nodes):
            node.tnlh_curr = tnlh_curr[i]
            node.tnlh_curr_best = tnlh_curr_best[i]
        
        # TODO: use it instead of code above
        #tnlh_curr = tnlh_fixed_local - log2(where() - o)
    else:
        tnlh_curr = None
    
    # TODO: don't calculate PointVals for zero-p regions
    PointVals, PointCoords = getr4Values(vv, y, e, tnlh_curr, asdf1, C, p.contol, dataType, p) 
    if PointVals.size != 0:
        xk, Min = r2(PointVals, PointCoords, dataType)
    else: # all points have been removed by func7
        xk = p.xk
        Min = nan

    if r40 > Min:
        r40 = Min
        xRecord = xk.copy()# TODO: is copy required?
    
    r41 = PythonMin(Min, r41)
    
    fo = \
    float(0 if isSNLE else PythonMin(r41, r40 - (fTol if maxSolutions == 1 else 0)))

    tmp = array([node.key for node in (nodes + _in)])
    f_bound_estimation = tmp.min()
    if isfinite(r40):
        p.f_bound_distance = r40 - f_bound_estimation
    if p.goal in ('max', 'maximum'):
        f_bound_estimation = -f_bound_estimation
    p.f_bound_estimation = f_bound_estimation
    
#    print '!', p.iter, y, e, hasPoint(y, e, [10.,  20.,  10.,  50])

    if p.solver.dataHandling == 'raw':
        
        if fo != fo_prev and not  isSNLE:
            fos = array([node.fo for node in an])
            
            #prev
            #ind_update = where(fos > fo + 0.01* fTol)[0]
            
            #new
            th_keys = array([node.th_key for node in an])
            delta_fos = fos - fo
            ind_update = where(10 * delta_fos > fos - th_keys)[0]
            
            update_nlh = True if ind_update.size != 0 else False
#                  print 'o MB:', float(o_tmp.nbytes) / 1e6
#                  print 'percent:', 100*float(ind_update.size) / len(an) 
            if update_nlh:
                #nodesToUpdate = an[ind_update]
                nodesToUpdate = [an[i] for i in ind_update]
#                    from time import time
#                    tt = time()
                updateNodes(nodesToUpdate, fo)
#                    if not hasattr(p, 'Time'):
#                        p.Time = time() - tt
#                    else:
#                        p.Time += time() - tt
                    
            tmp = array([node.key for node in an])
            cond = tmp > fo
            r10 = where(cond)[0]
            g = PythonMin([an[i].key for i in r10]+[g])
            ind_remain = where(logical_not(cond))[0]
            an = [an[i] for i in ind_remain]

        NN = atleast_1d([node.tnlh_curr_best for node in an])
        r10 = logical_or(isnan(NN), NN == inf)

        if any(r10):
            ind = where(logical_not(r10))[0]
            an = [an[i] for i in ind]#an[ind]
            #tnlh = take(tnlh, ind, axis=0, out=tnlh[:ind.size])
            #NN = take(NN, ind, axis=0, out=NN[:ind.size])
            NN = NN[ind]

        if 1 or not isSNLE or p.maxSolutions == 1:
            #pass
            astnlh = argsort(NN)
#            print(astnlh[:10])
            an = [an[i] for i in astnlh]#an[astnlh]
            
#        print(an[0].nlhc, an[0].tnlh_curr_best)
        # Changes
#        if NN.size != 0:
#            ind = searchsorted(NN, an[0].tnlh_curr_best+1)
#            tmp1, tmp2 = an[:ind], an[ind:]
#            arr = [node.key for node in tmp1]
#            Ind = argsort(arr)
#            an = hstack((tmp1[Ind], tmp2))
        #print [node.tnlh_curr_best for node in an[:10]]
    
    else: #if p.solver.dataHandling == 'sorted':
        if isSNLE and p.maxSolutions != 1: 
            an = nodes + _in#hstack((nodes, _in))
        elif isPyPy:
            an = nodes + _in
            an.sort(key = lambda obj: obj.key)
        else:
            nodes.sort(key = lambda obj: obj.key)

            if len(_in) == 0:
                an = nodes
            else:
                arr1 = [node.key for node in _in]
                arr2 = [node.key for node in nodes]
                r10 = searchsorted(arr1, arr2)
                an = insert(_in, r10, nodes).tolist()
#                if p.debug:
#                    arr = array([node.key for node in an])
#                    #print arr[0]
#                    assert all(arr[1:]>= arr[:-1])

    if maxSolutions != 1:
        Solutions = r46(PointCoords, PointVals, fTol, varTols, Solutions)
        
        p._nObtainedSolutions = len(solutions)
        if p._nObtainedSolutions > maxSolutions:
            solutions = solutions[:maxSolutions]
            p.istop = 0
            p.msg = 'user-defined maximal number of solutions (p.maxSolutions = %d) has been exeeded' % p.maxSolutions
            return an, g, fo, None, Solutions, xRecord, r41, r40

    p.iterfcn(xRecord, r40)
    if not isSNLE and isfinite(r41) and len(an):
        tmp = array([node.key for node in an])
        cond_exclude = r40 - tmp <= \
        p.rTol * where(abs(tmp) < abs(r40), abs(tmp), abs(r40))
        g = PythonMin([g] + [an[j].key for j in where(cond_exclude)[0]])
        cond_remain = logical_not(cond_exclude)
        ind = where(cond_remain)[0]
        an = [an[i] for i in ind]
    
    if p.istop != 0: 
        return an, g, fo, None, Solutions, xRecord, r41, r40
    if isSNLE and maxSolutions == 1 and Min <= fTol:
        # TODO: rework it for nonlinear systems with non-bound constraints
        p.istop, p.msg = 1000, 'required solution has been obtained'
        return an, g, fo, None, Solutions, xRecord, r41, r40
    
    an, g = func9(an, fo, g, p)
        
    nn = maxNodes#1 if asdf1.isUncycled and all(isfinite(o)) and p._isOnlyBoxBounded and not p.probType.startswith('MI') else maxNodes

    an, g = func5(an, nn, g, p)
    nNodes.append(len(an))
        
    return an, g, fo, _s, Solutions, xRecord, r41, r40


def r46(PointCoords, PointVals, fTol, varTols, Solutions):
    solutions, coords = Solutions.solutions, Solutions.coords
    
    r5Ind =  where(PointVals < fTol)[0]

    r5 = PointCoords[r5Ind]
    
    for c in r5:
        if len(solutions) == 0 or not any(all(abs(c - coords) < varTols, 1)): 
            solutions.append(c)
            #coords = asarray(solutions)
            Solutions.coords = append(Solutions.coords, c.reshape(1, -1), 0)
            
    return Solutions


def r45(y, e, vv, p, asdf1, dataType, r41, nlhc, _s, indT):
    y, e, o, a, definiteRange, exactRange, _s, indT = func82(y, e, vv, asdf1, dataType, p, 
                                                      r41, _s, indT)
    if o is None:
        return y, e, o, a, r41, _s, indT
    if p.debug and any(a + 1e-15 < o):  
        p.warn('interval lower bound exceeds upper bound, it seems to be FuncDesigner kernel bug')
    if p.debug and any(logical_xor(isnan(o), isnan(a))):
        p.err('bug in FuncDesigner intervals engine')
    
    n = p.n
    m = o.size // (2*n)
    o, a = o.reshape(2*n, m).T, a.reshape(2*n, m).T
    assert len(_s) == m
    
    if p.probType not in ('SNLE', 'NLSP') and asdf1.isUncycled and not p.probType.startswith('MI') \
    and len(p._discreteVarsList)==0 and exactRange:# for SNLE fo = 0
        # TODO: 
        # handle constraints with restricted domain and matrix definiteRange
        ind = where(definiteRange)[0]
        
        if ind.size != 0:
            o2 = o[ind]
            if nlhc is not None:
                nlhc = nlhc[ind]
            # TODO: if o has at least one -inf => prob is unbounded
            tmp1 = o2[nlhc==0] if nlhc is not None else o2
            if tmp1.size != 0:
                tmp1 = nanmin(tmp1)
                
                ## to prevent roundoff issues ##
                tmp1 += 1e-14*abs(tmp1)
                if tmp1 == 0: tmp1 = 1e-300 
                ######################
                
                r41 = nanmin((r41, tmp1)) 
        
    return y, e, o, a, r41, _s, indT

def updateNodes(nodesToUpdate, fo):
    if len(nodesToUpdate) == 0: return
    a_tmp = vstack([node.a for node in nodesToUpdate])
    Tmp = a_tmp
    Tmp[Tmp>fo] = fo                

    o_tmp = vstack([node.o for node in nodesToUpdate])
    Tmp -= o_tmp
    Tmp[Tmp<1e-300] = 1e-300
    Tmp[o_tmp>fo] = nan
    tnlh_all_new =  - log2(Tmp)
    
    del Tmp, a_tmp
    
    tnlh_all_new += vstack([node.tnlhf for node in nodesToUpdate])#tnlh_fixed[ind_update]
    
    tnlh_curr_best = nanmin(tnlh_all_new, 1)

    o_tmp[o_tmp > fo] = -inf
    M = atleast_1d(nanmax(o_tmp, 1))
    for j, node in enumerate(nodesToUpdate): 
        node.fo = fo
        node.tnlh_curr = tnlh_all_new[j]
        node.tnlh_curr_best = tnlh_curr_best[j]
        node.th_key = M[j]

#    return tnlh_all_new, tnlh_curr_best, M


#from multiprocessing import Pool
#from numpy import array_split
#def updateNodes(nodesToUpdate, fo, p):
#    if p.nProc == 1:
#        Chunks = [nodesToUpdate]
#        result = [updateNodesEngine((nodesToUpdate, fo))]
#    else:
#        Chunks = array_split(nodesToUpdate, p.nProc)
#        if not hasattr(p, 'pool'):
#            p.pool = Pool(processes = p.nProc)
#        #result = p.pool.imap(updateNodesEngine, [(c, fo) for c in Chunks])
#        result = p.pool.map(updateNodesEngine, [(c, fo) for c in Chunks])
#    for i, elem in enumerate(result):
#        if elem is None: continue
#        tnlh_all_new, tnlh_curr_best, M = elem
#        for j, node in enumerate(Chunks[i]): 
#            node.fo = fo
#            node.tnlh_curr = tnlh_all_new[j]
#            node.tnlh_curr_best = tnlh_curr_best[j]
#            node.th_key = M[j]
