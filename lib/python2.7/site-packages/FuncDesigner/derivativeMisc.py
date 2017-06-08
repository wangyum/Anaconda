PythonAll = all
from FDmisc import Len, FuncDesignerException, DiagonalType, scipyAbsentMsg, pWarn, scipyInstalled, Diag, \
Copy, Eye, isPyPy, isspmatrix


from baseClasses import OOFun, Stochastic
from numpy import isscalar, ndarray, atleast_2d, prod, int64, asarray, ones_like, array_equal, asscalar
import numpy as np
from multiarray import multiarray
from ooPoint import ooPoint

try:
    from DerApproximator import get_d1#, check_d1
    DerApproximatorIsInstalled = True
except:
    DerApproximatorIsInstalled = False
    

def _D(Self, x, fixedVarsScheduleID, Vars=None, fixedVars = None, useSparse = 'auto'):
    if Self.is_oovar: 
        if (fixedVars is not None and Self in fixedVars) or (Vars is not None and Self not in Vars):
            return {} 
        tmp = x[Self]
        return {Self:Eye(asarray(tmp).size)} if not isinstance(tmp, multiarray) else {Self: ones_like(tmp).view(multiarray)}
        
    if Self.input[0] is None: return {} # fixed oofun. TODO: implement input = [] properly
        
    if Self.discrete: 
        return {}
        #raise FuncDesignerException('The oofun or oovar instance has been declared as discrete, no derivative is available')
    
    CondSamePointByID = True if isinstance(x, ooPoint) and Self._point_id1 == x._id else False
    sameVarsScheduleID = fixedVarsScheduleID == Self._lastDiffVarsID 
    
    dep = Self._getDep()
    
    rebuildFixedCheck = not sameVarsScheduleID
    if rebuildFixedCheck:
        Self._isFixed = (fixedVars is not None and dep.issubset(fixedVars)) or (Vars is not None and dep.isdisjoint(Vars))
    if Self._isFixed: return {}
    ##########################
    
    # TODO: optimize it. Omit it for simple cases.
    #isTransmit = Self._usedIn == 1 # Exactly 1! not 0, 2, ,3, 4, etc
    #involveStore = not isTransmit or Self._directlyDwasInwolved
    involveStore = Self.isCostly

    #cond_same_point = hasattr(Self, '_d_key_prev') and sameDerivativeVariables and (CondSamePointByID or (involveStore and         all([array_equal(x[elem], Self.d_key_prev[elem]) for elem in dep])))
    
    cond_same_point = sameVarsScheduleID and \
    ((CondSamePointByID and Self._d_val_prev is not None) or \
    (involveStore and Self._d_key_prev is not None \
    and PythonAll(array_equal(x[elem], Self._d_key_prev[elem]) for elem in dep)))
    
    if cond_same_point:
        Self.same_d += 1
        #return deepcopy(Self.d_val_prev)
        return dict((key, Copy(val)) for key, val in Self._d_val_prev.items())
    else:
        Self.evals_d += 1

    if isinstance(x, ooPoint): Self._point_id1 = x._id
    if fixedVarsScheduleID != -1: Self._lastDiffVarsID = fixedVarsScheduleID

    derivativeSelf = Self._getDerivativeSelf(x, fixedVarsScheduleID, Vars, fixedVars)

    r = Derivative()
    ac = -1
    for i, inp in enumerate(Self.input):
        if not isinstance(inp, OOFun): continue
        if inp.discrete: continue

        if inp.is_oovar: 
            if (Vars is not None and inp not in Vars) or (fixedVars is not None and inp in fixedVars):
                continue                
            ac += 1
            tmp = derivativeSelf[ac]
            val = r.get(inp, None)
            if val is not None:
                if isscalar(tmp) or (type(val) == type(tmp) == ndarray and prod(tmp.shape) <= prod(val.shape)): # some sparse matrices has no += implemented 
                    r[inp] += tmp
                else:
                    if isspmatrix(val) and type(tmp) == DiagonalType:
                        tmp = tmp.resolve(True)
                    r[inp] = r[inp] + tmp
            else:
                r[inp] = tmp
        else:
            ac += 1
            
            elem_d = inp._D(x, fixedVarsScheduleID, Vars=Vars, fixedVars=fixedVars, useSparse = useSparse) 
            
            t1 = derivativeSelf[ac]
            
            for key, val in elem_d.items():
                #if isinstance(t1, Stochastic) or isinstance(val, Stochastic):
                    #rr = t1 * val
                if isinstance(t1, Stochastic) or ((isscalar(val) or isinstance(val, multiarray)) and (isscalar(t1) or isinstance(t1, multiarray))):
                    rr = t1 * val
                elif isinstance(val, Stochastic):
                    rr = val * t1
                elif type(t1) == DiagonalType and type(val) == DiagonalType:
                    rr = t1 * val
                elif type(t1) == DiagonalType or type(val) == DiagonalType:
                    if isspmatrix(t1): # thus val is DiagonalType
                        rr = t1._mul_sparse_matrix(val.resolve(True))
                    else:
                        if not isPyPy or type(val) != DiagonalType:
                            rr = t1 *  val #if  type(t1) == DiagonalType or type(val) not in (ndarray, DiagonalType) else (val.T * t1).T   # for PyPy compatibility
                        else:
                            rr = (val * t1.T).T
                elif isscalar(val) or isscalar(t1) or prod(t1.shape)==1 or prod(val.shape)==1:
                    rr = (t1 if isscalar(t1) or prod(t1.shape)>1 else asscalar(t1) if isinstance(t1, ndarray) else t1[0, 0]) \
                    * (val if isscalar(val) or prod(val.shape)>1 else asscalar(val) if isinstance(val, ndarray) else val[0, 0])
                else:
                    if val.ndim < 2: val = atleast_2d(val)
                    if useSparse is False:
                        t2 = val
                    else:
                        t1, t2 = considerSparse(t1, val)
                    
                    if not type(t1) == type(t2) == ndarray:
                        # CHECKME: is it trigger somewhere?
                        if not scipyInstalled:
                            Self.pWarn(scipyAbsentMsg)
                            rr = np.dot(t1, t2)
                        else:
                            from scipy.sparse import isspmatrix_csc, isspmatrix_csr, csc_matrix, csr_matrix
                            t1 = t1 if isspmatrix_csc(t1) else t1.tocsc() if isspmatrix(t1)  else csc_matrix(t1)
                            t2 = t2 if isspmatrix_csr(t2) else t2.tocsr() if isspmatrix(t2)  else csr_matrix(t2)
                            if t2.shape[0] != t1.shape[1]:
                                if t2.shape[1] == t1.shape[1]:
                                    t2 = t2.T
                                else:
                                    raise FuncDesignerException('incorrect shape in FuncDesigner function _D(), inform developers about the bug')
                            rr = t1._mul_sparse_matrix(t2)
                            if useSparse is False:
                                rr = rr.toarray() 
                    else:
                        rr = np.dot(t1, t2)
                #assert rr.ndim>1
                
                Val = r.get(key, None)
                ValType = type(Val)
                if Val is not None:
                    if type(rr) == DiagonalType:
                        if ValType == DiagonalType:
                            
                            Val = Val + rr # !!!! NOT inplace! (elseware will overwrite stored data used somewhere else)
                            
                        else:
                            tmp  = rr.resolve(useSparse)
                            if type(tmp) == ndarray and hasattr(Val, 'toarray'):
                                Val = Val.toarray()
                            if type(tmp) == ValType == ndarray and Val.size >= tmp.size:
                                Val += tmp
                            else: # may be problems with sparse matrices inline operation, which are badly done in scipy.sparse for now
                                Val = Val + tmp
                    else:
                        if isinstance(Val, ndarray) and hasattr(rr, 'toarray'): # i.e. rr is sparse matrix
                            rr = rr.toarray() # I guess r[key] will hardly be all-zeros
                        elif hasattr(Val, 'toarray') and isinstance(rr, ndarray): # i.e. Val is sparse matrix
                            Val = Val.toarray()
                        if type(rr) == ValType == ndarray and rr.size == Val.size: 
                            Val += rr
                        else: 
                            Val = Val + rr
                    r[key] = Val
                else:
                    r[key] = rr
    Self._d_val_prev = dict((key, Copy(value)) for key, value in r.items())
    Self._d_key_prev = dict((elem, Copy(x[elem])) for elem in dep) if involveStore else None
    return r


