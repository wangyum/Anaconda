#created by Dmitrey

#from numpy import ndarray
#from time import strftime
from threading import Thread
from openopt import __version__ as ooversion
from setDefaultIterFuncs import BUTTON_ENOUGH_HAS_BEEN_PRESSED, USER_DEMAND_EXIT
from ooMisc import killThread
import platform#, pylab

TkinterIsInstalled = True# sometimes Tkinter is not installed
if platform.python_version()[0] == '2': # Python2
    try:
        from Tkinter import Tk, Text, Toplevel, Button, Entry, Menubutton, Label, Frame, \
        StringVar, DISABLED, ACTIVE, Scrollbar
    except:
        TkinterIsInstalled = False
else: # Python3
    try:
        from tkinter import Tk, Text, Toplevel, Button, Entry, Menubutton, Label, Frame, \
        StringVar, DISABLED, ACTIVE, Scrollbar
    except:
        TkinterIsInstalled = False

def manage(p, *args, **kwargs):

    if not TkinterIsInstalled: 
        p.err('''
        Tkinter is not installed. 
        If you have Linux you could try using "apt-get install python-tk"
        ''')
        
    p.__dict__['_immutable'] = False
    bg_color = p._bg_color
    p.isManagerUsed = True
    
    # expected args are (solver, start) or (start, solver) or one of them
    p._args = args
    p._kwargs = kwargs
    

    for arg in args:
        if type(arg) == str or hasattr(arg, '__name__'): 
            p.solver = arg
        elif arg in (0, 1, True, False): 
            start = arg
        else: 
            p.err('Incorrect argument for manage()')

    start = kwargs.pop('start', True)

    if 'solver' in kwargs: 
        p.solver = kwargs['solver']

    # root

    root = Tk()
    p.GUI_root = root
    p.GUI_items = {'root':root}

    '''                                     F0, F_side                                  '''
    useGrid = False
    if useGrid:
        F_side = Frame(root)#, width=30)
        F_side.grid(row=0, column=0, padx=2, pady=2)#, sticky=N+S+E)
        F0 = Frame(root)
        F0.grid(row=0, column=1, padx=2, pady=2)#, sticky=N+S+W)
        F0.pack = F0.grid
        F_side.pack = F_side.grid
        F0.pack_forget = F0.grid_remove
        F_side.pack_forget = F_side.grid_remove
    else:
        F0 = Frame(root)#, width=30)
        F_side = Frame(root)
    F0_side = 'right'
    textSide = 'left'
    p.GUI_items['F0'] = F0
    p.GUI_items['F_side'] = F_side
    

    '''                                  F_log, F_result                               '''
    F_log = Frame(F_side)
    F_log.isVisible = False
    p.GUI_items['F_log'] = F_log
    
    F_result = Frame(F_side)
    p.GUI_items['F_result'] = F_result
    F_result.pack(fill='both', expand=True)
    F_result.pack_forget()
    F_result.isVisible = False
    F_result.made = False
    
    
    scrollbar = Scrollbar(F_log)
    scrollbar.pack(side='right', fill='y')
    textOutput = Text(F_log, yscrollcommand=scrollbar.set, bg=bg_color)
    scrollbar.config(command=textOutput.yview)
    
    p._setTextFuncs()
    for func in ('warn', 'err', 'info', 'disp', 'hint', 'pWarn'):
        setattr(p, func, updated_output(getattr(p, func), textOutput))
    
#    if p.managerTextOutput is not False and p.managerTextOutput in ('right', 'left'):
#        textSide = p.managerTextOutput
#        if p.managerTextOutput == 'right': 
#            F0_side = 'left'
    
    textOutput.pack(expand=True, fill='both')
    F_log.isVisible = True
    if p.managerTextOutput is False:
        F_side.pack_forget()
        F_side.isVisible = False
        F_log.isVisible = False

    F_log.pack(fill='both', expand=True)
    
    if not useGrid:
        F_side.pack(side=textSide, fill='both', expand=True)
        F0.pack(side=F0_side, fill='both', expand=True)
        
    F_side.isVisible = True
    F_side.isSideWidget = True
    F_side._root = root
    
    
    """                                               Title                                                """
    #root.wm_title('OpenOpt  ' + ooversion)
    

    """                                              Buttons                                               """

    '''                              Label                          '''
    ButtonsColumn = Frame(F0)
