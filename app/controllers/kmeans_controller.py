from views.kmeans_view import KMeansView
from models.kmeans_model import KMeansModel

class KMeansController:
    def __init__(self, app):
        self.app = app
        self.model = KMeansModel()
        self.view = KMeansView(app.scrollable_frame, self)

        self.app.frames["K-Means"] = self.view

    def load_data(self, file_path):
        """
        Xử lý khi người dùng chọn file để đọc dữ liệu.
        """
        try:
            data = self.model.load_data(file_path)
            self.view.update_data_table(data)  # Gọi View để hiển thị dữ liệu
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
