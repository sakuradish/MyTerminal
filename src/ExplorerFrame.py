# ===================================================================================
import tkinter as tk
from ComposeFrame import ComposeFrame
from MyDataBase import MyDataBase
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
    def __init__(self,master, explorerdata, cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.explorerdata = explorerdata
        self.InitializeStaticWidget()
        self.PlaceStaticWidget()
        self.UpdateStaticWidgetProperty()
# ===================================================================================
    def InitializeStaticWidget(self):
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
        # combobox1
        label1 = tk.Label(self, text='base')
        self.v1 = tk.StringVar()
        cb1 = ttk.Combobox(self, textvariable=self.v1)
        self.label1 = label1
        self.cb1 = cb1
        self.cb1.set(os.getcwd())
        # combobox2
        label2 = tk.Label(self, text='filter')
        self.v2 = tk.StringVar()
        cb2 = ttk.Combobox(self, textvariable=self.v2)
        self.label2 = label2
        self.cb2 = cb2
# ===================================================================================
    def PlaceStaticWidget(self):
        self.label1.place(relx=0,rely=0,relwidth=0.2,relheight=0.05)
        self.cb1.place(relx=0.2,rely=0,relwidth=0.8,relheight=0.05)
        self.text.place(relx=0,rely=0.05,relwidth=0.95,relheight=0.85)
        self.x_sb.place(relx=0,rely=0.9,relwidth=0.95,relheight=0.05)
        self.y_sb.place(relx=0.95,rely=0.05,relwidth=0.05,relheight=0.85)
        self.label2.place(relx=0,rely=0.95,relwidth=0.2,relheight=0.05)
        self.cb2.place(relx=0.2,rely=0.95,relwidth=0.8,relheight=0.05)
# ===================================================================================
    def UpdateStaticWidgetProperty(self, event=None):
        # text
        self.text.configure(state='normal')
        self.text.delete('1.0','end')
        for record in self.explorerdata.GetAllRecords(filter={'path':self.cb2.get()}):
            self.text.insert('end', self.explorerdata.ConvertRecordToString(record) + "\n")
        self.text.see('end')
        self.text.configure(state='disabled')
        # combobox1
        records = self.explorerdata.GetAllRecordsByColumn('base')
        records = [record['data']['base'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb1.configure(values=records)
        # combobox2
        records = self.explorerdata.GetAllRecordsByColumn('base')
        records = [record['data']['base'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb2.configure(values=records)
# ===================================================================================
    def Glob(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            os.system("start " + path)
            Checked = {}
            basedirs = [path]
            while 1:
                NotChecked = [basedir for basedir in basedirs if not basedir in Checked]
                if not NotChecked:
                    break
                for basedir in NotChecked:
                    Checked[basedir] = True
                    try:
                        files = [file for file in glob.glob(basedir + "/*", recursive=False) if os.path.isfile(file)]
                        dirs = [dir for dir in glob.glob(basedir + "/*", recursive=False) if os.path.isdir(dir)]
                        basedirs += dirs
                        for file in files:
                            print(file)
                            update = datetime.datetime.fromtimestamp(os.stat(file).st_mtime)
                            update = update.strftime('%Y/%m/%d')
                            size = str(os.stat(file).st_size)
                            self.explorerdata.InsertRecordWithLogInfo([self.cb1.get(), file, update, size])
                    except:
                        update = datetime.datetime.fromtimestamp(os.stat(basedir).st_mtime)
                        update = update.strftime('%Y/%m/%d')
                        size = str(os.stat(basedir).st_size)
                        self.explorerdata.InsertRecordWithLogInfo([self.cb1.get(), basedir, update, size])
                        print(basedir+" can not glob for some error")
# ===================================================================================
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            if self.cb1 == self.master.focus_get() and self.cb1.get() != "":
                self.Glob(self.cb1.get())
                self.UpdateStaticWidgetProperty()
            elif self.cb2 == self.master.focus_get():
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