from baseProblem import MatrixProblem
import numpy as np
#from MOP import MOPsolutions

class BPP(MatrixProblem):
    _optionalData = ['objective']
    probType = 'BPP'
    expectedArgs = ['items', 'bins']
    allowedGoals = ['min', 'max', 'minimum', 'maximum']
    showGoal = True
    _immutable = False
    
    def __init__(self, *args, **kw):
        self.goal = 'min'
        self.bins = {}
        #self.objective = ''
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
        bins, items = self.bins, self.items
        #n = len(items)
#        objective = KW.get('objective', self.objective)
#        if isinstance(objective, (list, tuple, set)):
#            nCriteria = len(self.objective)
#            if 3 * nCriteria != np.asarray(self.objective).size:
#                objective = [(objective[3*i], objective[3*i+1], objective[3*i+2]) for i in range(int(round(np.asarray(self.objective).size / 3)))]
#            if len(objective) == 1:
#                KW['fTol'], KW['goal'] = objective[0][1:]
#        else:
#            objective = [(self.objective, KW.get('fTol', getattr(self, 'fTol')), KW.get('goal', getattr(self, 'goal')))]

        nCriteria = 1#len(objective)
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

        item_numbers = [item.get('n', 1) for item in items]
        nItemTypes = len(items)
        nItems = sum(item_numbers)
        
        Cons = KW.pop('constraints', [])
        if type(Cons) not in (list, tuple):
            Cons = [Cons]
        
        Funcs = {}
        
        usedValues = getUsedValues(Cons)
        bins_keys = set(bins.keys())
        for Set in (bins_keys, usedValues):
            if 'n' in Set:
                Set.remove('n')
        UsedValues = usedValues.copy()
        
        UsedValues.update(bins_keys)
        
        cr_values = {}
        for val in UsedValues:
            if val == 'nItems':
                cr_values[val] = 1
            else:
                cr_values[val] = [obj[val] for obj in items]
        
        nBins = bins.get('n', -1)
        if nBins == -1:
            if len(UsedValues) == 1 and type(bins) == dict:
                Tmp_items = sum(list(cr_values.values()[0]))
                Tmp_bins = bins[list(UsedValues)[0]]
                approx_n_bins = int(np.ceil((2.0 * Tmp_items) / Tmp_bins))
            else:
                approx_n_bins = nItems
            nBins = approx_n_bins
            
        X = fd.oovars(nBins * nItemTypes, domain=int, lb=0).view(np.ndarray).reshape(nItemTypes, nBins)
        
        requireCount  = False
        for item in items:
            if 'n' in item:
#                x[i].domain = np.arange(obj['n']+1) if is_interalg else int
#                x[i].ub = obj['n']
#                x[i].lb = 0
                requireCount  = True
                break
        
        y = fd.oovars(nBins, domain = bool)('y')
        aux_objective = fd.sum(y)
        
        #cr_values = dict([(obj[0], []) for obj in objective])
        
#        MainCr = mainCr if type(mainCr) in (str, np.str_) else list(usedValues)[0]
#        
#        isMainCrMin = objective[0][2] in ('min', 'minimum')
        
        # handling objective(s)
#        FF = []
        
        
        
        for optCrName in UsedValues:
            F = [fd.sum(X[:, j].view(fd.ooarray) * cr_values[optCrName]) for j in range(nBins)]
            Funcs[optCrName] = F
        
        FUNCS = [dict((optCrName, Funcs[optCrName][j]) for optCrName in UsedValues) for j in range(nBins)]
        
