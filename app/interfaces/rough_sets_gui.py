import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.algorithms.rough_sets import (
    equivalence_classes,
    b_lower_approximation_for_X,
    b_upper_approximation_for_X,
    boundary_region,
    outside_region,
    dependency_degree,
)
import pandas as pd
from graphviz import Digraph
from io import BytesIO
from PIL import Image, ImageTk



def rough_sets_interface(root, frames, main_menu, scroll_canvas, scrollable_frame):

    # Ẩn các frame khác
    for frame in frames.values():
        frame.pack_forget()

    # Hiển thị frame chính
    frame = frames["Tập Thô"]
    frame.pack(fill="both", expand=True)

    # Xóa các widget cũ trong frame
    for widget in frame.winfo_children():
        widget.destroy()
    # Biến toàn cục
    data = None

    
    
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
    
    # Hàm tải file
    def load_file():
        nonlocal data
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                data = pd.read_excel(file_path)
                file_label.config(text=f"Tải thành công: {file_path.split('/')[-1]}")
                tree["columns"] = list(data.columns)
                tree["show"] = "headings"
                tree.delete(*tree.get_children())
                for col in data.columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120)
                for _, row in data.iterrows():
                    tree.insert("", "end", values=row.tolist())
                # Cập nhật danh sách cột và tập ID
                update_column_and_x_lists()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")

    # Cập nhật danh sách cột và tập ID
    def update_column_and_x_lists():
        all_columns_listbox.delete(0, tk.END)
        for col in data.columns:
            all_columns_listbox.insert(tk.END, col)
        target_combobox["values"] = list(data.columns)
        target_combobox.set(data.columns[-1])
        all_x_listbox.delete(0, tk.END)
        if "ID" in data.columns:
            for id_value in data["ID"]:
                all_x_listbox.insert(tk.END, id_value)

    # Hàm chuyển các mục giữa các Listbox
    def move_items(source_listbox, target_listbox):
        selected_indices = list(source_listbox.curselection())
        for i in selected_indices:
            item = source_listbox.get(i)
            target_listbox.insert(tk.END, item)
        for i in reversed(selected_indices):
            source_listbox.delete(i)

    # Hàm tạo biểu đồ bằng Graphviz
    def generate_graph(lower, upper, boundary, outside, X):
        try:
            # Đảm bảo các dữ liệu đầu vào là set
            lower = set(lower)
            upper = set(upper)
            boundary = set(boundary)
            outside = set(outside)
            X = set(X)

            dot = Digraph(format='png')

            # Thêm các nút
            dot.node('X', f"X: {', '.join(map(str, X))}", shape='box', style='rounded,filled', color='blue:red', gradientangle='90', fillcolor='white')
            dot.node('Upper', f"Upper B X: {', '.join(map(str, upper))}", shape='box', style='rounded,filled', color='blue:red', gradientangle='90', fillcolor='white')
            dot.node('Lower', f"Lower B X: {', '.join(map(str, lower))}", shape='box', style='rounded,filled', color='blue:red', gradientangle='90', fillcolor='white')
            dot.node('Boundary', f"Boundary B X: {', '.join(map(str, boundary))}", shape='box', style='rounded,filled', color='blue:red', gradientangle='90', fillcolor='white')
            dot.node('Outside', f"Outside B X: {', '.join(map(str, outside))}", shape='box', style='rounded,filled', color='blue:red', gradientangle='90', fillcolor='white')

            # Thêm các cạnh
            dot.edge('X', 'Upper')
            dot.edge('Upper', 'Lower')
            dot.edge('Upper', 'Boundary')
            dot.edge('X', 'Outside')


            # Trả về ảnh
            graph_image = dot.pipe(format='png')
            return graph_image

        except Exception as e:
            raise ValueError(f"Không thể tạo biểu đồ: {e}")


    # Hàm phân tích
    def analyze():
        if data is None:
            messagebox.showwarning("Cảnh báo", "Hãy tải file trước.")
            return

        try:
            # Lấy các giá trị đầu vào
            b_attributes = [selected_columns_listbox.get(i) for i in range(selected_columns_listbox.size())]
            c_attribute = target_combobox.get()
            X = [selected_x_listbox.get(i) for i in range(selected_x_listbox.size())]

            if not b_attributes or not c_attribute or not X:
                messagebox.showwarning("Cảnh báo", "Hãy chọn đầy đủ tập B, tập X và cột mục tiêu.")
                return

            # Tính toán bằng thuật toán
            b_lower = set(b_lower_approximation_for_X(data, X, b_attributes)['ID'])
            b_upper = set(b_upper_approximation_for_X(data, X, b_attributes)['ID'])
            boundary = boundary_region(data, list(b_lower), list(b_upper))
            outside = outside_region(data, list(b_upper))
            dependency = dependency_degree(data, c_attribute, b_attributes)

            
            equivalence_result = equivalence_classes(data, b_attributes)
            # Hiển thị kết quả trong giao diện
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Các Lớp Tương Đương: {equivalence_result}\n")
            result_text.insert(tk.END, f"Xấp xỉ dưới B: {list(b_lower)}\n")
            result_text.insert(tk.END, f"Xấp xỉ trên B: {list(b_upper)}\n")
            result_text.insert(tk.END, f"Vùng biên B: {list(boundary)}\n")
            result_text.insert(tk.END, f"Vùng ngoài B: {list(outside)}\n")
            result_text.insert(tk.END, f"Mức độ phụ thuộc: {dependency:.2f}\n")

            # Hiển thị biểu đồ trong Canvas
            graph_image_data = generate_graph(list(b_lower), list(b_upper), list(boundary), list(outside), X)
            image = Image.open(BytesIO(graph_image_data))
            photo = ImageTk.PhotoImage(image)

            canvas.delete("all")
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.image = photo

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phân tích: {e}")



    # Khung nội dung
    content_frame = tk.Frame(frame, bg="#F8F9FA")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Giao diện
    tk.Label(content_frame, text="Phân Tích Rough Sets", font=("Arial", 20, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=20)

    file_frame = tk.Frame(content_frame)
    file_frame.pack(pady=10)
    tk.Button(file_frame, text="Chọn File",font=("Arial", 12), bg="#2182f0", fg="white", command=load_file).pack(side="left", padx=10)
    file_label = tk.Label(file_frame, text="Chưa tải file")
    file_label.pack(side="left")

    # Treeview với thanh cuộn riêng
    tree_frame = tk.Frame(content_frame)
    tree_frame.pack(pady=10, fill="both", expand=True)
    tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    tree = ttk.Treeview(tree_frame, show="headings", yscrollcommand=tree_scrollbar.set)
    tree_scrollbar.configure(command=tree.yview)

    tree.pack(side="left", fill="both", expand=True)
    tree_scrollbar.pack(side="right", fill="y")

    column_frame = tk.LabelFrame(content_frame, text="Chọn Tập Thuộc Tính và Cột Mục Tiêu")
    column_frame.pack(pady=10, fill="x", padx=20)

    tk.Label(column_frame, text="Tất cả Cột:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    all_columns_listbox = tk.Listbox(column_frame, selectmode="multiple", height=5)
    all_columns_listbox.grid(row=1, column=0, padx=10, pady=5)

    tk.Label(column_frame, text="Tập Thuộc Tính B:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
    selected_columns_listbox = tk.Listbox(column_frame, selectmode="multiple", height=5)
    selected_columns_listbox.grid(row=1, column=2, padx=10, pady=5)

    tk.Button(column_frame, text=">>", command=lambda: move_items(all_columns_listbox, selected_columns_listbox)).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(column_frame, text="<<", command=lambda: move_items(selected_columns_listbox, all_columns_listbox)).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(column_frame, text="Tập X:").grid(row=0, column=3, padx=10, pady=5, sticky="w")
    all_x_listbox = tk.Listbox(column_frame, selectmode="multiple", height=5)
    all_x_listbox.grid(row=1, column=3, padx=10, pady=5)

    selected_x_listbox = tk.Listbox(column_frame, selectmode="multiple", height=5)
    selected_x_listbox.grid(row=1, column=5, padx=10, pady=5)

    tk.Button(column_frame, text=">>", command=lambda: move_items(all_x_listbox, selected_x_listbox)).grid(row=1, column=4, padx=10, pady=5)
    tk.Button(column_frame, text="<<", command=lambda: move_items(selected_x_listbox, all_x_listbox)).grid(row=2, column=4, padx=10, pady=5)

    tk.Label(column_frame, text="Cột Mục Tiêu C:").grid(row=0, column=6, padx=10, pady=5, sticky="w")
    target_combobox = ttk.Combobox(column_frame, state="readonly")
    target_combobox.grid(row=1, column=6, padx=10, pady=5)

    result_frame = tk.LabelFrame(content_frame, text="Kết Quả")
    result_frame.pack(pady=10, fill="both", expand=True)
    result_text = tk.Text(result_frame)
    result_text.pack(fill="both", expand=True)

    # Biểu đồ
    graph_frame = tk.LabelFrame(content_frame, text="Biểu Đồ")
    graph_frame.pack(pady=10, fill="both", expand=True)
    canvas = tk.Canvas(graph_frame, bg="white", height=400)
    canvas.pack(fill="both", expand=True)

    analyze_button = tk.Button(content_frame, text="Phân Tích", font=("Arial", 12), bg="#007BFF", fg="white", command=analyze)
    analyze_button.pack(pady=20)

    # Hàm để reset dữ liệu và giao diện
    def reset_data():
        nonlocal data
        data = None
        file_label.config(text="Chưa tải file")
        tree.delete(*tree.get_children())
        all_columns_listbox.delete(0, tk.END)
        selected_columns_listbox.delete(0, tk.END)
        all_x_listbox.delete(0, tk.END)
        selected_x_listbox.delete(0, tk.END)
        target_combobox.set('')
        result_text.delete(1.0, tk.END)
        canvas.delete("all")

    # Nút reset giao diện
    reset_button = tk.Button(content_frame, text="Reset", font=("Arial", 12), bg="#DC3545", fg="white", command=reset_data)
    reset_button.pack(pady=10)

    # Nút quay lại menu chính
    back_button = tk.Button(content_frame, text="Quay lại Menu", font=("Arial", 12), bg="#DC3545", fg="white",
                        command=lambda: main_menu(root, frames, scroll_canvas, scrollable_frame))
    back_button.pack(pady=10)

