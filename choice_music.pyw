import random
import tkinter
from tkinter import Frame, Button, Label
from pygame import mixer

root = tkinter.Tk()
root.title("抽取音乐")
mixer.init()

rs_list = list(range(1, 18+1))
pt_list = list(range(1, 26+1))
kn_list = list(range(1, 20+1))

row1 = Frame(root)
row2 = Frame(root)
row3 = Frame(root)
row4 = Frame(root)
row5 = Frame(root)

current = "rs"

def change(btn):
    global current
    rs_b['bg'] =  pt_b['bg'] = kn_b['bg'] = "grey"
    current = btn
    num_var.set('??')
    if btn == "rs":
        rs_b['bg'] = "#00FF00"
    elif btn == "pt":
        pt_b['bg'] = "#FFFF00"
    else:
        kn_b['bg'] = '#FF0000'
    ch_list = globals()[current + "_list"]
    if ch_list:
        ch_b['state'] = 'normal'
    else:
        ch_b['state'] = 'disabled'

rs_b = Button(row1, text="热身题", font=('default', 20), command=lambda: change("rs"), bg="#00FF00")
rs_b.pack(side="left")
pt_b = Button(row1, text="普通题", font=('default', 20), command=lambda: change("pt"), bg="grey")
pt_b.pack(side="left")
kn_b = Button(row1, text="困难题", font=('default', 20), command=lambda: change("kn"), bg="grey")
kn_b.pack(side="left")

num_var = tkinter.IntVar(value="??")
Label(row2, text="第", font=('default', 20)).pack(side="left")
Label(row2, textvariable=num_var, font=('default', 40)).pack(side="left")
Label(row2, text="题", font=('default', 20)).pack(side="left")

rs_l = tkinter.IntVar(value=len(rs_list))
pt_l = tkinter.IntVar(value=len(pt_list))
kn_l = tkinter.IntVar(value=len(kn_list))
Label(row3, text="热身: ").pack(side="left")
Label(row3, textvariable=rs_l).pack(side="left")
Label(row3, text=", 普通: ").pack(side="left")
Label(row3, textvariable=pt_l).pack(side="left")
Label(row3, text=", 困难: ").pack(side="left")
Label(row3, textvariable=kn_l).pack(side="left")

def choice():
    global con_or_play
    pause()
    ch_list = globals()[current+"_list"]
    index = random.choice(ch_list)
    globals()[current+"_l"].set(globals()[current+"_l"].get()-1)
    ch_list.remove(index)
    if not ch_list:
        ch_b['state'] = 'disabled'
    num_var.set(index)
    con_or_play = "play"

con_or_play = "play"
vol = 1
vol_var = tkinter.DoubleVar(value=float(vol))

def vol_add():
    global vol
    if vol == 0:
        vol_down['state'] = 'normal'
    vol = (vol*10+1)/10 # fix: 1.1 + 0.1 = 1.2000000000000002
    if vol == 1:
        vol_up['state'] = 'disabled'
    vol_var.set(vol)
    mixer.music.set_volume(vol)

def vol_min():
    global vol
    if vol == 1:
        vol_up['state'] = 'normal'
    vol = (vol*10-1)/10
    if vol == 0:
        vol_down['state'] = 'disabled'
    vol_var.set(vol)
    mixer.music.set_volume(vol)

def play():
    if num_var.get() == '??':
        return
    if con_or_play == "play":
        d = {'rs': '热身', 'pt': '普通', 'kn': '困难'}
        path = f'{d[current]}/{num_var.get()}.mp3'
        mixer.music.load(path)
        mixer.music.play()
    else:
        mixer.music.unpause()
    pl_b['state'] = 'disabled'
    pu_b['state'] = 'normal'

def pause():
    global con_or_play
    con_or_play = "con"
    pl_b['state'] = 'normal'
    pu_b['state'] = 'disabled'
    mixer.music.pause()

ch_b = Button(row4, text="抽取", font=('default', 20), command=choice)
ch_b.pack(side="left", fill="both")
pl_b = Button(row4, text="播放", font=('default', 20), command=play)
pl_b.pack(side="left", fill="both")

col = Frame(row4)
vol_up = Button(col, text='↑', command=vol_add, state="disabled")
vol_up.pack(side="top", fill="both")
Label(col, textvariable=vol_var).pack(side="top", fill="both")
vol_down = Button(col, text='↓', command=vol_min)
vol_down.pack(side="top", fill="both")
col.pack(side="left", fill="both")

pu_b = Button(row4, text="暂停", font=('default', 20), command=pause, state='disabled')
pu_b.pack(side="left", fill="both")

sc1 = tkinter.IntVar(value=0)
sc2 = tkinter.IntVar(value=0)
sc3 = tkinter.IntVar(value=0)
sc4 = tkinter.IntVar(value=0)
sl1 = Label(row5, textvariable=sc1, font=('default', 30))
sl1.grid(column=0, row=0)
sl1.bind("<Button-1>", lambda event: sc1.set(0))
sl2 = Label(row5, textvariable=sc2, font=('default', 30))
sl2.grid(column=1, row=0)
sl2.bind("<Button-1>", lambda event: sc2.set(0))
sl3 = Label(row5, textvariable=sc3, font=('default', 30))
sl3.grid(column=2, row=0)
sl3.bind("<Button-1>", lambda event: sc3.set(0))
sl4 = Label(row5, textvariable=sc4, font=('default', 30))
sl4.grid(column=3, row=0)
sl4.bind("<Button-1>", lambda event: sc4.set(0))

as1 = Button(row5, text="+1", font=('default', 20), command=lambda: sc1.set(sc1.get() + 1))
as1.grid(column=0, row=1)
as2 = Button(row5, text="+1", font=('default', 20), command=lambda: sc2.set(sc2.get() + 1))
as2.grid(column=1, row=1)
as3 = Button(row5, text="+1", font=('default', 20), command=lambda: sc3.set(sc3.get() + 1))
as3.grid(column=2, row=1)
as4 = Button(row5, text="+1", font=('default', 20), command=lambda: sc4.set(sc4.get() + 1))
as4.grid(column=3, row=1)

row1.pack(side="top")
row2.pack(side="top")
row3.pack(side="top")
row4.pack(side="top")
row5.pack(side="top")

root.mainloop()