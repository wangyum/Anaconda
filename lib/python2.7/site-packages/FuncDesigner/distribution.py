import operator, overloads as o, numpy as np
from numpy import ndarray
from ooarray import ooarray
from FuncDesigner.multiarray import multiarray

from ooFun import oofun, FuncDesignerException
try:
    from constraints import BaseFDConstraint
except:
    # for previous versions, TODO: remove in future
    from ooFun import BaseFDConstraint
    
#from FuncDesigner.FDmisc import raise_except

from baseClasses import Stochastic, OOArray, distrib_err_fcn


class stochasticDistribution(Stochastic):
    __array_priority__ = 10#00001
    isSorted = False
    quantified = True
#    licenseMsgWasShown = np.array(False)
#    _is_product = False
    
    def __init__(self, _values=None, _probabilities=None, distribType = 'undefined', ppf = None, N = None, quantiles=None, Str = ''):
        Stochastic.__init__(self)
        self.distribType = distribType
        if Str != '':
            self._str = Str
        if ppf is not None:
            assert quantiles is None, 'quantiles in constructor are unimplemented yet'
    
            if N is None:
                self.quantified = False
                   #r.__repr__ = lambda self: self._str
                self._yield_quantified = lambda k: stochasticDistribution(ppf(np.arange(1.0, float(k+1)) / (k+2)), [1.0/k]*k, Str = (self._str + ' quantified into %d points' % k), distribType = self.distribType)
                return
            else:
                if quantiles is None:
                    quantiles = np.arange(1, N+1) / float(N+2)
                else:
                    assert len(quantiles) == N, 'lenght of quantiles must be equal to number of points to be created'
                
                values = ppf(quantiles)
                probabilities = np.array([1.0/N]*N)
                self._str = Str + ' quantified into %d points' % N
        else:
            values = _values if type(_values) == np.ndarray else np.asfarray(_values)
            if _probabilities is None:
                raise FuncDesignerException('for assignment with this set of parameters you should provide probabilities as well')
            probabilities = _probabilities if type(_probabilities) == np.ndarray else np.asfarray(_probabilities)
        if np.any(probabilities < -1e-15):
            raise FuncDesignerException('probabilities cannot be negative')
        if values.size != probabilities.size:
            s = '''
            in stochastic distribution constructor lenght of values (got: %d) must be equal to lenght of probabilities (got: %d)
            ''' % (values.size, probabilities.size)
            raise FuncDesignerException(s)
        probabilitiesSum = np.sum(probabilities)
        Diff = np.abs(probabilitiesSum - 1)
        if Diff > 1e-7:
            p_sum_msg = 'probabilities sum differs too much: 1.0 expected, differrence = %e' % Diff
            raise FuncDesignerException(p_sum_msg)
        if Diff > 1e-10:
            # not inplace for more safety
            probabilities = probabilities / probabilitiesSum 
            
        #obj = asanyarray(values).view(self)
        self.values = values.copy()
        self.probabilities = probabilities.copy()
        
        #return obj

    #__copy__ = lambda self: stochasticDistribution(self.values.copy(), self.probabilities.copy(), distribType = self.distribType)
    
    def __repr__(self):
        if self._str != '':
            return self._str
        self.sort()
        n = self.values.size
        if n <= 9:
            s1, s2 = str(self.values), str(self.probabilities)
        else:
            s1 = str(self.values[:4])[:-1] + ' ... ' + str(self.values[-4:])[1:]
            s2 = str(self.probabilities[:4])[:-1] + ' ... ' + str(self.probabilities[-4:])[1:]
        if self.distribType == 'undefined':
            s0 = ''
        elif self.distribType == 'discrete':
            s0 = 'discrete '
        else:
            assert self.distribType == 'continuous'
            s0 = 'discretized continuous '
        s = \
        '''
        %sstochastic distribution of size %d
        with values %s
        and probabilities %s
        ''' % (s0, n, s1, s2)
        return s
    
    def __copy__(self):
        return stochasticDistribution(self.values.copy(), self.probabilities.copy())._update(self)
    copy = __copy__
    
    def _update(self, other):
        self.distribType = other.distribType
        if 'stochDep' in other.__dict__:
            self.stochDep = other.stochDep.copy()
        if 'maxDistributionSize' in other.__dict__:
            self.maxDistributionSize = other.maxDistributionSize
        if '_p' in other.__dict__:
            self._p = other._p
        return self
    
    __pos__ = lambda self: self
    __sub__ = lambda self, other: mergeDistributions(self, other, operator.sub)#self + (-asfarray(other).copy()) if type(other) in (list, tuple, ndarray) else self + (-other)

    __add__ = lambda self, other: mergeDistributions(self, other, operator.add)
    __radd__ = lambda self, other: mergeDistributions(self, other, operator.add)
    
    #TODO: improve it
    __neg__ = lambda self: mergeDistributions(0.0, self, operator.sub)
   
    __mul__ = lambda self, other: mergeDistributions(self, other, operator.mul)
    __rmul__ = lambda self, other: self.__mul__(other)
    
    __div__ = lambda self, other: mergeDistributions(self, other, operator.truediv)    
    __truediv__ = __div__
    __rdiv__ = lambda self, other: mergeDistributions(other, self, operator.truediv)    
    __rtruediv__ = __rdiv__
    
    __pow__ = lambda self, other: mergeDistributions(self, other, operator.pow)
    __rpow__ = lambda self, other: mergeDistributions(other, self, operator.pow)    
    
    # TODO: other of non-scalar type?
    __gt__ = lambda self, other: self.values > (other if not isinstance(other, stochasticDistribution) else other.values)
    __ge__ = lambda self, other: self.values >= (other if not isinstance(other, stochasticDistribution) else other.values)
    __lt__ = lambda self, other: self.values < (other if not isinstance(other, stochasticDistribution) else other.values)
    __le__ = lambda self, other: self.values <= (other if not isinstance(other, stochasticDistribution) else other.values)
    __eq__ = lambda self, other: self.values == other 
    
    
    def __xor__(self, other): raise FuncDesignerException('For function pow() use a**b, not a^b')
    __rxor__ = __xor__

    reduce = lambda self, N, inplace = True: reduce_distrib(self, N, inplace)
    
    toarray = lambda self: self
    
    mean = lambda self: self.Mean
    std = lambda self: self.Std
    var = lambda self: self.Var
    
    def __getattr__(self, attr):
        if attr == 'size':
            if 'values' not in self.__dict__:
                raise FuncDesignerException('this distribution is unquantified yet thus it has no size yet')
            self.size = self.values.size
            return self.size
        elif attr == 'values':
            raise FuncDesignerException('this distribution is unquantified yet thus it has no array of possible values yet')
        elif attr == 'probabilities':
            raise FuncDesignerException('this distribution is unquantified yet thus it has no array of probabilities yet')            
        elif attr == 'Mean':
            self.Mean = (self.values * self.probabilities).sum()
            return self.Mean
        elif attr == 'Std':
            self.Std = o.sqrt(self.Var, attachConstraints = False)
            return self.Std
        elif attr == 'Var':
            self.Var = o.abs(o.sum((self.values)**2 * self.probabilities) - self.Mean**2)
            return self.Var
        elif attr == 'cdf':
            self.cdf = cdf(self)
            return self.cdf
        elif attr == 'pdf':
            self.pdf = pdf(self)
            return self.pdf
        elif attr == 'A':
            return self
        elif attr == 'ndim':
            return 1
        elif attr == 'shape':
            return (self.size, )
        else:
            raise AttributeError('incorrect attribute "%s" of FuncDesigner stochastic class' % attr)
    
    def sort(self, *args, **kw):
        if self.isSorted: return self
        ind = np.argsort(self.values, *args, **kw)
        self.values = self.values[ind]
        self.probabilities = self.probabilities[ind]
        self.isSorted = True
        return self


