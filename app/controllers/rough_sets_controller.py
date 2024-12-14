from models.rough_set_model import RoughSetModel
import pandas as pd
from tkinter import messagebox, filedialog
from io import BytesIO
from PIL import Image, ImageTk


class RoughSetsController:
    def __init__(self, app):
        self.app = app
        self.model = None  # Model sẽ được tạo sau khi dữ liệu được tải
        self.view = None  # View sẽ được tạo và đăng ký vào frames
        self.init_view()

    def init_view(self):
        """Khởi tạo View và thêm vào frames."""
        from views.rough_sets_view import RoughSetsView
        self.view = RoughSetsView(self.app.scrollable_frame, self)
        self.app.frames["Tập Thô"] = self.view
        self.app.center_frame()
        


    def load_file(self):
        """Xử lý khi người dùng chọn file để tải dữ liệu."""
        try:
            file_path = self.view.file_label.cget("text")
            file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
            if file_path:
                data = pd.read_excel(file_path)
                self.model = RoughSetModel(data)  # Khởi tạo Model với dữ liệu mới
                self.view.file_label.config(text=f"Tải thành công: {file_path.split('/')[-1]}")
                self.update_treeview(data)
                self.update_column_and_x_lists(data)
                self.app.center_frame()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")

    def update_treeview(self, data):
        """Cập nhật dữ liệu hiển thị trong TreeView."""
        self.view.tree["columns"] = list(data.columns)
        self.view.tree["show"] = "headings"
        self.view.tree.delete(*self.view.tree.get_children())
        for col in data.columns:
            self.view.tree.heading(col, text=col)
            self.view.tree.column(col, width=120)
        for _, row in data.iterrows():
            self.view.tree.insert("", "end", values=row.tolist())

    def update_column_and_x_lists(self, data):
        """Cập nhật danh sách các thuộc tính và tập X."""
        self.view.all_columns_listbox.delete(0, "end")
        for col in data.columns:
            self.view.all_columns_listbox.insert("end", col)
        self.view.target_combobox["values"] = list(data.columns)
        self.view.target_combobox.set(data.columns[-1])
        self.view.all_x_listbox.delete(0, "end")
        if "ID" in data.columns:
            for id_value in data["ID"]:
                self.view.all_x_listbox.insert("end", id_value)

    def move_items(self, source_listbox, target_listbox):
        """Di chuyển các mục giữa các Listbox."""
        selected_indices = list(source_listbox.curselection())
        for i in selected_indices:
            item = source_listbox.get(i)
            target_listbox.insert("end", item)
        for i in reversed(selected_indices):
            source_listbox.delete(i)

    def analyze(self):
        """Xử lý phân tích dữ liệu."""
        if not self.model:
            messagebox.showwarning("Cảnh báo", "Hãy tải dữ liệu trước.")
            return

        try:
            # Lấy các giá trị đầu vào
            b_attributes = [self.view.selected_columns_listbox.get(i) for i in range(self.view.selected_columns_listbox.size())]
            c_attribute = self.view.target_combobox.get()
            X = [self.view.selected_x_listbox.get(i) for i in range(self.view.selected_x_listbox.size())]

            if not b_attributes or not c_attribute or not X:
                messagebox.showwarning("Cảnh báo", "Hãy chọn đầy đủ tập B, tập X và cột mục tiêu.")
                return

            # Sử dụng model để tính toán
            b_lower = self.model.b_lower_approximation(X, b_attributes)
            b_upper = self.model.b_upper_approximation(X, b_attributes)
            boundary = self.model.boundary_region(set(b_lower['ID']), set(b_upper['ID']))
            outside = self.model.outside_region(set(b_upper['ID']))
            dependency = self.model.dependency_degree(c_attribute, b_attributes)
            equivalence_result = self.model.equivalence_classes(b_attributes)

            # Hiển thị kết quả
            self.view.result_text.delete(1.0, "end")
            self.view.result_text.insert("end", f"Các Lớp Tương Đương: {equivalence_result}\n")
            self.view.result_text.insert("end", f"Xấp xỉ dưới B: {list(b_lower['ID'])}\n")
            self.view.result_text.insert("end", f"Xấp xỉ trên B: {list(b_upper['ID'])}\n")
            self.view.result_text.insert("end", f"Vùng biên B: {list(boundary)}\n")
            self.view.result_text.insert("end", f"Vùng ngoài B: {list(outside)}\n")
            self.view.result_text.insert("end", f"Mức độ phụ thuộc: {dependency:.2f}\n")

            # Hiển thị biểu đồ
            self.display_graph(set(b_lower['ID']), set(b_upper['ID']), boundary, outside, X)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phân tích: {e}")

    def display_graph(self, lower, upper, boundary, outside, X):
        """Tạo và hiển thị biểu đồ trong Canvas."""
        try:
            graph_image = self.model.generate_graph(lower, upper, boundary, outside, X)
            image = Image.open(BytesIO(graph_image))
            photo = ImageTk.PhotoImage(image)

            self.view.canvas.delete("all")
            self.view.canvas.create_image(0, 0, anchor="nw", image=photo)
            self.view.canvas.image = photo
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị biểu đồ: {e}")

    def reset_data(self):
        """Reset giao diện và dữ liệu."""
        self.model = None  # Reset model
        self.view.file_label.config(text="Chưa tải file")
        self.view.tree.delete(*self.view.tree.get_children())
        self.view.all_columns_listbox.delete(0, "end")
        self.view.selected_columns_listbox.delete(0, "end")
        self.view.all_x_listbox.delete(0, "end")
        self.view.selected_x_listbox.delete(0, "end")
        self.view.target_combobox.set("")
        self.view.result_text.delete(1.0, "end")
        self.view.canvas.delete("all")
        self.view.tree["columns"] = []  # Xóa cấu trúc cột trong TreeView
        self.view.tree["show"] = ""  # Đặt lại chế độ hiển thị của TreeView
        self.app.center_frame()

    def go_back_to_menu(self):
        self.app.show_frame("main_menu")


