from baseProblem import MatrixProblem
import numpy as np
from MOP import MOPsolutions

class KSP(MatrixProblem):
    _optionalData = []
    probType = 'KSP'
    expectedArgs = ['objective', 'items']
    allowedGoals = ['min', 'max', 'minimum', 'maximum']
    showGoal = True
    
    def __init__(self, *args, **kw):
        self.goal = 'max'
        self.objective = 'weight'
        MatrixProblem.__init__(self, *args, **kw)
        self._init_kwargs = kw
        self._immutable = True
        
    def manage(self, *args, **kw):
        kw['routine'] = 'manage'
        r = self.solve(*args, **kw)
        return r
        
    def solve(self, *args, **kw):
        import FuncDesigner as fd, openopt as oo 
        
        if len(args) > 1:
            self.err('''
            incorrect number of arguments for solve(), 
            must be at least 1 (solver), other must be keyword arguments''')
        solver = args[0] if len(args) != 0 else kw.get('solver', self.solver)
        routine = kw.pop('routine', 'solve')

        KW = self._init_kwargs.copy()
        KW.update(kw)
        items = self.items
        n = len(items)
        objective = KW.get('objective', self.objective)
        if isinstance(objective, (list, tuple, set)):
            nCriteria = len(self.objective)
            if 3 * nCriteria != np.asarray(self.objective).size:
                objective = [(objective[3*i], objective[3*i+1], objective[3*i+2]) for i in range(int(round(np.asarray(self.objective).size / 3)))]
            if len(objective) == 1:
                KW['fTol'], KW['goal'] = objective[0][1:]
        else:
            objective = [(self.objective, KW.get('fTol', getattr(self, 'fTol')), KW.get('goal', getattr(self, 'goal')))]

        nCriteria = len(objective)
        isMOP = nCriteria > 1
        #mainCr = objective[0][0]
        
        solverName = solver if type(solver) == str else solver.__name__
        is_interalg = solverName == 'interalg'
        is_glp = False#solverName == 'sa'
        if is_glp:
            assert nCriteria == 1, 'you cannot solve multiobjective KSP by the solver'
            
        #is_interalg_raw_mode = is_interalg and KW.get('dataHandling', oo.oosolver(solver).dataHandling) in ('auto','raw')
        KW.pop('objective', None)
        P = oo.MOP if nCriteria > 1 else oo.GLP if is_interalg else oo.MILP if not is_glp else oo.GLP

        
        x = fd.oovars(n, domain=bool)
        requireCount  = False
        for i, obj in enumerate(items):
            if 'n' in obj:
                x[i].domain = np.arange(obj['n']+1) if is_interalg else int
                x[i].ub = obj['n']
                x[i].lb = 0
                requireCount  = True

        #cr_values = dict([(obj[0], []) for obj in objective])
        
        constraints = []
        
        Funcs = {}
        Cons = KW.pop('constraints', [])
        if type(Cons) not in (list, tuple):
            Cons = [Cons]
        usedValues = getUsedValues(Cons)
        usedValues.update(getUsedValues([obj[0] for obj in objective]))
        cr_values = {}
        for val in usedValues:
            cr_values[val] = 1 if val == 'nItems' else [obj[val] for obj in items]
        
#        MainCr = mainCr if type(mainCr) in (str, np.str_) else list(usedValues)[0]
#        
#        isMainCrMin = objective[0][2] in ('min', 'minimum')
        
        # handling objective(s)
        FF = []
        
        for optCrName in usedValues:
            F = fd.sum(x * cr_values[optCrName])
            Funcs[optCrName] = F
        
        for obj in objective:
            FF.append((Funcs[obj[0]](obj[0]) if type(obj[0]) in (str, np.str_) else obj[0](Funcs), obj[1], obj[2]))

        for c in Cons:
            tmp = c(Funcs)
            if type(tmp) in (list, tuple, set):
                constraints += list(tmp)
            else:
                constraints.append(tmp)
        
        startPoint = {x:[0]*n}

        p = P(FF if isMOP else FF[0][0], startPoint, constraints = constraints)#, fixedVars = fixedVars)
        if not isMOP:
            p.goal=self.goal
        p.finish = lambda r, p: encode(r, isMOP, n, x, requireCount, items, FF, usedValues)
        r = getattr(p, routine)(solver, **KW)
        if r is None:
            return
        
#        if P != oo.MOP:
#            r.ff = p.ff
        
        return r

class D:
    def __init__(self):
        self.used_vals = set()
    def __getitem__(self, item):
        self.used_vals.add(item)
        return 1.0
    
def getUsedValues(Iterator):
    d = D()
    r = set()
    for elem in Iterator:
        if type(elem) in [str, np.str_]:
            r.add(elem)
        else:
            elem(d)
    r.update(d.used_vals)
    return r
     
def encode(r, isMOP, n, x, requireCount, items, FF, usedValues):
    if isMOP:
        #assert not requireCount, 'MOP with nItem > 1 is unimplemented yet'
        r.solution = 'for MOP see r.solutions instead of r.solution'
        #tmp_c, tmp_v = r.solutions.coords, r.solutions.values  
        if len(r.solutions):
            S = []
            for s in r.solutions:
                tmp = [((i, int(s[x[i]])) if requireCount else i) for i in range(n) if s[x[i]]>=1]
                if 'name' in items[0]:
                    tmp = [(items[i]['name'], k) for i, k in tmp] if requireCount else [items[i]['name'] for i in tmp]
                S.append(dict(tmp) if requireCount else tmp)
            Vals = dict([(ff[0].name, r.solutions.values[:, i]) for i, ff in enumerate(FF)])

            Dicts = [s.copy() for s in S]
            for v in usedValues:
                if v != 'nItems':
                    for i, d in enumerate(Dicts):
                        d[v] = Vals[v][i]
            r.solutions = MOPsolutions(Dicts)
            r.solutions.coords = S
            r.solutions.values = Vals
    else:
        tmp = [((i, int(r.xf[x[i]])) if requireCount else i) for i in range(n) if r.xf[x[i]]>=1]
        if 'name' in items[0]:
            tmp = [(items[i]['name'], k) for i, k in tmp] if requireCount else [items[i]['name'] for i in tmp]
        r.xf = dict(tmp) if requireCount else tmp
    r.probType = 'KSP'
