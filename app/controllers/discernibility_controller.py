import pandas as pd
from models.discernibility_model import DiscernibilityModel
from tkinter import filedialog, messagebox

class DiscernibilityController:
    def __init__(self, app):
        self.app = app
        self.model = None
        self.view = None
        self.data = None
        self.matrix = None
        self.init_view()

    def init_view(self):
        from views.discernibility_view import DiscernibilityView
        self.view = DiscernibilityView(self.app.scrollable_frame, self)
        self.app.frames["Hàm phân biệt"] = self.view
        self.app.center_frame()

    def load_file(self):
        """Load data from file."""
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            self.view.update_log("Hủy tải file.")
            return
        try:
            # Đọc file
            raw_data = pd.read_excel(file_path)
            
            # Kiểm tra nếu có cột ID
            if 'ID' not in raw_data.columns:
                messagebox.showwarning("Cảnh báo", "Dữ liệu không chứa cột 'ID'.")
                self.view.update_log("Dữ liệu không chứa cột 'ID'.")
                return
            
            self.data = raw_data  # Dữ liệu gốc (bao gồm ID) để hiển thị
            self.processed_data = raw_data.drop(columns=['ID'])  # Loại bỏ cột ID để chạy thuật toán
            
            # Cập nhật TreeView hiển thị dữ liệu
            self.view.update_treeview(self.data)
            self.view.file_label.config(text=f"File đã tải: {file_path.split('/')[-1]}")
            self.view.update_log(f"Tải file thành công: {file_path.split('/')[-1]}")
            self.app.center_frame()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file: {e}")
            self.view.update_log(f"Lỗi khi tải file: {e}")


    def create_matrix(self):
        """Tạo ma trận phân biệt."""
        if self.data is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước.")
            self.view.update_log("Tạo ma trận thất bại: Chưa có dữ liệu.")
            return
        try:
            criteria = self.processed_data.columns[:-1].tolist()  # Loại cột mục tiêu
            target = self.processed_data.columns[-1]
            self.model = DiscernibilityModel(self.processed_data, criteria, target)
            self.matrix = self.model.generate_discernibility_matrix()
            self.view.update_matrix_treeview(self.matrix)
            self.view.update_log("Đã tạo ma trận phân biệt.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo ma trận phân biệt: {e}")
            self.view.update_log(f"Lỗi khi tạo ma trận phân biệt: {e}")

    def optimize_matrix(self):
        """Tối ưu ma trận phân biệt."""
        if self.matrix is None or self.matrix.empty:
            messagebox.showwarning("Cảnh báo", "Vui lòng tạo ma trận phân biệt trước.")
            self.view.update_log("Tối ưu thất bại: Ma trận phân biệt chưa được tạo.")
            return
        try:
            optimized_result = self.model.optimize_discernibility_matrix(self.matrix)
            self.view.display_optimized_result(optimized_result)
            self.view.update_log("Tối ưu ma trận thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tối ưu ma trận: {e}")
            self.view.update_log(f"Lỗi khi tối ưu ma trận: {e}")

    def reset_data(self):
        """Reset toàn bộ giao diện và dữ liệu trong view."""
        try:
            # Xóa dữ liệu trong model và controller
            self.data = None
            self.matrix = None

            # Reset nhãn file
            self.view.file_label.config(text="Chưa tải file")

            # Xóa dữ liệu trong TreeView hiển thị dữ liệu
            self.view.tree.delete(*self.view.tree.get_children())
            self.view.tree["columns"] = []
            
            # Xóa dữ liệu trong TreeView hiển thị ma trận phân biệt
            self.view.matrix_tree.delete(*self.view.matrix_tree.get_children())
            self.view.matrix_tree["columns"] = []

            # Reset ô kết quả tối ưu
            self.view.result_text.delete(1.0, "end")

            # Reset log
            self.view.update_log("Dữ liệu đã được reset.")
            self.app.center_frame()
        except Exception as e:
            self.view.update_log(f"Lỗi khi reset dữ liệu: {e}")

    def go_back_to_menu(self):
        """Quay lại menu chính."""
        self.view.update_log("Quay lại menu chính.")
        self.app.show_frame("main_menu")
