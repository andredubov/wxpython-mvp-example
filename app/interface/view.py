from typing import Any
from abc import abstractmethod
from .presenter import CounterViewPresenterInterface


class CounterViewInterface():
    """Интерфейс представления счетчика"""

    @abstractmethod
    def set_presenter(self, presenter: CounterViewPresenterInterface) -> None:
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

    @abstractmethod
    def on_increment_click(self, event):
        """
        Обрабатывает событие клика на кнопку увеличения счетчика.
        Args:
            event: событие нажатия кнопки, переданное фреймворком
        """
        ...

    @abstractmethod
    def on_decrement_click(self, event):
        """
        Обрабатывает событие клика на кнопку уменьшения счетчика.
        Args:
            event: событие нажатия кнопки, переданное фреймворком
        """
        ...

    @abstractmethod
    def on_reset_click(self, event):
        """
        Обрабатывает событие клика на кнопку сброса счетчика.
        Args:
            event: событие нажатия кнопки, переданное фреймворком
        """
        ...

    @abstractmethod
    def on_show_log_click(self, event):
        """
        Обрабатывает событие клика на кнопку отображения истории изменений.
        Args:
            event: событие нажатия кнопки, переданное фреймворком
        """
        ...


class LogViewInterface():
    """Интерфейс представления логов"""

    @abstractmethod
    def append_log(self, message: str) -> None:
        """Добавляет сообщение в лог"""
        ...