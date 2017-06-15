PythonMax = max
from numpy import all, any, isfinite, inf, nan, ndarray, ones, \
ravel, asfarray, prod, asarray, atleast_1d, isinf
import numpy as np
from oologfcn import *
from oographics import Graphics
from setDefaultIterFuncs import setDefaultIterFuncs, denyingStopFuncs
from nonLinFuncs import nonLinFuncs
from residuals import residuals
from ooIter import ooIter

#from Point import Point currently lead to bug
from openopt.kernel.Point import Point

from iterPrint import ooTextOutput
from ooMisc import setNonLinFuncsNumber, assignScript, norm
from nonOptMisc import isspmatrix, scipyInstalled, scipyAbsentMsg, csr_matrix
from copy import copy as Copy
try:
    from DerApproximator import check_d1
    DerApproximatorIsInstalled = True
except:
    DerApproximatorIsInstalled = False

ProbDefaults = {'diffInt': 1.5e-8,  'xtol': 1e-6,  'noise': 0}
from runProbSolver import runProbSolver
import GUI

from fdPrepare import fdPrepare


class user:
    def __init__(self):
        pass

class oomatrix:
    def __init__(self):
        pass
    def matMultVec(self, x, y):
        return np.dot(x, y) if not isspmatrix(x) else x._mul_sparse_matrix(csr_matrix(y.reshape((y.size, 1)))).A.flatten() 
    def matmult(self, x, y):
        return np.dot(x, y)
        #return asarray(x) ** asarray(y)
    def dotmult(self, x, y):
        return x * y
        #return asarray(x) * asarray(y)

class autocreate:
    def __init__(self): pass

