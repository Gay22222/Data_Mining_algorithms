import pandas as pd
from tkinter import filedialog, messagebox
import statistics
import numpy as np

from models.correlation_model import CorrelationModel

class CorrelationController:
    def __init__(self, app):
        """
        Controller cho phân tích tương quan Pearson.
        """
        self.app = app
        self.view = None
        self.model = CorrelationModel()  # Tích hợp model
        self.data = None  # Dữ liệu từ file Excel
        self.column_x = None  # Cột được chọn làm X
        self.column_y = None  # Cột được chọn làm Y
        self.init_view()

    def init_view(self):
        """Khởi tạo View."""
        from views.correlation_view import CorrelationView
        self.view = CorrelationView(self.app.scrollable_frame, self)
        self.app.frames["Correlation"] = self.view
        self.app.center_frame()

    def load_file(self):
        """
        Tải file Excel và hiển thị dữ liệu gốc trong TreeView.
        """
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            if not file_path:
                return

            # Đọc dữ liệu từ file Excel
            self.data = pd.read_excel(file_path)

            # Kiểm tra dữ liệu có hợp lệ không
            if self.data.empty or len(self.data.columns) < 2:
                raise ValueError("Dữ liệu không hợp lệ hoặc không đủ cột để phân tích.")

            # Hiển thị dữ liệu lên TreeView
            self.view.update_treeview(self.data)

            # Cập nhật Combobox để chọn cột
            self.view.x_combobox["values"] = list(self.data.columns)
            self.view.y_combobox["values"] = list(self.data.columns)

            # Hiển thị thông báo
            self.view.file_label.config(text=f"Tải file: {file_path.split('/')[-1]}")
            self.view.update_log("Tải file thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file: {e}")
            self.view.update_log(f"Lỗi khi tải file: {e}")

    def confirm_columns(self):
        """
        Xác nhận cột X và Y do người dùng chọn.
        """
        try:
            self.column_x = self.view.x_combobox.get()
            self.column_y = self.view.y_combobox.get()

            # Kiểm tra người dùng đã chọn đầy đủ cột chưa
            if not self.column_x or not self.column_y:
                raise ValueError("Vui lòng chọn cả cột X và cột Y.")

            # Lấy dữ liệu X và Y
            data_x = self.data[self.column_x].to_list()
            data_y = self.data[self.column_y].to_list()

            # Thiết lập dữ liệu cho model
            self.model.set_data(data_x, data_y)

            # Cập nhật log
            self.view.update_log(f"Đã chọn cột X: {self.column_x}, cột Y: {self.column_y}.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xác nhận cột: {e}")
            self.view.update_log(f"Lỗi khi xác nhận cột: {e}")

    def analyze_correlation(self):
        """
        Thực hiện phân tích tương quan Pearson.
        """
        try:
            # Tính các giá trị thống kê
            stats_data = self.model.calculate_stats()
            self.view.update_stats_treeview(stats_data)

            # Tính Pearson r
            r = self.model.calculate_pearson()
            correlation_text = self.model.interpret_correlation()

            # Hiển thị kết quả
            self.view.update_results(r, correlation_text)
            self.view.update_log("Phân tích tương quan thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phân tích tương quan: {e}")
            self.view.update_log(f"Lỗi khi phân tích tương quan: {e}")

    def reset(self):
        """
        Đặt lại toàn bộ dữ liệu và giao diện.
        """
        try:
            # Reset dữ liệu trong model và controller
            self.model = CorrelationModel()
            self.data = None
            self.column_x = None
            self.column_y = None

            # Reset TreeView của View
            for treeview in [self.view.data_tree, self.view.stats_tree]:
                treeview.delete(*treeview.get_children())  # Xóa toàn bộ dữ liệu trong TreeView
                treeview["columns"] = []  # Xóa các heading của TreeView
                for column in treeview["columns"]:
                    treeview.heading(column, text="")  # Xóa tiêu đề

            # Reset nhãn file
            self.view.file_label.config(text="Chưa tải file")

            # Reset các ComboBox
            self.view.x_combobox.set("")
            self.view.y_combobox.set("")
            self.view.x_combobox["values"] = []
            self.view.y_combobox["values"] = []

            # Reset các nhãn kết quả
            self.view.pearson_value_label.config(text="---")
            self.view.correlation_label.config(text="---")

            # Reset log
            self.view.update_log("Đã reset dữ liệu và giao diện.")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể reset: {e}")
            self.view.update_log(f"Lỗi khi reset: {e}")



    def go_back_to_menu(self):
        """
        Quay lại menu chính.
        """
        self.app.show_frame("main_menu")
