from abc import ABC
import os
import json
from tkinter import font


from typing import Any, Final

from ttkbootstrap import Messagebox


class SettingSupport(ABC):
    FONT_NAME_DEFAULT:Final[str]="Segoe UI"

    __fileName = "config.json"
    __keyFontName = "font_name"
    __keyFontSize = "font_size"

    def __init__(self):
        self.FileName:str = self.__fileName
        self._settingData:dict[str, Any] = self.LoadSetting()        
        if not self._settingData is None:
            self.__fontName = self._settingData.get(self.__keyFontName, self.FONT_NAME_DEFAULT)
            self.__fontSize = int(self._settingData.get(self.__keyFontSize, 8))
            self.DefaultFont = (self.__fontName, self.__fontSize)

    @property
    def HasData(self)->bool:
        return bool(self._settingData)

    @property
    def SettingDataList(self)->dict[str, Any]:
        return self._settingData

    def ConvertHexToBGR(self, _hexStr:str)->tuple[int, int, int]:
        _hexStr = _hexStr.lstrip("#")
        if len(_hexStr) != 6: return (0, 0, 0)
        r = int(_hexStr[0:2], 16)
        g = int(_hexStr[2:4], 16)
        b = int(_hexStr[4:6], 16)
        return (b, g, r)

    def GetFontSizeValue(self, _factor:float | None)->int:
        if _factor is None: _factor = 1  
        return int(self.__fontSize * _factor)

    def MakeFont(self, size:float=1, bold:bool=False, italic:bool=False, underline:bool=False)->font.Font:
        return font.Font(
                family=self.__fontName if self.__fontName and len(self.__fontName) else self.FONT_NAME_DEFAULT,
                size=int(self.__fontSize * (size if size != 0 else 1)),
                weight='bold' if bold else 'normal',
                slant="italic" if italic else 'roman',
                underline=underline,
                overstrike=False
            )
    
    def LoadSetting(self)->dict[str, Any]:
        supportPath = os.path.dirname(os.path.abspath(__file__))
        configFilename = os.path.join(supportPath, self.__fileName)
        defaultConfig:dict[str, Any] = {}
        
        if os.path.exists(configFilename):
            try:
                with open(configFilename, "r", encoding="utf-8") as f:
                    userDict = json.load(f)
                for k, v in userDict.items():
                    if isinstance(v, dict) and k in defaultConfig:
                        defaultConfig[k].update(v)
                    else:
                        defaultConfig[k] = v

                self._settingData = defaultConfig
            except Exception:
                pass
        return defaultConfig

    def _GetSaveSettingData(self)->dict[str, Any]:
        return {}

    def SaveSetting(self):
        _data:dict[str, Any] = self._GetSaveSettingData()
        if not _data: return
        self.__saveSettingData(_data)
        
    def __saveSettingData(self, _data:dict | None=None, _showAlert:bool=True):
        supportPath = os.path.dirname(os.path.abspath(__file__))
        configFilename = os.path.join(supportPath, self.__fileName)

        if not _data or not isinstance(_data, dict) or len(_data) <= 0:
            return
        _flag:bool=False
        for _key, _value in _data.items():
            try:
                self._settingData[_key] = _value
                _flag=True
            except: pass
        
        if _flag:
            try:
                with open(configFilename, "w", encoding="utf-8") as f:
                    json.dump(self._settingData, f, indent=4, ensure_ascii=False)
                if _showAlert: Messagebox.show_info(
                    "Configuration saved",
                    "Local runtime metrics and UI settings successfully committed to config.json",
                )
            except Exception as e:
                if _showAlert: Messagebox.show_error("Error", f"Could not write configuration payload: {e}")
