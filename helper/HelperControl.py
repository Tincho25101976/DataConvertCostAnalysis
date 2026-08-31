from enum import Enum
from dataclasses import dataclass
import math
import copy
import re
from typing import Any, Callable, Final, Literal, Optional, Protocol, Union, TypeVar, get_args, runtime_checkable

import tkinter as tk
from tkinter import ttk, font as tkFont
from unittest import result
from colorama import Style
import pandas as pd
from sympy import true
import ttkbootstrap as tb

from setting.Setting import Setting
from helper.HelperToolTip import ToolTip

TFrame = TypeVar('TFrame', bound=tk.Frame | tk.Misc)
AnchorType = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
SideType = Literal['left', 'right', 'top', 'bottom']
FillType = Literal['none', 'x', 'y', 'both']
ScrollOrientation = Literal["vertical", "horizontal"]

#region StatusDock
class StatusDock(Enum):
    NORMAL=0
    LEFT=1
    RIGHT=2
#endregion

#-------------------------------------------------------
# TKLabelType
#-------------------------------------------------------
#region TKLabelType
class TKLabelType(Enum):
    NORMAL=0
    INFORMATION=1
    COUNT=2
    SUMMARY=3
#endregion

#-------------------------------------------------------------------------------
# GeometryType
#-------------------------------------------------------------------------------
#region GeometryType
class GeometryType(Enum):
    Pack=0
    Grid=1
    Place=2
    Undefined=-1
#endregion

#-------------------------------------------------------------------------------
# ControlStyleType
#-------------------------------------------------------------------------------
#region ControlStyleType
class ControlStyleType(Enum):
    NORMAL=0
    THEME=1
#endregion

#-------------------------------------------------------------------------------
# ItemStructTreeview
#-------------------------------------------------------------------------------
#region ItemStructTreeview
@dataclass(frozen=True)
class ItemStructTreeview:
    key:str
    text:str
    width:int=50
    anchor:AnchorType=tk.CENTER
    minWidth:int=80
    stretch:bool=False
    def __post_init__(self):
        object.__setattr__(self, 'key', self.key.strip())

#endregion

#-------------------------------------------------------------------------------
# HelperItemLayout
#-------------------------------------------------------------------------------
#region HelperItemLayout
@dataclass(frozen=True)
class HelperItemLayout:
    side:str=tk.NONE
    fill:str=tk.NONE
    expand:bool=False
    anchor:str | None=tk.NONE
    relief:str=tk.NONE
    bd:float=0.0
    row:int=0 
    column:int=0 
    sticky:str=tk.NSEW
    padx:tuple[float, float] | float =(1, 3)
    pady:tuple[float, float] | float =(1, 3)
    geometryType:GeometryType = GeometryType.Pack

    width:int | None=None

    @property
    def isSide(self)->bool: 
        value:bool = self.__isCheck(self.side) and isinstance(self.side, str) and self.side in get_args(SideType)
        return value
    @property
    def isFill(self)->bool: 
        value:bool = self.__isCheck(self.fill) and isinstance(self.fill, str) and self.fill in get_args(FillType)
        return value
    @property
    def isAnchor(self)->bool: 
        value:bool = self.__isCheck(self.anchor) and isinstance(self.anchor, str) and self.anchor in get_args(AnchorType)
        return value
    @property
    def isSticky(self)->bool: return self.__isCheck(self.sticky)
    @property
    def isRelief(self)->bool: return self.__isCheck(self.relief)
    @property
    def isWidth(self)->bool: return not self.width is None and self.width > 0

    @property
    def sideValue(self)->SideType:
        if isinstance(self.side, str) and self.side in get_args(SideType):
            return self.side  # type: ignore[return-value]
        return 'left'
    @property
    def fillValue(self)->FillType:
        if isinstance(self.fill, str) and self.fill in get_args(FillType):
            return self.fill  # type: ignore[return-value]
        return 'none'
    @property
    def anchorValue(self)->AnchorType:
        if isinstance(self.anchor, str) and self.anchor in get_args(AnchorType):
            return self.anchor  # type: ignore[return-value]
        return 'nw'
    @property
    def widthValue(self)->int: return self.width if self.width else 0
    @widthValue.setter
    def widthValue(self, value:int | None): 
        object.__setattr__(self, "width", value)

    def __isCheck(self, data:str | None)->bool:
        return not data is None and len(data) > 0 and not data == tk.NONE
    def configure(self, **kwargs):
        for _key, _value in kwargs.items():
            if hasattr(self, _key):
                object.__setattr__(self, _key, _value)
        return self

    def clone(self, **kwargs)->'HelperItemLayout':
        data:HelperItemLayout = copy.deepcopy(self)
        for _key, _value in kwargs.items():
            if hasattr(data, _key):
                object.__setattr__(data, _key, _value)
        return data
#endregion

#-------------------------------------------------------------------------------
# Checkeable
#-------------------------------------------------------------------------------
#region ScrollableWidget
@runtime_checkable
class ScrollableWidget(Protocol):
    def yview(self, *args):
        ...

#endregion
   
#-------------------------------------------------------------------------------
# HelperControl
#-------------------------------------------------------------------------------
#region TBScrollableControl
TBScrollableControl = Union[
        tb.Treeview,
        tb.Canvas,
        tb.Text,
        tb.ScrolledText,
        tb.Listbox,
        tb.Entry,
        ScrollableWidget,
    ]
#endregion

