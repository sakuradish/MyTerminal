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
class AccountBookFrame(tk.Frame):
    def __init__(self,master, memodata, cnf={},**kw):
        super().__init__(master,cnf,**kw)
        self.memodata = memodata
        self.InitializeStaticWidget()
        self.PlaceStaticWidget()
        self.UpdateStaticWidgetProperty()
# ===================================================================================
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
        # combobox1
        label1 = tk.Label(self, text='year')
        self.v1 = tk.StringVar()
        cb1 = ttk.Combobox(self, textvariable=self.v1)
        self.label1 = label1
        self.cb1 = cb1
        self.cb1.set(str(datetime.date.today().year))
        # combobox2
        label2 = tk.Label(self, text='month')
        self.v2 = tk.StringVar()
        cb2 = ttk.Combobox(self, textvariable=self.v2)
        self.label2 = label2
        self.cb2 = cb2
        self.cb2.set(str(datetime.date.today().month))
        # combobox3
        label3 = tk.Label(self, text='date')
        self.v3 = tk.StringVar()
        cb3 = ttk.Combobox(self, textvariable=self.v3)
        self.label3 = label3
        self.cb3 = cb3
        self.cb3.set(str(datetime.date.today().day))
        # combobox4
        label4 = tk.Label(self, text='category')
        self.v4 = tk.StringVar()
        cb4 = ttk.Combobox(self, textvariable=self.v4)
        self.label4 = label4
        self.cb4 = cb4
        self.cb4.bind('<<ComboboxSelected>>', self.UpdateStaticWidgetProperty)
        self.cb4.set(self.memodata.GetLastRecordsByColumn('category')['data']['category'])
        # combobox5
        label5 = tk.Label(self, text='where')
        self.v5 = tk.StringVar()
        cb5 = ttk.Combobox(self, textvariable=self.v5)
        self.label5 = label5
        self.cb5 = cb5
        self.cb5.bind('<<ComboboxSelected>>', self.UpdateStaticWidgetProperty)
        self.cb5.set(self.memodata.GetLastRecordsByColumn('where')['data']['where'])
        # combobox6
        label6 = tk.Label(self, text='method')
        self.v6 = tk.StringVar()
        cb6 = ttk.Combobox(self, textvariable=self.v6)
        self.label6 = label6
        self.cb6 = cb6
        self.cb6.bind('<<ComboboxSelected>>', self.UpdateStaticWidgetProperty)
        # combobox7
        label7 = tk.Label(self, text='amount')
        self.v7 = tk.StringVar()
        cb7 = ttk.Combobox(self, textvariable=self.v7)
        self.label7 = label7
        self.cb7 = cb7
        self.cb7.bind('<<ComboboxSelected>>', self.UpdateStaticWidgetProperty)
# ===================================================================================
    def PlaceStaticWidget(self):
        self.text.place(relx=0,rely=0,relwidth=0.95,relheight=0.55)
        self.x_sb.place(relx=0,rely=0.55,relwidth=0.95,relheight=0.05)
        self.y_sb.place(relx=0.95,rely=0,relwidth=0.05,relheight=0.55)
        self.label1.place(relx=0,rely=0.6,relwidth=0.2,relheight=0.05)
        self.cb1.place(relx=0.2,rely=0.6,relwidth=0.8,relheight=0.05)
        self.label2.place(relx=0,rely=0.65,relwidth=0.2,relheight=0.05)
        self.cb2.place(relx=0.2,rely=0.65,relwidth=0.8,relheight=0.05)
        self.label3.place(relx=0,rely=0.7,relwidth=0.2,relheight=0.05)
        self.cb3.place(relx=0.2,rely=0.7,relwidth=0.8,relheight=0.05)
        self.label4.place(relx=0,rely=0.75,relwidth=0.2,relheight=0.05)
        self.cb4.place(relx=0.2,rely=0.75,relwidth=0.8,relheight=0.05)
        self.label5.place(relx=0,rely=0.8,relwidth=0.2,relheight=0.05)
        self.cb5.place(relx=0.2,rely=0.8,relwidth=0.8,relheight=0.05)
        self.label6.place(relx=0,rely=0.85,relwidth=0.2,relheight=0.05)
        self.cb6.place(relx=0.2,rely=0.85,relwidth=0.8,relheight=0.05)
        self.label7.place(relx=0,rely=0.9,relwidth=0.2,relheight=0.05)
        self.cb7.place(relx=0.2,rely=0.9,relwidth=0.8,relheight=0.05)
# ===================================================================================
    def UpdateStaticWidgetProperty(self, event=None):
        # text
        self.text.configure(state='normal')
        self.text.delete('1.0','end')
        for record in self.memodata.GetAllRecords(filter={'category':self.cb4.get(), 'where':self.cb5.get()}):
            # self.master.update()
            self.text.insert('end', self.memodata.ConvertRecordToString(record) + "\n")
        self.text.see('end')
        self.text.configure(state='disabled')
        # combobox4
        records = self.memodata.GetAllRecordsByColumn('category')
        records = [record['data']['category'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb4.configure(values=records)
        # combobox5
        records = self.memodata.GetAllRecordsByColumn('where', filter={'category':self.cb4.get()})
        records = [record['data']['where'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb5.configure(values=records)
        # combobox6
        records = self.memodata.GetAllRecordsByColumn('method')
        records = [record['data']['method'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb6.configure(values=records)
        # combobox7
        records = self.memodata.GetAllRecordsByColumn('amount', filter={'where':self.cb5.get()})
        records = [record['data']['amount'] for record in records]
        records = list(dict.fromkeys(records))
        self.cb7.configure(values=records)
# ===================================================================================
    def OnKeyEvent(self, event):
        if event.keysym == 'Return':
            if self.cb7 == self.master.focus_get() and self.cb7.get() != "":
                year = self.cb1.get()
                month = self.cb2.get()
                day = self.cb3.get()
                date = year+"/"+month+"/"+day
                category = self.cb4.get()
                where = self.cb5.get()
                method = self.cb7.get()
                amount = self.cb8.get()
                self.memodata.InsertRecordWithLogInfo([date, category, where, method, amount])
                self.UpdateStaticWidgetProperty()
                self.cb6.set("")
                self.cb7.set("")
# ===================================================================================
if __name__ == '__main__':
    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    memodata = MyDataBase("../data/accountbook.txt", ['date', 'category', 'where', 'method', 'amount'])
    memoframe = AccountBookFrame(root, memodata)
    framecompose.AddFrame(memoframe, 'memoframe', key=memoframe.OnKeyEvent)

    # メインループ
    root.mainloop()
# ===================================================================================