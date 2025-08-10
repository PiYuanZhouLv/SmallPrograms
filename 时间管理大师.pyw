from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import time
import datetime

start_time = None
start_time2= None
stop_time = None
stop_time2= None
is_running = False

__doc__ = '''时间管理大师——帮助文档

目录'''

root = Tk()
# print(dir(root))
root.title('时间管理大师')
main = ttk.Frame(root)
main.grid()
note = ttk.Notebook(main, width=800, height=400)
note.grid()

now_page = ttk.Frame(note)
ttk.Label(now_page, text='当前时间：', font='TkTextFont 30').grid(row=1, column=1, sticky=(N, E, W, S))
now_time = StringVar()
now_label = ttk.Label(now_page, textvariable=now_time, font='TkTextFont 100', justify='center', width=800)
now_label.grid(row=2, column=1)
def get_now_time():
    now_time.set(time.strftime(' %Y-%m-%d\n %H:%M:%S', time.localtime()))
    root.after(100, get_now_time)
root.after(1, get_now_time)
note.add(now_page, text='时间')

count_page = ttk.Frame(note)
h = StringVar()
h.set('00')
m = StringVar()
m.set('00')
s = StringVar()
s.set('00')
ms = StringVar()
ms.set('000')
ttk.Label(count_page, text='秒表1：', font='TkTextFont 20').grid(row=1, column=1)
ttk.Label(count_page, textvariable=h, font='TkTextFont 100').grid(row=2, column=1)
ttk.Label(count_page, text=':', font='TkTextFont 100').grid(row=2, column=2)
ttk.Label(count_page, textvariable=m, font='TkTextFont 100').grid(row=2, column=3)
ttk.Label(count_page, text=':', font='TkTextFont 100').grid(row=2, column=4)
ttk.Label(count_page, textvariable=s, font='TkTextFont 100').grid(row=2, column=5)
ttk.Label(count_page, text='.', font='TkTextFont 100').grid(row=2, column=6)
ttk.Label(count_page, textvariable=ms, font='TkTextFont 50').grid(row=2, column=7, sticky=(S, W))
def b_start(*args):
    global start_time, stop_time
    start['state'] = 'disabled'
    stop['state'] = 'normal'
    if not start_time:
        start_time = datetime.datetime(1, 1, 1).now()
    else:
        t = datetime.datetime(1, 1, 1).now()-stop_time
        start_time = start_time + t
    root.after(1, starts)
def starts():
    global s, m, h, ms, sv, mv, hv, msv, after_num
    now_time = datetime.datetime(1, 1, 1).now()
    msv = now_time.microsecond-start_time.microsecond
    sv = now_time.second-start_time.second
    mv = now_time.minute-start_time.minute
    hv = now_time.hour-start_time.hour
    if msv<0:
        sv -= 1
        msv += 1000000
    if sv<0:
        mv -= 1
        sv += 60
    if mv<0:
        hv -= 1
        mv += 60
    if hv<0:
        hv += 24
    h.set(str(hv) if len(str(hv))==2 else '0'+str(hv))
    m.set(str(mv) if len(str(mv))==2 else '0'+str(mv))
    s.set(str(sv) if len(str(sv))==2 else '0'+str(sv))
    ms.set(str(msv).rjust(6, '0')[:3])
    after_num = root.after(5, starts)
start = ttk.Button(count_page, text='开始', command=b_start)
start.grid(row=3, column=2)
def stops(*args):
    global stop_time
    start['state'] = 'normal'
    stop['state'] = 'disabled'
    root.after_cancel(after_num)
    stop_time = datetime.datetime(1, 1, 1).now()
stop = ttk.Button(count_page, text='暂停', command=stops)
stop.grid(row=3, column=4)
stop['state'] = 'disabled'
def resets(*args):
    global start_time, stop_time
    if start_time:
        stops()
    ms.set('000')
    s.set('00')
    m.set('00')
    h.set('00')
    start_time = stop_time = None
