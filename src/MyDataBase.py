# ===================================================================================
import os
import datetime
import shutil
# ===================================================================================
class MyDataBase():
    def __init__(self, filepath, columns):
        self.filepath = filepath
        self.columns = columns
        self.callbacks = []
        if not os.path.exists(self.filepath):
            if not os.path.exists(os.path.dirname(self.filepath)):
                os.makedirs(os.path.dirname(self.filepath))
            with open(self.filepath, 'a', encoding='utf-8') as f:
                print("Create " + self.filepath)
        self.DailyBackup()
# ===================================================================================
    def DailyBackup(self):
        folder = "../backup/" + str(datetime.date.today()) + "/"
        file = folder + os.path.basename(self.filepath)
        if not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(file):
            shutil.copy2(self.filepath, file)
# ===================================================================================
    def InsertRecordWithDate(self, *records):
        print(records)
        with open(self.filepath, 'a', encoding='utf-8') as f:
            dt = datetime.datetime.now()
            f.write(dt.strftime("%Y/%m/%d"))
            f.write("\t" + dt.strftime('%a'))
            f.write("\t" + dt.strftime('%X'))
            for i in range(0, len(self.columns), 1):
                f.write("\t" + records[i].replace("\n", ""))
            f.write("\n")
        self.OnUpdate()
# ===================================================================================
    def InsertRecord(self, record):
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(record.replace("\n", "") + "\n")
# ===================================================================================
    def DeleteAllRecords(self):
        os.remove(self.filepath)
# ===================================================================================
    # def DeleteRecordByData(self, column, data):
    #     index = self.columns.index(column)
    #     records = self.GetAllRecords()
    #     self.DeleteAllRecords()
    #     for record in records:
    #         if record.split("\t")[index + 3] != data:
    #             self.InsertRecord(record)
    #     self.OnUpdate()
# ===================================================================================
    def DeleteRecordByIndex(self, index):
        records = self.GetAllRecords()
        self.DeleteAllRecords()
        for record in records:
            if record.split("\t")[0] != records[index].split("\t")[0] \
               or record.split("\t")[1] != records[index].split("\t")[1] \
               or record.split("\t")[2] != records[index].split("\t")[2]:
                self.InsertRecord(record)
        self.OnUpdate()
# ===================================================================================
    def GetColumns(self):
        return self.columns
# ===================================================================================
    def GetLastRecordsByColumn(self, column):
        records = self.GetAllRecordsByColumn(column)
        if records:
            return records[-1]
        else:
            return ""
# ===================================================================================
    def GetAllRecordsByColumn(self, column):
        if column in self.columns:
            index = self.columns.index(column)
            records = self.GetAllRecords()
            filtered = [record.split("\t")[index + 3] for record in records]
            return filtered
        else:
            return self.GetAllRecords()
# ===================================================================================
    def GetLastRecords(self):
        records = self.GetAllRecords()
        if records:
            return records[-1]
        else:
            return ""
# ===================================================================================
    def GetAllRecords(self, sort=""):
        if not sort:
            return open(self.filepath, 'r', encoding='utf-8').readlines()
        else:
            index = self.columns.index(sort)
            sorted = []
            records = open(self.filepath, 'r', encoding='utf-8').readlines()
            sortitems = [record.split("\t")[index + 3] for record in records]
            sortitems = list(dict.fromkeys(sortitems))
            for item in sortitems:
                for record in records:
                    if record.split("\t")[index + 3] == item:
                        sorted.append(record)
            return sorted
# ===================================================================================
    def AddOnUpdateCallback(self, callback):
        self.callbacks.append(callback)
# ===================================================================================
    def OnUpdate(self):
        for callback in self.callbacks:
            callback()
# ===================================================================================
if __name__ == '__main__':
    memodata = MyDataBase("memo.txt", ['project', 'task', 'memo'])
    memodata.InsertRecordWithDate('project', 'task', 'memo')
    print(memodata.GetAllRecords())
    print(memodata.GetAllRecordsByColumn('project'))
    print(memodata.GetLastRecords())
    print(memodata.GetLastRecordsByColumn('project'))
    input("press any key ...")
# ===================================================================================