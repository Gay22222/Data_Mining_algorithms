import tkinter as tk
from tkinter import ttk


def center_frame(scroll_canvas, scrollable_frame):
    """
    Căn giữa nội dung của frame trên scroll_canvas.
    """
    canvas_width = scroll_canvas.winfo_width()
    frame_width = scrollable_frame.winfo_reqwidth()
    x_offset = max((canvas_width - frame_width) // 2, 0)
    scroll_canvas.coords("scrollable_window", x_offset, 0)



def create_scrollable_frame(root):
    """Tạo một khung Canvas cuộn được dùng chung."""
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill="both", expand=True)

    scroll_canvas = tk.Canvas(canvas_frame, bg="#F8F9FA", highlightthickness=0)
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=scroll_canvas.yview)
    scrollable_frame = tk.Frame(scroll_canvas, bg="#F8F9FA")

    scroll_canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    scroll_canvas.pack(side="left", fill="both", expand=True)
    scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="scrollable_window")

    # Cập nhật vùng cuộn khi nội dung thay đổi
    def configure_canvas(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_canvas)

    # Đảm bảo nội dung được căn giữa
    def center_frame(event=None):
        canvas_width = scroll_canvas.winfo_width()
        frame_width = scrollable_frame.winfo_reqwidth()
        x_offset = max((canvas_width - frame_width) // 2, 0)
        scroll_canvas.coords("scrollable_window", x_offset, 0)

    # Gọi ngay khi Frame được tạo (khi nội dung thay đổi lần đầu tiên)
    root.after(0, lambda: center_frame())

    # Gắn sự kiện thay đổi kích thước để giữ căn giữa
    scroll_canvas.bind("<Configure>", center_frame)

    # Xử lý sự kiện chuột lăn
    def _on_mousewheel(event):
        if event.delta:  # Windows và macOS
            scroll_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        else:  # Linux (Button-4 và Button-5)
            if event.num == 4:
                scroll_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                scroll_canvas.yview_scroll(1, "units")

    scrollable_frame.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", _on_mousewheel))
    scrollable_frame.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))

    return scroll_canvas, scrollable_frame
