import pandas as pd
import numpy as np
from graphviz import Digraph

class ID3Model:
    def __init__(self):
        """
        Khởi tạo ID3 Model.
        """
        self.tree = None

    def entropy(self, data):
        """
        Tính Entropy của dữ liệu.
        Args:
            data (pd.Series): Cột dữ liệu mục tiêu.
        Returns:
            float: Giá trị entropy.
        """
        probabilities = data.value_counts(normalize=True)
        return -sum(p * np.log2(p) for p in probabilities)

    def gini_index(self, data):
        """
        Tính chỉ số Gini của dữ liệu.
        Args:
            data (pd.Series): Cột dữ liệu mục tiêu.
        Returns:
            float: Giá trị Gini.
        """
        probabilities = data.value_counts(normalize=True)
        return 1 - sum(p ** 2 for p in probabilities)

    def information_gain(self, data, target, feature, method="gain"):
        """
        Tính thông tin thu được (Gain) hoặc chỉ số Gini giảm.
        Args:
            data (pd.DataFrame): Tập dữ liệu.
            target (str): Cột mục tiêu.
            feature (str): Cột thuộc tính đang xét.
            method (str): Phương pháp tính toán: "gain" hoặc "gini".
        Returns:
            float: Giá trị Gain hoặc Gini giảm.
        """
        total_rows = len(data)
        unique_values = data[feature].unique()

        if method == "gain":
            parent_entropy = self.entropy(data[target])
            weighted_entropy = 0
            for value in unique_values:
                subset = data[data[feature] == value]
                weighted_entropy += (len(subset) / total_rows) * self.entropy(subset[target])
            return parent_entropy - weighted_entropy

        elif method == "gini":
            parent_gini = self.gini_index(data[target])
            weighted_gini = 0
            for value in unique_values:
                subset = data[data[feature] == value]
                weighted_gini += (len(subset) / total_rows) * self.gini_index(subset[target])
            return parent_gini - weighted_gini

    def best_split(self, data, target, method):
        """
        Tìm thuộc tính tốt nhất để chia dữ liệu.
        Args:
            data (pd.DataFrame): Tập dữ liệu.
            target (str): Cột mục tiêu.
            method (str): Phương pháp tính toán: "gain" hoặc "gini".
        Returns:
            str: Tên thuộc tính tốt nhất.
        """
        features = [col for col in data.columns if col != target]
        gains = {feature: self.information_gain(data, target, feature, method) for feature in features}
        return max(gains, key=gains.get)

    def build_tree(self, data, target, method="gain", depth=0):
        """
        Xây dựng cây quyết định dựa trên phương pháp ID3.
        Args:
            data (pd.DataFrame): Tập dữ liệu.
            target (str): Cột mục tiêu.
            method (str): Phương pháp tính toán: "gain" hoặc "gini".
            depth (int): Độ sâu hiện tại của cây.
        Returns:
            dict: Cây quyết định dưới dạng từ điển.
        """
        # Dừng khi tất cả các nhãn giống nhau
        if len(data[target].unique()) == 1:
            return data[target].iloc[0]

        # Dừng khi không còn thuộc tính nào để chia
        if len(data.columns) == 1:
            return data[target].mode()[0]

        # Tìm thuộc tính tốt nhất để chia
        best_feature = self.best_split(data, target, method)
        tree = {best_feature: {}}

        # Chia dữ liệu theo thuộc tính tốt nhất
        for value in data[best_feature].unique():
            subset = data[data[best_feature] == value].drop(columns=[best_feature])
            tree[best_feature][value] = self.build_tree(subset, target, method, depth + 1)

        return tree

    def build_tree_and_store(self, data, target, method="gain"):
        """
        Xây dựng cây và lưu vào self.tree.
        Args:
            data (pd.DataFrame): Tập dữ liệu.
            target (str): Cột mục tiêu.
            method (str): Phương pháp tính toán.
        """
        self.tree = self.build_tree(data, target, method)
        return self.tree



    def generate_graph(self, tree):
        """
        Tạo biểu đồ Graphviz từ cây quyết định và trả về dữ liệu nhị phân.
        Args:
            tree (dict): Cây quyết định được sinh ra từ thuật toán ID3.
        Returns:
            bytes: Hình ảnh biểu đồ dưới dạng nhị phân.
        """
        dot = Digraph(format='png')

        def add_edges(subtree, parent):
            for key, value in subtree.items():
                if isinstance(value, dict):
                    # Thêm node con và nối với parent (xóa text cạnh mũi tên)
                    node_name = f"{parent}_{key}"
                    dot.node(node_name, key, shape="ellipse", style="filled", color="lightblue")
                    dot.edge(parent, node_name)  # Không có label cho cạnh
                    add_edges(value, node_name)
                else:
                    # Thêm node lá
                    leaf_name = f"{parent}_{key}_leaf"
                    dot.node(leaf_name, f"{key}: {value}", shape="box", style="filled", color="lightgreen")
                    dot.edge(parent, leaf_name)  # Không có label cho cạnh

        # Tạo node gốc đầu tiên từ key chính của cây
        root_key = list(tree.keys())[0]
        dot.node(root_key, root_key, shape="ellipse", style="filled", color="lightblue")
        add_edges(tree[root_key], root_key)

        # Trả về biểu đồ dưới dạng nhị phân
        return dot.pipe(format="png")
