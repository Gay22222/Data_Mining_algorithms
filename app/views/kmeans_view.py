import tkinter as tk
from tkinter import filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class KMeansView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root, bg="#F8F9FA")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """Tạo giao diện K-Means."""
        # Tiêu đề
        tk.Label(self, text="K-Means", font=("Arial", 24, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

        # Khung chứa các nút và trường nhập
        button_frame = tk.Frame(self, bg="#F8F9FA")
        button_frame.pack(pady=10)

        # Nút chọn file
        tk.Button(button_frame, text="Chọn File", font=("Arial", 12), bg="#2182f0", fg="white", command=self.select_file).grid(row=0, column=0, padx=10)

        # Trường nhập K
        tk.Label(button_frame, text="Nhập K:", font=("Arial", 12), bg="#F8F9FA").grid(row=0, column=1, padx=10)
        self.k_entry = tk.Entry(button_frame, font=("Arial", 12), width=5)
        self.k_entry.insert(0, "1")
        self.k_entry.grid(row=0, column=2, padx=10)

        # Nút chạy thuật toán
        tk.Button(button_frame, text="Chạy Thuật Toán", font=("Arial", 12), bg="#2182f0", fg="white", command=self.run_kmeans).grid(row=0, column=3, padx=10)

        # Nút Reset
        tk.Button(button_frame, text="Reset", font=("Arial", 12), bg="#DC3545", fg="white", command=self.reset_data).grid(row=0, column=4, padx=10)

        # Danh sách điểm dữ liệu
        tk.Label(self, text="Danh sách các điểm:", font=("Arial", 12), bg="#F8F9FA").pack(pady=10)
        self.data_table = ttk.Treeview(self, columns=("X", "Y"), show="headings", height=15)
        self.data_table.heading("X", text="X")
        self.data_table.heading("Y", text="Y")
        self.data_table.pack(fill="x", padx=20)

        # Kết quả ngôn ngữ tự nhiên
        tk.Label(self, text="Kết quả:", font=("Arial", 12), bg="#F8F9FA").pack(pady=10)
        self.result_text = tk.Text(self, wrap="word", height=15, state="disabled")
        self.result_text.pack(fill="x", padx=20)

        # Biểu đồ
        tk.Label(self, text="Biểu đồ:", font=("Arial", 12), bg="#F8F9FA").pack(pady=10)
        self.canvas_frame = tk.Frame(self, bg="#F8F9FA")
        self.canvas_frame.pack(fill="both", padx=20, pady=10, expand=True)

        # Nhãn thông báo
        self.message_label = tk.Label(self, text="", font=("Arial", 12), bg="#F8F9FA", fg="black")
        self.message_label.pack(pady=10)

        # Nút quay lại menu
        tk.Button(self, text="Quay lại Menu", font=("Arial", 12), bg="#DC3545", fg="white", command=self.go_back_to_menu).pack(pady=10)

    def select_file(self):
        """Hàm xử lý chọn file."""
        self.controller.load_data()


    def run_kmeans(self):
        """Hàm xử lý chạy thuật toán K-Means."""
        try:
            k = int(self.k_entry.get())
            self.controller.run_kmeans(k)
        except ValueError:
            self.show_message("K phải là số nguyên dương.", "red")

    def reset_data(self):
        """Hàm xử lý Reset dữ liệu."""
        self.controller.reset_data()

    def go_back_to_menu(self):
        """Hàm quay lại menu chính."""
        self.controller.app.show_frame("main_menu")

    def update_data_table(self, data):
        """
        Cập nhật dữ liệu trong bảng TreeView.
        """
        # Xóa các hàng cũ trong bảng
        self.data_table.delete(*self.data_table.get_children())
        for point in data:
            # Chuyển từng điểm dữ liệu thành định dạng hiển thị phù hợp
            self.data_table.insert("", "end", values=(f"{point[0]:.2f}", f"{point[1]:.2f}"))


    def show_results(self, results):
        """Hiển thị kết quả K-Means."""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, results)
        self.result_text.config(state="disabled")

    def show_plot(self, fig):
        """Hiển thị biểu đồ kết quả K-Means."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_message(self, message, color):
        """Hiển thị thông báo."""
        self.message_label.config(text=message, fg=color)

    def reset_view(self):
        """Reset giao diện về trạng thái ban đầu."""
        self.data_table.delete(*self.data_table.get_children())
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state="disabled")
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.message_label.config(text="")