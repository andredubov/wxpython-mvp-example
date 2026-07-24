"""
Интерфейсы для оконных компонентов приложения.

Определяет абстрактные классы для всех оконных компонентов,
позволяя абстрагироваться от конкретной GUI-библиотеки (wxPython)
и обеспечивая тестируемость.
"""

from abc import abstractmethod
from typing import Callable, Tuple


class WindowInterface():
    """
    Базовый интерфейс для оконных компонентов.

    Предоставляет абстрактные методы для управления окном,
    скрывая детали реализации конкретной GUI-библиотеки.
    """

    @abstractmethod
    def set_size(self, size: Tuple[int, int]) -> None:
        """Устанавливает размер окна."""
        ...

    @abstractmethod
    def set_min_size(self, size: Tuple[int, int]) -> None:
        """Устанавливает минимальный размер окна."""
        ...

    @abstractmethod
    def set_position(self, position: Tuple[int, int]) -> None:
        """Устанавливает позицию окна на экране."""
        ...

    @abstractmethod
    def get_position(self) -> Tuple[int, int]:
        """Возвращает текущую позицию окна."""
        ...

    @abstractmethod
    def get_size(self) -> Tuple[int, int]:
        """Возвращает текущий размер окна."""
        ...

    @abstractmethod
    def center(self) -> None:
        """Центрирует окно на экране."""
        ...

    @abstractmethod
    def show(self) -> None:
        """Отображает окно."""
        ...

    @abstractmethod
    def raise_on_top(self) -> None:
        """Выводит окно на передний план."""
        ...

    @abstractmethod
    def destroy(self) -> None:
        """Уничтожает окно и освобождает ресурсы."""
        ...

    @abstractmethod
    def bind_close(self, handler: Callable) -> None:
        """
        Привязывает обработчик к событию закрытия окна.

        Args:
            handler: Функция-обработчик, вызываемая при закрытии окна.
        """
        ...

    @abstractmethod
    def set_title(self, title: str) -> None:
        """Устанавливает заголовок окна."""
        ...