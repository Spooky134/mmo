from excel_worker.custom_data_frame import CustomDataFrame
from excel_worker.excel_worker import SaveToExcel

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