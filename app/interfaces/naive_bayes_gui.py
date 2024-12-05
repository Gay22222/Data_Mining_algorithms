import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.algorithms.naive_bayes import NaiveBayesClassifierModified, load_data


def naive_bayes_interface(root, frames, main_menu, scroll_canvas, scrollable_frame):
    # Ẩn tất cả các frame khác
    for frame in frames.values():
        frame.pack_forget()

    # Tạo frame chính
    frame = frames["Naive Bayes"]
    frame.pack(fill="both", expand=True)

    # Tạo khung nội dung
    content_frame = tk.Frame(frame, bg="#F8F9FA")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Biến toàn cục
    data = None
    nb_classifier = None
    unique_values = {}
    feature_columns = []
    target_column = None
    inputs = {}

    # Tiêu đề
    tk.Label(content_frame, text="Phân Lớp Naive Bayes", font=("Arial", 20, "bold"), bg="#F8F9FA", fg="#2182f0").pack(pady=10)

    # Khu vực tải file dữ liệu
    file_frame = tk.Frame(content_frame, bg="#F8F9FA")
    file_frame.pack(pady=10)
    tk.Button(file_frame, text="Tải File Dữ Liệu", command=lambda: load_file(), bg="#2182f0", fg="white").pack(side="left", padx=10)
    file_label = tk.Label(file_frame, text="Chưa có file nào được tải", bg="#F8F9FA")
    file_label.pack(side="left")

    # TreeView để hiển thị dữ liệu
    tree_frame = tk.Frame(content_frame, bg="#F8F9FA")
    tree_frame.pack(pady=10)
    tree = ttk.Treeview(tree_frame, show="headings")
    tree.pack(fill="x", padx=10)

    # Khu vực chọn cột
    column_frame = tk.LabelFrame(content_frame, text="Chọn Cột", bg="#F8F9FA")
    column_frame.pack(pady=10, fill="x", padx=20)

    # Listbox tất cả cột
    tk.Label(column_frame, text="Tất cả Cột:", bg="#F8F9FA").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    all_columns_listbox = tk.Listbox(column_frame, selectmode="multiple", height=5)
    all_columns_listbox.grid(row=1, column=0, padx=10, pady=5)

    # Listbox cột đặc trưng
    tk.Label(column_frame, text="Cột Đặc Trưng:", bg="#F8F9FA").grid(row=0, column=2, padx=10, pady=5, sticky="w")
    selected_columns_listbox = tk.Listbox(column_frame, selectmode="multiple", height=5)
    selected_columns_listbox.grid(row=1, column=2, padx=10, pady=5)

    # Nút chuyển cột
    def move_columns_to_features():
        selected_indices = list(all_columns_listbox.curselection())
        for i in selected_indices:
            column_name = all_columns_listbox.get(i)
            selected_columns_listbox.insert(tk.END, column_name)
            all_columns_listbox.delete(i)

    def remove_columns_from_features():
        selected_indices = list(selected_columns_listbox.curselection())
        for i in selected_indices:
            column_name = selected_columns_listbox.get(i)
            all_columns_listbox.insert(tk.END, column_name)
            selected_columns_listbox.delete(i)

    tk.Button(column_frame, text=">>", command=move_columns_to_features).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(column_frame, text="<<", command=remove_columns_from_features).grid(row=2, column=1, padx=10, pady=5)

    # Combobox chọn cột mục tiêu
    tk.Label(column_frame, text="Cột Mục Tiêu:", bg="#F8F9FA").grid(row=0, column=3, padx=10, pady=5, sticky="w")
    target_combobox = ttk.Combobox(column_frame, state="readonly")
    target_combobox.grid(row=1, column=3, padx=10, pady=5, sticky="w")

    # Khu vực nhập dữ liệu mẫu
    input_frame = tk.LabelFrame(content_frame, text="Nhập Mẫu Cần Phân Loại", bg="#F8F9FA")
    input_frame.pack(pady=10, fill="x", padx=20)

    # Tùy chọn làm trơn Laplace
    laplace_var = tk.BooleanVar(value=False)
    tk.Radiobutton(content_frame, text="Không Làm Trơn Laplace", variable=laplace_var, value=False, bg="#F8F9FA").pack()
    tk.Radiobutton(content_frame, text="Làm Trơn Laplace", variable=laplace_var, value=True, bg="#F8F9FA").pack()

    # Nhãn kết quả
    result_label = tk.Label(content_frame, text="Kết Quả: ", font=("Arial", 14), bg="#F8F9FA", fg="#2182f0")
    result_label.pack(pady=10)

    # Log trạng thái
    log_label = tk.Label(content_frame, text="Log:", font=("Arial", 10), bg="#F8F9FA", anchor="w", fg="green")
    log_label.pack(fill="x", padx=10)

    def update_log(message):
        log_label.config(text=f"Log: {message}")

    def load_file():
        nonlocal data, unique_values
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        try:
            data = load_data(file_path)
            file_label.config(text=f"File đã tải: {file_path.split('/')[-1]}")
            tree["columns"] = list(data.columns)
            tree["show"] = "headings"
            for col in data.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            for _, row in data.iterrows():
                tree.insert("", "end", values=row.tolist())
            all_columns_listbox.delete(0, tk.END)
            for col in data.columns:
                all_columns_listbox.insert(tk.END, col)
            target_combobox["values"] = list(data.columns)
            target_combobox.set(data.columns[-1])
            unique_values.update({col: data[col].dropna().unique().tolist() for col in data.columns})
            update_log("File đã được tải thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file: {e}")
            update_log(f"Lỗi: {e}")

    def update_sample_inputs():
        for widget in input_frame.winfo_children():
            widget.destroy()
        selected_features = [selected_columns_listbox.get(i) for i in range(selected_columns_listbox.size())]
        for i, feature in enumerate(selected_features):
            tk.Label(input_frame, text=feature, bg="#F8F9FA").grid(row=0, column=i, padx=10)
            inputs[feature] = ttk.Combobox(input_frame, values=unique_values[feature], state="readonly", width=15)
            inputs[feature].grid(row=1, column=i, padx=10)

    def classify_sample():
        nonlocal nb_classifier, feature_columns, target_column
        if data is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước khi phân loại.")
            update_log("Phân loại thất bại: Dữ liệu chưa được tải.")
            return
        try:
            feature_columns = [selected_columns_listbox.get(i) for i in range(selected_columns_listbox.size())]
            target_column = target_combobox.get()
            if not feature_columns or not target_column:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn đầy đủ cột đặc trưng và cột mục tiêu.")
                update_log("Phân loại thất bại: Cột đặc trưng hoặc cột mục tiêu chưa được chọn.")
                return
            X_train = data[feature_columns]
            y_train = data[target_column]
            nb_classifier = NaiveBayesClassifierModified(laplace_smoothing=laplace_var.get())
            nb_classifier.fit(X_train, y_train)
            sample = {feature: inputs[feature].get() for feature in feature_columns}
            if any(value == "" for value in sample.values()):
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn đầy đủ các giá trị mẫu.")
                update_log("Phân loại thất bại: Thiếu giá trị trong mẫu.")
                return
            prediction = nb_classifier.predict(sample)
            result_label.config(text=f"Kết Quả: {prediction}")
            update_log(f"Phân loại thành công. Kết quả: {prediction}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phân loại: {e}")
            update_log(f"Lỗi khi phân loại: {e}")

    tk.Button(content_frame, text="Cập Nhật Mẫu", command=update_sample_inputs, bg="#2182f0", fg="white").pack(pady=10)
    tk.Button(content_frame, text="Phân Loại", command=classify_sample, bg="#2182f0", fg="white").pack(pady=10)

    def reset_data():
        nonlocal data, nb_classifier, unique_values, feature_columns, target_column, inputs
        data = None
        nb_classifier = None
        unique_values = {}
        feature_columns = []
        target_column = None
        inputs.clear()
        for row in tree.get_children():
            tree.delete(row)
        all_columns_listbox.delete(0, tk.END)
        selected_columns_listbox.delete(0, tk.END)
        target_combobox.set("")
        for widget in input_frame.winfo_children():
            widget.destroy()
        result_label.config(text="Kết Quả: ")
        update_log("Dữ liệu đã được reset.")

    tk.Button(content_frame, text="Reset", font=("Arial", 12), bg="#DC3545", fg="white", command=reset_data).pack(pady=10)
    tk.Button(content_frame, text="Quay lại Menu", font=("Arial", 12), bg="#DC3545", fg="white",
              command=lambda: main_menu(root, frames, scroll_canvas, content_frame)).pack(pady=10)
