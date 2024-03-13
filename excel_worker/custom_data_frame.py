import pandas as pd

class CustomDataFrame(pd.DataFrame):    
    def add_column(self, name_column: str, data: list) -> None:
        if len(data) < self.shape[0]: 
            data.extend(['']*(self.shape[0] - len(data)))
        elif len(data) > self.shape[0]:
            data = data[:self.shape[0]]

        self[name_column] = data

    def add_row(self, data: list) -> None:
        if len(data) < self.shape[1]:
            data.extend([''] * (self.shape[1] - len(data)))
        elif len(data) > self.shape[1]:
            data = data[:self.shape[1]]
            
        self.loc[self.shape[0]] = data