class discrete(stochasticDistribution):
    def __init__(self, *args, **kw):
        stochasticDistribution.__init__(self, *args, **kw)
        self.distribType = 'discrete'
    
class continuous(stochasticDistribution):
    def __init__(self, *args, **kw):
        stochasticDistribution.__init__(self, *args, **kw)
        self.distribType = 'continuous'

class stochFunc:
    #_str = None
    def __init__(self, distrib):
        d = distrib
        if not d.quantified:
            print('''
            Warning! The involved stochastic distribution is not quantified yet, 
            quantiles ~= 1/1500, ..., 1499/1500 will be used''')
            d = d._yield_quantified(1500)
        self.distrib = d
        
    def engine(self):
        raise FuncDesignerException('virtual method stochFunc.engine has not been overloaded')
        

        
class cdf(stochFunc):
    _str = 'CDF'
    
    def plot(self):
        try:
            import pylab
        except:
            raise FuncDesignerException('to plot you should have matplotlib installed')
        self.distrib.sort()
        x, y = self.distrib.values, np.cumsum(self.distrib.probabilities)
        if self.distrib.distribType == 'continuous':
            pylab.plot(x, y)
        elif self.distrib.distribType == 'discrete':
            X = np.hstack((x[0], np.vstack((x, x)).T.flatten(), x[-1]))
            Y = np.hstack((0.0, y[0], np.vstack((y, y)).T.flatten()))
            pylab.plot(X, Y)
        else:
            pylab.scatter(x, y, s=1)
        x_l, x_u = x[0]-0.05*(x[-1]-x[0]), x[-1]+0.05*(x[-1]-x[0])
        pylab.xlim(x_l, x_u)
        pylab.ylim(-0.05, 1.05)
        pylab.plot([x_l, x_u], [0, 0], color='g', linewidth = 2)
        pylab.plot([x_l, x_u], [1, 1], color='g', linewidth = 2)
        pylab.title(self._str)
        pylab.grid('on')
        pylab.show()        