reset = ttk.Button(count_page, text='重置', command=resets)
reset.grid(row=3, column=6)
ttk.Separator(count_page, orient=HORIZONTAL, ).grid(row=4, column=1, columnspan=7, sticky=(N, S, W, E))
h2 = StringVar()
h2.set('00')
m2 = StringVar()
m2.set('00')
s2 = StringVar()
s2.set('00')
ms2 = StringVar()
ms2.set('000')
ttk.Label(count_page, text='秒表2：', font='TkTextFont 20').grid(row=5, column=1)
ttk.Label(count_page, textvariable=h2, font='TkTextFont 100').grid(row=6, column=1)
ttk.Label(count_page, text=':', font='TkTextFont 100').grid(row=6, column=2)
ttk.Label(count_page, textvariable=m2, font='TkTextFont 100').grid(row=6, column=3)
ttk.Label(count_page, text=':', font='TkTextFont 100').grid(row=6, column=4)
ttk.Label(count_page, textvariable=s2, font='TkTextFont 100').grid(row=6, column=5)
ttk.Label(count_page, text='.', font='TkTextFont 100').grid(row=6, column=6)
ttk.Label(count_page, textvariable=ms2, font='TkTextFont 50').grid(row=6, column=7, sticky=(S, W))
def b_start2(*args):
    global start_time2, stop_time2
    start2['state'] = 'disabled'
    stop2['state'] = 'normal'
    if not start_time2:
        start_time2 = datetime.datetime(1, 1, 1).now()
    else:
        t = datetime.datetime(1, 1, 1).now()-stop_time2
        start_time2 = start_time2 + t
    root.after(1, starts2)
def starts2():
    global s2, m2, h2, ms2, sv2, mv2, hv2, msv2, after_num2
    now_time = datetime.datetime(1, 1, 1).now()
    msv2 = now_time.microsecond-start_time2.microsecond
    sv2 = now_time.second-start_time2.second
    mv2 = now_time.minute-start_time2.minute
    hv2 = now_time.hour-start_time2.hour
    if msv2<0:
        sv2 -= 1
        msv2 += 1000000
    if sv2<0:
        mv2 -= 1
        sv2 += 60
    if mv2<0:
        hv2 -= 1
        mv2 += 60
    if hv2<0:
        hv2 += 24
    h2.set(str(hv2) if len(str(hv2))==2 else '0'+str(hv2))
    m2.set(str(mv2) if len(str(mv2))==2 else '0'+str(mv2))
    s2.set(str(sv2) if len(str(sv2))==2 else '0'+str(sv2))
    ms2.set(str(msv2).rjust(6, '0')[:3])
    after_num2 = root.after(5, starts2)
start2 = ttk.Button(count_page, text='开始', command=b_start2)
start2.grid(row=7, column=2)
def stops2(*args):
    global stop_time2
    start2['state'] = 'normal'
    stop2['state'] = 'disabled'
    root.after_cancel(after_num2)
    stop_time2 = datetime.datetime(1, 1, 1).now()
stop2 = ttk.Button(count_page, text='暂停', command=stops2)
stop2.grid(row=7, column=4)
stop2['state'] = 'disabled'
def resets2(*args):
    global start_time2
    if start_time2:
        stops2()
    ms2.set('000')
    s2.set('00')
    m2.set('00')
    h2.set('00')
    start_time2 = stop_time2 = None
reset2 = ttk.Button(count_page, text='重置', command=resets2)
reset2.grid(row=7, column=6)
note.add(count_page, text='秒表')

