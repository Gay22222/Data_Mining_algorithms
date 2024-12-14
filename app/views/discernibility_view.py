import tkinter as tk
from tkinter import ttk

class DiscernibilityView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root, bg="#F8F9FA")
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện."""
        # Tiêu đề
        tk.Label(self, text="Tối ưu Ma Trận Phân Biệt", font=("Arial", 20, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

        # Khu vực chọn file
        self.init_file_section()

        # Hiển thị dữ liệu trong TreeView
        self.init_treeview_section()

        # Hiển thị ma trận phân biệt
        self.init_matrix_section()

        # Kết quả tối ưu
        self.init_optimized_result_section()
        
        # Log
        self.init_log_section()
        
        # Chú thích
        self.init_note_section()

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
        """Hiển thị dữ liệu."""
        tree_frame = tk.Frame(self, bg="#F8F9FA")
        tree_frame.pack(pady=10, fill="both", expand=True)
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set, show="headings")
        tree_scrollbar.configure(command=self.tree.yview)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")

    def init_matrix_section(self):
        """Hiển thị ma trận phân biệt."""
        matrix_frame = tk.LabelFrame(self, text="Ma Trận Phân Biệt", bg="#F8F9FA")
        matrix_frame.pack(pady=10, fill="both", expand=True)
        self.matrix_tree = ttk.Treeview(matrix_frame, show="headings")
        self.matrix_tree.pack(fill="both", expand=True)

    def init_optimized_result_section(self):
        """Hiển thị kết quả tối ưu."""
        result_frame = tk.LabelFrame(self, text="Kết Quả Tối Ưu", bg="#F8F9FA")
        result_frame.pack(pady=10, fill="both", expand=True)
        self.result_text = tk.Text(result_frame, height=5)
        self.result_text.pack(fill="both", expand=True)

    def init_log_section(self):
        """Thêm khu vực ghi log."""
        log_frame = tk.LabelFrame(self, text="Log", bg="#F8F9FA")
        log_frame.pack(pady=10, fill="x", padx=20)

        # Sử dụng Label để hiển thị log 
        self.log_label = tk.Label(
            log_frame,
            text="",
            bg="#F8F9FA",
            fg="green",
            anchor="w",  # Căn trái
            font=("Arial", 10)
        )
        self.log_label.pack(fill="x", padx=10)

    def init_note_section(self):
        log_frame = tk.LabelFrame(self, text="Chú thích", bg="#F8F9FA")
        log_frame.pack(pady=10, fill="x", padx=20)
        self.note_label = tk.Label(
            log_frame,
            text="Các kí hiệu trong bảng ma trận là chữ cái đầu của tên cột",
            bg="#F8F9FA",
            fg="green",
            anchor="w",  # Căn trái
            font=("Arial", 10)
        )
        self.note_label.pack(fill="x", padx=10)

    def init_control_buttons(self):
        """Thêm các nút điều khiển."""
        tk.Button(self, text="Tạo Ma Trận", bg="#2182f0", fg="white", command=self.controller.create_matrix).pack(pady=5)
        tk.Button(self, text="Tối Ưu Ma Trận", bg="#2182f0", fg="white", command=self.controller.optimize_matrix).pack(pady=5)
        tk.Button(self, text="Reset", bg="#DC3545", fg="white", command=self.controller.reset_data).pack(pady=5)
        tk.Button(self, text="Quay lại Menu", bg="#DC3545", fg="white", command=self.controller.go_back_to_menu).pack(pady=5)

    def update_log(self, message):
        """Cập nhật log."""
        self.log_label.config(text=f"Log: {message}")


    def update_treeview(self, data):
        """Cập nhật dữ liệu vào TreeView."""
        self.tree["columns"] = list(data.columns)
        self.tree.delete(*self.tree.get_children())
        for col in data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        for _, row in data.iterrows():
            self.tree.insert("", "end", values=row.tolist())

    def update_matrix_treeview(self, matrix):
        """Cập nhật TreeView cho ma trận phân biệt."""
        self.matrix_tree["columns"] = list(matrix.columns)
        self.matrix_tree.delete(*self.matrix_tree.get_children())
        for col in matrix.columns:
            self.matrix_tree.heading(col, text=col)
            self.matrix_tree.column(col, width=100)
        for i in matrix.index:
            self.matrix_tree.insert("", "end", values=[matrix.at[i, j] for j in matrix.columns])

    def display_optimized_result(self, result):
        """Hiển thị kết quả tối ưu."""
        self.result_text.delete(1.0, "end")
        self.result_text.insert("end", result)