class pdf(stochFunc):
    _str = 'PDF'

    def plot(self):
        try:
            import pylab
        except:
            raise FuncDesignerException('to plot you should have matplotlib installed')
        if self.distrib.distribType != 'continuous':
            raise FuncDesignerException('you can use pdf for continuous distribution only')
        
        # Temporary, to omit same values or very close to zero division effects
        # TODO: rework it
        d2 = self.distrib.reduce(self.distrib.size-1, inplace = False)
        d2.sort()
        vals, probs = d2.values, d2.probabilities
        cp = np.cumsum(probs)
        d_right =  (cp[1:] - cp[:-1]) / (vals[1:]-vals[:-1])
        d = np.hstack((d_right[0], 0.5*(d_right[1:] + d_right[:-1]), (cp[-1] - cp[-2]) / (vals[-1]-vals[-2])))
        x, y = vals, d
        pylab.plot(x, y)
        x_l, x_u = x[0]-0.05*(x[-1]-x[0]), x[-1]+0.05*(x[-1]-x[0])
        pylab.xlim(x_l, x_u)
        My, my = np.max(y), np.min(y)
        d_y = My - my
        pylab.ylim(-0.05 * d_y, My + 0.05*d_y)
        pylab.plot([x_l, x_u], [0, 0], color='g', linewidth = 2)
        pylab.title(self._str)
        pylab.grid('on')
        pylab.show()   

def gauss(m = 0.0, sigma = 1.0, N = None, quantiles = None):
    # Gauss (normal) distribution
    # similar usage to scipy.stats.norm(location, scale)
    from scipy.stats import norm
    ppf_engine = norm(m, sigma).ppf
    r = continuous(ppf = ppf_engine, quantiles = quantiles, N = N, 
                   Str = 'gauss (normal) distribution with m = %g and sigma = %g' % (m, sigma))
#    r.Mean = m
#    r.Var = sigma**2
#    r.Std = sigma
    return r
    
