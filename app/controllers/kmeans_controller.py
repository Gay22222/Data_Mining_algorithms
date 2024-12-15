from views.kmeans_view import KMeansView
from models.kmeans_model import KMeansModel
import pandas as pd
from tkinter import filedialog

class KMeansController:
    def __init__(self, app):
        self.app = app
        self.model = KMeansModel()
        self.view = KMeansView(app.scrollable_frame, self)

        self.app.frames["K-Means"] = self.view

    def load_data(self):
        """
        Xử lý khi người dùng chọn file Excel để đọc dữ liệu.
        """
        try:
            # Mở hộp thoại chọn file
            file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
            if not file_path:
                self.view.show_message("Không có file nào được chọn.", "red")
                return

            # Đọc dữ liệu từ file Excel
            df = pd.read_excel(file_path)

            # Kiểm tra định dạng dữ liệu
            if not all(col in df.columns for col in ['x', 'y']):
                self.view.show_message("File phải chứa hai cột: 'x' và 'y'.", "red")
                return

            # Chuyển dữ liệu thành mảng numpy
            data = df[['x', 'y']].to_numpy()
            self.model.data = data

            # Cập nhật dữ liệu vào View
            self.view.update_data_table(data)
            self.view.show_message("File đã được tải thành công.", "green")

        except Exception as e:
            self.view.show_message(f"Lỗi: {e}", "red")


    def run_kmeans(self, k):
        try:
            centroids, labels, clusters = self.model.run_kmeans(k)
            self.view.show_results(self.model.display_results())
            self.view.show_plot(self.model.generate_kmeans_plot())
        except Exception as e:
            self.view.show_message(f"Lỗi: {e}", "red")

    def reset_data(self):
        self.model.data = None
        self.view.reset_view()