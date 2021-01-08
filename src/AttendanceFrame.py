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
class AttendanceFrame(tk.Frame):
    def __init__(self,master, attendancedata,cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.attendancedata = attendancedata
        self.attendancedata.AddOnUpdateCallback(self.UpdateData)
        self.InitializeStaticWidget()
        self.UpdateData()
    def InitializeStaticWidget(self):
        # text
        my_font = font.Font(self.master ,family=u'ＭＳ ゴシック',size=14)
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
        # Combobox1
        label1 = tk.Label(self, text='year')
        self.v1 = tk.StringVar()
        cb1 = ttk.Combobox(self, textvariable=self.v1)
        self.label1 = label1
        self.cb1 = cb1
        # combobox2
        label2 = tk.Label(self, text='month')
        self.v2 = tk.StringVar()
        cb2 = ttk.Combobox(self, textvariable=self.v2)
        self.label2 = label2
        self.cb2 = cb2
        # combobox3
        label3 = tk.Label(self, text='date')
        self.v3 = tk.StringVar()
        cb3 = ttk.Combobox(self, textvariable=self.v3)
        self.label3 = label3
        self.cb3 = cb3
        # combobox4
        label4 = tk.Label(self, text='weekday')
        self.v4 = tk.StringVar()
        cb4 = ttk.Combobox(self, textvariable=self.v4)
        self.label4 = label4
        self.cb4 = cb4
        # combobox5
        label5 = tk.Label(self, text='type')
        self.v5 = tk.StringVar()
        cb5 = ttk.Combobox(self, textvariable=self.v5)
        self.label5 = label5
        self.cb5 = cb5
        # combobox6
        label6 = tk.Label(self, text='time')
        self.v6 = tk.StringVar()
        cb6 = ttk.Combobox(self, textvariable=self.v6)
        self.label6 = label6
        self.cb6 = cb6
        self.PlaceStaticWidget()
    def PlaceStaticWidget(self):
        # text
        self.text.place(relx=0,rely=0,relwidth=0.97,relheight=0.47)
        self.x_sb.place(relx=0,rely=0.47,relwidth=0.97,relheight=0.03)
        self.y_sb.place(relx=0.97,rely=0,relwidth=0.03,relheight=0.47)
        # combobox1
        self.label1.place(relx=0,rely=0.55,relwidth=0.2,relheight=0.05)
        self.cb1.place(relx=0.2,rely=0.55,relwidth=0.8,relheight=0.05)
        # combobox2
        self.label2.place(relx=0,rely=0.6,relwidth=0.2,relheight=0.05)
        self.cb2.place(relx=0.2,rely=0.6,relwidth=0.8,relheight=0.05)
        # combobox3
        self.label3.place(relx=0,rely=0.65,relwidth=0.2,relheight=0.05)
        self.cb3.place(relx=0.2,rely=0.65,relwidth=0.8,relheight=0.05)
        # combobox4
        self.label4.place(relx=0,rely=0.7,relwidth=0.2,relheight=0.05)
        self.cb4.place(relx=0.2,rely=0.7,relwidth=0.8,relheight=0.05)
        # combobox5
        self.label5.place(relx=0,rely=0.75,relwidth=0.2,relheight=0.05)
        self.cb5.place(relx=0.2,rely=0.75,relwidth=0.8,relheight=0.05)
        # combobox6
        self.label6.place(relx=0,rely=0.8,relwidth=0.2,relheight=0.05)
        self.cb6.place(relx=0.2,rely=0.8,relwidth=0.8,relheight=0.05)
# ===================================================================================
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            if (self.cb5 == self.master.focus_get() or self.cb6 == self.master.focus_get()) and \
               self.cb5.get() != "" and self.cb6.get() != "":
                self.attendancedata.InsertRecordWithLogInfo([self.cb1.get(),self.cb2.get(),self.cb3.get(),self.cb4.get(),self.cb5.get(),self.cb6.get()])
                self.UpdateData()
# ===================================================================================
    def UpdateData(self):
        if self.attendancedata.GetAllRecords():
            self.text.configure(state='normal')
            self.text.delete('1.0','end')
            for record in self.attendancedata.GetAllRecords():
                self.text.insert('end', self.attendancedata.ConvertRecordToString(record) + "\n")
            self.text.see('end')
            self.text.configure(state='disabled')
            # combobox1
            records = self.attendancedata.GetAllRecordsByColumn('year')
            records = [record['data']['year'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb1.configure(values=records)
            self.cb1.set(self.attendancedata.GetLastRecordsByColumn('year')['data']['year'])
            # combobox2
            records = self.attendancedata.GetAllRecordsByColumn('month')
            records = [record['data']['month'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb2.configure(values=records)
            self.cb2.set(self.attendancedata.GetLastRecordsByColumn('month')['data']['month'])
            # combobox3
            records = self.attendancedata.GetAllRecordsByColumn('date')
            records = [record['data']['date'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb3.configure(values=records)
            self.cb3.set(self.attendancedata.GetLastRecordsByColumn('date')['data']['date'])
            # combobox4
            records = self.attendancedata.GetAllRecordsByColumn('weekday')
            records = [record['data']['weekday'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb4.configure(values=records)
            self.cb4.set(self.attendancedata.GetLastRecordsByColumn('weekday')['data']['weekday'])
            # combobox5
            records = self.attendancedata.GetAllRecordsByColumn('type')
            records = [record['data']['type'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb5.configure(values=records)
            self.cb5.set("")
            # combobox6
            records = self.attendancedata.GetAllRecordsByColumn('time')
            records = [record['data']['time'] for record in records]
            records = list(dict.fromkeys(records))
            self.cb6.configure(values=records)
            self.cb6.set("")
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    attendancedata = MyDataBase("../data/attendance.txt", ['year', 'month', 'date', 'weekday', 'type', 'time'])
    attendanceframe = AttendanceFrame(root, attendancedata)
    framecompose.AddFrame(attendanceframe, 'attendanceframe', key=attendanceframe.OnKeyEvent)

    # メインループ
    root.mainloop()
# ===================================================================================