norm = normal = gauss
    
def exponential(location = 0.0, scale = 1.0, N = None, quantiles = None):
    # Exponential distribution
    # similar usage to scipy.stats.expon(loc, scale)
    # The scale parameter is equal to scale = 1.0 / lambda
    # see http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html
    from scipy.stats import expon
    ppf_engine = expon(location, scale).ppf
    return continuous(ppf = ppf_engine, quantiles = quantiles, N = N, Str = 'exponential distribution with location = %g and scale = %g' % (location, scale))

expon = exponential

def uniform(location = 0.0, scale = 1.0, N = None, quantiles = None):
    # Uniform distribution
    # similar usage to scipy.stats.uniform(from, to)
    from scipy.stats import uniform
    ppf_engine = uniform(location, scale).ppf
    r = continuous(ppf = ppf_engine, quantiles = quantiles, N = N, Str = 'uniform distribution with location = %g and scale = %g' % (location, scale))
#    r.Mean = 0.5*(location + scale)
#    r.Var = 
    return r

def mergeDistributions(d1, d2, operation):
    #assert isinstance(d1, stochasticDistribution), 'unimplemented yet'
    is_d1_stoch = isinstance(d1, stochasticDistribution)
    is_d2_stoch = isinstance(d2, stochasticDistribution)
    
    if is_d1_stoch and type(d2) == multiarray:
        #return np.array([mergeDistributions(d1, elem, operation) for elem in np.atleast_1d(d2)]).view(multiarray)
        return np.array([mergeDistributions(d1, elem, operation) for elem in \
                         (d2 if d2.ndim > 1 else d2.reshape(-1, 1)).view(np.ndarray)]).view(multiarray)
    
    if is_d2_stoch and type(d1) == multiarray:
        #return np.array([mergeDistributions(elem, d2, operation) for elem in np.atleast_1d(d1)]).view(multiarray)
        return np.array([mergeDistributions(elem, d2, operation) for elem in \
                         (d1 if d1.ndim > 1 else d1.reshape(-1, 1)).view(np.ndarray)]).view(multiarray)
        
    
    if is_d1_stoch and is_d2_stoch:
        if not hasattr(d1, 'stochDep') or not hasattr(d1, 'stochDep'):
            distrib_err_fcn()
    
    cond_same_stoch = is_d2_stoch and is_d1_stoch and set(d1.stochDep.keys()) == set(d2.stochDep.keys())
    if not is_d1_stoch or not is_d2_stoch or cond_same_stoch:
        if not is_d2_stoch: # thus d1 is stoch
            d2 = np.asfarray(d2) if operation == operator.truediv \
            or (hasattr(operator, 'div')  and operation == operator.div) and not isinstance(d2, ooarray) else np.asanyarray(d2)
            #assert d2.size == 1, 'unimplemented for size > 1 yet'
            vals2 = d2.reshape(1, -1) if d2.size > 1 else d2
            vals1 = d1.values
            distribType = d1.distribType
        elif not is_d1_stoch: # thus d2 is stoch
            d1 = np.asfarray(d1) if operation == operator.truediv \
            or (hasattr(operator, 'div')  and operation == operator.div) and not isinstance(d1, ooarray) else np.asanyarray(d1)
            assert d1.size == 1, 'unimplemented for size > 1 yet'
            vals1 = d1.reshape(1, -1) if d1.size > 1 else d1
            vals2 = d2.values
            distribType = d2.distribType
        else:#cond_same_stoch
            vals1 = d1.values
            vals2 = d2.values
            distribType = d1.distribType if d1.distribType == d2.distribType else 'undefined'
            
        Vals = operation(vals1, vals2) 
        
        r = stochasticDistribution(Vals.flatten(), 
                                 d1.probabilities.copy() if is_d1_stoch else d2.probabilities.copy(), 
                                 distribType)
        if is_d1_stoch and is_d2_stoch:
            r.stochDep = d1.stochDep.copy()
            for key, val in d2.stochDep.items():
                if key in r.stochDep:
                    r.stochDep[key] += val
                else:
                    r.stochDep[key] = val
        elif is_d1_stoch:
            r.stochDep = d1.stochDep.copy()
        else:
            if not is_d2_stoch: raise FuncDesignerException('bug in FuncDesigner kernel')
            r.stochDep = d2.stochDep.copy()
        #!!!!!!!!!!!! TODO: getOrder (for linear probs)
        
    else:
        f = lambda D1, D2:\
            operation(
                          D1.reshape(-1, 1), 
                          D2 if operation != operator.truediv \
                          or isinstance(D2, (oofun, ooarray)) \
                          or isinstance(D1, (oofun, ooarray))  \
                          else np.asfarray(D2) \
                          ).reshape(1, -1)

        distribType = d1.distribType if d1.distribType == d2.distribType else 'undefined'
        F = f(d1.values, d2.values)
        
        if np.all(d1.probabilities == d1.probabilities[0]) and np.all(d2.probabilities == d2.probabilities[0]):
            Probabilities = np.empty(d1.probabilities.size*d2.probabilities.size)
            Probabilities.fill(d1.probabilities[0] * d2.probabilities[0])
        else:
            Probabilities = (d1.probabilities.reshape(-1, 1) * d2.probabilities.reshape(1, -1)).flatten()
        
        r = stochasticDistribution(F.flatten(), Probabilities, distribType)
        
        '''                                                     adjust stochDep                                                     '''
        if len(set(d1.stochDep.keys()) & set(d2.stochDep.keys())) != 0 and len(set(d1.stochDep.keys()) | set(d2.stochDep.keys())) > 1:
