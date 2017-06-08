from numpy import hstack,  asarray, abs, atleast_1d, \
logical_not, argsort, vstack, sum, array, nan, all
import numpy as np
from FuncDesigner import oopoint, FDmisc
where = FDmisc.where
#from FuncDesigner.boundsurf import boundsurf


def interalg_ODE_routine(p, solver):
    isIP = p.probType == 'IP'
    isODE = p.probType == 'ODE'
    if isODE:
        f, y0, r30, ftol = p.equations, p.x0, p.times, p.ftol
        assert len(f) == 1, 'multiple ODE equations are unimplemented for FuncDesigner yet'
        f = list(f.values())[0]
        t = list(f._getDep())[0]
    elif isIP:
        assert p.n == 1 and p.__isNoMoreThanBoxBounded__()
        f, y0, ftol = p.user.f[0], 0.0, p.ftol
        if p.fTol is not None: ftol = p.fTol
        t = list(f._getDep())[0]
        r30 = p.domain[t]
        p.iterfcn(p.point([nan]*p.n))
    else:
        p.err('incorrect prob type for interalg ODE routine') 
    
    eq_var = list(p._x0.keys())[0]

    dataType = solver.dataType
    if type(ftol) == int: 
        ftol = float(ftol) # e.g. someone set ftol = 1
    # Currently ftol is scalar, in future it can be array of same length as timeArray
    if len(r30) < 2:
        p.err('length ot time array must be at least 2')    
#    if any(r30[1:] < r30[:-1]):
#        p.err('currently interalg can handle only time arrays sorted is ascending order')  
#    if any(r30 < 0):
#        p.err('currently interalg can handle only time arrays with positive values')  
#    if p.times[0] != 0:
#        p.err('currently solver interalg requires times start from zero')  
    
    r37 = abs(r30[-1] - r30[0])
#    if len(r30) == 2:
#        r30 = np.linspace(r30[0], r30[-1], 150)
    r28 = asarray(atleast_1d(r30[:-1]), dataType)
    r29 = asarray(atleast_1d(r30[1:]), dataType)
    
    r20_store = array([], float)
    r38_store = array([], float)
    r39_store = array([], float)
    maxActiveNodes = 150000#solver.maxActiveNodes

    storedr28 = []
    r27 = []
    r31 = []
    r32 = []
    r33 = ftol
    F = 0.0
    p._Residual = 0
    
    # Main cycle
    for itn in range(p.maxIter+1):
        p.extras['nNodes'].append(r28.size)
        p.extras['nActiveNodes'].append(r28.size)
        mp = oopoint(
                     {t: [r28, r29] if r30[-1] > r30[0] else [r29, r28]}, 
                     skipArrayCast = True
                     )
        mp.isMultiPoint = True
        mp.nPoints = r28.size
        
        mp.dictOfFixedFuncs = p.dictOfFixedFuncs
        mp._dictOfRedirectedFuncs = p._dictOfRedirectedFuncs
        mp.maxDistributionSize = p.maxDistributionSize
        mp.surf_preference = True
        tmp = f.interval(mp, ia_surf_level = 2 if isIP else 1)
        if not all(tmp.definiteRange):
            p.err('''
            solving ODE and IP by interalg is implemented for definite (real) range only, 
            no NaN values in integrand are allowed''')
        # TODO: perform check on NaNs
        isBoundsurf = hasattr(tmp, 'resolve')
        if isBoundsurf:
            if isIP:
                if tmp.level == 1:
                    #adjustr4WithDiscreteVariables(wr4, p)
                    cs = oopoint([(v, asarray(0.5*(val[0] + val[1]), dataType)) for v, val in mp.items()])
                    cs.dictOfFixedFuncs = p.dictOfFixedFuncs
                    cs._dictOfRedirectedFuncs = p._dictOfRedirectedFuncs
                    r21, r22 = tmp.values(cs)
                    o, a = atleast_1d(r21), atleast_1d(r22)
                    r20 = a-o
                    approx_value = 0.5*(a+o)
                else:
                    assert tmp.level == 2
                    ts, te = r28, r29
                    A, B = (te**2 + te*ts+ts**2) / 3.0, 0.5 * (te + ts)
                    a, b, c = tmp.l.d2.get(t, 0.0), tmp.l.d.get(t, 0.0), tmp.l.c
                    val_l = a * A + b * B + c 
                    a, b, c = tmp.u.d2.get(t, 0.0), tmp.u.d.get(t, 0.0), tmp.u.c
                    val_u =  a * A + b * B + c 
                    r20 = val_u - val_l
                    approx_value = 0.5 * (val_l + val_u)