def getDerivativeSelf(Self, x, fixedVarsScheduleID, Vars,  fixedVars):
    Input = Self._getInput(x, fixedVarsScheduleID=fixedVarsScheduleID, Vars=Vars,  fixedVars=fixedVars)
    expectedTotalInputLength = sum([Len(elem) for elem in Input])
    
#        if hasattr(Self, 'size') and isscalar(Self.size): nOutput = Self.size
#        else: nOutput = Self(x).size 

    hasUserSuppliedDerivative = Self.d is not None
    if hasUserSuppliedDerivative:
        derivativeSelf = []
        if type(Self.d) == tuple:
            if len(Self.d) != len(Self.input):
               raise FuncDesignerException('oofun error: num(derivatives) not equal to neither 1 nor num(inputs)')
               
            for i, deriv in enumerate(Self.d):
                inp = Self.input[i]
                if not isinstance(inp, OOFun) or inp.discrete: 
                    #if deriv is not None: 
                        #raise FuncDesignerException('For an oofun with some input oofuns declared as discrete you have to set oofun.d[i] = None')
                    continue
                
                #!!!!!!!!! TODO: handle fixed cases properly!!!!!!!!!!!!
                #if hasattr(inp, 'fixed') and inp.fixed: continue
                if inp.is_oovar and ((Vars is not None and inp not in Vars) or (fixedVars is not None and inp in fixedVars)):
                    continue
                    
                if deriv is None:
                    if not DerApproximatorIsInstalled:
                        raise FuncDesignerException('To perform gradients check you should have DerApproximator installed, see http://openopt.org/DerApproximator')
                    derivativeSelf.append(get_d1(Self.fun, Input, diffInt=Self.diffInt, stencil = Self.stencil, \
                                                 args=Self.args, varForDifferentiation = i, pointVal = Self._getFuncCalcEngine(x), exactShape = True))
                else:
                    # !!!!!!!!!!!!!! TODO: add check for user-supplied derivative shape
                    tmp = deriv(*Input)
                    if not isscalar(tmp) and type(tmp) in (ndarray, tuple, list) and type(tmp) != DiagonalType: # i.e. not a scipy.sparse matrix
                        tmp = atleast_2d(tmp)
                        
                        ########################################

                        _tmp = Input[i]
                        Tmp = 1 if isscalar(_tmp) or prod(_tmp.shape) == 1 else len(Input[i])
                        if tmp.shape[1] != Tmp: 
                            # TODO: add debug msg
