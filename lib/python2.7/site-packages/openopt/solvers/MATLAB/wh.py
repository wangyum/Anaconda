import numpy as np
try:
    from scipy.sparse import find, isspmatrix
except ImportError:
    isspmatrix = lambda *args, **kw: False


import socket, subprocess

#from time import sleep
TCP_IP = '127.0.0.1'
TCP_PORT = 5001

from os.path import abspath, dirname, normpath
path = dirname(abspath(__file__))

def wh(d, matlabExecutable):
    args = ['-nodesktop', 
                   '-r',  '"addpath %s ; OpenOpt_Proxy"' %normpath(path)
                   ]
    Matlab = matlabExecutable+' '+' '.join(args)
    subprocess.Popen(Matlab, shell=True)
    for k, v in d.items():
        exec(k + '=v')
#    is_sparse = False # to suppress Python3 issue
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    #print "waiting for connection"
    conn, addr = s.accept() # hangs until other end connects
    #print 'Connection address:', addr

    isPyPy = False

    CycleCond = True

    while CycleCond:
    #    print "waiting for message"
        cmd_class = conn.recv(10).strip()
    #    print "cmd_class: ",cmd_class
        if cmd_class in ('put', b'put'):
            name = conn.recv(10).strip()
#            if type(name) == bytes:
#                name = name.decode()
    #        print "name: ",name
            shape_str = conn.recv(30).strip()
    #        print "shape_str: ",shape_str
            shape = tuple(map(int,shape_str.split()))
            n_floats = np.prod(shape)
            targ_flat = np.zeros(n_floats,'float')        
            n_read = 0
            while n_read < n_floats:
                n_toread = min(128,n_floats-n_read)
                arr = np.fromstring(conn.recv(n_toread*8),dtype='>f8')
                targ_flat[n_read:n_read+n_toread] = arr
                n_read += n_toread
    #            print "%i/%i floats read"%(n_read,n_floats)        
    #        print('isPyPy1:', isPyPy)
            if isPyPy:
                targ = targ_flat.reshape(shape)#[::-1]).T
            else:
                targ = targ_flat.reshape(shape,order="F")
    #        print('targ:', targ)
    #        input()
    #        print "received array: ",targ
            exec("%s = targ"%name)
        elif cmd_class in ('exec', b'exec'):
            stmt = conn.recv(100).strip()
#            if type(stmt) == bytes:
#                stmt = stmt.decode()
    #        print "statment: ",stmt
            exec(stmt)
        elif cmd_class in ("get", b'get'):
            name = conn.recv(10).strip()
#            name_str = name.decode() if type(name) == bytes else name
                
    #        print "getting variable: ",name
            try:
#                print(name, type(name))
#                print(name == 'is_sparse')
#                print(type(is_sparse))

#                if name_str == 'is_sparse':
#                    src = is_sparse
#                else:
                exec("src = %s"%name)
            except NameError:
                exec("src = []")
#            except UnboundLocalError:
#                exec("src = []")
            src = np.atleast_2d(src)
            Str = "%30s"%str(src.shape).replace(")","]").replace("(","[")
#            print(Str)
            conn.send(Str)
            if isPyPy:
                src_str = src.astype('>f8').T.tostring()
            else:
                src_str = src.astype('>f8').tostring(order="F")
            n_floats = src.size
            n_sent = 0
            while n_sent < n_floats:
                n_tosend = min(1024,n_floats-n_sent)            
                conn.send(src_str[n_sent*8:(n_sent+n_tosend)*8])
                n_sent += n_tosend
    #            print "%i/%i floats sent"%(n_sent,n_tosend)  
        else:
            raise Exception("unrecognized command (cmd_class=%s)"%cmd_class)
