#PythonSum = sum
import numpy as np, copy

def categoricalAttribute(oof, attr):
    from ooFun import oofun
    L = len(oof.domain)
    if not hasattr(oof, 'aux_domain'):
        oof.aux_domain = copy.copy(oof.domain)
        ind_numeric = [j for j, elem in enumerate(oof.aux_domain[0]) if type(elem) not in (str, np.str_)]
        if len(ind_numeric):
            ind_first_numeric = ind_numeric[0]
            oof.aux_domain.sort(key = lambda elem: elem[ind_first_numeric])
        oof.domain = np.arange(len(oof.domain))
    ind = oof.fields.index(attr)
    dom = np.array([oof.aux_domain[j][ind] for j in range(L)])
    f = lambda x: dom[int(x)] if type(x) != np.ndarray else dom[np.asarray(x, int)]
    r = oofun(f, oof, engine = attr, vectorized = True, domain = dom)
    r._interval_ = lambda domain, dtype: categorical_interval(r, oof, domain, dtype)
    return r

def categorical_interval(r, oof, domain, dtype):
    l, u = domain[oof]
    l_ind, u_ind = np.asarray(l, int), np.asarray(u, int) +1
    s = l_ind.size
    vals = np.zeros((2, s), dtype)
    for j in range(s):
        tmp = r.domain[l_ind[j]:u_ind[j]]
        vals[0, j], vals[1, j] = tmp.min(), tmp.max()
    definiteRange = True
    return vals, definiteRange