#region HelperCustomStyle
class HelperCustomStyleName(Enum):
    _label:str
    LABEL_NORMAL_STYLE_NAME = (0, "CustomLabelNormal.primary.TLabel")
    LABEL_INFORMATION_STYLE_NAME = (1, "CustomLabelInformation.primary.TLabel")
    LABEL_COUNT_STYLE_NAME = (2, "CustomLabelCount.primary.TLabel")
    LABEL_SUMMARY_STYLE_NAME = (3, "CustomLabelSummary.primary.TLabel")
    LABEL_LINK_STYLE_NAME = (4, "CustomLabelLink.primary.TLabel")
    ENTRY_STYLE_NAME = (5, "CustomEntry.primary.TEntry")
    COMBOBOX_STYLE_NAME = (6, "CustomComboBox.primary.TCombobox")
    SCALE_STYLE_NAME = (7, "Horizontal.TScale")
    SCALE_LABEL_STYLE_NAME = (8, "CustomScale.primary.TLabel")
    RADIOBUTTON_STYLE_NAME = (9, "CustomRadiobutton.primary.TRadiobutton")
    FRAME_LABEL_STYLE_NAME = (10, "CustomLabelFrame.primary.TLabelframe")
    TEXT_STYLE_NAME = (11, "CustomTextBox.primary.TText")
    BUTTON_STYLE_NAME = (12, "CustomButtom.primary.TButton")
    SEPARATOR_STYLE_NAME = (13, "CustomSeparator.primary.TSeparator")
    PROGRESS_BAR_STYLE_NAME = (14, 'CustomProgressbar.primary.Horizontal.TProgressbar')
    TREEVIEW_STYLE_NAME  = (15, "CustomTreeview.primary.Treeview")
    CHECKBOX_STYLE_NAME = (16, "Custom.primary.TCheckbutton")
    NOTEBOOK_STYLE_NAME = (17, "Custom.TNotebook")

    TREEVIEW_STYLE_HEADING_NAME  = (100, "CustomTreeview.primary.Treeview.Heading")
    FRAME_LABEL_STYLE_LABEL_NAME = (101, "CustomLabelFrame.primary.TLabelframe.Label")
    NOTEBOOK_STYLE_TAB_NAME = (102, "Custom.TNotebook.Tab")

    PRIMARY_ROUNDTOGGLE_STYLE_NAME = (500, 'primary.Roundtoggle.Toolbutton')

    HELPER_STYLE_NAME = (999, 'CustomStyleHelper')

    UNDEFINED = (-1, '')

    def __new__(cls, value:int, label:str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._label = label
        return obj

    @property
    def label(self) -> str:
        return self._label

    @classmethod
    def FindByLabel(cls, label: str, _allowRaise:bool=True) -> 'HelperCustomStyleName':
        for member in cls:
            if member.label.lower() == label.lower():
                return member
        if _allowRaise: 
            raise ValueError(f"No {cls.__name__} member found with label: '{label}'")
        return HelperCustomStyleName.UNDEFINED

class HelperCustomStyle:
    #region Constants
    #TREEVIEW_STYLE_NAME:Final[str] = "CustomTreeview.primary.Treeview"
    #CHECKBOX_STYLE_NAME:Final[str] = "Custom.primary.TCheckbutton"
    #NOTEBOOK_STYLE_NAME:Final[str] = "Custom.TNotebook"

    #LABEL_NORMAL_STYLE_NAME:Final[str] = "CustomLabelNormal.primary.TLabel"
    #LABEL_INFORMATION_STYLE_NAME:Final[str] = "CustomLabelInformation.primary.TLabel"
    #LABEL_COUNT_STYLE_NAME:Final[str] = "CustomLabelCount.primary.TLabel"
    #LABEL_SUMMARY_STYLE_NAME:Final[str] = "CustomLabelSummary.primary.TLabel"
    #LABEL_LINK_STYLE_NAME:Final[str] = "CustomLabelLink.primary.TLabel"
    #ENTRY_STYLE_NAME:Final[str] = "CustomEntry.primary.TEntry"
    #COMBOBOX_STYLE_NAME:Final[str] = "CustomComboBox.primary.TCombobox"
    #SCALE_STYLE_NAME:Final[str] = "Horizontal.TScale"
    #SCALE_LABEL_STYLE_NAME:Final[str] = "CustomScale.primary.TLabel"
    #RADIOBUTTON_STYLE_NAME:Final[str] = "CustomRadiobutton.primary.TRadiobutton"
    #FRAME_LABEL_STYLE_NAME:Final[str] = "CustomLabelFrame.primary.TLabelframe"
    #TEXT_STYLE_NAME:Final[str] = "CustomTextBox.primary.TText"
    #BUTTON_STYLE_NAME:Final[str] = "CustomButtom.primary.TButton"
    #SEPARATOR_STYLE_NAME:Final[str] = "CustomSeparator.primary.TSeparator"
    #PROGRESS_BAR_STYLE_NAME:Final[str] = 'CustomProgressbar.primary.Horizontal.TProgressbar'

    COMBOBOX_WIDTH_DEFAULT:Final[int]=8
    SPINBOX_WIDTH_DEFAULT:Final[int]=5
    ENTRY_WIDTH_DEFAULT:Final[int]=40

    KEYWORD_BACKGROUND:Final[str] = 'background'
    KEYWORD_FOREGROUND:Final[str] = 'foreground'
    KEYWORD_FONT:Final[str] = 'font'

    HELPER_STYLE_NAME:Final[str] = 'CustomStyleHelper'
    #endregion

    #region Constructor
    def __init__(self, _settingApp: Setting, _style:tb.Style):
        self.settingApp:Setting = _settingApp

        self.__style:tb.Style = _style
        if not self.__style:
            return
        #--------------------------------------------------------
        # Colors:
        self.ColorPrimary = getattr(self.__style.colors, 'primary')
        self.ColorSelectBackground = getattr(self.__style.colors, 'selectbg')
        self.ColorSelectForeground = getattr(self.__style.colors, 'selectfg')
        self.ColorBackground = getattr(self.__style.colors, 'bg')
        self.ColorForeground = getattr(self.__style.colors, 'fg')

        self.__FOREGROUND_TREEVIEW_DEFAULT:Final[str]='#0f141c'
        self.__BACKGROUND_TREEVIEW_DEFAULT:Final[str]= self.ColorBackground 

        self.StyleDataList:list[str] = []

        def __setStyleConfigure(styleName:HelperCustomStyleName, **kw):
            if not self.__style: return
            self.__style.configure(styleName.label, **kw)
            if not styleName.label in self.StyleDataList:
                self.StyleDataList.append(styleName.label)

        def __setStyleMap(styleName:HelperCustomStyleName, **kw):
            if not self.__style: return
            self.__style.map(styleName.label, **kw)


        __setStyleConfigure(HelperCustomStyleName.PRIMARY_ROUNDTOGGLE_STYLE_NAME,
                    font=self.settingApp.MakeFont(bold=True, italic=True)
        )

        __setStyleConfigure(HelperCustomStyleName.SCALE_STYLE_NAME, 
                               font=self.settingApp.MakeFont(size=0.8, italic=True), troughcolor="#1e2530", 
                               groovewidth=6, sliderlength=20)
        __setStyleConfigure(HelperCustomStyleName.SCALE_LABEL_STYLE_NAME, 
                               font=self.settingApp.MakeFont(bold=True, italic=True))
        __setStyleConfigure(HelperCustomStyleName.LABEL_NORMAL_STYLE_NAME, 
                               font=self.settingApp.MakeFont(1.1, italic=True, bold=True), 
                               foreground="#e0e0e0")
        __setStyleConfigure(HelperCustomStyleName.LABEL_INFORMATION_STYLE_NAME, 
                               font=self.settingApp.MakeFont(1.1, italic=True, bold=True), 
                               foreground="#778899")
        __setStyleConfigure(HelperCustomStyleName.LABEL_SUMMARY_STYLE_NAME, 
                               font=self.settingApp.MakeFont(1.3, italic=True, bold=True), 
                               foreground=self.ColorForeground)
        __setStyleConfigure(HelperCustomStyleName.LABEL_COUNT_STYLE_NAME, 
                               font=self.settingApp.MakeFont(1.3, bold=True, italic=True), 
                               foreground="#778899")
        __setStyleConfigure(HelperCustomStyleName.LABEL_LINK_STYLE_NAME, 
                               font=self.settingApp.MakeFont(italic=True), 
                               foreground="#3498db")
        __setStyleConfigure(HelperCustomStyleName.ENTRY_STYLE_NAME, font=self.settingApp.DefaultFont)

        #--------------------------------------------------------
        # FrameLabel
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.FRAME_LABEL_STYLE_NAME, font=self.settingApp.MakeFont(italic=True))
        __setStyleConfigure(HelperCustomStyleName.FRAME_LABEL_STYLE_LABEL_NAME,
            font=self.settingApp.MakeFont(italic=True, bold=True, size=1.2),
            foreground="#ffffff",
        )
        #--------------------------------------------------------
        # Combobox
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.COMBOBOX_STYLE_NAME, font=self.settingApp.DefaultFont)
        self.ComboboxPopdownSettings = {
                                        "-background": "#2b2b2b",
                                        "-foreground": "#ffffff",
                                        "-selectbackground": self.ColorSelectBackground,
                                        "-selectforeground": self.ColorSelectForeground,
                                        "-font": self.settingApp.MakeFont(size=1.3, italic=True)
                                    }
        #--------------------------------------------------------
        # Treeview
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.TREEVIEW_STYLE_NAME,
                        background=self.__BACKGROUND_TREEVIEW_DEFAULT,
                        foreground='#f2f2f2',
                        fieldbackground="#1e2530",
                        rowheight=25,
                        font=self.settingApp.MakeFont(italic=True),
                        borderwidth=0,
                    )
        __setStyleConfigure(HelperCustomStyleName.TREEVIEW_STYLE_HEADING_NAME,
                        background='#000000',
                        foreground="#f2f2f2",
                        font=self.settingApp.MakeFont(bold=True, italic=True),
                        relief="flat",
                        padding=8,
                    )
        __setStyleMap(HelperCustomStyleName.TREEVIEW_STYLE_NAME, 
                        background=[("selected", "#d7d7d7")], foreground=[("selected", "#000000")])
        __setStyleMap(HelperCustomStyleName.TREEVIEW_STYLE_HEADING_NAME, 
                        background=[("active", "#192231")])
        #--------------------------------------------------------
        # Checkbutton
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.CHECKBOX_STYLE_NAME,
            font=self.settingApp.MakeFont(bold=True, italic=True),
            foreground="#e0e0e0",
            background=self.ColorBackground,
            indicatorbackground="#2d2d2d",
            indicatorforeground="#ffffff",
            padding=6,
        )
        __setStyleMap(HelperCustomStyleName.CHECKBOX_STYLE_NAME,
            indicatorbackground=[("pressed", "#ffffff"), ("selected", "#ffffff"), ("active", "#404040")],
            indicatorforeground=[("selected", "#000000")],
            foreground=[("active", "#ffffff"),  ("disabled", "#555555")],
            background=[("active", self.ColorBackground), ("pressed", self.ColorBackground), 
                        ("selected", self.ColorBackground), ("disabled", self.ColorBackground)],
        )
        #--------------------------------------------------------
        # Radiobutton
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.RADIOBUTTON_STYLE_NAME,
            font=self.settingApp.MakeFont(bold=True, italic=True),
            foreground="#e0e0e0",
            background=self.ColorBackground,
            indicatorbackground="#2d2d2d",
            indicatorforeground="#ffffff",
            indicatordiameter=14,
            padding=6,
        )
        __setStyleMap(HelperCustomStyleName.RADIOBUTTON_STYLE_NAME,
            indicatorbackground=[("pressed", "#ffffff"), ("selected", "#ffffff"), 
                                 ("active", "#404040"), ("disabled", "#222222")],
            indicatorforeground=[("selected", "#000000"), ("disabled", "#555555")],
            foreground=[("active", "#ffffff"), ("disabled", "#555555")],
            background=[("active", self.ColorBackground), ("pressed", self.ColorBackground), 
                        ("selected", self.ColorBackground), ("disabled", self.ColorBackground)],
        )
        #--------------------------------------------------------
        # Notebook
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.NOTEBOOK_STYLE_NAME,
            background="#1e1e1e", 
            borderwidth=0,
            tabmargins=[2, 5, 2, 0],  
        )
        __setStyleConfigure(HelperCustomStyleName.NOTEBOOK_STYLE_TAB_NAME,
            background="#2d2d2d",
            foreground="#888888",
            padding=[10, 8],
            font=self.settingApp.MakeFont(size=1.2, bold=True, italic=True),
            borderwidth=0,
            focuscolor="",
        )
        __setStyleMap(HelperCustomStyleName.NOTEBOOK_STYLE_TAB_NAME,
            background=[("selected", "#3d3d3d"), ("active", "#333333")],
            foreground=[("selected", "#ffffff"), ("active", "#e0e0e0")],
        )
        #--------------------------------------------------------
        # TextBox:
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.TEXT_STYLE_NAME,
                background=self.ColorBackground,
                foreground=self.ColorForeground,
                selectbackground='#375a7f',
                selectforeground=self.ColorForeground,
                insertbackground='#5bc0de',
                font=self.settingApp.MakeFont(1.2, italic=True),
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            )
        #--------------------------------------------------------
        # Button:
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.BUTTON_STYLE_NAME,
                font=self.settingApp.MakeFont(italic=True),
                background="#375a7f",
                foreground="#ffffff",
                bordercolor="#5bc0de",
                darkcolor="#375a7f",
                lightcolor="#375a7f",
                relief="flat",
                borderwidth=1,
                padding=(15, 8),
            )
        __setStyleMap(HelperCustomStyleName.BUTTON_STYLE_NAME,
                background=[ ("disabled", "#2b4c68"), ("pressed", "#2b4764"), ("active", "#4b77a9"), ],
                foreground=[ ("disabled", "#6c757d"), ("pressed", "#ffffff"), ("active", "#ffffff"), ],
                bordercolor=[("active", "#ffffff"), ("pressed", "#5bc0de")],
            )
        #--------------------------------------------------------
        # Separator:
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.SEPARATOR_STYLE_NAME, 
                background="#2b4c68", darkcolor="#2b4c68", lightcolor="#2b4c68")
        __setStyleMap(HelperCustomStyleName.SEPARATOR_STYLE_NAME, 
                background=[("disabled", "#153248")])

        #--------------------------------------------------------
        # ProgressBar:
        #--------------------------------------------------------
        __setStyleConfigure(HelperCustomStyleName.PROGRESS_BAR_STYLE_NAME,
                thickness=20,  # Grosor/Alto de la barra en píxeles
                troughcolor="#2c3e50",  # Color del carril/fondo de la barra
                #background="#1abc9c",  # Color del indicador de relleno (progreso)
                bordercolor="#34495e",  # Color del borde exterior
                borderwidth=1,  # Ancho del borde en píxeles
                paddings=2,  # Espaciado interno entre el carril y el relleno
            )
    #endregion

    #region Properties
    @property
    def style(self) -> tb.Style: return self.__style
    @style.setter
    def style(self, value: tb.Style): self.__style = value
    
    @property
    def styleDefault(self):
        _tag = self.__getDictionaryTag(self.KEYWORD_BACKGROUND, self.ColorBackground)
        _tag |= self.__getDictionaryTag(self.KEYWORD_FOREGROUND, self.ColorForeground)
        return _tag
    @property
    def styleDefaultInverted(self):
        _tag = self.__getDictionaryTag(self.KEYWORD_BACKGROUND, self.ColorForeground)
        _tag |= self.__getDictionaryTag(self.KEYWORD_FOREGROUND, self.ColorBackground)
        return _tag
    #endregion

    #region Methods
    def __getDictionaryTag(self, key:str, value):
        return {key.lower(): value}
    
    def GetStyleForTag(self, _background:str, _foreground:str | None=None, 
                       _size:float=1, _bold:bool=False, _italic:bool=True):
        if _size is None: _size=1
        if _bold is None: _bold=False
        if _italic is None: _italic=False
        if _foreground is None or len(_foreground) <= 0: _foreground = self.__FOREGROUND_TREEVIEW_DEFAULT
        _tag:dict[str, str] = {}
        _tag |= self.__getDictionaryTag(self.KEYWORD_BACKGROUND, _background)
        _tag |= self.__getDictionaryTag(self.KEYWORD_FOREGROUND, _foreground)
        _tag |= self.__getDictionaryTag(self.KEYWORD_FONT, self.settingApp.MakeFont(size=_size, bold=_bold, italic=_italic))
        return _tag

    def SetHelperStyle(self, _className:str, _background:str='#558833', _addName:str | None = None)->str | None:
        if not _className: return None
        result = self.MakeHelperStyleName(_className, _addName)
        if not result: return None
        self.style.configure(result, background=_background)
        return result

    def MakeHelperStyleName(self, _className:str, _addName:str | None = None)->str:
        return f"{self.HELPER_STYLE_NAME}{(_addName if _addName is not None else '')}.primary.{_className}"
    
    #endregion
#endregion

