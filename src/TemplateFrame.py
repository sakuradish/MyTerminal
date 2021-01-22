# ===================================================================================
from ComposeFrame import ComposeFrame
from MyDataBase import MyDataBase
from MyLogger import mylogger
# ===================================================================================
import datetime
import tkinter as tk
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
import math
# ===================================================================================
class TemplateFrame(tk.Frame):
    @mylogger.deco
    def __init__(self, master, mydata ,cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.mydata = mydata
        self.widgets = {}
        self.editor = {}
        self.tempcnt = 0
        self.InitializeStaticWidget()
# ===================================================================================
    def Combobox(self, text):
        label = tk.Label(self, text=text)
        v = tk.StringVar()
        cb = ttk.Combobox(self, textvariable=v)
        return [label, cb, v]
    def ComboboxNonLabel(self):
        v = tk.StringVar()
        cb = ttk.Combobox(self, textvariable=v)
        return [cb, v]
# ===================================================================================
    @mylogger.deco
    def InitializeStaticWidget(self):
        for column in mydata.GetDataColumns():
            self.widgets[column] = self.Combobox(column)
        # 仮実装
        self.tempcnt = int((1 - 0.05*len(self.widgets)) / 0.05)
        print(self.tempcnt)
        self.editor = {}
        for i in range(0, self.tempcnt, 1):
            print(i)
            self.editor[i] = {}
            for column in mydata.GetDataColumns():
                self.editor[i][column] = self.ComboboxNonLabel()
        print(self.editor)
        self.UpdateStaticWidgetProperty()
        self.PlaceStaticWidget()
# ===================================================================================
    @mylogger.deco
    def PlaceStaticWidget(self):
        count = 0
        for column in mydata.GetDataColumns():
            self.widgets[column][0].place(relx=0,rely=0+0.05*count,relwidth=0.2,relheight=0.05)
            self.widgets[column][1].place(relx=0.2,rely=0+0.05*count,relwidth=0.8,relheight=0.05)
            count += 1
        # 仮実装
        print("koko yobareteru???????????????")
        offsety = count*0.05
        for i in range(0, self.tempcnt, 1):
            for column in mydata.GetDataColumns():
                print(i,column)
                relwidth = 1 / len(self.widgets)
                relheight = 0.05
                relx = 0 + relwidth*mydata.GetDataColumns().index(column)
                rely = offsety + 0.05*i
                self.editor[i][column][0].place(relx=relx,rely=rely,relwidth=relwidth,relheight=relheight)
# ===================================================================================
    @mylogger.deco
    def UpdateStaticWidgetProperty(self):
        if self.mydata.GetAllRecords():
            for column in mydata.GetDataColumns():
                records = self.mydata.GetAllRecordsByColumn(column)
                records = [record['data'][column] for record in records]
                records = list(dict.fromkeys(records))
                self.widgets[column][1].configure(values=records)
                self.widgets[column][1].set(self.mydata.GetLastRecordsByColumn(column)['data'][column])
# ===================================================================================
    @mylogger.deco
    def InitializeDynamicWidget(self):
        pass
# ===================================================================================
    @mylogger.deco
    def PlaceDynamicWidget(self):
        pass
# ===================================================================================
    @mylogger.deco
    def UpdateDynamicWidgetProperty(self):
        pass
# ===================================================================================
    @mylogger.deco
    def OnTick(self):
        pass
# ===================================================================================
    @mylogger.deco
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            isCbFocused = False
            for column in mydata.GetDataColumns():
                if self.widgets[column][1] == self.master.focus_get() and self.widgets[column][1] != "":
                    isCbFocused = True
                    break
            record = []
            for column in mydata.GetDataColumns():
                record.append(self.widgets[column][1].get())
            self.mydata.InsertRecordWithLogInfo(record)
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    mydata = MyDataBase("../data/mydata.txt", ['colmun1', 'colmun2', 'colmun3', 'column4'])
    templateframe = TemplateFrame(root, mydata)
    framecompose.AddFrame(templateframe, 'templateframe', key=templateframe.OnKeyEvent, time=templateframe.OnTick)

    # メインループ
    root.mainloop()
# ===================================================================================