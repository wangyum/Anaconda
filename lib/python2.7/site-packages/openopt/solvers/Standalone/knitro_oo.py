#from numpy import *
import numpy as np
from openopt.kernel.baseSolver import baseSolver
from openopt.kernel.nonOptMisc import Vstack, Find, isspmatrix
from knitro import *
from openopt.kernel.setDefaultIterFuncs import SMALL_DELTA_X,  SMALL_DELTA_F
    
class knitro(baseSolver):
    __name__ = 'knitro'
    __license__ = "proprietary"
    __authors__ = 'Ziena Optimization LLC'
    __alg__ = ""
    __homepage__ = 'http://www.ziena.com'
    __info__ = ""
    __optionalDataThatCanBeHandled__ = ['A', 'Aeq', 'b', 'beq', 'lb', 'ub', 'c', 'h']
    _canHandleScipySparse = True
    useStopByException = False
    iterfcnConnected = True
    # CHECK ME!
    #__isIterPointAlwaysFeasible__ = lambda self, p: p.__isNoMoreThanBoxBounded__()
    
    options = ''

    def __init__(self): pass
    def __solver__(self, p):
#        try:
#            os.close(1); os.close(2) # may not work for non-Unix OS
#        except:
#            pass
        p.kernelIterFuncs.pop(SMALL_DELTA_X, None)
        p.kernelIterFuncs.pop(SMALL_DELTA_F, None)
        
        n = p.n

        ncon = p.nc + p.nh + p.b.size + p.beq.size

        g_L, g_U = np.zeros(ncon), np.zeros(ncon)
        g_L[:p.nc] = -np.inf
        g_L[p.nc+p.nh:p.nc+p.nh+p.b.size] = -np.inf

        
        # non-linear constraints, both eq and ineq
        if p.isFDmodel:
            r = []
            if p.nc != 0: r.append(p._getPattern(p.user.c))
            if p.nh != 0: r.append(p._getPattern(p.user.h))
            if p.nb != 0: r.append(p.A)
            if p.nbeq != 0: r.append(p.Aeq)
            if len(r)>0:
#                if all([isinstance(elem, np.ndarray) for elem in r]):
                r = Vstack(r)
#                else:
#                    r = Vstack(r)
#                    if isspmatrix(r):
#                        from scipy import __version__
#                        if __version__.startswith('0.7.3') or __version__.startswith('0.7.2') or __version__.startswith('0.7.1') or __version__.startswith('0.7.0'):
#                            p.pWarn('updating scipy to version >= 0.7.4 is very recommended for the problem with the solver %s' % self.__name__)
            else:
                r = np.array([])
            
            if isspmatrix(r):
                I, J, _ = Find(r)
                # DON'T remove it!
                I, J = np.array(I, np.int64), np.array(J, np.int64)
            
            elif isinstance(r, np.ndarray):
                if r.size == 0:
                    I, J= np.array([], dtype=np.int64),np.array([], dtype=np.int64)
                else:
                    I, J = np.where(r)
            
            else:
                p.disp('unimplemented type:%s' % str(type(r))) # dense matrix? 
#            nnzj = len(I)
        else:
            I, J = np.where(np.ones((ncon, p.n)))
            #I, J = None, None
#            nnzj = ncon * p.n #TODO: reduce it

        def eval_cons(x):
            r = np.array(())
            if p.userProvided.c: r = p.c(x)
            if p.userProvided.h: r = np.hstack((r, p.h(x)))
            r = np.hstack((r, p._get_AX_Less_B_residuals(x), p._get_AeqX_eq_Beq_residuals(x)))
            return r
            
        def evaluateFC (x, c):
            x = np.array(x)#TODO: REMOVE IT IN FUTURE VERSIONS
            obj = p.f(x)
            c[:] = eval_cons(x)
            return obj
    
        def eval_jac_g(x):
            r = []
            if p.userProvided.c: r.append(p.dc(x))
            if p.userProvided.h: r.append(p.dh(x))
            if p.nb != 0: r.append(p.A)
            if p.nbeq != 0: r.append(p.Aeq)
            # TODO: fix it!
