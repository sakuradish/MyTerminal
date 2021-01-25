# ===================================================================================
from MyLogger.MyLogger import mylogger
mylogger = mylogger.GetInstance()
# ===================================================================================
import os
import datetime
import shutil
# ===================================================================================
class MyRecordManager():
    @mylogger.deco
    def __init__(self, datacolumns):
        # self.logcolumns = self.logcolumns
        self.logcolumns = ['date', 'weekday', 'time']
        self.datacolumns = datacolumns
# ===================================================================================
    @mylogger.deco
    def GetDataColumns(self):
        return self.datacolumns
# ===================================================================================
    @mylogger.deco
    def GetEmptyRecord(self):
        record = {}
        record['index'] = -1
        dt = datetime.datetime.now()
        record['log'] = {}
        record['log']['date'] = dt.strftime("%Y/%m/%d")
        record['log']['weekday'] = dt.strftime('%a')
        record['log']['time'] = dt.strftime('%X')
        record['data'] = {}
        for column in self.datacolumns:
            record['data'][column] = ""
        return record
# ===================================================================================
    @mylogger.deco
    def ExtractRecordsByColumn(self, arg_records, column):
        if column:
            mylogger.info("メモリ削減に必要かも？")
            return arg_records
        else:
            return arg_records
# ===================================================================================
    @mylogger.deco
    def ExtractRecordsByRow(self, arg_records, row):
        if row:
            return arg_records[row]
        else:
            return arg_records
# ===================================================================================
    @mylogger.deco
    def FilterRecords(self, arg_records, filter):
        ret_records = []
        if filter:
            for arg_record in arg_records:
                isMatched = True
                for k,v in filter.items():
                    if not v.lower() in arg_record['data'][k].lower():
                        isMatched = False
                        break
                if isMatched:
                    ret_records.append(arg_record)
            return ret_records
        else:
            return arg_records
# ===================================================================================
    @mylogger.deco
    def SortRecords(self, arg_records, sort):
        ret_records = []
        if sort:
            # とりあえず古い順に重複をなくして並び変える
            sortitems = [record['data'][sort] for record in arg_records]
            sortitems = list(dict.fromkeys(sortitems))
            for item in sortitems:
                for arg_record in arg_records:
                    if arg_record['data'][sort] == item:
                        ret_records.append(arg_record)
            return ret_records
        else:
            return arg_records
# ===================================================================================
    @mylogger.deco
    def ConvertLinesToRecordsSub(self, lines):
        records = []
        index = 0
        for line in lines:
            line = line.replace("\n", "")
            log = {}
            for column in self.logcolumns:
                try:
                    log[column] = line.split("\t")[self.logcolumns.index(column)]
                except:
                    log[column] = ""
            data = {}
            for column in self.datacolumns:
                try:
                    data[column] = line.split("\t")[self.datacolumns.index(column) + len(self.logcolumns)]
                except:
                    data[column] = ""
            records.append({'index':index, 'log':log, 'data':data})
            index += 1
        return records
# ===================================================================================
    @mylogger.deco
    def ConvertLinesToRecords(self, lines, row=None, column=None, sort=None, filter={}):
        records = self.ConvertLinesToRecordsSub(lines)
        records = self.ExtractRecordsByColumn(records, column)
        records = self.ExtractRecordsByRow(records, row)
        records = self.FilterRecords(records, filter)
        records = self.SortRecords(records, sort)
        return records
# ===================================================================================
    @mylogger.deco
    def ConvertRecordsToLines(self, records):
        lines = []
        for record in records:
            line = ""
            line += record['log']['date']
            line += "\t" + record['log']['weekday']
            line += "\t" + record['log']['time']
            for column in self.datacolumns:
                line += "\t" + record['data'][column]
            line += "\n"
            lines.append(line)
        return lines
# ===================================================================================


# ===================================================================================
class MyDataBase():
    @mylogger.deco
    def __init__(self, filepath, columns):
        self.filepath = filepath
        self.rm = MyRecordManager(columns)
        self.callbacks = []
        self.InitializeDataBase()
