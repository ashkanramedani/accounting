"""
    Class Name : json_handler
    Version Code : 1.0.0
    Last Update : 2019-10-23 15:20:00
    Python Version : 3.7.0
"""

import json


class json_handler:
    def __init__(self, FilePath="", ShowJsonErrors=True):
        self.VERSION = "1.4.0 build:9705301047"  # Version of class
        self.Data = {}
        self.filePath = ""
        self.Separator = ":"
        self.ShowErrors = ShowJsonErrors
        self.ErrorMessage = ""
        if FilePath != "":
            result = self.open(FilePath)
            if not result:
                self.ErrorMessage = "[Init]: Input file not exists!"
                return
            self.filePath = FilePath

    def load(self, Data=None):
        if Data is None:
            Data = {}
        self.Data = Data

    def strToJson(self, strString="", Use=False):
        if strString == "":
            dictJson = {}
        else:
            strString = strString.replace("'", "\"")
            dictJson = json.loads(strString)
        if Use is True:
            self.Data = dictJson
        return dictJson

    def jsonToStr(self, Indent=4, SortKeys=True):
        Indent = int(Indent)
        return json.dumps(self.Data, indent=Indent, sort_keys=SortKeys)

    def open(self, FilePath):
        with open(FilePath) as data_file:
            self.Data = json.load(data_file)
            data_file.close()
            self.filePath = FilePath
        return self.Data

    def save(self, FilePath=""):
        if FilePath == "":
            FilePath = self.filePath
        with open(FilePath, 'w') as outfile:
            json.dump(self.Data, outfile, indent=4, sort_keys=True)
            outfile.close()

    def fetch(self, Path=""):
        Data = self.Data
        if Path == "":
            return Data
        if self.Separator in Path:
            Path = Path.split(self.Separator)
            for Key in Path:
                Data = Data[Key]
            return Data
        else:
            if Path in Data.keys():
                return Data[Path]

    def update(self, Path="", UpdateValue=None):
        if UpdateValue is None:
            UpdateValue = ""
        Data = self.Data
        if Path == "":
            return True
        if self.Separator in Path:
            Path = Path.split(self.Separator)
            for Key in Path:
                data = Data
                Data = data[Key]
            Data[Path[len(Path) - 1]] = UpdateValue
        else:
            if Path in Data.keys():
                Data[Path] = UpdateValue
            else:
                self.ErrorMessage = "[Update]: Key not found!"
                return False
        return self.Data

    def show(self, Indent=4, SortKeys=True):
        Indent = int(Indent)
        print(json.dumps(self.Data, indent=Indent, sort_keys=SortKeys))

    def keysInPath(self, Path=""):
        keys = []
        Data = self.Data
        if Path == "":
            return []
        if self.Separator in Path:
            Path = Path.split(self.Separator)
            for Key in Path:
                Data = Data[Key]
                keys.append(Key)
            return keys
        return Data.keys()

    def keys(self, Path=""):
        Data = self.Data
        if Path == "":
            return Data.keys()
        if self.Separator in Path:
            Path = Path.split(self.Separator)
            for Key in Path:
                Data = Data[Key]
            return Data.keys()
        return Data.keys()

    def add(self, Key, Value="", Path=""):
        print(Path)
        if Path != "":
            data = self.fetch(Path)
        else:
            data = self.Data
        if not data:
            self.ErrorMessage = "[Add]: Cannot fetch path!"
            return False
        if type(data) == dict:
            if Key in data.keys():
                self.ErrorMessage = "[Add]: Duplicate key!"
                return False
            Key = str(Key)
            data[Key] = Value
        elif type(data) == str:
            NewData = {Key: Value}
            res = self.update(Path, NewData)
            if not res:
                self.ErrorMessage = "[Add]: Cannot update key!"
                return False
        else:
            self.ErrorMessage = "[Add]: Unsupported data type!"
            return False
        return True
