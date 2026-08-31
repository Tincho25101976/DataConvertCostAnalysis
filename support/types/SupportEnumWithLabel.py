from abc import ABC
from typing import Type, TypeVar, Generic, Self
from enum import Enum


TSelf = TypeVar("TSelf", bound='HelperSupportEnum')
                
class HelperSupportEnum(Enum):
    _label:str    

    def __new__(cls, value:int, label:str)->Self:
        obj = object.__new__(cls)
        obj._value_ = value
        obj._label = label
        return obj

    @property
    def label(self) -> str:
        return self._label

    @classmethod
    def FindByLabel(cls:Type[TSelf], label: str, _allowRaise:bool=True) -> TSelf:
        find:str=label.lower()
        for member in cls:
            if member.label.lower() == find:
                return member
        if _allowRaise: 
            raise ValueError(f"No {cls.__name__} member found with label: '{label}'")
        return getattr(cls, 'UNDEFINED') # type: ignore[return-value]