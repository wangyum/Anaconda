class OpenOptException(BaseException):
    def __init__(self,  msg):
        self.msg = msg
    def __str__(self):
        return self.msg
        #pass

#def ooassert(cond, msg):
#    assert cond, msg

def oowarn(msg):
    s = oowarn.s + msg
    print(s)
    return s
oowarn.s = 'OpenOpt Warning: '

errSet = set()
def ooerr(msg):
    s = ooerr.s + msg
    if msg not in errSet:
        print(s)
    errSet.add(msg)
    raise OpenOptException(msg)
ooerr.s = 'OpenOpt Error: '
ooerr.set = errSet

pwSet = set()
def ooPWarn(msg):
    if msg in pwSet: return ''
    pwSet.add(msg)
    oowarn(msg)
    return msg
ooPWarn.s = 'OpenOpt Warning: '
ooPWarn.set = pwSet
    
def ooinfo(msg):
    s = ooinfo.s + msg
    print(s)
    return s
ooinfo.s = 'OpenOpt info: '

def oohint(msg):
    s = oohint.s + msg
    print(s)
    return s
oohint.s = 'OpenOpt hint: '

def oodisp(msg):
    print(msg)
    return msg
oodisp.s = ''


def oodebugmsg(p,  msg):
    if p.debug: 
        print('OpenOpt debug msg: %s' % msg)
        return msg
    return ''
