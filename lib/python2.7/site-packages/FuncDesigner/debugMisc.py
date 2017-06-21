# created by Dmitrey
import inspect
from baseClasses import OOArray
from numpy import isscalar

def print_info(oof):
    Str = '-'*15 + ' FuncDesigner info on initialization of object with id %d ' % oof._id + '-'*15 
    print('\n'+Str)
    print('type: %s' % type(oof))
    if isinstance(oof, OOArray):
        print('ooarray %s' % oof.name)
        if not oof._is_array_of_oovars:
            print('ooarray expression: %s' % oof.name)
    else: # oofun, mb oovar
        if oof.is_oovar:
            print('oovar %s' % oof.name)
        else:
            print('oofun %s' % oof.name)
            print('oofun expression: %s' % oof.expr)
    print('Stack info:')
    for frame_tuple in inspect.stack()[2:]:
        # minor optimization for Eric Python IDE
        if 'dist-packages' in frame_tuple[1] and 'eric'in frame_tuple[1]:
            break
        print('%s, line %d, in %s' % frame_tuple[1:4])
        if frame_tuple[4] is not None:
            for elem in frame_tuple[4]:
                print('\t%s' % elem)
    print('_'*len(Str))

class FD_objects(dict):
    wasCleared = False
    def __setitem__(self, key, val):
        maxObjectsNum = fd_trace_id.maxObjectsNum
        if len(self) > maxObjectsNum:
            self.clear()
            self.wasCleared = True
        dict.__setitem__(self, key, val)
#    set = __setitem__
    def __getitem__(self, key):
        r = dict.get(self, key, None)
        if r is None:
            if self.wasCleared:
                maxObjectsNum = fd_trace_id.maxObjectsNum
                print('''
                The object by the id hasn't been found, probably because of
                FD objects tracing has been cleared due to maxObjectsNum exceed,
                use fd_trace_id.maxObjectsNum = new_val for a value bigger 
                than the current (%d)
                ''' % maxObjectsNum)
            print("FuncDesigner object with this id (%d) doesn't exist" % key)
        return r

class FD_trace_id:
    object = objects = FD_objects()
    maxObjectsNum = 1500000
    traced_id = -15
    def __init__(self):
        pass
    def __call__(self, *args, **kw):
        assert len(kw) == 0 and len(args) == 1
        assert isscalar(args[0])
        self.traced_id = args[0]
    traces = lambda self, val: val == self.traced_id

fd_trace_id = FD_trace_id()