#region HelperItemLayoutControls
class HelperItemLayoutControls:
    def __init__(self):
        pass
    def _getHelperItemLayoutFrame(self, fill:str=tk.X, expand:bool=False, 
                                side:str=tk.NONE, width:int | None=None, anchor:str | None=None)-> HelperItemLayout:
        return HelperItemLayout(fill=fill, expand=expand, side=side, width=width, anchor=anchor)
        
    def _getHelperItemLayoutLabelFrame(self, side:str=tk.LEFT, fill=tk.BOTH, 
                                expand=True, width:int | None=None)-> HelperItemLayout:
        return HelperItemLayout(fill=fill, expand=expand, side=side, width=width)
    
    def _getHelperItemLayoutScale(self, side:str=tk.TOP, 
                                expand:bool=True, width:int | None=None)-> HelperItemLayout:
        return HelperItemLayout(fill=tk.X, expand=expand, side=side, width=width)
    
    def _getHelperItemLayoutLabelLink(self, side:str=tk.NONE, anchor:str=tk.E, 
                                expand:bool=False, pady:tuple[float, float]=(0, 3))-> HelperItemLayout:
        return HelperItemLayout(anchor=anchor, side=side, expand=expand, pady=pady)

    def _getHelperItemLayoutComboBox(self, fill:str=tk.X, 
                                expand:bool=False, side:str=tk.LEFT, width:int | None=None)-> HelperItemLayout:
        return HelperItemLayout(side=side, expand=expand, fill=fill, width=width)

    def _getHelperItemLayoutButton(self, side:str=tk.NONE, 
                                expand:bool=True, fill:str=tk.X, width:int | None=None)->HelperItemLayout:
        return HelperItemLayout(side=side, expand=expand, fill=fill, width=width)

    def _getHelperItemLayoutLabel(self, side=tk.NONE, anchor=tk.W, width:int | None=None)->HelperItemLayout:
        return HelperItemLayout(side=side, anchor=anchor, width=width, pady=(0, 1))

    def _getHelperItemLayoutEntry(self, side:str=tk.RIGHT, 
                                expand:bool=True, width:int | None=None)->HelperItemLayout:
        return HelperItemLayout(side=side, expand=expand, fill=tk.X, width=width)

    def _getHelperItemLayoutSpinbox(self, side:str=tk.BOTTOM, fill:str=tk.X, 
                                expand:bool=True, width:int |None=None)->HelperItemLayout:
        return HelperItemLayout(side=side, fill=fill, expand=expand, width=width)

    def _getHelperItemLayoutCheckBox(self, side=tk.LEFT, fill=tk.NONE, 
                                expand=False, width:int |None=None)->HelperItemLayout:
        return HelperItemLayout(side=side, fill=fill, expand=expand, width=width)
    
    def _getHelperItemLayoutProgressBar(self, side:str=tk.TOP, 
                                    expand:bool=True, width:int | None=None)-> HelperItemLayout:
            return HelperItemLayout(fill=tk.X, expand=expand, side=side, width=width)

#endregion

