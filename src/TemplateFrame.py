# ===================================================================================
from ComposeFrame import ComposeFrame
from MyDataBase import MyDataBase
from MyLogger.MyLogger import mylogger
# mylogger = mylogger.GetInstance()
mylogger = mylogger.GetInstance("DEBUG")
from WidgetFactory import WidgetFactory
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
        self.inputfield = {'label':{}, 'combobox':{}}
        self.filterfield = {}
        self.viewerfield = {}
        self.viewerstart = 0
        self.InitializeStaticWidget()
        self.InitializeDynamicWidget()
# ===================================================================================
    @mylogger.deco
    def InitializeStaticWidget(self):
        columns = self.mydata.GetDataColumns()
        self.inputfield['label'] = WidgetFactory.Label(self, columns, 0,0,0.2,0.4)
        self.inputfield['combobox'] = WidgetFactory.Combobox(self, columns, 0.2,0,0.8,0.4)
        self.filterfield = WidgetFactory.Combobox(self, columns, 0,0.43,1,0.04, "ToRight")
        self.UpdateStaticWidgetProperty()
# ===================================================================================
    @mylogger.deco
    def UpdateStaticWidgetProperty(self):
        columns = self.mydata.GetDataColumns()
        for column in columns:
            records = self.mydata.GetRecords()
            records = [record['data'][column] for record in records]
            records = list(dict.fromkeys(records))
            self.inputfield['combobox']['widgets'][column]['combobox'].configure(values=records)
            self.inputfield['combobox']['widgets'][column]['combobox'].set(self.mydata.GetRecords(row=-1)['data'][column])
            self.filterfield['widgets'][column]['combobox'].configure(values=records)
            # self.filterfield[column]['combobox'].set(self.mydata.GetRecords(row=-1)['data'][column])
# ===================================================================================
    @mylogger.deco
    def InitializeDynamicWidget(self):
        # get records
        columns = self.mydata.GetDataColumns()
        filter = {}
        for column in columns:
            filter[column] = self.filterfield['widgets'][column]['combobox'].get()
        records = self.mydata.GetRecords(filter=filter)
        # destroy
        for key,field in self.viewerfield.items():
            WidgetFactory.Destroy(field['combobox']['id'])
            WidgetFactory.Destroy(field['label']['id'])
        self.viewerfield = {}
        # init
        count = 0
        for record in records:
            if count >= 10:
                break
            self.viewerfield[count] = {}
            self.viewerfield[count]['combobox'] = WidgetFactory.Combobox(self, columns, 0.05,0.5+0.04*count,0.95,0.04, "ToRight")
            self.viewerfield[count]['label'] = WidgetFactory.Label(self, ['index'], 0,0.5+0.04*count,0.05,0.04, "ToRight")
            self.viewerfield[count]['record'] = record
            count += 1
        self.UpdateDynamicWidgetProperty()
# ===================================================================================
    @mylogger.deco
    def UpdateDynamicWidgetProperty(self):
        # get records
        columns = self.mydata.GetDataColumns()
        filter = {}
        for column in columns:
            filter[column] = self.filterfield['widgets'][column]['combobox'].get()
        records = self.mydata.GetRecords(filter=filter)
        # update
        count = 0
        start = self.viewerstart
        end = start + len(self.viewerfield)
        for recordidx in range(start, end, 1):
            record = records[recordidx]
            for column in self.mydata.GetDataColumns():
                self.viewerfield[count]['combobox']['widgets'][column]['combobox'].set(record['data'][column])
            self.viewerfield[count]['label']['widgets']['index']['label'].configure(text=str(record['index']))
            count += 1
# ===================================================================================
    @mylogger.deco
    def OnTick(self):
        pass
# ===================================================================================
    @mylogger.deco
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            isInputFieldFocused = False
            columns = self.mydata.GetDataColumns()
            for column in columns:
                combobox = self.inputfield['combobox']['widgets'][column]['combobox']
                if combobox == self.master.focus_get() and combobox.get() != "":
                    isInputFieldFocused = True
                    break
            isViewerFieldFocused = False
            for i in range(0, len(self.viewerfield), 1):
                for column in columns:
                    combobox = self.viewerfield[i]['combobox']['widgets'][column]['combobox']
                    if combobox == self.master.focus_get() and combobox.get() != "":
                        isViewerFieldFocused = True
                        break

            if isInputFieldFocused:
                record = self.mydata.GetEmptyRecord()
                for column in columns:
                    record['data'][column] = self.inputfield['combobox']['widgets'][column]['combobox'].get()
                self.mydata.PushbackRecords([record])
            elif isViewerFieldFocused:
                records = []
                for i in range(0, len(self.viewerfield), 1):
                    record = self.viewerfield[i]['record']
                    for column in columns:
                        record['data'][column] = self.viewerfield[i]['combobox']['widgets'][column]['combobox'].get()
                    records.append(record)
                self.mydata.ReplaceRecords(records)
        elif event.keysym == 'd':
            length = len(self.mydata.GetRecords())
            self.viewerstart += 1
            if self.viewerstart < 0:
                self.viewerstart = 0
            elif length <= self.viewerstart + 10:
                self.viewerstart = length - 10
        elif event.keysym == 'u':
            length = len(self.mydata.GetRecords())
            self.viewerstart -= 1
            if self.viewerstart < 0:
                self.viewerstart = 0
            elif length <= self.viewerstart + 10:
                self.viewerstart = length - 10
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

    # # メインループ
    root.mainloop()
# ===================================================================================