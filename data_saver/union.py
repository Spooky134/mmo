from excel_worker.custom_data_frame import CustomDataFrame
from excel_worker.excel_worker import SaveToExcel

class UnionSaveToExcel(SaveToExcel):
    def __init__(self, data: dict, custom_data_frame: CustomDataFrame = None) -> None:
        super().__init__(data, custom_data_frame)
    
    def save(self, file_path: str) -> None:
        self.custom_data_frame.add_column('labels', self._data['labels'])
        self.custom_data_frame.to_excel(file_path, index=False)