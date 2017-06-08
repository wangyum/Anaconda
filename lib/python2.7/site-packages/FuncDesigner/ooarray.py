PythonMax = max
PythonAll = all
from baseClasses import OOArray
from FuncDesigner.multiarray import multiarray
from ooFun import oofun
from constraints import Constraint
from numpy import isscalar, asscalar, ndarray, atleast_1d, asanyarray, array
import numpy as np
from FDmisc import FuncDesignerException
from debugMisc import print_info, fd_trace_id

class ooarray(OOArray):
    __array_priority__ = 25 # !!! it should exceed oofun.__array_priority__ !!!
    _is_array_of_oovars = False
    def __new__(self, *args, **kwargs):
        #assert len(kwargs) == 0
        tmp = args[0] if len(args) == 1 else args
        
        ########################
        ########################
        #temp walkaround for an issue that seems to be numpy bug (mb in pypy?)
        obj = array(tmp, object).view(self)
        if obj.dtype == object and PythonAll(np.isscalar(elem) for elem in obj):
            obj = array(tmp, float).view(self)
#        isNumericArray = not PythonAll(np.isscalar(elem) for elem in )
##        if Tmp.dtype != object:
#        obj = (array(tmp, object) if Tmp.dtype == object else Tmp.copy()).view(self)  
        ########################
#        else:
#        obj = array(tmp, object).view(self)
        ########################
        ########################
        
        #if obj.ndim != 1: raise FuncDesignerException('only 1-d ooarrays are implemented now')
        #if obj.dtype != object:obj = np.asfarray(obj) #TODO: FIXME !

        obj._id = oofun._id
        obj.name = 'unnamed_ooarray_%d' % obj._id
        fd_trace_id.object[obj._id] = obj
        
        if fd_trace_id.traces(obj._id):
            print_info(obj)
        
        oofun._id += 1
        return obj
    
    def __init__(self, *args, **kw):
        self._id = oofun._id
        self.name = 'unnamed_ooarray_%d' % self._id
        if fd_trace_id.traces(self._id):
            print_info(self)
        fd_trace_id.object[self._id] = self
        oofun._id += 1

    
    __hash__ = lambda self: self._id
    
    def __len__(self):
        return self.size

    expected_kwargs = set(('tol', 'name'))
    def __call__(self, *args, **kwargs):
        #if self.dtype != object: return self.view(ndarray)
        
        # TODO: give different names for each element while assigning name to ooarray
        expected_kwargs = self.expected_kwargs
        #if not set(kwargs.keys()).issubset(expected_kwargs):
            #raise FuncDesignerException('Unexpected kwargs: should be in '+str(expected_kwargs)+' got: '+str(kwargs.keys()))
            
        for elem in expected_kwargs:
            if elem in kwargs:
                setattr(self, elem, kwargs[elem])
        
        if len(args) > 1: raise FuncDesignerException('No more than single argument is expected')
        
        if len(args) == 0:
           if len(kwargs) == 0: raise FuncDesignerException('You should provide at least one argument')
           #return self
           
        if len(args) != 0 and isinstance(args[0], str):
            self.name = args[0]
            for i, elem in enumerate(self.view(ndarray)):
                if isinstance(elem, oofun):
                    elem(self.name + '_' + str(i))
            args = args[1:]
            if len(args) == 0:
                return self
        #tmp = asarray([asscalar(asarray(self[i](*args, **kwargs))) if isinstance(self[i], oofun) else self[i] for i in range(self.size)])
        
        if self.size == 1 and type(self.item()) == oofun:
            return self.item()(*args, **kwargs)
        
        # TODO: get rid of self in args[0]
        if self._is_array_of_oovars and isinstance(args[0], dict) and self in args[0] and len(args) == 1 and len(kwargs) == 0:
            return args[0][self]
            
        Tmp = [self[i](*args, **kwargs) if isinstance(self[i], oofun) else self[i] for i in range(self.size)]
        tmp = asanyarray(Tmp)
        if np.any([isinstance(elem, multiarray) for elem in Tmp]):
            tmp = tmp.T.view(multiarray)
        if tmp.ndim == 2 or tmp.dtype != object:
            return tmp
        else:
            #tmp = tmp.flatten()
            return ooarray(tmp)

    def expression(self, *args, **kw):
        return str([elem.expression(*args, **kw) if isinstance(elem, oofun) else str(elem) for elem in self.view(ndarray)])
    
    def __getattr__(self, attr):
        if attr == 'dep':
            r = set.union(*[elem.dep for elem in self.view(ndarray) if isinstance(elem, (oofun, ooarray))])
            self.dep = r
            return r
        elif attr == 'expr':
            return str([elem.expr if isinstance(elem, oofun) else str(elem) for elem in self.view(ndarray)])
        else:
            raise AttributeError('incorrect attribute of ooarray')
    
    def _getFuncCalcEngine(self, *args, **kw):
        raise FuncDesignerException('''
        incorrect usage of ooarray evaluation; 
        inform developers if it seems to be a bug
        ''')
    
    def getOrder(self, *args, **kw):
        return PythonMax([0] + [elem.getOrder(*args, **kw) for elem in self.view(ndarray) if isinstance(elem, (oofun, ooarray))])

    def __mul__(self, other):
        if self.size == 1:
            return ooarray(self.item()*other)
        elif isscalar(other):
            # TODO: mb return mere ooarray(self.view(ndarray)*other) or other.view(ndarray)
            # doesn't work with PyPy yet, todo; check later
            return ooarray(self.view(ndarray)*other if self.dtype != object else [self[i]*other for i in range(self.size)])
        elif isinstance(other, oofun):
            hasSize = 'size' in dir(other)
            if not hasSize: 
