import tkinter as tk
from tkinter import filedialog, ttk
from app.algorithms.kmeans import load_data, kmeans, generate_kmeans_plot, format_point
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def kmeans_interface(root, frames, main_menu, scroll_canvas, scrollable_frame):
    # Ẩn các frame khác
    for frame in frames.values():
        frame.pack_forget()

    # Lấy frame K-Means
    frame = frames["K-Means"]
    frame.pack(fill="both", expand=True)

    # Xóa các widget cũ trong frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Tạo khung nội dung
    content_frame = tk.Frame(frame, bg="#F8F9FA")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Xử lý sự kiện chuột lăn
    def _on_mousewheel(event):
        if event.delta:  # Windows/macOS
            scroll_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        else:  # Linux (Button-4 và Button-5)
            if event.num == 4:
                scroll_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                scroll_canvas.yview_scroll(1, "units")
    scrollable_frame.unbind("<MouseWheel>")
    root.unbind_all("<MouseWheel>") 
    # Gắn sự kiện chuột lăn khi chuột vào/ra khung cuộn
    scrollable_frame.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", _on_mousewheel))
    scrollable_frame.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))
    
    # Biến toàn cục
    data = None
    canvas = None

    # Tiêu đề
    tk.Label(content_frame, text="K-Means", font=("Arial", 24, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

    # Chức năng chọn file
    def select_file():
        nonlocal data
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                data = load_data(file_path)
                data_table.delete(*data_table.get_children())
                for point in data:
                    data_table.insert("", "end", values=(point[0], point[1]))
                result_label.config(text="File đã được tải thành công.", fg="green")
            except Exception as e:
                result_label.config(text=f"Lỗi: {e}", fg="red")

    # Chức năng chạy thuật toán K-Means
    def run_kmeans():
        nonlocal canvas
        try:
            k = int(k_entry.get())
            if k <= 0:
                result_label.config(text="K phải lớn hơn 0.", fg="red")
                return
            if data is None:
                result_label.config(text="Chọn file trước.", fg="red")
                return
            centroids, labels, clusters = kmeans(data, k)
            result_label.config(text=f"Thuật toán thành công: {len(clusters)} cụm.", fg="green")

            # Hiển thị kết quả chi tiết
            result_text.config(state="normal")
            result_text.delete(1.0, tk.END)
            for i, cluster in enumerate(clusters):
                result_text.insert(tk.END, f"Cụm {i + 1} - Trọng tâm: {format_point(centroids[i])}\n")
                for idx in cluster:
                    result_text.insert(tk.END, f"  Điểm: {format_point(data[idx])}\n")
            result_text.config(state="disabled")

            # Hiển thị biểu đồ
            if canvas:
                canvas.get_tk_widget().destroy()
            fig = generate_kmeans_plot(data, labels, centroids)
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
        except Exception as e:
            result_label.config(text=f"Lỗi: {e}", fg="red")

    # Nút và trường nhập K
    button_frame = tk.Frame(content_frame, bg="#F8F9FA")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Chọn File", font=("Arial", 12), bg="#2182f0", fg="white", command=select_file).grid(row=0, column=0, padx=10)
    tk.Label(button_frame, text="Nhập K:", font=("Arial", 12), bg="#F8F9FA").grid(row=0, column=1, padx=10)
    k_entry = tk.Entry(button_frame, font=("Arial", 12), width=5)
    k_entry.insert(0, "1")
    k_entry.grid(row=0, column=2, padx=10)
    tk.Button(button_frame, text="Chạy Thuật Toán", font=("Arial", 12), bg="#2182f0", fg="white", command=run_kmeans).grid(row=0, column=3, padx=10)

    # TreeView danh sách điểm
    tk.Label(content_frame, text="Danh sách các điểm:", font=("Arial", 12), bg="#F8F9FA").pack(pady=10)
    data_table = ttk.Treeview(content_frame, columns=("X", "Y"), show="headings", height=15)
    data_table.heading("X", text="X")
    data_table.heading("Y", text="Y")
    data_table.pack(fill="x", padx=20)

    # Kết quả ngôn ngữ tự nhiên
    tk.Label(content_frame, text="Kết quả:", font=("Arial", 12), bg="#F8F9FA").pack(pady=10)
    result_text = tk.Text(content_frame, wrap="word", height=15, state="disabled")
    result_text.pack(fill="x", padx=20)

    # Biểu đồ
    tk.Label(content_frame, text="Biểu đồ:", font=("Arial", 12), bg="#F8F9FA").pack(pady=10)
    canvas_frame = tk.Frame(content_frame, bg="#F8F9FA")
    canvas_frame.pack(fill="both", padx=20, pady=10, expand=True)

    # Nhãn thông báo
    result_label = tk.Label(content_frame, text="", font=("Arial", 12), bg="#F8F9FA", fg="black")
    result_label.pack(pady=10)

    # Nút reset
    def reset_data():
        nonlocal data, canvas
        data = None
        data_table.delete(*data_table.get_children())
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.config(state="disabled")
        result_label.config(text="")
        if canvas:
            canvas.get_tk_widget().destroy()
            canvas = None

    tk.Button(content_frame, text="Reset", font=("Arial", 12), bg="#DC3545", fg="white", command=reset_data).pack(pady=10)

    # Nút quay lại Menu
    tk.Button(content_frame, text="Quay lại Menu", font=("Arial", 12), bg="#DC3545", fg="white",
              command=lambda: main_menu(root, frames, scroll_canvas, scrollable_frame)).pack(pady=10)
