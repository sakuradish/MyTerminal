# ===================================================================================
import tkinter as tk
from ComposeFrame import ComposeFrame
from MyDataBase import MyDataBase
from MemoFrame import MemoFrame
from InBoxFrame import InBoxFrame
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    memodata = MyDataBase("../data/memo.txt", ['project', 'task', 'memo'])
    memoframe = MemoFrame(root, memodata)
    framecompose.AddFrame(memoframe, 'memoframe', key=memoframe.OnKeyEvent)
    tododata = MyDataBase("../data/todo.txt", ['todo'])
    donedata = MyDataBase("../data/done.txt", ['done'])
    inboxframe = InBoxFrame(root, memodata, tododata, donedata)
    framecompose.AddFrame(inboxframe, 'inboxframe', key=inboxframe.OnKeyEvent)
    frame1 = tk.Frame(bg='#000000')
    frame2 = tk.Frame(bg='#0000ff')
    frame3 = tk.Frame(bg='#00ff00')
    frame4 = tk.Frame(bg='#00ffff')
    frame5 = tk.Frame(bg='#ff0000')
    frame6 = tk.Frame(bg='#ff00ff')
    # frame7 = tk.Frame(bg='#ffff00')
    # frame8 = tk.Frame(bg='#ffffff')
    framecompose.AddFrame(frame1, '#000000')
    framecompose.AddFrame(frame2, '#0000ff')
    framecompose.AddFrame(frame3, '#00ff00')
    framecompose.AddFrame(frame4, '#00ffff')
    framecompose.AddFrame(frame5, '#ff0000')
    framecompose.AddFrame(frame6, '#ff00ff')
    # framecompose.AddFrame(frame7, '#ffff00')
    # framecompose.AddFrame(frame8, '#ffffff')

    # メインループ
    root.mainloop()
# ===================================================================================