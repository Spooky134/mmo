from excel_worker.custom_data_frame import CustomDataFrame
from excel_worker.excel_worker import SaveToExcel


class StandardSaveToExcel(SaveToExcel):
    def __init__(self, data: dict, custom_data_frame: CustomDataFrame=None) -> None:
        super().__init__(data, custom_data_frame)
        
    def save(self, file_path: str) -> None:
        self.custom_data_frame.add_row(self.data['zero_point'].line)
        self.custom_data_frame.add_column('centres(x)', [point.coords[0] for point in self.data['mid_points']])
        self.custom_data_frame.add_column('y', [point.coords[1] for point in self.data['mid_points']])
        self.custom_data_frame.add_column('distances', self.data['distances'])

        self.custom_data_frame.to_excel(file_path, index=False)