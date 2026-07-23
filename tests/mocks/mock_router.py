from app.interface import AppRouterInterface

class MockAppRouter(AppRouterInterface):

    def __init__(self):
        super().__init__()
        self.is_started = False
        self.is_showed_log_window = False
        self.is_closed_all = False
        self.is_hide_splash_screen = False
        self.show_log_calls = 0

    def start(self) -> None:
        """Запускает приложение (показывает главное окно)"""
        self.is_started = True

    def show_log_window(self) -> None:
        """Открывает или активирует окно логов"""
        self.is_showed_log_window = True
        self.show_log_calls += 1

    def close_all(self) -> None:
        """Закрывает все окна и завершает приложение"""
        self.is_closed_all = True

    def hide_splash_screen(self) -> None:
        """Скрывает сплэш-скрин (если есть)"""
        self.is_hide_splash_screen = True