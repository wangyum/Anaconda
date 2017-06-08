from ooFun import oofun, atleast_oofun
import numpy as np
from FDmisc import FuncDesignerException
from translator import FuncDesignerTranslator
from ooPoint import ooPoint as oopoint
from ooVar import oovar

try:
    from scipy import integrate
    scipyInstalled = True
except:
    scipyInstalled = False

def integrator(func, domain,  **kwargs):
    if not scipyInstalled:
        raise FuncDesignerException('to use scipy_integrate_quad you should have scipy installed, see scipy.org')

#    if not isinstance(domain, dict) or len(domain) != 1: 
#        raise FuncDesignerException('currently integration domain must be of type Pythoon dict {integr_var:(val_from, val_to)} only')
    
    #integration_var = domain.keys()[0]
    #_from, _to =  domain.values()[0]
    integration_var, a, b = domain
    if not isinstance(integration_var, oovar):
        raise FuncDesignerException('integration variable must be FuncDesigner oovar')
    a, b, func = atleast_oofun(a), atleast_oofun(b), atleast_oofun(func)

    def f(point=None):

        p2 = point.copy()
        #if integration_var not in p2:
            #p2[integration_var] = 0.0 # to ajust size, currently only R^1 is implemented
        #T = FuncDesignerTranslator(p2)
        def vect_func(x):
            p2[integration_var] = x
            tmp = func(p2)
            if np.isscalar(tmp): return tmp
            elif tmp.size == 1: return np.asscalar(tmp)
            else: FuncDesignerException('incorrect data type, probably bug in uncDesigner kernel')
    #vect_func = lambda x: func(T.vector2point(x))

        # TODO: better handling of fixed variables
        return integrate.quad(vect_func, a(point), b(point), **kwargs)[0]
       
#    def aux_f(point):
#        point = oopoint(_point)
#        if a(point).size != b(point).size: raise FuncDesignerException('sizes of point-from and point-to must be equal')
#        if a(point).size != 1 or b(point).size != 1:  raise FuncDesignerException('currently integration is implemented for single variable only')
#        dep = a._getDep() | b._getDep() | func._getDep()
#        involved_vars = set(point.keys()).add(integration_var)
#        if not dep.issubset(involved_vars): raise FuncDesignerException('user-provided point for integration has no information on some variables')
#        
#        p2 = point.copy()
#        if integration_var not in p2:
#            p2[integration_var] = 0.0 # to ajust size, currently only R^1 is implemented
#        T = FuncDesignerTranslator(p2)
#        vect_func = lambda x: func(T.vector2point(x))
        
    
    # TODO: derivatives
    # !!!!!!!!!!!!! TODO: derivatives should not be zeros! Fix it!
    r = oofun(f, None) 
    r.fun = lambda *args: f(point=r._Point)
    
    # TODO : use decorators here
    tmp_f = r._getFunc
    tmp_D = r._D
    def aux_f(*args,  **kwargs):
        if isinstance(args[0], dict):
            r._Point = args[0]
        return tmp_f(*args,  **kwargs)
    def aux_D(*args,  **kwargs):
        raise FuncDesignerException('derivatives from scipy_quad are not implemented yet')
        if isinstance(args[0], dict):
            r._Point = args[0]
        return tmp_D(*args,  **kwargs)
    r._getFunc = aux_f
    r._D = aux_D
    
    return r

#    r = oofun(lambda x, y: integrate.quad(func, x, y, **kwargs)[0], input = [a, b])
#    r.d = (lambda x, y: -func(x), lambda x, y: func(y))
#    return r
    
#def 
    