class baseProblem(oomatrix, residuals, ooTextOutput):
    isObjFunValueASingleNumber = True
    manage = GUI.manage # GUI func
    #_useGUIManager = False # TODO: implement it
    prepared = False
    _baseProblemIsPrepared = False
    isManagerUsed = False
    managerTextOutput = True
    
    name = 'unnamed'
    state = 'init'# other: paused, running etc
    castFrom = '' # used by converters qp2nlp etc
    nonStopMsg = ''
    xlabel = 'time'
    plot = False # draw picture or not
    show = True # use command pylab.show() after solver finish or not
    _immutable  = False
    

    iter = 0
    cpuTimeElapsed = 0.
    TimeElapsed = 0.
    isFinished = False
    invertObjFunc = False # True for goal = 'max' or 'maximum'
    nProc = 1 # number of processors to use

    lastPrintedIter = -1
    
    iterObjFunTextFormat = '%0.3e'
    finalObjFunTextFormat = '%0.8g'
    debug = 0
    
    iprint = 10
    #if iprint<0 -- no output
    #if iprint==0 -- final output only

    maxDistributionSize = 0 # used in stochastic problems

    maxIter = 1000
    maxFunEvals = 10000 # TODO: move it to NinLinProblem class?
    maxCPUTime = inf
    maxTime = inf
    maxLineSearch = 500 # TODO: move it to NinLinProblem class?
    xtol = ProbDefaults['xtol'] # TODO: move it to NinLinProblem class?
    gtol = 1e-6 # TODO: move it to NinLinProblem class?
    ftol = 1e-6
    contol = 1e-6
    discrtol = 1e-5 # tolerance required for discrete constraints 
    fTol = None
    rTol = 1e-8#used in interalg
    f_bound_distance = nan
    f_bound_estimation = nan

    minIter = 0
    minFunEvals = 0
    minCPUTime = 0.0
    minTime = 0.0
    
    storeIterPoints = False 

    userStop = False # becomes True is stopped by user
    
    useSparse = 'auto' # involve sparse matrices: 'auto' (autoselect, premature) | True | False
    useAttachedConstraints = False

    x0 = None
    isFDmodel = False # OO kernel set it to True if oovars/oofuns are used

    noise = ProbDefaults['noise'] # TODO: move it to NinLinProblem class?

    showFeas = False
    useScaledResidualOutput = False

    hasLogicalConstraints = False
    
    _isStochastic = False
    
    # A * x <= b inequalities
    A = None
    b = None

    # Aeq * x = b equalities
    Aeq = None
    beq = None
    
    #non-linear constraints
    c = None # c(x)<=0
    h = None # h(x)=0

    
    scale = None

    goal = None# should be redefined by child class
    # possible values: 'maximum', 'min', 'max', 'minimum', 'minimax' etc
    showGoal = False# can be redefined by child class, used for text & graphic output

    color = 'b' # blue, color for plotting
    specifier = '-'# simple line for plotting
    plotOnlyCurrentMinimum = False # some classes like GLP change the default to True
    xlim = (nan,  nan)
    ylim = (nan,  nan)
    legend = ''

    fixedVars = None
    freeVars = None
    
    istop = 0
    
    maxSolutions = 1 # used in interalg and mb other solvers

    fEnough = -inf # if value less than fEnough will be obtained
    # and all constraints no greater than contol
    # then solver will be stopped.
    # this param is handled in iterfcn of OpenOpt kernel
    # so it may be ignored with some solvers not closely connected to OO kernel

    fOpt = None # optimal value, if known
    implicitBounds = inf
    
    convex = 'unknown' # used in interalg
    _linear_objective = False # used in interalg
    _textFuncsInitialized = False


    def __init__(self, *args, **kwargs):
        # TODO: add the field to ALL classes
        self._setTextFuncs()
        self.data4TextOutput = ['objFunVal', 'log10(maxResidual)']
        self.nEvals = {}
        self._init_kwargs = {}
        self.finish = []# functions f_i(r,p) to be evaluated after finish
        self._bg_color = '#FFFFF0'
        
        if hasattr(self, 'expectedArgs'): 
            if len(self.expectedArgs)<len(args):
                self.err('Too much arguments for '+self.probType +': '+ str(len(args)) +' are got, at most '+ str(len(self.expectedArgs)) + ' were expected')
            for i, arg in enumerate(args):
                setattr(self, self.expectedArgs[i], arg)
        self.norm = norm
        self.denyingStopFuncs = denyingStopFuncs()
        self.iterfcn = lambda *args, **kwargs: ooIter(self, *args, **kwargs)# this parameter is only for OpenOpt developers, not common users
        self.graphics = Graphics()
        self.user = user()
        self.F = lambda x: self.objFuncMultiple2Single(self.objFunc(x)) # TODO: should be changes for LP, MILP, QP classes!

        self.point = lambda *args,  **kwargs: Point(self, *args,  **kwargs)

        self.timeElapsedForPlotting = [0.]
        self.cpuTimeElapsedForPlotting = [0.]
        #user can redirect these ones, as well as debugmsg
        self.debugmsg = lambda msg: oodebugmsg(self,  msg)
        
        self.constraints = [] # used in isFDmodel

        self.callback = [] # user-defined callback function(s)
        
        self.solverParams = autocreate()

        self.userProvided = autocreate()

        self.special = autocreate()

        self.intVars = [] # for problems like MILP
        self.binVars = [] # for problems like MILP
        self.optionalData = []#string names of optional data like 'c', 'h', 'Aeq' etc
        
        if self.allowedGoals is not None: # None in EIG
            if 'min' in self.allowedGoals:
                self.minimize = lambda *args, **kwargs: minimize(self, *args, **kwargs)
            if 'max' in self.allowedGoals:
                self.maximize = lambda *args, **kwargs: maximize(self, *args, **kwargs)
                
        assignScript(self, kwargs)
    
 
    def __setattr__(self, attr, val): 
#        print attr
        if self._immutable and attr != '_immutable': 
            self.err('''
            The OpenOpt problem instance is immutable here, 
            arguments should pass to constructor or solve()'''
            )
        self.__dict__[attr] = val
    
    def _setTextFuncs(self):   
        if self._textFuncsInitialized: 
            return
        self.err =  ooerr
        self.warn = oowarn
        self.info = ooinfo
        self.hint = oohint
        self.pWarn = ooPWarn
        self.disp = oodisp
        self._textFuncsInitialized = True

    def __finalize__(self):
        if self.isFDmodel:
            self.xf = self._vector2point(self.xf)
            self.constraints = self._initial_constraints

    def objFunc(self, x):
        return self.f(x) # is overdetermined in LP, QP, LLSP etc classes

    def __isFiniteBoxBounded__(self): # TODO: make this function 'lazy'
        return all(isfinite(self.ub)) and all(isfinite(self.lb))

    def __isNoMoreThanBoxBounded__(self): # TODO: make this function 'lazy'
        return self.b.size ==0 and self.beq.size==0 and (self._baseClassName == 'Matrix' or (not self.userProvided.c and not self.userProvided.h))