#region HelperControlTKinter
class HelperControlTKinter:
    def __init__(self, _setting:Setting, _style:tb.Style):
        self.settingApp:Setting = _setting
        self.cs:HelperCustomStyle= HelperCustomStyle(_setting, _style)
    
    #region Methods
    
    #region tkinter Classic
    '''
    def _getControlLabelFrame(self, _parent:tk.Misc, text:str, 
                _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.BOTH))->tk.LabelFrame: 
        result:tk.LabelFrame = tk.LabelFrame(
            _parent,
            text=f"{text}: ",
            padx=1,
            pady=1,
            **self.settingApp.SettingFrameLabel
        )
        self.__packagingWidget(result, _pack)  
        if not _pack is None and _pack.isRelief:
            result.config(bd=_pack.bd, relief=_pack.relief)
        return result
    def _getControlFrame(self, _parent:tk.Misc, 
                    _pack:HelperItemLayout=HelperItemLayout(fill=tk.X, expand=False))->tk.Frame:
        result = tk.Frame(_parent)
        self.__packagingWidget(result, _pack)
        if not _pack is None: 
            match(_pack.geometryType):
                case GeometryType.Pack:
                    if _pack.isWidth and (_pack.width > 50):
                        result.pack_propagate(False)
            if _pack.isRelief:
                result.config(bd=_pack.bd, relief=_pack.relief)
        return result
    def _getControlScale(self, _parent:tk.Misc, _text:str | None, _from:float, _to:float, 
                        _interval:float, _variable:tk.IntVar | tk.DoubleVar, _command=None, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.BOTTOM, fill=tk.X, expand=True))->tk.Scale:
        _frame = _parent
        if not _text is None and len(_text) > 0:
            _frame: tk.Frame = tk.Frame(_parent)
            _frame.pack(fill=tk.X, pady=1)
            _lbl:tk.Label = tk.Label(_frame, text=f"{_text}:", **self.settingApp.SettingLabel)
            _lbl.pack(anchor=tk.NW, padx=(0, 2))
        result:tk.Scale = tk.Scale(
            _frame,
            from_=_from,
            to=_to,
            resolution=_interval,
            orient=tk.HORIZONTAL,
            font=self.settingApp.DefaultSliderFont,
            width=10,
            takefocus=1,
            highlightthickness=1,
            highlightcolor="#2196F3",
            variable=_variable
        )
        if not _command is None: 
            def _executeCallback(e):
                try:
                    _command(e)
                except TypeError:
                    _command
                    
            result.config(command=_executeCallback)
        
        result.set(_variable.get())
        self.__packagingWidget(result, _pack.configure(anchor=tk.W))
        result.bind("<Button-1>", lambda event: event.widget.focus_set())
        return result
    def _getControlButton(self, _parent:tk.Misc, _text:str, _command, _state:bool=True, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.NONE, expand=True, fill=tk.X), 
                        _addSeparator:bool=False)->tk.Button:
        _frame:tk.Misc=_parent
        if _addSeparator: 
            _frame:tk.Frame = tk.Frame(_parent)
            _frame.pack(padx=(0, 2), pady=(2, 0))        
            if not _pack is None: 
                if _pack.isSide: _frame.pack(side=_pack.side)
                if _pack.expand: _frame.pack(expand=_pack.expand)
                if _pack.isFill: _frame.pack(fill=_pack.fill)
            ttk.Separator(_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))

        result:tk.Button = tk.Button(
            _frame,
            text=_text,
            command=_command,
            pady=2,
            padx=2,
            **self.settingApp.SettingButton
        )
        if _state: result.config(state=tk.NORMAL)
        else: result.config(state=tk.DISABLED)
        self.__packagingWidget(result, _pack)
        return result
    def _getControlLabel(self, _parent:tk.Misc, _text:str, _type:TKLabelType=TKLabelType.NORMAL, 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.NONE, anchor=tk.W, pady=(0, 1)))->tk.Label:
        _setting = None
        match(_type):
            case TKLabelType.NORMAL: _setting = self.settingApp.SettingLabel
            case TKLabelType.INFORMATION: _setting = self.settingApp.SettingLabelInfo
            case TKLabelType.COUNT: _setting = self.settingApp.SettingLabelCount
        
        result:tk.Label = tk.Label(_parent, **_setting) if _setting is not None else tk.Label(_parent)

        match(_type):
            case TKLabelType.NORMAL | TKLabelType.COUNT: 
                result.config(text=f"{_text}{":" if len(_text) > 0 else ""}")
            case TKLabelType.INFORMATION: result.config(text="...")

        self.__packagingWidget(result, _pack)
        return result
    def _getControlLabelLink(self, _parent:tk.Misc, _text:str, _command, 
                            _pack:HelperItemLayout=HelperItemLayout(anchor=tk.E, side=tk.NONE))->tk.Label:
        result:tk.Label = tk.Label(_parent, text=f"[{_text}]", **self.settingApp.SettingLabelLink)
        self.__packagingWidget(result, _pack)
        result.bind("<Button-1>", lambda event: _command())
        return result
    def _getControlEntry(self, _parent:tk.Misc, _commandValidate=None, 
                        _commandExecute=None, _textVariable=None, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.RIGHT, expand=True, fill=tk.X))->tk.Entry:
        result:tk.Entry = tk.Entry(
            _parent,
            font=self.settingApp.DefaultFont,
        )
        if not _commandValidate is None:
            result.config(validate="key", validatecommand=_commandValidate)

        if not _textVariable is None:
            result.config(textvariable=_textVariable)
        self.__packagingWidget(result, _pack)
        if not _commandExecute is None:
            result.bind("<Return>", _commandExecute)
            result.bind("<FocusOut>", _commandExecute)

        return result
    def _getControlEntryWithLabel(self, _parent:tk.Misc, _text:str, _commandValidate=None, 
                                _commandExecute=None, _textVariable:tk.Variable | None=None, 
                                _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=True, fill=tk.X), 
                                _addSeparator:bool=False)->tk.Entry:
        _frame = self.__getk.MiscWithLabel(_parent, _text, _addSeparator, _pack)
        result:tk.Entry = self._getControlEntry(_frame, _commandValidate=_commandValidate, 
                                _commandExecute=_commandExecute, _textVariable=_textVariable, 
                                _pack=_pack)
        return result
    def _getControlComboBox(self, _parent:tk.Misc, _values:list | None =None, 
                        _defaultValue=None, _command=None, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.X))->ttk.Combobox:
        result:ttk.Combobox = ttk.Combobox(
            _parent,
            **self.settingApp.SettingComboBox
        )
        if not _values is None: 
            result.config(values=_values)
            if not _defaultValue is None: result.set(_defaultValue)

        self.__packagingWidget(result, _pack)

        if _command is not None:
            if isinstance(_command, (list, tuple)):
                def _dispatch_all(e, funcs=_command):
                    for f in funcs:
                        if callable(f):
                            try:
                                f(e)
                            except TypeError:
                                f()

                result.bind("<<ComboboxSelected>>", _dispatch_all)

            elif callable(_command):
                result.bind("<<ComboboxSelected>>", _command)

        return result
    def _getControlComboBoxWithLabel(self, _parent:tk.Misc, _text:str, _values:list | None=None, 
                                    _defaultValue=None, _command=None, 
                                    _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.X), 
                                    _addSeparator:bool=False)->ttk.Combobox:
        _frame:tk.Frame = tk.Frame(_parent)
        _frame.pack(padx=(0, 2), pady=(2, 0))        
        if not _pack is None: 
            if _pack.isSide: _frame.pack(side=_pack.side)
            if _pack.expand: _frame.pack(expand=_pack.expand)
            if _pack.isFill: _frame.pack(fill=_pack.fill)

        if _addSeparator: ttk.Separator(_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))

        _lbl:tk.Label = tk.Label(_frame, text=f"{_text}:", **self.settingApp.SettingLabel)
        _lbl.pack(side=tk.LEFT, anchor=tk.NW, padx=(0, 2), pady=(2, 0))

        if not _pack is None: _pack.configure(side=tk.LEFT)
        result:ttk.Combobox = self._getControlComboBox(_frame, _values=_values, _defaultValue=_defaultValue, 
                                          _command=_command, _pack=_pack)

        return result
    def _getControlSeparator(self, _parent:tk.Misc, _orient:str=tk.VERTICAL, _pad:int=0):
        result = ttk.Separator(_parent, orient=_orient)
        if _pad < 0: _pad=0
        match (_orient):
            case tk.HORIZONTAL: result.pack(side=tk.TOP, fill=tk.X, pady=(_pad, 2))
            case tk.VERTICAL: result.pack(side=tk.LEFT, fill=tk.Y, padx=(_pad, 2))

        return result
    def _getControlSpinbox(self, _parent:tk.Misc, _text:str, _from:float, _to:float, _interval:float, 
                            _textVariable:tk.Variable, _defaultValue:float=0, 
                            _command=None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.BOTTOM, fill=tk.X, expand=True, width=8), 
                            _addSeparator:bool=False)->ttk.Spinbox:
        _frame:tk.Misc = _parent
        _frame.pack(padx=(0, 2), pady=(2, 0))        
        if not _pack is None: 
            if _pack.isSide: _frame.pack(side=_pack.side)
            if _pack.expand: _frame.pack(expand=_pack.expand)
            if _pack.isFill: _frame.pack(fill=_pack.fill)

        if _addSeparator: self._getControlSeparator(_frame)
        _format = "%.2f"
        if not _text is None and len(_text) > 0:
            _frame = tk.Frame(_parent)
            _frame.pack(fill=tk.X, pady=(2, 0))
            if _pack and _pack.isSide: _frame.pack(side=_pack.side)
            _lbl = tk.Label(_frame, text=f"{_text}:", **self.settingApp.SettingLabel)
            _lbl.pack(side=tk.LEFT, anchor=tk.NW, padx=(0, 2), pady=(2, 0))
        result: ttk.Spinbox = ttk.Spinbox(
                    _frame,
                    from_=_from,
                    to=_to,
                    increment=_interval,
                    format=_format,
                    textvariable=_textVariable,
                )
        def __formatDecimalsPlaceAndCommand(event=None):
            try:
                val = float(result.get())
                val = max(_from, min(_to, val))
                result.set(f"{val:.2f}")
            except ValueError:
                result.set(f"{_defaultValue:.2f}")

            if event and _command is not None:
                _command()

        result.bind("<Return>", __formatDecimalsPlaceAndCommand)
        result.bind("<FocusOut>", __formatDecimalsPlaceAndCommand)

        if not _command is None:
            result.config(command=_command)

        self.__packagingWidget(result, _pack)
        if not _defaultValue is None: result.set(f"{_defaultValue:.2f}")
        return result
    def _getControlTreeview(self, _parent:tk.Misc, 
                        _setting:list[ItemStructTreeview], 
                        _pack:HelperItemLayout=HelperItemLayout(tk.LEFT, tk.BOTH, True))->ttk.Treeview:
        if not _setting : raise ValueError("La lista de setting no puede ser nula o esta vacia...")  
        _columnsGrid = [s.key for s in _setting]
        result:ttk.Treeview = ttk.Treeview(
            _parent,
            columns=_columnsGrid,
            show="headings",
            selectmode="browse",
        )
        for c in _setting:
            result.heading(c.key, text=c.text, command=lambda c=c.key: self.__sortedColumnsTreeview(result, c, False))
            result.column(c.key, width=c.width, anchor=c.anchor)

        _scroll: tk.Scrollbar = tk.Scrollbar(_parent, orient=tk.VERTICAL, command=result.yview)
        result.configure(yscrollcommand=_scroll.set)
        self.__packagingWidget(result, _pack)
        _scroll.pack(side=tk.RIGHT, fill=tk.Y)

        return result
    def _getControlCheckbox(self, _parent: tk.Misc, _text: str, _variable: tk.BooleanVar, _command=None, 
                                _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.NONE, expand=False),
                                _tooltip:str | None=None)->ttk.Checkbutton:
        style = ttk.Style()
        style.configure("Transparent.TCheckbutton", background=_parent.cget("background"))
        result = ttk.Checkbutton(
            _parent,
            text=_text,
            variable=_variable,
            command=_command,
            **self.settingApp.SettingButton
        )
        self.__packagingWidget(result, _pack)
        if _tooltip:
            ToolTip(result, _tooltip, self.settingApp.DefaultToolTipFont)
        return result
    def _getControlNotebook(self, _parent:tk.Misc)->ttk.Notebook: 
        result:ttk.Notebook = ttk.Notebook(_parent)
        result.pack(fill=tk.BOTH, expand=True)
        return result
    '''
    #endregion
    
    #region tkBootstrap
    def _getControlLabelFrameBS(self, _parent:tk.Misc, text:str, 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.BOTH))->tb.LabelFrame: 
        result:tb.LabelFrame = tb.LabelFrame(
            _parent,
            text=f"{text}: ",
            padding=(5, 5),
            style=HelperCustomStyleName.FRAME_LABEL_STYLE_NAME.label
        )
        self.__packagingWidget(result, _pack)  
        #if not _pack is None and _pack.isRelief:
        #    result.config(bd=_pack.bd, relief=_pack.relief)
        return result
    def _getControlFrameBS(self, _parent:tk.Misc, 
                           _pack:HelperItemLayout=HelperItemLayout(fill=tk.X, expand=False))->tb.Frame:
        result:tb.Frame = tb.Frame(_parent)
        self.__packagingWidget(result, _pack)
        if not _pack is None: 
            match(_pack.geometryType):
                case GeometryType.Pack:
                    if _pack.isWidth and (_pack.width is not None and _pack.width > 50):
                        result.pack_propagate(False)
            #if _pack.isRelief:
            #    result.config(bd=_pack.bd, relief=_pack.relief)
        return result
    def _getControlScaleBS(self, _parent:tk.Misc, _text:str, _from:float, _to:float, 
                        _interval:float, _variable:tk.Variable, _command=None, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.BOTTOM, fill=tk.X, expand=True))->tb.Scale:
        _frame:tb.Frame 
        _label:tb.Label | None
        _frame, _label = self.__getFrameWithLabelBS(_parent, _text, False, _pack, _forceLabel=True)
        result: tb.Scale = tb.Scale(
            _frame,
            from_=_from,
            to=_to,
            takefocus=True,
            variable=_variable,
            style=HelperCustomStyleName.SCALE_STYLE_NAME.label
        )

        if _command is not None:
            def _executeCallback(event=None):
                val = result.get()
                callbacks = (_command if isinstance(_command, (list, tuple)) else [_command])
                for fn in callbacks:
                    if callable(fn):
                        try:
                            fn(val) 
                        except TypeError:
                            try:
                                fn(event)
                            except TypeError:
                                fn()

        self.__packagingWidget(result, _pack.configure(anchor=tk.W))
        result.bind("<Button-1>", lambda event: event.widget.focus_set())
        try:
            self.__onScaleMouseRelease(_label=_label, _text=_text, _value=_variable)
            result.bind("<B1-Motion>", _executeCallback)
            _variable.trace_add(
                        "write",
                        lambda *args: self.__onScaleMouseRelease(_label=_label, _text=_text, _value=_variable, _step=_interval)
                    )
            #result.bind("<ButtonRelease-1>", lambda s: self.__onScaleMouseRelease(_label=_label, text=_text, value=int(_variable.get())))
        except:
            pass
        return result
    def _getControlButtonBS(self, _parent:tk.Misc, _text:str, 
                            _command:Callable[..., Any],                             
                            _state:bool=True, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.NONE, 
                                            expand=True, fill=tk.X), _addSeparator:bool=False)-> tb.Button:
            _frame = _parent if not _addSeparator else self.GetFrameWithSeperator(_parent, _pack, 5)
            result: tb.Button = tb.Button(
                _frame,
                text=_text,
                command=_command,
                style=HelperCustomStyleName.BUTTON_STYLE_NAME.label
            )
            if _state: result.config(state=tk.NORMAL)
            else: result.config(state=tk.DISABLED)            

            self.__packagingWidget(result, _pack)
            return result
    def _getControlLabelBS(self, parent:tk.Misc, _text:str, 
                        _type:TKLabelType=TKLabelType.NORMAL, 
                        _variable:tk.StringVar | None = None,
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.NONE, anchor=tk.W, pady=(0, 1)))->tb.Label:
            _setting = None
            match(_type):
                case TKLabelType.NORMAL: _setting = HelperCustomStyleName.LABEL_NORMAL_STYLE_NAME.label
                case TKLabelType.INFORMATION: _setting = HelperCustomStyleName.LABEL_INFORMATION_STYLE_NAME.label
                case TKLabelType.COUNT: _setting = HelperCustomStyleName.LABEL_COUNT_STYLE_NAME.label
                case TKLabelType.SUMMARY: _setting = HelperCustomStyleName.LABEL_SUMMARY_STYLE_NAME.label
            
            result:tb.Label = tb.Label(parent, style=_setting)
    
            match(_type):
                case TKLabelType.NORMAL | TKLabelType.COUNT: 
                    result.config(text=f"{_text}{":" if len(_text) > 0 else ""}")
                case TKLabelType.INFORMATION | TKLabelType.SUMMARY: result.config(text="..." if len(_text) == 0 else _text)

            if _variable:
                result.configure(textvariable=_variable, text=_variable.get())
    
            self.__packagingWidget(result, _pack)
            return result
    def _getControlLabelLinkBS(self, _parent:tk.Misc, _text:str, 
                        _command:Callable[[], Any], 
                        _pack:HelperItemLayout=HelperItemLayout(anchor=tk.E, side=tk.NONE))->tb.Label:
        result:tb.Label = tb.Label(_parent, text=f"[{_text}]", cursor="hand2", 
                                style=HelperCustomStyleName.LABEL_LINK_STYLE_NAME.label)
        self.__packagingWidget(result, _pack)
        result.bind("<Button-1>", lambda event: _command())
        return result    
    def _getControlEntryBS(self, _parent:tk.Misc, _commandValidate=None, _commandExecute=None, _textVariable=None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.RIGHT, expand=True, fill=tk.X),
                            _status:bool=True,
                            _width:int|None = None)->tb.Entry:
        result: tb.Entry = tb.Entry(
            _parent,
            style=HelperCustomStyleName.ENTRY_STYLE_NAME.label
        )
        if not _commandValidate is None:
            result.configure(validate="key", validatecommand=_commandValidate)

        if not _textVariable is None:
            result.configure(textvariable=_textVariable)

        result.configure(state=(tk.NORMAL if _status else tk.DISABLED))  
        if not _width is None:
            result.configure(width=_width)

        self.__packagingWidget(result, _pack)
        if not _commandExecute is None:
            result.bind("<Return>", _commandExecute)
            result.bind("<FocusOut>", _commandExecute)

        return result
    def _getControlEntryWithLabelBS(self, _parent:tk.Misc, _text:str, _commandValidate=None, 
                            _commandExecute=None, _textVariable:tk.Variable | None=None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=True, fill=tk.X), 
                            _addSeparator:bool=False,
                            _status:bool=True,
                            _width:int | None = None)->tb.Entry:
        _frame:tb.Frame = self.__getFrameWithLabelBS(_parent, _text, _addSeparator, _pack)[0]
        result:tb.Entry = self._getControlEntryBS(_frame, _commandValidate=_commandValidate, 
                                    _commandExecute=_commandExecute, 
                                    _textVariable=_textVariable, _pack=_pack,
                                    _status=_status,
                                    _width=_width)
        return result
    def _getControlEntryWithLabelWidthBS(self, _parent:tk.Misc, _text:str, _commandValidate=None, 
                            _commandExecute=None, _textVariable:tk.Variable | None=None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=True, fill=tk.X), 
                            _addSeparator:bool=False,
                            _status:bool=True,
                            _width:int | None = None)->tb.Entry:
        if not _width:
            _width = self.cs.ENTRY_WIDTH_DEFAULT
        result:tb.Entry = self._getControlEntryWithLabelBS(_parent, _text, 
                                    _commandValidate=_commandValidate, 
                                    _commandExecute=_commandExecute, 
                                    _textVariable=_textVariable, 
                                    _pack=_pack,
                                    _addSeparator=_addSeparator,
                                    _status=_status,
                                    _width=_width)
        return result
    def _getControlComboBoxBS(self, _parent:tk.Misc, _values:list | None=None, 
                            _defaultValue=None, _command=None, 
                            _textVariable:tk.StringVar | None = None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.X))->tb.Combobox:
        result: tb.Combobox = tb.Combobox(
            _parent,
            state="readonly",
            style=HelperCustomStyleName.COMBOBOX_STYLE_NAME.label
        )
        if not _values is None: 
            result.config(values=_values)
            if not _defaultValue is None: result.set(_defaultValue)

        if not _textVariable is None and isinstance(_textVariable, tk.StringVar): 
            result.configure(textvariable = _textVariable)
            if not _defaultValue: result.set(_textVariable.get())

        try:
            popdown_listbox = (result.tk.eval(f"ttk::combobox::PopdownWindow {result}") + ".f.l")
            tcl_args = []
            for opt, val in self.cs.ComboboxPopdownSettings.items():
                tcl_args.extend([opt, val])

            result.tk.call(popdown_listbox, "configure", *tcl_args)
        except tk.TclError:
            pass

        self.__packagingWidget(result, _pack)

        if _command is not None:
            if isinstance(_command, (list, tuple)):
                def _dispatch_all(e, funcs=_command):
                    for f in funcs:
                        if callable(f):
                            try:
                                f(e)
                            except TypeError:
                                f()

                result.bind("<<ComboboxSelected>>", _dispatch_all)

            elif callable(_command):
                def _dispatch_single(e, func=_command):
                    try:
                        func(e)
                    except TypeError:
                        func()

                result.bind("<<ComboboxSelected>>", _dispatch_single)

        return result
    def _getControlComboBoxWithLabelBS(self, _parent:tk.Misc, _text:str, _values:list | None=None, 
                        _defaultValue=None, _command=None, 
                        _textVariable:tk.StringVar | None = None, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.X), 
                        _addSeparator:bool=False)->tb.Combobox:
        _frame:tb.Frame = self.__getFrameWithLabelBS(_parent, _text, _addSeparator, _pack)[0]
        if not _pack is None: 
            _pack.configure(side=tk.LEFT)
        result:tb.Combobox = self._getControlComboBoxBS(_frame, _values=_values, 
                                _defaultValue=_defaultValue, _command=_command, 
                                _textVariable=_textVariable, _pack=_pack)

        return result
    def _getControlSeparatorBS(self, _parent:tk.Misc, _orient:str=tk.VERTICAL, _pad:int=0)->tb.Separator:
        result: tb.Separator = tb.Separator(_parent, orient=_orient, 
                                style=HelperCustomStyleName.SEPARATOR_STYLE_NAME.label)
        if _pad < 0: _pad=0
        match (_orient):
            case tk.HORIZONTAL: result.pack(side=tk.TOP, fill=tk.X, expand=False, padx=0, pady=_pad)
            case tk.VERTICAL: result.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=_pad, pady=0)

        return result
    def _getControlSpinboxBS(self, _parent:tk.Misc, _text:str, _from:float, _to:float, _interval:float, 
                            _textVariable:tk.Variable, _defaultValue:float=0, 
                            _command=None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.BOTTOM, fill=tk.X, expand=True, width=8), 
                            _addSeparator:bool=False)->tb.Spinbox:
        _format = "%.2f"
        _frame:tb.Frame = self.__getFrameWithLabelBS(_parent, _text, _addSeparator, _pack)[0]
        result: tb.Spinbox = tb.Spinbox(
                    _frame,
                    from_=_from,
                    to=_to,
                    increment=_interval,
                    format=_format,
                    textvariable=_textVariable,
                )
        def __formatDecimalsPlaceAndCommand(event=None):
            try:
                val = float(result.get())
                val = max(_from, min(_to, val))
                result.set(f"{val:.2f}")
            except ValueError:
                result.set(f"{_defaultValue:.2f}")

            if event and _command is not None:
                _command()

        result.bind("<Return>", __formatDecimalsPlaceAndCommand)
        result.bind("<FocusOut>", __formatDecimalsPlaceAndCommand)

        if not _command is None:
            result['command'] =_command

        self.__packagingWidget(result, _pack)
        if not _defaultValue is None: result.set(f"{_defaultValue:.2f}")
        return result
    def _getControlTreeviewBS(self, _parent:tk.Misc, _setting:list[ItemStructTreeview], 
                    _pack:HelperItemLayout=HelperItemLayout(tk.LEFT, tk.BOTH, True)) -> tb.Treeview:
        #if not _setting : raise ValueError("Setting list is null...")  
        _columnsGrid = [s.key for s in _setting] if _setting else []
        result: tb.Treeview = tb.Treeview(
            _parent,
            #columns=_columnsGrid,
            show="headings",
            selectmode="browse",
            style=HelperCustomStyleName.TREEVIEW_STYLE_NAME.label
        )
        self._setControlTreeviewLayoutBS(result, _setting)
        '''
        for c in _setting:
            col_key: str = c.key
            def _sort_cmd(key: str = col_key) -> None:
                self.__sortedColumnsTreeview(result, key, False)

            result.heading(c.key, text=c.text, command=_sort_cmd)
            result.column(c.key, width=c.width, anchor=c.anchor, 
                          minwidth=(c.minWidth if c.minWidth > 0 else 0),
                          stretch=c.stretch)
        '''

        _scroll = self._getControlScrollbarBS(result, _parent)
        self.__packagingWidget(result, _pack)
        _scroll.pack(side=tk.RIGHT, fill=tk.Y)

        return result
    def _setControlTreeviewLayoutBS(self, result:tb.Treeview, _setting:list[ItemStructTreeview]):
            #if not _setting : raise ValueError("Setting list is null...")  
            _columnsGrid = [s.key for s in _setting] if _setting else []
            result.configure(columns= _columnsGrid)
            for c in _setting:
                col_key: str = c.key
                def _sort_cmd(key: str = col_key) -> None:
                    self.__sortedColumnsTreeview(result, key, False)
    
                result.heading(c.key, text=c.text, command=_sort_cmd)
                result.column(c.key, width=c.width, anchor=c.anchor, 
                              minwidth=(c.minWidth if c.minWidth > 0 else 0),
                              stretch=c.stretch)
    
            return result
    def _getControlCheckboxBS(self, _parent: tk.Misc, _text: str, _variable: tk.BooleanVar, 
                            _command:Callable[[], Any] | None = None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.NONE, expand=False),
                            _tooltip:str | None=None)->tb.Checkbutton:
        result:tb.Checkbutton = tb.Checkbutton(
            _parent,
            text=_text,
            variable=_variable,
            style=HelperCustomStyleName.CHECKBOX_STYLE_NAME.label
        )
        if _command: result.configure(command=_command)
        self.__packagingWidget(result, _pack)
        if _tooltip:
            ToolTip(result, _tooltip, self.settingApp.MakeFont(size=1.2, italic=True))
        return result
    def _getControlNotebookBS(self, _parent:tk.Misc)->tb.Notebook: 
        result:tb.Notebook = tb.Notebook(_parent, style=HelperCustomStyleName.NOTEBOOK_STYLE_NAME.label)
        result.pack(fill=tk.BOTH, expand=True)

        return result
    def _getControlRadioButtomBS(self, _parent:tk.Misc, _text:str, _value, _variable:tk.Variable, 
                            _command:Callable[[], Any] | None = None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.NONE, expand=False))->tb.Radiobutton:
        result = tb.Radiobutton(
            _parent,
            text=_text,
            value=_value,
            variable=_variable,
            style=HelperCustomStyleName.RADIOBUTTON_STYLE_NAME.label
        )
        if _command: result.configure(command=_command)
        self.__packagingWidget(result, _pack)
        return result
    def _getControlScrollbarBS(self, _control:TBScrollableControl, 
                    _parent:tk.Misc | None=None, _orientation:ScrollOrientation=tk.VERTICAL) -> tb.Scrollbar:
        if not isinstance(_control, tk.Misc):
            raise TypeError(f"Control don't support, contol type {type(_control).__name__}")

        if _orientation == tk.VERTICAL and not hasattr(_control, "yview"):
            raise AttributeError( f"The widget '{type(_control).__name__}' don't support vertical scrollbar ('yview' not found)" )
        elif _orientation == tk.HORIZONTAL and not hasattr(_control, "xview"):
            raise AttributeError( f"The widget '{type(_control).__name__}' don't support horizontal scrollbar ('xview' not found)" )

        _parentEnd:tk.Misc = _parent if _parent is not None else _control.master
        result = tb.Scrollbar(_parentEnd, orient=_orientation, bootstyle="round")

        if _orientation == tk.VERTICAL:
            result.config(command=getattr(_control, "yview"))
            _control['yscrollcommand']=result.set
        else:
            result.config(command=getattr(_control, "xview"))
            _control['xscrollcommand']=result.set

        return result
    def _getControlTextBS(self, _parent:tk.Misc, _state:bool=True, 
                            _pack:HelperItemLayout=HelperItemLayout(tk.LEFT, tk.BOTH, True)) -> tb.ScrolledText:
        result = tb.ScrolledText(
                _parent,
                bootstyle="primary-round",
                bg="#153248",
                fg="#ffffff",
                insertbackground="#5bc0de",
                selectbackground="#375a7f",
                font=self.settingApp.MakeFont(1.3, italic=True),
                height=10,
                wrap=tk.WORD,
                state=tk.NORMAL if _state else tk.DISABLED
            )
        self.__packagingWidget(result, _pack)
        return result
    def _getControlProgressBarBS(self, _parent:tk.Misc, _text:str | None = None, 
                            _mode:str | None = 'determinate', 
                            _maximum:float=100.0,
                            _variable:tk.DoubleVar | None = None,
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.TOP, fill=tk.X, expand=True))->tb.Progressbar:
            if not _mode or len(_mode) <= 0: 
                _mode = 'determinate'
            if _maximum <= 0: 
                _maximum=100.0
            if not _variable: 
                _variable = tk.DoubleVar(value=0.0)
            _text = (_text if _text else '')
            _packWidth:HelperItemLayout = _pack.clone()
            _pack.configure(width = None)
            
            _frame:tb.Frame 
            _label:tb.Label | None
            _frame, _label = self.__getFrameWithLabelBS(_parent, _text, False, _packWidth, _forceLabel=True)
            result: tb.Progressbar = tb.Progressbar(
                _frame,
                mode=_mode,
                maximum=_maximum,
                style=HelperCustomStyleName.PROGRESS_BAR_STYLE_NAME.label
            )
            if _variable: 
                result.configure(variable=_variable)
            self.__packagingWidget(result, _pack.configure(anchor=tk.W))
            try:
                if _variable:
                    self.__onProgressBarRelease(_label=_label, _text=_text, _value=_variable)
                    _variable.trace_add(
                                "write",
                                lambda *args: self.__onProgressBarRelease(_label=_label, _text=_text, _value=_variable)
                            )
            except:
                pass
            return result
    def _getControlCheckboxList(self, _parent:tk.Misc, _text:str | None = None, data:list[tuple[str, bool]] = [], 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.BOTH, expand=False))->'ScrolledCheckboxList':
        result:ScrolledCheckboxList = ScrolledCheckboxList(_parent, _text, data)
        self.__packagingWidget(result, _pack)
        return result
    def _getControlProgressList(self, _parent:tk.Misc, _text:str | None = None, data:list[str] = [], 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.BOTH, expand=False))->'ScrolledProgressList':
        result:ScrolledProgressList = ScrolledProgressList(_parent, _text, data)
        self.__packagingWidget(result, _pack)
        return result
    #endregion
    
    #region Helper
    def __packagingWidget(self, _control:tk.Widget, _pack:HelperItemLayout)->tk.Widget:
        if not _control or not _pack : return _control
        match(_pack.geometryType):
            case GeometryType.Pack | GeometryType.Undefined:
                if _pack.isSide: _control.pack(side=_pack.sideValue)
                if _pack.isFill: _control.pack(fill=_pack.fillValue)
                if _pack.isAnchor: _control.pack(anchor=_pack.anchorValue)
                if _pack.expand and not _pack.isWidth: _control.pack(expand=_pack.expand)
                elif _pack.isWidth: _control["width"] = _pack.width
                _control.pack(padx=_pack.padx, pady=_pack.pady)
            case GeometryType.Grid:
                _control.grid(padx=_pack.padx, pady=_pack.pady)
                _control.grid(row=_pack.row, column=_pack.column)
                if _pack.isSticky: _control.grid(sticky=_pack.sticky)

        return _control
    
    def __getFrameWithLabelBS(self, _parent:tk.Misc, _text:str | None=None, _addSeparator:bool=False, 
                            _pack:HelperItemLayout |None=None, _forceLabel:bool=False)->tuple[tb.Frame, Optional[tb.Label]]:        
        _hasText:bool = (not _text is None and len(_text) > 0) 
        _frame:tb.Frame = tb.Frame(_parent) if not _hasText else tb.Frame(_parent)
        _label:tb.Label | None=None
        if not _pack is None: 
            if _pack.isSide: _frame.pack(side=_pack.sideValue)
            if _pack.expand: _frame.pack(expand=_pack.expand)
            if _pack.isFill: _frame.pack(fill=_pack.fillValue)
            if _addSeparator: 
                _frame.pack(padx=(0, 2), pady=(2, 0))                    
                self._getControlSeparatorBS(_frame)
            else: _frame.pack(padx=(0, 2), pady=2)

        if _hasText or _forceLabel:
            _textEnd = _text if _hasText else ''
            _label = tb.Label(_frame, text=f"{_textEnd}{(":" if _hasText else "")}", anchor=tk.W, 
                              style=HelperCustomStyleName.SCALE_LABEL_STYLE_NAME.label)
            _label.pack(side=tk.LEFT, padx=(0, 2))
            if _forceLabel and not _pack is None and _pack.width:
                _label.configure(width=_pack.width)
                _label.pack_propagate(False)
        return (_frame , _label)
    
    def GetFrameWithSeperator(self, _parent:tk.Misc, _pack:HelperItemLayout | None = None, _pad:int=0)->tb.Frame:
        _frame:tb.Frame = tb.Frame(_parent)
        _frame.pack(padx=(0, 2), pady=(1, 0))        
        if not _pack is None: 
            if _pack.isSide: _frame.pack(side=_pack.sideValue)
            if _pack.expand: _frame.pack(expand=_pack.expand)
            if _pack.isFill: _frame.pack(fill=_pack.fillValue)
        self._getControlSeparatorBS(_frame, _pad=_pad)
        return _frame
    
    #endregion

    #region Delegates
    def __sortedColumnsTreeview(self, treeview, col, reverse):
        dataList = [(treeview.set(child, col), child) for child in treeview.get_children('')]
        try:
            dataList.sort(key=lambda x: float(x[0]), reverse=reverse)
        except ValueError:
            dataList.sort(key=lambda x: x[0], reverse=reverse)

        for index, (_val, child) in enumerate(dataList):
            treeview.move(child, '', index)

        treeview.heading(col, command=lambda: self.__sortedColumnsTreeview(treeview, col, not reverse)) 
    def __onScaleMouseRelease(self, _label:tb.Label | None, _text:str, _value:tk.Variable, _step:float | int=1):
        if _label is None: return
        _hasText = _text is not None and len(_text) > 0
        _textEnd = f"{_text if _hasText else ''}{' => ' if _hasText else ''}"  
        _label.configure(text=f"{_textEnd}({_value.get():.0f}) ")

    def __onProgressBarRelease(self, _label:tb.Label | None, _text:str, _value:tk.DoubleVar):
            if _label is None: return
            _hasText = _text is not None and len(_text) > 0
            _textEnd = f"{_text if _hasText else ''}{' => ' if _hasText else ''}"  
            _label.configure(text=f"{_textEnd}({_value.get():.2f}%) ")
    '''
    def __applyScaleStep(self, _variable: tk.Variable, _step: float):
        if _variable is None: return
        _current = float(_variable.get())
        _ending = round(_current / _step) * _step
        if abs(_current - _ending) > 1e-5: _variable.set(_ending)
    '''
    #endregion

    #endregion