#                                print('incorrect shape in FD AD _getDerivativeSelf')
#                                print tmp.shape[0], nOutput, tmp
                            if tmp.shape[0] != Tmp: raise FuncDesignerException('error in getDerivativeSelf()')
                            tmp = tmp.T
                                
                        ########################################

                    derivativeSelf.append(tmp)
        else:
            tmp = Self.d(*Input)
            if not isscalar(tmp) and type(tmp) in (ndarray, tuple, list): # i.e. not a scipy.sparse matrix
                tmp = atleast_2d(tmp)
                
                if tmp.shape[1] != expectedTotalInputLength: 
                    # TODO: add debug msg
                    if tmp.shape[0] != expectedTotalInputLength: raise FuncDesignerException('error in getDerivativeSelf()')
                    tmp = tmp.T
                    
            ac = 0
            if isinstance(tmp, ndarray) and hasattr(tmp, 'toarray') and not isinstance(tmp, multiarray): tmp = tmp.A # is dense matrix
            
            #if not isinstance(tmp, ndarray) and not isscalar(tmp) and type(tmp) != DiagonalType:
            if len(Input) == 1:
#                    if type(tmp) == DiagonalType: 
#                            # TODO: mb rework it
#                            if Input[0].size > 150 and tmp.size > 150:
#                                tmp = tmp.resolve(True).tocsc()
#                            else: tmp =  tmp.resolve(False) 
                derivativeSelf = [tmp]
            else:
                for i, inp in enumerate(Input):
                    t = Self.input[i]
                    if t.discrete or (t.is_oovar and ((Vars is not None and t not in Vars) or (fixedVars is not None and t in fixedVars))):
                        ac += inp.size
                        continue                                    
                    if isinstance(tmp, ndarray):
                        TMP = tmp[:, ac:ac+Len(inp)]
                    elif isscalar(tmp):
                        TMP = tmp
                    elif type(tmp) == DiagonalType: 
                        if tmp.size == inp.size and ac == 0:
                            TMP = tmp
                        else:
                            # print debug warning here
                            # TODO: mb rework it
                            if inp.size > 150 and tmp.size > 150:
                                tmp = tmp.resolve(True).tocsc()
                            else: tmp =  tmp.resolve(False) 
                            TMP = tmp[:, ac:ac+inp.size]
                    else: # scipy.sparse matrix
                        TMP = tmp.tocsc()[:, ac:ac+inp.size]
                    ac += Len(inp)
                    derivativeSelf.append(TMP)
                
        # TODO: is it required?
