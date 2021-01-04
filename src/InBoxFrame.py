# ===================================================================================
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
class InBoxFrame(tk.Frame):
    def __init__(self, master, memodata, tododata, donedata ,cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.memodata = memodata
        self.memodata.AddOnUpdateCallback(self.InitializeToDoList)
        self.tododata = tododata
        self.donedata = donedata
        self.num = 1
        self.todolist = []
        self.buttonlist = []
        self.v1 = tk.StringVar()

        # combobox1
        label1 = tk.Label(self, text='project')
        self.v1 = tk.StringVar()
        cb1 = ttk.Combobox(self, textvariable=self.v1)
        label1.place(relx=0,rely=0,relwidth=0.2,relheight=0.1)
        cb1.place(relx=0.2,rely=0,relwidth=0.8,relheight=0.1)
        self.label1 = label1
        self.cb1 = cb1

        # combobox2
        label2 = tk.Label(self, text='todo')
        self.v2 = tk.StringVar()
        cb2 = ttk.Combobox(self, textvariable=self.v2)
        label2.place(relx=0,rely=0.1,relwidth=0.2,relheight=0.1)
        cb2.place(relx=0.2,rely=0.1,relwidth=0.8,relheight=0.1)
        self.label2 = label2
        self.cb2 = cb2

        self.InitializeToDoList()
# ===================================================================================
    def drawToDoList(self):
        lines = self.tododata.GetAllRecordsByColumn('todo')
        for line in lines:
            # テキストボックスの値を取得
            task = tk.StringVar()
            task.set(line)

            # 新規タスクを追加
            todo = tk.Label(self, textvariable=task)
            todo.place(rely=self.num*0.03+0.2, relx=0, relwidth=0.6)
            self.todolist.append(todo)

            # 新規タスクの削除ボタンを追加
            button = tk.Button(self, text="DONE "+ str(self.num), highlightbackground='gray')
            button.bind("<Button-1>", self.CompleteToDo)
            button.bind("<Return>", self.CompleteToDo)
            button.place(rely=self.num*0.03+0.2, relx=0.6, relwidth=0.2)
            self.buttonlist.append(button)

            self.num += 1
# ===================================================================================
    def CompleteToDo(self, event):
        deletenum = int(event.widget["text"].split(" ")[1])
        index = deletenum-1
        lines = self.tododata.GetAllRecordsByColumn('todo')
        self.memodata.InsertRecordWithDate(self.cb1.get(),lines[index],"DONE : "+lines[index])
        self.tododata.DeleteRecordByIndex(index)
        self.donedata.InsertRecordWithDate(lines[index])
        self.InitializeToDoList()
# ===================================================================================
    def InitializeToDoList(self):
        self.num = 1
        for todo in self.todolist:
            todo.place_forget()
            todo.destroy()
        for button in self.buttonlist:
            button.place_forget()
            button.destroy()
        records = self.memodata.GetAllRecordsByColumn('project')
        records = list(dict.fromkeys(records))
        self.cb1.configure(values=records)
        self.cb1.set(self.memodata.GetLastRecordsByColumn('project'))
        records = self.tododata.GetAllRecordsByColumn('todo')
        records = list(dict.fromkeys(records))
        self.cb2.configure(values=records)
        self.cb2.set("")
        self.todolist = []
        self.buttonlist = []
        self.drawToDoList()
# ===================================================================================
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            if self.cb2 == self.master.focus_get() and self.cb2.get() != "":
                project = self.cb1.get()
                task = self.cb2.get()
                self.tododata.InsertRecordWithDate(task)
                self.memodata.InsertRecordWithDate(project, task, "TODO : "+task)
                self.InitializeToDoList()
                self.cb2.set("")
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    memodata = MyDataBase("../data/memo.txt", ['project', 'task', 'memo'])
    tododata = MyDataBase("../data/todo.txt", ['todo'])
    donedata = MyDataBase("../data/done.txt", ['done'])
    inboxframe = InBoxFrame(root, memodata, tododata, donedata)
    framecompose.AddFrame(inboxframe, 'inboxframe', key=inboxframe.OnKeyEvent)

    # メインループ
    root.mainloop()
# ===================================================================================