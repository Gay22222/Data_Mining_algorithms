import tkinter as tk
from controllers.main_menu_controller import MainMenuController
from controllers.kmeans_controller import KMeansController
from controllers.rough_sets_controller import RoughSetsController
from controllers.naive_bayes_controller import NaiveBayesController
from controllers.discernibility_controller import DiscernibilityController
from controllers.apriori_controller import AprioriController
from models.scrollable_frame import create_scrollable_frame

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyDataMiner")
        self.root.geometry("1600x800")
        self.root.configure(bg="#F8F9FA")

        # Tạo khung cuộn
        self.scroll_canvas, self.scrollable_frame = create_scrollable_frame(self.root)

        # Quản lý frames
        self.frames = {}

        # Tạo controller cho Main Menu và K-Means
        self.main_menu_controller = MainMenuController(self)
        self.kmeans_controller = KMeansController(self)
        self.rough_sets_controller = RoughSetsController(self)
        self.naive_bayes_controller = NaiveBayesController(self)
        self.discernibility_controller = DiscernibilityController(self)
        self.apriori_controller = AprioriController(self)


    def show_frame(self, frame_key):
        """
        Hiển thị frame và cập nhật vùng cuộn nếu cần.
        """
        if frame_key not in self.frames:
            print(f"Frame '{frame_key}' không tồn tại.")
            return

        # Ẩn tất cả các frame khác
        for frame in self.frames.values():
            frame.pack_forget()

        # Hiển thị frame hiện tại
        current_frame = self.frames[frame_key]
        current_frame.pack(fill="both", expand=True)

        # Cập nhật vùng hiển thị của canvas
        self.scroll_canvas.update_idletasks()

        # Nếu quay lại main_menu, reset vùng cuộn
        if frame_key == "main_menu":
            self.scroll_canvas.configure(scrollregion=(0, 0, self.root.winfo_width(), self.root.winfo_height()))
        else:
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

        # Căn giữa nội dung frame
        self.center_frame()

    def center_frame(self):
        """
        Căn giữa nội dung trong scrollable_frame.
        """
        self.scroll_canvas.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        canvas_width = self.scroll_canvas.winfo_width()
        frame_width = self.scrollable_frame.winfo_reqwidth()
        if frame_width == 0:
            self.scrollable_frame.update_idletasks()
            frame_width = self.scrollable_frame.winfo_reqwidth()
        x_offset = max((canvas_width - frame_width) // 2, 0)
        self.scroll_canvas.coords("scrollable_window", x_offset, 0)
    
    def run(self):
        self.show_frame("main_menu")
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
