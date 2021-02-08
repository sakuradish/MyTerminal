# ===================================================================================
from MyLogger.MyLogger import mylogger
mylogger = mylogger.GetInstance("DEBUG")
# ===================================================================================
import tkinter as tk
import datetime
from tkinter import ttk
import math
# ===================================================================================
class ComposeFrame(tk.Tk):
    @mylogger.deco
    def __init__(self, **kw):
        super().__init__(**kw)
        self.frames = []
        self.isKeyEventProcessing = False
        self.isMouseEventProcessing = False
        self.bind("<Control-Key>", self.OnKeyEvent)
        self.bind("<Button>", self.OnMouseEvent)
# ===================================================================================
    @mylogger.deco
    def AddFrame(self, frame, id, key=None, mouse=None, time=None):
        button = tk.Button(self, text=id)
        # button.state(['pressed'])
        button.bind("<Button-1>", self.toggleView)
        button.bind("<Return>", self.toggleView)
        if len(self.frames) < 2:
            self.frames.append([frame, id, True, button, key, mouse, time])
        else:
            self.frames.append([frame, id, False, button, key, mouse, time])
        self.initialize()
# ===================================================================================
    @mylogger.deco
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
        # 行数,列数などを算出
        if visibleFrames == []:
            return
        rowmax = 1
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
    @mylogger.deco
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
    @mylogger.deco
    def initialize(self):
        for frame in self.frames:
            frame[0].place_forget()
            frame[3].place_forget()
        self.Draw()
# ===================================================================================
    @mylogger.deco
    def OnKeyEvent(self, event):
        try:
            index = int(event.keysym) - 1
            if self.frames[index][2]:
                self.frames[index][2] = False
            else:
                self.frames[index][2] = True
            self.initialize()
        except:
            pass

        if self.isKeyEventProcessing == False:
            self.isKeyEventProcessing = True
            print(event)
            for frame in self.frames:
                if frame[4]:
                    frame[4](event)
            self.isKeyEventProcessing = False
# ===================================================================================
    @mylogger.deco
    def OnMouseEvent(self, event):
        if self.isMouseEventProcessing == False:
            self.isMouseEventProcessing = True
            print(event)
            for frame in self.frames:
                if frame[5]:
                    frame[5](event)
            self.isMouseEventProcessing = False
# ===================================================================================
    @mylogger.deco
    def OnTick(self):
        for frame in self.frames:
            if frame[6]:
                frame[6]()
        # print(datetime.datetime(2021, 5, 5, 10,10,10) - datetime.datetime.now())
        self.after(10000,self.OnTick)
# ===================================================================================
if __name__ == '__main__':

    framecompose = ComposeFrame()
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
    framecompose.mainloop()
# ===================================================================================