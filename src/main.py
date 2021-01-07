# ===================================================================================
import tkinter as tk
from ComposeFrame import ComposeFrame
from MyDataBase import MyDataBase
from MemoFrame import MemoFrame
from InBoxFrame import InBoxFrame
from AttendanceFrame import AttendanceFrame
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    # database
    memodata = MyDataBase("../data/memo.txt", ['project', 'task', 'memo'])
    tododata = MyDataBase("../data/todo.txt", ['project', 'todo', 'year', 'month', 'date', 'hour', 'minute', 'state'])
    tasklog = MyDataBase("../data/done.txt", ['project', 'task', 'state'])
    attendancedata = MyDataBase("../data/attendance.txt", ['year', 'month', 'date', 'weekday', 'type', 'time'])
    # memoframe
    memoframe = MemoFrame(root, memodata, tododata)
    # inboxframe
    inboxframe = InBoxFrame(root, memodata, tododata, tasklog)
    # attendanceframe
    attendanceframe = AttendanceFrame(root, attendancedata)
    # sampleframes
    frame1 = tk.Frame(bg='#000000')
    frame2 = tk.Frame(bg='#0000ff')
    frame3 = tk.Frame(bg='#00ff00')
    frame4 = tk.Frame(bg='#00ffff')
    frame5 = tk.Frame(bg='#ff0000')
    frame6 = tk.Frame(bg='#ff00ff')
    # composeframe
    composeframe = ComposeFrame(root)
    composeframe.AddFrame(memoframe, 'memoframe', key=memoframe.OnKeyEvent)
    composeframe.AddFrame(inboxframe, 'inboxframe', key=inboxframe.OnKeyEvent, time=inboxframe.OnTick)
    composeframe.AddFrame(attendanceframe, 'attendanceframe', key=attendanceframe.OnKeyEvent)
    composeframe.AddFrame(frame1, '#000000')
    composeframe.AddFrame(frame2, '#0000ff')
    composeframe.AddFrame(frame3, '#00ff00')
    composeframe.AddFrame(frame4, '#00ffff')
    composeframe.AddFrame(frame5, '#ff0000')
    composeframe.AddFrame(frame6, '#ff00ff')

    # メインループ
    root.mainloop()
# ===================================================================================