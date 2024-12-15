import pandas as pd
from tkinter import filedialog, messagebox
from models.id3_model import ID3Model

class ID3Controller:
    def __init__(self, app):
        """
        Controller cho thuật toán ID3.
        """
        self.app = app
        self.model = ID3Model()
        self.view = None
        self.data = None
        self.target_column = None
        self.tree_result = None

        self.init_view()

    def init_view(self):
        """
        Khởi tạo View và liên kết với frame chính.
        """
        from views.id3_view import ID3View
        self.view = ID3View(self.app.scrollable_frame, self)
        self.app.frames["ID3"] = self.view
        self.app.center_frame()

    def load_file(self):
        """
        Tải file Excel và hiển thị dữ liệu trong TreeView.
        """
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            if not file_path:
                return

            # Đọc dữ liệu từ file Excel
            data = pd.read_excel(file_path)
            if "ID" in data.columns:
                self.data = data.drop(columns=["ID"])  # Loại bỏ cột ID khỏi dữ liệu tính toán
            else:
                self.data = data

            # Tự động chọn cột cuối cùng làm cột mục tiêu
            self.target_column = self.data.columns[-1]
            self.view.update_treeview(self.data)
            self.view.file_label.config(text=f"File đã tải: {file_path}")
            self.view.update_log(f"Dữ liệu đã được tải thành công. Cột mục tiêu: {self.target_column}")
            self.app.center_frame()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file: {e}")
            self.view.update_log(f"Lỗi khi tải file: {e}")

    def train_model(self, method):
        """
        Huấn luyện mô hình và tính toán cây quyết định dựa trên phương pháp chọn.
        Args:
            method (str): Phương pháp tính toán ("Gain" hoặc "Gini").
        """
        if self.data is None or self.target_column is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước.")
            self.view.update_log("Không thể huấn luyện mô hình: Dữ liệu bị thiếu.")
            return
        try:
            # Tính toán cây quyết định bằng phương pháp Gain hoặc Gini
            if method == "Gain":
                self.tree_result = self.model.build_tree(self.data, self.target_column, method="gain")
            elif method == "Gini":
                self.tree_result = self.model.build_tree(self.data, self.target_column, method="gini")
            else:
                raise ValueError("Phương pháp tính toán không hợp lệ.")

            # Hiển thị kết quả trên giao diện
            self.view.display_results(self.tree_result)
            
            # Tạo và hiển thị biểu đồ
            graph_data = self.model.generate_graph(self.tree_result)
            self.view.display_graph(graph_data)
            
            self.view.update_log(f"Huấn luyện thành công với phương pháp: {method}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể huấn luyện mô hình: {e}")
            self.view.update_log(f"Lỗi khi huấn luyện mô hình: {e}")

    def reset(self):
        """
        Đặt lại toàn bộ dữ liệu và giao diện.
        """
        try:
            # Reset dữ liệu trong model và controller
            self.model = ID3Model()
            self.data = None
            self.target_column = None
            self.tree_result = None

            # Reset giao diện
            self.view.reset()
            self.view.update_log("Dữ liệu và giao diện đã được reset.")
            self.app.center_frame()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể reset: {e}")
            self.view.update_log(f"Lỗi khi reset: {e}")

    def go_back_to_menu(self):
        """
        Quay lại menu chính.
        """
        self.app.show_frame("main_menu")
