PythonAny = any
from numpy import asscalar, copy, asarray, isfinite, ndarray, array, where, any
from fdmisc import formDictOfFixedFuncs, linear_render, formDictOfRedirectedFuncs


def fdConstraint(p, c, StartPointVars, areFixed, oovD, A, b, Aeq, beq, Z, D_kwargs, LB, UB, inplaceLinearRender):
        #import FuncDesigner as fd
        from FuncDesigner.constraints import SmoothFDConstraint
        from FuncDesigner.BooleanOOFun import BooleanOOFun
        from FuncDesigner import _Stochastic
        if not isinstance(c, SmoothFDConstraint) and isinstance(c, BooleanOOFun): 
            p.hasLogicalConstraints = True
            #continue
        probtol = p.contol
        f, tol = c.oofun, c.tol
        _lb, _ub = c.lb, c.ub
        Name = f.name
        
        dep = f.Dep
        
        isFixed = areFixed(dep)

        if f.is_oovar and isFixed:  
            if p._x0 is None or f not in p._x0: 
                p.err('your problem has fixed oovar '+ Name + ' but no value for the one in start point is provided')
            
            if isinstance(p._x0[f], _Stochastic):
                p.err('''
                Bounds %g <= %s <= %g on distribution "%s":
                box bounds and other direct constraints 
                cannot be directly applied on stochastic variables,
                you should use functions like mean, std, var, P.''' % (c.lb, f.name, c.ub, p._x0[f])
                )
            
            # TODO: mb use c.tol / p.contol?
            if not c.lb <= p._x0[f] <= c.ub:
                s ='''fixed variable "%s" has infeasible box constraint in start point
                (%g <= %g <= %g) 
                thus the problem is infeasible
                ''' % (f.name, c.lb, p._x0[f], c.ub)
                p.err(s)
            
            return True
        
        if not dep.issubset(StartPointVars):
            p.err('your start point has no enough variables to define constraint ' + c.name)

        if tol < 0:
            if any(_lb  == _ub):
                p.err("You can't use negative tolerance for the equality constraint " + c.name)
            elif any(_lb - tol >= _ub + tol):
                p.err("You can't use negative tolerance for so small gap in constraint" + c.name)

            Shift = (1.0+1e-13)*probtol 
            #######################
            # not inplace modification!!!!!!!!!!!!!
            _lb = _lb + Shift
            _ub = _ub - Shift
            #######################
        
        if tol != 0: p.useScaledResidualOutput = True
        
        # TODO: omit it for interalg
        if tol not in (0, probtol, -probtol):
            scaleFactor = abs(probtol / tol)
            
            f *= scaleFactor
            #c.oofun = f#c.oofun * scaleFactor
            _lb, _ub = _lb * scaleFactor, _ub * scaleFactor
            Contol = tol
            Contol2 = Contol * scaleFactor
        else:
            Contol = asscalar(copy(probtol))
            Contol2 = Contol 
            
        if isFixed:
            # TODO: get rid of p.contol, use separate contols for each constraint
            
            if not c(p._x0, tol=Contol2):
                s = """'constraint "%s" with all-fixed optimization variables it depends on is infeasible in start point, 
                hence the problem is infeasible, maybe you should change start point'""" % c.name
                p.err(s)
            return True

        from FuncDesigner import broadcast
        hasFixedVariables = len(p.fixedVarsSet)
#        for j in range(2):
        if hasFixedVariables:
            broadcast(formDictOfFixedFuncs, f, p.useAttachedConstraints, p)
        if p._isStochastic:
            broadcast(formDictOfRedirectedFuncs, f, p.useAttachedConstraints, p)
            if 0 and hasFixedVariables:
                broadcast(formDictOfFixedFuncs, f, p.useAttachedConstraints, p.dictOfFixedFuncs, areFixed, p._x0)
                #TODO: is it ever encountered?
                #broadcast(formDictOfRedirectedFuncs, f, p.useAttachedConstraints, p)

        f_order = f.getOrder(p.freeVarsSet, p.fixedVarsSet, fixedVarsScheduleID = p._FDVarsID)
#        print('c_order:', f_order)
        
        if p.probType in ['LP', 'MILP', 'LLSP', 'LLAVP'] and f_order > 1:
            p.err('for LP/MILP/LLSP/LLAVP all constraints have to be linear, while ' + f.name + ' is not')
        
        if not f.is_oovar and f_order < 2:
            D_kwargs2 = D_kwargs.copy()
            if inplaceLinearRender:
                # interalg only
                D_kwargs2['useSparse'] = False
            D = f.D(Z, **D_kwargs2)
            if inplaceLinearRender:
                # interalg only
                if PythonAny(asarray(val).size > 1 for val in D.values()):
                    p.err('currently interalg can handle only FuncDesigner.oovars(n), not FuncDesigner.oovar() with size > 1')
                f = linear_render(f, D, Z)
#        else:
#            D = {}
        
        # TODO: simplify condition of box-bounded oovar detection
        if f.is_oovar:
            inds = oovD[f]
            f_size = inds[1] - inds[0]

            if any(isfinite(_lb)):
                if _lb.size not in (f_size, 1): 
                    p.err('incorrect size of lower box-bound constraint for %s: 1 or %d expected, %d obtained' % (Name, f_size, _lb.size))
                    
                # for PyPy compatibility
                if type(_lb) == ndarray and _lb.size == 1:
                    _lb = _lb.item()
                
                val = array(f_size*[_lb] if type(_lb) == ndarray and _lb.size < f_size else _lb)
                LB[f] = val if f not in LB else where(val > LB[f], val, LB[f])

            if any(isfinite(_ub)):
                if _ub.size not in (f_size, 1): 
                    p.err('incorrect size of upper box-bound constraint for %s: 1 or %d expected, %d obtained' % (Name, f_size, _ub.size))
                
                # for PyPy compatibility
                if type(_ub) == ndarray and _ub.size == 1:
                    _ub = _ub.item()
                    
                val = array(f_size*[_ub] if type(_ub) == ndarray and _ub.size < f_size else _ub)
                UB[f] = val if f not in UB else where(val < UB[f], val, UB[f])
                    
        elif _lb == _ub:
            if f_order < 2:
                Aeq.append(p._pointDerivative2array(D))      
                beq.append(-f(Z)+_lb)
            elif p.h is None: p.h = [f-_lb]
            else: p.h.append(f-_lb)
        elif isfinite(_ub):
            if f_order < 2:
                A.append(p._pointDerivative2array(D))                       
                b.append(-f(Z)+_ub)
            elif p.c is None: p.c = [f - _ub]
            else: p.c.append(f - _ub)
        elif isfinite(_lb):
            if f_order < 2:
                A.append(-p._pointDerivative2array(D))                       
                b.append(f(Z) - _lb)                        
            elif p.c is None: p.c = [- f + _lb]
            else: p.c.append(- f + _lb)
        else:
            p.err('inform OpenOpt developers of the bug')
            
        if not f.is_oovar:
            Contol = max((0, Contol2))
            # TODO: handle it more properly, especially  for lb, ub of array type
            # FIXME: name of f0 vs f
#            p._FD.nonBoxConsWithTolShift.append((f0, lb_0 - Contol, ub_0 + Contol))
#            p._FD.nonBoxCons.append((f0, lb_0, ub_0, Contol))
            p._FD.nonBoxConsWithTolShift.append((c, f, _lb - Contol, _ub + Contol))
            p._FD.nonBoxCons.append((c, f, _lb, _ub, Contol))
#            if tol not in (0, probtol, -probtol):
#                print('!', f, _lb, _ub, Contol)
        return False



