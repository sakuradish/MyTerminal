# ===================================================================================
import tkinter as tk
import datetime
# from tkinter import font
from tkinter import ttk
# from PIL import Image, ImageTk
# import time
import math
# ===================================================================================
class ComposeFrame(tk.Frame):
    def __init__(self, master=None,cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.frames = []
        self.isKeyEventProcessing = False
        self.isMouseEventProcessing = False
        self.master.bind("<Key>", self.OnKeyEvent)
        self.master.bind("<Button>", self.OnMouseEvent)
        self.OnTick()
# ===================================================================================
    def AddFrame(self, frame, id, key=None, mouse=None, time=None):
        button = tk.Button(self.master, text=id)
        # button.state(['pressed'])
        button.bind("<Button-1>", self.toggleView)
        button.bind("<Return>", self.toggleView)
        if len(self.frames) < 2:
            self.frames.append([frame, id, True, button, key, mouse, time])
        else:
            self.frames.append([frame, id, False, button, key, mouse, time])
        self.initialize()
# ===================================================================================
    def Draw(self):
        # toggleボタンを表示更新
        num = 0
        for frame in self.frames:
            if frame[2] == True:
                frame[3].configure(bg='blue')
            else:
                frame[3].configure(bg='gray')
            frame[3].place(relwidth=0.1, relx=num*0.1)
            num += 1
        # 表示状態のFrameのみ抽出
        visibleFrames = []
        for frame in self.frames:
            if frame[2] == True:
                visibleFrames.append(frame[0])
        rowmax = 1
        # 行数,列数などを算出
        while 1:
            if rowmax * rowmax > len(visibleFrames):
                rowmax -= 1
                break
            else:
                rowmax += 1
        colmax = math.ceil(len(visibleFrames) / rowmax)
        offsety = 0.9 / rowmax
        relheight = 0.9 / rowmax
        offsetx = 1 / colmax
        relwidth = 1 / colmax
        # Frameを配置
        for row in range(0, rowmax, 1):
            for col in range(0, colmax, 1):
                index = row*colmax+col
                relx = col*offsetx
                rely = 0.1+row*offsety
                if len(visibleFrames) - 1 >= index:
                    # print(visibleFrames[index].place_info())
                    visibleFrames[index].place(relx=relx,rely=rely,relwidth=relwidth,relheight=relheight)
# ===================================================================================
    def toggleView(self, event):
        target = event.widget["text"]
        for frame in self.frames:
            if frame[1] == target:
                if frame[2] == True:
                    frame[2] = False
                else:
                    frame[2] = True
        self.initialize()
# ===================================================================================
    def initialize(self):
        for frame in self.frames:
            frame[0].place_forget()
            frame[3].place_forget()
        self.Draw()
# ===================================================================================
    def OnKeyEvent(self, event):
        if self.isKeyEventProcessing == False:
            self.isKeyEventProcessing = True
            print(event)
            for frame in self.frames:
                if frame[4]:
                    frame[4](event)
            self.isKeyEventProcessing = False
# ===================================================================================
    def OnMouseEvent(self, event):
        if self.isMouseEventProcessing == False:
            self.isMouseEventProcessing = True
            print(event)
            for frame in self.frames:
                if frame[5]:
                    frame[5](event)
            self.isMouseEventProcessing = False
# ===================================================================================
    def OnTick(self):
        for frame in self.frames:
            if frame[6]:
                frame[6]()
        # print(datetime.datetime(2021, 5, 5, 10,10,10) - datetime.datetime.now())
        self.master.after(1000,self.OnTick)
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    frame1 = tk.Frame(bg='#000000')
    frame2 = tk.Frame(bg='#0000ff')
    frame3 = tk.Frame(bg='#00ff00')
    frame4 = tk.Frame(bg='#00ffff')
    frame5 = tk.Frame(bg='#ff0000')
    frame6 = tk.Frame(bg='#ff00ff')
    frame7 = tk.Frame(bg='#ffff00')
    frame8 = tk.Frame(bg='#ffffff')
    framecompose.AddFrame(frame1, '#000000')
    framecompose.AddFrame(frame2, '#0000ff')
    framecompose.AddFrame(frame3, '#00ff00')
    framecompose.AddFrame(frame4, '#00ffff')
    framecompose.AddFrame(frame5, '#ff0000')
    framecompose.AddFrame(frame6, '#ff00ff')
    framecompose.AddFrame(frame7, '#ffff00')
    framecompose.AddFrame(frame8, '#ffffff')

    # メインループ
    root.mainloop()
# ===================================================================================