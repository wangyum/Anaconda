from ooFun import oofun
import numpy as np
from numpy import all
from FDmisc import FuncDesignerException, Diag
from boundsurf import boundsurf
from Interval import defaultIntervalEngine

try:
    from scipy import interpolate
    scipyInstalled = True
except:
    scipyInstalled = False

def scipy_InterpolatedUnivariateSpline(*args, **kwargs):
    if not scipyInstalled:
        raise FuncDesignerException('to use scipy_InterpolatedUnivariateSpline you should have scipy installed, see scipy.org')
    assert len(args)>1 
    assert not isinstance(args[0], oofun) and not isinstance(args[1], oofun), \
    'init scipy splines from oovar/oofun content is not implemented yet'
    S = interpolate.InterpolatedUnivariateSpline(*args, **kwargs)
    
    return SplineGenerator(S, *args, **kwargs)
    
        # TODO: check does isCostly = True better than False for small-scale, medium-scale, large-scale
#    return SplineGenerator

class SplineGenerator:
    def __call__(self, INP):
        us = self._un_sp
        if not isinstance(INP, oofun):
            raise FuncDesignerException('for scipy_InterpolatedUnivariateSpline input should be oovar/oofun,other cases not implemented yet')
        
        def d(x): 
            X = np.asanyarray(x)
            r = Diag(us.__call__(X, 1).view(X.__class__))
            return r

        def f(x):
            x = np.asanyarray(x)
            tmp = us.__call__(x.flatten() if x.ndim > 1 else x)
            return tmp if x.ndim <= 1 else tmp.reshape(x.shape)
        r = oofun(f, INP, d = d, isCostly = True, vectorized=True)

        r.engine_monotonity = self.engine_monotonity
        r.engine_convexity = self.engine_convexity
        
        if self.criticalPoints is not False:
            r._interval_ = lambda *args, **kw: spline_interval_analysis_engine(r, *args, **kw)
            r._nonmonotone_x = self._nonmonotone_x
            r._nonmonotone_y = self._nonmonotone_y
        else:
            r.criticalPoints = False
            
        def Plot():
            print('Warning! Plotting spline is recommended from FD spline generator, not initialized spline')
            self.plot()
        def Residual():
            print('Warning! Getting spline residual is recommended from FD spline generator, not initialized spline')
            return self.residual()
            
        r.plot, r.residual = Plot, Residual
        return r
        
    def __init__(self, us, *args, **kwargs):
        self._un_sp = us
        _X, _Y = np.asfarray(args[0]), np.asfarray(args[1])
        ind = np.argsort(_X)
        _X, _Y = _X[ind], _Y[ind]
        self._X, self._Y = _X, _Y
        
        if len(args) >= 5:
            k = args[4]
        elif 'k' in kwargs:
            k = kwargs['k']
        else:
            k = 3 # default for InterpolatedUnivariateSpline
            
        self._k = k
        
        # TODO: handle 1500 as standalone FD.interpolate() parameter
        if k != 1:
            xx = np.hstack((np.linspace(_X[0], _X[-1], 1500), _X[1:-1]))
        else:
           xx =  np.copy(_X)
        xx.sort()
        yy = self._un_sp.__call__(xx)
        self._xx, self._yy = xx, yy
        
        diff_yy = np.diff(yy)
        diffY = np.diff(_Y)
        monotone_increasing_y = all(diffY >= 0) and all(diff_yy >= 0)
        monotone_decreasing_y = all(diffY <= 0) and all(diff_yy <= 0)
    
        self.engine_monotonity = np.nan
        self.engine_convexity = np.nan
        
        d2y = np.diff(diffY)
        if all(d2y >= 0):
            self.engine_convexity = 1
        elif all(d2y <= 0):
            self.engine_convexity = -1
        
        self.criticalPoints = None
        if k not in (1, 2, 3):
            def _interval(*args, **kw):
                raise FuncDesignerException('''
                Currently interval calculations are implemented for 
                sorted monotone splines with order 1 or 3 only''')
            self._interval = _interval
        elif monotone_increasing_y or monotone_decreasing_y:
            self.criticalPoints = False
            if monotone_increasing_y:
                self.engine_monotonity = 1
            elif monotone_decreasing_y:
                self.engine_monotonity = -1
        else:
            ind_nonmonotone = np.where(diff_yy[1:] * diff_yy[:-1] < 0)[0] + 1
            self._nonmonotone_x = xx[ind_nonmonotone]
            self._nonmonotone_y = yy[ind_nonmonotone]
            
    def plot(self):
        try:
            import pylab
        except:
            print('You should have matplotlib installed')
            return
        pylab.scatter(self._X, self._Y, marker='o')
        pylab.plot(self._xx, self._yy)
        
        pylab.grid('on')
        pylab.title('FuncDesigner spline checker')
        pylab.show()
    
    def residual(self):
        YY = self._un_sp.__call__(self._X)
        return np.max(np.abs(YY - self._Y))

def spline_interval_analysis_engine(S, domain, dtype):
    lb_ub, definiteRange = S.input[0]._interval(domain, dtype, ia_surf_level = 1 if not np.isnan(S.engine_convexity) else 0)
    if type(lb_ub) == boundsurf:
        assert S._nonmonotone_x.size == 1, 'bug in FD kernel'
        return defaultIntervalEngine(lb_ub, S.fun, S.d, S.engine_monotonity, S.engine_convexity, \
                          criticalPoint = S._nonmonotone_x, criticalPointValue = S._nonmonotone_y)
    lb, ub = lb_ub[0], lb_ub[1]
    
    x, y = S._nonmonotone_x, S._nonmonotone_y
    tmp = S.fun(lb_ub)
    tmp.sort(axis=0)
    _inf, _sup = tmp[0], tmp[1]
    for i, xx in enumerate(x):
        yy = y[i]
        ind = np.where(np.logical_and(lb < xx, xx < ub))[0]
        _inf[ind] = np.where(_inf[ind] < yy, _inf[ind], yy)
        _sup[ind] = np.where(_sup[ind] > yy, _sup[ind], yy)
    r = np.vstack((_inf, _sup))

    # TODO: modify definiteRange for out-of-bounds splines
    # definiteRange = False
        
    return r, definiteRange
