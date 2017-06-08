PythonMax = max
from numpy import ndarray, atleast_1d, isfinite, all, any, string_, zeros_like, inf, \
ones, array_equal, array, ravel
from fdmisc import formDictOfFixedFuncs, linear_render, formDictOfRedirectedFuncs

from nonOptMisc import EmptyClass, isPyPy, oosolver, Hstack, Vstack
#from oologfcn import OpenOptException
from fdConstraint import fdConstraint

def fdPrepare(p):
    p.isFDmodel = True
    p._FD = EmptyClass()
    p._FD.nonBoxConsWithTolShift = []
    p._FD.nonBoxCons = []
    from FuncDesigner import _getAllAttachedConstraints, _getDiffVarsID, ooarray, oopoint, oofun
    from FuncDesigner.distribution import Stochastic
    
    p._FDVarsID = _getDiffVarsID()
    
    probDep = set()
    

    
    if p.probType in ['SLE', 'NLSP', 'SNLE', 'LLSP']:
        equations = p.C if p.probType in ('SLE', 'LLSP') else p.f
        F = equations
        updateDep(probDep, equations)
        ConstraintTags = [(elem if not isinstance(elem, (set, list, tuple, ndarray)) else elem[0]).isConstraint for elem in equations]
        cond_all_oofuns_but_not_cons = not any(ConstraintTags) 
        cond_cons = all(ConstraintTags) 
        if not cond_all_oofuns_but_not_cons and not cond_cons:
            p.err('for FuncDesigner SLE/SNLE constructors args must be either all-equalities or all-oofuns')            
        if p.fTol is not None:
            fTol = min((p.ftol, p.fTol))
            p.warn('''
            both ftol and fTol are passed to the SNLE;
            minimal value of the pair will be used (%0.1e);
            also, you can modify each personal tolerance for equation, e.g. 
            equations = [(sin(x)+cos(y)=-0.5)(tol = 0.001), ...]
            ''' % fTol)
        else:
            fTol = p.ftol
        p.fTol = p.ftol = fTol
        appender = lambda arg: [appender(elem) for elem in arg] if isinstance(arg, (ndarray, list, tuple, set))\
        else ((arg.oofun*(fTol/arg.tol) if arg.tol != fTol and arg.tol != 0 else arg.oofun) if arg.isConstraint else arg)
        EQs = []
        for eq in equations:
            rr = appender(eq)
            if type(rr) == list:
                EQs += rr
            else:
                EQs.append(rr)
        #EQs = [((elem.oofun*(fTol/elem.tol) if elem.tol != 0 else elem.oofun) if elem.isConstraint else elem) for elem in equations]
        if p.probType in ('SLE', 'LLSP'): 
            p.C = EQs
        elif p.probType in ('NLSP', 'SNLE'): 
            p.f = EQs
#                    p.user.F = EQs
        else: 
            p.err('bug in OO kernel')
    else:
        F = [p.f]
        updateDep(probDep, p.f)
        
    probDep2 = probDep.copy()
    updateDep(probDep, p.constraints)
    updateDepWithInvolvedVariables(probDep2, p.constraints)
    
    unInvolvedVariables = probDep.difference(probDep2) # that have only box constraints
    
    
    
    # TODO: implement it
    
