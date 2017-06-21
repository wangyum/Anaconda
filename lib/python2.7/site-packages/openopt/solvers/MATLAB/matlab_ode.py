from wh_conn_solver import wh_conn_solver

class matlab_ode(wh_conn_solver):
    __license__ = "proprietary"
    __authors__ = ""
    __alg__ = ""
    __optionalDataThatCanBeHandled__ = []
    arrAttribs = ('x0', 'times')
    funcAttribs = ('f', 'df')
    solver_id = 100

    def __init__(self): 
        pass

