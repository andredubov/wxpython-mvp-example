from typing import Callable
from abc import ABC, abstractmethod


class CounterModelInterface(ABC):
    """Интерфейс модели данных"""

    @abstractmethod
    def get_count(self) -> int:
        """Возвращает текущее значение счетчика"""
        ...

    @abstractmethod
    def increment(self) -> None:
        """Увеличивает счетчик на 1"""
        ...

    @abstractmethod
    def decrement(self) -> None:
        """Уменьшает счетчик на 1 (если больше 0)"""
        ...

    @abstractmethod
    def reset(self) -> None:
        """Сбрасывает счетчик на 0"""
        ...

    @abstractmethod
    def set_count(self, value: int) -> None:
        """Устанавливает конкретное значение счетчика"""
        ...

    @abstractmethod
    def subscribe(self, callback: Callable[[int, str], None]) -> None:
        """
        Подписывает callback на уведомления об изменениях
        Args:
            callback: функция, принимающая (new_value, action_description)
        """
        ...

    @abstractmethod
    def unsubscribe(self, callback: Callable[[int, str], None]) -> None:
        """Отписывает callback от уведомлений"""
        ...