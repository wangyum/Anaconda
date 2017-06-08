from baseProblem import MatrixProblem

class STAB(MatrixProblem):
    _optionalData = []
    probType = 'STAB'
    expectedArgs = ['graph']
    allowedGoals = ['graph stability number']
    showGoal = False
    
    def __init__(self, *args, **kw):
        MatrixProblem.__init__(self, *args, **kw) 
        # TODO: simplify it, handle _init_kwargs in parent class
        self._init_kwargs = kw
        self._immutable = True

    def solve(self, *args, **kw):        
        return set_routine(self,  *args, **kw)

    def manage(self, *args, **kw):
        kw['routine'] = 'manage'
        r = self.solve(*args, **kw)
        return r
    
#    def objFunc(self, x):
#        return dot(self.f, x) + self._c


def set_routine(p,  *args, **kw):
    if len(args) > 1:
        p.err('''
        incorrect number of arguments for solve(), 
        must be at least 1 (solver), other must be keyword arguments''')
    solver = args[0] if len(args) != 0 else kw.get('solver', p.solver)
    routine = kw.pop('routine', 'solve')
    KW = p._init_kwargs.copy()
    KW.update(kw)
    import FuncDesigner as fd, openopt
    is_interalg = openopt.oosolver(solver).__name__ == 'interalg'
    
    graph = p.graph # must be networkx instance
    nodes = graph.nodes()
    edges = graph.edges()
    
    n = len(nodes)
    
    node2index = dict((node, i) for i, node in enumerate(nodes))
    index2node = dict((i, node) for i, node in enumerate(nodes))
    
    
    x = fd.oovars(n, domain=bool)
    objective = fd.sum(x)
    startPoint = {x:[0]*n}
    
    fixedVars = {}
   
    includedNodes = getattr(kw, 'includedNodes', None)
    if includedNodes is None:
        includedNodes = getattr(p, 'includedNodes', ())
    for node in includedNodes:
        fixedVars[x[node2index[node]]] = 1

    excludedNodes = getattr(kw, 'excludedNodes', None)
    if excludedNodes is None:
        excludedNodes = getattr(p, 'excludedNodes', ())
    for node in excludedNodes:
        fixedVars[x[node2index[node]]] = 0

    if p.probType == 'DSP':
        constraints = []
        engine = fd.OR if is_interalg else lambda List: fd.sum(List) >= 1
        Engine = lambda d, n: engine([x[node2index[k]] for k in (list(d.keys())+[n])]) 
        for node in nodes:
            adjacent_nodes_dict = graph[node]
            if len(adjacent_nodes_dict) == 0:
                fixedVars[x[node2index[node]]] = 1
                continue
            constraints.append(Engine(adjacent_nodes_dict, node))
    else:
        constraints = \
        [fd.NAND(x[node2index[i]], x[node2index[j]]) for i, j in edges] \
        if is_interalg else \
        [x[node2index[i]]+x[node2index[j]] <=1 for i, j in edges]
    
    P = openopt.GLP if is_interalg else openopt.MILP
    goal = 'min' if p.probType == 'DSP' else 'max' 
    p = P(objective, startPoint, constraints = constraints, fixedVars = fixedVars, goal = goal)
    
    for key, val in kw.items():
        setattr(p, key, val)
    
    p.finish = lambda r, p: encode(r, n, x, index2node)
    r = getattr(p, routine)(solver, **KW)
    
    return r

def encode(r, n, x, index2node):
    r.solution = [index2node[i] for i in range(n) if r.xf[x[i]] == 1]
    r.ff = len(r.solution)
