from numpy import all, abs
from overloads import hstack
from FDmisc import FuncDesignerException

def d(arg, v, **kw):#, *args, **kw):
    N = len(v)
#    if len(args) == 1:
#        derivativeSide = args[0]
#        assert derivativeSide in ('left', 'right', 'both')
#    else:
#        derivativeSide = 'both'
    stencil = kw.get('stencil', 3)
    if stencil not in (2, 3):
       raise FuncDesignerException('for d1 only stencil = 2 and 3 are implemented')
    
    timestep = v[1]-v[0]
    if not all(abs(v[1:] - v [:-1] - timestep) < 1e-10):
        raise FuncDesignerException('unimplemented for non-uniform step yet')
    if stencil == 2:
        r1 = -3*arg[0] + 4*arg[1] - arg[2]
        r2 = (arg[2:N] - arg[0:N-2]) / 2.0
        r3 = 3*arg[N-1] - 4*arg[N-2] + arg[N-3]
        return hstack((r1, r2, r3)) / timestep
    elif stencil == 3:
        r1 = -22 * arg[0] + 36 * arg[1] - 18 * arg[2] + 4 * arg[3]
        r2 = -22 * arg[1] + 36 * arg[2] - 18 * arg[3] + 4 * arg[4] # TODO: mb rework it?
        r3 = arg[0:N-4] -8*arg[1:N-3] + 8*arg[3:N-1] - arg[4:N]
        r4 = 22 * arg[N-5] - 36 * arg[N-4] + 18 * arg[N-3] - 4 * arg[N-2] # TODO: mb rework it?
        r5 = 22 * arg[N-4] - 36 * arg[N-3] + 18 * arg[N-2] - 4 * arg[N-1]
        return hstack((r1, r2, r3, r4, r5)) / (12*timestep)
    
#    if derivativeSide == 'both':
#        r =  hstack((r1, r2, r3))
#    elif derivativeSide == 'left':
#        r =  hstack((r1, r2))
#    else: # derivativeSide == 'right'
#        r =  hstack((r2, r3))
    return r

def d2(arg, v, **kw):#, *args, **kw):
    N = len(v)
    timestep = v[1]-v[0]
    if not all(abs(v[1:] - v [:-1] - timestep) < 1e-10):
       raise FuncDesignerException('unimplemented for non-uniform step yet')
    stencil = kw.get('stencil', 1)
    if stencil not in (1, ):
       raise FuncDesignerException('for d2 only stencil = 1 is implemented')
    if stencil == 1:
        r1 = arg[0] - 2*arg[1] + arg[2]
        r2 = arg[0:N-2] - 2 * arg[1:N-1] + arg[2:N]
        r3 = arg[N-1] - 2*arg[N-2] + arg[N-3]
        return hstack((r1, r2, r3)) / timestep**2

