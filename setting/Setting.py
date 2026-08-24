from typing import Any

from setting.SettingSupport import SettingSupport

class Setting(SettingSupport):
    __keyTables:str = 'tableName'
    __keyColumns:str = 'columns'
    __keyIsProcess:str = 'isProcess'
    __keyName:str = 'name'
    
    def __init__(self):
        super().__init__()
        raw_tables: list[dict[str, Any]] = self._settingData.get(self.__keyTables, [])

        self.tablesConfig: dict[str, dict[str, Any]] = {}

        for tbl in raw_tables:
            name = tbl.get(self.__keyName)
            if name:
                self.tablesConfig[name] = {
                    self.__keyColumns: tbl.get(self.__keyColumns, []),
                    self.__keyIsProcess: tbl.get(self.__keyIsProcess, False),
                }

    def _GetSaveSettingData(self)->dict[str, Any]:
        data = super()._GetSaveSettingData()
        tables_list = []
        for name, config in self.tablesConfig.items():
            tables_list.append({
                self.__keyName: name,
                self.__keyColumns: config[self.__keyColumns],
                self.__keyIsProcess: config[self.__keyIsProcess],
            })

        data[self.__keyTables] = tables_list
        return data

    def GetColumnsByTable(self, tableName:str)->list[str] | None:
        _data = self.tablesConfig.get(tableName)
        if _data:
            return _data.get(self.__keyColumns)
        return None

    def IsTableProcessable(self, tableName:str)->bool:
        _data = self.tablesConfig.get(tableName)
        if _data:
            return _data.get(self.__keyIsProcess, False)
        return False

    def GetProcessableTables(self)->list[str]:
        return [
            name
            for name, config in self.tablesConfig.items()
            if config.get(self.__keyIsProcess, False)
        ]

    def SaveOrUpdateTableConfig(self, tableName:str, columns:list[str], isProcess:bool, autoSave:bool=True)->None:
        if not tableName: return

        self.tablesConfig[tableName] = {
            self.__keyColumns: columns,
            self.__keyIsProcess: isProcess
        }
        if autoSave:
            self.SaveSetting()
