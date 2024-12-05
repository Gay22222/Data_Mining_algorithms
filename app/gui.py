import tkinter as tk
from tkinter import ttk
from app.interfaces.main_menu import create_main_menu
from app.interfaces.kmeans_gui import kmeans_interface
from app.interfaces.naive_bayes_gui import naive_bayes_interface
from app.interfaces.rough_sets_gui import rough_sets_interface


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
    def center_frame(event):
        canvas_width = scroll_canvas.winfo_width()
        frame_width = scrollable_frame.winfo_reqwidth()
        x_offset = max((canvas_width - frame_width) // 2, 0)
        scroll_canvas.coords("scrollable_window", x_offset, 0)

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

    # Gắn sự kiện lăn chuột
    scrollable_frame.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", _on_mousewheel))
    scrollable_frame.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))

    # Xử lý cho Linux
    scrollable_frame.bind("<Enter>", lambda e: root.bind_all("<Button-4>", _on_mousewheel))
    scrollable_frame.bind("<Enter>", lambda e: root.bind_all("<Button-5>", _on_mousewheel))
    scrollable_frame.bind("<Leave>", lambda e: root.unbind_all("<Button-4>"))
    scrollable_frame.bind("<Leave>", lambda e: root.unbind_all("<Button-5>"))

    return scroll_canvas, scrollable_frame


def create_app():
    """
    Tạo ứng dụng PyDataMiner.
    """
    root = tk.Tk()
    root.title("PyDataMiner")
    root.geometry("1600x800")
    root.configure(bg="#F8F9FA")

    # Tạo khung cuộn
    scroll_canvas, scrollable_frame = create_scrollable_frame(root)

    # Khởi tạo các frame
    frames = {}

    # Callback để hiển thị frame
    def show_frame(frame_key):
        for frame in frames.values():
            frame.pack_forget()
        frames[frame_key].pack(fill="both", expand=True)
        scroll_canvas.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    # Thêm các frame vào dictionary
    frames["main_menu"] = create_main_menu(scrollable_frame, root, frames, show_frame)
    frames["Tập Thô"] = tk.Frame(scrollable_frame, bg="#F8F9FA")  # Placeholder
    frames["K-Means"] = tk.Frame(scrollable_frame, bg="#F8F9FA")  # Placeholder
    frames["Naive Bayes"] = tk.Frame(scrollable_frame, bg="#F8F9FA")  # Placeholder

    # Hiển thị frame menu chính
    show_frame("main_menu")

    root.mainloop()


if __name__ == "__main__":
    create_app()