#            startPointVars = set(p.x0.keys())
#            D = startPointVars.difference(probDep)
#            if len(D):
#                print('values for variables %s are missing in start point' % D)
#            D2 = probDep.difference(startPointVars)
#            if len(D2):
#                p.x0 = dict([(key, p.x0[key]) for key in D2])

    for fn in ['lb', 'ub', 'A', 'Aeq', 'b', 'beq']:
        if not hasattr(p, fn): continue
        val = getattr(p, fn)
        if val is not None and any(isfinite(val)):
            p.err('while using oovars providing lb, ub, A, Aeq for whole prob is forbidden, use for each oovar instead')
            
    if not isinstance(p.x0, dict):
        p.err('Unexpected start point type: ooPoint or Python dict expected, '+ str(type(p.x0)) + ' obtained')
    
    x0 = p.x0.copy()

    tmp = []
    p._init_ooarrays = set()
    p._init_fixed_ooarrays = set()
    
    for key, val in x0.items():
        if type(key) == ooarray:
            p._init_ooarrays.add(key)
        if isinstance(val, Stochastic):
            p._isStochastic = True
        if not isinstance(key, (list, tuple, ndarray)):
            tmp.append((key, val))
        else: # can be ooarray 
            val = atleast_1d(val)
            if len(key) != val.size:
                p.err('''
                for the sake of possible bugs prevention lenght of oovars array 
                must be equal to lenght of its start point value, 
                assignments like x = oovars(m); startPoint[x] = 0 are forbidden, 
                use startPoint[x] = [0]*m or np.zeros(m) instead''')
            for i in range(val.size):
                tmp.append((key[i], val[i]))
    Tmp = dict(tmp)
    
    if isinstance(p.fixedVars, dict):
        for key, val in p.fixedVars.items():
            if type(key) == ooarray:
                p._init_fixed_ooarrays.add(key)
            if isinstance(key, (list, tuple, ndarray)): # can be only ooarray 
                if type(val) not in (list, tuple, ndarray) or len(key) != len(val):
                    p.err('''
                    for the sake of possible bugs prevention lenght of oovars array 
                    must be equal to lenght of its start point value, 
                    assignments like x = oovars(m); fixedVars[x] = 0 are forbidden, 
                    use fixedVars[x] = [0]*m or np.zeros(m) instead''')
                for i in range(len(val)):
                    Tmp[key[i]] = val[i]
            else:
                Tmp[key] = val
        p.fixedVars = set(p.fixedVars.keys())
    # mb other operations will speedup it?
    if p.probType != 'ODE':
        Keys = set(Tmp.keys()).difference(probDep)
        for key in Keys:
            Tmp.pop(key)
            
    p.probDep = probDep
    x0 = p.x0 = Tmp
    p._aux_fixedVars = dict((v, x0[v]) for v in unInvolvedVariables)
    p._stringVars = set()
    for key, val in x0.items():
        #if key.domain is not None and key.domain is not bool and key.domain is not 'bool':
        if type(val) in (str, string_):
            p._stringVars.add(key)
            key.formAuxDomain()
            x0[key] = key.aux_domain[val]#searchsorted(key.aux_domain, val, 'left')
        elif key.fields == () and key.domain is not None and key.domain is not bool and key.domain is not 'bool' \
        and key.domain is not int and key.domain is not 'int' and val not in key.domain:
            x0[key] = key.domain[0]
    
    x0 = p.x0 = oopoint(x0)
    x0.maxDistributionSize = p.maxDistributionSize

    from fdTranslators import setStartVectorAndTranslators
    setStartVectorAndTranslators(p)
    
    F_ = p.C if p.probType in ('SLE', 'LLSP') else p.f
    
    f_elems = [F_] if isinstance(F_, oofun) else F_.view(ndarray) if isinstance(F_, ooarray) else F 

    # TODO: rework it for MOP
    f_order = inf if p.probType=='MOP' else PythonMax(elem.getOrder(p.freeVarsSet, p.fixedVarsSet, fixedVarsScheduleID = p._FDVarsID) for elem in f_elems)
    #print('f_order:', f_order)
    
    if p.probType in ['LP', 'MILP', 'SOCP'] and f_order > 1:
        p.err('for LP/MILP objective function has to be linear, while this one ("%s") is not' % p.f.name)
    
    if p.fixedVars is None:
       D_kwargs = {'fixedVars':p.fixedVarsSet}
    elif p.freeVars is not None and len(p.freeVars)<len(p.fixedVars):
        D_kwargs = {'Vars':p.freeVarsSet}
    else:
        D_kwargs = {'fixedVars':p.fixedVarsSet}
    D_kwargs['useSparse'] = p.useSparse
    D_kwargs['fixedVarsScheduleID'] = p._FDVarsID
    D_kwargs['exactShape'] = True
    
    p._D_kwargs = D_kwargs
    
    variableTolerancesDict = dict((v, v.tol) for v in p._freeVars)
    p.variableTolerances = p._point2vector(variableTolerancesDict)
    
    if len(p._fixedVars) < len(p._freeVars) and 'isdisjoint' in dir(set()):
        areFixed = lambda dep: dep.issubset(p.fixedVarsSet)
        #isFixed = lambda v: v in p._fixedVars
        Z = dict((v, zeros_like(val) if v not in p.fixedVarsSet else val) for v, val in p._x0.items())
        _isFixedNonStoch = lambda t: t in p.fixedVarsSet and not isinstance(p._x0[t], Stochastic)#could be improved
    else:
        areFixed = lambda dep: dep.isdisjoint(p.freeVarsSet)
        #isFixed = lambda v: v not in p._freeVars
        Z = dict((v, zeros_like(val) if v in p.freeVarsSet else val) for v, val in p._x0.items())
        _isFixedNonStoch = lambda t: t not in p.freeVarsSet and not isinstance(p._x0[t], Stochastic)#could be improved
    p._isFixedNonStoch = _isFixedNonStoch
    p._areFixed = areFixed
    Z = oopoint(Z, maxDistributionSize = p.maxDistributionSize)
    p._Z = Z
   
    #p.isFixed = isFixed
    lb, ub = -inf*ones(p.n), inf*ones(p.n)

    # TODO: get rid of start c, h = None, use [] instead
    A, b, Aeq, beq = [], [], [], []
    
    if type(p.constraints) not in (list, tuple, set):
        p.constraints = [p.constraints]
    oovD = p._oovarsIndDict
    LB = {}
    UB = {}
    
    """                                    gather attached constraints                                    """
    C = list(p.constraints)
    p._initial_constraints = C
    p.constraints = set(p.constraints)
    for v in p._x0.keys():