timer_page = ttk.Frame(note)
rh = StringVar()
rh.set('00')
rm = StringVar()
rm.set('00')
rs = StringVar()
rs.set('00')
tw = StringVar()
tw.set('开始')
ttk.Label(timer_page, text='计时器1：', font='TkTextFont 20').grid(row=1, column=1)
ttk.Entry(timer_page, textvariable=rh, font='TkTextFont 100', width=2).grid(row=2, column=1)
ttk.Label(timer_page, text=':', font='TkTextFont 100').grid(row=2, column=2)
ttk.Entry(timer_page, textvariable=rm, font='TkTextFont 100', width=2).grid(row=2, column=3)
ttk.Label(timer_page, text=':', font='TkTextFont 100').grid(row=2, column=4)
ttk.Entry(timer_page, textvariable=rs, font='TkTextFont 100', width=2).grid(row=2, column=5)
def b_run_stop(*args):
    if tw.get() == '开始':
        tw.set('停止')
        root.after(1, run)
    else:
        tw.set('开始')
        root.after_cancel(after_id)
def run():
    global after_id
    s_t = time.time()
    vh = int(rh.get())
    vm = int(rm.get())
    vs = int(rs.get())
    vs -= 1
    if vs < 0:
        if vm == vh == 0:
            root.after(1, end)
            return
        vm -= 1
        vs += 60
    if vm < 0:
        vh -= 1
        vm += 60
    rh.set(str(vh) if len(str(vh))==2 else '0'+str(vh))
    rm.set(str(vm) if len(str(vm))==2 else '0'+str(vm))
    rs.set(str(vs) if len(str(vs))==2 else '0'+str(vs))
    e_t = time.time()
    t = int((e_t - s_t)*1000)
    after_id = root.after(1000-t if 1000-t > 0 else 0, run)
def end():
    tw.set('开始')
    root.bell()
ttk.Button(timer_page, textvariable=tw, width=30, padding=(5, 5, 5, 5), command=b_run_stop).grid(row=2, column=6, sticky=(E,))
ttk.Separator(timer_page, orient=HORIZONTAL, ).grid(row=3, column=1, columnspan=6, sticky=(N, S, W, E))
rh2 = StringVar()
rh2.set('00')
rm2 = StringVar()
rm2.set('00')
rs2 = StringVar()
rs2.set('00')
tw2 = StringVar()
tw2.set('开始')
ttk.Label(timer_page, text='计时器2：', font='TkTextFont 20').grid(row=4, column=1)
ttk.Entry(timer_page, textvariable=rh2, font='TkTextFont 100', width=2).grid(row=5, column=1)
ttk.Label(timer_page, text=':', font='TkTextFont 100').grid(row=5, column=2)
ttk.Entry(timer_page, textvariable=rm2, font='TkTextFont 100', width=2).grid(row=5, column=3)
ttk.Label(timer_page, text=':', font='TkTextFont 100').grid(row=5, column=4)
ttk.Entry(timer_page, textvariable=rs2, font='TkTextFont 100', width=2).grid(row=5, column=5)
def b_run_stop2(*args):
    if tw2.get() == '开始':
        tw2.set('停止')
        root.after(1, run2)
    else:
        tw2.set('开始')
        root.after_cancel(after_id2)
def run2():
    global after_id2
    s_t = time.time()
    vh = int(rh2.get())
    vm = int(rm2.get())
    vs = int(rs2.get())
    vs -= 1
    if vs < 0:
        if vm == vh == 0:
            root.after(1, end2)
            return
        vm -= 1
        vs += 60
    if vm < 0:
        vh -= 1
        vm += 60
    rh2.set(str(vh) if len(str(vh))==2 else '0'+str(vh))
    rm2.set(str(vm) if len(str(vm))==2 else '0'+str(vm))
    rs2.set(str(vs) if len(str(vs))==2 else '0'+str(vs))
    e_t = time.time()
    t = int((e_t - s_t)*1000)
    after_id2 = root.after(1000-t if 1000-t > 0 else 0, run2)
def end2():
    tw2.set('开始')
    root.bell()
    root.after(1000, root.bell)
ttk.Button(timer_page, textvariable=tw2, width=30, padding=(5, 5, 5, 5), command=b_run_stop2).grid(row=5, column=6, sticky=(E,))
note.add(timer_page, text='计时器')

