#PythonSum = sum
import NLP

from ooMisc import isspmatrix
from baseProblem import MatrixProblem
from numpy import asfarray, dot, nan, zeros, isfinite, all, ravel, diag, isscalar, arange, ndarray
from copy import copy as PythonCopy


class QP(MatrixProblem):
    probType = 'QP'
    goal = 'minimum'
    allowedGoals = ['minimum', 'min']
    showGoal = False
    _optionalData = ['A', 'Aeq', 'b', 'beq', 'lb', 'ub', 'QC', 'intVars']
    expectedArgs = ['H', 'f']
    FuncDesignerSign = 'H'
    C = 0.0
    
    def _Prepare(self):
        if not self._isFDmodel():
            if not isspmatrix(self.H):
                self.H = asfarray(self.H) # TODO: handle the case in runProbSolver()
            self.n = self.H.shape[0]
            if not hasattr(self, 'x0') or self.x0 is None or self.x0[0] is nan:
                self.x0 = zeros(self.n)
        MatrixProblem._Prepare(self)
        if self._isFDmodel():
            H, f, C = quad_render(self.H, self)
            self.user.f = (self.H, )
            self.H, self.f, self.C = H, f, C
#            print(H, f, C)
            
            if self.fixedVars is None or (self.freeVars is not None and len(self.freeVars)<len(self.fixedVars)):
                order_kw = {'Vars': self.freeVarsSet}
            else:
                order_kw = {'fixedVars': self.fixedVarsSet}
            order_kw['fixedVarsScheduleID'] = self._FDVarsID 
            from FuncDesigner import ooarray
            for c in self.constraints:
                if isinstance(c, ooarray):
                    for elem in c:
                        processConstraint(elem, order_kw, self)
                else:
                    processConstraint(c, order_kw, self)
            r = []
            for v in self._freeVarsList:
                if isinstance(v.domain, (tuple, list, ndarray, set)):
                    self.err('for FuncDesigner MILP models only variables with domains int, bool or None (real) are implemented for now')
                if v.domain is int or v.domain is  'int' or v.domain is bool or v.domain is 'bool':
                    r1, r2 = self._oovarsIndDict[v]
                    r += arange(r1, r2).tolist()
            
            self.intVars, self._intVars = r, self.intVars
        self._intVars_vector = self.intVars
    
    def __init__(self, *args, **kwargs):
        self.QC = []
        MatrixProblem.__init__(self, *args, **kwargs)
        if self._isFDmodel():
            if len(args) > 1:
                self.x0 = args[1]
            self.f = args[0]
        else:
            if len(args) > 1 or 'f' in kwargs.keys():
                self.f = ravel(self.f)

    def objFunc(self, x):
        return asfarray(0.5*dot(x, self.matMultVec(self.H, x)) + dot(self.f, x).sum()).flatten() + self.C

    def qp2nlp(self, solver, **solver_params):
        if hasattr(self,'x0'): p = NLP.NLP(ff, self.x0, df=dff, d2f=d2ff)
        else: p = NLP.NLP(ff, zeros(self.n), df=dff, d2f=d2ff)
        p.args.f = self # DO NOT USE p.args = self IN PROB ASSIGNMENT!
        p.iprint = self.iprint
        self.fill(p)
        self.iprint = -1
        

        # for QP plot is via NLP
        p.show = self.show
        p.plot, self.plot = self.plot, 0

        #p.checkdf()
        r = p.solve(solver, **solver_params)
        self.xf, self.ff, self.rf = r.xf, r.ff, r.rf
        return r

    def __finalize__(self):
        if self.isFDmodel: self.intVars = self._intVars
        MatrixProblem.__finalize__(self)

ff = lambda x, QProb: QProb.objFunc(x)
def dff(x, QProb):
    r = dot(QProb.H, x)
    if all(isfinite(QProb.f)) : r += QProb.f
    return r

def d2ff(x, QProb):
    r = QProb.H
    return r

def processConstraint(c, order_kw, p):
    if c is True:
        return
    order = c.oofun.getOrder(**order_kw)
    if order < 2:
        return
    elif order > 2:
        assert 0, 'at most quadratic constraint is expected'
    H, f, C = quad_render(c.oofun, p)
    finite_lb = isfinite(c.lb)
    finite_ub = isfinite(c.ub)
    assert np.logical_xor(finite_lb, finite_ub), 'exactly one finite bound is expected'
    if finite_lb:
        p.QC.append((-H, -f, -c.lb - C))
    else:#finite_ub
        p.QC.append((H, f, -c.ub + C))
        

from nonOptMisc import scipyInstalled
import numpy as np

