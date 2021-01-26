# ===================================================================================
from ComposeFrame import ComposeFrame
from MyLogger.MyLogger import mylogger
mylogger = mylogger.GetInstance()
# ===================================================================================
import tkinter as tk
from tkinter import ttk
# ===================================================================================
class WidgetFactory():
    def __init__(self):
        self.widgets = {}
# ===================================================================================
    @classmethod
    def GetInstance(cls):
        if not hasattr(cls, "this_"):
            cls.this_ = cls()
        return cls.this_
# ===================================================================================
    def NewId(self):
        ret_id = 0
        for id in self.widgets.keys():
            if ret_id <= id:
                ret_id = id + 1
        return ret_id
# ===================================================================================
    def CalcCoordinates(self, length, index, x, y, w, h, direction="ToBottom"):
        if direction == "ToBottom":
            relw = w
            relh = h / length
            relx = x
            rely = y + relh * index
        elif direction == "ToRight":
            relw = w / length
            relh = h
            relx = x + relw * index
            rely = y
        return {'relx':relx, 'rely':rely, 'relw':relw, 'relh':relh}
# ===================================================================================
    @classmethod
    def Combobox(cls, parent, items, x, y, w, h, direction="ToBottom"):
        id = cls.GetInstance().NewId()
        ret = {'id':id, 'widgets':{}}
        cls.GetInstance().widgets[id] = []
        for item in items:
            length = len(items)
            index = items.index(item)
            v = tk.StringVar()
            combobox = ttk.Combobox(parent, textvariable=v)
            coordates = cls.GetInstance().CalcCoordinates(length, index, x, y, w, h, direction=direction)
            combobox.place(relx=coordates['relx'], rely=coordates['rely'], relwidth=coordates['relw'], relheight=coordates['relh'])
            cls.GetInstance().widgets[id].append(combobox)
            ret['widgets'][item] = {'combobox':combobox, 'stringvar':v, 'coordates':coordates}
        return ret
# ===================================================================================
    @classmethod
    def Label(cls, parent, items, x, y, w, h, direction="ToBottom"):
        id = cls.GetInstance().NewId()
        ret = {'id':id, 'widgets':{}}
        cls.GetInstance().widgets[id] = []
        for item in items:
            length = len(items)
            index = items.index(item)
            label = tk.Label(parent, text=item)
            coordates = cls.GetInstance().CalcCoordinates(length, index, x, y, w, h, direction=direction)
            label.place(relx=coordates['relx'], rely=coordates['rely'], relwidth=coordates['relw'], relheight=coordates['relh'])
            cls.GetInstance().widgets[id].append(label)
            ret['widgets'][item] = {'label':label, 'coordates':coordates}
        return ret
# ===================================================================================
    @classmethod
    def Destroy(cls, id):
        for widget in cls.GetInstance().widgets[id]:
            widget.destroy()
        del cls.GetInstance().widgets[id]
# ===================================================================================
if __name__ == '__main__':

    # ウィンドウ作成
    root = tk.Tk()
    root.title("MyTerminal")
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight())
    root.state("zoomed")

    framecompose = ComposeFrame(root)
    frame1 = tk.Frame(bg='#ffffff')
    framecompose.AddFrame(frame1, '#000000')

    cb1 = WidgetFactory.Combobox(frame1, ['a','b'], 0,0,1,1)
    cb2 = WidgetFactory.Label(frame1, ['a','b'], 0,0,1,1)
    WidgetFactory.Destroy(cb1['id'])
    WidgetFactory.Destroy(cb2['id'])
    cb3 = WidgetFactory.Combobox(frame1, ['column1','column2','column3','column4','column5'], 0.3,0.1,0.8,0.6)
    label = WidgetFactory.Label(frame1, ['column1','column2','column3','column4','column5'], 0.1,0.1,0.2,0.6)
    cb4 = WidgetFactory.Combobox(frame1, ['column1','column2','column3','column4','column5'], 0,0.8,1,0.1, "ToRight")

    # # メインループ
    root.mainloop()
# ===================================================================================