more_timer_page = ttk.Frame(note)
th = StringVar()
th.set('00')
tm = StringVar()
tm.set('00')
ts = StringVar()
ts.set('00')
n = StringVar()
# n.set('<-')
# n.set('√')
th2 = StringVar()
th2.set('00')
tm2 = StringVar()
tm2.set('00')
ts2 = StringVar()
ts2.set('00')
n2 = StringVar()
th3 = StringVar()
th3.set('00')
tm3 = StringVar()
tm3.set('00')
ts3 = StringVar()
ts3.set('00')
n3 = StringVar()
hv = None
mv = None
sv = None
hv2 = None
mv2 = None
sv2 = None
hv3 = None
mv3 = None
sv3 = None
def stop_(*args):
    global after_number, is_running
    if is_running:
        root.after_cancel(after_number)
        is_running = False
def br_1(*args):
    global is_running, hv, mv, sv
    if is_running:
        return
    is_running = True
    if not hv:
        hv = th.get()
        mv = tm.get()
        sv = ts.get()
    n.set('<-')
    n2.set('')
    n3.set('')
    root.after(1, run_1)
def run_1():
    global after_number
    s_t = time.time()
    vh = int(th.get())
    vm = int(tm.get())
    vs = int(ts.get())
    vs -= 1
    if vs < 0:
        if vm == vh == 0:
            root.after(1, end_1)
            return
        vm -= 1
        vs += 60
    if vm < 0:
        vh -= 1
        vm += 60
    th.set(str(vh) if len(str(vh))==2 else '0'+str(vh))
    tm.set(str(vm) if len(str(vm))==2 else '0'+str(vm))
    ts.set(str(vs) if len(str(vs))==2 else '0'+str(vs))
    e_t = time.time()
    t = int((e_t - s_t)*1000)
    after_number = root.after(1000-t if 1000-t > 0 else 0, run_1)
def end_1():
    global hv, mv, sv, is_running
    is_running = False
    th.set(hv)
    tm.set(mv)
    ts.set(sv)
    hv = mv = sv = None
    n.set('√')
    root.lift()
    root.bell()
    root.after(1, n2.set('3'))
    root.after(1000, lambda : n2.set('2'))
    root.after(2000, lambda : n2.set('1'))
    root.after(3000, br_2)
def br_2(*args):
    global is_running, hv2, mv2, sv2
    if is_running:
        return
    is_running = True
    if not hv2:
        hv2 = th2.get()
        mv2 = tm2.get()
        sv2 = ts2.get()
    n.set('')
    n2.set('<-')
    n3.set('')
    root.after(1, run_2)
def run_2():
    global after_number
    s_t = time.time()
    vh = int(th2.get())
    vm = int(tm2.get())
    vs = int(ts2.get())
    vs -= 1
    if vs < 0:
        if vm == vh == 0:
            root.after(1, end_2)
            return
        vm -= 1
        vs += 60
    if vm < 0:
        vh -= 1
        vm += 60
    th2.set(str(vh) if len(str(vh))==2 else '0'+str(vh))
    tm2.set(str(vm) if len(str(vm))==2 else '0'+str(vm))
    ts2.set(str(vs) if len(str(vs))==2 else '0'+str(vs))
    e_t = time.time()
    t = int((e_t - s_t)*1000)
    after_number = root.after(1000-t if 1000-t > 0 else 0, run_2)
def end_2():
    global hv2, mv2, sv2, is_running
    is_running = False
    th2.set(hv2)
    tm2.set(mv2)
    ts2.set(sv2)
    hv2 = mv2 = sv2 = None
    n2.set('√')
    root.lift()
    root.bell()
    root.after(1000, root.bell)
    root.after(1001, lambda : n3.set('3'))
    root.after(2000, lambda : n3.set('2'))
    root.after(3000, lambda : n3.set('1'))
    root.after(4000, br_3)
def br_3(*args):
    global is_running, hv3, mv3, sv3
    if is_running:
        return
    is_running = True
    if not hv3:
        hv3 = th3.get()
        mv3 = tm3.get()
        sv3 = ts3.get()
    n.set('')
    n2.set('')
    n3.set('<-')
    root.after(1, run_3)
