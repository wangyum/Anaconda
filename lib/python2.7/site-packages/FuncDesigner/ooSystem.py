from FDmisc import FuncDesignerException, pWarn, _getAllAttachedConstraints
from ooFun import oofun
from constraints import BaseFDConstraint
from ooarray import ooarray
from ooPoint import ooPoint
from numpy import isnan, ndarray, isfinite, asscalar, all, asarray, atleast_1d, array_equal
from sle import sle

class ooSystem:
    def __init__(self, *args,  **kwargs):
        assert len(kwargs) == 0, 'ooSystem constructor has no implemented kwargs yet'
        self.items = set()
        self.constraints = set()
        self.nlpSolvers = ['ralg']
        self.lpSolvers = ['glpk', 'lpSolve', 'cvxopt_lp', 'cplex','pclp','nlp:ipopt', 'nlp:algencan', 'nlp:scipy_slsqp', 'nlp:ralg']
        for arg in args:
            if isinstance(arg, set):
               self.items.update(arg)
            elif isinstance(arg, list) or isinstance(arg, tuple):
                self.items.update(set(arg))
            elif isinstance(arg, oofun):
                self.items.add(arg)
            else:
                raise FuncDesignerException('Incorrect type %s in ooSystem constructor' % type(arg))
        self._changed = True
        
    
    # [] yields result wrt allowed contol:
    #__getitem__ = lambda self, point: ooSystemState([(elem, elem[point]) for elem in self])
    def __getitem__(self, item):
        raise FuncDesignerException('ooSystem __getitem__ is reserved for future purposes')
    
    def __iadd__(self, *args, **kwargs):
        assert len(kwargs) == 0, 'not implemented yet'
        self._changed = True
        if type(args[0]) in [list, tuple, set]:
            assert len(args) == 1
            Args = args[0]
        else:
            Args = args
        for elem in Args:
            if not isinstance(elem, oofun): raise FuncDesignerException('ooSystem operation += expects only oofuns')
        self.items.update(set(Args))
        return self
        
    def __iand__(self, *args, **kwargs):
        assert len(kwargs) == 0, 'not implemented yet'
        self._changed = True
        if type(args[0]) in [list, tuple, set]:
            assert len(args) == 1
            Args = args[0]
        else:
            Args = args
        for elem in Args:
            if isinstance(elem, (ooarray, list, tuple)):
                for tmp_elem in elem: self.__iand__(tmp_elem) 
            else:
                if not isinstance(elem, BaseFDConstraint): raise FuncDesignerException('ooSystem operation &= expects only FuncDesigner constraints')
                #self.constraints.update(set(Args))
                self.constraints.add(elem)
        return self
    
        
    # TODO: provide a possibility to yield exact result (ignoring contol)    
    def __call__(self, point):
        if not isinstance(point,  dict): raise FuncDesignerException('argument should be Python dictionary')
        if not isinstance(point, ooPoint):
            point = ooPoint(point)
        r = ooSystemState([(elem, simplify(elem(point))) for elem in self.items])

        # handling constraints
        #!!!!!!!!!!!!!!!!!!! TODO: perform attached constraints lookup only once if ooSystem wasn't modified by += or &= etc
        
        cons = self._getAllConstraints()
        
        
        activeConstraints = []
        allAreFinite = all([all(isfinite(asarray(elem(point)))) for elem in self.items])
        
        for c in cons:
            val = c.oofun(point)
            if c(point) is False or any(isnan(atleast_1d(val))): 
                activeConstraints.append(c)
                #_activeConstraints.append([c, val, max((val-c.ub, c.lb-val)), c.tol])
                
        r.isFeasible = True if len(activeConstraints) == 0 and allAreFinite else  False
        #r._activeConstraints = activeConstraints
        r.activeConstraints = activeConstraints
        return r
        
    def minimize(self, *args, **kwargs):
        kwargs['goal'] = 'minimum'
        return self._solve(*args, **kwargs)
        
    def maximize(self, *args, **kwargs):
        kwargs['goal'] = 'maximum'
        return self._solve(*args, **kwargs)

    def solve(self, *args, **kwargs):
        kwargs['goal'] = 'solution'
        assert len(args) == 0 or all([not isinstance(arg, oofun) for arg in args])
        return self._solve(*args, **kwargs)

    def _solve(self, *args, **kwargs):
        
        #!!!!! TODO: determing LP, MILP, MINLP if possible
        try:
            import openopt
        except ImportError:
            raise FuncDesignerException('to perform the operation you should have openopt installed')
        
        
        constraints = self._getAllConstraints()
            
        # TODO: mention it in doc
        if 'constraints' in kwargs:
            tmp = set(kwargs['constraints'])
            tmp.update(set(constraints))
            kwargs['constraints'] = tmp
        else:
            kwargs['constraints'] = constraints
        
        freeVars, fixedVars = kwargs.get('freeVars', None), kwargs.get('fixedVars', None)
        isSystemOfEquations = kwargs['goal'] == 'solution'
        
        isLinear = all([(c.oofun.getOrder(freeVars, fixedVars) < 2) for c in constraints])
        
        if isSystemOfEquations:
            if isLinear: # Linear equations system
                p = sle(list(kwargs['constraints']), *args, **kwargs)
            else: # Nonlinear equations system
                f = kwargs['constraints']
                ############################################
                #cons = self._getAllConstraints()
                
                # OLD
