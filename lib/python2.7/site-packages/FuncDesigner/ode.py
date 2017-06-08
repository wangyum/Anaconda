from translator import FuncDesignerTranslator
from FDmisc import FuncDesignerException, _getDiffVarsID
from numpy import ndarray, hstack, vstack, isscalar, asarray
from ooVar import oovar
from ooFun import atleast_oofun

class ode:
    # Ordinary differential equations
    
    _isInitialized = False
    solver = 'scipy_lsoda'
    
    
    def __init__(self, equations, startPoint, *args, **kwargs):
        if len(args) > 2:  
            raise FuncDesignerException('incorrect ode definition, too many args are obtained')
        
        if not isinstance(equations, dict):
            raise FuncDesignerException('1st argument of ode constructor should be Python dict')

        if not isinstance(startPoint, dict):
            raise FuncDesignerException('2nd argument of ode constructor should be Python dict')
      
        if len(args) == 2:
            print("""
            FuncDesigner warning: you're using obsolete ode() API, 
            now time should be passed as 3rd argument {timeVariable: times}
            or just array of times if equations are time-independend""")
            timeVariable, times = args[0], args[1]
        else:
            if len(args) != 1 or type(args[0]) not in (dict, list, tuple, ndarray):
                raise FuncDesignerException('3rd argument of ode constructor must be dict {timeVariable:array_of_times} or just array_of_times')
            if type(args[0]) == dict:
                if len(args[0]) != 1:
                    raise FuncDesignerException('in time argument dict has to have exactly 1 entry')
                timeVariable, times = list(args[0].items())[0]
                if not isinstance(timeVariable, oovar):
                    raise FuncDesignerException('incorrect time variable, must be FuncDesigner oofun')
            else:
                times = args[0]
                timeVariable = None

        self.timeVariable = timeVariable

        if timeVariable is not None and timeVariable in equations:
            raise FuncDesignerException("ode: differentiation of a variable by itself (time by time) is treated as a potential bug and thus is forbidden")

        if not (isinstance(times, (list, tuple)) or (isinstance(times, ndarray) and times.ndim == 1)): 
            raise FuncDesignerException('incorrect user-defined time argument, must be Python list or numpy array of time values')
        self.times = times
        self._fd_func, self._startPoint, self._timeVariable, self._times, self._kwargs = equations, startPoint, timeVariable, times,  kwargs
        
        startPoint = startPoint.copy()#dict((key, val) for key, val in startPoint.items())
        if timeVariable is not None:
            startPoint[timeVariable] = times[0]
        y0 = []
        Funcs = []
        
        # setting oovar.size is risky - it can affect code written after the ode is solved
        # thus Point4TranslatorAssignment is used instead
        Point4TranslatorAssignment = {}
        
        for v, func in equations.items():
            func = atleast_oofun(func)
#            if not isinstance(func,  oofun):
#                func = fixed_oofun(func)
            if not isinstance(v, oovar):
                raise FuncDesignerException('ode: dict keys must be FuncDesigner oovars, got "%s" instead' % type(v))
            startFVal = asarray(func(startPoint))
            y0.append(asarray(startPoint[v]))
            Funcs.append(func)
            Point4TranslatorAssignment[v] = startFVal
            
            if startFVal.size != asarray(startPoint[v]).size or (hasattr(v, 'size') and isscalar(v.size) and startFVal.size != v.size):
                raise FuncDesignerException('error in user-defined data: oovar "%s" size is not equal to related function value in start point' % v.name)
        
        self.y0 = hstack(y0)
        self.varSizes = [y.size for y in y0]
        ooT = FuncDesignerTranslator(Point4TranslatorAssignment)
        self.ooT = ooT
        def func(y, t): 
            tmp = dict(ooT.vector2point(y))
            if timeVariable is not None:
                tmp[timeVariable] = t
            r = hstack([func(tmp) for func in Funcs])
            return r
        self.func = func
        
        
        _FDVarsID = _getDiffVarsID()
        def derivative(y, t):
#            print('d')
            tmp = dict(ooT.vector2point(y))
            if timeVariable is not None:
                tmp[timeVariable] = t
            r = []
            for func in Funcs:
                tt = func.D(tmp, fixedVarsScheduleID = _FDVarsID)
                if timeVariable is not None:
                    tt.pop(timeVariable, None)
                r.append(ooT.pointDerivative2array(tt))
            return vstack(r)
        self.derivative = derivative
        self.Point4TranslatorAssignment = Point4TranslatorAssignment
        
    def solve(self, solver='scipy_lsoda', *args, **kwargs): # mb for future implementation - add  some **kwargs here as well
        if len(args) > 0:
            raise FuncDesignerException('no args are currently available for the function ode::solve')
        solverName = solver if isinstance(solver, str) else solver.__name__
        
        is_scipy_lsoda = solverName == 'scipy_lsoda'
        is_scipy_solver = solverName in ('vode', 'zvode', 'lsoda', 'dopri5', 'dop853')
        
        if is_scipy_lsoda or is_scipy_solver:
            try:
                from scipy import integrate
            except ImportError:
                raise FuncDesignerException('to solve ode you mush have scipy installed, see http://openop.org/SciPy')
                
        
        is_matlab_solver = solverName.startswith('ode')
        is_interalg = solverName.startswith('interalg')
        
        if not is_scipy_lsoda:
            try:
                from openopt import ODE
            except ImportError:
                raise FuncDesignerException('You should have openopt insalled')
            
            
        if is_interalg:
            prob = ODE(self._fd_func, self._startPoint, self.times, **self._kwargs)
            r = prob.solve(solver, **kwargs)
            y_var = list(prob._x0.keys())[0]
            res = 0.5 * (prob.extras[y_var]['infinums'] + prob.extras[y_var]['supremums'])
            times = hstack((prob.extras['startTimes'], prob.extras['endTimes'][-1]))
            if len(self._times) != 2:
                from scipy.interpolate import InterpolatedUnivariateSpline
