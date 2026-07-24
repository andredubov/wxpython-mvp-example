"""
Реализация фабрики окон для приложения.

Создает реальные wxPython-окна для использования в продакшене.
"""

from app.interface import WindowFactoryInterface
from app.view import CounterView, LogView


class DefaultWindowFactory(WindowFactoryInterface):
    """
    Реализация фабрики окон, создающая реальные wxPython-окна.

    Используется в основном приложении для создания GUI-компонентов.
    """

    def create_counter_view(self, parent, title: str) -> CounterView:
        """
        Создает главное окно приложения.

        Args:
            parent: Родительское окно (wx.Window или None).
            title: Заголовок окна.

        Returns:
            CounterView: Экземпляр главного окна .
        """
        return CounterView(parent=parent, title=title)

    def create_log_view(self, parent, title: str) -> LogView:
        """
        Создает окно логов.

        Args:
            parent: Родительское окно (wx.Window или None).
            title: Заголовок окна.

        Returns:
            LogView: Экземпляр окна логов.
        """
        return LogView(parent=parent, title=title)