#                if v.fields != ():
#                    v.aux_domain = Copy(v.domain)
##                    # TODO: mb rework it
##                    ind_numeric = [j for j, elem in enumerate(v.aux_domain[0]) if type(elem) not in (str, np.str_)]
##                    if len(ind_numeric):
##                        ind_first_numeric = ind_numeric[0]
##                        v.aux_domain.sort(key = lambda elem: elem[ind_first_numeric])
#                    v.domain = np.arange(len(v.domain))
        if not array_equal(v.lb, -inf):
            p.constraints.add(v >= v.lb)
        if not array_equal(v.ub, inf):
            p.constraints.add(v <= v.ub)            
            
    if p.useAttachedConstraints: 
        if hasattr(p, 'f'):
            if type(p.f) in [list, tuple, set]:
                C += list(p.f)
            else: # p.f is oofun
                C.append(p.f)
        p.constraints.update(_getAllAttachedConstraints(C))

    FF = p.constraints.copy()
    for _F in F:
        if isinstance(_F, (tuple, list, set)):
            FF.update(_F)
        elif isinstance(_F, ndarray):
            if _F.size > 1:
                FF.update(_F)
            else:
                FF.add(_F.item())
        else:
            FF.add(_F)
    unvectorizableFuncs = set()

    #unvectorizableVariables = set([var for var, val in p._x0.items() if isinstance(val, _Stochastic) or asarray(val).size > 1])
    
    # TODO: use this
    unvectorizableVariables = set([])
    
    # temporary replacement:
    #unvectorizableVariables = set([var for var, val in p._x0.items() if asarray(val).size > 1])
    
    
    cond = False
    #debug
#            unvectorizableVariables = set(p._x0.keys())
#            hasVectorizableFuncs = False
#            cond = True
    #debug end
    if 1 and isPyPy:
        hasVectorizableFuncs = False
        unvectorizableFuncs = FF
    else:
        hasVectorizableFuncs = False
        if len(unvectorizableVariables) != 0:
            for ff in FF:
                _dep = ff._getDep()
                if cond or len(_dep & unvectorizableVariables) != 0:
                    unvectorizableFuncs.add(ff)
                else:
                    hasVectorizableFuncs = True
        else:
            hasVectorizableFuncs = True
    p.unvectorizableFuncs = unvectorizableFuncs
    p.hasVectorizableFuncs = hasVectorizableFuncs
    
    for v in p.freeVarsSet:
        d = v.domain
        if d is bool or d is 'bool':
            p.constraints.update([v>0, v<1])
        elif d is not None and d is not int and d is not 'int':
            # TODO: mb add integer domains?
            v.domain = array(list(d))
            v.domain.sort()
            p.constraints.update([v >= v.domain[0], v <= v.domain[-1]])
            if hasattr(v, 'aux_domain'):
                p.constraints.add(v <= len(v.aux_domain)-1)
            
#            for v in p._stringVars:
#                if isFixed(v):
#                    ind = searchsorted(v.aux_domain, p._x0[v], 'left')
#                    if v.aux_domain

    """                                         handling constraints                                         """
    StartPointVars = set(p._x0.keys())
    p._dictOfStochVars = dict((k, v) for k, v in p._x0.items() if isinstance(v, Stochastic))
    p.dictOfFixedFuncs = {}
    p._dictOfRedirectedFuncs = {}#p._dictOfStochVars
