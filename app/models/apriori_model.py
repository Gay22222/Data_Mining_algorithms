import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


class AprioriModel:
    def __init__(self):
        self.min_sup = None  # Ngưỡng hỗ trợ tối thiểu
        self.min_conf = None  # Ngưỡng độ tin cậy tối thiểu
        self.transactions = []  # Danh sách các giao dịch
        self.frequent_itemsets = None  # Tập phổ biến với độ hỗ trợ
        self.rules = None  # Các luật kết hợp

    def set_params(self, min_sup, min_conf):
        """Đặt giá trị ngưỡng hỗ trợ và độ tin cậy."""
        if min_sup is None or min_sup <= 0 or min_sup > 1:
            raise ValueError("Ngưỡng hỗ trợ (min_sup) phải nằm trong khoảng (0, 1].")
        if min_conf is not None and (min_conf <= 0 or min_conf > 1):
            raise ValueError("Ngưỡng độ tin cậy (min_conf) phải nằm trong khoảng (0, 1].")
        self.min_sup = min_sup
        self.min_conf = min_conf


    def prepare_transactions(self, data):
        """
        Chuẩn bị dữ liệu giao dịch từ DataFrame đầu vào.
        Kiểm tra dữ liệu có đủ cột 'ID' và 'items' hay không.
        """
        if 'ID' not in data.columns or 'items' not in data.columns:
            raise ValueError("Dữ liệu phải chứa các cột 'ID' và 'items'.")
        self.transactions = data.groupby('ID')['items'].apply(list).tolist()

    def generate_binary_matrix(self):
        """
        Tạo ma trận nhị phân (one-hot encoding) từ danh sách giao dịch.
        Đảm bảo rằng dữ liệu đã được chuẩn bị trước.
        """
        if not self.transactions:
            raise ValueError("Danh sách giao dịch rỗng. Hãy gọi prepare_transactions() trước.")
        te = TransactionEncoder()
        binary_matrix = te.fit(self.transactions).transform(self.transactions)
        binary_matrix_df = pd.DataFrame(binary_matrix, columns=te.columns_)
        binary_matrix_df.insert(0, 'ID', [f"o{i+1}" for i in range(len(self.transactions))])  # Thêm cột 'ID'
        return binary_matrix_df

    def find_frequent_itemsets(self, binary_matrix):
        """
        Tìm tập phổ biến bằng thuật toán Apriori.
        Args:
            binary_matrix (pd.DataFrame): Ma trận nhị phân, không chứa cột 'ID'.
        Returns:
            pd.DataFrame: DataFrame chứa các tập phổ biến, độ hỗ trợ và độ dài.
        """
        if self.min_sup is None:
            raise ValueError("min_sup chưa được thiết lập. Hãy gọi set_params().")
        if 'ID' in binary_matrix.columns:
            binary_matrix = binary_matrix.drop(columns=['ID'], errors='ignore')  # Loại bỏ cột 'ID'

        # Sử dụng hàm apriori từ mlxtend
        self.frequent_itemsets = apriori(binary_matrix, min_support=self.min_sup, use_colnames=True)
        self.frequent_itemsets['length'] = self.frequent_itemsets['itemsets'].apply(lambda x: len(x))  # Thêm cột 'length'
        self.num_itemsets = len(self.frequent_itemsets)
        return self.frequent_itemsets

    def find_maximal_frequent_itemsets(self):
        """
        Tìm tập phổ biến tối đại từ tập phổ biến.
        Lọc các tập mà không có tập cha nào lớn hơn.
        Returns:
            pd.DataFrame: DataFrame chứa các tập phổ biến tối đại.
        """
        if self.frequent_itemsets is None or self.frequent_itemsets.empty:
            raise ValueError("Chưa có tập phổ biến. Hãy gọi find_frequent_itemsets() trước.")
        
        # Lọc ra các tập phổ biến tối đại
        maximal_itemsets = self.frequent_itemsets.copy()
        maximal_itemsets['is_subset'] = maximal_itemsets['itemsets'].apply(
            lambda itemset: any(
                itemset < other for other in maximal_itemsets['itemsets'] if itemset != other
            )
        )
        maximal_itemsets = maximal_itemsets[~maximal_itemsets['is_subset']].drop(columns=['is_subset'])  # Loại bỏ cột phụ
        return maximal_itemsets

    def generate_rules(self, frequent_itemsets_df):
        """
        Sinh các luật kết hợp từ tập phổ biến.
        Args:
            frequent_itemsets_df (pd.DataFrame): DataFrame chứa các tập phổ biến.
        Returns:
            pd.DataFrame: DataFrame chứa các luật kết hợp với các cột cần thiết.
        """
        if frequent_itemsets_df.empty:
            raise ValueError("Tập phổ biến rỗng. Không thể sinh luật kết hợp.")

        try:
            # Chuyển đổi cột 'itemsets' thành frozenset nếu chưa đúng định dạng
            

            # Tính toán luật kết hợp
            rules = association_rules(
                frequent_itemsets_df,num_itemsets=self.num_itemsets, metric="confidence", min_threshold=self.min_conf
            )

            # Lọc các cột cần thiết
            rules = rules[
                [
                    "antecedents",
                    "consequents",
                    "antecedent support",
                    "consequent support",
                    "support",
                    "confidence",
                ]
            ]

            # Đảm bảo các giá trị trong 'antecedents' và 'consequents' được chuyển sang dạng danh sách
            rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x))
            rules["consequents"] = rules["consequents"].apply(lambda x: list(x))

            self.rules = rules
            return rules

        except Exception as e:
            raise ValueError(f"Lỗi khi sinh luật kết hợp: {e}")