#        for obj in objective:
#            FF.append((Funcs[obj[0]](obj[0]) if type(obj[0]) in (str, np.str_) else obj[0](Funcs), obj[1], obj[2]))

        constraints = []
        
        # 1. Constraints from p.constraints

        for c in Cons:
            tmp = [c(_F) for _F in FUNCS]
            constraints += tmp
        
        # 2. Constraints from bins parameters
        for k, v in bins.items():
            if k != 'n':
                constraints += [fd.sum(X[:, j].view(fd.ooarray) * cr_values[k]) <= v*y[j] for j in range(nBins)]
        
        # 3. Number of items of type i from all bins equals to item_numbers[i]
        constraints += [fd.sum(X[i].view(fd.ooarray)) == item_numbers[i] for i in range(nItemTypes)]
        
        # 4. box bounds for interalg
        # TODO: rework when domain=int for interalg will be ready
        if is_interalg:
            for i in range(nItemTypes):
                for v in X[i]:
                    v.domain = np.arange(nItemTypes+1)
#            constraints += [X[i].view(fd.ooarray) <= item_numbers[i] for i in range(nItemTypes)]
        
        startPoint = dict((X[i, j], 0) for i in range(nItemTypes) for j in range(nBins))
        startPoint[y] = [0]*nBins
        
        p = P(aux_objective, startPoint, constraints = constraints)
#        p = P(FF if isMOP else FF[0][0], startPoint, constraints = constraints)#, fixedVars = fixedVars)
        if not isMOP:
            p.goal=self.goal
        
#        r._UsedValues, r._nBins = UsedValues, nBins
#        r._y, r._X, r._items = y, X, items
#        r._optCrName, r._requireCount = optCrName, requireCount
#        r._encode = encode
#        r._encode(r)
        p.finish = lambda r, p: encode(r, UsedValues, nBins, y, X, items, optCrName, requireCount)
        r = getattr(p, routine)(solver, **KW)
        if r is None:
            return
            
        if P != oo.MOP:
            r.ff = p.ff
            
        if isMOP:
            assert 0, 'unimplemented'
#            #assert not requireCount, 'MOP with nItem > 1 is unimplemented yet'
#            r.solution = 'for MOP see r.solutions instead of r.solution'
#            #tmp_c, tmp_v = r.solutions.coords, r.solutions.values  
#            if len(r.solutions):
#                S = []
#                for s in r.solutions:
#                    tmp = [((i, int(s[x[i]])) if requireCount else i) for i in range(n) if s[x[i]]>=1]
#                    if 'name' in items[0]:
#                        tmp = [(items[i]['name'], k) for i, k in tmp] if requireCount else [items[i]['name'] for i in tmp]
#                    S.append(dict(tmp) if requireCount else tmp)
#                Vals = dict([(ff[0].name, r.solutions.values[:, i]) for i, ff in enumerate(FF)])
#
#                Dicts = [s.copy() for s in S]
#                for v in usedValues:
#                    if v != 'nItems':
#                        for i, d in enumerate(Dicts):
#                            d[v] = Vals[v][i]
#                r.solutions = MOPsolutions(Dicts)
#                r.solutions.coords = S
#                r.solutions.values = Vals
        else:
            pass
#            tmp = [((i, int(r.xf[x[i]])) if requireCount else i) for i in range(n) if r.xf[x[i]]>=1]
#            if 'name' in items[0]:
#                tmp = [(items[i]['name'], k) for i, k in tmp] if requireCount else [items[i]['name'] for i in tmp]
#            r.xf = dict(tmp) if requireCount else tmp
        return r

#################################################
#################################################
#################################################

def encode(r, UsedValues, nBins, y, X, items, optCrName, requireCount):
    if requireCount:
        xf = [dict((item.get('name',i), int(r.xf[X[i, j]])) for i, item in enumerate(items) if r.xf[X[i, j]]>0) for j in range(nBins) if r.xf[y[j]]]
    else:
        xf = [tuple(item.get('name',i) for i, item in enumerate(items) if r.xf[X[i, j]]==1) for j in range(nBins) if r.xf[y[j]]]
    
    r.values = dict((optCrName, tuple(sum(item[optCrName]*r.xf[X[i, j]] for i, item in enumerate(items)) for j in range(nBins) if r.xf[y[j]])) for optCrName in UsedValues)
    r.xf = xf
    r.probType = 'BPP'

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
     
