import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io

class ID3View(tk.Frame):
    def __init__(self, root, controller):
        """
        Giao diện cho thuật toán ID3.
        """
        super().__init__(root, bg="#F8F9FA")
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện."""
        # Tiêu đề
        tk.Label(self, text="Cây Quyết Định - ID3", font=("Arial", 20, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

        # Khu vực chọn file
        self.init_file_section()

        # Hiển thị dữ liệu trong TreeView
        self.init_data_treeview_section()

        # Khu vực chọn phương pháp tính
        self.init_method_selection_section()

        # Khu vực kết quả tính toán
        self.init_result_section()

        # Log khu vực
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

    def init_method_selection_section(self):
        """Khu vực chọn phương pháp tính toán."""
        method_frame = tk.LabelFrame(self, text="Chọn Cách Tính", bg="#F8F9FA")
        method_frame.pack(pady=10, fill="x", padx=20)

        # Combobox chọn phương pháp tính toán
        tk.Label(method_frame, text="Cách Tính:", bg="#F8F9FA").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.method_combobox = ttk.Combobox(method_frame, state="readonly", width=20)
        self.method_combobox['values'] = ['Gain', 'Gini']
        self.method_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.method_combobox.current(0)  # Chọn "Gain" làm mặc định

    def init_result_section(self):
        """Khu vực kết quả tính toán."""
        result_frame = tk.LabelFrame(self, text="Kết Quả Tính Toán", bg="#F8F9FA")
        result_frame.pack(pady=10, fill="both", expand=True, padx=5)

        self.result_text = tk.Text(result_frame, wrap="word", height=3, bg="white", fg="black", font=("Arial", 10))
        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Khung hiển thị biểu đồ
        result_frame_graph = tk.LabelFrame(self, text="Biểu đồ", bg="#F8F9FA")
        result_frame_graph.pack(pady=10, fill="both", expand=True, padx=5)
        self.graph_frame = tk.Frame(result_frame_graph, bg="#F8F9FA")
        self.graph_frame.pack(pady=10, fill="both", expand=True)

    def init_log_section(self):
        """Khu vực ghi log."""
        log_frame = tk.LabelFrame(self, text="Log", bg="#F8F9FA")
        log_frame.pack(pady=10, fill="x", padx=20)

        self.log_label = tk.Label(log_frame, text="", bg="#F8F9FA", fg="green", anchor="w", font=("Arial", 10))
        self.log_label.pack(fill="x", padx=10)

    def init_control_buttons(self):
        """Các nút điều khiển."""
        button_frame = tk.Frame(self, bg="#F8F9FA")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Phân Tích", bg="#2182f0", fg="white", command=lambda: self.controller.train_model(self.method_combobox.get())).pack(side="left", padx=10)
        tk.Button(button_frame, text="Reset", bg="#DC3545", fg="white", command=self.controller.reset).pack(side="left", padx=10)
        tk.Button(button_frame, text="Quay Lại", bg="#DC3545", fg="white", command=self.controller.go_back_to_menu).pack(side="left", padx=10)

    def update_treeview(self, data):
        """Cập nhật dữ liệu vào TreeView."""
        self.data_tree["columns"] = list(data.columns)
        self.data_tree.delete(*self.data_tree.get_children())
        for col in data.columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=120)
        for _, row in data.iterrows():
            self.data_tree.insert("", "end", values=row.tolist())

    def display_results(self, result_text):
        """Hiển thị kết quả tính toán."""
        self.result_text.delete(1.0, "end")
        self.result_text.insert("end", result_text)
        
    def display_graph(self, graph_data):
        """
        Hiển thị biểu đồ cây quyết định từ dữ liệu nhị phân.
        Args:
            graph_data (bytes): Dữ liệu nhị phân của hình ảnh biểu đồ.
        """
        # Xóa widget cũ nếu có
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Tạo hình ảnh từ dữ liệu nhị phân
        image = Image.open(io.BytesIO(graph_data))
        photo = ImageTk.PhotoImage(image)

        # Hiển thị hình ảnh trên Label
        label = tk.Label(self.graph_frame, image=photo, bg="#F8F9FA")
        label.image = photo  # Giữ tham chiếu để không bị garbage collect
        label.pack(padx=10, pady=5)

    def update_log(self, message):
        """Cập nhật log."""
        self.log_label.config(text=f"Log: {message}")

    def reset(self):
        """Đặt lại giao diện."""
        # Xóa toàn bộ dữ liệu trong TreeView
        self.data_tree.delete(*self.data_tree.get_children())
        self.data_tree["columns"] = ()  # Reset các cột về rỗng

        # Xóa kết quả tính toán trong Text box
        self.result_text.delete(1.0, "end")

        # Xóa biểu đồ trong khung result_frame_graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Reset Combobox về giá trị mặc định
        self.method_combobox.current(0)

        # Xóa Log
        self.log_label.config(text="Log:")

