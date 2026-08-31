from typing import Protocol, runtime_checkable, Self

@runtime_checkable
class ISupportEnum(Protocol):
    @property
    def value(self)->int: ...
    @property
    def label(self)->str: ...

    @classmethod
    def FindByLabel(cls, label: str, _allowRaise:bool=True) -> Self:
        ...