def run_3():
    global after_number
    s_t = time.time()
    vh = int(th3.get())
    vm = int(tm3.get())
    vs = int(ts3.get())
    vs -= 1
    if vs < 0:
        if vm == vh == 0:
            root.after(1, end_3)
            return
        vm -= 1
        vs += 60
    if vm < 0:
        vh -= 1
        vm += 60
    th3.set(str(vh) if len(str(vh))==2 else '0'+str(vh))
    tm3.set(str(vm) if len(str(vm))==2 else '0'+str(vm))
    ts3.set(str(vs) if len(str(vs))==2 else '0'+str(vs))
    e_t = time.time()
    t = int((e_t - s_t)*1000)
    after_number = root.after(1000-t if 1000-t > 0 else 0, run_3)
def end_3():
    global hv3, mv3, sv3, is_running
    is_running = False
    th3.set(hv3)
    tm3.set(mv3)
    ts3.set(sv3)
    hv3 = mv3 = sv3 = None
    n3.set('√')
    root.lift()
    root.bell()
    root.after(1000, root.bell)
    root.after(2000, root.bell)
    root.after(2001, lambda : n.set('3'))
    root.after(3000, lambda : n.set('2'))
    root.after(4000, lambda : n.set('1'))
    root.after(5000, br_1)
ttk.Separator(more_timer_page, orient=VERTICAL, ).grid(row=1, column=7, sticky=(N, S, W, E))
ttk.Entry(more_timer_page, textvariable=th, font='TkTextFont 75', width=2).grid(row=1, column=1)
ttk.Label(more_timer_page, text=':', font='TkTextFont 75').grid(row=1, column=2)
ttk.Entry(more_timer_page, textvariable=tm, font='TkTextFont 75', width=2).grid(row=1, column=3)
ttk.Label(more_timer_page, text=':', font='TkTextFont 75').grid(row=1, column=4)
ttk.Entry(more_timer_page, textvariable=ts, font='TkTextFont 75', width=2).grid(row=1, column=5)
ttk.Separator(more_timer_page, orient=HORIZONTAL, ).grid(row=3, column=1, columnspan=6, sticky=(N, S, W, E))
ttk.Label(more_timer_page, textvariable=n, font='TkTextFont 75').grid(row=1, column=8)
ttk.Separator(more_timer_page, orient=VERTICAL, ).grid(row=4, column=7, sticky=(N, S, W, E))
ttk.Entry(more_timer_page, textvariable=th2, font='TkTextFont 75', width=2).grid(row=4, column=1)
ttk.Label(more_timer_page, text=':', font='TkTextFont 75').grid(row=4, column=2)
ttk.Entry(more_timer_page, textvariable=tm2, font='TkTextFont 75', width=2).grid(row=4, column=3)
ttk.Label(more_timer_page, text=':', font='TkTextFont 75').grid(row=4, column=4)
ttk.Entry(more_timer_page, textvariable=ts2, font='TkTextFont 75', width=2).grid(row=4, column=5)
ttk.Separator(more_timer_page, orient=HORIZONTAL, ).grid(row=5, column=1, columnspan=6, sticky=(N, S, W, E))
ttk.Label(more_timer_page, textvariable=n2, font='TkTextFont 75').grid(row=4, column=8)
ttk.Separator(more_timer_page, orient=VERTICAL, ).grid(row=6, column=7, sticky=(N, S, W, E))
ttk.Entry(more_timer_page, textvariable=th3, font='TkTextFont 75', width=2).grid(row=6, column=1)
ttk.Label(more_timer_page, text=':', font='TkTextFont 75').grid(row=6, column=2)
ttk.Entry(more_timer_page, textvariable=tm3, font='TkTextFont 75', width=2).grid(row=6, column=3)
ttk.Label(more_timer_page, text=':', font='TkTextFont 75').grid(row=6, column=4)
ttk.Entry(more_timer_page, textvariable=ts3, font='TkTextFont 75', width=2).grid(row=6, column=5)
ttk.Button(more_timer_page, text='从此开始', width=30, padding=(5, 5, 5, 5), command=br_1).grid(row=1, column=6)
ttk.Button(more_timer_page, text='从此开始', width=30, padding=(5, 5, 5, 5), command=br_2).grid(row=4, column=6)
ttk.Button(more_timer_page, text='从此开始', width=30, padding=(5, 5, 5, 5), command=br_3).grid(row=6, column=6)
ttk.Separator(more_timer_page, orient=HORIZONTAL, ).grid(row=7, column=1, columnspan=6, sticky=(N, S, W, E))
ttk.Label(more_timer_page, textvariable=n3, font='TkTextFont 75').grid(row=6, column=8)
ttk.Button(more_timer_page, text='停止', padding=(5, 5, 5, 5), command=stop_).grid(row=8, column=1, columnspan=6, sticky=(N, E, W, S))
note.add(more_timer_page, text='交替计时')

