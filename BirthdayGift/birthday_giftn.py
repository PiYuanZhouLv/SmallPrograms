import tkinter
from tkinter import messagebox as msgbox
from pynput.mouse import Events, Button
import datetime
import threading
import colorsys
import random
import queue
import math

import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

if datetime.date(2023, 9, 14) != datetime.date.today():
    import sys
    sys.exit()

root = tkinter.Tk()
root.withdraw()

msgbox.showinfo('温馨提示','''\
同学们：

　　嗨嗨嗨，我又莱里奥！今天是杨祎涵同学的生日，
这个程序是送给她的生日礼物。

　　部分同学应该已经知道这是谁编写的，至少杨祎涵同学知道。
如果你很好奇这个程序是谁写的，可以去问她，别忘了祝她生日快乐！

　　这个程序远不止这个弹窗功能，在双击鼠标左键时也有特殊效果哟~
　　P.S. 加了一些新的动画特效

　　最后，祝杨祎涵同学生日快乐，祝全体同学学习进步，快乐成长！

　　　　　　　　　　　　　　　　　　　　　　　　　　署名
　　　　　　　　　　　　　　　　　　　　　　　　2023年9月14日''')

class TipWindow:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.tick = -1
        self.color = "#{:0>2X}{:0>2X}{:0>2X}".format(*list(map(lambda x: int(x * 256), colorsys.hls_to_rgb(random.random(), 0.4, 0.8))))
        self.window = tkinter.Toplevel(root, bg='#000000')
        self.window.configure(bg='#000000')
        self.label = tkinter.Label(self.window, text='杨祎涵 生日快乐', foreground=self.color, background='#000000', font=(None, 30, 'bold'))
        self.label.pack()
        self.window.attributes('-topmost', True)
        self.window.attributes('-toolwindow', True)
        self.window.resizable(False, False)
        self.window.attributes('-transparent', '#000000')
        self.window.overrideredirect(True)
        self.window.update()
    def running(self, *_):
        f = random.choice([self.running1, self.running2, self.running3, self.running4, self.running5, self.running6])
        print(f)
        self.window.after(0, f)
    def running1(self, *_):
        if self.tick == -1:
            self.window.geometry(f'+{self.pos[0]-self.window.winfo_width()//2}+{self.pos[1]-self.window.winfo_height()}')
            self.window.update()
        self.tick += 1
        self.window.geometry(f'+{self.pos[0]-self.window.winfo_width()//2}+{self.pos[1]-self.tick-self.window.winfo_height()}')
        self.window.attributes('-alpha', 1-0.01*self.tick)
        self.window.update()
        if self.tick >= 100:
            self.window.destroy()
            return
        else:
            self.window.after(10, self.running1)
    def running2(self, *_):
        if self.tick == -1:
            self.y = random.randint(0, int(self.window.winfo_screenheight()-self.window.winfo_height()))
        self.tick += 1
        self.window.geometry(f"+{int(self.window.winfo_screenwidth()-((self.window.winfo_screenwidth()+self.window.winfo_width())*self.tick/300))}+{self.y}")
        if self.tick >= 300:
            self.window.destroy()
            return
        else:
            self.window.after(10, self.running2)
    def running3(self, *_):
        if self.tick == -1:
            self.x = random.randint(0, int(self.window.winfo_screenwidth()-self.window.winfo_width()))
        self.tick += 1
        self.window.geometry(f"+{self.x}+{int(-self.window.winfo_height()+((self.window.winfo_screenheight()+self.window.winfo_height())*self.tick/200))}")
        if self.tick >= 200:
            self.window.destroy()
            return
        else:
            self.window.after(10, self.running3)
    def running4(self, *_):
        if self.tick == -1:
            self.window.geometry(f"+{random.randint(0, int(self.window.winfo_screenwidth()-self.window.winfo_width()))}+{random.randint(0, int(self.window.winfo_screenheight()-self.window.winfo_height()))}")
        self.tick += 1
        self.window.attributes('-alpha', abs(math.sin(math.pi*self.tick/100)))
        if self.tick >= 200:
            self.window.destroy()
            return
        else:
            self.window.after(10, self.running4)
    def running5(self, *_):
        if self.tick == -1:
            self.hue = random.random()
            self.window.geometry(f"+{random.randint(0, int(self.window.winfo_screenwidth()-self.window.winfo_width()))}+{random.randint(0, int(self.window.winfo_screenheight()-self.window.winfo_height()))}")
        self.tick += 1
        self.label.configure(fg="#{:0>2X}{:0>2X}{:0>2X}".format(*list(map(lambda x: int(x * 256), colorsys.hls_to_rgb((self.hue+self.tick/200)%1, 0.4, 0.8)))))
        if self.tick >= 200:
            self.window.destroy()
            return
        else:
            self.window.after(10, self.running5)
    def running6(self, *_):
        self.tick += 1
        self.window.geometry(f"+{int(self.pos[0]-self.window.winfo_width()/2+100*math.cos(math.pi*self.tick/100+math.pi/2))}+{int(self.pos[1]-self.window.winfo_height()/2+100*math.sin(math.pi*self.tick/100+math.pi/2))}")
        if self.tick >= 200:
            self.window.destroy()
            return
        else:
            self.window.after(10, self.running6)

q = queue.Queue()

def LeftDown(event: Events, timeout=None):
    while True:
        e = event.get(timeout)
        if e is None:
            return None
        if type(e) == Events.Click and e.pressed and e.button == Button.left:
            return e

def listening():
    with Events() as event:
        while not stop:
            LeftDown(event)
            if e := LeftDown(event, 0.1):
                q.put((e.x, e.y))

stop = False

linstener = threading.Thread(target=listening)
linstener.start()

try:
    while True:
        while not q.empty():
            root.after(0, TipWindow(q.get()).running)
        root.update()
except KeyboardInterrupt:
    print('stopping...')
    stop = True
    linstener.join()