#    def __1stBetterThan2nd__(self,  f1, f2,  r1=None,  r2=None):
#        if self.isUC:
#            #TODO: check for goal = max/maximum
#            return f1 < f2
#        else:#then r1, r2 should be defined
#            return (r1 < r2 and  self.contol < r2) or (((r1 <= self.contol and r2 <=  self.contol) or r1==r2) and f1 < f2)
#
#    def __1stCertainlyBetterThan2ndTakingIntoAcoountNoise__(self,   f1, f2,  r1=None,  r2=None):
#        if self.isUC:
#            #TODO: check for goalType = max
#            return f1 + self.noise < f2 - self.noise
#        else:
#            #return (r1 + self.noise < r2 - self.noise and  self.contol < r2) or \
#            return (r1 < r2  and  self.contol < r2) or \
#            (((r1 <= self.contol and r2 <=  self.contol) or r1==r2) and f1 + self.noise < f2 - self.noise)


    def solve(self, *args, **kwargs):
        return runProbSolver(self, *args, **kwargs)
        
    def _solve(self, *args, **kwargs):
        self.debug = True
        return self.solve(*args, **kwargs)
    
    def objFuncMultiple2Single(self, f):
        #this function can be overdetermined by child class
        if asfarray(f).size != 1: self.err('unexpected f size. The function should be redefined in OO child class, inform OO developers')
        return f

    def fill(self, newProb, sameConstraints=True):
        # fills some fields of new prob with old prob values
        newProb.castFrom = self.probType

        #TODO: hold it in single place

        fieldsToAssert = ['contol', 'xtol', 'ftol', 'gtol', 'iprint', 'maxIter', 'maxTime', 'maxCPUTime','fEnough', 'goal', 'color', 'debug', 'maxFunEvals', 'xlabel']
        # TODO: boolVars, intVars
        if sameConstraints: fieldsToAssert+= ['lb', 'ub', 'A', 'Aeq', 'b', 'beq']

        for key in fieldsToAssert:
            if hasattr(self, key): setattr(newProb, key, getattr(self, key))


        # note: because of 'userProvided' from prev line
        #self self.userProvided is same to newProb.userProvided
        