def quad_render(arg, p):
#    from FuncDesigner import oofun
    from FuncDesigner.ooPoint import ooPoint
    from FuncDesigner.baseClasses import OOArray
    if isinstance(arg, OOArray):
        assert arg.size == 1, 'quad_render works with oofuns with scalar output only'
        arg = arg.item()
    #assert type(arg) == oofun, 'oofun input expected'
    assert p.fixedVars is None, 'quadratic rendering is unimplemented for fixedVars yet'
    
    optVarSizes = p._optVarSizes
#    print(optVarSizes.values(), np.array(optVarSizes.values()))
    assert all(np.array(list(optVarSizes.values())) == 1), 'quadratic rendering is unimplemented for oovar(size=n) yet, use oovars(n) instead'
        
    oovarsIndDict = p._oovarsIndDict
    n = p.n
    
    if 1 and scipyInstalled and p.useSparse is not False:
        useSparse = p.useSparse
        if useSparse == 'auto':
            useSparse = p.n > 150
    else:
        useSparse = False
        
    if useSparse:
        from scipy.sparse import lil_matrix
        H = lil_matrix((n, n))
    else:
        H = np.zeros((n, n))
    f = np.zeros(n)
    c = 0.0
    
    startPoint = p._x0
    
    if p.fixedVars is None or (p.freeVars is not None and len(p.freeVars)<len(p.fixedVars)):
        order_kw = {'Vars': p.freeVarsSet}
        Z = dict((v, np.zeros_like(p._x0[v]) if v in p._freeVars else p._x0[v]) for v in p._x0.keys())
    else:
        order_kw = {'fixedVars': p.fixedVarsSet}
        Z = dict((v, np.zeros_like(p._x0[v]) if v not in p._fixedVars else p._x0[v]) for v in p._x0.keys())
    Z = ooPoint(Z)
    D_kwargs = p._D_kwargs
    D_kwargs['useSparse'] = useSparse
    order_kw['fixedVarsScheduleID'] = p._FDVarsID 
    
#    D = arg.D(Z, **D_kwargs)
    
    elems = PythonCopy(arg._summation_elements) if arg._isSum else [arg]
    
    while(len(elems) != 0):
        elem = elems.pop()
        if np.isscalar(elem) or type(elem) == np.ndarray:
            c += elem
            continue
        order = elem.getOrder(**order_kw)
        assert order <= 2, 'constant,linear or quadratic function is expected'
        if order == 0:
            c += elem(startPoint)
        elif order == 1:
            # TODO: mb rework fd.sum() to sum(linear) + sum(nonlin)
            pointDerivative = elem.D(Z, **D_kwargs)
            if len(pointDerivative) != 0:
                # TODO: check iadd with different types (dense/sparse)
                asdf(p, pointDerivative, useSparse, f)
#                tmp = p._pointDerivative2array(pointDerivative, useSparse = useSparse)
#                if hasattr(tmp, 'toarray'):
#                    tmp = tmp.toarray()
#                f += tmp.flatten()
            c += elem(Z)
        elif order == 2:
            if elem._isProd:
                prod_elements =  elem._prod_elements
                last_prod_elem = prod_elements[-1]
                lastElemIsScalar = np.isscalar(last_prod_elem) or\
                    (type(last_prod_elem) == np.ndarray and last_prod_elem.size == 1)
                L = len(prod_elements)
                if L > 2:
                    assert lastElemIsScalar, 'unimplemented yet'
                    assert len(prod_elements) == 3
                    elem1, elem2, koeff = prod_elements
                    squared_elem = None
                else:# L == 2:
                    if lastElemIsScalar:
                        koeff = last_prod_elem
                        tmp = prod_elements[0]
                        if tmp._isSum:
                            elems += [koeff * Elem for Elem in tmp._summation_elements]
                            continue
                        else:
                            squared_elem = tmp.input[0] if not tmp.is_oovar else tmp
                        elem1 = elem2 = None
                    else:
                        koeff = None
                        elem1, elem2 = prod_elements
                        squared_elem = None
                if elem2 is not None and elem2._isSum:
                    elem1, elem2 = elem2, elem1
                if elem1 is not None and elem1._isSum:
                    Tmp = koeff*elem2 if koeff is not None else elem2
                    elems += [Tmp * Elem for Elem in elem1._summation_elements]
                    continue
            
            else:
                if elem.fun == np.sum: # oofun.sum()
                    assert len(elem.input) == 1
                    elems.append(elem.input[0])
                    continue
                else:
                    squared_elem = elem.input[0] if not elem.is_oovar else elem
                koeff = None
            if squared_elem is not None:
