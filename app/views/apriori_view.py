import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class AprioriView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root, bg="#F8F9FA")
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện chính."""
        # Tiêu đề
        tk.Label(self, text="Apriori Algorithm", font=("Arial", 20, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

        # Khu vực chọn file
        self.init_file_section()

        # Khu vực nhập min_sup và min_conf
        self.init_threshold_section()

        # TreeView cho dữ liệu và kết quả
        self.init_treeview_section()

        # Khu vực log
        self.init_log_section()

        # Nút điều khiển
        self.init_control_buttons()

    def init_file_section(self):
        """Khu vực chọn file."""
        file_frame = tk.Frame(self, bg="#F8F9FA")
        file_frame.pack(pady=10)
        tk.Button(file_frame, text="Chọn File", bg="#2182f0", fg="white", command=self.controller.load_file).pack(side="left", padx=10)
        self.file_label = tk.Label(file_frame, text="Chưa tải file", bg="#F8F9FA")
        self.file_label.pack(side="left")

    def init_threshold_section(self):
        """Khu vực nhập ngưỡng hỗ trợ và độ tin cậy."""
        threshold_frame = tk.Frame(self, bg="#F8F9FA")
        threshold_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(threshold_frame, text="min_sup:", bg="#F8F9FA").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.min_sup_entry = tk.Entry(threshold_frame, width=10)
        self.min_sup_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(threshold_frame, text="min_conf:", bg="#F8F9FA").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.min_conf_entry = tk.Entry(threshold_frame, width=10)
        self.min_conf_entry.grid(row=0, column=3, padx=10, pady=5)

    def init_treeview_section(self):
        """Khu vực TreeView cho dữ liệu và kết quả."""
        # Dữ liệu ban đầu
        self.add_treeview_section("Dữ Liệu Ban Đầu", "data_tree")

        # Ma trận nhị phân
        self.add_treeview_section("Ma Trận Nhị Phân", "binary_tree")

        # Tập phổ biến
        self.add_treeview_section("Tập Phổ Biến", "frequent_tree")

        # Tập phổ biến tối đại
        self.add_treeview_section("Tập Phổ Biến Tối Đại", "maximal_tree")

        # Luật kết hợp
        self.add_treeview_section("Luật Kết Hợp", "rules_tree")

    def add_treeview_section(self, title, tree_attr):
        """Thêm một khu vực TreeView với scrollbar."""
        frame = tk.LabelFrame(self, text=title, bg="#F8F9FA")
        frame.pack(pady=10, fill="both", expand=True)
        scroll = ttk.Scrollbar(frame, orient="vertical")
        tree = ttk.Treeview(frame, show="headings", yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        scroll.config(command=tree.yview)
        tree.pack(fill="both", expand=True)
        setattr(self, tree_attr, tree)

    def init_log_section(self):
        """Thêm khu vực ghi log."""
        log_frame = tk.LabelFrame(self, text="Log", bg="#F8F9FA")
        log_frame.pack(pady=10, fill="both", expand=True)
        self.log_text = tk.Text(log_frame, height=4, state="disabled", bg="#E8F6F3", fg="green")
        self.log_text.pack(fill="both", expand=True)

    def init_control_buttons(self):
        """Thêm các nút điều khiển."""
        button_frame = tk.Frame(self, bg="#F8F9FA")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Tìm Tập Phổ Biến", bg="#007BFF", fg="white", command=self.controller.find_frequent_itemsets).pack(side="left", padx=10)
        tk.Button(button_frame, text="Tìm Tập Phổ Biến Tối Đại", bg="#007BFF", fg="white", command=self.controller.find_maximal_itemsets).pack(side="left", padx=10)
        tk.Button(button_frame, text="Sinh Luật Kết Hợp", bg="#007BFF", fg="white", command=self.controller.generate_rules).pack(side="left", padx=10)
        tk.Button(button_frame, text="Reset", bg="#DC3545", fg="white", command=self.controller.reset).pack(side="left", padx=10)
        tk.Button(button_frame, text="Quay Lại Menu", bg="#DC3545", fg="white", command=self.controller.go_back_to_menu).pack(side="left", padx=10)

    def update_treeview(self, tree, data, columns):
        """Cập nhật TreeView với dữ liệu."""
        tree.delete(*tree.get_children())
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)
        for row in data:
            tree.insert("", "end", values=row)

    def update_log(self, message):
        """Cập nhật log."""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.configure(state="disabled")
