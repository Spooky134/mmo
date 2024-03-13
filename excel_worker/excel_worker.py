from abc import abstractmethod, ABC
from copy import deepcopy
from excel_worker.custom_data_frame import CustomDataFrame
import pandas as pd

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