#            print(d1.stochDep.keys())
#            print(d2.stochDep.keys())
#            print(set(d1.stochDep.keys()) | set(d2.stochDep.keys()))
            raise FuncDesignerException('''
            This stochastic function has structure that makes it impossible to handle in OpenOpt Suite yet.
            If gradient-based solver is involved, sometimes using derivative-free one instead (e.g. scipy_cobyla, de, bobyqa) can be successful
            ''')
        stochDep = d1.stochDep.copy()
        for key, val in d2.stochDep.items():
            if key in stochDep:
                stochDep[key] += val
            else:
                stochDep[key] = val
        r.stochDep = stochDep
        
    if is_d1_stoch:
        m1 = getattr(d1, 'maxDistributionSize', 0)
    else:
        m1 = 0
    if is_d2_stoch:
        m2 = getattr(d2, 'maxDistributionSize', 0)
    else:
        m2 = 0
    N = max((m1, m2))
    if N == 0:
        s = '''
            if one of function arguments is stochastic distribution 
            without resolving into quantified value 
            (e.g. uniform(-10,10) instead of uniform(-10,10, 100), 100 is number of point to emulate)
            then you should evaluate the function 
            onto oopoint with assigned parameter maxDistributionSize'''
        raise FuncDesignerException(s)
    r = r.reduce(N)
    r.maxDistributionSize = N

    if is_d1_stoch and hasattr(d1, '_p'):
        r._p = d1._p
    elif is_d2_stoch and hasattr(d2, '_p'):
        r._p = d2._p
        
#    if operation == operator.mul:
#        r._is_product = True
#        r._product_elements = [self, other]
    return r


