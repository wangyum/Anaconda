from openopt.kernel.baseSolver import baseSolver
import DIRECT, numpy as np
from openopt.kernel.setDefaultIterFuncs import SMALL_DELTA_X,  SMALL_DELTA_F

class direct(baseSolver):
    __name__ = 'direct'
    __license__ = "MIT"
    __authors__ = ''
    __alg__ = ""
    iterfcnConnected = False
    __homepage__ = ''

    __info__ = ""
    __optionalDataThatCanBeHandled__ = ['lb', 'ub']
    __isIterPointAlwaysFeasible__ = True#lambda self, p: p.__isNoMoreThanBoxBounded__()
    _requiresFiniteBoxBounds = True
    
    
    eps=0.0001
#    maxf=20000
#    maxT=6000
    algmethod=0
#    fglobal=-1e+100
    fglper=0.01
    volper=-1.0
    sigmaper=-1.0
    logfilename='DIRresults.txt'
    
    funcForIterFcnConnection = 'f'
    _requiresBestPointDetection = True

    def __init__(self):pass
    def __solver__(self, p):

        #if not p.__isFiniteBoxBounded__(): p.err('this solver requires finite lb, ub: lb <= x <= ub')
        
        p.kernelIterFuncs.pop(SMALL_DELTA_X, None)
        p.kernelIterFuncs.pop(SMALL_DELTA_F, None)

        def objective(x, userData = None):
            r = p.f(x)
            has_nan = int(np.any(np.isnan(r)))
            return r, has_nan

        lb, ub = p.lb, p.ub
#        lb[lb < -1e20] = -1e20
#        ub[ub > 1e20] = 1e20

        maxf = min((p.maxFunEvals, 19999))
        maxT = min((p.maxIter, 89999))
        fglobal = max((p.fOpt, -1e+100))
        
        xf, fmin, ierror = DIRECT.solve(objective, lb, ub, eps=self.eps, maxf=maxf, maxT=maxT, 
                                        algmethod=self.algmethod, fglobal=fglobal, fglper=self.fglper, 
                                        volper=self.volper, sigmaper=self.sigmaper, 
                                        logfilename=self.logfilename)
        
        p.xf, p.ff = xf, fmin
        if p.istop == 0: 
            p.istop = 1000
            p.msg = ierror

