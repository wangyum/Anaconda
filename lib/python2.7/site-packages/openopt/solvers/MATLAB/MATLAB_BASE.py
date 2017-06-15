from openopt.kernel.baseSolver import baseSolver
from mlabwrap import mlab

scipy_installed = False
try:
    from scipy.sparse import find, isspmatrix
    scipy_installed = True
except ImportError:
    pass

class MATLAB_BASE(baseSolver):
    __license__ = "proprietary"
    __authors__ = "Mathworks"
    _requiresBestPointDetection = True
    
    def _Solve(self, p, *args):
        SolverName = self.__name__
        if scipy_installed:
            Args = [arg if not isspmatrix(arg) else scipy_sparse_to_mlab_sparse(arg) for arg in args]
        else:
            Args = list(args)
        
        opts = []
        for fn in self.opts: 
            opts += [fn, optConverter(p, fn)]
        opts = mlab.optimoptions(SolverName, *opts)
        
        Args.append(opts)
        r = getattr(mlab, SolverName)(*Args)
        p.istop = 1000
        return r

def optConverter(p, fn):
    if fn == 'Display':
        return 'off' if p.iprint < 0 else 'final' if p.iprint == 0 else 'iter'
    elif fn == 'TolFun':
        return p.ftol
    elif fn == 'TolX':
        return p.xtol
    elif fn == 'MaxIter':
        return p.maxIter
    elif fn == 'MaxTime':
        return p.maxTime
    elif fn == 'TolXInteger':
        return p.discrtol
    else:
        assert 0, 'incorrect or unimplemented in OpenOpt yet MATLAB param'
        
def scipy_sparse_to_mlab_sparse(scipy_sparse_matrix): 
    I, J, values = find(scipy_sparse_matrix)
    return mlab.sparse(I+1, J+1, values, scipy_sparse_matrix.shape[0], scipy_sparse_matrix.shape[1]) 