#            if any([isspmatrix(elem) for elem in r]):
#                r = Vstack([(atleast_2d(elem) if elem.ndim < 2 else elem) for elem in r])
#            elif len(r)!=0:
#                r = vstack(r)
            r = Vstack(r)
            
            # TODO: make it more properly
            rr = (r.tocsr() if isspmatrix(r) else r)
            R = rr[I, J] if np.prod(rr.shape) != 0 else np.array([])
            if isspmatrix(R) or type(R) == np.matrix: 
                R = R.A
            elif not isinstance(R, np.ndarray): 
                p.err('bug in OpenOpt-knitro connection, inform OpenOpt developers, type(R) = %s' % type(R))
            return R.flatten()

        def evaluateGA(x, objGrad, jac):
            x = np.array(x)#TODO: REMOVE IT IN FUTURE VERSIONS
            df = p.df(x)
            dcons = eval_jac_g(x).tolist()
            objGrad[:] = df
            jac[:] = dcons


        objGoal = KTR_OBJGOAL_MINIMIZE
        objType = KTR_OBJTYPE_GENERAL;
        bndsLo = p.lb.copy()
        bndsUp = p.ub.copy()
        bndsLo[bndsLo < -KTR_INFBOUND] = -KTR_INFBOUND
        bndsUp[bndsUp > KTR_INFBOUND] = KTR_INFBOUND
        bndsLo = bndsLo.tolist()
        bndsUp = bndsUp.tolist()
        m = p.nc + p.nh + p.nb + p.nbeq
        cType = [ KTR_CONTYPE_GENERAL ] * (p.nc+p.nh) + [ KTR_CONTYPE_LINEAR ] * (p.nb+p.nbeq)
        cBndsLo = np.array([-np.inf]*p.nc + [0.0]*p.nh + [-np.inf]*p.nb + [0.0] * p.nbeq)
        cBndsLo[cBndsLo < -KTR_INFBOUND] = -KTR_INFBOUND
        cBndsLo = cBndsLo.tolist()
        cBndsUp = [0.0]* m
        jacIxConstr = I.tolist()
        jacIxVar    = J.tolist()
        hessRow = None#[  ]
        hessCol = None#[  ]

        xInit = p.x0.tolist()

        #---- CREATE A NEW KNITRO SOLVER INSTANCE.
        kc = KTR_new()
        if kc == None:
            raise RuntimeError ("Failed to find a Ziena license.")
            
        if KTR_set_int_param_by_name(kc, "hessopt", 4):
            raise RuntimeError ("Error setting knitro parameter 'hessopt'")
        
        if KTR_set_double_param_by_name(kc, "feastol", p.contol):
            raise RuntimeError ("Error setting knitro parameter 'feastol'")
            
        if KTR_set_char_param_by_name(kc, "outlev", "0"):
            raise RuntimeError ("Error setting parameter 'outlev'")

        if KTR_set_int_param_by_name(kc, "maxit", p.maxIter):
            raise RuntimeError ("Error setting parameter 'maxit'")

        #---- INITIALIZE KNITRO WITH THE PROBLEM DEFINITION.
        ret = KTR_init_problem (kc, n, objGoal, objType, bndsLo, bndsUp,
                                        cType, cBndsLo, cBndsUp,
                                        jacIxVar, jacIxConstr,
                                        hessRow, hessCol,
                                        xInit, None)
        if ret:
            raise RuntimeError ("Error initializing the problem, KNITRO status = %d" % ret)
        
        
        #------------------------------------------------------------------ 
        #     FUNCTION callbackEvalFC
        #------------------------------------------------------------------
         ## The signature of this function matches KTR_callback in knitro.h.
         #  Only "obj" and "c" are modified.
         ##
        def callbackEvalFC (evalRequestCode, n, m, nnzJ, nnzH, x, lambda_, obj, c, objGrad, jac, hessian, hessVector, userParams):
            if evalRequestCode == KTR_RC_EVALFC:
                obj[0] = evaluateFC(x, c)
                return 0
            else:
                return KTR_RC_CALLBACK_ERR

        #------------------------------------------------------------------
        #     FUNCTION callbackEvalGA
        #------------------------------------------------------------------
         ## The signature of this function matches KTR_callback in knitro.h.
         #  Only "objGrad" and "jac" are modified.
         ##
        def callbackEvalGA (evalRequestCode, n, m, nnzJ, nnzH, x, lambda_, obj, c, objGrad, jac, hessian, hessVector, userParams):
            if evalRequestCode == KTR_RC_EVALGA:
                evaluateGA(x, objGrad, jac)
                p.iterfcn(np.array(x), obj[0], np.max(np.array(c)))
                return 0 if p.istop == 0 else KTR_RC_USER_TERMINATION
            else:
                return KTR_RC_CALLBACK_ERR
        
        #---- REGISTER THE CALLBACK FUNCTIONS THAT PERFORM PROBLEM EVALUATION.
        #---- THE HESSIAN CALLBACK ONLY NEEDS TO BE REGISTERED FOR SPECIFIC
        #---- HESSIAN OPTIONS (E.G., IT IS NOT REGISTERED IF THE OPTION FOR
        #---- BFGS HESSIAN APPROXIMATIONS IS SELECTED).
        if KTR_set_func_callback(kc, callbackEvalFC):
            raise RuntimeError ("Error registering function callback.")
        if KTR_set_grad_callback(kc, callbackEvalGA):
            raise RuntimeError ("Error registering gradient callback.")