#                if not hasattr(Self, 'outputTotalLength'): Self(x)
#                
#                if derivativeSelf.shape != (Self.outputTotalLength, Self.inputTotalLength):
#                    s = 'incorrect shape for user-supplied derivative of oofun '+Self.name+': '
#                    s += '(%d, %d) expected, (%d, %d) obtained' % (Self.outputTotalLength, Self.inputTotalLength,  derivativeSelf.shape[0], derivativeSelf.shape[1])
#                    raise FuncDesignerException(s)
    else:
        if Vars is not None or (fixedVars is not None and len(fixedVars) != 0): raise FuncDesignerException("sorry, custom oofun derivatives don't work with Vars/fixedVars arguments yet")
        if not DerApproximatorIsInstalled:
            raise FuncDesignerException('To perform this operation you should have DerApproximator installed, see http://openopt.org/DerApproximator')
            
        derivativeSelf = get_d1(Self.fun, Input, diffInt=Self.diffInt, stencil = Self.stencil, args=Self.args, pointVal = Self._getFuncCalcEngine(x), exactShape = True)
        if type(derivativeSelf) == tuple:
            derivativeSelf = list(derivativeSelf)
        elif type(derivativeSelf) != list:
            derivativeSelf = [derivativeSelf]
    
    #assert all([elem.ndim > 1 for elem in derivativeSelf])
   # assert len(derivativeSelf[0])!=16
    #assert (type(derivativeSelf[0]) in (int, float)) or derivativeSelf[0][0]>480.00006752 or derivativeSelf[0][0]<480.00006750
    return derivativeSelf


def considerSparse(t1, t2):  
    # TODO: handle 2**15 & 0.25 as parameters
    if int64(prod(t1.shape)) * int64(prod(t2.shape)) > 2**15 \
    and ((isinstance(t1, ndarray) and t1.nonzero()[0].size < 0.25*t1.size) or \
    (isinstance(t2, ndarray) and t2.nonzero()[0].size < 0.25*t2.size)):
        if not scipyInstalled: 
            pWarn(scipyAbsentMsg)
            return t1,  t2
            
        from scipy.sparse import csc_matrix, csr_matrix, isspmatrix_csc, isspmatrix_csr
        if not isspmatrix_csc(t1): 
            t1 = csc_matrix(t1)
        if t1.shape[1] != t2.shape[0]: # can be from flattered t1
            assert t1.shape[0] == t2.shape[0], 'bug in FuncDesigner Kernel, inform developers'
            t1 = t1.T
        if not isspmatrix_csr(t2): 
            t2 = csr_matrix(t2)
            
    return t1, t2

def mul_aux_d(x, y):
    Xsize, Ysize = Len(x), Len(y)
    if Xsize == 1:
        return Copy(y)
    elif Ysize == 1:
        return Diag(None, scalarMultiplier = y, size = Xsize)
    elif Xsize == Ysize:
        return Diag(y)
    else:
        raise FuncDesignerException('for oofun multiplication a*b should be size(a)=size(b) or size(a)=1 or size(b)=1')   

class Derivative(dict):
    def __init__(self):
        pass