#                if 'ftol' in kwargs.keys():
#                    s = self._kwargs['ftol']
#                elif 'fTol' in kwargs.keys():
#                    s = self._kwargs['fTol']
#                elif 'ftol' in self._kwargs.keys():
#                    s = self._kwargs['ftol']
#                elif 'fTol' in self._kwargs.keys():
#                    s = self._kwargs['fTol']
                    
                # walkaround a bug with essential slowdown
                if times[-1] < times[0]:
                    times = times[::-1]
                    res = res[::-1]
                #1
                interp = InterpolatedUnivariateSpline(times, res, k=1)#, s=s**2) 
                
                times = self._times
                res = interp(times)
                
                #2
#                from numpy import searchsorted
#                ind = searchsorted(prob.extras['startTimes'], self._times, 'right')
#                ind[ind==times.size] = times.size-1
#                tmp = res[ind]
##                lti, rti = self._times - prob.extras['startTimes'][ind], prob.extras['endTimes'][ind] - self._times
##                tmp = (lti * res[ind] + rti * res[ind]) / (lti + rti)
##                tmp[logical_and(lti==0, rti==0)] = res[ind]
#                res = tmp
                
            r.xf = {y_var:res}
            r._xf = {y_var.name: res}
            if self.timeVariable is not None:
                r.xf[self._timeVariable] = times
                r._xf[self._timeVariable.name] = times
        else:
            kw = self._kwargs.copy()
            kw.update(kwargs)
            
            if 'rtol' in kw:
                ODE.warn('For OpenOpt ODE you should use reltol instead of rtol')
                kw['reltol'] = kw.pop('rtol')
                
            if 'atol' in kw:
                ODE.warn('For OpenOpt ODE you should use abstol instead of atol')
                kw['abstol'] = kw.pop('atol')
                
            KW = {'rtol': kw.get('reltol', 1.49012e-8), 'atol': kw.get('abstol', 1.49012e-8)}
            if solverName in ('vode', 'zvode', 'lsoda'):
                KW['with_jacobian'] = True
            else:
                assert solverName.startswith('ode') or solverName in ('dopri5', 'dop853', 'scipy_lsoda')
                # ode* are matlab solvers
                    
            if is_scipy_lsoda: 
                y, infodict = integrate.odeint(self.func, self.y0, 
                                               self.times, Dfun = self.derivative, full_output=True, **KW)
            elif is_scipy_solver: 
                F, D = lambda t, y: self.func(y, t), lambda t, y: self.derivative(y, t)
                prob = integrate.ode(F, D).set_integrator(solverName, **KW)
                prob.set_initial_value(self.y0, self.times[0])
                T, Y = [prob.t], [prob.y]
                while self.times[0] <= prob.t < self.times[-1] or self.times[-1] < prob.t <= self.times[0]:
                    prob.integrate(self.times[-1], step=True)
                    T.append(prob.t)
                    Y.append(prob.y)
                if len(self.times) > 2:
                    from scipy import interpolate
                    Y = asarray(Y).T
                    y = asarray([interpolate.interp1d(T, _y)(self.times) for _y in Y]).T
                else:
                    y = asarray(Y)
                
            elif solverName.startswith('ode'): #MATLAB solver
                prob = ODE(self.func, self.y0, self.times, d = self.derivative)
                prob._Prepare()
                prob.f, prob.df = self.func, self.derivative
                r = prob.solve(solver, **kw)
                y = prob._xf 
            else:
                raise  FuncDesignerException('incorrect ODE solver')
                
            resultDict = dict(self.ooT.vector2point(y.T))
            
            for key, value in resultDict.items():
                if min(value.shape) == 1:
                    resultDict[key] = value.flatten()
            r = FuncDesigner_ODE_Result(resultDict)
                
            r.msg = infodict['message'] if is_scipy_lsoda else ''
            r.extras = {'infodict': infodict} if is_scipy_lsoda else {}
        return r
        

class FuncDesigner_ODE_Result:
    # TODO: prevent code clone with runprobsolver.py
    def __init__(self, resultDict):
        self.xf = resultDict
        if not hasattr(self, '_xf'):
            self._xf = dict((var.name, value) for var, value in resultDict.items())
    def __call__(self, *args):
        r = [(self._xf[arg] if isinstance(arg,  str) else self.xf[arg]) for arg in args]
        return r[0] if len(args)==1 else r