#    F_side._pack_forget = F_side.pack_forget
#    F_side.pack_forget = lambda : f_side_pack_forget(F_side, root, ButtonsColumn)
    ButtonsColumn.pack(ipady=4, expand=True)
    
    Label(ButtonsColumn, text=' OpenOpt ' + ooversion + ' ').pack(expand=True, fill='x')
    Label(ButtonsColumn, text=' Solver: ' + (p.solver if isinstance(p.solver, str) else p.solver.__name__) + ' ').pack(expand=True, fill='x')
    Label(ButtonsColumn, text=' Problem: ' + p.name + ' ').pack(expand=True, fill='x')
    p.GUI_items['ButtonsColumn'] = ButtonsColumn
    
    #TODO: mb use Menubutton 

    #Statistics
#    stat = StringVar()
#    stat.set('')
#    Statistics = Button(ButtonsColumn, textvariable = stat, command = lambda: invokeStatistics(p))

#    cw = Entry(ButtonsColumn)
#
#    
#    b = Button(ButtonsColumn, text = 'Evaluate!', command = lambda: invokeCommand(cw))
#    cw.pack(fill='x'', side='left')
#    b.pack(side='right')
        
    '''                              Run                          '''
    
    t = StringVar()
    t.set("      Run      ")
    RunPause = Button(ButtonsColumn, textvariable = t, command = lambda: invokeRunPause(p))
    RunPause.pack(ipady=15, expand=True, fill='x', pady=8)
    p.GUI_items['RunPause'] = RunPause
    p.statusTextVariable = t


    '''                              Log                          '''
        
    Log = Button(ButtonsColumn, text = '    Log    ', command = lambda:invokeLog(p))
    Log.pack(expand=True, fill='x', pady=8, ipady=5)
    p.GUI_items['Log'] = Log

    '''                             Result                         '''
    
    Result = Button(ButtonsColumn, text = '   Result   ', command = lambda: invokeResult(p))
    Result.config(state=DISABLED)
    # TODO: MOP
    if p.probType in ('NLP', 'SNLE', 'NLSP', 'GLP', 'LP', #'MOP',
    'MILP', 'NSP', 'MINLP', 'LLSP', 'SLE', 'TSP', 'SOCP', 'SDP') \
    or p.probType.endswith('QP'):
        Result.pack(expand=True, fill='x', pady=8, ipady=5)
    p.GUI_items['Result'] = Result

    '''                             Enough                         '''

    Enough = Button(ButtonsColumn, text = '   Enough!   ', 
                    command = lambda: invokeEnough(p))
    Enough.config(state=DISABLED)
    Enough.pack(expand=True, fill='x', pady=8, ipady=5)
    p.GUI_items['Enough'] = Enough


    '''                             Exit                         '''

    Quit = Button(ButtonsColumn, text="      Exit      ", command = lambda:invokeExit(p))
    Quit.pack(ipady=15, expand=True, fill='x', pady=8)
    p.GUI_items['Quit'] = Quit
    
    
    for w in (Quit, Enough, Result, Log, RunPause):
        w.config(borderwidth=2)
    
    '''                             Time                         '''
    Frame(ButtonsColumn).pack(ipady=0, expand=True, fill='x')
    F = Frame(ButtonsColumn)
    _time = StringVar()
    p._manager_time = 0
    p._manager_time_variable = _time
    Label(F, text=" Time:\t\t").pack(side='left', expand=True, fill='x')
    _time.set("%d" % p._manager_time)
    _Time = Label(F, textvariable = _time)
    _Time.pack(side='right', ipady=1, ipadx=3, padx=3, expand=True, fill='x')
    p.GUI_items['time'] = _time
    F.pack(ipady=1, ipadx=3, padx=3, expand=True, fill='x')
    p.GUI_items['TimeFrame'] = F
    
    '''                         CPU Time                         '''
    Frame(ButtonsColumn).pack(ipady=0, expand=True, fill='x')
    F = Frame(ButtonsColumn)
    _cputime = StringVar()
    p._manager_cputime = 0
    _cputime.set(p._manager_cputime)
    p._manager_cputime_variable = _cputime
    Label(F, text=" CPU Time:\t").pack(side='left', expand=True, fill='x')
    _time.set("%d" % p._manager_cputime)
    _CPUTime = Label(F, textvariable = _cputime)
    _CPUTime.pack(side='right', ipady=1, ipadx=3, padx=3, expand=True, fill='x')
    p.GUI_items['cputime'] = _cputime
    F.pack(ipady=1, ipadx=3, padx=3, expand=True, fill='x')
    p.GUI_items['CPUTimeFrame'] = F


    """                                            Start main loop                                      """
    #state = 'paused'

    if start:
        Thread(target=invokeRunPause, args=(p, )).start()
    root.mainloop()
    #finalShow(p)


    """                                              Handle result                                       """

    if hasattr(p, 'tmp_result'):
        r = p.tmp_result
        delattr(p, 'tmp_result')
    else:
        r = None


    """                                                    Return                                           """
    return r
    