#                tmp = squared_elem.input[0] if not squared_elem.is_oovar else squared_elem
#                assert tmp.is_oovar, 'unimplemented yet'
#                d = tmp.D(Z, **D_kwargs)
                d = squared_elem.D(Z, **D_kwargs)

                #assert len(d) == 1, 'unimplemented yet'
                if len(d) > 1:
                    assert squared_elem._isSum, 'unimplemented yet'
                    Tmp = squared_elem * koeff if koeff is not None else squared_elem
                    elems += [Tmp * Elem for Elem in squared_elem._summation_elements]
                    continue
                oov, lin_coeff = list(d.items())[0]
                const = squared_elem(Z)
#                print('const:', const)
#                const = tmp(Z)
                if isscalar(lin_coeff):
                    Tmp2 = np.float(lin_coeff ** 2)  
                    Tmp1 = 2.0 * lin_coeff * const
                else:
                    Diag = diag(lin_coeff)
                    Tmp2 = Diag **2.0
                    Tmp1 = 2.0 * Diag * const
                Tmp0 = const ** 2.0
                if koeff is not None:
                    Tmp2 *= koeff
                    Tmp1 *= koeff
                    Tmp0 *= koeff
                Ind = oovarsIndDict[oov]
#                assert Ind[1]-Ind[0] == 1, 'unimplemented yet'
                if Ind[1]-Ind[0] == 1:
                    H[Ind[0], Ind[0]] += Tmp2
                    f[Ind[0]] += Tmp1
                else:
                    H[range(Ind[0], Ind[1]), range(Ind[0], Ind[1])] += Tmp2
                    f[range(Ind[0], Ind[1])] += Tmp1
                c += Tmp0 if isscalar(Tmp0) else Tmp0.sum()
#                for k, v in d.items():
#                    pass
            else:
                assert elem1.is_oovar and elem2.is_oovar, 'unimplemented yet'
                Tmp = 1.0 if koeff is None else koeff
                Ind1, Ind2 = oovarsIndDict[elem1], oovarsIndDict[elem2]
                assert Ind1[1]-Ind1[0] == 1, 'unimplemented yet'
                assert Ind2[1]-Ind2[0] == 1, 'unimplemented yet'
                
                H[Ind1[0], Ind2[0]] += Tmp
                
    H = H + H.T
    return H, f, c

#def updateH(H, ind1, ind2, elem):
#    H[ind1, ind2] += elem

def asdf(p, pointDerivative, useSparse, f):
    if 1 or useSparse is False:
        for k, v in pointDerivative.items():
            Ind = p._oovarsIndDict[k]
            if type(v) in (float, np.float64):
                f[Ind[0]]+=v
            else:
                f[Ind[0]:Ind[1]] += v if type(v) != ndarray else v.item()
    else:
        tmp = p._pointDerivative2array(pointDerivative, useSparse = useSparse)
        if hasattr(tmp, 'toarray'):
            tmp = tmp.toarray()
        f += tmp.flatten()

    
    
#    if p.fixedVars is None or (p.freeVars is not None and len(p.freeVars)<len(p.fixedVars)):
#        Z = dict([(v, zeros_like(self._x0[v]) if v in self._freeVars else self._x0[v]) for v in self._x0.keys()])
##        varIsFixed = lambda v: v not in p.freeVars
#    else:
#        Z = dict([(v, zeros_like(self._x0[v]) if v not in self._fixedVars else self._x0[v]) for v in self._x0.keys()])
##        varIsFixed = lambda v: v in p.fixedVars
    
#    Elems = arg._summation_elements if arg._isSum else [arg]
#    for elem in Elems:
#        if isinstance(elem, OOArray):
#            assert elem.size == 1, 'quadratic rendering is implemented for oofuns with scalar output only'
#            elem = elem.item()
#            
#        if isinstance(elem, oofun):
#            if elem.is_oovar:
#                if varIsFixed(elem):
#                    c += startPoint[elem]
#                f[oovarsIndDict[elem]] += 1.0
#            else:
#                if elem._alt__neg__ is not None:
#                    elem = (-1)*elem._neg_elem
#                assert elem._isProd, 'incompatible oofun or bug in quad_render'
#                elem1, elem2 =  elem._prod_elements[0], elem._prod_elements[-1]
#                assert isinstance(elem1, oofun)
#                if isinstance(elem2, oofun):
#                    
#                
#                
#        elif isinstance(elem, np.ndarray):
#            assert elem.size == 1, 'quadratic rendering is implemented for oofuns with scalar output only'
#            c += elem
#        else:
#            assert 0, 'quadratic rendering is implemented for type %s' % type(elem)
