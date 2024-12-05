import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class RoughSetsView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root, bg="#F8F9FA")
        self.controller = controller
        self.data = None  # DataFrame lưu dữ liệu
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện chính."""
        # Tiêu đề
        tk.Label(self, text="Phân Tích Rough Sets", font=("Arial", 20, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

        # Khu vực chọn file
        file_frame = tk.Frame(self, bg="#F8F9FA")
        file_frame.pack(pady=10)
        tk.Button(file_frame, text="Chọn File", font=("Arial", 12), bg="#2182f0", fg="white", command=self.controller.load_file).pack(side="left", padx=10)
        self.file_label = tk.Label(file_frame, text="Chưa tải file", bg="#F8F9FA")
        self.file_label.pack(side="left")

        # Hiển thị dữ liệu trong TreeView
        self.tree_frame = tk.Frame(self, bg="#F8F9FA")
        self.tree_frame.pack(pady=10, fill="both", expand=True)
        self.tree_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical")
        self.tree = ttk.Treeview(self.tree_frame, show="headings", yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.configure(command=self.tree.yview)
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree_scrollbar.pack(side="right", fill="y")

        # Các Listbox và Combobox
        self.column_frame = tk.LabelFrame(self, text="Chọn Tập Thuộc Tính và Cột Mục Tiêu", bg="#F8F9FA")
        self.column_frame.pack(pady=10, fill="x", padx=20)
        self.init_column_widgets()

        # Kết quả phân tích
        result_frame = tk.LabelFrame(self, text="Kết Quả", bg="#F8F9FA")
        result_frame.pack(pady=10, fill="both", expand=True)
        self.result_text = tk.Text(result_frame)
        self.result_text.pack(fill="both", expand=True)

        # Biểu đồ
        graph_frame = tk.LabelFrame(self, text="Biểu Đồ", bg="#F8F9FA")
        graph_frame.pack(pady=10, fill="both", expand=True)
        self.canvas = tk.Canvas(graph_frame, bg="white", height=400)
        self.canvas.pack(fill="both", expand=True)

        # Các nút điều khiển
        self.add_control_buttons()

    def init_column_widgets(self):
        """Khởi tạo các widget liên quan đến cột."""
        # Danh sách tất cả các cột
        tk.Label(self.column_frame, text="Tất cả Cột:", bg="#F8F9FA").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.all_columns_listbox = tk.Listbox(self.column_frame, selectmode="multiple", height=5)
        self.all_columns_listbox.grid(row=1, column=0, padx=10, pady=5)

        # Thuộc tính B
        tk.Label(self.column_frame, text="Tập Thuộc Tính B:", bg="#F8F9FA").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.selected_columns_listbox = tk.Listbox(self.column_frame, selectmode="multiple", height=5)
        self.selected_columns_listbox.grid(row=1, column=2, padx=10, pady=5)

        # Nút di chuyển
        tk.Button(self.column_frame, text=">>", command=lambda: self.controller.move_items(self.all_columns_listbox, self.selected_columns_listbox)).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.column_frame, text="<<", command=lambda: self.controller.move_items(self.selected_columns_listbox, self.all_columns_listbox)).grid(row=2, column=1, padx=10, pady=5)

        # Tập X
        tk.Label(self.column_frame, text="Tập X:", bg="#F8F9FA").grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.all_x_listbox = tk.Listbox(self.column_frame, selectmode="multiple", height=5)
        self.all_x_listbox.grid(row=1, column=3, padx=10, pady=5)

        self.selected_x_listbox = tk.Listbox(self.column_frame, selectmode="multiple", height=5)
        self.selected_x_listbox.grid(row=1, column=5, padx=10, pady=5)

        tk.Button(self.column_frame, text=">>", command=lambda: self.controller.move_items(self.all_x_listbox, self.selected_x_listbox)).grid(row=1, column=4, padx=10, pady=5)
        tk.Button(self.column_frame, text="<<", command=lambda: self.controller.move_items(self.selected_x_listbox, self.all_x_listbox)).grid(row=2, column=4, padx=10, pady=5)

        # Cột mục tiêu
        tk.Label(self.column_frame, text="Cột Mục Tiêu C:", bg="#F8F9FA").grid(row=0, column=6, padx=10, pady=5, sticky="w")
        self.target_combobox = ttk.Combobox(self.column_frame, state="readonly")
        self.target_combobox.grid(row=1, column=6, padx=10, pady=5)

    def add_control_buttons(self):
        """Thêm các nút điều khiển."""
        tk.Button(self, text="Phân Tích", font=("Arial", 12), bg="#007BFF", fg="white", command=self.controller.analyze).pack(pady=10)
        tk.Button(self, text="Reset", font=("Arial", 12), bg="#DC3545", fg="white", command=self.controller.reset_data).pack(pady=10)
        tk.Button(self, text="Quay lại Menu", font=("Arial", 12), bg="#DC3545", fg="white",
          command=self.controller.go_back_to_menu).pack(pady=10)
