# ===================================================================================
from ComposeFrame import ComposeFrame
from MyDataBase import MyDataBase
from MyLogger.MyLogger import mylogger
mylogger = mylogger.GetInstance()
# ===================================================================================
import datetime
import tkinter as tk
from tkinter import font
from tkinter import ttk
# from PIL import Image, ImageTk
import os
import time
# import math
# ===================================================================================
class TemplateFrame(tk.Frame):
    @mylogger.deco
    def __init__(self, master, mydata ,cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.mydata = mydata
        self.inputfield = {}
        self.filterfield = {}
        self.editorfield = {}
        self.editorstart = 0
        self.editorend = 10
        self.editorrowcnt = 0
        self.InitializeStaticWidget()
        self.InitializeDynamicWidget()
# ===================================================================================
    def Combobox(self, text):
        label = tk.Label(self, text=text)
        v = tk.StringVar()
        cb = ttk.Combobox(self, textvariable=v)
        return {'label':label, 'combobox':cb, 'stringvar':v}
    def ComboboxNonLabel(self):
        v = tk.StringVar()
        cb = ttk.Combobox(self, textvariable=v)
        return {'combobox':cb, 'stringvar':v}
# ===================================================================================
    @mylogger.decodeco
    def InitializeStaticWidget(self):
        for column in mydata.GetDataColumns():
            self.inputfield[column] = self.Combobox(column)
        for column in mydata.GetDataColumns():
            self.filterfield[column] = self.ComboboxNonLabel()
        self.UpdateStaticWidgetProperty()
        self.PlaceStaticWidget()
# ===================================================================================
    @mylogger.deco
    def PlaceStaticWidget(self):
        count = 0
        columns = mydata.GetDataColumns()
        for column in columns:
            index = columns.index(column)
            relheight = 0.4 / len(columns)
            rely = 0+relheight*index
            self.inputfield[column]['label'].place(relx=0,rely=rely,relwidth=0.2,relheight=relheight)
            self.inputfield[column]['combobox'].place(relx=0.2,rely=rely,relwidth=0.8,relheight=relheight)
        for column in columns:
            index = columns.index(column)
            relwidth = 1 / len(columns)
            relheight = 0.04
            relx = relwidth*index
            rely = 0.43
            self.filterfield[column]['combobox'].place(relx=relx,rely=rely,relwidth=relwidth,relheight=relheight)
# ===================================================================================
    @mylogger.deco
    def UpdateStaticWidgetProperty(self):
        if self.mydata.GetRecords():
            for column in mydata.GetDataColumns():
                records = self.mydata.GetRecords()
                records = [record['data'][column] for record in records]
                records = list(dict.fromkeys(records))
                self.inputfield[column]['combobox'].configure(values=records)
                self.inputfield[column]['combobox'].set(self.mydata.GetRecords(row=-1)['data'][column])
                self.filterfield[column]['combobox'].configure(values=records)
                # self.filterfield[column]['combobox'].set(self.mydata.GetRecords(row=-1)['data'][column])
# ===================================================================================
    @mylogger.decodeco
    def InitializeDynamicWidget(self):
        # destroy
        for i in range(0, self.editorrowcnt, 1):
            for column in mydata.GetDataColumns():
                self.editorfield[i][column]['combobox'].destroy()
        # get records
        filter = {}
        for column in mydata.GetDataColumns():
            filter[column] = self.filterfield[column]['combobox'].get()
        records = mydata.GetRecords(filter=filter)
        # calc row count
        self.editorrowcnt = len(records)
        if self.editorrowcnt > 10:
            self.editorrowcnt = 10
        # create widget
        self.editorfield = {}
        count = 0
        for record in records:
            if self.editorrowcnt <= count:
                break
            self.editorfield[count] = {'record':record}
            for column in mydata.GetDataColumns():
                self.editorfield[count][column] = self.ComboboxNonLabel()
            count += 1
        self.UpdateDynamicWidgetProperty()
        self.PlaceDynamicWidget()
# ===================================================================================
    @mylogger.deco
    def PlaceDynamicWidget(self):
        columns = mydata.GetDataColumns()
        for i in range(0, self.editorrowcnt, 1):
            for column in columns:
                index = columns.index(column)
                relwidth = 1 / len(self.inputfield)
                relheight = 0.04
                relx = 0 + relwidth*index
                rely = 0.5 + 0.04*i
                self.editorfield[i][column]['combobox'].place(relx=relx,rely=rely,relwidth=relwidth,relheight=relheight)
# ===================================================================================
    @mylogger.deco
    def UpdateDynamicWidgetProperty(self):
        # get records
        filter = {}
        for column in mydata.GetDataColumns():
            filter[column] = self.filterfield[column]['combobox'].get()
        records = self.mydata.GetRecords(filter=filter)
        # records = self.mydata.GetRecords()

        # # 現在ページ向けの開始・終了インデックスを算出
        # start = (int(self.currentpage.get())-1) * self.itemnum
        # end = start + self.itemnum
        # if len(records) <= end:
        #     end = len(records)
        # for num in range(start, end, 1):
        count = 0
        for recordidx in range(self.editorstart, self.editorend, 1):
        # for record in records:
            # if len(self.editorfield) <= recordidx:
            #     break
            record = records[recordidx]
            for column in mydata.GetDataColumns():
                self.editorfield[count][column]['combobox'].set(record['data'][column])
            # recordidx += 1
            count += 1
# ===================================================================================
    @mylogger.deco
    def OnTick(self):
        pass
# ===================================================================================
    @mylogger.deco
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            # 入力エリアでEnter
            isInputFieldFocused = False
            for column in mydata.GetDataColumns():
                if self.inputfield[column]['combobox'] == self.master.focus_get() and self.inputfield[column]['combobox'] != "":
                    isInputFieldFocused = True
                    break
            if isInputFieldFocused:
                record = self.mydata.GetEmptyRecord()
                for column in mydata.GetDataColumns():
                    record['data'][column] = self.inputfield[column]['combobox'].get()
                self.mydata.PushbackRecords([record])
            # 編集エリアでEnter
            isEditorFieldFocused = False
            for i in range(0, self.editorrowcnt, 1):
                for column in mydata.GetDataColumns():
                    if self.editorfield[i][column]['combobox'] == self.master.focus_get() and self.editorfield[i][column]['combobox'] != "":
                        isEditorFieldFocused = True
                        break
            if isEditorFieldFocused:
                records = []
                for i in range(0, self.editorrowcnt, 1):
                    record = self.editorfield[i]['record']
                    for column in mydata.GetDataColumns():
                        record['data'][column] = self.editorfield[i][column]['combobox'].get()
                    records.append(record)
                self.mydata.ReplaceRecords(records)
            self.UpdateStaticWidgetProperty()
            self.InitializeDynamicWidget()
        elif event.keysym == 'd':
            print("page scroll")
            self.editorstart += 1
            # self.editorstart = 1
            self.editorend = self.editorstart + self.editorrowcnt
            if len(mydata.GetRecords()) < self.editorend:
                self.editorend = len(mydata.GetRecords())
                self.editorstart = self.editorend - self.editorrowcnt
            print(self.editorstart)
            self.UpdateStaticWidgetProperty()
            self.InitializeDynamicWidget()
        elif event.keysym == 'u':
            print("page scroll")
            self.editorstart -= 1
            # self.editorstart = 1
            self.editorend = self.editorstart + self.editorrowcnt
            if self.editorstart < 0:
                self.editorstart = 0
                self.editorend = self.editorrowcnt
            print(self.editorstart)
            self.UpdateStaticWidgetProperty()
            self.InitializeDynamicWidget()
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