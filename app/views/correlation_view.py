import tkinter as tk
from tkinter import ttk

class CorrelationView(tk.Frame):
    def __init__(self, root, controller):
        """
        Giao diện phân tích tương quan Pearson.
        """
        super().__init__(root, bg="#F8F9FA")
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện."""
        # Tiêu đề
        tk.Label(self, text="Phân Tích Tương Quan Pearson", font=("Arial", 20, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

        # Khu vực chọn file
        self.init_file_section()

        # Hiển thị dữ liệu trong TreeView
        self.init_data_treeview_section()

        # Khu vực chọn cột X và Y
        self.init_column_selection_section()

        # Khu vực thống kê
        self.init_stats_section()

        # Kết quả Pearson
        self.init_result_section()

        # Log
        self.init_log_section()

        # Nút điều khiển
        self.init_control_buttons()

    def init_file_section(self):
        """Khu vực chọn file."""
        file_frame = tk.Frame(self, bg="#F8F9FA")
        file_frame.pack(pady=10)
        tk.Button(file_frame, text="Chọn File", bg="#2182f0", fg="white", command=self.controller.load_file).pack(side="left", padx=10)
        self.file_label = tk.Label(file_frame, text="Chưa tải file", bg="#F8F9FA", fg="black")
        self.file_label.pack(side="left")

    def init_data_treeview_section(self):
        """Hiển thị dữ liệu."""
        tree_frame = tk.LabelFrame(self, text="Dữ Liệu Nhập Vào", bg="#F8F9FA")
        tree_frame.pack(pady=10, fill="both", expand=True)
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        self.data_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set, show="headings")
        tree_scrollbar.configure(command=self.data_tree.yview)
        self.data_tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")

    def init_column_selection_section(self):
        """Khu vực chọn cột X và Y."""
        column_frame = tk.LabelFrame(self, text="Chọn Thuộc Tính X và Y", bg="#F8F9FA")
        column_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(column_frame, text="Chọn cột X:", bg="#F8F9FA", fg="#333333").grid(row=0, column=0, padx=10, pady=5)
        self.x_combobox = ttk.Combobox(column_frame, state="readonly", width=20)
        self.x_combobox.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(column_frame, text="Chọn cột Y:", bg="#F8F9FA", fg="#333333").grid(row=0, column=2, padx=10, pady=5)
        self.y_combobox = ttk.Combobox(column_frame, state="readonly", width=20)
        self.y_combobox.grid(row=0, column=3, padx=10, pady=5)

        tk.Button(column_frame, text="Xác Nhận", bg="#2182f0", fg="white", command=self.controller.confirm_columns).grid(row=0, column=4, padx=10)

    def init_stats_section(self):
        """Khu vực thống kê."""
        stats_frame = tk.LabelFrame(self, text="Thống Kê Thuộc Tính", bg="#F8F9FA")
        stats_frame.pack(pady=10, fill="both", expand=True)

        self.stats_tree = ttk.Treeview(stats_frame, columns=("Thống Kê", "Giá Trị"), show="headings")
        self.stats_tree.heading("Thống Kê", text="Thống Kê")
        self.stats_tree.heading("Giá Trị", text="Giá Trị")
        self.stats_tree.column("Thống Kê", width=150, anchor="center")
        self.stats_tree.column("Giá Trị", width=100, anchor="center")
        self.stats_tree.pack(fill="both", expand=True)

    def init_result_section(self):
        """Hiển thị kết quả phân tích Pearson."""
        result_frame = tk.LabelFrame(self, text="Kết Quả Phân Tích", bg="#F8F9FA")
        result_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(result_frame, text="Hệ Số Pearson r:", bg="#F8F9FA", fg="#333333").grid(row=0, column=0, padx=10, pady=5)
        self.pearson_value_label = tk.Label(result_frame, text="---", bg="#F8F9FA", fg="#2182f0", font=("Arial", 12, "bold"))
        self.pearson_value_label.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(result_frame, text="Hướng Tương Quan:", bg="#F8F9FA", fg="#333333").grid(row=0, column=2, padx=10, pady=5)
        self.correlation_label = tk.Label(result_frame, text="---", bg="#F8F9FA", fg="#2182f0", font=("Arial", 12, "bold"))
        self.correlation_label.grid(row=0, column=3, padx=10, pady=5)

    def init_log_section(self):
        """Thêm khu vực ghi log."""
        log_frame = tk.LabelFrame(self, text="Log", bg="#F8F9FA")
        log_frame.pack(pady=10, fill="x", padx=20)

        self.log_label = tk.Label(
            log_frame,
            text="",
            bg="#F8F9FA",
            fg="green",
            anchor="w",
            font=("Arial", 10)
        )
        self.log_label.pack(fill="x", padx=10)

    def init_control_buttons(self):
        """Thêm các nút điều khiển."""
        button_frame = tk.Frame(self, bg="#F8F9FA")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Phân Tích", bg="#2182f0", fg="white", command=self.controller.analyze_correlation).pack(side="left", padx=10)
        tk.Button(button_frame, text="Reset", bg="#DC3545", fg="white", command=self.controller.reset).pack(side="left", padx=10)
        tk.Button(button_frame, text="Quay Lại", bg="#DC3545", fg="white", command=self.controller.go_back_to_menu).pack(side="left", padx=10)

    def update_log(self, message):
        """Cập nhật log."""
        self.log_label.config(text=f"Log: {message}")

    def update_treeview(self, data):
        """Cập nhật dữ liệu vào TreeView."""
        self.data_tree["columns"] = list(data.columns)
        self.data_tree.delete(*self.data_tree.get_children())
        for col in data.columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=120)
        for _, row in data.iterrows():
            self.data_tree.insert("", "end", values=row.tolist())

    def update_stats_treeview(self, stats_data):
        """Cập nhật TreeView thống kê."""
        self.stats_tree.delete(*self.stats_tree.get_children())
        for stat, value in stats_data.items():
            self.stats_tree.insert("", "end", values=(stat, value))

    def update_results(self, pearson_r, correlation_text):
        """Cập nhật kết quả Pearson."""
        self.pearson_value_label.config(text=f"{pearson_r:.3f}")
        self.correlation_label.config(text=correlation_text)
