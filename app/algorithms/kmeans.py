import numpy as np
import matplotlib.pyplot as plt

# Hàm hỗ trợ định dạng tọa độ
def format_point(point):
    """
    Định dạng tọa độ dưới dạng [x.xx ; y.yy].
    """
    return f"[{point[0]:.2f} ; {point[1]:.2f}]"

# Hàm hỗ trợ làm tròn kết quả
def round_array(arr, decimals=2):
    """
    Làm tròn tất cả các phần tử trong mảng numpy đến số thập phân chỉ định.
    """
    return np.round(arr, decimals=decimals)

# Đọc dữ liệu từ file
def load_data(file_path):
    """
    Đọc dữ liệu từ file và trả về một mảng numpy.
    Mỗi dòng trong file là một điểm dữ liệu với các giá trị phân cách bởi dấu phẩy.
    """
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Chuyển mỗi dòng thành tuple các giá trị float
                point = tuple(map(float, line.strip().split(',')))
                data.append(point)
        return np.array(data)
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc file: {e}")

# Thuật toán K-Means
def kmeans(data, k, max_iters=100, tolerance=1e-4):
    """
    Thuật toán K-Means Clustering:
    - data: mảng numpy chứa dữ liệu đầu vào.
    - k: số cụm.
    - max_iters: số lần lặp tối đa.
    - tolerance: sai số để dừng thuật toán.
    """
    n_samples, n_features = data.shape
    if k <= 0 or k > n_samples:
        raise ValueError("Số cụm K phải nằm trong khoảng [1, số điểm dữ liệu].")
    
    # Khởi tạo các trọng tâm cụm (centroids) ngẫu nhiên
    np.random.seed(42)  # Đặt seed để đảm bảo kết quả lặp lại
    centroids = data[np.random.choice(n_samples, k, replace=False)]

    for _ in range(max_iters):
        # Phân cụm
        clusters = [[] for _ in range(k)]
        for idx, point in enumerate(data):
            distances = np.linalg.norm(point - centroids, axis=1)  # Tính khoảng cách Euclidean
            cluster_idx = np.argmin(distances)
            clusters[cluster_idx].append(idx)

        # Lưu lại các centroid trước đó để kiểm tra hội tụ
        previous_centroids = centroids.copy()
        
        # Cập nhật các centroid mới
        for i in range(k):
            if clusters[i]:  # Nếu cụm không rỗng
                centroids[i] = np.mean(data[clusters[i]], axis=0)
            else:  # Nếu cụm rỗng, giữ nguyên centroid
                centroids[i] = previous_centroids[i]

        # Kiểm tra hội tụ
        diff = np.linalg.norm(centroids - previous_centroids)
        if diff <= tolerance:
            break

    # Gán nhãn (labels) cho từng điểm dữ liệu
    labels = np.zeros(n_samples, dtype=int)
    for cluster_idx, cluster_points in enumerate(clusters):
        for point_idx in cluster_points:
            labels[point_idx] = cluster_idx

    # Làm tròn kết quả trọng tâm
    centroids = round_array(centroids, decimals=2)
    return centroids, labels, clusters

# Vẽ biểu đồ kết quả
def plot_clusters(data, labels, centroids):
    """
    Vẽ biểu đồ K-Means Clustering:
    - data: dữ liệu gốc.
    - labels: nhãn cụm của từng điểm dữ liệu.
    - centroids: tọa độ các centroid.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', alpha=0.6, edgecolor='k', s=50)
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='red', marker='X', label='Centroids')
    plt.title("K-Means Clustering", fontsize=16)
    plt.xlabel("X", fontsize=12)
    plt.ylabel("Y", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Tạo biểu đồ dưới dạng Figure (dùng cho giao diện Tkinter)
def generate_kmeans_plot(data, labels, centroids):
    """
    Trả về Figure của biểu đồ K-Means để nhúng vào giao diện Tkinter với nội dung Việt hóa.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', alpha=0.6, edgecolor='k', s=50)
    ax.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200, label='Trọng tâm')  # "Centroids" -> "Trọng tâm"
    ax.set_title("Biểu đồ phân cụm K-Means", fontsize=14)  # "K-Means Clustering" -> "Biểu đồ phân cụm K-Means"
    ax.set_xlabel("Trục X", fontsize=10)  # "X" -> "Trục X"
    ax.set_ylabel("Trục Y", fontsize=10)  # "Y" -> "Trục Y"
    ax.legend()
    ax.grid(True)
    return fig


# Hàm hiển thị kết quả định dạng
def display_results(centroids, clusters, data):
    """
    Hiển thị kết quả định dạng với tọa độ [x.xx ; y.yy].
    """
    result = []
    for i, cluster in enumerate(clusters):
        cluster_info = f"Cụm {i + 1} - Trọng tâm: {format_point(centroids[i])}\n"
        cluster_info += "\n".join([f"  Điểm: {format_point(data[idx])}" for idx in cluster])
        result.append(cluster_info)
    return "\n\n".join(result)