#endregion

#region HelperControl
class HelperControl:
    def __init__(self, _settingApp: Setting, 
                _style:tb.Style,
                _styleType: ControlStyleType=ControlStyleType.NORMAL):
        self.settingApp: Setting = _settingApp
        self.styleType: ControlStyleType = _styleType
        self.cs:HelperCustomStyle = HelperCustomStyle(_settingApp, _style)
        self.il:HelperItemLayoutControls = HelperItemLayoutControls()
        self.ct:HelperControlTKinter = HelperControlTKinter(_settingApp, _style)
    
    #region Properties:
    @property
    def __COMBOBOX_WIDTH_DEFAULT(self)->int: 
        if not hasattr(self, 'cs'): return 0
        return self.cs.COMBOBOX_WIDTH_DEFAULT
    @property
    def __SPINBOX_WIDTH_DEFAULT(self)->int: 
        if not hasattr(self, 'cs'): return 0
        return self.cs.SPINBOX_WIDTH_DEFAULT
    #endregion

    #region Methods

    #region LabelFrame:
    def ControlLabelFrame(self, _parent:tk.Misc, _text:str, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, 
                        expand=True, fill=tk.BOTH, padx=(0,0), pady=(0,0)))->tb.LabelFrame:
        return self.ct._getControlLabelFrameBS(_parent, _text, _pack)
    def ControlLabelFrameLEFT(self, _parent:tk.Misc, _text:str, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=True, 
                                fill=tk.BOTH, padx=(0,0), pady=(0,0)))->tb.LabelFrame:
        _pack.configure(side=tk.LEFT, padx=(0, 1))
        return self.ControlLabelFrame(_parent, _text, _pack)
    def ControlLabelFrameRIGHT(self, _parent:tk.Misc, _text:str, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.RIGHT, expand=True, 
                            fill=tk.BOTH, padx=(0,0), pady=(0,0)))->tb.LabelFrame:
        _pack.configure(side=tk.RIGHT, padx=(1, 0))
        return self.ControlLabelFrame(_parent, _text, _pack)
    def ControlLabelFrameForRow(self, _parent:tk.Misc, _text:str, 
                _pack:HelperItemLayout=HelperItemLayout(side=tk.TOP, 
                        expand=False, fill=tk.X, padx=(0, 0), pady=(0, 0)))->tb.LabelFrame:
        _pack.configure(side=tk.TOP)
        return self.ControlLabelFrame(_parent, _text, _pack)
    def ControlLabelFrameForRowEnd(self, _parent:tk.Misc, _text:str, 
                _pack:HelperItemLayout=HelperItemLayout(side=tk.TOP, 
                        expand=True, fill=tk.BOTH, padx=(0, 0), pady=(0, 0)))->tb.LabelFrame:
        _pack.configure(side=tk.TOP, fill=tk.BOTH, expand=True)
        return self.ControlLabelFrame(_parent, _text, _pack)
    #endregion
    
    #region Frame:
    def ControlFrame(self, _parent:tk.Misc, 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.BOTH))->tb.Frame:
        return self.ct._getControlFrameBS(_parent, _pack)
    def ControlFrameForRow(self, _parent:tk.Misc, _expand:bool=False)->tb.Frame:
        _pack:HelperItemLayout=HelperItemLayout(side=tk.TOP, expand=_expand, fill=tk.X, padx=(0, 0), pady=(0, 0))
        return self.ControlFrame(_parent, _pack)
    def ControlFrameForRowEnd(self, _parent:tk.Misc, 
                _pack:HelperItemLayout=HelperItemLayout(side=tk.TOP, 
                        expand=True, fill=tk.BOTH, padx=(0, 0), pady=(0, 0)))->tb.Frame:
        _pack.configure(side=tk.TOP)
        return self.ControlFrame(_parent, _pack)
    def ControlFrameForColumn(self, _parent:tk.Misc, 
                _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, 
                        expand=True, fill=tk.BOTH, padx=(0, 0), pady=(0, 0)))->tb.Frame:
        _pack.configure(side=tk.LEFT)
        return self.ControlFrame(_parent, _pack)    
    def ControlFrameForColumnEnd(self, _parent:tk.Misc, 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.RIGHT, 
                        expand=False, fill=tk.BOTH, padx=(0, 0), pady=(0, 0)))->tb.Frame:
        _pack.configure(side=tk.LEFT)
        return self.ControlFrame(_parent, _pack)
    def ControlFrameLeftPanel(self, _parent:tk.Misc, _width:int=450)->tb.Frame:
        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, 
                                expand=False, fill=tk.Y, width=_width, padx=10, pady=5)
        result:tb.Frame = self.ct._getControlFrameBS(_parent, _pack)
        if result is not None: result.pack_propagate(False)
        return result
    def ControlFrameRightPanel(self, _parent:tk.Misc)->tb.Frame:
        _pack:HelperItemLayout=HelperItemLayout(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=5)
        return self.ct._getControlFrameBS(_parent, _pack)
    #endregion
    
    #region Scale:
    def ControlScale(self, _parent:tk.Misc, _text:str | None, _from:float, _to:float, 
                    _interval:float, _variable:tk.Variable, _command=None, 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.TOP, fill=tk.X, expand=True))->tb.Scale:
        return self.ct._getControlScaleBS(_parent, (_text if _text else ''), _from, _to, _interval, _variable, _command, _pack)
    def ControlScaleLEFT(self, _parent:tk.Misc, _text:str | None, _from:float, _to:float, _interval:float, 
                         _variable:tk.Variable, _command=None)->tb.Scale:
        _pack:HelperItemLayout = self.il._getHelperItemLayoutScale(side=tk.LEFT)
        return self.ControlScale(_parent, _text, _from, _to, _interval, _variable, _command, _pack)
    #endregion
    
    #region Button:
    def ControlButton(self, _parent:tk.Misc, _text:str, 
                        _command:Callable[..., Any], 
                        _state:bool=True, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.NONE, expand=True, fill=tk.X), 
                        _addSeparator:bool=False)->tb.Button:
        return self.ct._getControlButtonBS(_parent, _text, _command, _state, _pack, _addSeparator)
    def ControlButtonLEFT(self, _parent:tk.Misc, _text:str, 
                        _command:Callable[..., Any], 
                        _state:bool=True, 
                        _pack:HelperItemLayout | None=None, _addSeparator:bool=False)->tb.Button:
        if _pack is None: _pack = self.il._getHelperItemLayoutButton(side=tk.LEFT)
        return self.ControlButton(_parent, _text, _command, _state, _pack, _addSeparator)
    def ControlButtonRIGHT(self, _parent:tk.Misc, _text:str, 
                        _command:Callable[..., Any], 
                        _state:bool=True, 
                        _pack:HelperItemLayout | None =None, _addSeparator:bool=False)->tb.Button:
        if _pack is None: _pack = self.il._getHelperItemLayoutButton(side=tk.RIGHT, expand=False)
        return self.ControlButton(_parent, _text, _command, _state, _pack, _addSeparator)
    #endregion
    
    #region Label:
    def ControlLabel(self, _parent:tk.Misc, _text:str, _type:TKLabelType=TKLabelType.NORMAL, 
                    _variable:tk.StringVar | None = None,
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.NONE, anchor=tk.W, pady=(0, 1)))->tb.Label:
            return self.ct._getControlLabelBS(_parent, _text, _type, _variable, _pack)
    def ControlLabelLEFT(self, _parent:tk.Misc, _text:str, _type:TKLabelType=TKLabelType.NORMAL,
                        _variable:tk.StringVar | None = None)->tb.Label:
        _pack = self.il._getHelperItemLayoutLabel(side=tk.LEFT)
        return self.ControlLabel(_parent, _text, _type, _variable, _pack)
    def ControlLabelRIGHT(self, _parent:tk.Misc, _text:str, _type:TKLabelType=TKLabelType.NORMAL,
                        _variable:tk.StringVar | None = None)->tb.Label:
        _pack = self.il._getHelperItemLayoutLabel(side=tk.RIGHT)
        return self.ControlLabel(_parent, _text, _type, _variable, _pack)
    def ControlLabelInfo(self, _parent:tk.Misc, _text:str, _variable:tk.StringVar | None = None)->tb.Label:
        _pack = self.il._getHelperItemLayoutLabel(side=tk.TOP)
        return self.ControlLabel(_parent, _text, TKLabelType.INFORMATION, _variable, _pack)
    def ControlLabelInfoLEFT(self, _parent:tk.Misc, _text:str, _variable:tk.StringVar | None = None)->tb.Label:
        _pack = self.il._getHelperItemLayoutLabel(side=tk.LEFT)
        return self.ControlLabel(_parent, _text, TKLabelType.INFORMATION, _variable, _pack)
    def ControlLabelInfoRIGHT(self, _parent:tk.Misc, _text:str, _variable:tk.StringVar | None = None)->tb.Label:
        _pack = self.il._getHelperItemLayoutLabel(side=tk.RIGHT)
        return self.ControlLabel(_parent, _text, TKLabelType.INFORMATION, _variable, _pack)
    def ControlLabelSummary(self, _parent:tk.Misc, _text:str, _variable:tk.StringVar | None = None)->tb.Label:
        _pack = self.il._getHelperItemLayoutLabel(side=tk.TOP).configure(pady=(2, 2))
        return self.ControlLabel(_parent, _text, TKLabelType.SUMMARY, _variable, _pack)
    def ControlLabelCountRIGHT(self, _parent:tk.Misc, _text:str, 
                            _variable:tk.StringVar | None = None,
                            _addSeparator:bool=False)->tb.Label:        
        _pack = self.il._getHelperItemLayoutLabel(side=tk.RIGHT)
        _frame:tk.Misc = _parent if not _addSeparator else self.ct.GetFrameWithSeperator(_parent, _pack, 5)
        return self.ControlLabel(_frame, _text, TKLabelType.COUNT, _variable, _pack)
    def ControlLabelCountLEFT(self, _parent:tk.Misc, _text:str, _variable:tk.StringVar | None = None)->tb.Label:
        _pack = self.il._getHelperItemLayoutLabel(side=tk.LEFT)
        return self.ControlLabel(_parent, _text, TKLabelType.COUNT, _variable, _pack)
    #endregion
    
    #region LabelLink
    def ControlLabelLink(self, _parent:tk.Misc, _text:str, _command, 
                    _pack:HelperItemLayout=HelperItemLayout(anchor=tk.E, side=tk.NONE))->tb.Label:
        return self.ct._getControlLabelLinkBS(_parent, _text, _command, _pack)
    #endregion
    
    #region Entry:
    def ControlEntry(self, _parent:tk.Misc, _commandValidate=None, _commandExecute=None, _textVariable=None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.RIGHT, expand=True, fill=tk.X),
                            _status:bool=True, 
                            _width:int | None = None)->tb.Entry:
        return self.ct._getControlEntryBS(_parent, _commandValidate, _commandExecute, _textVariable, _pack, _status)
    def ControlEntryWithLabel(self, _parent:tk.Misc, _text:str, _commandValidate=None, 
                        _commandExecute=None, _textVariable:tk.Variable | None=None, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.X), 
                        _addSeparator:bool=False,
                        _status:bool=True,
                        _width:int | None = None)->tb.Entry:
        return self.ct._getControlEntryWithLabelBS(_parent, _text, _commandValidate, _commandExecute, 
                            _textVariable, _pack, _addSeparator, _status, _width)
    def ControlEntryWithLabelWidth(self, _parent:tk.Misc, _text:str, _commandValidate=None, 
                        _commandExecute=None, _textVariable:tk.Variable | None=None, 
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.X), 
                        _addSeparator:bool=False,
                        _status:bool=True,
                        _width:int | None = None)->tb.Entry:
        return self.ct._getControlEntryWithLabelWidthBS(_parent, _text, _commandValidate, _commandExecute, 
                            _textVariable, _pack, _addSeparator, _status, _width)
    #endregion
    
    #region ComboBox:
    def ControlComboBox(self, _parent:tk.Misc, _values:list | None=None, 
                        _defaultValue=None, _command=None, 
                        _textVariable:tk.StringVar | None = None,
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=True, fill=tk.X))->tb.Combobox:
        return self.ct._getControlComboBoxBS(_parent, _values, _defaultValue, 
                                                _command, _textVariable, _pack)
    def ControlComboBoxWithLabel(self, _parent:tk.Misc, _text:str, 
                        _values:list | None=None, _defaultValue=None, _command=None, 
                        _textVariable:tk.StringVar | None = None,
                        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=False, fill=tk.X), 
                        _addSeparator:bool=False)->tb.Combobox:
        
        return self.ct._getControlComboBoxWithLabelBS(_parent, _text, _values, _defaultValue, 
                                            _command, _textVariable, _pack, _addSeparator)
    def ControlComboBoxWithLabelWidth(self, _parent:tk.Misc, _text:str, _values:list | None=None, 
                                    _defaultValue=None, _command=None, 
                                    _textVariable:tk.StringVar | None = None, _addSeparator:bool=False, 
                                    _width:int | None=None,
                                    _expand:bool=False)->tb.Combobox:
        if _width is None or _width <= 0: _width = self.__COMBOBOX_WIDTH_DEFAULT
        if _expand: _width=None
        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, expand=_expand, fill=tk.X, width=_width)
        return self.ControlComboBoxWithLabel(_parent, _text, _values, _defaultValue, 
                                             _command, _textVariable, _pack, _addSeparator)
    #endregion
    
    #region Separator
    def ControlSeparator(self, _parent:tk.Misc, _orient:str=tk.VERTICAL, _pad:int=0)->tb.Separator:
        return self.ct._getControlSeparatorBS(_parent, _orient, _pad)
    #endregion
    
    #region SpinBox:
    def ControlSpinbox(self, _parent:tk.Misc, _text:str, _from:float, _to:float, _interval:float, 
                    _textVariable:tk.Variable, _defaultValue:float=0, _command=None, 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.BOTTOM, fill=tk.X, expand=False, width=8), 
                    _addSeparator:bool=False)->tb.Spinbox:
        '''
        match(self.styleType):
            case ControlStyleType.NORMAL: return self.ct._getControlSpinbox(_parent, _text, _from, _to, _interval, _textVariable, _defaultValue, _command, _pack, _addSeparator)
            case ControlStyleType.THEME: return self.ct._getControlSpinboxBS(_parent, _text, _from, _to, _interval, _textVariable, _defaultValue, _command, _pack, _addSeparator)
        return None
        '''
        return self.ct._getControlSpinboxBS(_parent, _text, _from, _to, _interval, 
                                            _textVariable, _defaultValue, _command, _pack, _addSeparator)
    def ControlSpinboxWidth(self, _parent:tk.Misc, _text:str, _from:float, _to:float, _interval:float, 
                            _textVariable:tk.Variable, _defaultValue:float=0, 
                            _command=None, _addSeparator:bool=False, _width:int | None=None)->tb.Spinbox:
        if _width is None or _width <= 0: _width = self.__SPINBOX_WIDTH_DEFAULT
        _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.X, expand=False, width=_width)
        return self.ControlSpinbox(_parent, _text, _from, _to, _interval, 
                                                _textVariable, _defaultValue, _command, _pack, _addSeparator)
    def ControlSpinboxWidthLEFT(self, _parent:tk.Misc, _text:str, _from:float, _to:float, _interval:float, 
                                _textVariable:tk.Variable, _defaultValue:float=0, 
                                _command=None, _addSeparator:bool=False, _width:int | None=None)->tb.Spinbox:
        result = self.ControlSpinboxWidth(_parent, _text, _from, _to, _interval, _textVariable, _defaultValue, _command, _addSeparator, _width)
        result.pack(side=tk.LEFT)
        return result
    def ControlSpinboxWidthRIGHT(self, _parent:tk.Misc, _text:str, _from:float, _to:float, _interval:float, 
                            _textVariable:tk.Variable, _defaultValue:float=0, 
                            _command=None, _addSeparator:bool=False, _width:int | None=None)->tb.Spinbox:
        result = self.ControlSpinboxWidth(_parent, _text, _from, _to, _interval, _textVariable, _defaultValue, _command, _addSeparator, _width)
        result.pack(side=tk.RIGHT)
        return result
    #endregion
    
    #region Treeview:
    def ControlTreeview(self, _parent:tk.Misc, _setting:list[ItemStructTreeview], 
                        _pack:HelperItemLayout=HelperItemLayout(tk.LEFT, tk.BOTH, True))->tb.Treeview:
        return self.ct._getControlTreeviewBS(_parent, _setting, _pack)
    def ControlTreeviewClear(self, _parent:tk.Misc)->tb.Treeview:
        _setting:list[ItemStructTreeview] = []
        _pack:HelperItemLayout=HelperItemLayout(tk.LEFT, tk.BOTH, True)
        return self.ct._getControlTreeviewBS(_parent, _setting, _pack)
    def ControlTreeviewSetLayout(self, result:tb.Treeview, df:pd.DataFrame)->tb.Treeview:
        _setting:list[ItemStructTreeview] = self.__GetStructTreeview(df)
        return self.ct._setControlTreeviewLayoutBS(result, _setting)
    #endregion

    #region CheckBox:
    def ControlCheckbox(self, _parent: tk.Misc, _text: str, _variable: tk.BooleanVar, _command=None, 
                            _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.NONE, expand=False),
                            _tooltip:str | None=None)->tb.Checkbutton:
        return self.ct._getControlCheckboxBS(_parent, _text, _variable, _command, _pack, _tooltip)
    #endregion
    
    #region RadioButton:
    def ControlRadioButton(self, _parent: tk.Misc, _text: str, _value, _variable: tk.Variable, _command=None, 
                    _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.NONE, expand=False))->tb.Radiobutton:
        return self.ct._getControlRadioButtomBS(_parent, _text, _value, _variable, _command, _pack)
    #endregion

    #region Notebook:
    def ControlNotebook(self, _parent:tk.Misc)->tb.Notebook:
        return self.ct._getControlNotebookBS(_parent)
    #endregion

    #region Scrollbar:
    def ControlScrollbar(self, _parent:tk.Misc, _control:TBScrollableControl, 
                         _orientation:ScrollOrientation=tk.VERTICAL)->tb.Scrollbar | None:
        return self.ct._getControlScrollbarBS(_control, _parent, _orientation)
    #endregion

    #region textBox:
    def ControlText(self, _parent:tk.Misc, _state:bool=True, 
                _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.BOTH, expand=True))->tb.ScrolledText:
        return self.ct._getControlTextBS(_parent, _state, _pack)
    #endregion
    
    #region ProgressBar:
    def ControlProgressBar(self, _parent:tk.Misc, _text:str | None = None, 
                            _mode:str | None = 'determinate', 
                            _maximum:float=100.0,
                            _variable:tk.DoubleVar | None = None,
                            _width:int|None = None)->tb.Progressbar:
        _pack:HelperItemLayout=HelperItemLayout(side=tk.TOP, fill=tk.X, expand=True, width=_width)
        return self.ct._getControlProgressBarBS(_parent, _text, _mode, _maximum, _variable, _pack)
    def ControlProgressBarLEFT(self, _parent:tk.Misc, _text:str | None = None, 
                            _maximum:float=100.0,
                            _variable:tk.DoubleVar | None = None,
                            _width:int|None = None)->tb.Progressbar:
        _mode:str = 'determinate'
        _pack:HelperItemLayout = self.il._getHelperItemLayoutProgressBar(side=tk.LEFT, width=_width)
        return self.ct._getControlProgressBarBS(_parent, _text, _mode, _maximum, _variable, _pack)
    #endregion

    #region CheckboxList:
    def ControlScrolledCheckboxList(self, _parent:tk.Misc, _text:str | None = None, _data:list[tuple[str, bool]] = [], 
                _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.BOTH, expand=True))->'ScrolledCheckboxList':
        return self.ct._getControlCheckboxList(_parent, _text, _data, _pack)
    #endregion

    #region ProgressList:
    def ControlScrolledProgressList(self, _parent:tk.Misc, _text:str | None = None, _data:list[str] = [], 
                _pack:HelperItemLayout=HelperItemLayout(side=tk.LEFT, fill=tk.BOTH, expand=True))->'ScrolledProgressList':
        return self.ct._getControlProgressList(_parent, _text, _data, _pack)
    #endregion

    #endregion

    #region Helper
    def SetHelperStyle(self, _control:ttk.Widget, _background:str='#558833', _addName:str | None = None):
        _className:str = _control.winfo_class()
        if not _className: return
        _style:str | None = self.cs.SetHelperStyle(_className, _background, _addName)
        if not _style: return
        _control['style']=_style

    def GetMeasureString(self, text: str, _control:tk.Widget) -> int:
            if not text or len(text)<=0: return 0
            _font:tkFont.Font = self.__GetStyleFont(_control.winfo_class())

            if not _font: 
                return len(text)
            result:int = _font.measure(text)
            return result

    def GetMeasureStringMax(self, text:list[str], _control:tk.Widget) -> int:
        if not text or len(text)<=0: return 0
        result:int = max([self.GetMeasureString(s, _control) for s in text])
        return result

    def __GetConvertPixelsToCharWidth(self, _font:tkFont.Font, maxPX:int, _paddingChars:int=1) -> int:
        _charZero = _font.measure("0")
        if _charZero <= 0:
            _charZero = 8  
            
        result = math.ceil(maxPX / _charZero)
        _paddingChars = _paddingChars if _paddingChars > 0 else 1
        return result + _paddingChars
    
    def GetMaxCharWidth(self, _control:tk.Widget, data:list[str], _addText:str | None = None, _paddingChars:int=1) -> int:
        if not _control or not data: return 0
        _dataAdd:list[str] = data if not _addText else [s + _addText for s in data] 
        _font:tkFont.Font = self.__GetStyleFont(_control.winfo_class())
        if not _font: return max([len(s) for s in _dataAdd])
        maxPX = max([self.GetMeasureString(s,_control) for s in _dataAdd])
        return self.__GetConvertPixelsToCharWidth(_font, maxPX, _paddingChars)

    def __GetStyleFont(self, styleName: str = "TLabel") -> tkFont.Font:
        resultDefault:tkFont.Font = self.settingApp.MakeFont(1.1, italic=True, bold=True)
        #style = tb.Style.get_instance()
        style = self.cs.style
        if not style: return resultDefault
        
        # Busca la propiedad 'font' del estilo indicado
        font_spec = style.lookup(styleName, "font", default=style.lookup('TLabel', 'font'))

        # Si el estilo no tiene una fuente explícita, hace fallback a la fuente por defecto
        if not font_spec:
            return resultDefault

        # Convertir a objeto tkFont.Font
        if isinstance(font_spec, str):
            try:
                return tkFont.nametofont(font_spec)
            except tk.TclError:
                return tkFont.Font(family=font_spec)
        elif isinstance(font_spec, (tuple, list)):
            return tkFont.Font(font=font_spec)
        elif isinstance(font_spec, tkFont.Font):
            return font_spec
        else:
            return resultDefault

    def GetStyleByName(self, styleName: HelperCustomStyleName) -> dict:
        result = self.cs.style.configure(styleName.label)
        return result
        
    def __GetStructTreeview(self, df:pd.DataFrame)->list[ItemStructTreeview]:
        result:list[ItemStructTreeview] = []
        if df.empty:
            return result

        headers = list(df.columns)
        for col in headers:
            col_width = max(len(str(col)) * 12, 100)
            item:ItemStructTreeview = ItemStructTreeview(f"_{col}", col, col_width, tk.W)
            result.append(item)

        return result
    #endregion
