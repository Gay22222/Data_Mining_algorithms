import tkinter as tk


class MainMenuView(tk.Frame):
    def __init__(self, scrollable_frame, root, frames, show_frame_callback):
        super().__init__(scrollable_frame, bg="#F8F9FA")

        # Tiêu đề menu chính
        tk.Label(
            self, text="Chào mừng đến với PyDataMiner",
            font=("Arial", 24, "bold"), bg="#F8F9FA"
        ).pack(pady=30)

        # Các nút chức năng
        buttons = [
            ("Tập Thô", lambda: show_frame_callback("Tập Thô")),
            ("K-Means", lambda: show_frame_callback("K-Means")),
            ("Naive Bayes", lambda: show_frame_callback("Naive Bayes")),
            ("Hàm phân biệt", lambda: show_frame_callback("Hàm phân biệt")),
            ("Apriori", lambda: show_frame_callback("Apriori"))
        ]

        for text, command in buttons:
            tk.Button(
                self, text=text, font=("Arial", 16),
                width=25, height=2, bg="#2182f0", fg="#FFFFFF", command=command
            ).pack(pady=10)

        # Nút thoát
        tk.Button(
            self, text="Thoát", font=("Arial", 16),
            width=15, height=2, bg="#DC3545", fg="#FFFFFF", command=root.quit
        ).pack(pady=30)
