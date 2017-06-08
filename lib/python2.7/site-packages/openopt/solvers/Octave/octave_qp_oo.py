from oct2py import Oct2Py
oc = Oct2Py()
from openopt.kernel.baseSolver import baseSolver
from openopt.kernel.nonOptMisc import isspmatrix
import numpy as np

class octave_qp(baseSolver):
    __name__ = 'octave_qp'
    __alg__ = ''
    __authors__ = ''
#    __isIterPointAlwaysFeasible__ = True
    
    __optionalDataThatCanBeHandled__ = ['lb', 'ub', 'A', 'Aeq', 'b', 'beq']
#    properTextOutput = True
    #_canHandleScipySparse = True

    def __init__(self): pass
    def __solver__(self, p):
        x, obj, info, Lambda = oc.qp(
                                     p.x0.reshape(-1, 1), 
                                     p.H.tocsr() if isspmatrix(p.H) else np.asfarray(p.H), 
                                     np.asfarray(p.f).reshape(-1, 1), 
                                     p.Aeq.tocsr() if isspmatrix(p.Aeq) else np.asfarray(p.Aeq) if p.nbeq != 0 else [], 
                                     p.beq.reshape(-1, 1) if p.nbeq != 0 else [], 
                                     p.lb.reshape(-1, 1), 
                                     p.ub.reshape(-1, 1), 
                                     [], 
                                     p.A.tocsr() if isspmatrix(p.A) else np.asfarray(p.A) if p.nb != 0 else [1.0]*p.n, 
                                     p.b.reshape(-1, 1) if p.nb != 0 else np.inf#p.b.reshape(p.n, 0)
                                     )
        p.xk = p.xf = x.flatten()
        p.istop = 1000