#        if KTR_set_hess_callback(kc, callbackEvalH):
#            raise RuntimeError ("Error registering hessian callback.")
        
#        def callbackProcessNode (evalRequestCode, n, m, nnzJ, nnzH, x, lambda_, obj, c, objGrad, jac, hessian, hessVector, userParams):
#            #---- THE KNITRO CONTEXT POINTER WAS PASSED IN THROUGH "userParams".
#            #kc = userParams
##            p.iterfcn(np.array(x), obj[0], np.max(np.array(c)))
#
#            #---- USER DEFINED TERMINATION EXAMPLE.
#            #---- UNCOMMENT BELOW TO FORCE TERMINATION AFTER 3 NODES.
#            #if KTR_get_mip_num_nodes (kc) == 3:
#            #    return KTR_RC_USER_TERMINATION
##            print p.istop
##            if p.istop != 0:
##                return KTR_RC_USER_TERMINATION
#            
#            return 0

        #---- REGISTER THE CALLBACK FUNCTION THAT PERFORMS SOME TASK AFTER
        #---- EACH COMPLETION OF EACH NODE IN BRANCH-AND-BOUND TREE.
        
        # for MINLP:
#        if KTR_set_mip_node_callback (kc, callbackProcessNode):
#            raise RuntimeError ("Error registering node process callback.")
        
        # for NLP:
#        if KTR_set_newpoint_callback (kc, callbackProcessNode):
#            raise RuntimeError ("Error registering newpoint callback.")        
        
#        if KTR_set_grad_callback (kc, callbackProcessNode):
#            raise RuntimeError ("Error registering grad callback.")        
            
        try:
            #---- SOLVE THE PROBLEM.
            #----
            #---- RETURN STATUS CODES ARE DEFINED IN "knitro.h" AND DESCRIBED
            #---- IN THE KNITRO MANUAL.
            x       = [0] * n
            lambda_ = [0] * (m + n)
            obj     = [0]
            nStatus = KTR_solve (kc, x, lambda_, 0, obj,
                                     None, None, None, None, None, None)
            x = np.array(x)
            if p.point(p.xk).betterThan(p.point(x)):
                obj = p.fk
                p.xk = p.xk.copy() # for more safety
            else:
                p.xk, p.fk = x.copy(), obj
            if p.istop == 0: p.istop = 1000
        finally:
            #---- BE CERTAIN THE NATIVE OBJECT INSTANCE IS DESTROYED.
            KTR_free(kc)