#endregion

#region CustomControls
class ScrolledCheckboxList(tb.Labelframe):
    def __init__(
            self,
            parent: tk.Misc,
            _text:str | None = None,
            items: list[tuple[str, bool]] | None = None,
            bootstyle: str = "primary-round-toggle"):
        super().__init__(parent)

        _setting:Setting = Setting()
        _style:tb.Style = HelperStyle.GetStyle(parent)
        _hc = HelperControlTKinter(_setting, _style)
        _cs = HelperCustomStyle(_setting, _style)

        self['style'] = HelperCustomStyleName.FRAME_LABEL_STYLE_NAME.label
        self.bootstyle = bootstyle
        self.vars: dict[str, tk.BooleanVar] = {}
        self._setSelectAll:tk.BooleanVar = tk.BooleanVar(value=True)
        self._isUpdatingAll: bool = False

        _hasText:bool = bool(_text)
        if _hasText: self.configure(text=_text)

        _frmRowSelectAll:tb.Frame = _hc._getControlFrameBS(self, _pack=HelperItemLayout(side=tk.TOP, 
                                expand=False, fill=tk.X, padx=(0, 0), pady=(0, 0)))
        
        self._chkSelectAll = tb.Checkbutton(
            _frmRowSelectAll,
            text='Select all',
            variable=self._setSelectAll,
            bootstyle=self.bootstyle,
            command=lambda: self.SelectAll(self._setSelectAll.get())
        )
        self._chkSelectAll.pack(anchor=tk.E, pady=(5, 0), padx=(0, 10), side=tk.RIGHT)

        self.scroll_frame = tb.ScrolledFrame(self, autohide=True)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)

        if items and len(items) > 0:
            self.SetItems(items)

    '''
    def SetItems(self, items:list[str], _state:bool=True)->None:
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.vars.clear()

        has_items = bool(items)
        self._chkSelectAll.configure(state=(tk.NORMAL if has_items else tk.DISABLED))

        for item in items:
            var = tk.BooleanVar(value=_state)
            var.trace_add('write', lambda *args: self.__UpdateSelectAllState())
            self.vars[item] = var

            chk = tb.Checkbutton(
                self.scroll_frame,
                text=item,
                variable=var,
                bootstyle=self.bootstyle,
            )
            chk.pack(anchor=tk.W, pady=(0, 1), padx=(1, 0))

        self._setSelectAll.set(_state if has_items else False)
    '''

    def SetItems(self, items:list[tuple[str, bool]])->None:
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.vars.clear()

        has_items = bool(items)
        self._chkSelectAll.configure(state=(tk.NORMAL if has_items else tk.DISABLED))

        for item, _value in items:
            var = tk.BooleanVar(value=_value)
            var.trace_add('write', lambda *args: self.__UpdateSelectAllState())
            self.vars[item] = var

            chk = tb.Checkbutton(
                self.scroll_frame,
                text=item,
                variable=var,
                bootstyle=self.bootstyle,
            )
            chk.pack(anchor=tk.W, pady=(0, 1), padx=(1, 0))

        _state:bool = all(s for _, s in items)
        self._setSelectAll.set(_state if has_items else False)

    def __UpdateSelectAllState(self) -> None:
        if self._isUpdatingAll or not self.vars: return
        allChecked:bool = all(var.get() for var in self.vars.values())
        self._setSelectAll.set(allChecked)

    def GetCheckedItems(self)->list[str]:
        return [item for item, var in self.vars.items() if var.get()]

    def SelectAll(self, state:bool=True)->None:
        for var in self.vars.values():
            var.set(state)