def reduce_distrib(distrib, N, inplace = True):
    #assert inplace == True
    # !!!!!!! TODO: use or not use inplace (especially for parallel computations)?
    if len(distrib.values) <= N:
        return distrib.copy() if inplace == False else distrib
        
    distrib.sort()    
    values, probabilities = distrib.values, distrib.probabilities
    csp = np.cumsum(probabilities)
    new_probabilities = np.asarray([1.0/N]*N)
    

    tmp = np.linspace(1.0/N, 1, N) 
    Ind = np.searchsorted(csp, tmp)
    Ind[Ind == -1] = 0
    Ind[Ind == values.size] = values.size-1
    Ind[Ind == values.size-1] = values.size-2
    
    # TODO: rework it as linear 1st order approximation
    Case = 0
    if Case == 1:
        new_values = values[Ind] 
    else:
        # TODO: use arange instead
        new_csp = np.cumsum(new_probabilities)
        
        v_l = values[Ind] 
        Ind2 = Ind + 1
        
        v_u = values[Ind2] 
        #new_values = ((csp[Ind2] - new_csp)*v_l + (csp[Ind] - new_csp)*v_u) / (csp[Ind2]-csp[Ind])
        new_values = v_l + (new_csp - csp[Ind])*(v_u-v_l) / (csp[Ind2]-csp[Ind])
    if inplace:
        distrib.values, distrib.probabilities = new_values, new_probabilities
        return distrib
    else:
        return stochasticDistribution(new_values, new_probabilities)._update(distrib)




def f_quantile(distrib, val, interpolate):
    # returns probability of event X <= val
    if isinstance(distrib, multiarray) or (isinstance(distrib, ndarray) and isinstance(distrib.flat[0], stochasticDistribution)):
        x = (distrib.reshape(-1, 1) if distrib.ndim < 2 else distrib).view(np.ndarray)
        if type(x[0]) == np.ndarray and x[0].size == 1:
            r = np.array([f_quantile(xx.item(), val, interpolate) for xx in x])#.view(multiarray)
        else:
            r = np.array([f_quantile(xx, val, interpolate) for xx in x])#.view(multiarray)
        r = r.reshape(distrib.shape).view(multiarray)
        return r#.view(multiarray)
        
        #return np.array([f_quantile(elem, val, interpolate) for elem in distrib.view(np.ndarray)]).view(multiarray)

    if not isinstance(distrib, stochasticDistribution):
        return 0.5*(np.asarray(distrib <= val, int)+1)
        #return 1.0 if distrib <= val else 0.0
    distrib.sort()
    vals = distrib.values
    if vals[-1] <= val: 
        return 1.0
    
    if interpolate not in (True, False) and distrib.distribType == 'undefined' and f_quantile.interpolate_w is False:
        print('''
        WARNING : you should provide parameter "interpolate" = True / False 
        into function P() for mixed discrete-continuous distributions; currently True will be used;
        for False only global solvers (http://openopt.org/GLP) are suitable
        ''')
        f_quantile.interpolate_w = True
    
    if vals[0] > val or (vals[0] == val and (interpolate is not False or distrib.distribType == 'continuous')): 
        return 0.0
        
    p = distrib.probabilities
    
    if distrib.distribType == 'discrete' and vals[0] == val:
        return p[0]
        
    ind = np.searchsorted(vals, val)
    if ind == -1: ind = 0
    
    r = p[:ind].sum()
    
    if (interpolate is not False or distrib.distribType == 'continuous') and ind < p.size - 1 and vals[ind+1] != vals[ind]:
        r += p[ind+1] * (vals[ind+1] - val) / (vals[ind+1] - vals[ind]) 
    
    return r
    
f_quantile.interpolate_w = False

def d_quantile(distrib, val, interpolate):

    # returns derivative of probability of event X <= val
    assert not isinstance(distrib, multiarray), 'd_quantile is not unimplemented for multiarrays yet'