#                if not all([array_equal(c.lb, c.ub) for c in f]):
#                    raise FuncDesignerException('Solving constrained nonlinear systems is not implemented for oosystem yet, use SNLE constructor instead')
#                kwargs['constraints'] = ()
                
                # NEW
                C,  F = [], []
                for c in f:
                    F.append(c) if array_equal(c.lb, c.ub) else C.append(c)
                kwargs['constraints'] = C
                f = F
                ############################################
                
                p = openopt.SNLE(f, *args, **kwargs)
                if 'nlpSolver' in kwargs:
                    p.solver = kwargs['nlpSolver']
                    
                
        else: # an optimization problem
            assert len(args) > 0,  'you should have objective function as 1st argument'
            objective = args[0]
            if isinstance(objective, BaseFDConstraint):
                raise FuncDesignerException("1st argument can't be of type 'FuncDesigner constraint', it should be 'FuncDesigner oofun'")
            elif not isinstance(objective, oofun):
                raise FuncDesignerException('1st argument should be objective function of type "FuncDesigner oofun"')
            
            isLinear &= objective.getOrder(freeVars, fixedVars) < 2
            
            if isLinear:
                p = openopt.LP(*args, **kwargs)
                if 'solver' not in kwargs:
                    for solver in self.lpSolvers:
                        if (':' not in solver and not openopt.oosolver(solver).isInstalled )or (solver == 'glpk' and not openopt.oosolver('cvxopt_lp').isInstalled):
                            continue
                        if solver == 'glpk' :
                            p2 = openopt.LP([1, -1], lb = [1, 1], ub=[10, 10])
                            try:
                                r = p2.solve('glpk', iprint=-5)
                            except:
                                continue
                            if r.istop < 0:
                                continue
                            else:
                                break
                    if ':' in solver:
                        pWarn('You have linear problem but no linear solver (lpSolve, glpk, cvxopt_lp) is installed; converter to NLP will be used.')
                    p.solver = solver
                else:
                    solverName = kwargs['solver']
                    if type(solverName) != str:
                        solverName = solverName.__name__
                    if solverName not in self.lpSolvers: 
                        solverName = 'nlp:' + solverName
                        p.solver = solverName 
                        p.warn('you are solving linear problem with non-linear solver')
            else:
                p = openopt.NLP(*args, **kwargs)
                if 'solver' not in kwargs:
                    p.solver = 'ralg'
                
        # TODO: solver autoselect
        #if p.iprint >= 0: p.disp('The optimization problem is  ' + p.probType)
        p._isFDmodel = lambda *args,  **kwargs: True
        return p.solve() if kwargs.get('manage', False) in (False, 0) else p.manage()
        
    def _getAllConstraints(self):
        if self._changed:
            cons = self.constraints
            cons.update(_getAllAttachedConstraints(self.items | self.constraints))
            self._AllConstraints = cons
            self._changed = False
        return self._AllConstraints
        
####################### ooSystemState #########################
class ooSystemState:
    def __init__(self, keysAndValues, *args, **kwargs):
        assert len(args) ==0
        assert len(kwargs) ==0
        #dict.__init__(self, *args, **kwargs)
        self._byID = dict((key, val) for key, val in  keysAndValues)
        self._byNames = dict((key.name, val) for key, val in keysAndValues)
        #self.update(self._byNames)
    
    __repr__ = lambda self: ''.join(['\n'+key+' = '+str(val) for key, val in self._byNames.items()])[1:]
    
    def __call__(self, *args,  **kwargs):
        assert len(kwargs) == 0, "ooSystemState method '__call__' has no implemented kwargs yet"
        r = [(self._byNames[arg] if isinstance(arg,  str) else self._byID[arg]) for arg in args]
        return r[0] if len(r)==1 else r
    
    #__call__ = _call
    #__getitem__ = _call
        # TODO: implement it
        # access by elements and their names

simplify = lambda val: asscalar(val) if isinstance(val, ndarray) and val.size == 1 else val













