import pandas as pd 
from models.apriori_model import AprioriModel
from tkinter import filedialog, messagebox


class AprioriController:
    def __init__(self, app):
        """
        Khởi tạo controller cho thuật toán Apriori.
        """
        self.app = app
        self.model = AprioriModel()
        self.view = None
        self.data = None  # Dữ liệu gốc từ file Excel
        self.binary_matrix = None  # Ma trận nhị phân
        self.frequent_itemsets = None  # Tập phổ biến
        self.maximal_itemsets = None  # Tập phổ biến tối đại
        self.rules = None  # Các luật kết hợp
        self.init_view()

    def init_view(self):
        """
        Khởi tạo view và liên kết với frame chính.
        """
        from views.apriori_view import AprioriView
        self.view = AprioriView(self.app.scrollable_frame, self)
        self.app.frames["Apriori"] = self.view
        self.app.center_frame()

    def load_file(self):
        """
        Tải file Excel và hiển thị dữ liệu gốc trong TreeView.
        """
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            if not file_path:
                return

            # Đọc dữ liệu từ file Excel
            data = pd.read_excel(file_path)
            self.data = data

            # Chuẩn bị giao dịch và tạo ma trận nhị phân
            self.model.prepare_transactions(data)
            self.binary_matrix = self.model.generate_binary_matrix()

            # Hiển thị dữ liệu ban đầu
            self.view.update_treeview(self.view.data_tree, data.values.tolist(), data.columns.tolist())

            # Hiển thị ma trận nhị phân
            self.view.update_treeview(
                self.view.binary_tree,
                self.binary_matrix.values.tolist(),
                self.binary_matrix.columns.tolist()
            )

            self.view.update_log("Tải file thành công.")
            self.app.center_frame()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file: {e}")
            self.view.update_log(f"Lỗi khi tải file: {e}")

    def find_frequent_itemsets(self):
        """Tìm tập phổ biến từ dữ liệu."""
        if self.data is None or self.binary_matrix is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu và tạo ma trận nhị phân trước.")
            self.view.update_log("Không thể tìm tập phổ biến: Dữ liệu hoặc ma trận nhị phân chưa được tạo.")
            return
        try:
            # Lấy ngưỡng min_sup từ giao diện
            min_sup = self.view.min_sup_entry.get()
            
            # Kiểm tra min_sup có hợp lệ không
            if not min_sup or not min_sup.replace('.', '', 1).isdigit() or float(min_sup) <= 0 or float(min_sup) > 1:
                messagebox.showerror("Lỗi", "Ngưỡng hỗ trợ (min_sup) không hợp lệ. Vui lòng nhập một số trong khoảng (0, 1].")
                self.view.update_log("Ngưỡng hỗ trợ không hợp lệ.")
                return

            min_sup = float(min_sup)
            self.model.set_params(min_sup, self.model.min_conf)

            # Loại bỏ cột ID khỏi binary_matrix
            binary_matrix_no_id = self.binary_matrix.drop(columns=["ID"], errors="ignore")

            # Tìm tập phổ biến
            frequent_itemsets_df = self.model.find_frequent_itemsets(binary_matrix_no_id)

            # Kiểm tra dữ liệu trả về
            if frequent_itemsets_df.empty:
                messagebox.showinfo("Thông báo", "Không tìm thấy tập phổ biến nào.")
                self.view.update_log("Không tìm thấy tập phổ biến nào.")
                return

            frequent_itemsets_df["support"] = frequent_itemsets_df["support"].round(3)
            
            # Lưu kết quả vào self.frequent_itemsets
            self.frequent_itemsets = {
                frozenset(itemset): support
                for itemset, support in zip(frequent_itemsets_df['itemsets'], frequent_itemsets_df['support'])
            }

            # Chuyển đổi `frozenset` thành chuỗi để hiển thị
            frequent_data = [
                [", ".join(itemset), support, len(itemset)]
                for itemset, support in self.frequent_itemsets.items()
            ]

            # Hiển thị tập phổ biến
            self.view.update_treeview(self.view.frequent_tree, frequent_data, ["Tập Phổ Biến", "Hỗ Trợ", "Độ Dài"])
            self.view.update_log("Tìm tập phổ biến thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm tập phổ biến: {e}")
            self.view.update_log(f"Lỗi khi tìm tập phổ biến: {e}")


    def find_maximal_itemsets(self):
        """Tìm tập phổ biến tối đại từ tập phổ biến."""
        if not self.frequent_itemsets or len(self.frequent_itemsets) == 0:
            # Nếu không có tập phổ biến nào, cảnh báo cho người dùng
            messagebox.showwarning("Cảnh báo", "Vui lòng tìm tập phổ biến trước.")
            self.view.update_log("Không thể tìm tập phổ biến tối đại: Tập phổ biến chưa được tìm.")
            return
        try:
            # Tìm tập phổ biến tối đại từ model
            maximal_itemsets_df = self.model.find_maximal_frequent_itemsets()
            self.maximal_itemsets = maximal_itemsets_df

            # Nếu không có tập phổ biến tối đại nào, thông báo
            if maximal_itemsets_df.empty:
                messagebox.showinfo("Thông báo", "Không có tập phổ biến tối đại nào được tìm thấy.")
                self.view.update_log("Không có tập phổ biến tối đại nào được tìm thấy.")
                return

            maximal_itemsets_df["support"] = maximal_itemsets_df["support"].round(3)
            
            # Chuyển đổi dữ liệu thành dạng hiển thị
            maximal_data = [
                [", ".join(itemset), self.frequent_itemsets[frozenset(itemset)], len(itemset)]
                for itemset in maximal_itemsets_df['itemsets']
            ]

            # Cập nhật TreeView để hiển thị tập phổ biến tối đại
            self.view.update_treeview(
                self.view.maximal_tree,
                maximal_data,
                ["Tập Phổ Biến Tối Đại", "Hỗ Trợ", "Độ Dài"]
            )
            self.view.update_log("Tìm tập phổ biến tối đại thành công.")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm tập phổ biến tối đại: {e}")
            self.view.update_log(f"Lỗi khi tìm tập phổ biến tối đại: {e}")



    def generate_rules(self):
        """Sinh các luật kết hợp từ tập phổ biến."""
        if not self.frequent_itemsets or len(self.frequent_itemsets) == 0:
            messagebox.showwarning("Cảnh báo", "Vui lòng tìm tập phổ biến trước.")
            self.view.update_log("Không thể sinh luật kết hợp: Tập phổ biến chưa được tìm.")
            return

        try:
            min_conf = self.view.min_conf_entry.get()
            # Kiểm tra min_sup có hợp lệ không
            if not min_conf or not min_conf.replace('.', '', 1).isdigit() or float(min_conf) <= 0 or float(min_conf) > 1:
                messagebox.showerror("Lỗi", "Ngưỡng tin cậy (min_conf) không hợp lệ. Vui lòng nhập một số trong khoảng (0, 1].")
                self.view.update_log("Ngưỡng tin cậy không hợp lệ.")
                return

            min_conf = float(min_conf)
            self.model.set_params(self.model.min_sup, min_conf)
            
            # Chuyển đổi self.frequent_itemsets từ dict sang DataFrame
            frequent_itemsets_df = pd.DataFrame(
                {
                    "itemsets": list(self.frequent_itemsets.keys()),
                    "support": list(self.frequent_itemsets.values())
                }
            )
            frequent_itemsets_df["itemsets"] = frequent_itemsets_df["itemsets"].apply(
                lambda x: frozenset(x) if not isinstance(x, frozenset) else x
            )

            # Gọi model để sinh luật
            rules = self.model.generate_rules(frequent_itemsets_df)

            # Chuyển đổi dữ liệu luật kết hợp sang danh sách để hiển thị
            # Làm tròn các cột hỗ trợ và độ tin cậy
            rules["antecedent support"] = rules["antecedent support"].round(3)
            rules["consequent support"] = rules["consequent support"].round(3)
            rules["support"] = rules["support"].round(3)
            rules["confidence"] = rules["confidence"].round(3)
            
            rules_data = rules.values.tolist()

            # Hiển thị các luật kết hợp trong TreeView
            self.view.update_treeview(
                self.view.rules_tree,
                rules_data,
                ["Tiền Đề", "Kết Quả", "Hỗ Trợ Tiền Đề", "Hỗ Trợ Kết Quả", "Hỗ Trợ", "Độ Tin Cậy"]
            )
            self.view.update_log("Sinh luật kết hợp thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sinh luật kết hợp: {e}")
            self.view.update_log(f"Lỗi khi sinh luật kết hợp: {e}")













    def reset(self):
        """
        Đặt lại toàn bộ dữ liệu và giao diện.
        """
        try:
            # Reset dữ liệu trong class
            self.data = None
            self.binary_matrix = None
            self.frequent_itemsets = None
            self.maximal_itemsets = None
            self.rules = None

            # Reset tất cả các TreeView (bao gồm cả xóa heading)
            for tree in [self.view.data_tree, self.view.binary_tree, self.view.frequent_tree, self.view.maximal_tree, self.view.rules_tree]:
                # Xóa toàn bộ các hàng trong TreeView
                tree.delete(*tree.get_children())
                # Xóa các heading nếu có
                for col in tree["columns"]:
                    tree.heading(col, text="")  # Xóa tiêu đề cột
                tree["columns"] = ()  # Xóa danh sách cột hiện tại

            # Reset các ô nhập liệu và log
            self.view.min_sup_entry.delete(0, "end")
            self.view.min_conf_entry.delete(0, "end")
            self.view.log_text.configure(state="normal")
            self.view.log_text.delete(1.0, "end")
            self.view.log_text.configure(state="disabled")

            # Reset nhãn file
            self.view.file_label.config(text="Chưa tải file")

            # Log thông báo reset thành công
            self.view.update_log("Dữ liệu và giao diện đã được reset.")
            self.app.center_frame()
        except Exception as e:
            # Xử lý lỗi nếu có
            self.view.update_log(f"Lỗi khi đặt lại: {e}")
            messagebox.showerror("Lỗi", f"Không thể đặt lại dữ liệu: {e}")


    def go_back_to_menu(self):
        """
        Quay lại menu chính.
        """
        self.app.show_frame("main_menu")
