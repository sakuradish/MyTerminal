# ===================================================================================
import tkinter as tk
from ComposeFrame import ComposeFrame
from MyDataBase import MyDataBase
from MyLogger import mylogger
# ===================================================================================
import datetime
import tkinter as tk
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
import time
import glob
import os
# ===================================================================================
class ExplorerFrame(tk.Frame):
    @mylogger.deco
    def __init__(self,master, explorerdata, cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.explorerdata = explorerdata
        self.InitializeStaticWidget()
        self.PlaceStaticWidget()
        self.UpdateStaticWidgetProperty()
# ===================================================================================
    @mylogger.deco
    def InitializeStaticWidget(self):
        # combobox1
        label1 = tk.Label(self, text='output')
        self.v1 = tk.StringVar()
        cb1 = ttk.Combobox(self, textvariable=self.v1)
        self.label1 = label1
        self.cb1 = cb1
        self.cb1.set(os.getcwd())
        # text
        my_font = font.Font(self.master ,family=u'ＭＳ ゴシック',size=8)
        text = tk.Text(self,wrap=tk.CHAR,undo=True, bg='black',font=my_font, foreground='white', insertbackground='white')
        x_sb = tk.Scrollbar(self,orient='horizontal')
        y_sb = tk.Scrollbar(self,orient='vertical')
        x_sb.config(command=text.xview)
        y_sb.config(command=text.yview)
        text.config(xscrollcommand=x_sb.set,yscrollcommand=y_sb.set)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.x_sb = x_sb
        self.y_sb = y_sb
        self.text = text
# ===================================================================================
    @mylogger.deco
    def PlaceStaticWidget(self):
        self.label1.place(relx=0,rely=0,relwidth=0.2,relheight=0.05)
        self.cb1.place(relx=0.2,rely=0,relwidth=0.8,relheight=0.05)
        self.text.place(relx=0,rely=0.05,relwidth=0.95,relheight=0.85)
        self.x_sb.place(relx=0,rely=0.9,relwidth=0.95,relheight=0.05)
        self.y_sb.place(relx=0.95,rely=0.05,relwidth=0.05,relheight=0.85)
# ===================================================================================
    @mylogger.deco
    def UpdateStaticWidgetProperty(self, event=None):
        print("nothing to update")
        # # text
        # self.text.configure(state='normal')
        # self.text.delete('1.0','end')
        # for record in self.explorerdata.GetAllRecords(filter={'path':self.cb2.get()}):
        #     self.text.insert('end', self.explorerdata.ConvertRecordToString(record) + "\n")
        # self.text.see('end')
        # self.text.configure(state='disabled')
        # combobox1
        # records = self.explorerdata.GetAllRecordsByColumn('base')
        # records = [record['data']['base'] for record in records]
        # records = list(dict.fromkeys(records))
        # self.cb1.configure(values=records)
        # combobox2
        # records = self.explorerdata.GetAllRecordsByColumn('base')
        # records = [record['data']['base'] for record in records]
        # records = list(dict.fromkeys(records))
        # self.cb2.configure(values=records)
# ===================================================================================
    @mylogger.deco
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            if self.cb1 == self.master.focus_get() and self.cb1.get() != "":
                # self.Glob(self.cb1.get())
                try:
                    with open(self.cb1.get(), 'w', encoding='utf-8') as f:
                        f.write("@startuml\n")
                        f.write("'#########################################################\n")
                        f.write("!include definition.pu\n")
                        f.write("'#########################################################\n")
                        f.write("activate DomainNameHere\n")
                        f.write("a->b:c\n")
                        # f.write(self.text.get(1.0, 'end-1c'))
                        for l in self.text.get(1.0, 'end-1c').split("\n"):
                            if l.find("if ") != -1:
                                l = "alt " + l
                            elif l.find("for ") != -1:
                                l = "loop " + l
                            f.write(l + "\n")
                        f.write("Deactivate DomainNameHere\n")
                        f.write("'#########################################################\n")
                        f.write("@enduml\n")
                except:
                    print("failed to draft PlantUML")
                self.UpdateStaticWidgetProperty()
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    explorerdata = MyDataBase("../data/explorer.txt", ['base', 'path', 'update', 'size'])
    explorerframe = ExplorerFrame(root, explorerdata)
    framecompose.AddFrame(explorerframe, 'explorerframe', key=explorerframe.OnKeyEvent)

    # メインループ
    root.mainloop()
# ===================================================================================