#        for key in ['f','df', 'd2f']:
#                if hasattr(self.userProvided, key) and getattr(self.userProvided, key):
#                    setattr(newProb, key, getattr(self.user, key))
        
        Arr = ['f', 'df']
        if sameConstraints:
            Arr += ['c','dc','h','dh','d2c','d2h']
        
        for key in Arr:
            if hasattr(self.userProvided, key):
                if getattr(self.userProvided, key):
                    #setattr(newProb, key, getattr(self.user, key))
                    setattr(newProb, key, getattr(self, key)) if self.isFDmodel else setattr(newProb, key, getattr(self.user, key))
                else:
                    setattr(newProb, key, None)
                        
    FuncDesignerSign = 'f'

    def _isFDmodel(self):
        try:
            #from FuncDesigner.ooFun import oofun
            from FuncDesigner import ooarray, oofun
        except ImportError:
            return False
        fds = getattr(self, self.FuncDesignerSign, None)
        if fds is None:
            return False        
        if isinstance(fds, (oofun, ooarray)):
            return True
        if isinstance(fds, dict):
            return True if isinstance(list(fds.keys())[0], (oofun, ooarray)) else False
        if isinstance(fds, (list, tuple, ndarray)):
            if isinstance(fds[0], (oofun, ooarray)):
                return True
            elif isinstance(fds[0], (list, tuple, ndarray)):
                return isinstance(fds[0][0], (oofun, ooarray))
        return False
    
    # Base class method
    def _prepare(self): 
        if self._baseProblemIsPrepared: return
        if self.useSparse == 0:
            self.useSparse = False
        elif self.useSparse == 1:
            self.useSparse = True
        if self.useSparse == 'auto' and not scipyInstalled:
            self.useSparse = False
        if self.useSparse == True and not scipyInstalled:
            self.err("You can't set useSparse=True without scipy installed")
        if self._isFDmodel():
            fdPrepare(self)
        else: # not FuncDesigner
            if self.fixedVars is not None or self.freeVars is not None:
                self.err('fixedVars and freeVars are valid for optimization of FuncDesigner models only')
        if self.x0 is None: 
            arr = ['lb', 'ub']
            if self.probType in ['LP', 'MILP', 'QP', 'SOCP', 'SDP']: arr.append('f')
            if self.probType in ['LLSP', 'LLAVP', 'LUNP']: arr.append('D')
            for fn in arr:
                if not hasattr(self, fn): continue
                tmp = getattr(self, fn)
                fv = asarray(tmp) if not isspmatrix(tmp) else tmp.A
                if any(isfinite(fv)):
                    self.x0 = np.zeros(fv.size)
                    break
        self.x0 = ravel(self.x0)
        
        if not hasattr(self, 'n'): self.n = self.x0.size
        if not hasattr(self, 'lb'): self.lb = -inf * ones(self.n)
        if not hasattr(self, 'ub'): self.ub =  inf * ones(self.n)        
        self._lb, self._ub = np.copy(self.lb), np.copy(self.ub)

        for fn in ('A', 'Aeq'):
            fv = getattr(self, fn)
            if fv is not None:
                #afv = asfarray(fv) if not isspmatrix(fv) else fv.toarray() # TODO: omit casting to dense matrix
                afv = asfarray(fv)  if type(fv) in [list, tuple] else fv
                if len(afv.shape) > 1:
                    if afv.shape[1] != self.n:
                        self.err('incorrect ' + fn + ' size')
                else:
                    if afv.shape != () and afv.shape[0] == self.n: afv = afv.reshape(1, self.n)
                setattr(self, fn, afv)
            else:
                setattr(self, fn, asfarray([]).reshape(0, self.n))
                
        nA, nAeq = prod(self.A.shape), prod(self.Aeq.shape) 
        SizeThreshold = 2 ** 15
        if scipyInstalled:
            from scipy.sparse import csc_matrix
            if isspmatrix(self.A) or (nA > SizeThreshold  and np.flatnonzero(self.A).size < 0.25*nA):
                self._A = csc_matrix(self.A)
            if isspmatrix(self.Aeq) or (nAeq > SizeThreshold and np.flatnonzero(self.Aeq).size < 0.25*nAeq):
                self._Aeq = csc_matrix(self.Aeq)
            
        elif nA > SizeThreshold or nAeq > SizeThreshold:
            self.pWarn(scipyAbsentMsg)
            
        self._baseProblemIsPrepared = True


class MatrixProblem(baseProblem):
    _baseClassName = 'Matrix'
    ftol = 1e-8
    contol = 1e-8
    #obsolete, should be removed
    # still it is used by lpSolve
    # Awhole * x {<= | = | >= } b
    Awhole = None # matrix m x n, n = len(x)
    bwhole = None # vector, size = m x 1
    dwhole = None #vector of descriptors, size = m x 1
    # descriptors dwhole[j] should be :
    # 1 : <Awhole, x> [j] greater (or equal) than bwhole[j]
    # -1 : <Awhole, x> [j] less (or equal) than bwhole[j]
    # 0 : <Awhole, x> [j] = bwhole[j]
    def __init__(self, *args, **kwargs):
        baseProblem.__init__(self, *args, **kwargs)
        self.kernelIterFuncs = setDefaultIterFuncs('Matrix')
        self.userProvided.c = False
        self.userProvided.h = False

    def _Prepare(self):
        if self.prepared == True:
            return
        baseProblem._prepare(self)
        self.prepared = True

    # TODO: move the function to child classes
    def _isUnconstrained(self):
        if  self.b.size !=0 or self.beq.size != 0: 
            return False
        
        # for PyPy compatibility
        if any(atleast_1d(self.lb) != -inf) or any(atleast_1d(self.ub) != inf):
            return False
            
        return True


