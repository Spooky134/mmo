import pandas as pd
from copy import deepcopy
from abc import abstractmethod, ABC

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


class ReadFromExcel:
    def __init__(self) -> None:
        self.__custom_data_frame = None

    @property
    def custom_data_frame(self) -> CustomDataFrame|None:
        return self.__custom_data_frame
    
      
    def read(self, file_path: str) -> None:
        self.__custom_data_frame = CustomDataFrame(pd.read_excel(file_path))


class SaveToExcel(ABC):
    def __init__(self, data: dict, custom_data_frame: CustomDataFrame=None) -> None:
        self.data = deepcopy(data)
        if custom_data_frame is None:
            self.custom_data_frame = CustomDataFrame()
        else:
            self.custom_data_frame = CustomDataFrame(custom_data_frame.copy(deep=True))

    @property
    def data(self) -> dict:
        return self._data
    
    @data.setter
    def data(self, data: dict) -> None:
        self._data = data

    @property
    def custom_data_frame(self) -> CustomDataFrame:
        return self._custom_data_frame
    
    @custom_data_frame.setter
    def custom_data_frame(self, custom_data_frame: CustomDataFrame) -> None:
        self._custom_data_frame = custom_data_frame

    @abstractmethod
    def save(self, path: str) -> None:
        pass


class ReferenceSaveToExcel(SaveToExcel):
    def __init__(self, data: dict, custom_data_frame: CustomDataFrame=None) -> None:
        super().__init__(data, custom_data_frame)
        
    def save(self, file_path: str) -> None:
        self.custom_data_frame.add_row(self.data['zero_point'].line)
        self.custom_data_frame.add_column('centres(x)', [point.coords[0] for point in self.data['mid_points']])
        self.custom_data_frame.add_column('y', [point.coords[1] for point in self.data['mid_points']])
        self.custom_data_frame.add_column('distances', self.data['distances'])

        self.custom_data_frame.to_excel(file_path, index=False)
        
    
class KMeansSaveToExcel(SaveToExcel):
    def __init__(self, data: dict, custom_data_frame: CustomDataFrame=None) -> None:
        super().__init__(data, custom_data_frame)

    def save(self, file_path: str) -> None:
        self.custom_data_frame.add_row(self.data['zero_point'].line)
        self.custom_data_frame.add_column('distances', self.data['distances_all'])
        self.custom_data_frame.add_column('mean distances', self.data['distances'])
        self.custom_data_frame.add_column('k-means', [point.id_point for point in self.data['k_means']])
        for label in self.data['class_count']:
            self.custom_data_frame.add_column(f'{label}', [self.data['class_count'][label]])

        self.custom_data_frame.to_excel(file_path, index=False)


class ParzenWindowSaveToExcel(SaveToExcel):
    def __init__(self, data: dict, custom_data_frame: CustomDataFrame=None) -> None:
        super().__init__(data, custom_data_frame)

    def save(self, file_path: str) -> None:
        self.custom_data_frame.add_row(self.data['zero_point'].line)
        self.custom_data_frame.add_column('distances all', self.data['distances_all'])
        self.custom_data_frame.add_column('radius', [self.data['radius']])
        self.custom_data_frame.add_column('distances in window', self.data['distances_in_window'])
        self.custom_data_frame.add_column('points_in_window', [point.id_point for point in self.data['points_in_window']])
        for label in self.data['class_count']:
            self.custom_data_frame.add_column(f'{label}', [self.data['class_count'][label]])

        self.custom_data_frame.to_excel(file_path, index=False)