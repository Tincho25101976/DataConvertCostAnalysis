from pandas import DataFrame


class DataTypeDataTable():
    def __init__(self, name:str, df:DataFrame) -> None:
        self.name = name
        self.df = df