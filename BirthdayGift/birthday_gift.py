import tkinter
from tkinter import messagebox as msgbox
from pynput.mouse import Events, Button
import datetime
import threading
import colorsys
import random
import queue

import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

if datetime.date(2023, 9, 5) != datetime.date.today():
    import sys
    sys.exit()

root = tkinter.Tk()
root.withdraw()

msgbox.showinfo('温馨提示','''\
同学们：

　　你们好！今天是宋晨钰同学的生日，这个程序是送给她的生日礼物。

　　相信部分同学能猜到这是谁编写的，至少宋晨钰同学应该能猜出来。
如果你很好奇这个程序是谁写的，可以去问她，别忘了祝她生日快乐！

　　这个程序远不止这个弹窗功能，在双击鼠标左键时也有特殊效果哟~

　　最后，祝宋晨钰同学生日快乐，祝全体同学学习进步，快乐成长！

　　　　　　　　　　　　　　　　　　　　　　　　　　署名
　　　　　　　　　　　　　　　　　　　　　　　　2023年9月5日''')

class TipWindow:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.tick = 0
        self.color = "#{:0>2X}{:0>2X}{:0>2X}".format(*list(map(lambda x: int(x * 256), colorsys.hls_to_rgb(random.random(), 0.4, 0.8))))
        self.window = tkinter.Toplevel(root, bg='#000000')
        self.window.configure(bg='#000000')
        tkinter.Label(self.window, text='宋晨钰 生日快乐', foreground=self.color, background='#000000', font=(None, 30, 'bold')).pack()
        self.window.attributes('-topmost', True)
        self.window.attributes('-toolwindow', True)
        self.window.resizable(False, False)
        self.window.attributes('-transparent', '#000000')
        self.window.overrideredirect(True)
        self.window.update()
        self.window.geometry(f'+{self.pos[0]-self.window.winfo_width()//2}+{self.pos[1]-self.window.winfo_height()}')
        self.window.update()
    def running(self, *_):
        self.tick += 1
        self.window.geometry(f'+{self.pos[0]-self.window.winfo_width()//2}+{self.pos[1]-self.tick-self.window.winfo_height()}')
        self.window.attributes('-alpha', 1-0.01*self.tick)
        self.window.update()
        if self.tick >= 100:
            self.window.destroy()
            return
        else:
            self.window.after(10, self.running)

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
