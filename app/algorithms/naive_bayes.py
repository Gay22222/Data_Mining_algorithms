import pandas as pd
from collections import defaultdict
import numpy as np

class NaiveBayesClassifierModified:
    def __init__(self, laplace_smoothing=False):
        self.laplace_smoothing = laplace_smoothing
        self.class_probs = {}  # Xác suất tiên nghiệm P(C)
        self.cond_probs = {}   # Xác suất có điều kiện P(X|C)
        self.feature_values = defaultdict(set)  # Giá trị thuộc tính cho từng feature

    def fit(self, X, y):
        """
        Huấn luyện mô hình với tập dữ liệu huấn luyện (X) và nhãn lớp (y).
        """
        n_samples = len(y)
        classes = y.unique()

        # Xác suất tiên nghiệm P(C)
        for c in classes:
            self.class_probs[c] = (y == c).sum() / n_samples

        # Xác suất có điều kiện P(X|C)
        for column in X.columns:
            self.cond_probs[column] = {}
            for c in classes:
                self.cond_probs[column][c] = defaultdict(int)
                subset = X[y == c][column]
                for value in subset:
                    self.feature_values[column].add(value)
                    self.cond_probs[column][c][value] += 1

                # Làm trơn Laplace (nếu được bật)
                total_count = sum(self.cond_probs[column][c].values())
                if self.laplace_smoothing:
                    for value in self.feature_values[column]:
                        self.cond_probs[column][c][value] = (self.cond_probs[column][c][value] + 1) / (total_count + len(self.feature_values[column]))
                else:
                    for value in self.feature_values[column]:
                        self.cond_probs[column][c][value] = self.cond_probs[column][c][value] / total_count

    def predict(self, sample):
        """
        Dự đoán nhãn lớp cho một mẫu.
        """
        class_scores = {}
        for c in self.class_probs:
            class_scores[c] = np.log(self.class_probs[c])  # Log của P(C)
            for feature, value in sample.items():
                if value in self.cond_probs[feature][c]:
                    class_scores[c] += np.log(self.cond_probs[feature][c][value])
                else:
                    class_scores[c] += np.log(1e-6 if not self.laplace_smoothing else 1 / (len(self.feature_values[feature]) + 1))

        return max(class_scores, key=class_scores.get)

# Hàm hỗ trợ đọc dữ liệu từ file Excel
def load_data(file_path):
    """
    Đọc dữ liệu từ file Excel và trả về DataFrame.
    """
    try:
        # Đọc toàn bộ dữ liệu, giữ nguyên tất cả các cột
        data = pd.read_excel(file_path, engine='openpyxl')
        return data
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc file: {e}")