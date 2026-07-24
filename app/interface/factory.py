"""
Интерфейс фабрики для создания окон приложения.

Используется для внедрения зависимостей в AppRouter,
позволяя подменять реализацию окон для тестирования.
"""

from abc import ABC, abstractmethod
from .view import CounterViewInterface, LogViewInterface


class WindowFactoryInterface(ABC):
    """
    Интерфейс фабрики для создания окон приложения.

    Позволяет абстрагировать создание окон wxPython для обеспечения
    тестируемости и гибкости.
    """

    @abstractmethod
    def create_counter_view(self, parent, title: str) -> CounterViewInterface:
        """
        Создает главное окно приложения.

        Args:
            parent: Родительское окно (wx.Window или None).
            title: Заголовок окна.

        Returns:
            CounterViewInterface: Экземпляр главного окна.
        """
        ...

    @abstractmethod
    def create_log_view(self, parent, title: str) -> LogViewInterface:
        """
        Создает окно логов.

        Args:
            parent: Родительское окно (wx.Window или None).
            title: Заголовок окна.

        Returns:
            LogViewInterface: Экземпляр окна логов.
        """
        ...
