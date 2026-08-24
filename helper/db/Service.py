import sqlite3
from sqlite3 import Connection
from enum import Enum
from typing import Any

class TypeQuerySource(Enum):
    LIST=0
    SINGLE=1
    UNDEFINED = -1

class Service:
    def __init__(self, _dbPath:str):
        self.dbPath = _dbPath

    def __getTypeQuerySource(self, _query: str | list[str])->TypeQuerySource:
        try:
            if _query is None: return TypeQuerySource.UNDEFINED
            if isinstance(_query, (list | tuple)):
                if all(isinstance(s, str) for s in _query): return TypeQuerySource.LIST
            elif isinstance(_query, str): return TypeQuerySource.SINGLE

            return TypeQuerySource.UNDEFINED
        except:
            return TypeQuerySource.UNDEFINED
    
    def ExecuteQuery(self, _query: str | list[str], _params: list | tuple | None = None)->bool:
        _typeQuery:TypeQuerySource = self.__getTypeQuerySource(_query)
        if _typeQuery == TypeQuerySource.UNDEFINED: return False
        _paramsData = () if not _params else _params
        conn: Connection | None = None
        try:
            conn = sqlite3.connect(self.dbPath)
            cursor = conn.cursor()
            match(_typeQuery):
                case TypeQuerySource.LIST: 
                    for s in _query: cursor.execute(s, _paramsData)
                case TypeQuerySource.SINGLE: cursor.execute(str(_query), _paramsData)

            conn.commit()            
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            raise e

        finally:
            if conn: conn.close()

    def ExecuteInsertQuery(self, _query: str, _params: list | tuple | None = None)->int | None:
        _typeQuery:TypeQuerySource = self.__getTypeQuerySource(_query)
        if _typeQuery == TypeQuerySource.UNDEFINED: return False
        _paramsData = () if not _params else _params
        conn: Connection | None = None
        result:int | None = None
        try:
            conn = sqlite3.connect(self.dbPath)
            cursor = conn.cursor()
            match(_typeQuery):
                case TypeQuerySource.SINGLE: cursor.execute(_query, _paramsData)

            result = cursor.lastrowid
            conn.commit()            
            return result
        except:
            if conn:
                conn.rollback()
            return None

        finally:
            if conn: conn.close()

    def ReturnQueryResult(self, _query: str, _params: list | tuple | None = None, _asDict:bool=False, 
                          _asList:list[int] | None = None)->list[Any] | None:
        _typeQuery:TypeQuerySource = self.__getTypeQuerySource(_query)
        if _typeQuery == TypeQuerySource.UNDEFINED: return []
        _paramsData = () if not _params else _params
        
        result:list[Any] | None = None
        conn: Connection | None = None
        try:
            conn = sqlite3.connect(self.dbPath)
            if _asDict: conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            match(_typeQuery):
                case TypeQuerySource.SINGLE: 
                    cursor.execute(_query, _paramsData)
                    result = [dict(row) for row in cursor.fetchall()] if _asDict else cursor.fetchall()

            if _asList is not None and len(_asList):
                result = self.GetList(result, _asList)
            return result
        except Exception as e:
            raise e

        finally:
            if conn: conn.close()

    def ReturnTopOneQueryResult(self, _query: str, _params: list | tuple | None = None)->Any:
        _typeQuery:TypeQuerySource = self.__getTypeQuerySource(_query)
        if _typeQuery == TypeQuerySource.UNDEFINED: return False
        _paramsData = () if not _params else _params
        
        result:Any | None = None
        conn: Connection | None = None
        try:
            conn = sqlite3.connect(self.dbPath)
            cursor = conn.cursor()
            match(_typeQuery):
                case TypeQuerySource.SINGLE: 
                    cursor.execute(_query, _paramsData)
                    result = cursor.fetchone()

            if result is None: return result
            else: return result[0]
        except Exception as e:
            raise e

        finally:
            if conn: conn.close()

    def GetList(self, _data:list[Any] | None, _index:list[int] | None =None)->list[Any] | None:
        if _data is None or not any(_data): return None
        if _index is None or not any(_index): _index = [0]
        result:list[Any] = []
        for s in _data:
            temp:list[Any]=[]
            for _id in _index:
                try:         
                    temp.append(s[_id])
                except IndexError: pass
            if temp: result.append(temp)
        return result