class Parallel:
    def __init__(self):
        self.f = False# 0 - don't use parallel calclations, 1 - use
        self.c = False
        self.h = False
        #TODO: add paralell func!
        #self.parallel.fun = dfeval

class Args:
    def __init__(self): pass
    f, c, h = (), (), ()

class NonLinProblem(baseProblem, nonLinFuncs, Args):
    _baseClassName = 'NonLin'
    diffInt = ProbDefaults['diffInt']        #finite-difference gradient aproximation step
    #lines with |info_user-info_numerical| / (|info_user|+|info_numerical+1e-15) greater than maxViolation will be shown
    maxViolation = 1e-2
    JacobianApproximationStencil = 1
    def __init__(self, *args, **kwargs):
        baseProblem.__init__(self, *args, **kwargs)
        if not hasattr(self, 'args'): self.args = Args()
        self.prevVal = {}
        for fn in ['f', 'c', 'h', 'df', 'dc', 'dh', 'd2f', 'd2c', 'd2h']:
            self.prevVal[fn] = {'key':None, 'val':None}

        self.functype = {}

        #self.isVectoriezed = False

#        self.fPattern = None
#        self.cPattern = None
#        self.hPattern = None
        self.kernelIterFuncs = setDefaultIterFuncs('NonLin')

    def checkdf(self, *args,  **kwargs):
        return self.checkGradient('df', *args,  **kwargs)

    def checkdc(self, *args,  **kwargs):
        return self.checkGradient('dc', *args,  **kwargs)

    def checkdh(self, *args,  **kwargs):
        return self.checkGradient('dh', *args,  **kwargs)
    
    def checkGradient(self, funcType, *args,  **kwargs):
        self._Prepare()
        if not DerApproximatorIsInstalled:
            self.err('To perform gradients check you should have DerApproximator installed, see http://openopt.org/DerApproximator')
        
        if not getattr(self.userProvided, funcType):
            self.warn("you haven't analitical gradient provided for " + funcType[1:] + ', turning derivatives check for it off...')
            return
        if len(args)>0:
            if len(args)>1 or 'x' in kwargs:
                self.err('checkd<func> funcs can have single argument x only (then x should be absent in kwargs )')
            xCheck = asfarray(args[0])
        elif 'x' in kwargs:
            xCheck = asfarray(kwargs['x'])
        else:
            xCheck = asfarray(self.x0)
        
        maxViolation = 0.01
        if 'maxViolation' in kwargs:
            maxViolation = kwargs['maxViolation']
            
        self.disp(funcType + (': checking user-supplied gradient of shape (%d, %d)' % (getattr(self, funcType[1:])(xCheck).size, xCheck.size)))
        self.disp('according to:')
        self.disp('    diffInt = ' + str(self.diffInt)) # TODO: ADD other parameters: allowed epsilon, maxDiffLines etc
        self.disp('    |1 - info_user/info_numerical| < maxViolation = '+ str(maxViolation))        
        
        check_d1(getattr(self, funcType[1:]), getattr(self, funcType), xCheck, **kwargs)
        
        # reset counters that were modified during check derivatives
        self.nEvals[funcType[1:]] = 0
        self.nEvals[funcType] = 0
        
    def _makeCorrectArgs(self):
        argslist = dir(self.args)
        if not ('f' in argslist and 'c' in argslist and 'h' in argslist):
            tmp, self.args = self.args, autocreate()
            self.args.f = self.args.c = self.args.h = tmp
        for j in ('f', 'c', 'h'):
            v = getattr(self.args, j)
            if type(v) != type(()): setattr(self.args, j, (v,))

