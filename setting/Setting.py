from typing import Any

from setting.SettingSupport import SettingSupport

class Setting(SettingSupport):
    __keyTables:str = 'tableName'
    __keyColumns:str = 'columns'
    __keyIsProcess:str = 'isProcess'
    __keySheet:str = 'sheetName'
    __keyTableAlias:str = 'tableAlias'
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
                    self.__keySheet: tbl.get(self.__keySheet, ''),
                    self.__keyTableAlias: tbl.get(self.__keyTableAlias, '')
                }

    def _GetSaveSettingData(self)->dict[str, Any]:
        data = super()._GetSaveSettingData()
        tables_list = []
        for name, config in self.tablesConfig.items():
            tables_list.append({
                self.__keyName: name,
                self.__keyColumns: config[self.__keyColumns],
                self.__keyIsProcess: config[self.__keyIsProcess],
                self.__keySheet: config[self.__keySheet],
                self.__keyTableAlias: config[self.__keyTableAlias]
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

    def GetTableAlias(self, tableName:str)->str:
        _data = self.tablesConfig.get(tableName)
        if _data:
            return _data.get(self.__keyTableAlias, tableName)
        return tableName

    def GetSheetName(self, tableName:str)->str | None:
        _data = self.tablesConfig.get(tableName)
        if _data:
            return _data.get(self.__keySheet, None)
        return None

    def GetProcessableTables(self)->list[tuple[str, bool]]:
        result:list[str] = [
            name
            for name, config in self.tablesConfig.items()
            if config.get(self.__keyIsProcess, False)
        ]
        return [(s, True) for s in result]

    def GetTables(self)->list[str]:
        return list(set([name for name, config in self.tablesConfig.items()]))

    def SaveOrUpdateTableConfig(self, tableName:str, columns:list[str], isProcess:bool, sheetName:str, tableAlias:str, autoSave:bool=True)->None:
        if not tableName: return

        self.tablesConfig[tableName] = {
            self.__keyColumns: columns,
            self.__keyIsProcess: isProcess,
            self.__keySheet: sheetName,
            self.__keyTableAlias: tableAlias
        }
        if autoSave:
            self.SaveSetting()
