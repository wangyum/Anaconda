import numpy as np, operator as o
from numpy import ndarray
from FuncDesigner.FDmisc import FuncDesignerException
from baseClasses import *

if 'div' in o.__dict__:
    div = o.div
else:
    div = o.truediv

#div = o.truediv

# TODO: rework buggy multiarray.size
#delattr(multiarray, 'size')

complementarity = {
                     o.add: o.add, 
                     o.sub: lambda x, y: y-x, 
                     o.mul: o.mul, 
                     div: lambda x, y: div(y, x), 
                     o.truediv: lambda x, y: truediv(y, x), 
                     o.pow: lambda x, y: pow(y, x), 
                     }

class multiarray(MultiArray):
    __array_priority__ = 5
    __add__ = lambda self, other: multiarray_op(self, other, o.add)
    __radd__ = __add__
    
    __sub__ = lambda self, other: multiarray_op(self, other, o.sub)
    __rsub__ = lambda self, other: multiarray_op(-self, other, o.add)
#    __neg__ = lambda self: (-self.view(ndarray)).view(multiarray)
    
    __mul__ = lambda self, other: multiarray_op(self, other, o.mul)
    __rmul__ = __mul__

    __div__ = lambda self, other: multiarray_op(self, other, div)
    __rdiv__ = lambda self, other: multiarray_op(other, self, div)
    
    __truediv__ = __div__
    __rtruediv__ = __rdiv__
    
    __pow__ = lambda self, other: multiarray_op(self, other, o.pow)
    __rpow__ = lambda self, other: multiarray_op(other, self, o.pow)
    
    __str__ = lambda self: str(self.view(ndarray))
    
    def __getitem__(self, ind): 
#        print '>', ind
#        if self.ndim <= 1:
#            if ind is 0:
#                return self
#            else:
#                print('multiarray ind:', ind)
#        print type(ind), ind
#        if ind == -3:
#            pass

        return (self.view(np.ndarray)[:, ind] if self.ndim > 1 else self.view(np.ndarray)[ind])\
        .view(multiarray)  if type(ind) in (int, np.int32, np.int64, np.int16, np.int8) \
        else self.__getslice__(ind.start, ind.stop) if type(ind) != tuple \
        else self.__getslice__(ind[0], ind[1])
        
        
    def __getslice__(self, ind1, ind2):
#        print '!', ind1, ind2
        #TODO: mb check if size is known then use it instead of None?
        cond_1 = ind1 is None
        cond_2 = ind2 is None or (type(ind2) == slice and ind2.start is None and ind2.stop is None and ind2.step is None)
        if cond_1 and cond_2:
            return self
            
        if cond_1: 
            ind1 = 0
        if cond_2: 
            ind2 = self.shape[1]
        r = self.view(np.ndarray)[:, ind1:ind2] if self.ndim > 1 else self.view(np.ndarray)[ind1:ind2]
        return r.view(multiarray)
        
        
    # TODO: check it!
    #toarray = lambda self: self.view(ndarray)

    def sum(self, *args, **kw):
        if any(v is not None for v in args): # somehow triggered from pswarm
            raise FuncDesignerException('arguments for FD multiarray sum are not implemened yet')
        if any(v is not None for v in kw.values()):
            raise FuncDesignerException('keyword arguments for FD multiarray sum are not implemened yet')
        tmp = self.reshape(-1, 1) if self.ndim < 2 else self
        return np.sum(tmp.view(ndarray), 1).view(multiarray)

def multiarray_op(x, y, op):
    if isinstance(y, Stochastic):
        return complementarity[op](y, x)
    if isinstance(y, multiarray):
#        print type(x)
#        if isinstance(x, Stochastic):
#            print('asdf1')
        Y = y.reshape(-1, 1) if y.ndim < 2 else y
        if isinstance(x, multiarray):
            assert x.ndim < 3 and y.ndim < 3, 'unimplemented yet'
            X = x.reshape(-1, 1) if x.ndim < 2 else x
            r = op(X.view(ndarray), Y.view(ndarray))
        else:
            r = op(x.reshape(-1, 1) if isinstance(x, ndarray) and x.size != 1 else x, Y.view(ndarray).T).T
    elif isinstance(x, multiarray): # and y is not multiarray here
#        print type(y)
#        if isinstance(y, Stochastic):
#            print('asdf1')
        X = x.reshape(-1, 1) if x.ndim < 2 else x
        r = op(X.view(ndarray), y.reshape(1, -1) if isinstance(y, ndarray) and y.size != 1 else y)
    else: # neither x nor y are multiarrays
        raise FuncDesignerException('bug in FuncDesigner kernel')
    return r.view(multiarray)


