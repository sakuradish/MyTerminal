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
# ===================================================================================
class MemoFrame(tk.Frame):
    def __init__(self,master, memodata, tododata, cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.memodata = memodata
        self.memodata.AddOnUpdateCallback(self.UpdateText)
        self.tododata = tododata
        self.tododata.AddOnUpdateCallback(self.UpdateText)
        self.draw()
    def draw(self):
        # text
        my_font = font.Font(self.master ,family=u'ＭＳ ゴシック',size=14)
        text = tk.Text(self,wrap=tk.CHAR,undo=True, bg='black',font=my_font, foreground='white', insertbackground='white')
        x_sb = tk.Scrollbar(self,orient='horizontal')
        y_sb = tk.Scrollbar(self,orient='vertical')
        x_sb.config(command=text.xview)
        y_sb.config(command=text.yview)
        text.config(xscrollcommand=x_sb.set,yscrollcommand=y_sb.set)
        text.place(relx=0,rely=0,relwidth=0.97,relheight=0.77)
        x_sb.place(relx=0,rely=0.77,relwidth=0.97,relheight=0.03)
        y_sb.place(relx=0.97,rely=0,relwidth=0.03,relheight=0.77)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.x_sb = x_sb
        self.y_sb = y_sb
        self.text = text

        # combobox1
        label1 = tk.Label(self, text='project')
        self.v1 = tk.StringVar()
        cb1 = ttk.Combobox(self, textvariable=self.v1)
        label1.place(relx=0,rely=0.85,relwidth=0.2,relheight=0.05)
        cb1.place(relx=0.2,rely=0.85,relwidth=0.8,relheight=0.05)
        self.label1 = label1
        self.cb1 = cb1

        # combobox2
        label2 = tk.Label(self, text='task')
        self.v2 = tk.StringVar()
        cb2 = ttk.Combobox(self, textvariable=self.v2)
        label2.place(relx=0,rely=0.9,relwidth=0.2,relheight=0.05)
        cb2.place(relx=0.2,rely=0.9,relwidth=0.8,relheight=0.05)
        self.label2 = label2
        self.cb2 = cb2

        # combobox3
        label3 = tk.Label(self, text='memo')
        self.v3 = tk.StringVar()
        cb3 = ttk.Combobox(self, textvariable=self.v3)
        label3.place(relx=0,rely=0.95,relwidth=0.2,relheight=0.05)
        cb3.place(relx=0.2,rely=0.95,relwidth=0.8,relheight=0.05)
        self.label3 = label3
        self.cb3 = cb3

        self.UpdateText()
# ===================================================================================
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            if self.cb1 == self.master.focus_get() or \
               self.cb2 == self.master.focus_get() or \
               self.cb3 == self.master.focus_get():
                self.UpdateText()
# ===================================================================================
    def UpdateText(self):
        self.text.configure(state='normal')
        self.text.delete('1.0','end')
        for record in self.memodata.GetAllRecords():
            # self.master.update()
            if record['data']['project'].find(self.cb1.get()) != -1 and \
               record['data']['task'].find(self.cb2.get()) != -1 and \
               record['data']['memo'].find(self.cb3.get()) != -1:
                self.text.insert('end', self.memodata.ConvertRecordToString(record) + "\n")
        self.text.see('end')
        self.text.configure(state='disabled')
        records = self.memodata.GetAllRecordsByColumn('project')
        records = [record['data']['project'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb1.configure(values=records)
        # self.cb1.set("")
        records = self.tododata.GetAllRecordsByColumn('todo')
        records = [record['data']['todo'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb2.configure(values=records)
        # self.cb2.set("")
        records = self.memodata.GetAllRecordsByColumn('memo')
        records = [record['data']['memo'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb3.configure(values=records)
        # self.cb3.set("")
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    memodata = MyDataBase("../data/memo.txt", ['project', 'task', 'memo'])
    tododata = MyDataBase("../data/todo.txt", ['project', 'todo', 'year', 'month', 'date', 'hour', 'minute', 'state'])
    memoframe = MemoFrame(root, memodata, tododata)
    framecompose.AddFrame(memoframe, 'memoframe', key=memoframe.OnKeyEvent)

    # メインループ
    root.mainloop()
# ===================================================================================