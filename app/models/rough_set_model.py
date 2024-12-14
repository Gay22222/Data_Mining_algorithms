import pandas as pd
from graphviz import Digraph

class RoughSetModel:
    def __init__(self, df):
        """
        Khởi tạo model với DataFrame.
        """
        if 'ID' not in df.columns:
            raise ValueError("DataFrame phải chứa cột 'ID' để định danh các đối tượng.")
        self.df = df

    def equivalence_classes(self, attributes):
        """
        Tính các lớp tương đương theo tập thuộc tính.
        """
        if not set(attributes).issubset(self.df.columns):
            raise ValueError("Một số thuộc tính trong B không tồn tại trong DataFrame.")
        equivalence_classes = self.df.groupby(attributes).groups
        result = []
        for group, indices in equivalence_classes.items():
            result.append(set(self.df.loc[indices, 'ID']))
        return result


    def b_lower_approximation(self, X, attributes):
        """
        Tính xấp xỉ dưới của tập X theo thuộc tính B.
        """
        equivalence_classes = self.df.groupby(attributes).groups
        b_lower = []
        for group, indices in equivalence_classes.items():
            if set(self.df.loc[indices, 'ID']).issubset(X):
                b_lower.extend(indices)
        return self.df.loc[b_lower]

    def b_upper_approximation(self, X, attributes):
        """
        Tính xấp xỉ trên của tập X theo thuộc tính B.
        """
        equivalence_classes = self.df.groupby(attributes).groups
        b_upper = []
        for group, indices in equivalence_classes.items():
            if set(self.df.loc[indices, 'ID']).intersection(X):
                b_upper.extend(indices)
        return self.df.loc[b_upper]

    def positive_region(self, decision_attribute, condition_attributes):
        """
        Tính vùng dương của tập thuộc tính điều kiện với thuộc tính quyết định.
        """
        if decision_attribute not in self.df.columns:
            raise ValueError(f"Cột '{decision_attribute}' không tồn tại trong DataFrame.")
        equivalence_classes = self.df.groupby(condition_attributes).groups
        pos_b_c = set()
        for group, indices in equivalence_classes.items():
            if len(self.df.loc[indices, decision_attribute].unique()) == 1:
                pos_b_c.update(indices)
        return pos_b_c

    def dependency_degree(self, decision_attribute, condition_attributes):
        """
        Tính mức độ phụ thuộc của tập thuộc tính điều kiện với thuộc tính quyết định.
        """
        if len(self.df) == 0:
            raise ValueError("DataFrame không có dữ liệu, không thể tính gamma(B, C).")
        pos_b_c = self.positive_region(decision_attribute, condition_attributes)
        total_objects = len(self.df)
        gamma_bc = len(pos_b_c) / total_objects
        return gamma_bc

    def boundary_region(self, b_lower, b_upper):
        """
        Tính vùng biên.
        """
        return set(b_upper) - set(b_lower)

    def outside_region(self, b_upper):
        """
        Tính vùng ngoài của tập xấp xỉ trên.
        """
        all_objects = set(self.df['ID'])
        return all_objects - set(b_upper)

    def calculate_rough_set_properties(self, X, attributes, decision_attribute):
        """
        Tính toàn bộ các tính chất của tập thô:
        - Xấp xỉ dưới.
        - Xấp xỉ trên.
        - Vùng biên.
        - Vùng ngoài.
        - Gamma (độ phụ thuộc).
        """
        if not isinstance(X, list):
            raise TypeError("Tập X phải là một danh sách.")
        if not set(attributes).issubset(self.df.columns):
            raise ValueError("Một số thuộc tính trong B không tồn tại trong DataFrame.")
        if decision_attribute not in self.df.columns:
            raise ValueError(f"Cột mục tiêu '{decision_attribute}' không tồn tại.")
        
        b_lower = self.b_lower_approximation(X, attributes)
        b_upper = self.b_upper_approximation(X, attributes)
        gamma = self.dependency_degree(decision_attribute, attributes)
        boundary = self.boundary_region(set(b_lower['ID']), set(b_upper['ID']))
        outside = self.outside_region(set(b_upper['ID']))

        return {
            "Lower(B, X)": set(b_lower['ID']),
            "Upper(B, X)": set(b_upper['ID']),
            "Boundary(B, X)": boundary,
            "Outside(B, X)": outside,
            "Gamma(B, C)": gamma
        }
    
    def generate_graph(self, lower, upper, boundary, outside, X):
        """
        Tạo biểu đồ Graphviz để minh họa tập thô.
        - lower: Xấp xỉ dưới.
        - upper: Xấp xỉ trên.
        - boundary: Vùng biên.
        - outside: Vùng ngoài.
        - X: Tập X.
        """
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

            # Trả về biểu đồ dưới dạng dữ liệu nhị phân
            return dot.pipe(format='png')

        except Exception as e:
            raise ValueError(f"Không thể tạo biểu đồ: {e}")