#    def __finalize__(self):
#        BaseProblem.__finalize__(self)
##        if self.isFDmodel:
##            self.xf = self._vector2point(self.xf)

    def _Prepare(self):
        baseProblem._prepare(self)
        if asarray(self.implicitBounds).size == 1:
            self.implicitBounds = [-self.implicitBounds, self.implicitBounds]
            self.implicitBounds.sort()# for more safety, maybe user-provided value is negative
        if hasattr(self, 'solver'):
            if not self.solver.iterfcnConnected:
                if self.solver.funcForIterFcnConnection == 'f':
                    if not hasattr(self, 'f_iter'):
                        self.f_iter = PythonMax(self.n, 4)
                else:
                    if not hasattr(self, 'df_iter'):
                        self.df_iter = True
        
        if self.prepared == True:
            return
        
        # TODO: simplify it
        self._makeCorrectArgs()
        for s in ('f', 'df', 'd2f', 'c', 'dc', 'd2c', 'h', 'dh', 'd2h'):
            derivativeOrder = len(s)-1
            self.nEvals[Copy(s)] = 0
            Attr = getattr(self, s, None)
            if Attr is not None and (not isinstance(Attr, (list, tuple)) or len(Attr) != 0) :
                setattr(self.userProvided, s, True)

                A = getattr(self,s)

                if type(A) not in [list, tuple]: #TODO: add or ndarray(A)
                    A = (A,)#make tuple
                setattr(self.user, s, A)
            else:
                setattr(self.userProvided, s, False)
            if derivativeOrder == 0:
                setattr(self, s, lambda x, IND=None, userFunctionType= s, ignorePrev=False, getDerivative=False: \
                        self.wrapped_func(x, IND, userFunctionType, ignorePrev, getDerivative))
                
#                setattr(self, s, lambda x, IND=None, userFunctionType= s, ignorePrev=False, getDerivative=False, \
#                        _linePointDescriptor = None: \
#                        self.wrapped_func(x, IND, userFunctionType, ignorePrev, getDerivative, _linePointDescriptor))
            elif derivativeOrder == 1:
                setattr(self, s, lambda x, ind=None, funcType=s[-1], ignorePrev = False, useSparse=self.useSparse:
                        self.wrapped_1st_derivatives(x, ind, funcType, ignorePrev, useSparse))
            elif derivativeOrder == 2:
                setattr(self, s, getattr(self, 'user_'+s))
            else:
                self.err('incorrect non-linear function case')

        self.diffInt = ravel(self.diffInt)
        
        # TODO: mb get rid of the field
        self.vectorDiffInt = self.diffInt.size > 1
        
        if self.scale is not None:
            self.scale = ravel(self.scale)
            if self.vectorDiffInt or self.diffInt[0] != ProbDefaults['diffInt']:
                self.info('using both non-default scale & diffInt is not recommended. diffInt = diffInt/scale will be used')
            self.diffInt = self.diffInt / self.scale
       

        #initialization, getting nf, nc, nh etc:
        for s in ['c', 'h', 'f']:
            if not getattr(self.userProvided, s):
                setattr(self, 'n'+s, 0)
            else:
                setNonLinFuncsNumber(self,  s)
                
        self.prepared = True

    # TODO: move the function to derived classes
    _isUnconstrained = lambda self:\
        self.b.size ==0 and self.beq.size==0 and not self.userProvided.c and not self.userProvided.h \
        and (len(self.lb)==0 or all(isinf(self.lb))) and (len(self.ub)==0 or all(isinf(self.ub)))
    

def minimize(p, *args, **kwargs):
    if 'goal' in kwargs:
        if kwargs['goal'] in ['min', 'minimum']:
            p.warn("you shouldn't pass 'goal' to the function 'minimize'")
        else:
            p.err('ambiguous goal has been requested: function "minimize", goal: %s' %  kwargs['goal'])
    p.goal = 'minimum'
    return runProbSolver(p, *args, **kwargs)

def maximize(p, *args, **kwargs):
    if 'goal' in kwargs:
        if kwargs['goal'] in ['max', 'maximum']:
            p.warn("you shouldn't pass 'goal' to the function 'maximize'")
        else:
            p.err('ambiguous goal has been requested: function "maximize", goal: %s' %  kwargs['goal'])
    p.goal = 'maximum'
    return runProbSolver(p, *args, **kwargs)            
