import ctypes
import os
import sys
import threading
from typing import Any, Callable, Final

import tkinter as tk
from tkinter import ttk, filedialog 
from matplotlib import table
from numpy import maximum
from pandas import DataFrame
from traitlets import HasTraits
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox, Querybox

from openpyxl import load_workbook, Workbook
from openpyxl.worksheet._read_only import ReadOnlyWorksheet
from openpyxl.worksheet.worksheet import Worksheet
import pandas as pd

from setting.Setting import Setting
from helper.HelperControl import HelperControl, ControlStyleType, ScrolledCheckboxList
#from helper.HelperControlCustom import ScrolledCheckboxList
from process.DataTypeProcess import DataTypeDataTable


class ImportProcess(tb.Window):
    __TITLE_DEFAULT:Final[str] = 'Cost analysis process'
    __CAPTION_DICT_HEADERS = 'headers'
    __CAPTION_DICT_ROWS = 'rows'

    def __init__(self, themename:str='superhero'):
        super().__init__(themename=themename)

        self.__appSetDarkTitleBar()

        self.title(self.__TITLE_DEFAULT)
        self.state("zoomed")
        self.geometry("1440x880")
        self.protocol("WM_DELETE_WINDOW", self.onCloseApplication)

        self.__appClearConsole()
        appIcon = self.__appSetIcon()
        if appIcon: self.iconphoto(True, appIcon)

        self.settingApp: Setting = Setting()
        self.hp: HelperControl = HelperControl(self.settingApp, ControlStyleType.THEME)

        

        self.__setEnvirotmeVariables()
        self.__setPanels(self.hp)



    #region set app
    def __appSetDarkTitleBar(self):
        try:
            self.update()
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())

            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(1)

            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value)
            )
        except Exception as e:
            pass
        
    def __appClearConsole(self):
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()

    def __appSetIcon(self)->tk.PhotoImage | None:
        iconPath = self.__getPath(["app_icon.png"])
        if os.path.exists(iconPath):
            return tk.PhotoImage(file=iconPath)
        return None

    def onCloseApplication(self):
        self.__workbookSecureClose(self.sourceWorkbook)
        self.__workbookSecureClose(self.sourceWorkbookMeta)
        
        if hasattr(self, '_excelData'): self._excelData = {}
        if hasattr(self, '_dfDataList'): self._dfDataList = None
        if hasattr(self, '_dfDataListIsProcess'): self._dfDataListIsProcess = None

        self.destroy()
        self.quit()
        sys.exit(0)
    #endregion

    #region path
    # ---------------------------------------------------------------------------------------
    # Path:
    # ---------------------------------------------------------------------------------------
    def __getPath(self, folder)->str:
        supportDir:str = os.path.dirname(os.path.abspath(__file__))
        samplesFolder:str = os.path.join(supportDir, *folder)
        return samplesFolder
    #endregion

    #region helper
    def __setValuesComboBox(self, _ctr:tb.Combobox, data:list[str] | None = None):
        if not _ctr: return
        _isInSelf = _ctr in self.__dict__.values()
        if not _isInSelf: return
        _ctr.set('')
        _ctr.configure(values=[])
        if data is None: return
        _ctr.configure(values=data)
        _ctr.set(data[0])
    def __workbookSecureClose(self, wb:Workbook | None):
        if not wb: return
        _isInSelf = wb in self.__dict__.values()
        if not _isInSelf: return
        wb.close()
        wb = None
    def __isInSelf(self, _ctr)->bool:
        if not _ctr: return False
        result:bool = _ctr in self.__dict__.values()
        return result
    #endregion

    #region panels
    def __setEnvirotmeVariables(self):
        self.sourceFilePath:str | None = os.path.join(self.__getPath(['source']), 'IndexCostAnalysis.xlsx')
        self.sourceWorkbook:Workbook | None = None
        self.sourceWorkbookMeta: Workbook | None = None

        self._excelSheetActive: tk.StringVar = tk.StringVar()
        self._excelTableActive:tk.StringVar = tk.StringVar()
        self._excelProgressFile:tk.DoubleVar = tk.DoubleVar(value=0)
        self._excelData:dict={}
        self._dfDataList:list[DataTypeDataTable] | None = None
        self._dfDataListIsProcess:list[DataTypeDataTable] | None = None

        self._structTableNameActive:tk.StringVar = tk.StringVar()
        self._structTableIsProcess:tk.BooleanVar = tk.BooleanVar(value=False)
        

    def __setPanels(self, hp:HelperControl):
        if hp is None: return

        #region main layout
        # Panel set:
        _frmLeftPanel = hp.ControlFrameLeftPanel(self)
        _notebookLeft = hp.ControlNotebook(_frmLeftPanel)

        _frmTabLeftOne = hp.ControlFrameForColumnEnd(_notebookLeft)
        #_frmTabTwo = hp.ControlFrameForColumnEnd(_notebookLeft)

        _notebookLeft.add(_frmTabLeftOne, text="Excel file")
        #_notebookLeft.add(_frmTabTwo, text="Image summary")

        hp.ControlSeparator(self)
        # Panel get:
        _frmRightPanel = hp.ControlFrameRightPanel(self)
        _notebookRight = hp.ControlNotebook(_frmRightPanel)
        _frmTabRightOne = hp.ControlFrameForColumnEnd(_notebookRight)
        _frmTabRightTwo = hp.ControlFrameForColumnEnd(_notebookRight)

        _notebookRight.add(_frmTabRightOne, text="Viewer")
        _notebookRight.add(_frmTabRightTwo, text="Struct")
        #endregion

        #region left
        _frmPathExcelFile = hp.ControlLabelFrameForRow(_frmTabLeftOne, "Workbook")
        _frmRow0:tb.Frame = hp.ControlFrameForRow(_frmPathExcelFile)
        self._cboSheet:tb.Combobox = hp.ControlComboBoxWithLabelWidth(_frmRow0, 'Sheets', 
                                            _command=self.__wbLoadTableBySheet,
                                            _textVariable=self._excelSheetActive,
                                            _width=18)
        self._cboTable:tb.Combobox = hp.ControlComboBoxWithLabelWidth(_frmRow0, 'Table',
                                            _textVariable=self._excelTableActive,
                                            _expand=True)

        _frmRow1:tb.Frame = hp.ControlFrameForRow(_frmPathExcelFile)
        self._cmdOpen = hp.ControlButtonLEFT(_frmRow1, 'Open', _command=self.__wbReadStructFile)
        self._cmdOpen = hp.ControlButtonLEFT(_frmRow1, 'Read', _command=self.__wbLoadAsync)
        self._cmdDataTable = hp.ControlButtonRIGHT(_frmRow1, 'Data table', _command=self.__onTableSelected)
        
        _frmRow2:tb.Frame = hp.ControlFrameForRow(_frmPathExcelFile)
        self._lblStatus:tb.Label = hp.ControlLabelInfoLEFT(_frmRow2, '...')

        _frmRow3:tb.Frame = hp.ControlFrameForRow(_frmPathExcelFile)
        self.progress_bar = hp.ControlProgressBar(_frmRow3, _variable=self._excelProgressFile)

        _frmSheetsProcess:tb.Labelframe = hp.ControlLabelFrameForRow(_frmTabLeftOne, "Sheets of process")
        self._lstChkSheetIsProcess:ScrolledCheckboxList = hp.ControlScrolledCheckboxList(
                                                        _frmSheetsProcess, 
                                                        None,
                                                        self.settingApp.GetProcessableTables())

        
        
        _frmNullPanel = hp.ControlFrameForRowEnd(_frmTabLeftOne)
        #endregion

        #region right
        #------------------------------------------------------------------------------------
        # Viewer
        #------------------------------------------------------------------------------------
        _frmViewer:tb.Labelframe = hp.ControlLabelFrameForRowEnd(_frmTabRightTwo, 'Data')
        self._twViewer:tb.Treeview = hp.ControlTreeviewClear(_frmViewer)

        #------------------------------------------------------------------------------------
        # Struct
        #------------------------------------------------------------------------------------
        _frmStruct:tb.LabelFrame = hp.ControlLabelFrameForRowEnd(_frmTabRightOne, "Metadata")

        _frmRowStruct01:tb.Frame = hp.ControlFrameForRow(_frmStruct)
        self._cboStructTable:tb.Combobox = hp.ControlComboBoxWithLabelWidth(_frmRowStruct01, 'Tables', 
                                            _textVariable=self._structTableNameActive,
                                            _command=self.__wsStructMakeStruct,
                                            _width=45)
        self._cmdStructSave:tb.Button = hp.ControlButtonRIGHT(_frmRowStruct01, 'Save struct', 
                                        _command=self.__wsStructSave)

        
        _frmRowStruct02:tb.Frame = hp.ControlFrameForRow(_frmStruct)
        self._chkStructIsProcess:tb.Checkbutton = hp.ControlCheckbox(_frmRowStruct02, 'Is process table', 
                                            _variable=self._structTableIsProcess)


        _frmRowStruct03:tb.Frame = hp.ControlFrameForRowEnd(_frmStruct)
        self._lstChkStructColumns:ScrolledCheckboxList = hp.ControlScrolledCheckboxList(_frmRowStruct03, 'Columns of table')
        
        #endregion
        #------------------------------------------------------
        # set:
    #endregion

    #region workbook actions
    def __wbLoadAsync(self, filePath:str | None = None):
        self._cmdOpen.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        self._dfDataListIsProcess = []
        self._dfDataList = []

        if filePath is None:
            filePath = filedialog.askopenfilename(
                filetypes=[("Excel Files", "*.xlsx")]
            )
            if not filePath:
                return
        else:
            filePath = filePath

        if not filePath or not os.path.exists(filePath): return
        self.sourceFilePath = filePath

        threading.Thread(
            target=self.__wbReadFile, args=(filePath, self.__wbProgressLoad), daemon=True
        ).start()

    def __wbReadStructFile(self):
        try:
            self.__setValuesComboBox(self._cboStructTable)
            filePath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
            if not filePath:
                    return
            self.sourceFilePath = filePath
            self.sourceWorkbookMeta = load_workbook(filePath, data_only=True, read_only=False)

            _sheetWithTable = []
            _tablesOfBook:list[str] = []
            for sheetName in self.sourceWorkbookMeta.sheetnames:
                ws:Worksheet = self.sourceWorkbookMeta[sheetName]
                if ws.tables and ws.sheet_state == 'visible':
                    _sheetWithTable.append(sheetName)
                    _tables = [str(s) for s in ws.tables.keys()]
                    if _tables:
                        _tablesOfBook.extend(_tables)

            if not _tablesOfBook:
                self.after(0, self.__wbIssueLoadFile, "Tables not found (ListObjects).")
                return

            self.__setValuesComboBox(self._cboStructTable, _tablesOfBook)

            if self.sourceWorkbookMeta:
                self.after(0, self.__wbLoadSheet)

        except Exception as e:
            self.after(0, self.__wbIssueLoadFile, str(e))
    
    def __wsStructMakeStruct(self):
        tableName:str = self._structTableNameActive.get()
        if not tableName or self.sourceWorkbookMeta is None: return
        wb:Workbook = self.sourceWorkbookMeta 
        _columns:list[str] = []
        if not wb: return
        for sheet_name in wb.sheetnames:
            ws:Worksheet = wb[sheet_name]
            if tableName in ws.tables.keys():
                table = ws.tables[tableName]
                _t = [str(col.name) for col in table.tableColumns]
                _columns.extend(_t)

        if not _columns: return
        if not self.__isInSelf(self._lstChkSheetIsProcess): return
        self._lstChkStructColumns.SetItems(_columns)

    def __wsStructSave(self):
        tableName:str = self._structTableNameActive.get()
        tableIsProcess:bool = self._structTableIsProcess.get()
        tableColumns:list[str] = self._lstChkStructColumns.GetCheckedItems()
        if tableName and tableColumns:
            self.settingApp.SaveOrUpdateTableConfig(tableName, tableColumns, tableIsProcess)


    def __wbReadFile(self, filePath:str, progressCallback: Callable[[float, str], None] | None = None):
        try:
            self._excelData.clear()
            self.sourceWorkbookMeta = load_workbook(filePath, data_only=True, read_only=False)

            _sheetWithTable = []
            for sheetName in self.sourceWorkbookMeta.sheetnames:
                ws = self.sourceWorkbookMeta[sheetName]
                if ws.tables and ws.sheet_state == 'visible':
                    _sheetWithTable.append(sheetName)

            if not _sheetWithTable:
                self.after(0, self.__wbIssueLoadFile, "Tables not found (ListObjects).")
                return

            self.sourceWorkbook = load_workbook(filePath, data_only=True, read_only=True)


            _rowCount: int = sum(
                                getattr(self.sourceWorkbook[s], "max_row", 0) or 0
                                for s in _sheetWithTable
                            )        
            _rowProcess:int = 0

            for sheetName in _sheetWithTable:
                sheet = self.sourceWorkbook[sheetName]
                _dataSheet = []
                
                if isinstance(sheet, (ReadOnlyWorksheet, Worksheet)):
                    for row in sheet.iter_rows(values_only=True):
                        _dataSheet.append(list(row))
                        _rowProcess += 1
                        
                        if progressCallback and _rowCount > 0:
                            _value:float = float((_rowProcess / _rowCount) * 100)
                            progressCallback(_value, f"Read -> {sheet.title} ||| (Row: {_rowProcess:05d} of {_rowCount:05d})")
                        
                self._excelData[sheet.title] = _dataSheet

            #self.sourceWorkbook.close()

            if self.sourceWorkbookMeta:
                self.after(0, self.__wbLoadSheet)

        except Exception as e:
            self.after(0, self.__wbIssueLoadFile, str(e))

        if self.sourceWorkbook:
            self.__wbLoadSheet()

    def __wbProgressLoad(self, _value: float, _sheetData: str):
        if hasattr(self, '_excelProgressFile'): self._excelProgressFile.set(value=_value)
        self._lblStatus.config(text=f'Process: {_sheetData}')

    def __wbEndingLoad(self):
        self._lblStatus.config(text='Load successful')
        self._cmdOpen.config(state=tk.NORMAL)

    def __wbIssueLoadFile(self, _message: str):
        self._lblStatus.config(text=_message)
        self._cmdOpen.config(state=tk.NORMAL)

    def __wbLoadSheet(self) -> list[str]:
        if hasattr(self, '_cboSheet'): self.__setValuesComboBox(self._cboSheet)
        if hasattr(self, '_cboTable'): self.__setValuesComboBox(self._cboTable)
        if not self.sourceWorkbookMeta: return []
        if not self._excelData: return []
        values: list[str] = list(self._excelData.keys())
        self.__setValuesComboBox(self._cboSheet, values)
        return values

    def __wbLoadTableBySheet(self) -> list[str]:
        if hasattr(self, '_cboTable'): self.__setValuesComboBox(self._cboTable)
        if not hasattr(self, '_cboSheet') or not hasattr(self, '_excelSheetActive'): return []
        sheet_name = self._excelSheetActive.get()
        if not sheet_name: return []
        if not self.sourceWorkbookMeta or sheet_name not in self.sourceWorkbookMeta.sheetnames:
            return []

        ws = self.sourceWorkbookMeta[sheet_name]
        tables_dict = getattr(ws, 'tables', {})
        values: list[str] = list(tables_dict.keys()) if tables_dict else []
        if values: self.__setValuesComboBox(self._cboTable, values)
        return values
        
    def __wbGetTableDataByName(self, sheetName:str, tableName:str) -> dict[str, list]:
        defaultReturn:dict[str, list] = {self.__CAPTION_DICT_HEADERS: [], self.__CAPTION_DICT_ROWS: []}
        if not self.sourceWorkbookMeta or sheetName not in self.sourceWorkbookMeta:
            return defaultReturn

        ws_meta:Worksheet = self.sourceWorkbookMeta[sheetName]

        if tableName not in ws_meta.tables:
            return defaultReturn

        excel_table = ws_meta.tables[tableName]
        table_range = excel_table.ref 
        if not table_range: 
            return defaultReturn

        from openpyxl.utils.cell import range_boundaries

        tupleRef:list[int] = [-1, -1, -1, -1]
        min_col, min_row, max_col, max_row = range_boundaries(table_range)
        for i, s in enumerate([min_col, min_row, max_col, max_row]):
            if isinstance(s, int): tupleRef[i] = int(s)
            else: return defaultReturn

        if not tupleRef or len(tupleRef) <= 0:
            return defaultReturn

        raw_sheet_data = self._excelData.get(sheetName, [])
        if not raw_sheet_data:
            return defaultReturn

        _colMin, _rowMin, _colMax, _rowMax = tupleRef 
        table_rows = []
        for r in range(_rowMin - 1, _rowMax):
            if r < len(raw_sheet_data):
                row_segment = raw_sheet_data[r][_colMin - 1 : _colMax]
                table_rows.append(row_segment)

        if not table_rows:
            return defaultReturn

        headers = table_rows[0]
        data_rows = table_rows[1:]

        return {self.__CAPTION_DICT_HEADERS: headers, self.__CAPTION_DICT_ROWS: data_rows}

    def __wbGetTableAsDataFrame(self, sheetName: str, tableName: str) -> pd.DataFrame:
        dataList:dict[str, Any] = self.__wbGetTableDataByName(sheetName, tableName)

        headers = dataList[self.__CAPTION_DICT_HEADERS]
        rows = dataList[self.__CAPTION_DICT_ROWS]

        if not headers:
            return pd.DataFrame()

        df = pd.DataFrame(rows, columns=headers)

        allowedColumns = self.settingApp.GetColumnsByTable(tableName)
        if allowedColumns:
            validColumns = [c for c in allowedColumns if c in df.columns]
            if validColumns:
                df = df[validColumns]

        self.__addToDataFrame(tableName, df)

        return df

    def __onTableSelected(self):
        sheet_name = self._excelSheetActive.get()
        table_name = self._excelTableActive.get()
        tree = self._twViewer
        if not sheet_name or not table_name and not tree:
            return

        df = self.__wbGetTableAsDataFrame(sheet_name, table_name)

        for item in tree.get_children():
            tree.delete(item)

        self.hp.ControlTreeviewSetLayout(tree, df)
        
        df_clean = df.fillna('')

        for _, row in df_clean.iterrows():
            tree.insert('', tk.END, values=list(row))

    def __addToDataFrame(self, name:str, df:DataFrame):
        if self._dfDataList is None: self._dfDataList = []
        if self._dfDataListIsProcess is None: self._dfDataListIsProcess = []
        tableIsProcess:list[str] = self._lstChkSheetIsProcess.GetCheckedItems()
        if not tableIsProcess:
            self._dfDataList.append(DataTypeDataTable(name, df))
        if name in tableIsProcess: self._dfDataListIsProcess.append(DataTypeDataTable(name, df))
        else: self._dfDataList.append(DataTypeDataTable(name, df))

    #endregion

    

if __name__ == "__main__":
    app = ImportProcess(themename='superhero')
    app.mainloop()
