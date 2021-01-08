# ===================================================================================
import os
import datetime
import shutil
# ===================================================================================
class MyDataBase():
    def __init__(self, filepath, columns):
        self.filepath = filepath
        self.logcolumns = ['date', 'weekday', 'time']
        self.datacolumns = columns
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
    def InsertRecordWithLogInfo(self, records):
        if len(records) != len(self.datacolumns):
            print("input records is not matching")
        temprecords = []
        dt = datetime.datetime.now()
        temprecords.append(dt.strftime("%Y/%m/%d"))
        temprecords.append(dt.strftime('%a'))
        temprecords.append(dt.strftime('%X'))
        temprecords += records
        self.InsertRecord(temprecords)
# ===================================================================================
    def InsertRecord(self, records):
        with open(self.filepath, 'a', encoding='utf-8') as f:
            for record in records:
                if records.index(record) == 0:
                    f.write(record.replace("\n", ""))
                else:
                    f.write("\t" + record.replace("\n", ""))
            f.write("\n")
        self.OnUpdate()
# ===================================================================================
    def DeleteRecordByIndex(self, index):
        records = self.GetAllRecords()
        del records[index]
        with open(self.filepath, 'w', encoding='utf-8') as f:
            for record in records:
                f.write(self.ConvertRecordToString(record) + "\n")
        self.OnUpdate()
# ===================================================================================
    def ConvertRecordToString(self, record, log=True, data=True):
        ret = ""
        texts = []
        if log:
            texts.append(record['log']['date'])
            texts.append(record['log']['weekday'])
            texts.append(record['log']['time'])
        if data:
            for column in self.datacolumns:
                texts.append(record['data'][column])
        for text in texts:
            if texts.index(text) == 0:
                ret += text
            else:
                ret += "\t" + text
        return ret
# ===================================================================================
    def GetLastRecordsByColumn(self, column):
        records = self.GetAllRecordsByColumn(column)
        if records:
            return records[-1]
        else:
            return ""
# ===================================================================================
    def GetAllRecordsByColumn(self, column):
        ret = []
        records = self.GetAllRecords()
        for record in records:
            index = record['index']
            data = {}
            data[column] = record['data'][column]
            ret.append({'index':index, 'data':data})
        return ret
# ===================================================================================
    def GetLastRecords(self):
        records = self.GetAllRecords()
        if records:
            return records[-1]
        else:
            return ""
# ===================================================================================
    def GetAllRecords(self, sort=""):
        ret = []
        records = open(self.filepath, 'r', encoding='utf-8').readlines()
        index = 0
        for record in records:
            record = record.replace("\n", "")
            log = {}
            for column in self.logcolumns:
                log[column] = record.split("\t")[self.logcolumns.index(column)]
            data = {}
            for column in self.datacolumns:
                data[column] = record.split("\t")[self.datacolumns.index(column) + len(self.logcolumns)]
            ret.append({'index':index, 'log':log, 'data':data})
            index += 1
        if not sort:
            return ret
        else:
            sorted = []
            sortitems = [record['data'][sort] for record in ret]
            sortitems = list(dict.fromkeys(sortitems))
            print(sortitems)
            for item in sortitems:
                for record in ret:
                    if record['data'][sort] == item:
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
    memodata = MyDataBase("../data/memo.txt", ['project', 'task', 'memo'])
    memodata.InsertRecordWithLogInfo(['project1', 'task1 to be deleted', 'memo'])
    memodata.InsertRecordWithLogInfo(['project2', 'task2', 'test'])
    print("=================================")
    print(memodata.GetAllRecords())
    print("=================================")
    memodata.DeleteRecordByIndex(0)
    print(memodata.GetAllRecords())
    print("=================================")
    print(memodata.GetAllRecordsByColumn('memo'))
    print(memodata.GetLastRecords())
    print(memodata.GetLastRecordsByColumn('project'))
    input("press any key ...")
# ===================================================================================