########################################################
########################################################
########################################################

def invokeRunPause(p, isEnough=False):
    try:
        import pylab
    except:
        if p.plot: 
            p.warn('to use graphics you should have matplotlib installed')
            p.plot = False
        
    if isEnough:
        p.GUI_items['RunPause'].config(state=DISABLED)

    if p.state == 'init':
        p.probThread = Thread(target=doCalculations, args=(p, ))
        p.state = 'running'
        p.statusTextVariable.set('    Pause    ')
        p.GUI_items['Enough'].config(state='normal')
        p.GUI_root.update_idletasks()
        p.probThread.start()

    elif p.state == 'running':
        p.state = 'paused'
        if p.plot: 
            pylab.ioff()
        p.statusTextVariable.set('      Run      ')
        p.GUI_root.update_idletasks()

    elif p.state == 'paused':
        p.state = 'running'
        if p.plot:
            pylab.ion()
        p.statusTextVariable.set('    Pause    ')
        p.GUI_root.update_idletasks()
        
########################################################
def doCalculations(p):
    p._immutable = False
    try:
        p.__dict__['tmp_result'] = p.solve(*p._args, **p._kwargs)
    except killThread:
        if p.plot and hasattr(p, 'figure'):
            #p.figure.canvas.draw_drawable = lambda: None
            try:
                import pylab
                pylab.ioff()
                pylab.close('all')
            except:
                pass
#    p._immutable = True
#    p.GUI_items['Result'].config(state='active')
    
    p.GUI_items['Result'].config(state='normal')
    p.GUI_items['RunPause'].config(state=DISABLED)
    p.GUI_items['Enough'].config(state=DISABLED)
    p.GUI_root.update_idletasks()
#    p.GUI_items['F0'].config(bg = 'PaleGreen')
#    p.GUI_items['F0'].config(bg = '#98FB98')
#    p.GUI_items['Result'].config(bg = '#98FB98')
#    p.GUI_items['ButtonsColumn'].config(bg = '#98FB98')
    
    # TODO: use colors as pylab plot final markers 
    color = 'red' if p.__dict__['tmp_result'] is None or p.stopcase < 0 \
    else 'LemonChiffon' if p.stopcase > 0 \
    else 'DarkBlue'
    
    W = ['ButtonsColumn', 'CPUTimeFrame', 'TimeFrame']
    L = [p.GUI_items[_w] for _w in W]
    for _w in W:
        L += p.GUI_items[_w].children.values()
    for w in L:
        if w.winfo_class() != 'Button':
            w.config(bg = color)
        