#    p._init_ooarrays = set()
    hasFixedVariables = len(p.fixedVarsSet)
    
    from FuncDesigner import broadcast
    if hasFixedVariables:
        for item in f_elems:
           broadcast(formDictOfFixedFuncs, item, p.useAttachedConstraints, p)
    if p._isStochastic:
        broadcast(formDictOfRedirectedFuncs, f_elems, p.useAttachedConstraints, p)
#    broadcast(getInitOOArrays, f_elems, p.useAttachedConstraints, p)
        
    if oosolver(p.solver).useLinePoints:
        p._firstLinePointDict = {}
        p._secondLinePointDict = {}
        p._currLinePointDict = {}
        
    inplaceLinearRender = oosolver(p.solver).__name__ == 'interalg'
    
    if inplaceLinearRender and hasattr(p, 'f'):
        D_kwargs2 = D_kwargs.copy()
        D_kwargs2['useSparse'] = False
        if type(p.f) in [list, tuple, set]:
            ff = []
            for f in p.f:
                if f.getOrder(p.freeVarsSet, p.fixedVarsSet, fixedVarsScheduleID = p._FDVarsID) < 2:
                    D = f.D(Z, **D_kwargs2)
                    f2 = linear_render(f, D, Z)
                    ff.append(f2)
                else:
                    ff.append(f)
            p.f = ff
        else: # p.f is oofun
            if f_order < 2:
                D = p.f.D(Z, **D_kwargs2)
                p.f = linear_render(p.f, D, Z)
                if p.isObjFunValueASingleNumber:
                    p._linear_objective = True
                    p._linear_objective_factor = p._pointDerivative2array(D).flatten()
                    p._linear_objective_scalar = p.f(Z)
                    
    handleConstraint_args = (StartPointVars, areFixed, oovD, A, b, Aeq, beq, Z, D_kwargs, LB, UB, inplaceLinearRender)
    
    for c in p.constraints:
        if isinstance(c, ooarray):
            for elem in c: 
                fdConstraint(p, elem, *handleConstraint_args) 
        elif c is True:
            continue
        elif c is False:
            p.err('one of elements from constraints is "False", solution is impossible')
        elif not hasattr(c, 'isConstraint'): 
            p.err('The type ' + str(type(c)) + ' is inappropriate for problem constraints')
        else:
            fdConstraint(p, c, *handleConstraint_args)

    '''                                              Handling A, Aeq, lb, ub                                                         '''
    if len(b) != 0:
        p.A, p.b = Vstack(A), Hstack([ravel(elem) for elem in b])
        if hasattr(p.b, 'toarray'): p.b = p.b.toarray()
    if len(beq) != 0:
        p.Aeq, p.beq = Vstack(Aeq), Hstack([ravel(elem) for elem in beq])
        if hasattr(p.beq, 'toarray'): p.beq = p.beq.toarray()
    for vName, vVal in LB.items():
        inds = oovD[vName]
        lb[inds[0]:inds[1]] = vVal
    for vName, vVal in UB.items():
        inds = oovD[vName]
        ub[inds[0]:inds[1]] = vVal
    p.lb, p.ub = lb, ub
    


##########################################################
def updateDep(Dep, elem):
    from FuncDesigner import oofun
    
    return [updateDep(Dep, f) for f in elem] if isinstance(elem, (tuple, list, set))\
    else [updateDep(Dep, f) for f in atleast_1d(elem)] if isinstance(elem, ndarray)\
    else Dep.update(set([elem]) if elem.is_oovar \
    else elem._getDep()) if isinstance(elem, oofun)\
    else None

def updateDepWithInvolvedVariables(Dep, elem): 
    # skips oovars that have only box bounds and are not involved in 
    # neither objective nor other constraints
    
    from FuncDesigner import oofun
    from FuncDesigner.constraints import BoxBoundConstraint
#    if type(elem) == list:
#        print elem
#    else:
#        print elem.expr, isinstance(elem, BoxBoundConstraint)
#    print '-----'
#    
    
    return [updateDepWithInvolvedVariables(Dep, f) for f in elem] if isinstance(elem, (tuple, list, set))\
    else [updateDepWithInvolvedVariables(Dep, f) for f in atleast_1d(elem)] if isinstance(elem, ndarray)\
    else Dep.update(set([elem]) if elem.is_oovar \
    else elem._getDep()) if isinstance(elem, oofun) and not isinstance(elem, BoxBoundConstraint)\
    else None
