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
class InBoxFrame(tk.Frame):
    @mylogger.deco
    def __init__(self, master, memodata, tododata, tasklog ,cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.memodata = memodata
        self.tododata = tododata
        self.tasklog = tasklog
        self.todolist = []
        self.itemnum = 18
        self.InitializeStaticWidget()
        self.InitializeDynamicWidget()
# ===================================================================================
    @mylogger.deco
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
        # sort
        label8 = tk.Label(self, text='sort')
        self.v8 = tk.StringVar()
        cb8 = ttk.Combobox(self, textvariable=self.v8)
        self.label8 = label8
        self.cb8 = cb8
        # state
        label9 = tk.Label(self, text='表示state')
        self.v8 = tk.StringVar()
        cb9 = ttk.Combobox(self, textvariable=self.v8)
        self.label9 = label9
        self.cb9 = cb9
        # how many item show at one time
        totalpage = tk.Label(self)
        v = tk.StringVar()
        v.set('1')
        totalpage.configure(textvariable=v)
        pagelavel1 = tk.Label(self, text='ページ中')
        currentpage = tk.Entry(self)
        currentpage.insert(0, '1')
        pagelavel2 = tk.Label(self, text='ページ目を表示中')
        self.totalpage = totalpage
        self.pagelavel1 = pagelavel1
        self.currentpage = currentpage
        self.pagelavel2 = pagelavel2
        # prev page button
        prev = tk.Button(self, text="prev", highlightbackground='gray')
        prev.bind("<Button-1>", self.PagePrev)
        prev.bind("<Return>", self.PagePrev)
        self.prev = prev
        # next page button
        next = tk.Button(self, text="next", highlightbackground='gray')
        next.bind("<Button-1>", self.PageNext)
        next.bind("<Return>", self.PageNext)
        self.next = next

        self.UpdateStaticWidgetProperty()
        self.PlaceStaticWidget()
# ===================================================================================
    @mylogger.deco
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
        # sort
        self.label8.place(relx=0.2,rely=0.35,relwidth=0.1,relheight=0.05)
        self.cb8.place(relx=0.3,rely=0.35,relwidth=0.05,relheight=0.05)
        # state
        self.label9.place(relx=0.35,rely=0.35,relwidth=0.1,relheight=0.05)
        self.cb9.place(relx=0.45,rely=0.35,relwidth=0.05,relheight=0.05)
        # how many item show at one time
        self.totalpage.place(relx=0.5,rely=0.35,relwidth=0.05,relheight=0.05)
        self.pagelavel1.place(relx=0.55,rely=0.35,relwidth=0.1,relheight=0.05)
        self.currentpage.place(relx=0.65,rely=0.35,relwidth=0.05,relheight=0.05)
        self.pagelavel2.place(relx=0.7,rely=0.35,relwidth=0.1,relheight=0.05)
        # prev page button
        self.prev.place(relx=0.8,rely=0.35,relwidth=0.1,relheight=0.05)
        # next page button
        self.next.place(relx=0.9,rely=0.35,relwidth=0.1,relheight=0.05)
# ===================================================================================
    @mylogger.deco
    def UpdateStaticWidgetProperty(self):
        if self.tododata.GetAllRecords():
            # combobox1
            records = self.tododata.GetAllRecordsByColumn('project')
            records = [record['data']['project'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb1.configure(values=records)
            self.cb1.set(self.tododata.GetLastRecordsByColumn('project')['data']['project'])
            # combobox1
            records = self.tododata.GetAllRecordsByColumn('todo')
            records = [record['data']['todo'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb2.configure(values=records)
            self.cb2.set("")
            # combobox3
            records = self.tododata.GetAllRecordsByColumn('year')
            records = [record['data']['year'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb3.configure(values=records)
            self.cb3.set(self.tododata.GetLastRecordsByColumn('year')['data']['year'])
            # combobox4
            records = self.tododata.GetAllRecordsByColumn('month')
            records = [record['data']['month'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb4.configure(values=records)
            self.cb4.set(self.tododata.GetLastRecordsByColumn('month')['data']['month'])
            # combobox5
            records = self.tododata.GetAllRecordsByColumn('date')
            records = [record['data']['date'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb5.configure(values=records)
            self.cb5.set(self.tododata.GetLastRecordsByColumn('date')['data']['date'])
            # combobox6
            records = self.tododata.GetAllRecordsByColumn('hour')
            records = [record['data']['hour'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb6.configure(values=records)
            self.cb6.set(self.tododata.GetLastRecordsByColumn('hour')['data']['hour'])
            # combobox7
            records = self.tododata.GetAllRecordsByColumn('minute')
            records = [record['data']['minute'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb7.configure(values=records)
            self.cb7.set(self.tododata.GetLastRecordsByColumn('minute')['data']['minute'])
            # sort
            records = self.tododata.GetDataColumns()
            self.cb8.configure(values=records)
            # state
            records = self.tododata.GetAllRecordsByColumn('state')
            records = [record['data']['state'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb9.configure(values=records)
# ===================================================================================
    @mylogger.deco
    def InitializeDynamicWidget(self):
        for todo in self.todolist:
            for widget in todo['widgets'].values():
                widget.place_forget()
                widget.destroy()
        self.todolist = []
        # リストを更新
        sort = self.cb8.get()
        if sort == "":
            sort == "project"
        records = self.tododata.GetAllRecords(sort=sort)
        for record in records:
            # プロジェクトを表示
            projecttext = tk.StringVar()
            project = tk.Label(self, textvariable=projecttext)
            # タスクを表示
            todotext = tk.StringVar()
            todo = tk.Label(self, textvariable=todotext)
            # 残り時間を表示
            remaintext = tk.StringVar()
            remain = tk.Label(self, textvariable=remaintext)
            # statusを表示
            statetext = tk.StringVar()
            status = tk.Label(self, textvariable=statetext)
            # OPENボタンを追加
            openbtn = tk.Button(self, text="OPEN", highlightbackground='gray')
            openbtn.bind("<Button-1>", self.OnOpenBtn)
            openbtn.bind("<Return>", self.OnOpenBtn)
            # DOINGボタンを追加
            doingbtn = tk.Button(self, text="DOING", highlightbackground='gray')
            doingbtn.bind("<Button-1>", self.OnDoingBtn)
            doingbtn.bind("<Return>", self.OnDoingBtn)
            # DONEボタンを追加
            donebtn = tk.Button(self, text="DONE", highlightbackground='gray')
            donebtn.bind("<Button-1>", self.OnDoneBtn)
            donebtn.bind("<Return>", self.OnDoneBtn)
            # 各タスクのメモ入力ボックスを表示
            memo = tk.Entry(self)
            # Separatorを表示
            separator = ttk.Separator(self)
            widgets = {'project':project, 'todo':todo, 'remain':remain, 'openbtn':openbtn, 'doingbtn':doingbtn, 'donebtn':donebtn, 'memo':memo, 'separator':separator, 'state':status}
            self.todolist.append({'widgets':widgets, 'record':record})
        self.UpdateDynamicWidgetProperty()
        self.PlaceDynamicWidget()
# ===================================================================================
    @mylogger.deco
    def PlaceDynamicWidget(self):
        # stateがOPENのものだけ表示
        records = []
        for todo in self.todolist:
            state = self.cb9.get()
            if state == "":
                state = "DOING"
            if todo['record']['data']['state'] == state:
                records.append(todo)
        recordnum = len(records)
        # 最大ページ数の表示をついでに更新
        totalpage = tk.StringVar()
        text = str(math.ceil(recordnum / self.itemnum))
        totalpage.set(text)
        self.totalpage.configure(textvariable=totalpage)
        # 現在ページ向けの開始・終了インデックスを算出
        start = (int(self.currentpage.get())-1) * self.itemnum
        end = start + self.itemnum
        if len(records) <= end:
            end = len(records)
        # 部品配置
        count = 1
        for num in range(start, end, 1):
            records[num]['widgets']['project'].place(rely=count*0.03+0.4, relx=0, relwidth=0.1)
            records[num]['widgets']['todo'].place(rely=count*0.03+0.4, relx=0.1, relwidth=0.4)
            records[num]['widgets']['remain'].place(rely=count*0.03+0.4, relx=0.5, relwidth=0.15)
            records[num]['widgets']['state'].place(rely=count*0.03+0.4, relx=0.65, relwidth=0.05)
            records[num]['widgets']['openbtn'].place(rely=count*0.03+0.4, relx=0.7, relwidth=0.03)
            records[num]['widgets']['doingbtn'].place(rely=count*0.03+0.4, relx=0.73, relwidth=0.03)
            records[num]['widgets']['donebtn'].place(rely=count*0.03+0.4, relx=0.76, relwidth=0.03)
            records[num]['widgets']['memo'].place(rely=count*0.03+0.4, relx=0.8, relwidth=0.2)
            records[num]['widgets']['separator'].place(rely=count*0.03+0.4, relx=0, relwidth=1)
            count += 1
# ===================================================================================
    @mylogger.deco
    def UpdateDynamicWidgetProperty(self):
        for todo in self.todolist:
            projecttext = tk.StringVar()
            projecttext.set(todo['record']['data']['project'])
            todo['widgets']['project'].configure(textvariable=projecttext)
            todotext = tk.StringVar()
            todotext.set(todo['record']['data']['todo'])
            todo['widgets']['todo'].configure(textvariable=todotext)
            remaintext = tk.StringVar()
            year = int(todo['record']['data']['year'])
            month = int(todo['record']['data']['month'])
            date = int(todo['record']['data']['date'])
            hour =int(todo['record']['data']['hour'])
            minute = int(todo['record']['data']['minute'])
            text = str(datetime.datetime(year, month, date, hour, minute, 0) - datetime.datetime.now())
            text = text[:text.rfind(".")]
            remaintext.set(text)
            todo['widgets']['remain'].configure(textvariable=remaintext)
            statetext = tk.StringVar()
            statetext.set(todo['record']['data']['state'])
            todo['widgets']['state'].configure(textvariable=statetext)
# ===================================================================================
    @mylogger.deco
    def PagePrev(self, event):
        total = int(self.totalpage.cget('text'))
        current = int(self.currentpage.get())
        if 1 < current:
            current -= 1
            self.currentpage.delete(0, 'end')
            self.currentpage.insert(0, str(current))
            self.InitializeDynamicWidget()
            self.UpdateStaticWidgetProperty()
# ===================================================================================
    @mylogger.deco
    def PageNext(self, event):
        total = int(self.totalpage.cget('text'))
        current = int(self.currentpage.get())
        if current < total:
            current += 1
            self.currentpage.delete(0, 'end')
            self.currentpage.insert(0, str(current))
            self.InitializeDynamicWidget()
            self.UpdateStaticWidgetProperty()
# ===================================================================================
    @mylogger.deco
    def OnOpenBtn(self, event):
        for todo in self.todolist:
            if todo['widgets']['openbtn'] == event.widget:
                index = todo['record']['index']
        project = self.tododata.GetAllRecordsByColumn('project')[index]['data']['project']
        todo = self.tododata.GetAllRecordsByColumn('todo')[index]['data']['todo']
        year = self.tododata.GetAllRecordsByColumn('year')[index]['data']['year']
        month = self.tododata.GetAllRecordsByColumn('month')[index]['data']['month']
        date = self.tododata.GetAllRecordsByColumn('date')[index]['data']['date']
        hour = self.tododata.GetAllRecordsByColumn('hour')[index]['data']['hour']
        minute = self.tododata.GetAllRecordsByColumn('minute')[index]['data']['minute']
        # self.memodata.InsertRecordWithLogInfo(project[index],todo[index],"DONE : "+todo[index])
        self.tododata.DeleteRecordByIndex(index)
        self.tododata.InsertRecordWithLogInfo([project,todo,year,month,date,hour,minute,"OPEN"])
        self.tasklog.InsertRecordWithLogInfo([project,todo,"OPEN"])
        self.UpdateStaticWidgetProperty()
        self.InitializeDynamicWidget()
# ===================================================================================
    @mylogger.deco
    def OnDoingBtn(self, event):
        for todo in self.todolist:
            if todo['widgets']['doingbtn'] == event.widget:
                index = todo['record']['index']
        project = self.tododata.GetAllRecordsByColumn('project')[index]['data']['project']
        todo = self.tododata.GetAllRecordsByColumn('todo')[index]['data']['todo']
        year = self.tododata.GetAllRecordsByColumn('year')[index]['data']['year']
        month = self.tododata.GetAllRecordsByColumn('month')[index]['data']['month']
        date = self.tododata.GetAllRecordsByColumn('date')[index]['data']['date']
        hour = self.tododata.GetAllRecordsByColumn('hour')[index]['data']['hour']
        minute = self.tododata.GetAllRecordsByColumn('minute')[index]['data']['minute']
        # self.memodata.InsertRecordWithLogInfo(project[index],todo[index],"DONE : "+todo[index])
        self.tododata.DeleteRecordByIndex(index)
        self.tododata.InsertRecordWithLogInfo([project,todo,year,month,date,hour,minute,"DOING"])
        self.tasklog.InsertRecordWithLogInfo([project,todo,"DOING"])
        self.UpdateStaticWidgetProperty()
        self.InitializeDynamicWidget()
# ===================================================================================
    @mylogger.deco
    def OnDoneBtn(self, event):
        for todo in self.todolist:
            if todo['widgets']['donebtn'] == event.widget:
                index = todo['record']['index']
        project = self.tododata.GetAllRecordsByColumn('project')[index]['data']['project']
        todo = self.tododata.GetAllRecordsByColumn('todo')[index]['data']['todo']
        year = self.tododata.GetAllRecordsByColumn('year')[index]['data']['year']
        month = self.tododata.GetAllRecordsByColumn('month')[index]['data']['month']
        date = self.tododata.GetAllRecordsByColumn('date')[index]['data']['date']
        hour = self.tododata.GetAllRecordsByColumn('hour')[index]['data']['hour']
        minute = self.tododata.GetAllRecordsByColumn('minute')[index]['data']['minute']
        # self.memodata.InsertRecordWithLogInfo(project[index],todo[index],"DONE : "+todo[index])
        self.tododata.DeleteRecordByIndex(index)
        self.tododata.InsertRecordWithLogInfo([project,todo,year,month,date,hour,minute,"DONE"])
        self.tasklog.InsertRecordWithLogInfo([project,todo,"DONE"])
        self.UpdateStaticWidgetProperty()
        self.InitializeDynamicWidget()
# ===================================================================================
    @mylogger.deco
    def OnTick(self):
        self.UpdateDynamicWidgetProperty()
# ===================================================================================
    @mylogger.deco
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
                state = self.cb9.get()
                if state == "":
                    state = "DOING"
                self.tododata.InsertRecordWithLogInfo([project, task, year, month, date, hour, minute, state])
                self.tasklog.InsertRecordWithLogInfo([project,task,state])
                # self.cb9.set("OPEN")
                self.InitializeDynamicWidget()
                self.UpdateStaticWidgetProperty()
            elif self.currentpage == self.master.focus_get() and self.currentpage.get() != "":
                self.InitializeDynamicWidget()
                self.UpdateStaticWidgetProperty()
            elif self.cb8 == self.master.focus_get() and self.cb8.get() != "":
                self.InitializeDynamicWidget()
                self.UpdateStaticWidgetProperty()
            elif self.cb9 == self.master.focus_get() and self.cb9.get() != "":
                self.InitializeDynamicWidget()
                self.UpdateStaticWidgetProperty()
            else:
                for todo in self.todolist:
                    if todo['widgets']['memo'] == self.master.focus_get() and todo['widgets']['memo'].get() != "":
                        index = todo['record']['index']
                        project = self.tododata.GetAllRecordsByColumn('project')[index]['data']['project']
                        task = self.tododata.GetAllRecordsByColumn('todo')[index]['data']['todo']
                        memo = todo['widgets']['memo'].get()
                        if os.path.exists(memo) or memo.find("http") != -1:
                            os.system("start " + memo)
                        self.memodata.InsertRecordWithLogInfo([project, task, memo])
                        todo['widgets']['memo'].delete(0,'end')
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
    tasklog = MyDataBase("../data/tasklog.txt", ['project', 'task', 'state'])
    inboxframe = InBoxFrame(root, memodata, tododata, tasklog)
    framecompose.AddFrame(inboxframe, 'inboxframe', key=inboxframe.OnKeyEvent, time=inboxframe.OnTick)

    # メインループ
    root.mainloop()
# ===================================================================================