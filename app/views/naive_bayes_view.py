
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class NaiveBayesView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root, bg="#F8F9FA")
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện."""
        # Tiêu đề
        tk.Label(self, text="Phân Lớp Naive Bayes", font=("Arial", 20, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

        # Khu vực chọn file
        self.init_file_section()

        # Hiển thị dữ liệu trong TreeView
        self.init_treeview_section()

        # Khu vực chọn cột
        self.init_column_section()

        # Khu vực nhập dữ liệu mẫu
        self.init_input_section()

        # Khu vực kết quả và log
        self.init_result_and_log_section()

        # Nút điều khiển
        self.init_control_buttons()
        
    def init_file_section(self):
        """Khu vực chọn file."""
        file_frame = tk.Frame(self, bg="#F8F9FA")
        file_frame.pack(pady=10)
        tk.Button(file_frame, text="Chọn File", bg="#2182f0", fg="white", command=self.controller.load_file).pack(side="left", padx=10)
        self.file_label = tk.Label(file_frame, text="Chưa tải file", bg="#F8F9FA")
        self.file_label.pack(side="left")

    def init_treeview_section(self):
        """Hiển thị dữ liệu bằng TreeView."""
        tree_frame = tk.Frame(self, bg="#F8F9FA")
        tree_frame.pack(pady=10, fill="both", expand=True)
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set, show="headings")
        tree_scrollbar.configure(command=self.tree.yview)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")


    def init_column_section(self):
        """Khu vực chọn cột."""
        column_frame = tk.LabelFrame(self, text="Chọn Tập Thuộc Tính và Cột Mục Tiêu", bg="#F8F9FA")
        column_frame.pack(pady=10, fill="x", expand=True, padx=20)

        # Tất cả các cột
        tk.Label(column_frame, text="Tất cả Cột:", bg="#F8F9FA").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.all_columns_listbox = tk.Listbox(column_frame, selectmode="multiple", height=5)
        self.all_columns_listbox.grid(row=1, column=0, padx=10, pady=5)

        # Cột đặc trưng (features)
        tk.Label(column_frame, text="Cột Đặc Trưng:", bg="#F8F9FA").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.selected_columns_listbox = tk.Listbox(column_frame, selectmode="multiple", height=5)
        self.selected_columns_listbox.grid(row=1, column=2, padx=10, pady=5)

        # Nút di chuyển giữa các cột
        tk.Button(column_frame, text=">>", command=lambda: self.controller.move_items(self.all_columns_listbox, self.selected_columns_listbox)).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(column_frame, text="<<", command=lambda: self.controller.move_items(self.selected_columns_listbox, self.all_columns_listbox)).grid(row=2, column=1, padx=10, pady=5)

        # Cột mục tiêu (target)
        tk.Label(column_frame, text="Cột Mục Tiêu:", bg="#F8F9FA").grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.target_combobox = ttk.Combobox(column_frame, state="readonly")
        self.target_combobox.grid(row=1, column=3, padx=10, pady=5)
        


    def init_input_section(self):
        """Khu vực nhập dữ liệu mẫu."""
        input_frame = tk.LabelFrame(self, text="Nhập Mẫu Cần Phân Loại", bg="#F8F9FA")
        input_frame.pack(pady=10, fill="x", padx=20)
        self.input_frame = input_frame  # Giữ tham chiếu để cập nhật sau
        


    def init_result_and_log_section(self):
        """Khu vực hiển thị kết quả và log."""
        result_frame = tk.LabelFrame(self, text="Kết Quả", bg="#F8F9FA")
        result_frame.pack(pady=10, fill="both", expand=True)
        self.result_text = tk.Text(result_frame)
        self.result_text.pack(fill="both", expand=True)

        log_frame = tk.LabelFrame(self, text="Log", bg="#F8F9FA")
        log_frame.pack(pady=10, fill="x", padx=20)
        self.log_label = tk.Label(log_frame, text="Log: ", bg="#F8F9FA", anchor="w", fg="green")
        self.log_label.pack(fill="x", padx=10)
        
        

    def init_control_buttons(self):
        """Thêm các nút điều khiển."""
        tk.Button(self, text="Cập Nhật Mẫu", bg="#2182f0", fg="white", command=self.controller.update_sample_inputs).pack(pady=10)
        tk.Button(self, text="Phân Loại", bg="#2182f0", fg="white", command=self.controller.classify_sample).pack(pady=10)
        tk.Button(self, text="Reset", bg="#DC3545", fg="white", command=self.controller.reset_data).pack(pady=10)
        tk.Button(self, text="Quay lại Menu", bg="#DC3545", fg="white", command=self.controller.go_back_to_menu).pack(pady=10)

    def update_treeview(self, data):
        """Cập nhật TreeView với dữ liệu."""
        self.tree["columns"] = list(data.columns)
        self.tree.delete(*self.tree.get_children())
        for col in data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        for _, row in data.iterrows():
            self.tree.insert("", "end", values=row.tolist())


    def add_input_combobox(self, feature_name, values):
        """
        Thêm một Combobox nhập liệu cho cột đặc trưng.
        """
        try:
            tk.Label(self.input_frame, text=feature_name, bg="#F8F9FA").pack(side="left", padx=10, pady=5)
            combobox = ttk.Combobox(self.input_frame, values=list(values), state="readonly", width=15)
            combobox.pack(side="left", padx=10, pady=5)
            return combobox
        except Exception as e:
            self.update_log(f"Lỗi khi thêm Combobox: {e}")
            raise

    
    def clear_input_frame(self):
        """Xóa nội dung trong khu vực nhập dữ liệu mẫu."""
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    def update_log(self, message):
        """Cập nhật thông báo log."""
        self.log_label.config(text=f"Log: {message}")

    def show_result(self, result):
        """Hiển thị kết quả phân loại."""
        self.result_text.delete(1.0, "end")
        self.result_text.insert("end", f"Kết Quả: {result}\n")
        
    

