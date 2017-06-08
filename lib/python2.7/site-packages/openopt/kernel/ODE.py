from baseProblem import NonLinProblem


class ODE(NonLinProblem):
    probType = 'ODE'
    goal = 'solution'
    allowedGoals = ['solution']
    showGoal = False
    _optionalData = []
    FuncDesignerSign = 'equations'
    expectedArgs = ['equations', 'startPoint', 'times']
    ftol = None
    reltol = 1.49012e-8
    abstol = 1.49012e-8
    def __init__(self, *args, **kwargs):
        NonLinProblem.__init__(self, *args, **kwargs)
        domain= args[1]
        self.x0 = domain
#        if any(diff(times) < 0): self.err('''
#        currently required ODE times should be sorted 
#        in ascending order, other cases are unimplemented yet
#        ''')
        
        #self.constraints = [timeVariable > times[0], timeVariable < times[-1]]
        

    def objFunc(self, x):
        return 0