#                print('''
#                FuncDesigner warning: 
#                to perform the operation 
#                (ooarray multiplication on oofun)
#                oofun size should be known.
#                Assuming oofun size is 1,
#                the value is ascribed to the oofun attributes.
#                Handling of the issue is intended to be 
#                enhanced in future.''')
                other.size = 1
                #raise FuncDesignerException('to perform the operation oofun size should be known')
            if other.size == 1:
                if any([isinstance(elem, oofun) for elem in atleast_1d(self)]):
                #if self.dtype == object:
                    s = atleast_1d(self)
                    return ooarray([s[i]*other for i in range(self.size)])
                else:
                    return ooarray(self*other)
            else: # other.size > 1
                # and self.size != 1
                s = atleast_1d(self)
                return ooarray([s[i]*other[i] for i in range(self.size)])
        elif isinstance(other, ndarray):
            # TODO: mb return mere ooarray(self.view(ndarray)*other)?or other.view(ndarray)
            return ooarray(self*asscalar(other) if other.size == 1 else [self[i]*other[i] for i in range(other.size)])
        elif type(other) in (list, tuple):
            r = self * array(other)
            return r
        else:
            raise FuncDesignerException('bug in multiplication')

    def __div__(self, other):
        if self.size == 1:
            return asscalar(self)/other
        elif isscalar(other) or (isinstance(other, ndarray) and other.size in (1, self.size)):
            return self * (1.0/other)
        elif isinstance(other, oofun):
            if self.dtype != object:
                return self.view(ndarray) / other
            else:
                s = atleast_1d(self)
                return ooarray([s[i] / other for i in range(self.size)])
        elif isinstance(other, ooarray):
            if self.dtype != object:
                return self.view(ndarray) / other.view(ndarray)
            else:
                # TODO: mb return mere ooarray(self.view(ndarray) / other)? or other.view(ndarray)
                s, o = atleast_1d(self), atleast_1d(other)
                return ooarray([s[i] / o[i] for i in range(self.size)])
        else:
            raise FuncDesignerException('unimplemented yet')
            
    __truediv__ = __div__
    __floordiv__ = __div__
    
    def __rdiv__(self, other):
        if self.size == 1:
            return other / asscalar(self)
        return ooarray([1.0 / elem for elem in self.view(ndarray)]) * other
    
    __rtruediv__ = __rdiv__
    
    def __add__(self, other):
        if isinstance(other, list):
            other = ooarray(other)
        if isinstance(other, ndarray) and other.size == 1:
            other = other.item()
        if isscalar(other) or (isinstance(other, ndarray) and other.size in (1, self.size)):