#                    import pylab, numpy
#                    xx = numpy.linspace(-1, 0, 1000)
#                    pylab.plot(xx, tmp.l.d2.get(t, 0.0)[1]*xx**2+ tmp.l.d.get(t, 0.0)[1]*xx+ tmp.l.c[1], 'r')
#                    pylab.plot(xx, tmp.u.d2.get(t, 0.0)[1]*xx**2+ tmp.u.d.get(t, 0.0)[1]*xx+ tmp.u.c[1], 'b')
#                    pylab.grid()
#                    pylab.show()
                    
            elif isODE:
                l, u = tmp.l, tmp.u
                assert len(l.d) <= 1 and len(u.d) <= 1 # at most time variable
                l_koeffs, u_koeffs = l.d.get(t, 0.0), u.d.get(t, 0.0)
                l_c, u_c = l.c, u.c
#                dT = r29 - r28 if r30[-1] > r30[0] else r28 - r29
                
                ends = oopoint([(v, asarray(val[1], dataType)) for v, val in mp.items()])
                ends.dictOfFixedFuncs = p.dictOfFixedFuncs
                ends._dictOfRedirectedFuncs = p._dictOfRedirectedFuncs
                ends_L, ends_U = tmp.values(ends)
                
                starts = oopoint([(v, asarray(val[0], dataType)) for v, val in mp.items()])
                starts.dictOfFixedFuncs = p.dictOfFixedFuncs
                starts._dictOfRedirectedFuncs = p._dictOfRedirectedFuncs
                starts_L, starts_U = tmp.values(starts)

#                o, a = atleast_1d(r21), atleast_1d(r22)

                o, a = tmp.resolve()[0]
#                r20 = 0.5 * u_koeffs * dT  + u_c  - (0.5 * l_koeffs * dT  + l_c)
                r20_end = 0.5 * (ends_U - ends_L)
                r20_start = 0.5 * (starts_U - starts_L)
                r20 = where(r20_end>r20_start, r20_end, r20_start)
                
#                r20 = 0.5 * u_koeffs * dT ** 2 + u_c * dT - (0.5 * l_koeffs * dT ** 2 + l_c * dT)
#                r20 =  0.5*u_koeffs * dT  + u_c  - ( 0.5*l_koeffs * dT  + l_c)

#                o = 0.5*l_koeffs * dT + l_c
#                a = 0.5*u_koeffs * dT + u_c
                #assert 0, 'unimplemented'
            else:
                assert 0
        else:
            o, a = atleast_1d(tmp.lb), atleast_1d(tmp.ub)
            ends_L = starts_L = o
            ends_U = starts_U = a
            r20 = a - o
            approx_value = 0.5 * (a+o)
        
        if isODE:
            r36 = atleast_1d(r20 <= 0.95 * r33)
            r36 = np.logical_and(r36, r20 < ftol)
            r36 = np.logical_and(r36, a-o < ftol)
#        else:
#            r36 = atleast_1d(r20 <= 0.95 * r33 / r37)

        
        if isODE and isBoundsurf:
            d = r37 #if not isODE or not isBoundsurf else len(r28)
            r36 = np.logical_and(
                                atleast_1d(r20_end <= 0.95 * r33 / d), 
                                atleast_1d(r20_start <= 0.95 * r33 / d)
                                )
            r36 &= atleast_1d(r20_end <= ftol)
            r36 &= atleast_1d(r20_start <= ftol)
        else:
            r36 = atleast_1d(r20 <= 0.95 * r33 / r37)
            