#    p.GUI_items['ButtonsColumn'].config(fg = '#98FB98')
    p.GUI_root.update_idletasks()
    
#    
        

########################################################
#def invokeStatistics(p):
def invokeCommand(cw):
    exec(cw.get())
    
########################################################
def updated_output(func, textOutput):
    def func2(msg):
        msgCap = func.s 
        Set = getattr(func, 'set', ())
        if msg in Set:
            return
        if msgCap == 'OpenOpt Error: ': #if type(Set) != tuple:
            textOutput.tag_config(msg, foreground="red")
            textOutput.config(foreground="red")
        textOutput.insert('end', msgCap + msg + '\n')
        textOutput.yview('end')
        func(msg)
    return func2
    
########################################################
def invokeResult(p):
    res = w = p.GUI_items['F_result']
    log = p.GUI_items['F_log']
    side = p.GUI_items['F_side']
    
#    p.disp('%s %s' % (side.isVisible, res.isVisible))
    r = p.tmp_result
    
    r._tkview(w)
        
    if side.isVisible:
        if res.isVisible:
            withdraw(res, side, root=p.GUI_items['root'])
        else:
            restore(res)
    else:
        restore(side, res)
    withdraw(log)
    
########################################################
def invokeExit(p):
    p._immutable = False
    p.userStop = True
    p.istop = USER_DEMAND_EXIT
    if hasattr(p, 'stopdict'): 
        p.stopdict[USER_DEMAND_EXIT] = True

    # however, the message is currently unused
    # since openopt return r = None
    p.msg = 'user pressed Exit button'

    p.GUI_root.destroy()

########################################################
def invokeLog(p):
    log = p.GUI_items['F_log']
    res = p.GUI_items['F_result']
    side = p.GUI_items['F_side']
    
    withdraw(res)
    if side.isVisible:
        if log.isVisible:
            withdraw(side, root=p.GUI_items['root'])
        else:
            restore(log)
    else:
        restore(side, log)
        
########################################################
def invokeEnough(p):
    
    p.userStop = True
    p.istop = BUTTON_ENOUGH_HAS_BEEN_PRESSED
    if hasattr(p, 'stopdict'):  
        p.stopdict[BUTTON_ENOUGH_HAS_BEEN_PRESSED] = True
    p.msg = 'button Enough has been pressed'

    if p.state == 'paused':
        invokeRunPause(p, isEnough=True)
    else:
        p.GUI_items['RunPause'].config(state=DISABLED)
        p.GUI_items['Enough'].config(state=DISABLED)
        p.GUI_items['Quit'].config(state=DISABLED)
        

#TODO: simplify it
########################################################
def restore(*args):
    for w in args:
        status = w.isVisible
#        assert w.winfo_viewable() == w.isVisible
        if status is False:
            w.pack(fill='both', expand=True)
            isSideWidget = getattr(w, 'isSideWidget', False)
            if isSideWidget:
                tmp = w._root.geometry() 
                sizes, x, y = tmp.split('+')
                size_x, size_y = sizes.split('x')
                X, Y = w.xy_sizes
                w._root.geometry('%dx%d+%d+%d'%(X+int(size_x), Y, int(x)-X, int(y)))
            w.isVisible = True
    
        
########################################################
def withdraw(*args, **kw):
    for w in args:
        status = w.isVisible
#        assert w.winfo_viewable() == w.isVisible
        if status:
            isSideWidget = getattr(w, 'isSideWidget', False)
            if isSideWidget:
                root=kw['root']
                width = w.winfo_width()
                tmp = root.geometry() 
                sizes, x, y = tmp.split('+')
                size_x, size_y = sizes.split('x')
                w.xy_sizes = (w.winfo_width(), w.winfo_height())
                sizes = str(int(size_x)-width) + 'x' + size_y
                w.pack_forget()
                new = sizes + '+'+str(int(x)+width)+'+'+y
                root.geometry(new)
            else:
                w.pack_forget()
            w.isVisible = False
