from wh_conn_solver import wh_conn_solver

class matlab_fsolve(wh_conn_solver):
    __name__ = 'matlab_fsolve'
    __authors__ = ""
    __alg__ = ""
    __optionalDataThatCanBeHandled__ = ()
    arrAttribs = ('x0', )
    funcAttribs = ('f', 'df')
    solver_id = 2

    def __init__(self): 
        pass

