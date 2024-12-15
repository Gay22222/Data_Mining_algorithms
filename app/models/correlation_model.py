import statistics
import numpy as np

class CorrelationModel:
    def __init__(self):
        """
        Khởi tạo model cho phân tích tương quan Pearson.
        """
        self.data_x = None  # Danh sách giá trị X
        self.data_y = None  # Danh sách giá trị Y
        self.stats = {}  # Thống kê X và Y
        self.pearson_r = None  # Giá trị Pearson r

    def set_data(self, data_x, data_y):
        """
        Thiết lập dữ liệu đầu vào cho X và Y.
        Args:
            data_x (list): Danh sách các giá trị thuộc cột X.
            data_y (list): Danh sách các giá trị thuộc cột Y.
        """
        if not data_x or not data_y or len(data_x) != len(data_y):
            raise ValueError("Dữ liệu không hợp lệ. X và Y phải có cùng kích thước và không được rỗng.")
        self.data_x = data_x
        self.data_y = data_y

    def calculate_stats(self):
        """
        Tính toán các giá trị thống kê cho X và Y.
        Returns:
            dict: Thống kê trung bình và độ lệch chuẩn cho X và Y.
        """
        try:
            stats = {
                "Trung Bình X": round(statistics.mean(self.data_x), 3),
                "Độ Lệch Chuẩn X": round(statistics.stdev(self.data_x), 3),
                "Trung Bình Y": round(statistics.mean(self.data_y), 3),
                "Độ Lệch Chuẩn Y": round(statistics.stdev(self.data_y), 3),
                "Kích Thước Mẫu": len(self.data_x)
            }
            self.stats = stats
            return stats
        except Exception as e:
            raise ValueError(f"Lỗi khi tính toán thống kê: {e}")

    def calculate_pearson(self):
        """
        Tính toán hệ số tương quan Pearson r.
        Returns:
            float: Giá trị Pearson r.
        """
        try:
            # Tính các giá trị trung gian
            mean_x = statistics.mean(self.data_x)
            mean_y = statistics.mean(self.data_y)
            covariance = sum([(x - mean_x) * (y - mean_y) for x, y in zip(self.data_x, self.data_y)])
            std_x = np.sqrt(sum([(x - mean_x) ** 2 for x in self.data_x]))
            std_y = np.sqrt(sum([(y - mean_y) ** 2 for y in self.data_y]))

            # Tính Pearson r
            self.pearson_r = covariance / (std_x * std_y)
            return round(self.pearson_r, 3)
        except Exception as e:
            raise ValueError(f"Lỗi khi tính Pearson r: {e}")

    def interpret_correlation(self):
        """
        Diễn giải kết quả tương quan dựa trên giá trị Pearson r.
        Returns:
            str: Kết luận về hướng tương quan.
        """
        if self.pearson_r is None:
            raise ValueError("Pearson r chưa được tính toán.")
        if self.pearson_r > 0:
            return "Tương Quan Thuận"
        elif self.pearson_r < 0:
            return "Tương Quan Nghịch"
        else:
            return "Không Có Tương Quan"
