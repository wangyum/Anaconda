from FuncDesigner import *
import openopt as oo

a = oovar('a', domain=bool)
b = oovars(2)('b')
c = oovar('c')
d = oovar('d')

objective = (a-1)**2 +100*sum((b-[0.1, 0.2])**2) + 3*(1+10*(1+100*c**2)) + 100*(d-5)**2+ (0.1*a+1)*(c+d)


constraints = [a>0, a<1.03, b>0, b<1.04,  c>0,  c<10.1, d>0, d<10, b**2<[0.01, 0.1], a+b<1, (a-0.1)**2+c<-7+d]
startpoint = {a: 10, b: [20, 1], c:10, d:0.1}
p = oo.QP(objective, startpoint, constraints = constraints)
#solver = 'cvxopt_qp'
#solver = 'qlcp'
solver = 'cplex' # currently only cplex can handle quadratic constraints
r = p.solve(solver)
print(r.xf)
'''
Solver:   Time Elapsed = 0.13 	CPU Time Elapsed = 0.13
objFunValue: 443.03032 (feasible, MaxResidual = 0)
{a: 0.050739341596100884, b_0: 0.070707304556103967, b_1: 0.20026473300961442, c: 7.2797568486102e-08, d: 7.0050009121706722}
'''
