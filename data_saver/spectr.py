from excel_worker.custom_data_frame import CustomDataFrame
from excel_worker.excel_worker import SaveToExcel

class SpectrSaveToExcel(SaveToExcel):
    def __init__(self, data: dict, custom_data_frame: CustomDataFrame = None) -> None:
        super().__init__(data, custom_data_frame)
    
    def save(self, file_path: str) -> None:
        self.custom_data_frame.add_column('labels', self._data['labels'])
        self.custom_data_frame.add_column('distances', self._data['distances'])
        self.custom_data_frame.add_column('differences', self._data['differences'])
        self.custom_data_frame.add_column('query', self._data['query'])

        self.custom_data_frame.add_column('count cluster', self._data['count cluster'])

        self.custom_data_frame.to_excel(file_path, index=False)