
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
        self.tododata = tododata
        self.donedata = donedata
        self.todolist = []
        self.InitializeStaticWidget()
        self.InitializeDynamicWidget()
# ===================================================================================
    def InitializeStaticWidget(self):
        # combobox1
        label1 = tk.Label(self, text='project')
        self.v1 = tk.StringVar()
        cb1 = ttk.Combobox(self, textvariable=self.v1)
        self.label1 = label1
        self.cb1 = cb1
        # combobox2
        label2 = tk.Label(self, text='todo')
        self.v2 = tk.StringVar()
        cb2 = ttk.Combobox(self, textvariable=self.v2)
        self.label2 = label2
        self.cb2 = cb2
        # Combobox3
        label3 = tk.Label(self, text='year')
        self.v3 = tk.StringVar()
        cb3 = ttk.Combobox(self, textvariable=self.v3)
        self.label3 = label3
        self.cb3 = cb3
        # combobox4
        label4 = tk.Label(self, text='month')
        self.v4 = tk.StringVar()
        cb4 = ttk.Combobox(self, textvariable=self.v4)
        self.label4 = label4
        self.cb4 = cb4
        # combobox5
        label5 = tk.Label(self, text='date')
        self.v5 = tk.StringVar()
        cb5 = ttk.Combobox(self, textvariable=self.v5)
        self.label5 = label5
        self.cb5 = cb5
        # combobox6
        label6 = tk.Label(self, text='hour')
        self.v6 = tk.StringVar()
        cb6 = ttk.Combobox(self, textvariable=self.v6)
        self.label6 = label6
        self.cb6 = cb6
        # combobox7
        label7 = tk.Label(self, text='minute')
        self.v7 = tk.StringVar()
        cb7 = ttk.Combobox(self, textvariable=self.v7)
        self.label7 = label7
        self.cb7 = cb7
        self.UpdateStaticWidgetProperty()
        self.PlaceStaticWidget()
# ===================================================================================
    def PlaceStaticWidget(self):
        # combobox1
        self.label1.place(relx=0,rely=0,relwidth=0.2,relheight=0.05)
        self.cb1.place(relx=0.2,rely=0,relwidth=0.8,relheight=0.05)
        # combobox2
        self.label2.place(relx=0,rely=0.05,relwidth=0.2,relheight=0.05)
        self.cb2.place(relx=0.2,rely=0.05,relwidth=0.8,relheight=0.05)
        # combobox3
        self.label3.place(relx=0,rely=0.1,relwidth=0.2,relheight=0.05)
        self.cb3.place(relx=0.2,rely=0.1,relwidth=0.8,relheight=0.05)
        # combobox4
        self.label4.place(relx=0,rely=0.15,relwidth=0.2,relheight=0.05)
        self.cb4.place(relx=0.2,rely=0.15,relwidth=0.8,relheight=0.05)
        # combobox5
        self.label5.place(relx=0,rely=0.2,relwidth=0.2,relheight=0.05)
        self.cb5.place(relx=0.2,rely=0.2,relwidth=0.8,relheight=0.05)
        # combobox6
        self.label6.place(relx=0,rely=0.25,relwidth=0.2,relheight=0.05)
        self.cb6.place(relx=0.2,rely=0.25,relwidth=0.8,relheight=0.05)
        # combobox7
        self.label7.place(relx=0,rely=0.3,relwidth=0.2,relheight=0.05)
        self.cb7.place(relx=0.2,rely=0.3,relwidth=0.8,relheight=0.05)
# ===================================================================================
    def UpdateStaticWidgetProperty(self):
        # combobox1
        records = self.memodata.GetAllRecordsByColumn('project')
        records = list(dict.fromkeys(records))
        self.cb1.configure(values=records)
        self.cb1.set(self.memodata.GetLastRecordsByColumn('project'))
        # combobox1
        records = self.tododata.GetAllRecordsByColumn('todo')
        records = list(dict.fromkeys(records))
        self.cb2.configure(values=records)
        self.cb2.set("")
        # combobox3
        records = self.tododata.GetAllRecordsByColumn('year')
        records = list(dict.fromkeys(records))
        self.cb3.configure(values=records)
        self.cb3.set(self.tododata.GetLastRecordsByColumn('year'))
        # combobox4
        records = self.tododata.GetAllRecordsByColumn('month')
        records = list(dict.fromkeys(records))
        self.cb4.configure(values=records)
        self.cb4.set(self.tododata.GetLastRecordsByColumn('month'))
        # combobox5
        records = self.tododata.GetAllRecordsByColumn('date')
        records = list(dict.fromkeys(records))
        self.cb5.configure(values=records)
        self.cb5.set(self.tododata.GetLastRecordsByColumn('date'))
        # combobox6
        records = self.tododata.GetAllRecordsByColumn('hour')
        records = list(dict.fromkeys(records))
        self.cb6.configure(values=records)
        self.cb6.set(self.tododata.GetLastRecordsByColumn('hour'))
        # combobox7
        records = self.tododata.GetAllRecordsByColumn('minute')
        records = list(dict.fromkeys(records))
        self.cb7.configure(values=records)
        self.cb7.set(self.tododata.GetLastRecordsByColumn('minute'))