#            if isinstance(other, ndarray) and other.size != self.size:
#                assert other.size == 1 or self.size == 1,  \
#                'ooarrays must be of same size or one of them has be of length 1'
#                N = PythonMax(self.size, other.size)
#                r = ooarray([self[i]+other[i] for i in range(N)])
#            else:
            r = ooarray(self.view(ndarray) + other)
        elif isinstance(other, oofun):
            if self.dtype != object:
                r = self.view(ndarray) + other
            else:
                s = atleast_1d(self)
                r = ooarray([s[i] + other for i in range(self.size)])
        elif isinstance(other, ndarray):
            if self.dtype != object:
                r = self.view(ndarray) + other.view(ndarray)
            elif self.size == 1:
                r = other + asscalar(self) 
            else:
                # TODO: mb return mere ooarray(self.view(ndarray) + other) or ooarray(self.view(ndarray) + other.view(ndarray))?
                r = ooarray([self[i] + other[i] for i in range(self.size)])
        else:
            raise FuncDesignerException('unimplemented yet')
        if isinstance(r, ndarray) and r.size == 1 and r.dtype in (object, oofun, float, np.float64):# not sf.Point,todo: rework
            r = asscalar(r)
        return r

#    # TODO: check why it doesn't work with oofuns
#    def __radd__(self, other):
#        return self + other
#        
#    def __rmul__(self, other):
#        return self * other
    __radd__ = __add__
    __rmul__ = __mul__

    # TODO : fix it