#            r36 = np.logical_and(r36, r20 < ftol)
#            r36 = np.logical_and(r36, a-o < ftol)

        ind = where(r36)[0]
        if isODE:
            storedr28.append(r28[ind])
            r27.append(r29[ind])
            r31.append(a[ind])
            r32.append(o[ind])
#            r31.append(ends_U[ind])
#            r32.append(ends_L[ind])
        else:
            assert isIP
            #F += 0.5 * sum((r29[ind]-r28[ind])*(a[ind]+o[ind]))
            F += sum((r29[ind]-r28[ind])*approx_value[ind])
        
        if ind.size != 0: 
            tmp = abs(r29[ind] - r28[ind])
            Tmp = sum(r20[ind] * tmp) #if not isODE or not isBoundsurf else sum(r20[ind])
            r33 -= Tmp
            if isIP: p._residual += Tmp
            r37 -= sum(tmp)
        
        ind = where(logical_not(r36))[0]
        if 1:#new
            if ind.size == 0 and r20_store.size == 0:
                p.istop = 1000
                p.msg = 'problem has been solved according to required user-defined accuracy %0.1g' % ftol
                break
            if ind.size != 0:
                # TODO: use merge sorted lists
                if r20_store.size != 0:
                    r20_store = hstack((r20_store, r20[ind]*abs(r29[ind] - r28[ind])))
                    r38_store =  hstack((r38_store, r28[ind]))
                    r39_store =  hstack((r39_store, r29[ind]))
                else:
                    r20_store = r20[ind]*abs(r29[ind] - r28[ind])
                    r38_store, r39_store = r28[ind], r29[ind]
                ind_a = argsort(r20_store)
                r20_store = r20_store[ind_a]
                r38_store = r38_store[ind_a]
                r39_store = r39_store[ind_a]
            r38_store, r38 = r38_store[:-maxActiveNodes], r38_store[-maxActiveNodes:]
            r39_store, r39 = r39_store[:-maxActiveNodes], r39_store[-maxActiveNodes:]
            r20_store = r20_store[:-maxActiveNodes]
            r40 = 0.5 * (r38 + r39)
            r28 = vstack((r38, r40)).flatten()
            r29 = vstack((r40, r39)).flatten()
        else:
            if ind.size == 0:
                p.istop = 1000
                p.msg = 'problem has been solved according to required user-defined accuracy %0.1g' % ftol
                break
                
            r38, r39 = r28[ind], r29[ind]
            r40 = 0.5 * (r38 + r39)
            r28 = vstack((r38, r40)).flatten()
            r29 = vstack((r40, r39)).flatten()
            
        # !!! unestablished !!!
        if isODE:
            p.iterfcn(fk = r33/ftol)
        elif isIP:
            p.iterfcn(xk=array(nan), fk=F, rk = ftol - r33)
        else:
            p.err('bug in interalgODE.py')
            
        if p.istop != 0 : 
            break
        
        #print(itn, r28.size)

    if isODE:
        
        t0, t1, lb, ub = hstack(storedr28), hstack(r27), hstack(r32), hstack(r31)
        ind = argsort(t0)
        if r30[0] > r30[-1]:
            ind = ind[::-1] # reverse
        t0, t1, lb, ub = t0[ind], t1[ind], lb[ind], ub[ind]
        lb, ub = hstack((y0, y0+(lb*(t1-t0)).cumsum())), hstack((y0, y0+(ub*(t1-t0)).cumsum()))
        #y_var = p._x0.keys()[0]
        #p.xf = p.xk = 0.5*(lb+ub)
        p.extras = {'startTimes': t0, 'endTimes': t1, eq_var:{'infinums': lb, 'supremums': ub}}
        return t0, t1, lb, ub
    elif isIP:
        P = p.point([nan]*p.n)
        P._f = F
        P._mr = ftol - r33
        P._mrName = 'None'
        P._mrInd = 0
#        p.xk = array([nan]*p.n)
#        p.rk = r33
#        p.fk = F
        #p._Residual = 
        p.iterfcn(asarray([nan]*p.n), fk=F, rk = ftol - r33)
    else:
        p.err('incorrect prob type in interalg ODE routine')
