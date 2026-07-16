from typing import Any
from abc import abstractmethod

class CounterViewInterface():
    """Интерфейс представления счетчика"""

    @abstractmethod
    def set_presenter(self, presenter: Any) -> None:
        """Устанавливает ссылку на презентер"""
        ...

    @abstractmethod
    def update_display(self, value: int) -> None:
        """Обновляет отображение значения счетчика"""
        ...

    @abstractmethod
    def set_reset_button_enabled(self, enabled: bool) -> None:
        """Включает/выключает кнопку сброса"""
        ...

    @abstractmethod
    def set_decrement_button_enabled(self, enabled: bool) -> None:
        """Включает/выключает кнопку уменьшения"""
        ...

    @abstractmethod
    def show_exit_confirmation(self) -> bool:
        """
        Показывает диалог подтверждения выхода
        Returns: True если пользователь подтвердил выход
        """
        ...


class LogViewInterface():
    """Интерфейс представления логов"""

    @abstractmethod
    def append_log(self, message: str) -> None:
        """Добавляет сообщение в лог"""
        ...