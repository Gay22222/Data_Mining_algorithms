import tkinter as tk


def create_main_menu(scrollable_frame, root, frames, show_frame_callback):
    """
    Tạo frame menu chính.

    Parameters:
        scrollable_frame: Frame cha cho nội dung.
        root: Tkinter root window.
        frames: Dictionary chứa tất cả frames.
        show_frame_callback: Hàm callback để điều khiển hiển thị frame khác.
    """
    frame = tk.Frame(scrollable_frame, bg="#F8F9FA")

    # Tiêu đề menu chính
    tk.Label(
        frame, text="Chào mừng đến với PyDataMiner",
        font=("Arial", 24, "bold"), bg="#F8F9FA"
    ).pack(pady=30)

    # Các nút chức năng
    functions = [
        ("Tập Thô", lambda: show_frame_callback("Tập Thô")),
        ("K-Means", lambda: show_frame_callback("K-Means")),
        ("Naive Bayes", lambda: show_frame_callback("Naive Bayes")),
    ]

    for text, command in functions:
        tk.Button(
            frame, text=text, font=("Arial", 16),
            width=25, height=2, bg="#2182f0", fg="#FFFFFF", command=command
        ).pack(pady=10)

    # Nút thoát
    tk.Button(
        frame, text="Thoát", font=("Arial", 16),
        width=15, height=2, bg="#DC3545", fg="#FFFFFF", command=root.quit
    ).pack(pady=30)

    return frame