#    assert isinstance(distrib, stochasticDistribution), 'd_quantile works for stochasticDistribution input only'
        #return 1.0 if distrib <= val else 0.0
    if not isinstance(distrib, stochasticDistribution):
        return 0.0
    
    distrib.sort()
    vals = distrib.values
    p = distrib.probabilities
    if vals[-1] <= val: 
        return 0.0

    if interpolate not in (True, False) and distrib.distribType == 'undefined' and f_quantile.interpolate_w is False:
        print('''
        WARNING : you should provide parameter "interpolate" = True / False 
        into function P() for mixed discrete-continuous distributions; currently True will be used;
        for False only global solvers (http://openopt.org/GLP) are suitable
        ''')
        f_quantile.interpolate_w = True
    
    if vals[0] > val or (vals[0] == val and (interpolate is not False or distrib.distribType == 'continuous')): 
        return 0.0
    

    if distrib.distribType == 'discrete':
        assert interpolate is not False, 'gradient-based solvers are inappropriate when parameter "interpolate" in P() set to False'
        if vals[0] == val:
            return 0.0
        
    ind = np.searchsorted(vals, val)
    if ind == -1: ind = 0
    
    # TODO: mb rework for derivatives to be smooth 
    r = -p[ind+1] / (vals[ind+1] - vals[ind]) 

    return r

def P(c, interpolate = 'auto'):
    if interpolate not in (True, False, 'auto'):
        raise FuncDesignerException("in P() parameter interpolate must be True, False or 'auto'")
    
    if c is True: return 1.0
    elif c is False: return 0.0
    
    if not isinstance(c, BaseFDConstraint):
        raise FuncDesignerException('arg of FuncDesigner.P() must be True, False or FuncDesigner constraint')
        
    if (type(c.ub) == np.ndarray and c.ub.size != 1) or (type(c.lb) == np.ndarray and c.lb.size != 1):
        raise FuncDesignerException('stochastic constraints are unimplemented for vectorized API yet')
        
    if np.isfinite(c.ub) and c.lb == -np.inf:
        r = oofun(lambda x: f_quantile(x, c.ub, interpolate), c.oofun, 
                  d = lambda x: d_quantile(x, c.ub, interpolate), engine_monotonity = -1, vectorized = True)
    elif np.isfinite(c.lb) and c.ub == np.inf:
        r = oofun(lambda x: 1.0 - f_quantile(x, c.lb, interpolate), c.oofun, 
                  d = lambda x: -d_quantile(x, c.lb, interpolate), engine_monotonity = 1, vectorized = True)
    else:
        raise FuncDesignerException('stochastic constraints are implemented for case xor(isfinite(lb),isfinite(ub)) only for now')
    r.engine = 'P'
    return r

def f_mean(x):
    if isinstance(x, multiarray):
        x = (x.reshape(-1, 1) if x.ndim < 2 else x).view(np.ndarray)
        if type(x[0]) == np.ndarray and x[0].size == 1:
            r = np.array([mean(xx.item()) for xx in x]).view(multiarray)
        else:
            r = np.array([mean(xx) for xx in x]).view(multiarray)
    elif not isinstance(x, stochasticDistribution):
        r = x
    else:
        r = x.Mean
    return r

is_prod_scalar = lambda arg: arg._isProd and (np.isscalar(arg._prod_elements[-1])\
    or (isinstance(arg._prod_elements[-1], ndarray) and not isinstance(arg._prod_elements[-1], OOArray)))

def mean(arg, *args, **kw):
    if isinstance(arg, stochasticDistribution):
        if not len(args) == len(kw) == 0:
            raise FuncDesignerException('incorrect usage of FuncDesigner mean() - it cannot handle additional arguments yet')
        r =  arg.Mean
    elif isinstance(arg, oofun):
        if not len(args) == len(kw) == 0:
            raise FuncDesignerException('incorrect usage of FuncDesigner mean() - it cannot handle additional arguments yet')
        if arg._isSum:
            r = o.sum([mean(elem) for elem in arg._summation_elements])
        elif is_prod_scalar(arg):
            # TODO: rework it when np.prod(objects) will be fixed
            multiplier, tmp = arg._fixed_part, arg._unfixed_part
            return multiplier * mean(tmp)
#        elif arg._isProd:
#            tmp = [elem for elem in arg._prod_elements if isinstance(elem, oofun) and elem.hasStochasticVariables]
        else:
