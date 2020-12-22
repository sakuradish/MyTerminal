import datetime
import tkinter as tk
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
import time

class MemoFrame(tk.Frame):
    def __init__(self,master,cnf={},**kw):
        super().__init__(master,cnf,**kw)

        my_font = font.Font(root,family=u'ＭＳ ゴシック',size=14)

        text = tk.Text(self,wrap=tk.CHAR,undo=True, bg='black',font=my_font, foreground='white', insertbackground='white')
        x_sb = tk.Scrollbar(self,orient='horizontal')
        y_sb = tk.Scrollbar(self,orient='vertical')

        with open('../data/new.txt','r') as f:
            fruits = list()
            lines = f.readlines()
            for line in lines:
                if not line.split("\t")[3] in fruits:
                    fruits.append(line.split("\t")[3])
        label1 = tk.Label(self, text='プロジェクト')
        self.v1 = tk.StringVar()
        cb1 = ttk.Combobox(
            self, textvariable=self.v1,
            values=fruits)
        cb1.set(fruits[-1])
        with open('../data/new.txt','r') as f:
            fruits = list()
            lines = f.readlines()
            for line in lines:
                if not line.split("\t")[4] in fruits:
                    fruits.append(line.split("\t")[4])
        label2 = tk.Label(self, text='タスク')
        self.v2 = tk.StringVar()
        cb2 = ttk.Combobox(
            self, textvariable=self.v2,
            values=fruits)
        cb2.set(fruits[-1])
        with open('../data/new.txt','r') as f:
            fruits = list()
            lines = f.readlines()
            for line in lines:
                if not line.split("\t")[5] in fruits:
                    fruits.append(line.split("\t")[5])
        label3 = tk.Label(self, text='メモ')
        self.v3 = tk.StringVar()
        cb3 = ttk.Combobox(
            self, textvariable=self.v3,
            values=fruits)

        x_sb.config(command=text.xview)
        y_sb.config(command=text.yview)
        text.config(xscrollcommand=x_sb.set,yscrollcommand=y_sb.set)

        text.place(relx=0,rely=0,relwidth=0.97,relheight=0.77)
        x_sb.place(relx=0,rely=0.77,relwidth=0.97,relheight=0.03)
        y_sb.place(relx=0.97,rely=0,relwidth=0.03,relheight=0.77)
        label1.place(relx=0,rely=0.85,relwidth=0.2,relheight=0.05)
        cb1.place(relx=0.2,rely=0.85,relwidth=0.8,relheight=0.05)
        label2.place(relx=0,rely=0.9,relwidth=0.2,relheight=0.05)
        cb2.place(relx=0.2,rely=0.9,relwidth=0.8,relheight=0.05)
        label3.place(relx=0,rely=0.95,relwidth=0.2,relheight=0.05)
        cb3.place(relx=0.2,rely=0.95,relwidth=0.8,relheight=0.05)

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.text = text
        self.x_sb = x_sb
        self.y_sb = y_sb
        self.label1 = label1
        self.cb1 = cb1
        self.label2 = label2
        self.cb2 = cb2
        self.label3 = label3
        self.cb3 = cb3

        f = open('../data/new.txt','r')
        lines = f.readlines()
        f.close()
        self.text.delete('1.0','end')
        for line in lines:
            self.text.insert('end',line)

class InBoxFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('Todo List')
        self.num = 1
        self.todolist = []
        self.buttonlist = []
        self.v1 = tk.StringVar()
        fruits = []
        cb = ttk.Combobox(
            self, textvariable=self.v1,
            values=fruits)
        self.cb = cb
        cb.place(relx=0,rely=0,relwidth=1,relheight=0.1)
        self.initializeToDoList()

    def drawToDoList(self):
        with open('../data/todo.txt','r') as f:
            lines = f.readlines()
            for line in lines:
                # テキストボックスの値を取得
                task = tk.StringVar()
                task.set(line)

                # 新規タスクを追加
                todo = tk.Label(self, textvariable=task)
                todo.place(rely=self.num*0.03+0.1, relx=0, relwidth=0.6)
                self.todolist.append(todo)

                # 新規タスクの削除ボタンを追加
                button = tk.Button(self, text="DONE "+ str(self.num), highlightbackground='gray')
                button.bind("<Button-1>", self.delete_value)
                button.place(rely=self.num*0.03+0.1, relx=0.6, relwidth=0.2)
                self.buttonlist.append(button)

                self.num += 1
    def delete_value(self, event):
        deletenum = int(event.widget["text"].split(" ")[1])
        index = deletenum-1
        with open('../data/todo.txt','r') as f:
            lines = f.readlines()
        with open('../data/todo.txt','w') as f:
            for line in lines:
                #同じtodo無い前提いまのところ
                if line == lines[index]:
                    with open('../data/done.txt','a') as o:
                        o.write(line)
                else:
                    f.write(line)
        self.initializeToDoList()
    def initializeToDoList(self):
        self.num = 1
        for todo in self.todolist:
            todo.place_forget()
        for button in self.buttonlist:
            button.place_forget()
        self.drawToDoList()

# ウィンドウ作成
root = tk.Tk()
root.title("MyTerminal")
root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
root.state("zoomed")

memoframe = MemoFrame(root)
memoframe.place(relx=0,rely=0,relwidth=0.5,relheight=1)
inboxframe = InBoxFrame(root)
inboxframe.place(relx=0.5,rely=0,relwidth=0.5,relheight=1)

isKeyEventProcessing = False
def OnKeyEvent(event):
    global isKeyEventProcessing
    if isKeyEventProcessing == False:
        if event.keysym == 'Return' and memoframe.cb3 == root.focus_get() and memoframe.cb3.get() != "":
            isKeyEventProcessing = True
            print(event)
            with open("../data/new.txt", "w") as f:
                f.write(memoframe.text.get('1.0','end'))
                dt = datetime.datetime.now()
                date = dt.strftime("%Y/%m/%d") + "\t" + dt.strftime('%a') + "\t" + dt.strftime('%X')
                f.write(date + "\t" + memoframe.cb1.get() + "\t" + memoframe.cb2.get() + "\t" + memoframe.cb3.get())
            f = open('../data/new.txt','r')
            lines = f.readlines()
            f.close()
            memoframe.text.delete('1.0','end')
            for line in lines:
                root.update()
                memoframe.text.insert('end',line)
                memoframe.text.see('end')
            memoframe.cb3.set("")
            isKeyEventProcessing = False
        elif event.keysym == 'Return' and inboxframe.cb == root.focus_get() and inboxframe.cb.get() != "":
            isKeyEventProcessing = True
            print(event)
            with open("../data/todo.txt", "a") as f:
                f.write(inboxframe.cb.get() + "\n")
            inboxframe.initializeToDoList()
            inboxframe.cb.set("")
            isKeyEventProcessing = False
def OnMouseEvent(event):
    print(event)

root.bind("<Key>", OnKeyEvent)
root.bind("<Button>", OnMouseEvent)

# メインループ
root.mainloop()