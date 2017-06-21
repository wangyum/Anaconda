# created by Dmitrey

#from numpy import inf, asfarray, copy, all, any, empty, atleast_2d, zeros, dot, asarray, atleast_1d, empty, ones, ndarray, \
#where, array, nan, ix_, vstack, eye, array_equal, isscalar, diag, log, hstack, sum, prod, nonzero, isnan
#from numpy.linalg import norm
#from misc import FuncDesignerException, Diag, Eye, pWarn, scipyAbsentMsg
#from copy import deepcopy

from FDmisc import FuncDesignerException
from baseClasses import Stochastic
from numpy import ndarray, isscalar, atleast_1d
try:
    from scipy.sparse import isspmatrix
except ImportError:
    isspmatrix = lambda *args, **kw: False

Len = lambda x: 1 if isscalar(x) else x.size if type(x)==ndarray else len(x)

   

def ooMultiPoint(*args, **kw):
    kw['skipArrayCast'] = True
    r = ooPoint(*args, **kw)
    r.isMultiPoint = True
    return r

class ooPoint(dict):
    _id = 0
    isMultiPoint = False
    modificationVar = None # default: no modification variable
    useSave = True
    useAsMutable = False
    exactRange = True
    surf_preference = False
    skipArrayCast = False
    
    def __init__(self, *args, **kwargs):
        self.storedIntervals = {}
        self.storedSums = {}
        self.dictOfFixedFuncs = {}
        self._dictOfStochVars = {}
        self._dictOfRedirectedFuncs = {}
        
        for fn in ('isMultiPoint', 'modificationVar', 'useSave', 'skipArrayCast', 'maxDistributionSize', 
        'useAsMutable', 'maxDistributionSize', 'resolveSchedule', 'surf_preference'):
            tmp = kwargs.get(fn, None)
            if tmp is not None:
                setattr(self, fn, tmp)
        
#        if self.skipArrayCast: 
#            Asanyarray = lambda arg: arg
#        else: 
#            Asanyarray = lambda arg: asanyarray(arg) if not isinstance(arg, Stochastic) else arg#if not isspmatrix(arg) else arg
            
        assert args or kwargs, 'incorrect oopoint constructor arguments'
        Iterator = (args[0].items() if isinstance(args[0], dict) else args[0]) if args else kwargs.items()
        # TODO: remove float() after Python 3 migration
        
        if self.skipArrayCast: 
            items = Iterator#((key, (Asanyarray(val[0]), Asanyarray(val[1])) if type(val) == tuple\
#            else float(val) if type(val) == int\
#            else val) for key, val in Iterator)
        else:
            # TODO: rework it
            items = ((key, (atleast_1d(val[0]), atleast_1d(val[1])) if type(val) == tuple\
            else atleast_1d(val) if not isinstance(val, Stochastic)\
            else val)\
            for key, val in Iterator)
        dict.__init__(self, items)

# TODO: fix it wrt ode2.py

#        for key, val in items:
#            #assert type(val) not in [list, ndarray] or type(val[0]) != int
#            if 'size' in key.__dict__ and type(key.size) == int and Len(val)  != key.size: 
#                s = 'incorrect size for oovar %s: %d is required, %d is obtained' % (key, self.size, Size)
#                raise FuncDesignerException(s)
        
        ooPoint._id += 1
        self._id = ooPoint._id
    
    def __setitem__(self, *args, **kwargs):
        if not self.useAsMutable:
            raise FuncDesignerException('ooPoint must be immutable')
        dict.__setitem__(self, *args, **kwargs)
        