#            def ff(x):
#                # TODO: same changes for std, var,other moments
#                #print (type(x), multiarray)
#                r =  np.array([mean(xx) for xx in x.view(np.ndarray)]).view(multiarray) if isinstance(x, multiarray) \
#                    else x if not isinstance(x, stochasticDistribution) else x.Mean
#                #if type(x) == np.ndarray:
##                print ('!', x, r.shape)
#                return r
            r = oofun(f_mean, arg, engine = 'mean', engine_monotonity = 0, vectorized = True)
            r.getOrder = arg.getOrder
#            r = oofun(lambda x: np.array([mean(xx) for xx in (x.reshape(-1, 1) if x.ndim < 2 else x).view(np.ndarray)]).view(multiarray)  if isinstance(x, multiarray) \
#            else x if not isinstance(x, stochasticDistribution) else x.Mean, arg)
            # TODO: move _D definition outside of the func
            def _D(*args, **kw):
                res = arg._D(*args, **kw)
                res = dict((key, elem.Mean if isinstance(elem, stochasticDistribution) else elem) for key, elem in res.items())
                return res
            r._D = _D
    else:
        r = np.mean(arg, *args, **kw)
    return r

def f_std(x):
    if isinstance(x, multiarray):
        x = (x.reshape(-1, 1) if x.ndim < 2 else x).view(np.ndarray)
        if type(x[0]) == np.ndarray and x[0].size == 1:
            r = np.array([std(xx.item()) for xx in x]).view(multiarray)
        else:
            r = np.array([std(xx) for xx in x]).view(multiarray)
    elif not isinstance(x, stochasticDistribution):
        r = np.std(x)
    else:
        r = x.Std
    return r

# TODO: std and var derivatives

def std(arg, *args, **kw):
    if isinstance(arg, stochasticDistribution):
        if not len(args) == len(kw) == 0:
            raise FuncDesignerException('incorrect usage of FuncDesigner std() - it cannot handle additional arguments yet')
        r = arg.Std
    elif isinstance(arg, oofun):
        if not len(args) == len(kw) == 0:
            raise FuncDesignerException('incorrect usage of FuncDesigner std() - it cannot handle additional arguments yet')
        #r = oofun(lambda x: np.array([std(X[i]) for i in range() in (x.reshape(-1, 1) if x.ndim < 2 else x).view(np.ndarray)]).view(multiarray)  if isinstance(x, multiarray)\
        if is_prod_scalar(arg):
            multiplier, tmp = arg._fixed_part, arg._unfixed_part
            return abs(multiplier) * std(tmp)
        
        r = oofun(f_std, arg, engine = 'std', vectorized = True)
    else:
        r = np.std(arg, *args, **kw)
    return r

    
def f_var(x):
    if isinstance(x, multiarray):
        x = (x.reshape(-1, 1) if x.ndim < 2 else x).view(np.ndarray)
        if type(x[0]) == np.ndarray and x[0].size == 1:
            r = np.array([var(xx.item()) for xx in x]).view(multiarray)
        else:
            r = np.array([var(xx) for xx in x]).view(multiarray)
    elif not isinstance(x, stochasticDistribution):
        r = np.var(x)
    else:
        r = x.Var
    return r

def var(arg, *args, **kw):
    if isinstance(arg, stochasticDistribution):
        if not len(args) == len(kw) == 0:
            raise FuncDesignerException('incorrect usage of FuncDesigner var() - it cannot handle additional arguments yet')
        r = arg.Var
    elif isinstance(arg, oofun):
        if not len(args) == len(kw) == 0:
            raise FuncDesignerException('incorrect usage of FuncDesigner var() - it cannot handle additional arguments yet')
        if is_prod_scalar(arg):
            multiplier, tmp = arg._fixed_part, arg._unfixed_part
            return multiplier**2 * var(tmp)
        
        #r = oofun(lambda x: np.array([var(xx) for xx in x.view(np.ndarray)]).view(multiarray)  if isinstance(x, multiarray)\
        r = oofun(f_var, arg, engine = 'var', vectorized = True)
    else:
        r = np.var(var, *args, **kw)
    return r
