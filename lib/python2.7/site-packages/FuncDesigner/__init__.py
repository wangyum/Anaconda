import os, sys
curr_dir = ''.join([elem + os.sep for elem in __file__.split(os.sep)[:-1]])
sys.path += [curr_dir]

__version__ = '0.5620'

from ooVar import oovar, oovars
#from ooFun import _getAllAttachedConstraints, broadcast, ooFun as oofun, AND, OR, NOT, NAND, NOR, XOR
from ooFun import oofun, fd_trace_id

from ooSystem import ooSystem as oosystem
from translator import FuncDesignerTranslator as ootranslator

from ooPoint import ooPoint as oopoint, ooMultiPoint 
from logic import AND, OR, XOR, NOT, EQUIVALENT, NAND, NOR
from baseClasses import Stochastic as _Stochastic
from FDmisc import FuncDesignerException, _getDiffVarsID, _getAllAttachedConstraints, broadcast

try:
    import distribution
    from distribution import P, mean, var, std
except ImportError:
    def sp_err(self, *args,  **kw): 
        raise FuncDesignerException('''
        to use FuncDesigner stochastic programming 
        you should have FuncDesigner with its stochastic module installed
        (this addon is commercial, free for research/educational small-scale problems only).
        Visit http://openopt.org/StochasticProgramming for more details.
        ''')
    class Distribution:
        __getattr__ = sp_err
    distribution = Distribution()
    P = mean = var = std = sp_err
    
from ooarray import ooarray
from numpy import ndarray
#def IMPLICATION(condition, *args):
#    if condition is False: 
#        return True
#    if len(args) == 1 and isinstance(args[0], (tuple, set, list, ndarray)):
#        return ooarray([IMPLICATION(condition, elem) for elem in args[0]]) if condition is not True else args[0]
#    elif len(args) > 1:
#        return ooarray([IMPLICATION(condition, elem) for elem in args]) if condition is not True else args
#    return NOT(condition & NOT(args[0])) if condition is not True else args[0]
def IMPLICATION(condition, *args):
    if condition is False: 
        return True
    if len(args) == 1 and isinstance(args[0], (tuple, set, list, ndarray)):
        return OR(NOT(condition), AND(args[0]))
        #return ooarray([IMPLICATION(condition, elem) for elem in args[0]]) if condition is not True else args[0]
    elif len(args) > 1:
        return OR(NOT(condition), AND(args))
#        return ooarray([IMPLICATION(condition, elem) for elem in args]) if condition is not True else args
    return NOT(condition & NOT(args[0])) if condition is not True else args[0]
    
ifThen = IMPLICATION

from sle import sle
from ode import ode
from dae import dae
from overloads import *
from stencils import d, d2
#from overloads import _sum as sum
from interpolate import scipy_InterpolatedUnivariateSpline as interpolator
from integrate import integrator

isE = False
try:
    import enthought
    isE = True
except ImportError:
    pass
try:
    import envisage
    import mayavi
    isE = True
except ImportError:
    pass
try:
    import xy
    isE = False
except ImportError:
    pass
  
if isE:
    s = """
    Seems like you are using OpenOpt from 
    commercial Enthought Python Distribution;
    consider using free GPL-licensed alternatives
    PythonXY (http://www.pythonxy.com) or
    Sage (http://sagemath.org) instead.
    """
    print(s)
    
del(isE, curr_dir, os, sys)