canvas_page = ttk.Frame(note)
h_ = ttk.Scrollbar(canvas_page, orient=HORIZONTAL)
v = ttk.Scrollbar(canvas_page, orient=VERTICAL)
canvas = Canvas(canvas_page, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set, xscrollcommand=h_.set, bg='#FFFFFF')
h_['command'] = canvas.xview
v['command'] = canvas.yview
ttk.Sizegrip(canvas_page).grid(column=1, row=1, sticky=(S,E))

canvas.grid(column=0, row=0, sticky=(N,W,E,S))
h_.grid(column=0, row=1, sticky=(W,E))
v.grid(column=1, row=0, sticky=(N,S))
canvas_page.grid_columnconfigure(0, weight=1)
canvas_page.grid_rowconfigure(0, weight=1)

lastx, lasty = 0, 0

def xy(event):
    global lastx, lasty
    lastx, lasty = canvas.canvasx(event.x), canvas.canvasy(event.y)

def setColor(newcolor):
    global color
    color = newcolor
    canvas.dtag('all', 'paletteSelected')
    canvas.itemconfigure('palette', outline='white')
    canvas.addtag('paletteSelected', 'withtag', 'palette%s' % color)
    canvas.itemconfigure('paletteSelected', outline='#999999')

def addLine(event):
    global lastx, lasty
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    canvas.create_line((lastx, lasty, x, y), fill=color, width=5, tags=('currentline2' if color == 'white' else 'currentline'))
    lastx, lasty = x, y

def doneStroke(event):
    if color == 'white':
        canvas.itemconfigure('currentline2', width=10)
    else:
        canvas.itemconfigure('currentline', width=1)

def ClearLine():
    canvas.delete('currentline2', 'currentline')
        
canvas.bind("<Button-1>", xy)
canvas.bind("<B1-Motion>", addLine)
canvas.bind("<B1-ButtonRelease>", doneStroke)

id = canvas.create_rectangle((10, 10, 30, 30), fill="red", tags=('palette', 'palettered'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("red"))
id = canvas.create_rectangle((10, 35, 30, 55), fill="blue", tags=('palette', 'paletteblue'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("blue"))
id = canvas.create_rectangle((10, 60, 30, 80), fill="black", tags=('palette', 'paletteblack', 'paletteSelected'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("black"))
id = canvas.create_rectangle((10, 85, 30, 105), fill="#F0F0F0", tags=('palette', 'palettewhite'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("white"))
canvas.tag_bind(id, "<Double-1>", lambda x: ClearLine())

setColor('black')
canvas.itemconfigure('palette', width=5)
note.add(canvas_page, text='附件--画布')

help_page = ttk.Frame(note)
text = Text(help_page, width=800, height=400)
text.insert('1.0', __doc__)
text['state'] = 'disabled'
text.grid()
note.add(help_page, text='帮助')
def askexit(*args):
    if messagebox.askyesno('时间管理大师', '确认退出?', default='no'):
        root.destroy()

root.protocol('WM_DELETE_WINDOW', askexit)
if __name__ == '__main__':
    root.mainloop()
