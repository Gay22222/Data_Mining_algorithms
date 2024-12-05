import numpy as np
import matplotlib.pyplot as plt

class KMeansModel:
    def __init__(self):
        self.data = None
        self.centroids = None
        self.labels = None
        self.clusters = None

    def format_point(self, point):
        """Định dạng tọa độ dưới dạng [x.xx ; y.yy]."""
        return f"[{point[0]:.2f} ; {point[1]:.2f}]"

    def load_data(self, file_path):
        """
        Đọc dữ liệu từ file và trả về mảng numpy.
        """
        data = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Loại bỏ khoảng trắng và xử lý định dạng
                    point = list(map(float, line.strip().split(',')))
                    data.append(point)
            self.data = np.array(data)
            return self.data
        except Exception as e:
            raise ValueError(f"Lỗi khi đọc file: {e}")

    def run_kmeans(self, k, max_iters=100, tolerance=1e-4):
        """Thực hiện thuật toán K-Means."""
        if self.data is None:
            raise ValueError("Dữ liệu chưa được tải.")
        n_samples, n_features = self.data.shape
        if k <= 0 or k > n_samples:
            raise ValueError("Số cụm K phải nằm trong khoảng [1, số điểm dữ liệu].")
        
        np.random.seed(42)
        centroids = self.data[np.random.choice(n_samples, k, replace=False)]

        for _ in range(max_iters):
            clusters = [[] for _ in range(k)]
            for idx, point in enumerate(self.data):
                distances = np.linalg.norm(point - centroids, axis=1)
                cluster_idx = np.argmin(distances)
                clusters[cluster_idx].append(idx)

            previous_centroids = centroids.copy()
            for i in range(k):
                if clusters[i]:
                    centroids[i] = np.mean(self.data[clusters[i]], axis=0)
                else:
                    centroids[i] = previous_centroids[i]

            if np.linalg.norm(centroids - previous_centroids) <= tolerance:
                break

        self.centroids = np.round(centroids, decimals=2)
        self.clusters = clusters
        self.labels = np.zeros(n_samples, dtype=int)
        for cluster_idx, cluster_points in enumerate(clusters):
            for point_idx in cluster_points:
                self.labels[point_idx] = cluster_idx
        return self.centroids, self.labels, self.clusters

    def generate_kmeans_plot(self):
        """Tạo biểu đồ phân cụm K-Means để nhúng vào giao diện Tkinter."""
        if self.data is None or self.centroids is None or self.labels is None:
            raise ValueError("Thuật toán chưa được chạy hoặc dữ liệu không hợp lệ.")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(self.data[:, 0], self.data[:, 1], c=self.labels, cmap='viridis', alpha=0.6, edgecolor='k', s=50)
        ax.scatter(self.centroids[:, 0], self.centroids[:, 1], c='red', marker='X', s=200, label='Trọng tâm')
        ax.set_title("Biểu đồ phân cụm K-Means", fontsize=14)
        ax.set_xlabel("Trục X", fontsize=10)
        ax.set_ylabel("Trục Y", fontsize=10)
        ax.legend()
        ax.grid(True)
        return fig

    def display_results(self):
        """Hiển thị kết quả định dạng."""
        if self.data is None or self.centroids is None or self.clusters is None:
            raise ValueError("Thuật toán chưa được chạy hoặc dữ liệu không hợp lệ.")
        result = []
        for i, cluster in enumerate(self.clusters):
            cluster_info = f"Cụm {i + 1} - Trọng tâm: {self.format_point(self.centroids[i])}\n"
            cluster_info += "\n".join([f"  Điểm: {self.format_point(self.data[idx])}" for idx in cluster])
            result.append(cluster_info)
        return "\n\n".join(result)
