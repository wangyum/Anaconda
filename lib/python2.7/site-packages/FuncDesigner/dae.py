from ooSystem import ooSystem as oosystem
from FDmisc import FuncDesignerException
from numpy import ndarray

class dae:
    def __init__(self, equations, time, startPoint = None):#, **kw):
        self.equations = equations
        self.startPoint = startPoint
        self.time = time
        s = 'for DAE time must be dict of len 1 or array, '
        if type(time) == dict:
            if len(time) != 1:
                raise FuncDesignerException(s + 'got dict of len ' + str(len(time)))
            self.timeInterval = asarray(next(iter(time.values())))
            self.N = self.timeInterval.size
        else:
            if type(time) not in (list, tuple, ndarray):
                raise FuncDesignerException(s + 'got type %s insead ' + str(type(time)))
            self.N = len(time)
            self.timeInterval = time
        if self.N < 2:
            raise FuncDesignerException('lenght of time must be at least 2')
        
        # !!!!!!!!!!
        # TODO: freeVars, fixedVars
        # !!!!!!!!!!
        
#        for fn in ['freeVars', 'fixedVars']:
#            if fn in kw

    def solve(self, solver = None, **kw):
        S = oosystem()
        S &= self.equations
        
        if self.startPoint is not None:
            startPoint = self.startPoint
        else:
            Dep = set()
            Dep.update(*[eq._getDep() for eq in self.equations])
            if None in Dep:
                Dep.remove(None)
            startPoint = {}
            for v in Dep:
                if 'size' in v.__dict__:
                    startPoint[v] = v.size
                else:
                    startPoint[v] = [0]*self.N
                   
                    
            #startPoint = dict([(v, [0]*v.size) for v in Dep])    
        kw2 = kw.copy()
        if solver is not None:
            kw2['solver'] = solver
        r = S.solve(startPoint, **kw2)#, iprint=1)
        r.plot = self.plot
        self.r = r
        return r
    
    def plot(self, v, grid='on'):
        try:
            from pylab import plot, grid as Grid, show, legend
        except ImportError:
            raise FuncDesignerException('to plot DAE results you should have matplotlib installed')
            
        f, = plot(self.timeInterval, self.r(v))
        legend([f], [v.name])
        Grid(grid)
        show()