#    def __rdiv__(self, other):
#        return self * other
    
    
    def __pow__(self, other):
        if isinstance(other, ndarray) and other.size > 1 and self.size > 1:
            return ooarray([self[i]**other[i] for i in range(self.size)])
            
        Self = atleast_1d(self.view(ndarray))
        if any(isinstance(elem, (ooarray, oofun)) for elem in Self):
        #if self.dtype == object:
            return ooarray([elem**other for elem in Self])

        # TODO: is this part of code trigger any time?
        return self.view(ndarray)**other
    
    def __rpow__(self, other):
        if isscalar(other) or ('size' in dir(other) and isscalar(other.size) and other.size == 1) or 'size' not in dir(other):
            return ooarray([other ** elem for elem in self.tolist()])
        return ooarray([other[i] ** elem for i, elem in enumerate(self.tolist())])
    
    def __eq__(self, other):
        if type(other) == str and other =='__builtins__': return False  
        r = self - other
        if r.dtype != object: return all(r)
        if r.size == 1: return asscalar(r)==0
        
        # TODO: rework it
        return ooarray([Constraint(elem, lb=0.0, ub=0.0) for elem in r.tolist()])
        #else: raise FuncDesignerException('unimplemented yet')
    
    
    def __lt__(self, other):
        if self.dtype != object and (not isinstance(other, ooarray) or other.dtype != object):
            return self.view(ndarray) < (other.view(ndarray) if isinstance(other, ooarray) else other)
        if isinstance(other, (ndarray, list, tuple)) and self.size > 1 and len(other) > 1:
            return ooarray([self[i] < other[i] for i in range(self.size)])
        if isscalar(other) or (isinstance(other, (ndarray, list, tuple)) and len(other) == 1):
            return ooarray([elem < other for elem in self])
        if isinstance(other, oofun):
            if 'size' in other.__dict__ and not isinstance(other.size, oofun):
                if other.size == self.size:
                    return ooarray([elem[i] < other[i] for i in range(self.size)])
                elif self.size == 1:
                    return ooarray([self[0] < other[i] for i in range(other.size)])
                else:
                    FuncDesignerException('bug or yet unimplemented case in FD kernel')
            else:
                # !!! assunimg other.size = 1
                return ooarray([elem < other for elem in self])
        raise FuncDesignerException('unimplemented yet')
            
    
    def __le__(self, other):
        if self.dtype != object and (not isinstance(other, ooarray) or other.dtype != object):
            return self.view(ndarray) <= (other.view(ndarray) if isinstance(other, ooarray) else other)
        if isinstance(other, (ndarray, list, tuple)) and self.size > 1 and len(other) > 1:
            return ooarray([self[i] <= other[i] for i in range(self.size)])
        if isscalar(other) or (isinstance(other, (ndarray, list, tuple)) and len(other) == 1):
            return ooarray([elem <= other for elem in self])
        if isinstance(other, oofun):
            if 'size' in other.__dict__ and not isinstance(other.size, oofun):
                if other.size == self.size:
                    return ooarray([elem[i] <= other[i] for i in range(self.size)])
                elif self.size == 1:
                    return ooarray([self[0] <= other[i] for i in range(other.size)])
                else:
                    FuncDesignerException('bug or yet unimplemented case in FD kernel')
            else:
                # !!! assunimg other.size = 1
                return ooarray([elem <= other for elem in self])            
        raise FuncDesignerException('unimplemented yet')
        
    
    def __gt__(self, other):
        if self.dtype != object and (not isinstance(other, ooarray) or other.dtype != object):
            return self.view(ndarray) > (other.view(ndarray) if isinstance(other, ooarray) else other)
        if isinstance(other, (ndarray, list, tuple)) and self.size > 1 and len(other) > 1:
            return ooarray([self[i] > other[i] for i in range(self.size)])
        if isscalar(other) or (isinstance(other, (ndarray, list, tuple)) and len(other) == 1):
            return ooarray([elem > other for elem in self])
        if isinstance(other, oofun):
            if 'size' in other.__dict__ and not isinstance(other.size, oofun):
                if other.size == self.size:
                    return ooarray([elem[i] > other[i] for i in range(self.size)])
                elif self.size == 1:
                    return ooarray([self[0] > other[i] for i in range(other.size)])
                else:
                    FuncDesignerException('bug or yet unimplemented case in FD kernel')
            else:
                # !!! assunimg other.size = 1
                return ooarray([elem > other for elem in self])            
        raise FuncDesignerException('unimplemented yet')
        
    
    def __ge__(self, other):
        if self.dtype != object and (not isinstance(other, ooarray) or other.dtype != object):
            return self.view(ndarray) >= (other.view(ndarray) if isinstance(other, ooarray) else other)
        if isinstance(other, (ndarray, list, tuple)) and self.size > 1 and len(other) > 1:
            return ooarray([self[i] >= other[i] for i in range(self.size)])
        if isscalar(other) or (isinstance(other, (ndarray, list, tuple)) and len(other) == 1):
            return ooarray([elem >= other for elem in self])
        if isinstance(other, oofun):
            if 'size' in other.__dict__ and not isinstance(other.size, oofun):
                if other.size == self.size:
                    return ooarray([elem[i] >= other[i] for i in range(self.size)])
                elif self.size == 1:
                    return ooarray([self[0] >= other[i] for i in range(other.size)])
                else:
                    FuncDesignerException('bug or yet unimplemented case in FD kernel')
            else:
                # !!! assunimg other.size = 1
                return ooarray([elem >= other for elem in self])                   
        raise FuncDesignerException('unimplemented yet')

    def sum(self, *args, **kw):
        r = ndarray.sum(self, *args, **kw)
        if type(r) == ooarray and r.size == 1:
            return r.item()
