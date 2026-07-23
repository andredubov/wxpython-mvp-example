from abc import ABC, abstractmethod


class AppRouterInterface(ABC):
    """Интерфейс роутера для навигации"""

    @abstractmethod
    def start(self) -> None:
        """Запускает приложение (показывает главное окно)"""
        ...

    @abstractmethod
    def show_log_window(self) -> None:
        """Открывает или активирует окно логов"""
        ...

    @abstractmethod
    def close_all(self) -> None:
        """Закрывает все окна и завершает приложение"""
        ...

    @abstractmethod
    def hide_splash_screen(self) -> None:
        """Скрывает сплэш-скрин (если есть)"""
        ...