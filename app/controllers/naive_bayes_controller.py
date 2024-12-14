import pandas as pd
from tkinter import messagebox, filedialog
from models.naive_bayes_model import NaiveBayesModel


class NaiveBayesController:
    def __init__(self, app):
        self.app = app
        self.model = NaiveBayesModel()  # Khởi tạo model
        self.view = None  # Sẽ khởi tạo view sau
        self.data = None
        self.feature_columns = []
        self.target_column = None
        self.inputs = {}
        self.init_view()
        

    def init_view(self):
        """Khởi tạo View và thêm vào frames."""
        from views.naive_bayes_view import NaiveBayesView
        self.view = NaiveBayesView(self.app.scrollable_frame, self)
        self.app.frames["Naive Bayes"] = self.view 
        self.app.center_frame()

    def load_file(self):
        """Xử lý khi người dùng chọn file để tải dữ liệu."""
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            if not file_path:
                return

            # Đọc dữ liệu từ file
            self.data = pd.read_excel(file_path)
            self.view.file_label.config(text=f"Tải thành công: {file_path.split('/')[-1]}")
            self.update_treeview(self.data)
            self.update_column_listboxes(self.data)
            self.view.update_log("Dữ liệu đã được tải thành công.")
            self.view.update_idletasks()
            self.app.center_frame()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")
            self.view.update_log(f"Lỗi khi tải dữ liệu: {e}")

    def update_treeview(self, data):
        """Cập nhật dữ liệu hiển thị trong TreeView."""
        self.view.update_treeview(data)
        self.app.center_frame()
        

    def update_column_listboxes(self, data):
        """Cập nhật danh sách các cột vào các Listbox."""
        self.view.all_columns_listbox.delete(0, "end")
        for col in data.columns:
            self.view.all_columns_listbox.insert("end", col)
        self.view.target_combobox["values"] = list(data.columns)
        self.view.target_combobox.set(data.columns[-1])
        self.app.center_frame()
        
    def move_items(self, source_listbox, target_listbox):
        """Di chuyển các mục giữa các Listbox."""
        selected_indices = list(source_listbox.curselection())
        for i in selected_indices:
            item = source_listbox.get(i)
            target_listbox.insert("end", item)
        for i in reversed(selected_indices):
            source_listbox.delete(i)
        self.app.center_frame()

    def update_sample_inputs(self):
        """Cập nhật các trường nhập dữ liệu mẫu."""
        try:
            self.view.clear_input_frame()
            self.feature_columns = [self.view.selected_columns_listbox.get(i) for i in range(self.view.selected_columns_listbox.size())]
            self.target_column = self.view.target_combobox.get()
            self.app.center_frame()

            if not self.feature_columns:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn các cột đặc trưng.")
                return

            # Tạo combobox cho từng cột đặc trưng
            self.inputs = {}
            for feature in self.feature_columns:
                self.inputs[feature] = self.view.add_input_combobox(feature, self.data[feature].unique())

            self.view.update_log("Đã cập nhật các trường nhập dữ liệu mẫu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật mẫu: {e}")
            self.view.update_log(f"Lỗi khi cập nhật mẫu: {e}")

    def classify_sample(self):
        """Phân loại một mẫu dựa trên dữ liệu đã tải."""
        try:
            if self.data is None:
                messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước khi phân loại.")
                return

            sample = {feature: self.inputs[feature].get() for feature in self.feature_columns}
            if any(value == "" for value in sample.values()):
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin mẫu.")
                return

            if not self.target_column or not self.feature_columns:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn các cột đặc trưng và cột mục tiêu.")
                return

            # Huấn luyện model
            X_train = self.data[self.feature_columns]
            y_train = self.data[self.target_column]
            self.model.fit(X_train, y_train)

            # Phân loại mẫu
            prediction = self.model.predict(sample)
            self.view.show_result(prediction)
            self.view.update_log(f"Phân loại thành công. Kết quả: {prediction}")
            self.app.center_frame()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phân loại: {e}")
            self.view.update_log(f"Lỗi khi phân loại: {e}")

    def reset_data(self):
        """
        Reset giao diện và dữ liệu.
        """
        try:
            # Đặt lại model
            self.model.reset()
            # Đặt lại giao diện
            self.view.file_label.config(text="Chưa tải file")  # Nhãn file
            self.view.tree.delete(*self.view.tree.get_children())  # Xóa TreeView
            self.view.all_columns_listbox.delete(0, "end")  # Xóa ListBox tất cả cột
            self.view.selected_columns_listbox.delete(0, "end")  # Xóa ListBox cột đặc trưng
            self.view.target_combobox.set("")  # Đặt lại ComboBox cột mục tiêu
            self.view.clear_input_frame()  # Xóa khu vực nhập mẫu
            self.view.result_text.delete(1.0, "end")  # Đặt lại nhãn kết quả
            self.view.update_log("Giao diện và dữ liệu đã được reset thành công.")  # Cập nhật log trạng thái
            self.view.tree["columns"] = []  # Xóa cấu trúc cột trong TreeView
            self.view.tree["show"] = ""  # Đặt lại chế độ hiển thị của TreeView
            self.app.center_frame()
        except Exception as e:
            self.view.update_log(f"Lỗi khi reset: {e}")
            messagebox.showerror("Lỗi", f"Không thể reset dữ liệu: {e}")

    def clear_input_frame(self):
        """
        Xóa toàn bộ widget trong khu vực nhập mẫu.
        """
        for widget in self.input_frame.winfo_children():
            widget.destroy()
    
    def go_back_to_menu(self):
        """Quay lại menu chính."""
        self.app.show_frame("main_menu")

    