# ===================================================================================
    @mylogger.deco
    def InitializeDataBase(self):
        # ファイルがない場合には作ったり、列が追加された場合には空文字を入れたり。
        if not os.path.exists(self.filepath):
            if not os.path.exists(os.path.dirname(self.filepath)):
                os.makedirs(os.path.dirname(self.filepath))
            with open(self.filepath, 'w', encoding='utf-8') as f:
                pass
        else:
            self.DailyBackup()
            mylogger.info("列追加あった場合の処理未実装")
# ===================================================================================
    @mylogger.deco
    def DailyBackup(self):
        folder = "../backup/" + str(datetime.date.today()) + "/"
        file = folder + os.path.basename(self.filepath)
        if not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(file):
            shutil.copy2(self.filepath, file)
# ===================================================================================
    @mylogger.deco
    def DeleteRecords(self, index=-1):
        if index == -1:
            os.remove(self.filepath)
            self.InitializeDataBase()
        else:
            mylogger.info(index,"を削除")
            records = self.GetRecords()
            del records[index]
            lines = self.rm.ConvertRecordsToLines(records)
            with open(self.filepath, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line)
        self.OnUpdate()
# ===================================================================================
    @mylogger.deco
    def WriteRecords(self, records):
        lines = self.rm.ConvertRecordsToLines(records)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line)
        self.OnUpdate()
# ===================================================================================
    @mylogger.deco
    def ReplaceRecords(self, records):
        # replace
        origin_records = self.GetRecords()
        columns = self.GetDataColumns()
        for record in records:
            for column in columns:
                origin_records[record["index"]]["data"][column] = record["data"][column]
        # write
        lines = self.rm.ConvertRecordsToLines(origin_records)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line)
        self.OnUpdate()
# ===================================================================================
    @mylogger.deco
    def PushbackRecords(self, records):
        lines = self.rm.ConvertRecordsToLines(records)
        with open(self.filepath, 'a', encoding='utf-8') as f:
            for line in lines:
                f.write(line)
        self.OnUpdate()
# ===================================================================================
    @mylogger.deco
    def GetRecords(self, row=None, column=None, sort=None, filter={}):
        lines = open(self.filepath, 'r', encoding='utf-8').readlines()
        return self.rm.ConvertLinesToRecords(lines, row=row, column=column, sort=sort, filter=filter)
# ===================================================================================
    @mylogger.deco
    def GetEmptyRecord(self):
        return self.rm.GetEmptyRecord()
# ===================================================================================
    @mylogger.deco
    def GetDataColumns(self):
        return self.rm.GetDataColumns()
# ===================================================================================
    @mylogger.deco
    def AddOnUpdateCallback(self, callback):
        self.callbacks.append(callback)
# ===================================================================================
    @mylogger.deco
    def OnUpdate(self):
        for callback in self.callbacks:
            callback()
# ===================================================================================
if __name__ == '__main__':
    data = MyDataBase("../data/MyDataBaseTest.txt", ['column1'])
    # data = MyDataBase("../data/MyDataBaseTest.txt", ['column1', 'column2', 'column3', 'column4'])
    # data = MyDataBase("../data/MyDataBaseTest.txt", ['column1', 'column2', 'column3', 'column4', 'column5'])
    data.DeleteRecords()
    record1 = data.GetEmptyRecord()
    record1['data']['column1'] = "test1"
    record2 = data.GetEmptyRecord()
    record2['data']['column1'] = "test2"
    record3 = data.GetEmptyRecord()
    record3['data']['column1'] = "test1"
    data.PushbackRecords([record1, record2, record3])
    print(data.GetRecords())
    print(data.GetRecords(row=-1))
    print(data.GetRecords(sort="column1"))
    print(data.GetRecords(filter={"column1":"test2"}))
    print(data.GetRecords())
    data.DeleteRecords(1)
    print(data.GetRecords())
    # print(data.GetRecords(filter={"column1":"test2"}))
    input("press any key ...")
# ===================================================================================