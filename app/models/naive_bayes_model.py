import pandas as pd
import numpy as np
from collections import defaultdict


class NaiveBayesModel:
    def __init__(self, laplace_smoothing=False):
        """
        Mô hình Naive Bayes với tùy chọn làm trơn Laplace.
        """
        self.laplace_smoothing = laplace_smoothing
        self.class_probs = {}  # P(C): Xác suất tiên nghiệm
        self.cond_probs = {}   # P(X|C): Xác suất có điều kiện
        self.feature_values = defaultdict(set)  # Giá trị thuộc tính duy nhất cho từng cột
        self.is_trained = False  # Kiểm tra trạng thái huấn luyện của model

    def fit(self, X, y):
        """
        Huấn luyện mô hình với dữ liệu đầu vào (X) và nhãn lớp (y).

        Args:
            X (pd.DataFrame): Tập thuộc tính.
            y (pd.Series): Nhãn lớp.
        """
        if X.empty or y.empty:
            raise ValueError("Dữ liệu huấn luyện không được rỗng.")
        if len(X) != len(y):
            raise ValueError("Số lượng mẫu X và y phải khớp nhau.")

        n_samples = len(y)
        classes = y.unique()

        # Tính toán P(C) - Xác suất tiên nghiệm
        for c in classes:
            self.class_probs[c] = (y == c).sum() / n_samples

        # Tính toán P(X|C) - Xác suất có điều kiện
        for column in X.columns:
            self.cond_probs[column] = {}
            for c in classes:
                self.cond_probs[column][c] = defaultdict(int)
                subset = X[y == c][column]
                for value in subset:
                    self.feature_values[column].add(value)
                    self.cond_probs[column][c][value] += 1

                # Áp dụng làm trơn Laplace nếu cần
                total_count = sum(self.cond_probs[column][c].values())
                if self.laplace_smoothing:
                    for value in self.feature_values[column]:
                        self.cond_probs[column][c][value] = (self.cond_probs[column][c][value] + 1) / (
                            total_count + len(self.feature_values[column])
                        )
                else:
                    for value in self.feature_values[column]:
                        self.cond_probs[column][c][value] = self.cond_probs[column][c][value] / total_count

        self.is_trained = True  # Đánh dấu mô hình đã được huấn luyện

    def predict(self, sample):
        """
        Dự đoán nhãn lớp cho một mẫu.

        Args:
            sample (dict): Mẫu cần dự đoán (dictionary với cặp key-value là tên thuộc tính và giá trị).

        Returns:
            str: Nhãn lớp được dự đoán.
        """
        if not self.is_trained:
            raise ValueError("Mô hình chưa được huấn luyện. Vui lòng gọi phương thức `fit()` trước khi dự đoán.")

        class_scores = {}
        for c in self.class_probs:
            class_scores[c] = np.log(self.class_probs[c])  # Log của P(C)
            for feature, value in sample.items():
                if value in self.cond_probs[feature][c]:
                    class_scores[c] += np.log(self.cond_probs[feature][c][value])
                else:
                    # Xử lý trường hợp giá trị không tồn tại
                    class_scores[c] += np.log(1e-6 if not self.laplace_smoothing else 1 / (len(self.feature_values[feature]) + 1))

        # Trả về nhãn lớp với xác suất cao nhất
        return max(class_scores, key=class_scores.get)



    def reset(self):
        """
        Reset lại trạng thái của model.
        """
        self.class_probs.clear()
        self.cond_probs.clear()
        self.feature_values.clear()