class ScrolledProgressList(tb.Labelframe):
    DEFAULT_TEXT_SUFIX_PROGRESS:Final[str] = ' => (100.00%)'
    def __init__(
            self,
            parent: tk.Misc,
            _text: str | None = None,
            items: list[str] | None = None,
            bootstyle: str = "primary-animated-striped"):
        super().__init__(parent)

        _setting:Setting=Setting()
        _style:tb.Style = HelperStyle.GetStyle(parent)
        self._hc = HelperControl(_setting, _style)
        self._cs = HelperCustomStyle(_setting, _style)

        self['style'] = HelperCustomStyleName.FRAME_LABEL_STYLE_NAME.label
        self.bootstyle = bootstyle
        
        self.pbars: dict[str, tb.Progressbar] = {}
        self.vars: dict[str, tk.DoubleVar] = {}

        _hasText: bool = bool(_text)
        if _hasText: 
            self.configure(text=_text)

        _frmRowOverall: tb.Frame = self._hc.ControlFrameForRow(self)

        self._varOverallText = tk.DoubleVar(value=0)
        self._pbarOverall = self._hc.ControlProgressBarLEFT(_frmRowOverall, _variable= self._varOverallText)

        # --- Frame Inferior: Contenedor Scrollable ---
        self.scroll_frame = tb.ScrolledFrame(self, autohide=True)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)

        if items and len(items) > 0:
            self.SetItems(items)

    def SetItems(self, items: list[str], _startValue: float = 0.0) -> None:
        """Inicializa las barras de progreso para la lista de ítems recibida."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.pbars.clear()
        self.vars.clear()

        has_items = bool(items)
        if not has_items: return
        _maxLen = self._hc.GetMaxCharWidth(self._pbarOverall, items, _addText = self.DEFAULT_TEXT_SUFIX_PROGRESS)
        for item in items:
            
            # Variable vinculada al avance del ítem y traza para recalcular el general
            var = tk.DoubleVar(value=_startValue)
            var.trace_add('write', lambda *args: self.__UpdateOverallState())
            self.vars[item] = var
            pbar = self._hc.ControlProgressBar(self.scroll_frame, item, _variable=var, _width=_maxLen)
            self.pbars[item] = pbar

        self.ResetAll(_startValue if has_items else 0.0)

    def UpdateProgress(self, item: str, value: float) -> None:
        """Actualiza el progreso de un ítem en particular (0.0 a 100.0)."""
        if item in self.vars:
            clamped_val = max(0.0, min(100.0, float(value)))
            self.vars[item].set(clamped_val)  # Dispara la actualización automática del Overall

    def __UpdateOverallState(self) -> None:
        """Recalcula el promedio de todos los progressbar e informa a la barra superior."""
        if not self.vars:
            self._pbarOverall["value"] = 0
            self._varOverallText.set(0)
            return

        total_value = sum(var.get() for var in self.vars.values())
        avg_value = total_value / len(self.vars)

        self._pbarOverall["value"] = avg_value
        self._varOverallText.set(avg_value)

    def GetProgressValues(self) -> dict[str, float]:
        """Devuelve un diccionario con el porcentaje actual de cada ítem."""
        return {item: var.get() for item, var in self.vars.items()}

    def ResetAll(self, state: float = 0.0) -> None:
        """Resetea todas las barras al valor recibido (por defecto 0.0)."""
        clamped_val = max(0.0, min(100.0, float(state)))
        for var in self.vars.values():
            var.set(clamped_val)

class HelperStyle():
    @staticmethod
    def GetStyle(_parent:tk.Misc)->tb.Style:
        root_window = _parent.winfo_toplevel()
        if isinstance(root_window, tb.Window):
            return root_window.style
        return tb.Style(_parent)

    
        
#endregion
