from wh_conn_solver import wh_conn_solver

class fmincon(wh_conn_solver):
    __name__ = 'fmincon'
    __authors__ = ""
    __alg__ = ""
    __optionalDataThatCanBeHandled__ = ['A', 'Aeq', 'b', 'beq', 'lb', 'ub', 'c', 'h']
    arrAttribs = ('x0', 'lb', 'ub', 'A', 'Aeq', 'b', 'beq', 'nc', 'nh')
    funcAttribs = ('f', 'df', 'c', 'dc', 'h', 'dh')
    solver_id = 1

    def __init__(self): 
        pass

