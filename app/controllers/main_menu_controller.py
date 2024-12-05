from views.main_menu_view import MainMenuView


class MainMenuController:
    def __init__(self, app):
        self.app = app

        # Khởi tạo view
        self.view = MainMenuView(
            self.app.scrollable_frame, 
            self.app.root, 
            self.app.frames, 
            self.app.show_frame
        )

        # Đăng ký frame vào từ điển
        self.app.frames["main_menu"] = self.view
