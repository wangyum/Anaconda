

#real_property = property
#
#def property(func):
#    name = '_cache_' + func.__name__
#    def wrapper(self, *a, **kw):
#        if hasattr(self, name):
#            value = getattr(self, name) + 1
#        else:
#            value = 1
#        setattr(self, name, value)
#
#        if True:#value > 1:
#            with open('/tmp/log', 'a') as f:
#                f.write('accessed %r %i times\n' % (func.__name__, value))
#
#        return func(self, *a, **kw)
#
#    return real_property(wrapper)
