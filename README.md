[Widget を配置しよう](https://www.shido.info/py/tkinter2.html)
[Python - Tkinter Text](https://www.tutorialspoint.com/python/tk_text.htm)
まずは動くもの
メモが空欄のときは保存しない。
保存したらメモを初期化。


import tkinter
from tkinter import messagebox

class Application(tkinter.Frame):
def __init__(self, master=None):
tkinter.Frame.__init__(self, master)
self.master.title('Todo List')
self.master.geometry('600x600')

self.num = 1         # タスクの行番号
self.todo = ""       # 追加するタスク
self.button = ""     # 追加するタスクの削除ボタン

self.taskValueList = []  # 画面に表示するタスクの値
self.todoList = []       # 画面に表示する追加タスク
self.buttonList = []     # 画面に表示する追加タスクの削除ボタン

self.pack()
self.create_widgets()

def create_widgets(self):
# 初期表示の部品を作成
self.label = tkinter.Label(self, text="Todo List", font=("", 25))
self.editBox = tkinter.Entry(self, width=30)
self.whiteLabel = tkinter.Label(self, text="")

# 初期表示の部品を配置
self.label.grid(row=0, column=0)
self.editBox.grid(row=1, column=0)
self.whiteLabel.grid(row=2, column=0)

# 追加ボタンを生成
self.button = tkinter.Button(self, width=10, text="ADD", highlightbackground='green')
self.button.bind("<Button-1>", self.add_value)
self.button.grid(row=1, column=1)

# 追加ボタン押下時の処理
def add_value(self, event):
# テキストボックスの値を取得
task = tkinter.StringVar()
task.set(self.editBox.get())
self.taskValueList.append(task)

# 新規タスクを追加
self.todo = tkinter.Label(self, width=30, textvariable=task)
self.todo.grid(row=3+self.num, column=0, sticky=tkinter.W)
self.todoList.append(self.todo)

# 新規タスクの削除ボタンを追加
self.button = tkinter.Button(self, width=10, text="DONE "+ str(self.num), highlightbackground='gray')
self.button.bind("<Button-1>", self.delete_value)
self.button.grid(row=3+self.num, column=1)
self.buttonList.append(self.button)

self.num += 1

# テキストボックスを初期化
self.editBox.delete(0, tkinter.END)

# 削除ボタン押下時の処理
def delete_value(self, event):
# 削除するタスク番号を取得
deletenum = int(event.widget["text"].split(" ")[1])
index = deletenum-1

# 削除前のタスクを一時保存
tmpTaskValueList = []
tmpTodoList = []
tmpButtonList = []
tmpTaskValueList = self.taskValueList
tmpTodoList = self.todoList
tmpButtonList = self.buttonList

# 削除後のタスクを格納するオブジェクト
newTaskValueList = []
newTodoList = []
newButtonList = []

for i in range(len(self.todoList)):

# 削除する番号より前のタスクはそのままにする
if i < index:
# 削除後タスクListに追加する
newTaskValueList.append(self.taskValueList[i])
newTodoList.append(self.todoList[i])
newButtonList.append(self.buttonList[i])
continue

# 削除する番号のタスクを削除
elif i == index:
self.todoList[i].destroy()
self.buttonList[i].destroy()

# 削除する番号より後ろのタスクは1つずつ前へ詰める
else:
self.todoList[i].destroy()
self.buttonList[i].destroy()

# 1つ前へ詰めたタスクの値を新規作成
self.todo = tkinter.Label(self, width=30, textvariable=tmpTaskValueList[i])
self.todo.grid(row=4+i, column=0, sticky=tkinter.W)

# 1つ前へ詰めた削除ボタンを新規作成
self.button = tkinter.Button(self, width=10, text="DONE "+ str(i), highlightbackground='gray')
self.button.bind("<Button-1>", self.delete_value)

# 削除後タスクListに追加する
newTaskValueList.append(tmpTaskValueList[i])
newTodoList.append(self.todo)
newButtonList.append(self.button)

self.button.grid(row=4+i, column=1)

# 削除後タスクListを元々のタスクListに置き換える
self.taskValueList = []
self.todoList = []
self.buttonList = []
self.taskValueList = newTaskValueList
self.todoList = newTodoList
self.buttonList = newButtonList
self.num -= 1

root = tkinter.Tk()
root.title("todo")
app = Application(master=root)
app.mainloop()