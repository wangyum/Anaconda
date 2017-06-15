PythonAny = any
PythonAll = all
from numpy import isscalar, ndarray, asscalar
from oologfcn import OpenOptException

    
def formDictOfFixedFuncs(oof, p):
    dictOfFixedFuncs, startPoint = p.dictOfFixedFuncs, p._x0
    from FuncDesigner.distribution import Stochastic
    oof = p._dictOfRedirectedFuncs.get(oof, oof)
    dep = oof.Dep#set([oof]) if oof.is_oovar else oof._getDep()
    # TODO: rework it as mixin of fixed and stoch variables
    #if PythonAll((isinstance(startPoint[t], stochasticDistribution) or areFixed(set([t]))) for t in dep):
#    cond_st = not PythonAny(isinstance(startPoint[t], stochasticDistribution) for t in dep) \
#    or 
    isFixedNonStoch = p._isFixedNonStoch
    x0 = p._x0
#    stochEngines = ('mean', 'std','var')

    cond = lambda t: isFixedNonStoch(t) or (isinstance(x0[t], Stochastic) and oof.engine == 'mean')
    c1 = PythonAll(cond(t) for t in dep)
    if c1:
        dictOfFixedFuncs[oof] = oof(startPoint)#TODO: add fixity ID as additional argument to the func

def linear_render(f, D, Z):
    #TODO: linear render for linear parts of sum of oofuns
    import FuncDesigner as fd
    if len(D) == 0:
        raise OpenOptException('probably you try to optimize a fixed constant')
    if f.is_oovar: 
        return f
    ff = f(Z)
    name, tol, _id = f.name, f.tol, f._id
    tmp = [(v if isscalar(val) and val == 1.0 else v * (val if type(val) != ndarray or val.ndim < 2 else val.flatten())) \
    for v, val in D.items()]

    c = ff if isscalar(ff) or ff.ndim <= 1 else asscalar(ff)
    if c != 0: tmp.append(c)
    f = tmp[0] if len(tmp) == 1 else tmp[0]+tmp[1] if len(tmp) == 2 else fd.sum(tmp)
    
    f.name, f.tol, f._id = name, tol, _id
    
    return f



def hasStochDep(s, x0):
    from FuncDesigner import oofun, ooarray
    from FuncDesigner.distribution import stochasticDistribution
#    print [isinstance(t, stochasticDistribution) for t in s.Dep]
    cond1 = (isinstance(s, oofun) and PythonAny(isinstance(x0[t], stochasticDistribution) for t in s.Dep))
    cond2 = (isinstance(s, ooarray) and PythonAny(hasStochDep(t, x0) for t in s.view(ndarray)))
    return cond1 or cond2
#    (isinstance(s, ooarray) and PythonAny(hasStochDep(t) for t in s.view(ndarray)))
    
def Get(elem, p):
    elem2 = p.dictOfFixedFuncs.get(elem, None)
    if elem2 is not None:
        return elem2

    return p._dictOfRedirectedFuncs.get(elem, elem)

def formDictOfRedirectedFuncs(elem, p):
#    return
    from FuncDesigner.overloads import prod as fd_prod
    from FuncDesigner import mean as fd_mean, oofun, abs as fd_abs, std as fd_std, var as fd_var
    x0 = p._x0
    dictOfRedirectedFuncs = p._dictOfRedirectedFuncs
#    if not isinstance(elem, oofun):# for more safety
#        return 
    #!!!!!!!!!!!! TODO: handle ooarray
    if not hasStochDep(elem, x0):
        return
    Iterator = elem.input if not elem._isSum else elem._summation_elements
    for elem_ in Iterator:
        elem_origin = elem_
        elem_ = dictOfRedirectedFuncs.get(elem_, elem_)
        if not isinstance(elem_, oofun):
            continue
        if elem_.engine in ('mean', 'std', 'var'):
#            print elem_.expr
            assert len(elem_.input) == 1, 'bug in FD kernel'
            inp = elem_.input[0]
#            if inp in p._dictOfRedirectedFuncs:
            if inp._isProd:
                inds = [True if hasStochDep(Get(s, p), x0) else False for s in inp._prod_elements]
                ordinaryElems = [Get(s, p) for j, s in enumerate(inp._prod_elements) if not inds[j]]
#                if len(ordinaryElems) == 0:
#                    continue
                stochElems = [Get(s, p) for j, s in enumerate(inp._prod_elements) if inds[j]]
                
                Tmp, tmp = fd_prod(ordinaryElems), fd_prod(stochElems)
#                formDictOfRedirectedFuncs(tmp, p)

                #TODO: rework _areFixed
                if isinstance(tmp, oofun) and p._areFixed(tmp.Dep):
                    tmp = tmp(p._x0)
                
                T = fd_mean(tmp) if elem_.engine == 'mean' else\
                fd_std(tmp) if elem_.engine == 'std' else \
                fd_var(tmp)
                
                if type(Tmp) == oofun:
                    formDictOfRedirectedFuncs(T, p)
                    T = dictOfRedirectedFuncs.get(T, T)
                    
                newElem = \
                Tmp * T if elem_.engine == 'mean' else \
                fd_abs(Tmp) * T if elem_.engine == 'std' else \
                Tmp**2 * T # for elem_.engine == 'var'
                
                dictOfRedirectedFuncs[elem_] = dictOfRedirectedFuncs[elem_origin] = newElem
                
                #TODO: store summation elements in dict
                # or mb store inputs in dict
                
                
                
#                elem_.input = [newElem]
        else:
            pass

# TODO: redirection for linear rest of sum
#def render_linear_parts(elem, p):
##    return
##    from FuncDesigner.overloads import prod as fd_prod
#    from FuncDesigner import oofun
#    x0 = p._x0
##    if not isinstance(elem, oofun):# for more safety
##        return 
#    #!!!!!!!!!!!! TODO: handle ooarray
#
#    Iterator = elem.input if not elem._isSum else elem._summation_elements
#    for elem_ in Iterator:
#        elem_origin = elem_
#        elem_ = p._dictOfRedirectedFuncs.get(elem_, elem_)
#        if not isinstance(elem_, oofun):
#            continue
#        if elem_.engine in ('mean', 'std', 'var'):
##            print elem_.expr
#            assert len(elem_.input) == 1, 'bug in FD kernel'
#            inp = elem_.input[0]
##            if inp in p._dictOfRedirectedFuncs:
#            if inp._isProd:
#                inds = [True if hasStochDep(s, x0) else False for s in inp._prod_elements]
#                ordinaryElems = [Get(s, p) for j, s in enumerate(inp._prod_elements) if not inds[j]]
#                if len(ordinaryElems) == 0:
#                    continue
#                stochElems = [Get(s, p) for j, s in enumerate(inp._prod_elements) if inds[j]]
#                
#                Tmp, tmp = fd_prod(ordinaryElems), fd_prod(stochElems)
#                if isinstance(tmp, oofun) and p._areFixed(tmp.Dep):
#                    tmp = tmp(p._x0)
#                newElem = \
#                Tmp * fd_mean(tmp) if elem_.engine == 'mean' else \
#                fd_abs(Tmp) * fd_std(tmp) if elem_.engine == 'std' else \
#                Tmp**2 * fd_var(tmp) # for elem_.engine == 'var'
#                
#                p._dictOfRedirectedFuncs[elem_] = p._dictOfRedirectedFuncs[elem_origin] = newElem
##                elem_.input = [newElem]
#        else:
#            pass