# ===================================================================================
    def InitializeDynamicWidget(self):
        for todo in self.todolist:
            for widget in todo[1]:
                widget.place_forget()
                widget.destroy()
        self.todolist = []
        self.buttonlist = []
        self.UpdateDynamicWidgetProperty()
        self.PlaceDynamicWidget()
# ===================================================================================
    def PlaceDynamicWidget(self):
        num = 1
        records = self.tododata.GetAllRecords(sort='project')
        for record in records:

            # プロジェクトを表示
            projecttext = tk.StringVar()
            project = tk.Label(self, textvariable=projecttext)
            project.place(rely=num*0.03+0.35, relx=0, relwidth=0.1)

            # タスクを表示
            todotext = tk.StringVar()
            todo = tk.Label(self, textvariable=todotext)
            todo.place(rely=num*0.03+0.35, relx=0.1, relwidth=0.4)

            # 残り時間を表示
            remaintext = tk.StringVar()
            remain = tk.Label(self, textvariable=remaintext)
            remain.place(rely=num*0.03+0.35, relx=0.5, relwidth=0.2)

            # 新規タスクの削除ボタンを追加
            button = tk.Button(self, text="DONE "+ str(num), highlightbackground='gray')
            button.bind("<Button-1>", self.CompleteToDo)
            button.bind("<Return>", self.CompleteToDo)
            button.place(rely=num*0.03+0.35, relx=0.7, relwidth=0.1)

            # 各タスクのメモ入力ボックスを表示
            memo = tk.Entry(self)
            memo.place(rely=num*0.03+0.35, relx=0.8, relwidth=0.2)

            # Separatorを表示
            separator = ttk.Separator(self)
            separator.place(rely=num*0.03+0.35, relx=0, relwidth=1)

            self.todolist.append([num, [project, todo, remain, button, memo, separator], record])

            num += 1
# ===================================================================================
    def UpdateDynamicWidgetProperty(self):
        for todo in self.todolist:
            projecttext = tk.StringVar()
            projecttext.set(todo[2].split("\t")[3])
            todo[1][0].configure(textvariable=projecttext)
            todotext = tk.StringVar()
            todotext.set(todo[2].split("\t")[4])
            todo[1][1].configure(textvariable=todotext)
            remaintext = tk.StringVar()
            year = int(todo[2].split("\t")[5])
            month = int(todo[2].split("\t")[6])
            date = int(todo[2].split("\t")[7])
            hour = int(todo[2].split("\t")[8])
            minute = int(todo[2].split("\t")[9])
            text = str(datetime.datetime(year, month, date, hour, minute, 0) - datetime.datetime.now())
            text = text[:text.rfind(".")]
            remaintext.set(text)
            todo[1][2].configure(textvariable=remaintext)
# ===================================================================================
    def CompleteToDo(self, event):
        for todo in self.todolist:
            if todo[1][3] == event.widget:
                deletenum = todo[0]
        index = deletenum-1
        lines = self.tododata.GetAllRecordsByColumn('todo')
        projects = self.tododata.GetAllRecordsByColumn('project')
        self.memodata.InsertRecordWithDate(projects[index],lines[index],"DONE : "+lines[index])
        self.tododata.DeleteRecordByIndex(index)
        self.donedata.InsertRecordWithDate(lines[index])
        self.InitializeDynamicWidget()
# ===================================================================================
    def OnTick(self):
        self.UpdateDynamicWidgetProperty()
# ===================================================================================
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            if self.cb2 == self.master.focus_get() and self.cb2.get() != "":
                project = self.cb1.get()
                task = self.cb2.get()
                year = self.cb3.get()
                month = self.cb4.get()
                date = self.cb5.get()
                hour = self.cb6.get()
                minute = self.cb7.get()
                self.tododata.InsertRecordWithDate(project, task, year, month, date, hour, minute)
                self.memodata.InsertRecordWithDate(project, task, "TODO : "+task)
                self.InitializeDynamicWidget()
                self.UpdateStaticWidgetProperty()
            else:
                for todo in self.todolist:
                    if todo[1][4] == self.master.focus_get() and todo[1][4].get() != "":
                        index = todo[0] -1
                        lines = self.tododata.GetAllRecordsByColumn('todo')
                        projects = self.tododata.GetAllRecordsByColumn('project')
                        self.memodata.InsertRecordWithDate(projects[index], lines[index], todo[1][4].get())
                        todo[1][4].delete(0,'end')
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    memodata = MyDataBase("../data/memo.txt", ['project', 'task', 'memo'])
    tododata = MyDataBase("../data/todo.txt", ['project', 'todo', 'year', 'month', 'date', 'hour', 'minute'])
    donedata = MyDataBase("../data/done.txt", ['done'])
    inboxframe = InBoxFrame(root, memodata, tododata, donedata)
    framecompose.AddFrame(inboxframe, 'inboxframe', key=inboxframe.OnKeyEvent, time=inboxframe.OnTick)

    # メインループ
    root.mainloop()
# ===================================================================================